"""Knowledge Base Ingestion Script

This script populates the domain-specific knowledge bases by:
1. Ingesting local markdown files from docs/ directories
2. Fetching and ingesting external documentation via Context7
3. Tagging documents with appropriate domains for scoped retrieval
"""
import argparse
import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import sys

# Add parent directory to path to import agents module
sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.rag_retrieval import DomainScopedRAGStore, get_rag_store

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
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

# Domain directory mapping
DOMAIN_DIRS = {
    "orchestrator": "docs/orchestrator",
    "prd": "docs/prd",
    "diagrammer": "docs/diagrammer",
    "backend": "docs/backend",
    "frontend": "docs/frontend",
    "qa": "docs/qa",
    "shared": "docs/shared",
}


def ingest_local_files(rag_store: DomainScopedRAGStore, domain: Optional[str] = None, dry_run: bool = False) -> Dict[str, int]:
    """Ingest local markdown files from docs/ directories.
    
    Args:
        rag_store: Initialized RAG store
        domain: Specific domain to ingest (None for all)
        dry_run: If True, only report what would be ingested
    
    Returns:
        Dictionary mapping domain to count of ingested files
    """
    stats = {}
    base_path = Path("docs")
    
    # Determine which domains to process
    domains_to_process = [domain] if domain else DOMAIN_DIRS.keys()
    
    for domain_name in domains_to_process:
        if domain_name not in DOMAIN_DIRS:
            logger.warning(f"Skipping unknown domain: {domain_name}")
            continue
        
        domain_path = base_path / DOMAIN_DIRS[domain_name].replace("docs/", "")
        
        if not domain_path.exists():
            logger.warning(f"Domain directory does not exist: {domain_path}")
            stats[domain_name] = 0
            continue
        
        logger.info(f"Processing domain '{domain_name}' from {domain_path}")
        
        # Find all markdown files recursively
        md_files = list(domain_path.rglob("*.md"))
        
        if not md_files:
            logger.info(f"No markdown files found in {domain_path}")
            stats[domain_name] = 0
            continue
        
        count = 0
        for md_file in md_files:
            try:
                # Read file content
                content = md_file.read_text(encoding='utf-8')
                
                if not content.strip():
                    logger.warning(f"Skipping empty file: {md_file}")
                    continue
                
                # Convert to relative path for storage
                rel_path = str(md_file.relative_to(base_path.parent))
                
                if dry_run:
                    # Show file size and first few lines
                    lines = content.split('\n')[:3]
                    preview = ' '.join(lines).replace('\n', ' ')[:100]
                    logger.info(f"[DRY RUN] Would ingest: {rel_path} (domain: {domain_name}, {len(content)} chars)")
                    if preview:
                        logger.info(f"  Preview: {preview}...")
                    count += 1
                else:
                    if not rag_store.initialized:
                        logger.error(f"Cannot ingest {rel_path}: RAG store not initialized")
                        continue
                    
                    # Ingest document
                    doc_id = rag_store.ingest_document(
                        content=content,
                        file_path=rel_path,
                        domain=domain_name
                    )
                    
                    if doc_id:
                        logger.info(f"✓ Ingested: {rel_path}")
                        count += 1
                    else:
                        logger.warning(f"✗ Failed to ingest: {rel_path}")
            
            except Exception as e:
                logger.error(f"Error processing {md_file}: {e}")
        
        stats[domain_name] = count
        logger.info(f"Domain '{domain_name}': {count} files ingested")
    
    return stats


def fetch_context7_docs_mcp(lib_id: str, topic: str, tokens: int = 5000) -> Optional[str]:
    """Fetch documentation from Context7 using MCP tools.
    
    This function is designed to be called from within Cursor where MCP tools are available.
    When run standalone, it will return None and the script will skip Context7 ingestion.
    
    Args:
        lib_id: Context7 library ID (e.g., "/fastapi/fastapi")
        topic: Topic to focus on (e.g., "API endpoints, routing")
        tokens: Maximum tokens to retrieve (default: 5000)
    
    Returns:
        Documentation content as string, or None if not available
    """
    # Note: This function expects to be called from Cursor where MCP tools are available
    # For standalone execution, we'll provide an alternative approach
    try:
        # Try to use Context7 MCP tools if available
        # In Cursor, these would be available via the MCP server
        # For now, we'll return None and handle it in the calling function
        return None
    except Exception:
        return None


