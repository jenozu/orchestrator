# Integration Guide: Orchestrator + RAG MCP

## Overview

This guide shows how to use the Orchestrator system together with the RAG MCP server for comprehensive project development.

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Cursor IDE                               │
└────────────────┬────────────────────────────────────────────┘
                 │
        ┌────────┴────────┐
        │                 │
┌───────▼────────┐   ┌───▼──────────────────┐
│  Orchestrator  │   │    RAG MCP Server    │
│  (Coordination)│   │  (Document-to-Code)  │
└───────┬────────┘   └───┬──────────────────┘
        │                │
        └────────┬───────┘
                 │
        ┌────────▼────────┐
        │  Shared RAG     │
        │   (ChromaDB)    │
        └─────────────────┘
```

## Use Cases

### Use Case 1: Orchestrator for Multi-Agent Coordination

**When**: Complex projects with multiple parallel tasks

```python
from agents.orchestrator import Orchestrator
from agents.logging import TaskTracker

orch = Orchestrator()
tracker = TaskTracker()

# Define tasks
tracker.register("prd", [], {"desc": "Create PRD"})
tracker.register("diagram", ["prd"], {"desc": "Create diagram"})
tracker.register("backend", ["prd"], {"desc": "Build backend"})
tracker.register("frontend", ["prd"], {"desc": "Build frontend"})

# Orchestrator coordinates execution
result = orch.run_once({"tasks": tracker.to_dict()})
```

### Use Case 2: RAG MCP for Document-to-Code

**When**: Single feature or component from spec

```python
# In Cursor chat:
You: Parse @docs/feature_spec.md and generate the code

# MCP server handles:
1. parse_prd() extracts requirements
2. retrieve_context() finds similar patterns
3. generate_project() creates code
4. debug_error() fixes any issues
```

### Use Case 3: Combined Workflow

**When**: Complex project starting from PRD

**Step 1**: Use RAG MCP to parse PRD
```python
# MCP: Parse document
requirements = await mcp_parser.parse("docs/project_prd.md")
```

**Step 2**: Use Orchestrator to coordinate buildout
```python
# Orchestrator: Coordinate agents
orch.execute_master_plan({
    "requirements": requirements,
    "output_dir": "project/"
})
```

**Step 3**: RAG MCP handles debugging
```python
# MCP: Debug errors from orchestrator's generated code
fixes = await mcp_debugger.fix(generated_code, errors)
```

## Shared RAG Store

Both systems can share the same ChromaDB collection:

```python
# Orchestrator agents use RAG for context
from mcp_codegen.rag.store import RAGStore

rag = RAGStore()
await rag.initialize()

# Use in orchestrator subagents
class BackendAgent:
    def __init__(self, rag_store):
        self.rag = rag_store
    
    async def generate_code(self, requirements):
        context = self.rag.retrieve_similar("Flask API")
        # Generate with context
```

## Integration Examples

### Example 1: Sequential Workflow

```python
# 1. MCP parses PRD
reqs = await mcp_codegen.agents.ParserAgent().parse_prd("prd.md")

# 2. Orchestrator coordinates multi-agent build
orch.coordinate_build(reqs)

# 3. If errors, MCP debugger fixes
for error in orch.errors:
    fix = await mcp_codegen.agents.DebugAgent().fix_error(
        code=error.code,
        error=error.message
    )
```

### Example 2: Parallel Execution

```python
# Orchestrator spawns parallel agents
with orch.parallel_execution():
    # Agent 1: Uses RAG MCP internally
    agent1.generate_with_mcp()
    
    # Agent 2: Uses RAG MCP internally
    agent2.generate_with_mcp()

# All agents share same RAG store
```

### Example 3: Code Review Workflow

```python
# Orchestrator generates code
generated_files = orch.execute_plan()

# MCP reviews and suggests improvements
for file in generated_files:
    review = await mcp_codegen.review_code(file.content)
    if review.needs_changes:
        orch.update_agent_prompts(review.suggestions)
```

## Configuration

### Shared Configuration

```python
# config.py (shared)
RAG_STORE_PATH = "./chroma_db"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

### Orchestrator Config

```python
# agents/config.py
ORCHESTRATOR_GRAPH_PATH = "./agents/graph.json"
MAX_PARALLEL_AGENTS = 4
```

### MCP Server Config

```python
# mcp_codegen/config.py
MCP_SERVER_PORT = 8000
RETRIEVAL_K = 5
MAX_DEBUG_RETRIES = 3
```

## Best Practices

### 1. Start with RAG MCP for Simple Tasks

Use MCP for straightforward document→code conversions:
- Single feature implementations
- Component scaffolding
- Quick prototypes

### 2. Use Orchestrator for Complex Projects

Use orchestrator when you need:
- Multiple parallel agents
- Complex dependencies
- Long-running workflows
- State management

### 3. Share RAG Store

Both systems benefit from same code patterns:
```python
# Initialize once
rag_store = RAGStore()
await rag_store.initialize()

# Pass to both
orchestrator = Orchestrator(rag_store)
mcp_server = MCPServer(rag_store)
```

### 4. Separate Concerns

- **Orchestrator**: Coordination, parallelism, workflows
- **RAG MCP**: Code generation, debugging, retrieval
- **Shared RAG**: Context for all agents

### 5. Incremental Integration

Start separate, then integrate:
1. ✅ Build orchestrator scaffold
2. ✅ Build RAG MCP scaffold
3. 🔄 Share RAG store
4. 🔄 Cross-agent communication
5. 🔄 Unified CLI/UI

## Troubleshooting

### Conflicting RAG Usage

**Problem**: Both systems writing to same collection  
**Solution**: Use collection prefixes or separate collections

```python
# Option 1: Prefixes
orchestrator_collection = "orchestrator_patterns"
mcp_collection = "mcp_patterns"

# Option 2: Metadata filtering
metadata_filter = {"source": "orchestrator"}
```

### State Synchronization

**Problem**: Orchestrator and MCP have different state  
**Solution**: Use shared memory store

```python
from agents.logging import MemoryStore

shared_store = MemoryStore()
orchestrator = Orchestrator(memory=shared_store)
mcp_server = MCPServer(memory=shared_store)
```

### Tool Conflicts

**Problem**: Same tool names in both systems  
**Solution**: Use namespaces

```python
# Orchestrator tools
orch_parse_prd()
orch_generate_diagram()

# MCP tools
mcp_parse_prd()
mcp_generate_code()
```

## Future Enhancements

### Unified CLI

```bash
orch-cli build --prd docs/prd.md --mode orchestrated
orch-cli build --prd docs/prd.md --mode mcp
orch-cli build --prd docs/prd.md --mode hybrid
```

### Shared Context Manager

```python
with ProjectContext("my_project"):
    # Both orchestrator and MCP share context
    orchestrator.execute()
    mcp_server.generate()
```

### Cross-Agent Learning

```python
# MCP learns from orchestrator's work
mcp_server.learn_from_orchestrator(orchestrator.history)

# Orchestrator uses MCP patterns
orchestrator.import_mcp_patterns(mcp_server.rag_store)
```

## Summary

✅ **Use Orchestrator** for multi-agent coordination  
✅ **Use RAG MCP** for document-to-code workflow  
✅ **Share RAG store** for common context  
✅ **Separate concerns** but integrate when needed  
✅ **Start simple** then add complexity  

Both systems are designed to work independently and together, giving you flexibility to choose the right tool for each task.

