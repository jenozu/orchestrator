# RAG MCP Quick Start

## Overview

This quick start guide shows you how to set up and use the Document-to-Code RAG system as a custom MCP server in Cursor.

## What You Get

✅ **Generate PRDs** from simple ideas  
✅ **Parse PRD/README** documents into structured requirements  
✅ **Generate complete projects** from requirements  
✅ **Retrieve similar code** patterns via RAG  
✅ **Auto-debug** errors with intelligent fixes  
✅ **Full Cursor integration** via MCP  

## Setup (5 minutes)

### Step 1: Install Dependencies

```bash
pip install chromadb openai mcp
```

### Step 2: Set API Key

```bash
export OPENAI_API_KEY="your-key-here"
```

Or add to `.cursor/mcp.json`:

```json
{
  "clients": [
    {
      "name": "codegen",
      "command": "python",
      "args": ["-m", "mcp_codegen.server"],
      "env": {
        "OPENAI_API_KEY": "your-key-here"
      }
    }
  ]
}
```

### Step 3: Update Cursor MCP Config

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

### Step 4: Populate RAG Store (Optional)

```python
# scripts/populate_rag.py
from mcp_codegen.rag.store import RAGStore

async def main():
    rag = RAGStore()
    await rag.initialize()
    
    # Add examples
    rag.add_code_example(
        code="""
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
""",
        metadata={"type": "algorithm", "language": "python", "topic": "recursion"}
    )
    
    rag.add_code_example(
        code="""
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return 'Hello World!'

if __name__ == '__main__':
    app.run()
""",
        metadata={"type": "web", "framework": "flask", "pattern": "hello_world"}
    )

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Usage

### In Cursor Chat

Once configured, you can use the tools directly in Cursor:

```
You: Generate a PRD for a budget tracking app

CodeGen: [Calls create_prd tool, generates comprehensive PRD]

You: Parse this document: @docs/prd.md and extract requirements

CodeGen: [Calls parse_prd tool]

You: Generate a Flask project based on those requirements

CodeGen: [Calls generate_project tool with RAG context]

You: There's an error in app.py: ImportError: No module named 'flask'

CodeGen: [Calls debug_error tool, retrieves similar solutions, proposes fix]
```

### Direct Python Usage

```python
# Example: Parse and generate
from mcp_codegen.agents.parser_agent import ParserAgent
from mcp_codegen.agents.code_agent import CodeAgent
from mcp_codegen.rag.store import RAGStore

async def main():
    # Initialize
    rag = RAGStore()
    await rag.initialize()
    
    # Parse
    parser = ParserAgent()
    reqs = await parser.parse_prd("docs/my_prd.md")
    print(f"Requirements: {reqs}")
    
    # Generate
    generator = CodeAgent(rag)
    files = await generator.generate_project(reqs, "output/")
    print(f"Created: {files}")

import asyncio
asyncio.run(main())
```

## Workflow Example

### 1. Generate or Write a PRD

**Option A: Generate a PRD**
```
You: Generate a PRD for a todo app with add, complete, delete, and filter features
CodeGen: [Creates comprehensive PRD with all sections]
```

**Option B: Write a PRD manually**
```markdown
# PRD: Todo App

## Goal
Build a simple todo application

## Features
- Add todos
- Mark complete
- Delete todos
- Filter by status

## Stack
- Flask backend
- SQLite database
- Basic HTML/CSS frontend
```

### 2. Parse and Generate

```python
# Parse PRD
reqs = parse_prd("docs/todo_prd.md")

# Output:
{
  "type": "web_app",
  "features": ["add", "complete", "delete", "filter"],
  "stack": ["flask", "sqlite", "html"],
  "output_dir": "todo_app"
}
```

### 3. RAG Retrieves Context

```python
context = retrieve_context("Flask todo app with SQLite")
# Returns similar Flask app patterns
```

### 4. Generate Code

```python
generate_project(reqs, "todo_app/")
# Creates:
# - app.py (Flask routes)
# - models.py (SQLite models)
# - templates/index.html
# - requirements.txt
```

### 5. Debug Errors

```python
# If error occurs:
debug_error(
    code=generated_code,
    error="ImportError: No module named 'flask'"
)
# Returns fix: Add 'flask' to requirements.txt
```

## Architecture

```
┌──────────┐
│ Cursor   │
│   IDE    │
└────┬─────┘
     │ MCP
┌────▼──────────────────────────┐
│   MCP CodeGen Server          │
│                               │
│  ┌─────────┐   ┌──────────┐  │
│  │ Parser  │──▶│ Generator│  │
│  └─────────┘   └────┬─────┘  │
│       │              │        │
│  ┌────▼──────────┐  │        │
│  │  RAG Store    │◀─┘        │
│  │  (ChromaDB)   │           │
│  └───────────────┘           │
│                               │
│  ┌─────────┐   ┌──────────┐  │
│  │Executor │──▶│ Debugger │  │
│  └─────────┘   └──────────┘  │
└───────────────────────────────┘
```

## Next Steps

1. **Populate RAG Store**: Add code examples relevant to your domain
2. **Customize Prompts**: Edit agent prompts in `mcp_codegen/agents/`
3. **Extend Tools**: Add new MCP tools as needed
4. **Test Workflow**: Try with a real PRD
5. **Integrate**: Use alongside orchestrator for complex projects

## Troubleshooting

### MCP Server Won't Start

```bash
# Check Python path
python -m mcp_codegen.server

# Check logs in Cursor
# Settings → MCP → View logs
```

### RAG Not Finding Results

```bash
# Check store is populated
python scripts/populate_rag.py

# Verify ChromaDB exists
ls chroma_db/
```

### Import Errors

```bash
# Reinstall dependencies
pip install chromadb openai mcp --force-reinstall
```

## References

- Full guide: `docs/RAG_MCP_GUIDE.md`
- MCP docs: https://modelcontextprotocol.io
- ChromaDB docs: https://docs.trychroma.com

## Support

For issues or questions:
1. Check `docs/RAG_MCP_GUIDE.md` for detailed implementation
2. Review `mcp_codegen/` source code
3. Test individual components in isolation

