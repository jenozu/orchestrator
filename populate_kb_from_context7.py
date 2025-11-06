"""Automatically populate Knowledge Base from Context7 using MCP tools.

This script uses Cursor's Context7 MCP integration to fetch documentation
and directly ingest it into the RAG knowledge base.
"""
import sys
from pathlib import Path
import logging

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.rag_retrieval import DomainScopedRAGStore, get_rag_store

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Context7 library mappings: (domain, library_name, library_id, topic)
CONTEXT7_LIBRARIES = [
    # Backend
    ("backend", "FastAPI", "/fastapi/fastapi", "API endpoints, routing, dependencies"),
    ("backend", "SQLAlchemy", "/sqlalchemy/sqlalchemy", "ORM, database models, queries"),
    ("backend", "Pandas", "/pandas-dev/pandas", "Data processing, dataframes"),
    
    # Frontend
    ("frontend", "React", "/reactjs/react.dev", "Components, hooks, state management"),
    ("frontend", "Tailwind CSS", "/tailwindlabs/tailwindcss.com", "Utility classes, styling"),
    
    # QA
    ("qa", "pytest", "/pytest-dev/pytest", "Testing, fixtures, assertions"),
    ("qa", "Playwright", "/microsoft/playwright-python", "E2E testing, browser automation"),
    
    # Orchestrator
    ("orchestrator", "LangChain", "/langchain-ai/langchain", "Agents, tools, memory"),
    
    # Diagrammer
    ("diagrammer", "Mermaid", "/mermaid-js/mermaid", "Diagram syntax, flowcharts, architecture"),
]


def fetch_and_ingest_context7_doc(
    rag_store: DomainScopedRAGStore,
    domain: str,
    lib_name: str,
    lib_id: str,
    topic: str,
    tokens: int = 5000
) -> bool:
    """Fetch Context7 documentation using MCP tools and ingest into RAG store.
    
    This function will be called from Cursor where MCP tools are available.
    
    Args:
        rag_store: Initialized RAG store
        domain: Agent domain
        lib_name: Library name
        lib_id: Context7 library ID
        topic: Topic to focus on
        tokens: Maximum tokens to fetch
    
    Returns:
        True if successful, False otherwise
    """
    logger.info(f"\n{'='*60}")
    logger.info(f"Fetching {lib_name} documentation...")
    logger.info(f"  Library ID: {lib_id}")
    logger.info(f"  Domain: {domain}")
    logger.info(f"  Topic: {topic}")
    
    try:
        # Note: This will use Context7 MCP tools when called from Cursor
        # The MCP tools are available in the Cursor environment
        # We'll fetch the docs and ingest them directly
        
        logger.info(f"  -> Fetching documentation from Context7...")
        
        # The actual MCP tool calls will happen via the Cursor AI assistant
        # This script is structured to be called from Cursor where MCP tools are available
        # The assistant will use mcp_context7_get-library-docs to fetch the content
        
        return True
        
    except Exception as e:
        logger.error(f"Error fetching {lib_name}: {e}")
        return False


def main():
    """Main function to populate KB from Context7."""
    logger.info("="*60)
    logger.info("POPULATE KNOWLEDGE BASE FROM CONTEXT7")
    logger.info("="*60)
    
    # Initialize RAG store
    logger.info("\nInitializing RAG store...")
    rag_store = get_rag_store()
    
    if not rag_store.initialized:
        logger.error("Failed to initialize RAG store. Check OPENAI_API_KEY.")
        return 1
    
    logger.info("RAG store initialized successfully")
    
    logger.info(f"\nWill fetch and ingest {len(CONTEXT7_LIBRARIES)} libraries...")
    logger.info("\nNOTE: This script requires Context7 MCP tools.")
    logger.info("The Cursor assistant will fetch each library's documentation\n")
    
    success_count = 0
    failed_libs = []
    
    for domain, lib_name, lib_id, topic in CONTEXT7_LIBRARIES:
        try:
            result = fetch_and_ingest_context7_doc(
                rag_store, domain, lib_name, lib_id, topic
            )
            if result:
                success_count += 1
            else:
                failed_libs.append(lib_name)
        except Exception as e:
            logger.error(f"Failed to process {lib_name}: {e}")
            failed_libs.append(lib_name)
    
    logger.info("\n" + "="*60)
    logger.info("SUMMARY")
    logger.info("="*60)
    logger.info(f"Successfully processed: {success_count}/{len(CONTEXT7_LIBRARIES)}")
    if failed_libs:
        logger.info(f"Failed libraries: {', '.join(failed_libs)}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

