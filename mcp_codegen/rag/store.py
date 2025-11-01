"""Vector store wrapper for RAG."""
import os
from typing import List, Dict, Any
import chromadb
from chromadb.utils import embedding_functions

from mcp_codegen.config import CHROMA_DIR, CHROMA_COLLECTION, OPENAI_API_KEY, EMBEDDING_MODEL


class RAGStore:
    """Vector store for code patterns and solutions."""
    
    def __init__(self):
        self.client = None
        self.collection = None
        self.initialized = False
    
    async def initialize(self):
        """Initialize ChromaDB client and collection."""
        if self.initialized:
            return
        
        self.client = chromadb.PersistentClient(path=str(CHROMA_DIR))
        
        embedding_fn = embedding_functions.OpenAIEmbeddingFunction(
            api_key=OPENAI_API_KEY,
            model_name=EMBEDDING_MODEL
        )
        
        self.collection = self.client.get_or_create_collection(
            name=CHROMA_COLLECTION,
            embedding_function=embedding_fn
        )
        
        self.initialized = True
    
    def add_code_example(self, code: str, metadata: Dict[str, Any]):
        """Add a code example to the store."""
        import uuid
        self.collection.add(
            documents=[code],
            metadatas=[metadata],
            ids=[str(uuid.uuid4())]
        )
    
    def retrieve_similar(self, query: str, n_results: int = 5) -> Dict[str, Any]:
        """Retrieve similar code examples."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return {
            "examples": results['documents'][0],
            "metadata": results['metadatas'][0],
            "distances": results['distances'][0]
        }

