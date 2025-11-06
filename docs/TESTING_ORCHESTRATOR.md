# Testing the Orchestrator System

This guide explains how to test the complete orchestrator system with domain-specific knowledge base (RAG) integration.

## Prerequisites Checklist

Before testing, ensure you have:

### ✅ Required Setup

- [ ] **Python Environment**: Virtual environment activated
- [ ] **Dependencies Installed**: `pip install -r requirements.txt`
- [ ] **OpenAI API Key**: Set `OPENAI_API_KEY` environment variable
- [ ] **ChromaDB**: Installed (via requirements.txt)
- [ ] **LangGraph**: Installed (for orchestrator graph)

### ✅ Knowledge Base Status

- [ ] **KB Populated**: Run ingestion script (optional, but recommended)
- [ ] **Local Docs Created**: 13+ documents in `docs/` directories
- [ ] **Context7 Docs**: Optional - can fetch later

## Quick Test: Verify Setup

### Test 1: Verify Imports

```bash
python -c "from agents.orchestrator import Orchestrator; print('✅ Orchestrator imports OK')"
python -c "from agents.subagents.intent_parser import run_task; print('✅ IntentParser imports OK')"
python -c "from agents.rag_retrieval import retrieve_knowledge; print('✅ RAG retrieval imports OK')"
```

### Test 2: Check RAG Store Initialization

```python
from agents.rag_retrieval import get_rag_store

rag_store = get_rag_store()
print(f"RAG Store Initialized: {rag_store.initialized}")
```

### Test 3: Verify Knowledge Base (Optional)

If you've populated the KB:

```python
from agents.rag_retrieval import retrieve_knowledge

# Test retrieval
context = retrieve_knowledge(
    query="How to create API endpoints?",
    agent_domain="backend"
)
print(f"Retrieved context length: {len(context)} chars")
```

## Testing the Orchestrator

### Test 1: Basic Orchestrator Execution

**File**: Create `test_orchestrator_basic.py`

```python
"""Basic orchestrator test."""
from agents.orchestrator import Orchestrator

def test_basic_orchestrator():
    """Test that orchestrator can be created and run."""
    # Create orchestrator
    orch = Orchestrator()
    
    # Build graph
    orch.build_graph()
    
    # Run with minimal state
    result = orch.run_once({"raw_user_request": "Build a todo app"})
    
    print("Orchestrator Result:")
    print(result)
    
    # Verify result structure
    assert "parsed_intent" in result or "status" in result
    print("✅ Orchestrator executed successfully")
    
    return result

if __name__ == "__main__":
    test_basic_orchestrator()
```

**Run**:
```bash
python test_orchestrator_basic.py
```

**Expected Output**:
- Should show `parsed_intent` with structured JSON
- May show `knowledge_retrieved: True` if KB is populated

### Test 2: IntentParser Integration

**File**: Create `test_intent_parser.py`

```python
"""Test IntentParser agent."""
from agents.subagents.intent_parser import run_task

def test_intent_parser():
    """Test IntentParser with sample request."""
    inputs = {
        "raw_user_request": "Build a todo app with user authentication, task CRUD operations, and filtering by status"
    }
    
    result = run_task(inputs)
    
    print("IntentParser Result:")
    print(result)
    
    # Verify structure
    assert "parsed_intent" in result
    assert result["parsed_intent"] is not None
    
    parsed = result["parsed_intent"]
    print(f"\n✅ Parsed Intent Structure:")
    print(f"  Project Description: {parsed.get('project_description', 'N/A')[:50]}...")
    print(f"  Required Features: {len(parsed.get('required_features', []))} features")
    
    return result

if __name__ == "__main__":
    test_intent_parser()
```

**Run**:
```bash
python test_intent_parser.py
```

### Test 3: Subagent with RAG Retrieval

**File**: Create `test_subagent_rag.py`

