# Learning & Memory System Guide

## Overview

Your system can learn and improve over time using **LangGraph Store** for persistent memory with semantic search capabilities. Combined with your existing RAG vector store, this creates a powerful learning loop.

## Key Components

### 1. **LangGraph Store** (Persistent Memory)
- Stores arbitrary key-value pairs with namespaces
- Supports semantic search across memories
- Automatic embedding and similarity search
- Survives across sessions

### 2. **Checkpointer** (State Persistence)
- Saves agent execution state
- Enables resumable workflows
- Thread/conversation management

### 3. **RAG Vector Store** (Already Created)
- Code patterns and solutions
- Error-fix mappings
- Best practices

## How Learning Works

```
┌───────────────────────────────────────────────────────────┐
│                    Learning Loop                          │
├───────────────────────────────────────────────────────────┤
│                                                            │
│  1. Agent encounters error/problem                        │
│     ↓                                                      │
│  2. Searches RAG + LangGraph Store                        │
│     ↓                                                      │
│  3. Retrieves similar solutions                           │
│     ↓                                                      │
│  4. Attempts fix with context                             │
│     ↓                                                      │
│  5. If successful:                                        │
│     → Stores solution in RAG store                        │
│     → Stores metadata in LangGraph Store                  │
│     → Updates error-fix mapping                           │
│     ↓                                                      │
│  6. Next time: Faster, better solutions                   │
│                                                            │
└───────────────────────────────────────────────────────────┘
```

## Implementation

### Step 1: Set Up LangGraph Store

```python
# agents/learning_memory.py
from langgraph.store.memory import InMemoryStore
from langchain.embeddings import init_embeddings

# Configure with semantic search
store = InMemoryStore(
    index={
        "embed": init_embeddings("openai:text-embedding-3-small"),
        "dims": 1536,
        "fields": ["error", "solution", "context", "$"]  # What to embed
    }
)

# Or use persistent Postgres store (production)
from langchain.langgraph_checkpoint_postgres import PostgresStore
store = PostgresStore.from_conn_string("postgresql://...")
```

### Step 2: Add Checkpointer

```python
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres import PostgresSaver

# In-memory for dev
checkpointer = InMemorySaver()

# Or Postgres for production
checkpointer = PostgresSaver.from_conn_string("postgresql://...")
```

### Step 3: Compile Graph with Both

```python
# agents/orchestrator.py
from agents.learning_memory import store, checkpointer

class Orchestrator:
    def __init__(self):
        self.store = store
        self.checkpointer = checkpointer
    
    def build_graph(self):
        graph = StateGraph(dict)
        # ... add nodes ...
        
        # Compile with both store and checkpointer
        self._graph = graph.compile(
            checkpointer=self.checkpointer,
            store=self.store
        )
```

### Step 4: Implement Learning in Debug Agent

```python
# mcp_codegen/agents/debug_agent.py
import uuid
from agents.learning_memory import store

class DebugAgent:
    def __init__(self, rag_store, langgraph_store):
        self.rag = rag_store  # ChromaDB
        self.store = langgraph_store  # LangGraph Store
    
    async def fix_error(self, code: str, error: str, context: dict = None):
        """Debug with learning."""
        
        # 1. Search both stores
        similar_fixes = await self._search_stores(error, code)
        
        # 2. Generate fix with context
        fix = await self._generate_fix(code, error, similar_fixes)
        
        # 3. Test the fix
        success = await self._test_fix(fix['fixed_code'])
        
        # 4. If successful, LEARN from it
        if success:
            await self._learn_from_success(error, fix, context)
        
        return fix
    
    async def _search_stores(self, error: str, code_context: str):
        """Search both RAG and LangGraph stores."""
        
        # Search LangGraph Store
        namespace = ("error_fixes", self.session_id)
        memories = await self.store.asearch(
            namespace,
            query=f"Error: {error}\nCode: {code_context[:200]}",
            limit=5
        )
        
        # Search RAG Store
        rag_results = self.rag.retrieve_similar(
            f"Error: {error}",
            n_results=5
        )
        
        # Combine results
        return {
            "memories": [m.value for m in memories],
            "rag_examples": rag_results['examples'],
            "metadata": rag_results['metadata']
        }
    
    async def _learn_from_success(self, error: str, fix: dict, context: dict):
        """Store successful fix for future reference."""
        import uuid
        
        # Store in LangGraph Store
        namespace = ("error_fixes", self.session_id)
        memory_id = str(uuid.uuid4())
        
        await self.store.aput(
            namespace,
            memory_id,
            {
                "error": error,
                "solution": fix['fixed_code'],
                "explanation": fix['explanation'],
                "context": context,
                "success_count": 1,
                "first_success": datetime.utcnow().isoformat()
            }
        )
        
        # Store in RAG Store
        self.rag.add_code_example(
            code=fix['fixed_code'],
            metadata={
                "type": "error_fix",
                "error_pattern": error,
                "language": fix.get('language', 'python'),
                "framework": context.get('framework'),
                "successful": True
            }
        )
```

