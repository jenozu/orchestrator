# Testing Guide: Build Your Todo App

## Quick Start to Get Running

### Step 1: Add MCP Server to Cursor Config

Edit `.cursor/mcp.json`:

```json
{
  "$schema": "https://schemas.cursor.sh/mcp.config.schema.json",
  "clients": [
    {
      "name": "filesystem",
      "command": "builtin",
      "args": {
        "tools": ["read_file", "write_file", "edit_file", "ls"]
      }
    },
    {
      "name": "codegen",
      "command": "python",
      "args": ["-m", "mcp_codegen.server"]
    }
  ],
  "policies": {
    "workspaceAllowlist": ["./"],
    "pathDenylist": ["node_modules/**", ".git/**", ".venv/**"],
    "maxToolOutputChars": 200000
  }
}
```

### Step 2: Install Missing Dependencies

```bash
pip install chromadb openai mcp langgraph-checkpoint-postgres
```

### Step 3: Restart Cursor

Close and reopen Cursor to load the new MCP configuration.

### Step 4: Test in Cursor Chat

Open Cursor and try this in the chat:

**To create a PRD from an idea:**
```
Can you use the create_prd MCP tool to generate a PRD for a 
habit tracking app?
```

**To parse an existing PRD:**
```
Can you use the MCP codegen parse_prd tool to parse docs/my_todo_prd.md?
```

## Recommended Reading Order

For your todo app project, read in this order:

### 1. **Start Here**: `QUICKSTART.md`
- 5-minute overview
- Basic usage examples
- How to run orchestrator

### 2. **Then**: `docs/RAG_MCP_QUICKSTART.md`
- MCP-specific setup
- How to use in Cursor
- Document → code workflow

### 3. **Reference**: `LEARNING_SYSTEM_SUMMARY.md`
- How learning works
- Examples and benefits

## Building Your Todo App

### Approach 1: Using MCP in Cursor (Recommended for Testing)

1. Create a simple PRD in `docs/my_todo_prd.md`:

```markdown
# Todo App PRD

## Goal
Build a simple todo application

## Features
- Add todos
- Mark complete
- Delete todos
- Filter by status (all, active, completed)

## Tech Stack
- Python Flask backend
- HTML/CSS frontend
- SQLite database
```

2. In Cursor chat, try:

```
Use the codegen MCP tools to parse docs/my_todo_prd.md 
and generate the project structure
```

3. Debug as needed - the system will learn from your fixes!

### Approach 2: Using Orchestrator Directly

```python
from agents.orchestrator import Orchestrator

orch = Orchestrator()
orch.build_graph()

# Define your todo app plan
tasks = [
    {"id": "prd", "deps": []},
    {"id": "backend", "deps": ["prd"]},
    {"id": "frontend", "deps": ["prd"]},
    {"id": "tests", "deps": ["backend", "frontend"]}
]

# Run orchestration
result = orch.run_once({"tasks": tasks})
```

## Testing the Learning System

### Test 1: Basic Functionality

```bash
# Verify imports work
python -c "from agents.learning_memory import get_learning_memory; print('Learning memory ready')"
python -c "from mcp_codegen.server import app; print('MCP server ready')"
```

### Test 2: End-to-End Workflow

1. Create a test PRD
2. Try parsing it in Cursor
3. Generate some code
4. Intentionally create an error
5. Use debug_error tool
6. Watch it learn!

### Test 3: Check Learning Stats

In Cursor chat:
```
Get the learning stats to see what the system has learned
```

## What to Expect

### If MCP Server Works
- Cursor chat will show codegen tools available
- `parse_prd` tool will extract requirements
- `generate_project` will create files
- `debug_error` will learn from fixes

### If Not Working
- Check `.cursor/mcp.json` syntax
- Verify Python dependencies installed
- Restart Cursor
- Check Cursor logs for MCP errors

## Next Steps After Testing

Once basic flow works:

1. **Populate RAG**: Add Flask/Python examples to vector store
2. **Run Real Tasks**: Generate actual todo app code
3. **Monitor Learning**: Check what patterns it learns
4. **Iterate**: Refine based on results

## Documentation Reference

| Need | Read This |
|------|-----------|
| Quick start | `QUICKSTART.md` |
| MCP setup | `docs/RAG_MCP_QUICKSTART.md` |
| Learning system | `LEARNING_SYSTEM_SUMMARY.md` |
| Full guide | `docs/RAG_MCP_GUIDE.md` |
| Integration | `docs/INTEGRATION_GUIDE.md` |
| Architecture | `README.md` |

## Common Issues

### "Module not found"
```bash
pip install -r requirements.txt --force-reinstall
```

### "MCP server not responding"
- Check `.cursor/mcp.json` JSON is valid
- Verify `python -m mcp_codegen.server` runs without errors
- Restart Cursor completely

### "No learning happening"
- Check if OPENAI_API_KEY is set
- Learning falls back gracefully without it
- See `LEARNING_SYSTEM_SUMMARY.md` for details

## Success Indicators

✅ MCP tools show up in Cursor  
✅ Can call parse_prd on a document  
✅ Debugger responds to errors  
✅ Learning stats shows data  
✅ Agents improve over time  

---

**Start with `QUICKSTART.md` and `docs/RAG_MCP_QUICKSTART.md` for fastest results!** 🚀