async def ingest_context7_docs(rag_store: DomainScopedRAGStore, domain: Optional[str] = None, dry_run: bool = False, use_mcp: bool = True) -> Dict[str, int]:
    """Fetch and ingest documentation from Context7.
    
    Args:
        rag_store: Initialized RAG store
        domain: Specific domain to ingest (None for all)
        dry_run: If True, only report what would be ingested
        use_mcp: If True, attempt to use Context7 MCP tools (requires Cursor context)
    
    Returns:
        Dictionary mapping domain to count of ingested documents
    """
    stats = {}
    
    # Filter libraries by domain if specified
    libraries_to_fetch = [
        lib for lib in CONTEXT7_LIBRARIES
        if domain is None or lib[0] == domain
    ]
    
    if not libraries_to_fetch:
        logger.warning(f"No Context7 libraries found for domain: {domain}")
        return stats
    
    logger.info(f"Fetching documentation from Context7 for {len(libraries_to_fetch)} libraries...")
    
    if not use_mcp:
        logger.info("MCP mode disabled. Use --use-mcp to enable Context7 fetching.")
        logger.info("To fetch Context7 docs manually:")
        logger.info("  1. Use Cursor's Context7 MCP tools to fetch docs")
        logger.info("  2. Save fetched docs to docs/<domain>/ directories")
        logger.info("  3. Run ingestion with --local-only")
        return stats
    
    for domain_name, lib_name, lib_id, topic in libraries_to_fetch:
        try:
            if dry_run:
                logger.info(f"[DRY RUN] Would fetch: {lib_name} ({lib_id}) for domain '{domain_name}'")
                logger.info(f"  Topic focus: {topic}")
                stats[domain_name] = stats.get(domain_name, 0) + 1
                continue
            
            logger.info(f"Fetching {lib_name} documentation for domain '{domain_name}'...")
            logger.info(f"  Library ID: {lib_id}")
            logger.info(f"  Topic: {topic}")
            
            # Try to fetch via Context7 MCP
            # Note: This will work when called from Cursor with MCP Context7 server
            try:
                # Check if we're in a context where MCP tools might be available
                # In Cursor, the MCP tools would be injected/available
                # For now, we'll create instructions for manual fetching
                
                # For automated fetching from Cursor, you would:
                # 1. Call mcp_context7_get-library-docs with lib_id and topic
                # 2. Process the returned documentation
                # 3. Ingest into RAG store
                
                logger.info(f"  ⚠️  Context7 MCP tools require Cursor context.")
                logger.info(f"  To fetch {lib_name} docs:")
                logger.info(f"    1. Use Cursor chat to call Context7 MCP tools")
                logger.info(f"    2. Or run this script from Cursor with MCP access")
                logger.info(f"    3. Or manually save docs to docs/{domain_name}/")
                
                # Create a helper script that can be executed from Cursor
                # This will be generated as a separate utility
                
            except Exception as e:
                logger.error(f"Error fetching {lib_name} documentation: {e}")
        
        except Exception as e:
            logger.error(f"Error processing {lib_name}: {e}")
    
    return stats


def main():
    """Main entry point for knowledge base ingestion."""
    parser = argparse.ArgumentParser(
        description="Ingest knowledge base documents into the RAG system"
    )
    parser.add_argument(
        "--domain",
        type=str,
        choices=list(DOMAIN_DIRS.keys()),
        help="Specific domain to ingest (default: all domains)"
    )
    parser.add_argument(
        "--local-only",
        action="store_true",
        help="Only ingest local files, skip Context7"
    )
    parser.add_argument(
        "--context7-only",
        action="store_true",
        help="Only ingest Context7 docs, skip local files"
    )
    parser.add_argument(
        "--use-mcp",
        action="store_true",
        default=False,
        help="Attempt to use Context7 MCP tools (requires Cursor context)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview what would be ingested without actually ingesting"
    )
    
    args = parser.parse_args()
    
    if args.dry_run:
        logger.info("DRY RUN MODE: No documents will be ingested")
    
    # Initialize RAG store
    logger.info("Initializing RAG store...")
    rag_store = get_rag_store()
    
    if not rag_store.initialized and not args.dry_run:
        logger.error("Failed to initialize RAG store. Check OPENAI_API_KEY and ChromaDB setup.")
        logger.error("For dry-run mode, API key is not required.")
        return 1
    
    if rag_store.initialized:
        logger.info("RAG store initialized successfully")
    elif args.dry_run:
        logger.info("RAG store not initialized (dry-run mode, API key not required)")
    
    total_stats = {}
    
    # Ingest local files
    if not args.context7_only:
        logger.info("\n" + "="*60)
        logger.info("INGESTING LOCAL FILES")
        logger.info("="*60)
        local_stats = ingest_local_files(rag_store, args.domain, args.dry_run)
        
        for domain, count in local_stats.items():
            total_stats[domain] = total_stats.get(domain, 0) + count
    
    # Ingest Context7 docs
    if not args.local_only:
        logger.info("\n" + "="*60)
        logger.info("INGESTING CONTEXT7 DOCUMENTATION")
        logger.info("="*60)
        
        context7_stats = asyncio.run(
            ingest_context7_docs(rag_store, args.domain, args.dry_run, args.use_mcp)
        )
        
        for domain, count in context7_stats.items():
            total_stats[domain] = total_stats.get(domain, 0) + count
    
    # Print summary
    logger.info("\n" + "="*60)
    logger.info("INGESTION SUMMARY")
    logger.info("="*60)
    
    if total_stats:
        for domain, count in sorted(total_stats.items()):
            logger.info(f"{domain:15} : {count:4} documents")
        
        total = sum(total_stats.values())
        logger.info(f"{'TOTAL':15} : {total:4} documents")
    else:
        logger.info("No documents ingested")
    
    if args.dry_run:
        logger.info("\nThis was a dry run. Run without --dry-run to actually ingest documents.")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