### Step 5: Add Metadata Tracking

```python
# agents/learning_tracker.py
class LearningTracker:
    """Track what the system learns over time."""
    
    def __init__(self, store):
        self.store = store
    
    async def record_pattern(self, category: str, pattern: dict):
        """Record a learned pattern."""
        namespace = ("learned_patterns", category)
        memory_id = str(uuid.uuid4())
        
        await self.store.aput(
            namespace,
            memory_id,
            {
                "pattern": pattern,
                "first_seen": datetime.utcnow().isoformat(),
                "occurrences": 1,
                "success_rate": 1.0
            }
        )
    
    async def update_pattern(self, pattern_id: str, success: bool):
        """Update pattern statistics."""
        pattern = await self.store.aget(namespace, pattern_id)
        pattern['occurrences'] += 1
        if success:
            pattern['success_rate'] = (
                pattern.get('success_count', 0) + 1
            ) / pattern['occurrences']
        
        await self.store.aput(namespace, pattern_id, pattern)
```

## Learning Scenarios

### Scenario 1: Error-Fix Learning

```python
# User: "I'm getting ImportError: No module named 'flask'"
# Agent: [searches stores, finds no exact match]
# Agent: [generates fix: add flask to requirements.txt]
# User: "That worked!"
# Agent: [learns: ImportError flask → add to requirements.txt]
# 
# Next time:
# User: "I'm getting ImportError: No module named 'requests'"
# Agent: [finds similar pattern for flask]
# Agent: "I remember seeing this before..."
```

### Scenario 2: Pattern Recognition

```python
# Agent learns common patterns:
# - "User forgot to install dependencies" (50 occurrences)
# - "Missing environment variable" (30 occurrences)
# - "Database connection issue" (20 occurrences)

# Agent uses frequency to prioritize solutions
```

### Scenario 3: Context-Aware Learning

```python
# Agent learns contextual patterns:
# - Flask projects: Common issue X, solution Y
# - Django projects: Common issue A, solution B
# - FastAPI projects: Common issue P, solution Q

# Next Flask project: Agent immediately suggests Y
```

### Scenario 4: Cross-Session Learning

```python
# Session 1: User A fixes Flask CORS issue
# Session 2: User B encounters same issue
# Agent: "I've seen this before, here's the solution that worked"
```

## Advanced Features

### 1. Success Rate Tracking

```python
# Track which solutions work best
{
    "error": "ImportError",
    "solutions": [
        {
            "fix": "Add to requirements.txt",
            "success_rate": 0.95,  # Works 95% of time
            "occurrences": 100
        },
        {
            "fix": "pip install",
            "success_rate": 0.60,  # Works 60% of time
            "occurrences": 50
        }
    ]
}
```

### 2. Temporal Learning

```python
# Learn from recent trends
{
    "recent_pattern": "Python 3.12 users have asyncio issues",
    "emerging_solution": "Update event loop policy",
    "first_seen": "2024-01-15",
    "frequency_increasing": True
}
```

### 3. A/B Testing Solutions

