# Quick Reference - Orchestrator & MCP Server

## 🚀 Quick Start Commands

### Run Tests

```powershell
# Easy way (handles encoding automatically)
.\run_test.ps1

# Manual way
$env:PYTHONIOENCODING="utf-8"
python test_rules_generator.py
```

### Start MCP Server

```powershell
# Test that the server starts (will initialize and exit - this is normal)
python scripts/run_mcp_server.py
```

### Use Orchestrator

```python
from agents.orchestrator import Orchestrator

orchestrator = Orchestrator()
orchestrator.build_graph()

result = orchestrator.run_once({
    "raw_user_request": "Your project description"
})
```

## 📋 What Each Test Does

### `run_test.ps1` or `test_rules_generator.py`

**Workflow:**
1. **IntentParser** - Parses your request into structured JSON
2. **RulesGenerator** - Creates project rules (`.cursor/rules.md`)
3. **RulesGenerator** - Creates task list (`docs/tasks.md`)
4. **PRD Agent** - Drafts Product Requirements Document

**Output:**
- `.cursor/rules.md` - Project coding standards and rules
- `docs/tasks.md` - Master task list with all project tasks
- `docs/prd.md` - Product Requirements Document

## 🛠️ Available Agents

| Agent | Purpose | Trigger |
|-------|---------|---------|
| **IntentParser** | Parse user requests | First in chain |
| **RulesGenerator** | Create rules & tasks | After IntentParser |
| **PRD Agent** | Create PRD | After RulesGenerator |
| **Backend Agent** | Generate backend code | On demand |
| **Frontend Agent** | Generate frontend code | On demand |
| **QA Agent** | Quality assurance | On demand |
| **Diagrammer** | Create diagrams | On demand |

## 🔧 MCP Server Tools

| Tool | Purpose | Required Params |
|------|---------|-----------------|
| `create_prd` | Create PRD from idea | `idea` |
| `parse_prd` | Parse PRD to JSON | `document_path` |
| `retrieve_context` | RAG search | `query` |
| `generate_project` | Generate code | `requirements`, `output_dir` |
| `debug_error` | Debug with learning | `code`, `error` |
| `search_learned_solutions` | Find learned fixes | `query` |
| `get_learning_stats` | Learning statistics | - |

## 📁 Key Files

| File | Purpose |
|------|---------|
| `.env` | API keys (automatically loaded) |
| `.cursor/rules.md` | Project rules (auto-generated) |
| `docs/tasks.md` | Master task list (auto-generated) |
| `docs/prd.md` | Product Requirements (auto-generated) |
| `merged_mcp_config.json` | MCP server configuration |

## 🔍 Troubleshooting

### Import Error: No module named 'mcp_codegen'
**Status**: ✅ FIXED
**Solution**: `scripts/run_mcp_server.py` now auto-adds project root to path

### Emoji Encoding Error (Windows)
**Solution**: Use `.\run_test.ps1` or set `$env:PYTHONIOENCODING="utf-8"`

### LangChain Beta Warning
**Status**: ℹ️ INFORMATIONAL ONLY
**Action**: None needed - the system works correctly

### MCP Server Exits Immediately
**Status**: ✅ EXPECTED BEHAVIOR
**Reason**: stdio-based servers only run when connected to MCP client

## 🌟 Workflow Example

```powershell
# 1. Start with a project idea
.\run_test.ps1

# 2. Check generated files
cat .cursor/rules.md
cat docs/tasks.md
cat docs/prd.md

# 3. Use the generated rules in your development
# The rules are automatically loaded by the agents

# 4. Continue with backend/frontend generation
python -c "from agents.orchestrator import Orchestrator; ..."
```

## 📊 Test Output Meaning

```
✅ Workflow completed successfully!
```
All agents executed successfully.

```
📁 Generated Files:
✅ .cursor/rules.md created successfully!
✅ docs/tasks.md created successfully!
```
Files were generated and saved.

```
📈 State Updates:
   - Rules Loaded by PRD: True
   - Tasks Loaded by PRD: True
```
PRD Agent successfully loaded the generated rules and tasks.

## 🔐 Security

- ✅ API keys stored in `.env` (in `.gitignore`)
- ✅ Never commit `.env` to version control
- ✅ All agents automatically load from `.env`
- ✅ No hardcoded credentials

## 📦 Dependencies

All managed in `requirements.txt`:
- ✅ OpenAI API
- ✅ LangChain (with beta embeddings)
- ✅ ChromaDB (for RAG)
- ✅ LangGraph (for orchestration)
- ✅ FastAPI (for backend generation)
- ✅ MCP SDK (for MCP server)

## 🎯 Common Use Cases

### 1. Generate Project Structure
```powershell
.\run_test.ps1
```

### 2. Test MCP Server
```powershell
python scripts/run_mcp_server.py
```

### 3. Check Learning Stats
```python
from agents.learning_memory import get_learning_memory

memory = get_learning_memory()
stats = memory.get_top_solutions(category="error_fixes")
print(stats)
```

### 4. Custom Orchestrator Workflow
```python
from agents.orchestrator import Orchestrator

orchestrator = Orchestrator()
orchestrator.build_graph()

# Your custom request
result = orchestrator.run_once({
    "raw_user_request": "Build an e-commerce platform..."
})
```

## 📚 Documentation Files

- `FIX_SUMMARY.md` - Complete fix details
- `MCP_SERVER_SETUP.md` - MCP server setup guide
- `QUICK_REFERENCE.md` - This file
- `README_ENV_SETUP.md` - Environment setup guide

## ✅ System Status

| Component | Status |
|-----------|--------|
| MCP Server | ✅ Working |
| Environment Loading | ✅ Working |
| Orchestrator | ✅ Working |
| Learning Memory | ✅ Working |
| RAG System | ✅ Working |
| IntentParser | ✅ Working |
| RulesGenerator | ✅ Working |
| PRD Agent | ✅ Working |

**Overall Status**: 🟢 READY FOR PRODUCTION

