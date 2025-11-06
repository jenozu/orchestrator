# Knowledge Base Ingestion Guide

This guide explains how to populate the domain-specific knowledge bases for the RAG system.

## Quick Start

### 1. Ingest Local Files (Recommended First Step)

The easiest way to start is to ingest existing markdown files from your `docs/` directories:

```bash
# Dry run to see what would be ingested
python scripts/ingest_knowledge_base.py --dry-run

# Actually ingest all local files
python scripts/ingest_knowledge_base.py --local-only

# Ingest only a specific domain
python scripts/ingest_knowledge_base.py --domain backend --local-only
```

### 2. Verify Ingestion

After ingestion, you can test retrieval:

```python
from agents.rag_retrieval import retrieve_knowledge

# Test retrieval
context = retrieve_knowledge(
    query="How to create API endpoints?",
    agent_domain="backend"
)
print(context)
```

## Ingestion Methods

### Method 1: Local File Ingestion (Automatic)

The script automatically:
- Scans `docs/<domain>/` directories recursively
- Finds all `.md` files
- Extracts domain from file path
- Ingests into ChromaDB with domain tags

**Example:**
- `docs/backend/api_standards.md` → domain: `backend`
- `docs/prd/scope_constraints_metrics.md` → domain: `prd`
- `docs/shared/cursor_rules.md` → domain: `shared`

### Method 2: Context7 Documentation (Integrated)

Context7 MCP integration is now available! You can fetch documentation using Cursor's Context7 MCP tools:

**Option A: Use Cursor Chat (Recommended)**
1. Ask Cursor to fetch Context7 docs: "Fetch Context7 documentation for FastAPI"
2. Save the fetched content to `docs/<domain>/` directories
3. Run local ingestion to ingest the saved files

**Option B: Use Helper Script**
```bash
# See instructions for fetching
python scripts/fetch_context7_docs.py --domain backend

# Then use Cursor chat to actually fetch the docs
```

**Option C: Automated (when run from Cursor)**
```bash
# Attempts to use Context7 MCP tools (requires Cursor context)
python scripts/ingest_knowledge_base.py --use-mcp
```

**Example Context7 Libraries to Fetch:**
- Backend: FastAPI (/fastapi/fastapi), SQLAlchemy (/sqlalchemy/sqlalchemy), Pandas (/pandas-dev/pandas)
- Frontend: React (/reactjs/react.dev), Tailwind CSS (/tailwindlabs/tailwindcss.com)
- QA: pytest (/pytest-dev/pytest), Playwright (/microsoft/playwright-python)
- Orchestrator: LangChain (/langchain-ai/langchain)
- Diagrammer: Mermaid (/mermaid-js/mermaid)

See `scripts/context7_fetch_helper.md` for detailed instructions.

### Method 3: Manual Ingestion (Programmatic)

You can also ingest documents programmatically:

```python
from agents.rag_retrieval import get_rag_store

rag_store = get_rag_store()
doc_id = rag_store.ingest_document(
    content="# Your Documentation\n\nContent here...",
    file_path="docs/backend/my_doc.md",
    domain="backend"
)
```

## Domain Mapping

Documents are automatically tagged with domains based on their path:

| Path Pattern | Domain |
|------------|--------|
| `docs/orchestrator/` | `orchestrator` |
| `docs/prd/` | `prd` |
| `docs/diagrammer/` | `diagrammer` |
| `docs/backend/` | `backend` |
| `docs/frontend/` | `frontend` |
| `docs/qa/` | `qa` |
| `docs/shared/` | `shared` |

## What Gets Ingested

### Already Created (Ready to Ingest)

These files are already in your `docs/` directories:

**Shared:**
- `docs/shared/cursor_rules.md`
- `docs/shared/naming_conventions.md`
- `docs/shared/file_structure.md`
- `docs/shared/communication_protocols.md`
- `docs/shared/memory_handling.md`

**Orchestrator:**
- `docs/orchestrator/agent_basics.md`
- `docs/orchestrator/prompt_structure.md`

**PRD:**
- `docs/prd/scope_constraints_metrics.md`
- `docs/prd.md` (existing)

**Diagrammer:**
- `docs/diagrammer/mermaid_templates.md`
- `docs/diagrammer/common_patterns.md`
- `docs/architecture.mmd` (if converted to .md)

**Backend:**
- `docs/backend/api_standards.md`
- `docs/backend/error_handling.md`

**Frontend:**
- `docs/frontend/component_patterns.md`

### External Sources (To Add)

You can add external documentation by:

1. **Downloading** relevant sections from official docs
2. **Saving** to appropriate `docs/<domain>/` directories
3. **Running** the ingestion script

**Recommended External Docs to Add:**

**Backend:**
- FastAPI official documentation sections
- SQLAlchemy ORM patterns
- API security best practices

**Frontend:**
- React component patterns
- Tailwind CSS utility reference
- Accessibility guidelines

**QA:**
- pytest fixtures and patterns
- Playwright automation guides
- Test pyramid concepts

## Troubleshooting

### RAG Store Not Initializing

- Check that `OPENAI_API_KEY` is set in environment
- Verify ChromaDB can be initialized
- Check logs for specific error messages

### No Documents Retrieved

- Run ingestion script to populate KB
- Verify documents are in correct domain directories
- Check that domain names match exactly (case-sensitive)

### Duplicate Documents

- ChromaDB uses UUIDs, so duplicates are technically possible
- Consider adding a deduplication step if needed
- Re-running ingestion won't cause issues (but may create duplicates)

## Next Steps

1. **Run initial ingestion** of local files
2. **Test retrieval** with sample queries
3. **Add external documentation** as needed
4. **Monitor agent performance** with RAG vs. without
5. **Iterate** based on what agents need

