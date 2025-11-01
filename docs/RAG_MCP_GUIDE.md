# RAG-Based Document-to-Code MCP System

## Overview

This guide explains how to build a custom MCP server that uses RAG (Retrieval-Augmented Generation) to turn ideas and PRD/README documents into working code, with built-in debugging capabilities.

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                  Cursor IDE                         │
└──────────────────┬──────────────────────────────────┘
                   │ MCP Protocol
┌──────────────────▼──────────────────────────────────┐
│              MCP CodeGen Server                     │
│  ┌────────────┐  ┌────────────┐  ┌──────────────┐ │
│  │  Parser    │  │    RAG     │  │   Executor   │ │
│  │  Agent     │  │   System   │  │   + Debugger │ │
│  └────────────┘  └────────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────┘
```

## Components

### 1. PRD Generation Agent
- Generates comprehensive PRDs from simple ideas
- Creates structured requirements with goals, user stories, milestones
- Provides tech stack recommendations

### 2. Document Parser Agent
- Extracts structured requirements from PRD/README
- Breaks down into functional components
- Identifies dependencies and constraints

### 3. RAG System
- Vector store for code patterns and solutions
- Semantic retrieval of similar examples
- Context augmentation for code generation

### 4. Code Generator
- LLM-based code generation with RAG context
- Multi-file project scaffolding
- Dependency management

### 5. Executor & Debugger
- Runs generated code in isolated environment
- Captures errors and stack traces
- Intelligent error analysis and fixing

### 6. MCP Server
- Exposes tools to Cursor via MCP protocol
- Manages state across tool invocations
- Returns structured results

## Implementation Plan

### Phase 1: MCP Server Foundation

```bash
mcp_codegen/
├── server.py              # MCP server entry point
├── tools/
│   ├── prd_tool.py        # PRD generation tool
│   ├── parser.py          # Document parsing tools
│   ├── rag.py             # RAG retrieval tools
│   ├── generator.py       # Code generation tools
│   └── debugger.py        # Error analysis tools
├── agents/
│   ├── prd_agent.py       # Generates PRDs from ideas
│   ├── parser_agent.py    # Parses PRD/README
│   ├── code_agent.py      # Generates code
│   └── debug_agent.py     # Fixes errors
├── rag/
│   ├── vector_store.py    # ChromaDB/Pinecone integration
│   ├── embedding.py       # Text embeddings
│   └── retrieval.py       # Similarity search
└── executor/
    ├── runner.py          # Execute code
    └── sandbox.py         # Isolate execution
```

### Phase 2: RAG System Setup

**Vector Store Choice:**
- **ChromaDB**: Local, easy setup, good for development
- **Pinecone**: Cloud, scalable, good for production
- **Weaviate**: Open source, self-hostable

**Embeddings:**
- **OpenAI ada-002**: High quality, requires API key
- **sentence-transformers**: Local, free, good alternative

**What to Store:**
- Code patterns and solutions
- API documentation snippets
- Error solutions
- Architecture patterns
- Best practices

### Phase 3: Code Generation Workflow

1. **Generate PRD** (optional): Create requirements document from idea
2. **Parse Document**: Extract requirements, features, constraints
3. **Retrieve Context**: Find similar solutions via RAG
4. **Generate Code**: Create files with LLM using context
5. **Execute**: Run code in sandbox
6. **Debug**: Analyze errors, propose fixes, iterate

### Phase 4: MCP Tools Design

```python
Tools exposed to Cursor:

1. create_prd(idea: str, output_path: str) -> PRD Document
   - Generate comprehensive PRD from simple idea
   - Returns: PRD file path and summary

2. parse_prd(document_path: str) -> Requirements
   - Parse PRD/README into structured requirements
   - Returns: components, features, dependencies

3. generate_project(requirements: dict, output_dir: str) -> Files
   - Generate complete project from requirements
   - Uses RAG for context
   - Returns: list of files created

4. execute_code(file_path: str, timeout: int) -> Result
   - Run code and capture output
   - Returns: stdout, stderr, exit_code