```python
"""Test subagent with RAG retrieval."""
from agents.subagents.backend import run_task

def test_backend_agent_with_rag():
    """Test backend agent retrieves knowledge."""
    # Simulate parsed intent from IntentParser
    inputs = {
        "parsed_intent": {
            "project_description": "Build a REST API for task management",
            "required_features": [
                "Create task endpoint",
                "List tasks endpoint",
                "Update task endpoint"
            ]
        }
    }
    
    result = run_task(inputs)
    
    print("Backend Agent Result:")
    print(result)
    
    # Check if RAG was used
    if result.get("knowledge_retrieved"):
        print(f"\n✅ RAG Retrieval Successful!")
        print(f"  Context Length: {result.get('context_length', 0)} chars")
    else:
        print("\n⚠️  RAG not retrieved (KB may be empty or API key not set)")
    
    return result

if __name__ == "__main__":
    test_backend_agent_with_rag()
```

**Run**:
```bash
python test_subagent_rag.py
```

### Test 4: End-to-End Workflow

**File**: Create `test_end_to_end.py`

```python
"""End-to-end orchestrator test."""
from agents.orchestrator import Orchestrator

def test_end_to_end():
    """Test complete workflow from user request to agent execution."""
    
    # User request
    user_request = "Create a simple todo app with add, complete, and delete features"
    
    print(f"User Request: {user_request}\n")
    print("="*60)
    
    # Initialize orchestrator
    orch = Orchestrator()
    orch.build_graph()
    
    # Execute with user request
    initial_state = {
        "raw_user_request": user_request
    }
    
    print("\nExecuting Orchestrator...")
    result = orch.run_once(initial_state)
    
    print("\n" + "="*60)
    print("FINAL RESULT")
    print("="*60)
    print(result)
    
    # Verify workflow
    if "parsed_intent" in result:
        print("\n✅ IntentParser executed")
        parsed = result["parsed_intent"]
        if parsed:
            print(f"✅ Parsed Intent: {parsed.get('project_description', 'N/A')[:50]}...")
    
    return result

if __name__ == "__main__":
    test_end_to_end()
```

**Run**:
```bash
python test_end_to_end.py
```

## Testing with Knowledge Base

### Step 1: Populate Knowledge Base (Recommended)

```bash
# Set API key first
$env:OPENAI_API_KEY="your-key-here"  # PowerShell
# or
export OPENAI_API_KEY="your-key-here"  # Bash

# Ingest local documentation
python scripts/ingest_knowledge_base.py --local-only
```

### Step 2: Test RAG Retrieval

```python
from agents.rag_retrieval import retrieve_knowledge

# Test backend KB
context = retrieve_knowledge("FastAPI endpoint creation", "backend")
print(f"Backend KB: {len(context)} chars retrieved")

# Test frontend KB
context = retrieve_knowledge("React component patterns", "frontend")
print(f"Frontend KB: {len(context)} chars retrieved")

# Test shared KB
context = retrieve_knowledge("coding standards", "shared")
print(f"Shared KB: {len(context)} chars retrieved")
```

### Step 3: Test Agents with RAG

Run the subagent tests above. They should now show:
- `knowledge_retrieved: True`
- `context_length: > 0`

## Expected Test Results

### ✅ Success Indicators

1. **Orchestrator**:
   - Creates graph successfully
   - Executes without errors
   - Returns structured state

2. **IntentParser**:
   - Parses user requests into JSON
   - Extracts project description and features
   - Returns valid `parsed_intent`

3. **Subagents**:
   - Read from `parsed_intent`
   - Retrieve knowledge from KB (if populated)
   - Return structured outputs

4. **RAG System**:
   - Initializes ChromaDB connection
   - Retrieves domain-scoped knowledge
   - Returns relevant context

### ⚠️ Common Issues

1. **"OPENAI_API_KEY not set"**
   - Set environment variable
   - Required for RAG embeddings and LLM calls

2. **"ChromaDB not available"**
   - Install: `pip install chromadb`
   - Check ChromaDB directory permissions

3. **"No documents retrieved"**
   - Run ingestion script first
   - Verify documents are in `docs/` directories
   - Check domain names match exactly

4. **"LangGraph not installed"**
   - Install: `pip install langgraph`
   - Orchestrator will fall back to simple execution

## Advanced Testing

