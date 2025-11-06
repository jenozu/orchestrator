"""Direct ingestion of Context7 documentation - fetches and ingests in one go."""
import sys
import logging
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

sys.path.insert(0, str(Path(__file__).parent.parent))

from agents.rag_retrieval import get_rag_store

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def format_doc(lib_name, lib_id, topic, content):
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

def ingest_library(store, domain, lib_name, lib_id, topic, content):
    """Ingest a single library's documentation."""
    try:
        formatted = format_doc(lib_name, lib_id, topic, content)
        file_path = f"context7://{lib_id.replace('/', '_')}"
        
        doc_id = store.ingest_document(
            content=formatted,
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
            print(f"[OK] Ingested {lib_name} ({len(formatted)} chars)")
            return True
        else:
            print(f"[FAIL] Failed to ingest {lib_name}")
            return False
    except Exception as e:
        print(f"[ERROR] {lib_name}: {e}")
        import traceback
        traceback.print_exc()
        return False

# Libraries configuration
LIBRARIES = [
    ("backend", "FastAPI", "/fastapi/fastapi", "API endpoints, routing, dependencies"),
    ("backend", "SQLAlchemy", "/sqlalchemy/sqlalchemy", "ORM, database models, queries"),
    ("backend", "Pandas", "/pandas-dev/pandas", "Data processing, dataframes"),
    ("frontend", "React", "/reactjs/react.dev", "Components, hooks, state management"),
    ("frontend", "Tailwind CSS", "/tailwindlabs/tailwindcss.com", "Utility classes, styling"),
    ("qa", "pytest", "/pytest-dev/pytest", "Testing, fixtures, assertions"),
    ("qa", "Playwright", "/microsoft/playwright-python", "E2E testing, browser automation"),
    ("orchestrator", "LangChain", "/langchain-ai/langchain", "Agents, tools, memory"),
    ("diagrammer", "Mermaid", "/mermaid-js/mermaid", "Diagram syntax, flowcharts, architecture"),
]

def main():
    """Main function - will be called by assistant with fetched content."""
    print("="*60)
    print("CONTEXT7 DOCUMENTATION INGESTION")
    print("="*60)
    
    store = get_rag_store()
    if not store.initialized:
        print("ERROR: RAG store not initialized")
        return 1
    
    initial_count = store.collection.count() if store.collection else 0
    print(f"\n[OK] RAG Store initialized")
    print(f"[INFO] Current count: {initial_count}")
    print(f"\n[INFO] Ready to ingest {len(LIBRARIES)} libraries")
    print("[INFO] The assistant will now ingest each library with fetched content.\n")
    
    return 0

if __name__ == "__main__":
    # If run directly, just show status
    # Actual ingestion will be done by assistant calling ingest_library() for each lib
    sys.exit(main())