5. debug_error(code: str, error: str, context: dict) -> Fix
   - Analyze error and propose fix
   - Uses RAG for similar error solutions
   - Returns: fixed_code, explanation

6. retrieve_context(query: str, k: int) -> Examples
   - RAG retrieval for similar code/patterns
   - Returns: top-k similar examples
```

## Technology Stack

### Core Dependencies

```txt
# RAG & Vector DB
chromadb>=0.4.0              # Local vector store
openai-embeddings>=1.0       # or sentence-transformers
langchain>=0.1.0             # RAG orchestration

# MCP Server
mcp>=1.0.0                   # Model Context Protocol

# Code Execution
docker>=6.0                  # Sandboxing (optional)
subprocess                   # Built-in execution

# LLM
openai>=1.0.0                # Code generation
anthropic>=0.3.0             # Alternative LLM

# Parsing
markdown>=3.5                # Doc parsing
pydantic>=2.0                # Schema validation
```

### Project Structure

```
orchestrator/                 # Your existing repo
├── mcp_codegen/             # NEW: MCP server
│   ├── __init__.py
│   ├── server.py            # MCP server entry
│   ├── config.py            # Configuration
│   │
│   ├── tools/               # MCP tools
│   │   ├── __init__.py
│   │   ├── parser_tool.py
│   │   ├── rag_tool.py
│   │   ├── generator_tool.py
│   │   └── debugger_tool.py
│   │
│   ├── agents/              # AI agents
│   │   ├── __init__.py
│   │   ├── parser_agent.py
│   │   ├── code_agent.py
│   │   └── debug_agent.py
│   │
│   ├── rag/                 # RAG components
│   │   ├── __init__.py
│   │   ├── store.py         # Vector store wrapper
│   │   ├── embedding.py     # Embedding functions
│   │   └── retrieval.py     # Similarity search
│   │
│   ├── executor/            # Code execution
│   │   ├── __init__.py
│   │   ├── runner.py        # Execute code
│   │   └── error_parser.py  # Parse stack traces
│   │
│   └── prompts/             # Agent prompts
│       ├── parser.md
│       ├── generator.md
│       └── debugger.md
│
├── .cursor/
│   └── mcp.json             # Add new MCP client
│
└── requirements.txt         # Update with new deps
```

## Setup Instructions

### Step 1: Install Dependencies

```bash
pip install chromadb openai langchain mcp pydantic markdown docker
```

### Step 2: Create MCP Server

```python
# mcp_codegen/server.py
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("codegen")

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="parse_prd",
            description="Parse PRD or README into structured requirements",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_path": {"type": "string"}
                },
                "required": ["document_path"]
            }
        ),
        Tool(
            name="generate_project",
            description="Generate complete project from requirements",
            inputSchema={
                "type": "object",
                "properties": {
                    "requirements": {"type": "object"},
                    "output_dir": {"type": "string"}
                },
                "required": ["requirements", "output_dir"]
            }
        ),
        # ... more tools
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "parse_prd":
        result = await parse_prd(arguments["document_path"])
        return [TextContent(type="text", text=result)]
    # ... handle other tools

if __name__ == "__main__":
    app.run()
```

### Step 3: Configure Cursor MCP

```json
// .cursor/mcp.json
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
      "args": ["-m", "mcp_codegen.server"],
      "env": {
        "OPENAI_API_KEY": "${OPENAI_API_KEY}"
      }
    }
  ],
  "policies": {
    "workspaceAllowlist": ["./"],
    "pathDenylist": ["node_modules/**", ".git/**", ".venv/**"],
    "maxToolOutputChars": 200000
  }
}
```

### Step 4: Initialize RAG Store

```python
# mcp_codegen/rag/store.py
import chromadb
from chromadb.utils import embedding_functions

class RAGStore:
    def __init__(self, persist_dir: str = "./chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection(
            name="code_patterns",
            embedding_function=embedding_functions.OpenAIEmbeddingFunction(
                api_key=os.getenv("OPENAI_API_KEY"),
                model_name="text-embedding-3-small"
            )
        )
    
    def add_code_example(self, code: str, metadata: dict):
        """Add a code example to the store."""
        self.collection.add(
            documents=[code],
            metadatas=[metadata],
            ids=[str(uuid.uuid4())]
        )
    
    def retrieve_similar(self, query: str, n_results: int = 5):
        """Retrieve similar code examples."""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results['documents'][0], results['metadatas'][0]
