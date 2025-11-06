"""RAG retrieval utility for domain-specific knowledge base access."""
import os
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path

# Load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # python-dotenv not installed, skip .env loading
    pass

try:
    import chromadb
    from chromadb.utils import embedding_functions
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    chromadb = None
    embedding_functions = None

logger = logging.getLogger(__name__)

# Valid agent domains
VALID_DOMAINS = ['orchestrator', 'prd', 'diagrammer', 'backend', 'frontend', 'qa', 'shared']

# Default configuration
DEFAULT_CHROMA_DIR = Path("./chroma_db")
DEFAULT_COLLECTION = "agent_knowledge_base"
DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"
DEFAULT_TOP_K = 5


def get_openai_api_key() -> Optional[str]:
    """Get OpenAI API key from environment."""
    return os.getenv("OPENAI_API_KEY", "")


class DomainScopedRAGStore:
    """RAG store with domain-scoped retrieval for agent knowledge bases."""
    
    def __init__(
        self,
        chroma_dir: Optional[Path] = None,
        collection_name: str = DEFAULT_COLLECTION,
        embedding_model: str = DEFAULT_EMBEDDING_MODEL
    ):
        """Initialize domain-scoped RAG store.
        
        Args:
            chroma_dir: Directory for ChromaDB persistence
            collection_name: Name of the ChromaDB collection
            embedding_model: OpenAI embedding model name
        """
        if not CHROMADB_AVAILABLE:
            logger.warning("ChromaDB not available. RAG retrieval will be disabled.")
            self.client = None
            self.collection = None
            self.initialized = False
            return
        
        self.chroma_dir = chroma_dir or DEFAULT_CHROMA_DIR
        self.collection_name = collection_name
        self.embedding_model = embedding_model
        self.client = None
        self.collection = None
        self.initialized = False
    
    def initialize(self):
        """Initialize ChromaDB client and collection."""
        if not CHROMADB_AVAILABLE:
            logger.warning("ChromaDB not available. Skipping initialization.")
            return
        
        if self.initialized:
            return
        
        try:
            api_key = get_openai_api_key()
            if not api_key:
                logger.warning("OPENAI_API_KEY not set. RAG retrieval will be disabled.")
                self.initialized = False
                return
            
            self.client = chromadb.PersistentClient(path=str(self.chroma_dir))
            
            embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
                api_key=api_key,
                model_name=self.embedding_model
            )
            
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                embedding_function=embedding_fn
            )
            
            self.initialized = True
            logger.info(f"RAG store initialized with collection: {self.collection_name}")
        
        except Exception as e:
            logger.error(f"Failed to initialize RAG store: {e}")
            self.initialized = False
    
    def ingest_document(
        self,
        content: str,
        file_path: str,
        domain: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> str:
        """Ingest a document into the vector store with domain tagging.
        
        Args:
            content: Document content text
            file_path: Source file path (used to infer domain if not provided)
            domain: Agent domain (orchestrator, prd, backend, etc.)
            metadata: Additional metadata to store
            
        Returns:
            Document ID
        """
        if not self.initialized:
            self.initialize()
        
        if not self.initialized or not self.collection:
            logger.warning("RAG store not initialized. Document not ingested.")
            return ""
        
        # Extract domain from path if not provided
        if domain is None:
            domain = self._infer_domain_from_path(file_path)
        
        # Validate domain
        if domain not in VALID_DOMAINS:
            logger.warning(f"Invalid domain '{domain}'. Using 'shared' instead.")
            domain = 'shared'
        
        # Prepare metadata
        doc_metadata = {
            'domain': domain,
            'source': file_path,
            **(metadata or {})
        }
        
        # Generate document ID
        import uuid
        doc_id = str(uuid.uuid4())
        
        try:
            # Add document to collection
            self.collection.add(
                documents=[content],
                metadatas=[doc_metadata],
                ids=[doc_id]
            )
            logger.info(f"Ingested document from {file_path} with domain '{domain}'")
            return doc_id
        except Exception as e:
            logger.error(f"Failed to ingest document: {e}")
            return ""
    
    def _infer_domain_from_path(self, file_path: str) -> str:
        """Infer domain from file path."""
        file_path_lower = file_path.lower()
        
        # Check for domain in path
        for domain in VALID_DOMAINS:
            if f'docs/{domain}/' in file_path_lower or f'/docs/{domain}/' in file_path_lower:
                return domain
        
        # Default to shared
        return 'shared'
    
    def retrieve_knowledge(
        self,
        query: str,
        agent_domain: str,
        top_k: int = DEFAULT_TOP_K
    ) -> str:
        """Retrieve relevant knowledge filtered by agent domain.
        
        Retrieves documents tagged with the specified agent_domain and 'shared' domain,
        excluding documents from other agent domains.
        
        Args:
            query: Search query/question
            agent_domain: The domain of the requesting agent (e.g., 'backend', 'prd')
            top_k: Number of top documents to retrieve
            
        Returns:
            Concatenated context string from retrieved documents
        """
        if not self.initialized:
            self.initialize()
        
        if not self.initialized or not self.collection:
            logger.warning("RAG store not initialized. Returning empty context.")
            return ""
        
        # Validate agent_domain
        if agent_domain not in VALID_DOMAINS:
            raise ValueError(
                f"Invalid agent_domain: {agent_domain}. "
                f"Must be one of: {VALID_DOMAINS}"
            )
        
        try:
            # Query with domain filter: include agent_domain and 'shared'
            # ChromaDB supports metadata filtering
            where_filter = {
                "$or": [
                    {"domain": {"$eq": agent_domain}},
                    {"domain": {"$eq": "shared"}}
                ]
            }
            
            results = self.collection.query(
                query_texts=[query],
                n_results=top_k,
                where=where_filter
            )
            
            # Extract documents
            if results and results.get('documents') and len(results['documents'][0]) > 0:
                documents = results['documents'][0]
                # Concatenate into context string
                context = "\n\n".join(documents)
                
                logger.info(
                    f"Retrieved {len(documents)} documents for domain '{agent_domain}' "
                    f"with query: {query[:50]}..."
                )
                return context
            else:
                logger.info(f"No documents found for domain '{agent_domain}' with query: {query[:50]}...")
                return ""
        
        except Exception as e:
            logger.error(f"Failed to retrieve knowledge: {e}")
            return ""


# Global RAG store instance
_rag_store: Optional[DomainScopedRAGStore] = None


def get_rag_store() -> DomainScopedRAGStore:
    """Get or create the global RAG store instance."""
    global _rag_store
    if _rag_store is None:
        _rag_store = DomainScopedRAGStore()
        _rag_store.initialize()
    return _rag_store


def retrieve_knowledge(
    query: str,
    agent_domain: str,
    top_k: int = DEFAULT_TOP_K
) -> str:
    """Convenience function for retrieving domain-scoped knowledge.
    
    Args:
        query: The search query/question
        agent_domain: The domain of the requesting agent (e.g., 'backend', 'prd')
        top_k: Number of top documents to retrieve (default: 5)
    
    Returns:
        Concatenated context string from retrieved documents
    """
    rag_store = get_rag_store()
    return rag_store.retrieve_knowledge(query, agent_domain, top_k)

