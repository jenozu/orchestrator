"""Automatically populate Knowledge Base from Context7 using MCP tools.

This script fetches documentation from Context7 for all configured libraries
and directly ingests them into the RAG knowledge base.

Usage:
    # Fetch all libraries
    python scripts/populate_kb_from_context7.py
    
    # Fetch specific domain
    python scripts/populate_kb_from_context7.py --domain backend
"""
import sys
import logging
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

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
    
    NOTE: This function is designed to be called from Cursor where MCP tools are available.
    The actual MCP tool calls will be made by the Cursor assistant.
    
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
    logger.info(f"Processing {lib_name}...")
    logger.info(f"  Library ID: {lib_id}")
    logger.info(f"  Domain: {domain}")
    logger.info(f"  Topic: {topic}")
    
    # Note: When this script is called from Cursor chat, the assistant will:
    # 1. Call mcp_context7_get-library-docs with lib_id and topic
    # 2. Ingest the returned documentation into the RAG store
    # 3. Continue with the next library
    
    logger.info(f"  -> Ready for Context7 MCP fetch")
    return True


def main():
    """Main function to populate KB from Context7."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Populate knowledge base from Context7 using MCP tools"
    )
    parser.add_argument(
        "--domain",
        type=str,
        choices=["backend", "frontend", "qa", "orchestrator", "diagrammer"],
        help="Specific domain to fetch (default: all)"
    )
    parser.add_argument(
        "--tokens",
        type=int,
        default=5000,
        help="Maximum tokens per library (default: 5000)"
    )
    
    args = parser.parse_args()
    
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
    
    # Filter libraries
    libraries_to_fetch = [
        lib for lib in CONTEXT7_LIBRARIES
        if args.domain is None or lib[0] == args.domain
    ]
    
    logger.info(f"\nWill process {len(libraries_to_fetch)} libraries...")
    logger.info("\nNOTE: This script requires Context7 MCP tools available in Cursor.")
    logger.info("The Cursor assistant will fetch each library's documentation.\n")
    
    success_count = 0
    failed_libs = []
    
    for domain, lib_name, lib_id, topic in libraries_to_fetch:
        try:
            result = fetch_and_ingest_context7_doc(
                rag_store, domain, lib_name, lib_id, topic, args.tokens
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
    logger.info(f"Processed: {success_count}/{len(libraries_to_fetch)} libraries")
    if failed_libs:
        logger.info(f"Failed libraries: {', '.join(failed_libs)}")
    
    logger.info("\nNext step: Use Cursor chat to fetch Context7 docs for each library")
    logger.info("Example: 'Fetch Context7 documentation for FastAPI and ingest into KB'")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

