# Context7 Documentation Fetching Guide

This guide explains how to fetch Context7 documentation and integrate it into the knowledge base.

## Method 1: Use Cursor Chat (Recommended)

Since Context7 MCP tools are available in Cursor, you can fetch docs directly:

### Example Prompt:

```
Fetch Context7 documentation for FastAPI (/fastapi/fastapi) with topic 
"API endpoints, routing, dependencies" and save it to docs/backend/fastapi_docs.md
```

### Step-by-Step:

1. **Ask Cursor to fetch docs** using Context7 MCP tools:
   - "Fetch Context7 docs for FastAPI"
   - "Get React documentation from Context7"
   - "Fetch pytest docs from Context7"

2. **Save the fetched content** to appropriate `docs/<domain>/` directories:
   - Backend docs → `docs/backend/`
   - Frontend docs → `docs/frontend/`
   - QA docs → `docs/qa/`

3. **Run ingestion** on the saved files:
   ```bash
   python scripts/ingest_knowledge_base.py --local-only
   ```

## Method 2: Use the Helper Script

The `scripts/fetch_context7_docs.py` script provides instructions for fetching:

```bash
# See what would be fetched
python scripts/fetch_context7_docs.py

# Fetch for specific domain
python scripts/fetch_context7_docs.py --domain backend

# Fetch specific library
python scripts/fetch_context7_docs.py --library FastAPI
```

## Method 3: Direct MCP Tool Usage

In Cursor, you can directly use Context7 MCP tools:

### Libraries to Fetch:

**Backend:**
- FastAPI: `/fastapi/fastapi` - Topic: "API endpoints, routing, dependencies"
- SQLAlchemy: `/sqlalchemy/sqlalchemy` - Topic: "ORM, database models, queries"
- Pandas: `/pandas-dev/pandas` - Topic: "Data processing, dataframes"

**Frontend:**
- React: `/reactjs/react.dev` - Topic: "Components, hooks, state management"
- Tailwind CSS: `/tailwindlabs/tailwindcss.com` - Topic: "Utility classes, styling"

**QA:**
- pytest: `/pytest-dev/pytest` - Topic: "Testing, fixtures, assertions"
- Playwright: `/microsoft/playwright-python` - Topic: "E2E testing, browser automation"

**Orchestrator:**
- LangChain: `/langchain-ai/langchain` - Topic: "Agents, tools, memory"

**Diagrammer:**
- Mermaid: `/mermaid-js/mermaid` - Topic: "Diagram syntax, flowcharts, architecture"

## Automated Integration (Future)

The ingestion script (`ingest_knowledge_base.py`) includes Context7 integration. When run from Cursor with `--use-mcp` flag, it will attempt to fetch and ingest docs automatically.

```bash
# This will attempt to use Context7 MCP tools (requires Cursor context)
python scripts/ingest_knowledge_base.py --use-mcp
```

## Recommended Workflow

1. **Start with local files** (already created):
   ```bash
   python scripts/ingest_knowledge_base.py --local-only
   ```

2. **Fetch Context7 docs via Cursor chat** for key libraries:
   - FastAPI (backend)
   - React (frontend)
   - pytest (qa)
   - LangChain (orchestrator)
   - Mermaid (diagrammer)

3. **Save fetched docs** to appropriate `docs/<domain>/` directories

4. **Re-run ingestion** to include new docs:
   ```bash
   python scripts/ingest_knowledge_base.py --local-only
   ```

5. **Test retrieval** to verify docs are accessible:
   ```python
   from agents.rag_retrieval import retrieve_knowledge
   context = retrieve_knowledge("FastAPI routing", "backend")
   print(context)
   ```

## File Naming Convention

When saving Context7 docs, use this naming:
- `docs/backend/fastapi_docs.md`
- `docs/frontend/react_docs.md`
- `docs/qa/pytest_docs.md`
- `docs/orchestrator/langchain_docs.md`
- `docs/diagrammer/mermaid_docs.md`

The ingestion script will automatically detect the domain from the directory path.

