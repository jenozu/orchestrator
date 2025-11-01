# Quick Start Guide

## Installation

```bash
# Clone or navigate to the orchestrator directory
cd C:\Users\andel\Desktop\orchestrator

# Create and activate a virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1  # On Windows PowerShell

# Install dependencies
pip install -r requirements.txt

# Verify installation
pytest tests/test_sanity.py -v
# Should output: 1 passed in 0.17s ✅
```

## Basic Usage

### 1. Create a PRD from an Idea (Using MCP)

After restarting Cursor with the MCP server configured, you can use the `create_prd` tool:

**In Cursor Chat:**
```
Can you use the create_prd MCP tool to generate a PRD for a 
budget tracking app that helps users monitor their spending?
```

This will create a comprehensive PRD at `docs/generated_prd.md` with:
- Summary and goals
- User stories
- Functional requirements
- Tech stack recommendations
- Milestones (MVP and Polish)
- Success metrics

### 2. Run the Orchestrator

```python
from agents.orchestrator import Orchestrator

# Create and initialize
orch = Orchestrator()
orch.build_graph()

# Execute once
result = orch.run_once({"initial": "data"})
print(result)  # {'status': 'started'}
```

### 3. Use Subagents

```python
from agents.subagents import prd, diagrammer, backend, frontend

# Run PRD agent
result = prd.run_task({"summary": "Build a todo app"})
print(result)  # {'doc_path': 'docs/prd.md', 'status': 'drafted'}

# Run Diagrammer agent
result = diagrammer.run_task({})
print(result)  # {'diagram_path': 'docs/architecture.mmd', 'status': 'updated'}
```

### 4. Track Tasks

```python
from agents.logging import TaskTracker

tracker = TaskTracker()
tracker.register("task1", [], {"desc": "Create PRD"})
tracker.register("task2", ["task1"], {"desc": "Create diagram"})

# Mark progress
tracker.mark_started("task1")
tracker.mark_completed("task1", {"doc": "docs/prd.md"})

# Get ready tasks
ready = tracker.get_ready()
print(ready)  # ['task2']
```

### 5. Create Worktrees for Parallel Development

```powershell
# Create a worktree for feature work
powershell -File scripts/worktrees.ps1 create feature/api-endpoints

# Work in the worktree directory
cd worktrees/feature/api-endpoints

# Remove when done
powershell -File scripts/worktrees.ps1 remove feature/api-endpoints
```

### 6. Use Learning System

```python
from agents.learning_memory import get_learning_memory

memory = get_learning_memory()

# Learn from a successful fix
await memory.learn_from_success(
    category="error_fixes",
    error="ImportError: No module named 'flask'",
    solution="Add 'flask' to requirements.txt",
    context={"project": "web_app"},
    success=True
)

# Search for learned solutions
solutions = await memory.search_solutions(
    category="error_fixes",
    query="ImportError missing module",
    limit=5
)
```

## Architecture Overview

```
┌─────────────────────────────────────────────────┐
│              Orchestrator                       │
│  Plans tasks, coordinates subagents, manages   │
│  dependencies and parallel execution           │
└────────────┬───────────────────────────────────┘
             │
    ┌────────┴────────┐
    │                 │
┌───▼────┐      ┌─────▼──────┐
│ PRD    │      │Diagrammer  │
│ Agent  │      │ Agent      │
└────────┘      └────────────┘
    │                 │
    │                 │
┌───▼────┐      ┌─────▼──────┐
│Backend │      │Frontend    │
│ Agent  │      │ Agent      │
└────────┘      └────────────┘
```

## Next Steps

1. **Read the Full Documentation**: See `README.md` for comprehensive details
2. **Check Implementation Status**: See `docs/IMPLEMENTATION_STATUS.md`
3. **Review Verification**: See `VERIFICATION.md` for test results
4. **Customize Prompts**: Edit files in `agents/prompts/` for your needs
5. **Explore RAG**: See `docs/RAG_MCP_GUIDE.md` for document-to-code system
6. **Learn About Learning**: See `docs/LEARNING_MEMORY_GUIDE.md` for persistent memory
7. **Configure SLMs**: Add model configurations for each agent type

## Key Files to Customize

- `agents/prompts/*.md` - Agent mission statements
- `.cursor/rules.md` - Coding standards
- `docs/prd.md` - Project requirements template
- `docs/architecture.mmd` - System architecture diagram
- `.cursor/mcp.json` - MCP tool configuration

## Troubleshooting

### Import Errors

```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Test Failures

```bash
# Run with verbose output
pytest tests/test_sanity.py -vv

# Check Python version (requires 3.11+)
python --version
```

### Worktree Issues

```bash
# Check if worktree already exists
git worktree list

# Remove stale worktrees
git worktree remove --force <path>
```

## Resources

- [Full README](README.md)
- [Implementation Status](docs/IMPLEMENTATION_STATUS.md)
- [Verification Report](VERIFICATION.md)
- [Cursor Docs](https://cursor.com/docs)
- [LangGraph Docs](https://docs.langchain.com/langgraph)

## Getting Help

1. Read `docs/` for detailed guides
2. Check `VERIFICATION.md` for test status
3. Review `docs/IMPLEMENTATION_STATUS.md` for known issues
4. Inspect agent prompts in `agents/prompts/`

---

**You're all set!** The orchestrator scaffold is ready to use. 🚀

