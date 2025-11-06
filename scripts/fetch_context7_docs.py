"""Context7 Documentation Fetcher

This script fetches documentation from Context7 using MCP tools and saves it to docs/ directories.
It's designed to be run from within Cursor where MCP Context7 tools are available.

Usage:
    When run from Cursor chat, it will use the available MCP Context7 tools.
    You can also import and use this in other scripts.
"""
import logging
from pathlib import Path
from typing import Optional, Dict, List
import sys

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Context7 library mappings from ingest_knowledge_base.py
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


def fetch_and_save_context7_doc(
    lib_id: str,
    lib_name: str,
    domain: str,
    topic: str,
    output_dir: Optional[Path] = None,
    tokens: int = 5000
) -> Optional[Path]:
    """Fetch documentation from Context7 and save to file.
    
    This function is designed to be called from Cursor where MCP Context7 tools are available.
    
    Args:
        lib_id: Context7 library ID (e.g., "/fastapi/fastapi")
        lib_name: Human-readable library name
        domain: Target domain (backend, frontend, etc.)
        topic: Topic to focus documentation on
        output_dir: Directory to save docs (default: docs/<domain>/)
        tokens: Maximum tokens to fetch (default: 5000)
    
    Returns:
        Path to saved file, or None if failed
    """
    if output_dir is None:
        output_dir = Path(f"docs/{domain}")
    
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create filename from library name
    safe_name = lib_name.lower().replace(" ", "_").replace("/", "_")
    output_file = output_dir / f"{safe_name}_docs.md"
    
    logger.info(f"Fetching {lib_name} documentation...")
    logger.info(f"  Library ID: {lib_id}")
    logger.info(f"  Topic: {topic}")
    logger.info(f"  Output: {output_file}")
    
    # Note: In Cursor, you would use the MCP Context7 tools here
    # For now, this provides the structure and instructions
    
    logger.warning(
        "This script requires Cursor's MCP Context7 tools.\n"
        "To use this from Cursor chat, ask:\n"
        f"  'Fetch Context7 documentation for {lib_name} ({lib_id}) "
        f"with topic '{topic}' and save to {output_file}'\n\n"
        "Or manually fetch using Context7 MCP tools and save the content."
    )
    
    return output_file


def main():
    """Main function to fetch Context7 docs for all configured libraries."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Fetch Context7 documentation and save to docs/ directories"
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
        help="Maximum tokens to fetch per library (default: 5000)"
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
    
    logger.info(f"Will fetch {len(libraries_to_fetch)} libraries...")
    logger.info("\n" + "="*60)
    logger.info("CONTEXT7 DOCUMENTATION FETCHER")
    logger.info("="*60)
    logger.info("\nThis script provides instructions for fetching Context7 docs.")
    logger.info("To actually fetch docs, use Cursor's MCP Context7 tools.\n")
    
    for domain, lib_name, lib_id, topic in libraries_to_fetch:
        output_file = fetch_and_save_context7_doc(
            lib_id=lib_id,
            lib_name=lib_name,
            domain=domain,
            topic=topic,
            tokens=args.tokens
        )
        logger.info("")
    
    logger.info("="*60)
    logger.info("After fetching docs, run:")
    logger.info("  python scripts/ingest_knowledge_base.py --local-only")
    logger.info("="*60)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

