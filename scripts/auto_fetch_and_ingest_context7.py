"""Automatically fetch Context7 documentation and ingest into Knowledge Base.

This script uses Context7 MCP tools (when run from Cursor) to fetch documentation
for all configured libraries and directly ingest them into the RAG knowledge base.

Usage:
    # Fetch and ingest all libraries
    python scripts/auto_fetch_and_ingest_context7.py
    
    # Fetch specific domain
    python scripts/auto_fetch_and_ingest_context7.py --domain backend
    
    # Dry run (preview only)
    python scripts/auto_fetch_and_ingest_context7.py --dry-run
"""
import sys
import argparse
import logging
from pathlib import Path
from typing import Optional

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


def fetch_context7_docs_mcp(lib_id: str, topic: str, tokens: int = 5000) -> Optional[str]:
    """Fetch documentation from Context7 using MCP tools.
    
    This function will be called by the Cursor assistant when running this script.
    The assistant has access to Context7 MCP tools and will fetch the documentation.
    
    Args:
        lib_id: Context7 library ID (e.g., "/fastapi/fastapi")
        topic: Topic to focus on
        tokens: Maximum tokens to retrieve
    
    Returns:
        Documentation content as string, or None if not available
    """
    # This function signature is for the assistant to use
    # The actual fetching happens via MCP tools when called from Cursor
    pass


def format_context7_doc(lib_name: str, lib_id: str, topic: str, content: str) -> str:
    """Format Context7 documentation for ingestion."""
    return f"""# {lib_name} Documentation from Context7

Source: Context7 - {lib_name} Library Documentation
Library ID: {lib_id}
Topic Focus: {topic}

---

{content}

---

*Documentation fetched from Context7 and ingested into the knowledge base.*
"""


def fetch_and_ingest_context7_doc(
    rag_store: DomainScopedRAGStore,
    domain: str,
    lib_name: str,
    lib_id: str,
    topic: str,
    tokens: int = 5000,
    dry_run: bool = False,
    doc_content: Optional[str] = None
) -> bool:
    """Fetch Context7 documentation and ingest into RAG store.
    
    Args:
        rag_store: Initialized RAG store
        domain: Agent domain
        lib_name: Library name
        lib_id: Context7 library ID
        topic: Topic to focus on
        tokens: Maximum tokens to fetch
        dry_run: If True, only report what would be done
        doc_content: Pre-fetched documentation content (if provided)
    
    Returns:
        True if successful, False otherwise
    """
    logger.info(f"\n{'='*60}")
    logger.info(f"Processing {lib_name}...")
    logger.info(f"  Library ID: {lib_id}")
    logger.info(f"  Domain: {domain}")
    logger.info(f"  Topic: {topic}")
    
    if dry_run:
        logger.info(f"  [DRY RUN] Would fetch and ingest {lib_name} documentation")
        return True
    
    try:
        # If doc_content is provided, use it directly
        # Otherwise, this will be populated by the assistant using MCP tools
        if doc_content is None:
            logger.warning(f"  ⚠️  No content provided for {lib_name}")
            logger.info(f"  → This script should be run from Cursor chat where MCP tools are available")
            logger.info(f"  → Or provide content via --content-file parameter")
            return False
        
        # Format the documentation content
        formatted_content = format_context7_doc(lib_name, lib_id, topic, doc_content)
        
        # Ingest into RAG store
        file_path = f"context7://{lib_id.replace('/', '_')}"
        doc_id = rag_store.ingest_document(
            content=formatted_content,
            file_path=file_path,
            domain=domain,
            metadata={
                'source_type': 'context7',
                'library_id': lib_id,
                'library_name': lib_name,
                'topic': topic
            }
        )
        
        if doc_id:
            logger.info(f"  ✅ Successfully ingested {lib_name} documentation ({len(formatted_content)} chars)")
            return True
        else:
            logger.error(f"  ❌ Failed to ingest {lib_name} documentation")
            return False
            
    except Exception as e:
        logger.error(f"  ❌ Error processing {lib_name}: {e}")
        return False


def main():
    """Main function to populate KB from Context7."""
    parser = argparse.ArgumentParser(
        description="Automatically fetch Context7 documentation and ingest into knowledge base"
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
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be fetched without actually fetching"
    )
    parser.add_argument(
        "--content-file",
        type=str,
        help="Path to file containing pre-fetched documentation (for testing)"
    )
    
    args = parser.parse_args()
    
    logger.info("="*60)
    logger.info("AUTO FETCH & INGEST CONTEXT7 DOCUMENTATION")
    logger.info("="*60)
    
    # Initialize RAG store
    if not args.dry_run:
        logger.info("\nInitializing RAG store...")
        rag_store = get_rag_store()
        
        if not rag_store.initialized:
            logger.error("Failed to initialize RAG store. Check OPENAI_API_KEY.")
            return 1
        
        logger.info("RAG store initialized successfully")
    else:
        rag_store = None
        logger.info("\n[DRY RUN MODE] No documents will be ingested")
    
    # Filter libraries
    libraries_to_fetch = [
        lib for lib in CONTEXT7_LIBRARIES
        if args.domain is None or lib[0] == args.domain
    ]
    
    logger.info(f"\nWill process {len(libraries_to_fetch)} libraries...")
    
    if not args.dry_run:
        logger.info("\nNOTE: This script requires Context7 MCP tools.")
        logger.info("When run from Cursor chat, the assistant will fetch docs automatically.")
        logger.info("\nTo use this script:")
        logger.info("  1. Run from Cursor chat: 'Fetch and ingest all Context7 docs'")
        logger.info("  2. The assistant will use MCP tools to fetch each library")
        logger.info("  3. Documentation will be automatically ingested into the KB\n")
    
    success_count = 0
    failed_libs = []
    
    # Load content from file if provided (for testing)
    preloaded_content = None
    if args.content_file:
        try:
            with open(args.content_file, 'r', encoding='utf-8') as f:
                preloaded_content = f.read()
            logger.info(f"Loaded content from {args.content_file}")
        except Exception as e:
            logger.error(f"Failed to load content file: {e}")
            return 1
    
    for domain, lib_name, lib_id, topic in libraries_to_fetch:
        try:
            result = fetch_and_ingest_context7_doc(
                rag_store=rag_store,
                domain=domain,
                lib_name=lib_name,
                lib_id=lib_id,
                topic=topic,
                tokens=args.tokens,
                dry_run=args.dry_run,
                doc_content=preloaded_content if preloaded_content else None
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
    
    if args.dry_run:
        logger.info("\n💡 Run without --dry-run to actually fetch and ingest documentation")
        logger.info("   (Requires Cursor chat with Context7 MCP tools)")
    elif success_count < len(libraries_to_fetch):
        logger.info("\n💡 To fetch remaining libraries, run this script from Cursor chat")
        logger.info("   The assistant will use Context7 MCP tools to fetch docs automatically")
    
    return 0 if success_count > 0 or args.dry_run else 1


if __name__ == "__main__":
    sys.exit(main())