```

### Step 5: Build Parser Agent

```python
# mcp_codegen/agents/parser_agent.py
from openai import OpenAI
import markdown

class ParserAgent:
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
    
    async def parse_prd(self, doc_path: str) -> dict:
        """Parse PRD/README into structured requirements."""
        with open(doc_path) as f:
            content = f.read()
        
        # Use LLM to extract requirements
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You extract structured requirements from documents."},
                {"role": "user", "content": f"Parse this document:\n\n{content}"}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
```

### Step 6: Build Code Generator Agent

```python
# mcp_codegen/agents/code_agent.py
class CodeAgent:
    def __init__(self, api_key: str, rag_store: RAGStore):
        self.client = OpenAI(api_key=api_key)
        self.rag = rag_store
    
    async def generate_project(self, requirements: dict, output_dir: str):
        """Generate complete project from requirements."""
        # Retrieve similar examples via RAG
        context = self.rag.retrieve_similar(
            f"Project with {requirements['type']} and {requirements['features']}"
        )
        
        # Generate code with context
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an expert code generator."},
                {"role": "user", "content": f"Generate code for:\n{requirements}\n\nUse these examples:\n{context}"}
            ]
        )
        
        # Write files to output_dir
        # ... implementation
```

### Step 7: Build Debugger Agent

```python
# mcp_codegen/agents/debug_agent.py
class DebugAgent:
    def __init__(self, api_key: str, rag_store: RAGStore):
        self.client = OpenAI(api_key=api_key)
        self.rag = rag_store
    
    async def fix_error(self, code: str, error: str) -> dict:
        """Analyze error and propose fix."""
        # Retrieve similar error solutions
        context = self.rag.retrieve_similar(f"Error: {error}")
        
        # Generate fix
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are an expert debugger."},
                {"role": "user", "content": f"Code:\n{code}\n\nError:\n{error}\n\nExamples:\n{context}"}
            ]
        )
        
        return {"fixed_code": response.choices[0].message.content}
```

## Usage in Cursor

Once the MCP server is running and configured:

1. **Load a PRD**: Open your PRD document in Cursor
2. **Invoke Parser**: Use the `parse_prd` tool to extract requirements
3. **Generate Code**: Trigger `generate_project` to create files
4. **Execute**: The code runs automatically or manually via `execute_code`
5. **Debug**: If errors occur, use `debug_error` to fix them
6. **Iterate**: The debugger can retry multiple times

## Populating RAG Store

Before use, populate the vector store with code examples:

```python
# scripts/populate_rag.py
from mcp_codegen.rag.store import RAGStore

rag = RAGStore()

# Add examples
rag.add_code_example(
    code="def fibonacci(n): ...",
    metadata={"type": "algorithm", "language": "python", "topic": "math"}
)

rag.add_code_example(
    code="flask app configuration...",
    metadata={"type": "web", "framework": "flask", "pattern": "config"}
)

# Add from GitHub, documentation, etc.
```

## Integration with Existing Orchestrator

The MCP server can work alongside your orchestrator:

- **Orchestrator**: Coordinates multi-agent workflows
- **MCP CodeGen**: Handles document→code specific tasks
- **Shared RAG**: Both can use the same vector store
- **Clear Separation**: Different responsibilities

## Next Steps

1. Implement MCP server skeleton
2. Set up ChromaDB vector store
3. Build parser, generator, and debugger agents
4. Create MCP tools and wire them up
5. Test end-to-end workflow
6. Populate RAG store with examples
7. Iterate on prompts and retrieval strategies

## References

- [MCP Specification](https://modelcontextprotocol.io)
- [Cursor MCP Docs](https://cursor.com/docs/context/mcp)
- [ChromaDB Docs](https://docs.trychroma.com)
- [LangChain RAG](https://python.langchain.com/docs/use_cases/question_answering)

