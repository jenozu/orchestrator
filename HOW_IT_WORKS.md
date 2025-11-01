# How the System Works (Simple Explanation)

## Where Everything Lives

**Everything runs on YOUR LOCAL COMPUTER** - no VPS, no cloud, no remote servers!

```
Your Computer (C:\Users\andel\Desktop\orchestrator)
│
├── Cursor IDE (runs locally)
│   │
│   ├── Your Code Editor
│   ├── Chat Interface
│   └── MCP Client (built-in)
│
├── Python Process (runs when you use Cursor)
│   │
│   └── mcp_codegen/server.py
│       ├── Waits for requests from Cursor
│       ├── Uses your local files
│       └── Stores data locally (ChromaDB, logs)
│
└── Your Workspace Files
    ├── docs/my_todo_prd.md
    ├── any code you generate
    └── local databases (chroma_db/)
```

## How It Works - Step by Step

### 1. You Type in Cursor Chat

```
You: "Parse docs/my_todo_prd.md"
```

### 2. Cursor Sends Request Locally

Cursor (running on your machine) → Python MCP server (also on your machine)

No network! Just inter-process communication on the same computer.

### 3. MCP Server Does the Work

```
mcp_codegen/server.py running on YOUR computer:
├── Reads docs/my_todo_prd.md from YOUR filesystem
├── Processes it using YOUR CPU
├── Returns results to Cursor
└── Stores learned patterns in YOUR local database
```

### 4. Results Come Back

Cursor displays the results in the chat.

## Data Storage - All Local

### Where Data Lives

| What | Where It's Stored |
|------|-------------------|
| **Your code** | `C:\Users\andel\Desktop\orchestrator\` |
| **RAG patterns** | `C:\Users\andel\Desktop\orchestrator\chroma_db\` |
| **Learned fixes** | `C:\Users\andel\Desktop\orchestrator\` (in-memory for now) |
| **Logs** | `C:\Users\andel\Desktop\orchestrator\logs\` |

**Everything stays on YOUR computer!**

### The Only External Call (Optional)

When you have an `OPENAI_API_KEY`, the system calls OpenAI's API to:
- Generate embeddings (vectors) for RAG search
- Call LLMs for code generation
- Get AI help

But all data stays on your machine!

## Architecture Flow

```
┌─────────────────────────────────────────────────────────────┐
│           YOUR COMPUTER (Local Only)                        │
│                                                             │
│  ┌──────────┐              ┌─────────────────┐            │
│  │  Cursor  │ ←────MCP────→│  Python Server  │            │
│  │   IDE    │   Protocol   │  mcp_codegen/   │            │
│  └────┬─────┘              └────────┬────────┘            │
│       │                              │                      │
│       │                              │                      │
│  ┌────▼──────────────────────────────▼─────────┐          │
│  │         Your File System                     │          │
│  │  ├── docs/my_todo_prd.md                     │          │
│  │  ├── chroma_db/ (vector database)            │          │
│  │  └── any generated code                      │          │
│  └──────────────────────────────────────────────┘          │
│                                                             │
│  (Everything above is LOCAL)                                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
                        │
                        ↓ (Optional: Only if you have API key)
              ┌─────────────────┐
              │   OpenAI API    │
              │   (Cloud)       │
              └─────────────────┘
            (For embeddings & LLM calls)
```

## How MCP Works

MCP (Model Context Protocol) is like a **local REST API**:

### Traditional Way (REST API on Server)
```
Your Computer → Internet → Server → Internet → Your Computer
```

### MCP Way (Local Inter-Process Communication)
```
Cursor (process 1) → Local IPC → Python Server (process 2) → Filesystem
```

**No network, no latency, no security concerns!**

## What Happens When You Use It

### Example: "Parse docs/my_todo_prd.md"

1. **You type in Cursor**
2. **Cursor reads `.cursor/mcp.json`** → sees "codegen" server
3. **Cursor starts Python**: `python -m mcp_codegen.server` (if not running)
4. **Cursor sends message**: "Hey, use parse_prd tool with this file path"
5. **MCP server receives**: "Got it, let me read that file"
6. **MCP server reads**: `docs/my_todo_prd.md` from YOUR disk
7. **MCP server processes**: (uses YOUR CPU)
8. **MCP server responds**: "Here's the parsed requirements"
9. **Cursor displays**: Results in chat

**All happens in milliseconds on your machine!**

## Security & Privacy

### ✅ What Stays Local
- All your code
- All your documents
- All learned patterns
- All RAG data
- All logs

### ⚠️ What Goes Out (Only if you have API key)
- API calls to OpenAI for:
  - Generating embeddings
  - LLM code generation
  
**You control this with your API key settings!**

## Setup Explained Simply

```json
// .cursor/mcp.json tells Cursor:
{
  "codegen": {
    "command": "python",           // Use Python
    "args": ["-m", "mcp_codegen.server"]  // Run THIS file locally
  }
}
```

This means: **"Hey Cursor, when I ask for codegen tools, run this Python file on my computer"**

## Production Scaling (Future)

If you want to scale later, you CAN move to VPS:

```
VPS:
├── Postgres database (persistent learning)
├── MCP server running 24/7
└── Shared knowledge across team

Your Computer:
└── Connects to VPS via network
```

But for now, **everything is local and that's perfectly fine!**

## Quick Verification

Want to see it's local?

```bash
# Check what's running on your machine
# Open Task Manager → Look for Python processes

# Check local files
dir C:\Users\andel\Desktop\orchestrator\chroma_db

# Check local logs
dir C:\Users\andel\Desktop\orchestrator\logs
```

**Everything you see is on YOUR computer!**

## Summary

- ✅ **No VPS needed** - everything runs locally
- ✅ **No cloud storage** - data stays on your machine  
- ✅ **Fast** - no network latency
- ✅ **Private** - your data stays yours
- ✅ **Simple** - just a local Python server

**The MCP server is just a helper script running on your computer to make Cursor smarter!**

