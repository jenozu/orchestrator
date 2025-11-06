"""Fetch Context7 Documentation and Ingest into Knowledge Base

This script uses Context7 MCP tools to fetch documentation and directly ingest it
into the RAG knowledge base. It's designed to be run from Cursor where MCP tools are available.

Usage:
    # Fetch all configured libraries
    python scripts/fetch_context7_to_kb.py
    
    # Fetch for specific domain
    python scripts/fetch_context7_to_kb.py --domain backend
    
    # Fetch specific library
    python scripts/fetch_context7_to_kb.py --library FastAPI
    
    # Dry run
    python scripts/fetch_context7_to_kb.py --dry-run
"""
import argparse
import asyncio
import logging
import sys
from pathlib import Path
from typing import Dict, Optional

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.rag_retrieval import DomainScopedRAGStore, get_rag_store

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Context7 library mappings
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


async def fetch_and_ingest_context7_doc(
    rag_store: DomainScopedRAGStore,
    domain: str,
    lib_name: str,
    lib_id: str,
    topic: str,
    tokens: int = 5000,
    dry_run: bool = False
) -> bool:
    """Fetch Context7 documentation and ingest into RAG store.
    
    This function uses Context7 MCP tools which are available when run from Cursor.
    
    Args:
        rag_store: Initialized RAG store
        domain: Agent domain
        lib_name: Library name
        lib_id: Context7 library ID
        topic: Topic to focus on
        tokens: Maximum tokens to fetch
        dry_run: If True, only report what would be done
    
    Returns:
        True if successful, False otherwise
    """
    if dry_run:
        logger.info(f"[DRY RUN] Would fetch: {lib_name} ({lib_id})")
        logger.info(f"  Domain: {domain}")
        logger.info(f"  Topic: {topic}")
        logger.info(f"  Tokens: {tokens}")
        return True
    
    logger.info(f"Fetching {lib_name} documentation...")
    logger.info(f"  Library ID: {lib_id}")
    logger.info(f"  Domain: {domain}")
    logger.info(f"  Topic: {topic}")
    
    try:
        # Note: In Cursor, we would call the MCP Context7 tools here
        # Since this script is run from Cursor, the MCP tools should be available
        # However, direct Python script execution doesn't have MCP access
        
        # For now, we'll provide instructions and a way to manually fetch
        logger.warning(
            "⚠️  Direct MCP Context7 tool access requires Cursor context.\n"
            "To fetch and ingest Context7 docs:\n"
            f"  1. In Cursor chat, ask: 'Fetch Context7 documentation for {lib_name} ({lib_id}) "
            f"with topic {topic}'\n"
            f"  2. Save the fetched content to docs/{domain}/{lib_name.lower().replace(' ', '_')}_docs.md\n"
            f"  3. Run: python scripts/ingest_knowledge_base.py --local-only\n\n"
            "Or use the helper function below to fetch via Cursor chat."
        )
        
        # Return False to indicate manual intervention needed
        return False
        
    except Exception as e:
        logger.error(f"Error fetching {lib_name}: {e}")
        return False


async def fetch_via_cursor_mcp(lib_id: str, topic: str, tokens: int = 5000) -> Optional[str]:
    """Fetch documentation using Context7 MCP tools.
    
    This function is designed to be called from Cursor where MCP tools are available.
    When called from Cursor chat, you can use the MCP Context7 tools directly.
    
    Args:
        lib_id: Context7 library ID
        topic: Topic to focus on
        tokens: Maximum tokens
    
    Returns:
        Documentation content or None
    """
    # This would use mcp_context7_get-library-docs when called from Cursor
    # For now, return None to indicate manual fetching is needed
    return None


async def main():
    """Main function."""
    parser = argparse.ArgumentParser(
        description="Fetch Context7 documentation and ingest into knowledge base"
    )
    parser.add_argument(
        "--domain",
        type=str,
        choices=["backend", "frontend", "qa", "orchestrator", "diagrammer"],
        help="Specific domain to fetch (default: all)"
    )
    parser.add_argument(
        "--library",
        type=str,
        help="Specific library name to fetch (e.g., 'FastAPI')"
    )
    parser.add_argument(
        "--tokens",
        type=int,
        default=5000,
        help="Maximum tokens per library (default: 5000)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be fetched without actually fetching"
    )
    
    args = parser.parse_args()
    
    # Filter libraries
    libraries_to_fetch = [
        lib for lib in CONTEXT7_LIBRARIES
        if (args.domain is None or lib[0] == args.domain)
        and (args.library is None or args.library.lower() in lib[1].lower())
    ]
    
    if not libraries_to_fetch:
        logger.warning("No libraries found matching criteria")
        return 1
    
    # Initialize RAG store
    if not args.dry_run:
        logger.info("Initializing RAG store...")
        rag_store = get_rag_store()
        
        if not rag_store.initialized:
            logger.error("Failed to initialize RAG store. Check OPENAI_API_KEY.")
            return 1
    else:
        rag_store = None
    
    logger.info(f"\n{'='*60}")
    logger.info("CONTEXT7 DOCUMENTATION FETCHER & INGESTER")
    logger.info(f"{'='*60}\n")
    logger.info(f"Will process {len(libraries_to_fetch)} libraries...\n")
    
    success_count = 0
    for domain, lib_name, lib_id, topic in libraries_to_fetch:
        if rag_store:
            result = await fetch_and_ingest_context7_doc(
                rag_store, domain, lib_name, lib_id, topic, args.tokens, args.dry_run
            )
            if result:
                success_count += 1
        else:
            # Dry run
            await fetch_and_ingest_context7_doc(
                None, domain, lib_name, lib_id, topic, args.tokens, True
            )
            success_count += 1
        logger.info("")
    
    logger.info(f"{'='*60}")
    if args.dry_run:
        logger.info(f"DRY RUN: Would process {success_count} libraries")
        logger.info("\nTo actually fetch docs, use Cursor chat with Context7 MCP tools:")
        logger.info("  Example: 'Fetch Context7 documentation for FastAPI'")
    else:
        logger.info(f"Processed {success_count}/{len(libraries_to_fetch)} libraries")
        logger.info("\n💡 Tip: Use Cursor chat to fetch Context7 docs, then save to docs/ directories")
        logger.info("   Then run: python scripts/ingest_knowledge_base.py --local-only")
    logger.info(f"{'='*60}")
    
    return 0


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))

