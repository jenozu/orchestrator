# Parallel Agent Build System

A system for orchestrating multiple specialized SLM-backed agents that run in parallel to build out projects, using Cursor, LangGraph, Git worktrees, and retrieval-augmented generation (RAG).

## Overview

This orchestrator coordinates multiple subagents to:
1. **Generate PRDs** from simple ideas (NEW!)
2. Create MVP/PRD summaries
3. Generate Mermaid architecture diagrams
4. Execute step-by-step plans following a master task list
5. Apply Cursor rules and leverage MCP tools
6. Use specialized SLMs for each task
7. Group edits for Cursor's "Apply All" workflow
8. **Learn and improve over time** with persistent memory

## Architecture

```
Users → Orchestrator → Subagents (PRD, Diagrammer, Backend, Frontend, QA)
                      ↓
                  Vector Store (RAG)
                  Git Worktrees (parallelism)
                  Cursor Apply All (batch edits)
```

## Quick Start

### Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Verify installation
pytest
```

### Create a Git Worktree for Parallel Work

```bash
# Bash
./scripts/worktrees.sh create feature/my-feature

# PowerShell
powershell -File scripts/worktrees.ps1 create feature/my-feature
```

### Run the Orchestrator

```python
from agents.orchestrator import Orchestrator

orch = Orchestrator()
orch.build_graph()
result = orch.run_once({"initial": "state"})
```

## Project Structure

```
.
├── agents/
│   ├── orchestrator.py      # Main orchestrator with LangGraph
│   ├── apply_all.py          # Batch edit proposal system
│   ├── logging.py            # Run logs, task tracker, memory
│   ├── learning_memory.py    # Persistent learning system
│   ├── subagents/            # Specialized agent implementations
│   │   ├── prd.py
│   │   ├── diagrammer.py
│   │   ├── backend.py
│   │   └── frontend.py
│   └── prompts/              # Mission prompts for each agent
├── mcp_codegen/             # RAG + Learning MCP Server
│   ├── server.py            # MCP server
│   ├── agents/              # Codegen agents
│   ├── tools/               # MCP tools
│   └── rag/                 # RAG system
├── docs/
│   ├── prd.md               # Product requirements template
│   ├── architecture.mmd     # System architecture diagram
│   ├── tasks.md             # Master task list
│   ├── RAG_MCP_GUIDE.md     # RAG MCP implementation
│   ├── LEARNING_MEMORY_GUIDE.md  # Learning system guide
│   └── worktrees.md         # Worktree usage guide
├── .cursor/
│   ├── rules.md             # Cursor coding standards
│   └── mcp.json             # MCP tool configuration
├── .github/
│   └── workflows/
│       └── ci.yml           # CI pipeline
├── scripts/
│   ├── worktrees.sh         # Bash worktree helper
│   └── worktrees.ps1        # PowerShell worktree helper
└── tests/
    └── test_sanity.py       # Basic sanity tests
```

## Features

### Orchestrator
- Task DAG execution with dependency resolution
- Parallel subagent dispatch
- Integration with LangGraph for state management

### Subagents
- **PRD Agent**: Drafts product requirements
- **Diagrammer Agent**: Creates Mermaid architecture diagrams
- **Backend Agent**: Scaffolds/modifies backend endpoints
- **Frontend Agent**: Builds UI components

### RAG (Retrieval-Augmented Generation)
- ✅ ChromaDB vector store with embeddings
- ✅ Ingestion pipelines for code, docs, PRs, CI logs
- ✅ Branch-local retrieval policies
- ✅ Deep semantic search on code patterns

### Learning & Memory
- ✅ **Persistent learning system** with LangGraph Store
- ✅ **Semantic search** across learned solutions
- ✅ **Success rate tracking** for continuous improvement
- ✅ **Automatic learning** from successful fixes
- ✅ **Self-improving debugger** that gets smarter over time

### Observability
- Structured run logging
- Task tracker with dependency management
- Memory store for orchestration state

### Cursor Integration
- Rules for coding standards and reviews
- MCP filesystem tools
- Batch edit proposals for "Apply All"
- **Learning-enabled MCP tools** (search_learned_solutions, get_learning_stats)
- **PRD generation tool** (create_prd) for generating requirements from ideas

## Development

### Adding a New Subagent

1. Create `agents/subagents/my_agent.py`:

```python
from typing import Dict, Any

def run_task(inputs: Dict[str, Any]) -> Dict[str, Any]:
    return {"status": "completed", "outputs": ...}
```

2. Add mission prompt to `agents/prompts/my_agent.md`
3. Register in orchestrator graph

### Customizing Cursor Rules

Edit `.cursor/rules.md` to set project-specific coding standards, review gates, and agent guidelines.

### MCP Configuration

Configure MCP tools in `.cursor/mcp.json`. See [Cursor MCP docs](https://cursor.com/docs/context/mcp).

### Learning System

Enable persistent learning with LangGraph Store. See `docs/LEARNING_MEMORY_GUIDE.md` for implementation details.

## CI/CD

CI runs on every push and PR:
- Lint Python files
- Run pytest suite
- Requires passing tests before merge

See `.github/workflows/ci.yml` for details.

## References

- [Cursor Worktrees](https://cursor.com/docs/configuration/worktrees)
- [Cursor GitHub Integration](https://cursor.com/docs/integrations/github)
- [Cursor MCP](https://cursor.com/docs/context/mcp)
- [Cursor Rules](https://cursor.com/docs/context/rules)
- [NVIDIA SLM Agents](https://research.nvidia.com/labs/lpr/slm-agents/)
- [LangChain Deep Agents](https://docs.langchain.com/oss/python/deepagents/overview#deep-agents-overview)
- [LangGraph Store](https://langchain-ai.github.io/langgraph/how-tos/memory/add-memory/)
- [LangGraph Persistence](https://langchain-ai.github.io/langgraph/concepts/persistence/)

## License

MIT

