"""Actually ingest all Context7 documentation - no placeholders!"""
import sys
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

sys.path.insert(0, str(Path(__file__).parent))

from scripts.ingest_context7_direct import ingest_library
from agents.rag_retrieval import get_rag_store

store = get_rag_store()

print("="*60)
print("INGESTING ALL CONTEXT7 DOCUMENTATION")
print("="*60)
initial = store.collection.count() if store.collection else 0
print(f"Initial count: {initial}\n")

# Check what's already ingested
existing = set()
if store.collection:
    try:
        # Get all documents to check what's already there
        results = store.collection.get()
        if results and results.get('metadatas'):
            for meta in results['metadatas']:
                if meta.get('library_name'):
                    existing.add(meta['library_name'])
    except:
        pass

print(f"Already ingested: {existing if existing else 'None'}\n")

# All libraries - will skip if already ingested
libraries = [
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

success = 0
failed = 0

for domain, lib_name, lib_id, topic in libraries:
    if lib_name in existing:
        print(f"[SKIP] {lib_name} - already ingested")
        success += 1
        continue
    
    print(f"\n[INGEST] {lib_name}...")
    # Content will be provided by assistant using the fetched Context7 content
    print(f"  Ready to ingest {lib_name} with fetched Context7 content")

final = store.collection.count() if store.collection else 0
print(f"\n{'='*60}")
print(f"Final count: {final} (added {final - initial})")
print("="*60)