```python
# Try multiple solutions, learn which is best
async def learn_best_solution(self, error, solutions):
    results = []
    for solution in solutions:
        success = await self._test_solution(solution)
        results.append({
            "solution": solution,
            "success": success,
            "time": time_taken
        })
    
    # Rank solutions by effectiveness
    best = sorted(results, key=lambda x: x['success'] and -x['time'])
    await self._remember_best(error, best[0])
```

### 4. Confidence Scoring

```python
def calculate_confidence(self, memory_match):
    """Calculate confidence in memory-based solution."""
    base_score = memory_match.distance  # Similarity
    success_rate = memory_match.value['success_rate']
    occurrences = memory_match.value['occurrences']
    
    # More occurrences = higher confidence
    occurrence_boost = min(occurrences / 100, 1.0)
    
    # Higher success rate = higher confidence
    success_boost = success_rate
    
    confidence = base_score * occurrence_boost * success_boost
    return confidence
```

## Production Setup

### Persistent Storage

```python
# Use Postgres for production
from langgraph.checkpoint.postgres import PostgresSaver, PostgresStore

DB_URI = "postgresql://user:pass@localhost/orchestrator"

store = PostgresStore.from_conn_string(DB_URI)
checkpointer = PostgresSaver.from_conn_string(DB_URI)

# Setup tables (first time only)
await store.setup()
await checkpointer.setup()
```

### Namespace Organization

```python
# Organize memories by namespace
namespaces = {
    ("error_fixes", "python"): "Python-specific errors",
    ("error_fixes", "flask"): "Flask framework errors",
    ("patterns", "api_design"): "API design patterns",
    ("solutions", "performance"): "Performance optimizations",
    ("learned_rules", "coding"): "Learned coding rules"
}
```

## Integration with Existing System

### Update Orchestrator

```python
# agents/orchestrator.py
from agents.learning_memory import store, checkpointer

class Orchestrator:
    def __init__(self):
        self.store = store
        self.checkpointer = checkpointer
        self._graph = None
    
    def build_graph(self):
        # ... define graph ...
        
        self._graph = graph.compile(
            checkpointer=self.checkpointer,
            store=self.store
        )
```

### Update MCP Server

```python
# mcp_codegen/server.py
from agents.learning_memory import store

@app.list_tools()
async def list_tools():
    return [
        # ... existing tools ...
        Tool(
            name="learn_from_fix",
            description="Store a successful fix for future reference",
            inputSchema={
                "type": "object",
                "properties": {
                    "error": {"type": "string"},
                    "fix": {"type": "string"},
                    "context": {"type": "object"}
                }
            }
        )
    ]
```

## Measuring Learning Success

### Metrics to Track

```python
{
    "total_patterns_learned": 156,
    "patterns_used": 89,
    "success_rate": 0.94,
    "average_solve_time": "12.3s",
    "confidence_trend": "increasing",
    "most_learned_category": "error_fixes",
    "patterns_by_framework": {
        "flask": 45,
        "django": 32,
        "fastapi": 18
    }
}
```

## Benefits

### 1. Faster Problem Solving
- No need to generate from scratch
- Immediate retrieval of proven solutions

### 2. Higher Success Rate
- Only reuse patterns that work
- Avoid repeating failed attempts

### 3. Domain Expertise
- Becomes expert in your specific domain
- Learns your team's patterns and conventions

### 4. Continuous Improvement
- Gets better with every interaction
- Adapts to your project's needs

## Next Steps

1. ✅ Add LangGraph Store to orchestrator
2. ✅ Configure semantic search
3. ✅ Add checkpointer for state
4. ✅ Implement learning in debug agent
5. ✅ Add success tracking
6. ✅ Monitor metrics
7. ✅ Iterate on learning strategies

## References

- [LangGraph Persistence Docs](https://langchain-ai.github.io/langgraph/how-tos/memory/add-memory/)
- [LangGraph Store API](https://langchain-ai.github.io/langgraph/concepts/persistence/)
- [Postgres Checkpoint](https://python.langchain.com/docs/langgraph_checkpoint_postgres)

---

**Your system will now learn and improve with every interaction!** 🚀