### Test Multiple Agents in Sequence

```python
from agents.subagents.intent_parser import run_task as run_intent_parser
from agents.subagents.prd import run_task as run_prd
from agents.subagents.backend import run_task as run_backend

# Simulate full workflow
user_request = "Build a todo app"

# Step 1: Parse intent
intent_result = run_intent_parser({"raw_user_request": user_request})
parsed_intent = intent_result["parsed_intent"]

# Step 2: Generate PRD
prd_result = run_prd({"parsed_intent": parsed_intent})
print(f"PRD: {prd_result}")

# Step 3: Scaffold backend
backend_result = run_backend({"parsed_intent": parsed_intent})
print(f"Backend: {backend_result}")
```

### Test Domain Filtering

```python
from agents.rag_retrieval import retrieve_knowledge

# Should only get backend + shared docs
backend_context = retrieve_knowledge("API patterns", "backend")

# Should only get frontend + shared docs  
frontend_context = retrieve_knowledge("API patterns", "frontend")

# Verify they're different (if KB populated)
print(f"Backend context length: {len(backend_context)}")
print(f"Frontend context length: {len(frontend_context)}")
```

## What's Ready vs. What's Not

### ✅ Ready for Testing

- ✅ Orchestrator structure
- ✅ IntentParser agent
- ✅ All subagents (PRD, Diagrammer, Backend, Frontend, QA)
- ✅ RAG retrieval system
- ✅ Domain-scoped knowledge bases
- ✅ Agent prompts with RAG instructions

### ⚠️ Partial Implementation

- ⚠️ **LLM Integration**: Agents have structure but may need actual LLM calls
- ⚠️ **Knowledge Base**: Needs population (ingestion script ready)
- ⚠️ **Orchestrator Graph**: Currently only has IntentParser → END

### 🔨 Not Yet Implemented

- 🔨 **Full Graph**: PRD, Diagrammer, Backend, Frontend nodes not connected
- 🔨 **Parallel Execution**: Agents run sequentially
- 🔨 **Code Generation**: Agents return placeholders, not actual code

## Next Steps After Testing

1. **If KB is empty**: Populate it using ingestion script
2. **If agents return placeholders**: Add LLM integration to agents
3. **If graph is incomplete**: Connect all subagents to orchestrator
4. **If RAG not working**: Verify API key and ChromaDB setup

## Quick Test Script

Create `quick_test.py`:

```python
"""Quick test of orchestrator system."""
import os
from agents.orchestrator import Orchestrator
from agents.rag_retrieval import get_rag_store

def quick_test():
    print("="*60)
    print("ORCHESTRATOR SYSTEM QUICK TEST")
    print("="*60)
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"✅ OPENAI_API_KEY: Set ({api_key[:10]}...)")
    else:
        print("⚠️  OPENAI_API_KEY: Not set (RAG will be disabled)")
    
    # Check RAG store
    rag_store = get_rag_store()
    print(f"✅ RAG Store: {'Initialized' if rag_store.initialized else 'Not initialized'}")
    
    # Test orchestrator
    print("\nTesting Orchestrator...")
    orch = Orchestrator()
    orch.build_graph()
    
    result = orch.run_once({
        "raw_user_request": "Build a simple todo app"
    })
    
    print("\nResult Keys:", list(result.keys()))
    if "parsed_intent" in result:
        print("✅ IntentParser: Executed")
        if result["parsed_intent"]:
            print(f"   Project: {result['parsed_intent'].get('project_description', 'N/A')[:50]}")
    else:
        print("⚠️  IntentParser: Not executed or returned error")
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)

if __name__ == "__main__":
    quick_test()
```

**Run**:
```bash
python quick_test.py
```

## Summary

The orchestrator system is **ready for basic testing** but needs:

1. **API Key**: Set `OPENAI_API_KEY` for RAG and LLM calls
2. **Knowledge Base**: Optional but recommended - populate with `ingest_knowledge_base.py`
3. **Dependencies**: Install all requirements

**Minimum test**: Run `quick_test.py` to verify basic functionality
**Full test**: Populate KB, then run all test scripts above

