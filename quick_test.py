"""Quick test of orchestrator system."""
import os
import sys
from pathlib import Path

# Load environment variables from .env file if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def quick_test():
    print("="*60)
    print("ORCHESTRATOR SYSTEM QUICK TEST")
    print("="*60)
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        print(f"[OK] OPENAI_API_KEY: Set ({api_key[:10]}...)")
    else:
        print("[WARN] OPENAI_API_KEY: Not set (RAG will be disabled)")
    
    # Check RAG store
    try:
        from agents.rag_retrieval import get_rag_store
        rag_store = get_rag_store()
        print(f"[OK] RAG Store: {'Initialized' if rag_store.initialized else 'Not initialized (API key needed)'}")
    except Exception as e:
        print(f"[WARN] RAG Store: Error - {e}")
    
    # Test orchestrator
    print("\nTesting Orchestrator...")
    try:
        from agents.orchestrator import Orchestrator
        orch = Orchestrator()
        orch.build_graph()
        print("[OK] Orchestrator: Created and graph built")
        
        result = orch.run_once({
            "raw_user_request": "Build a simple todo app"
        })
        
        print("\nResult Keys:", list(result.keys()))
        if "parsed_intent" in result:
            print("[OK] IntentParser: Executed")
            if result["parsed_intent"]:
                parsed = result["parsed_intent"]
                print(f"   Project: {parsed.get('project_description', 'N/A')[:50]}")
                print(f"   Features: {len(parsed.get('required_features', []))} features")
            else:
                print("[WARN] Parsed intent is None (check error field)")
        elif "error" in result:
            print(f"[ERROR] Error: {result.get('error')}")
        else:
            print("[WARN] IntentParser: May not have executed")
        
        # Test subagents
        print("\nTesting Subagents...")
        try:
            from agents.subagents.backend import run_task as run_backend
            test_input = {
                "parsed_intent": {
                    "project_description": "Test project",
                    "required_features": ["Feature 1"]
                }
            }
            backend_result = run_backend(test_input)
            print(f"[OK] Backend Agent: Executed (knowledge_retrieved: {backend_result.get('knowledge_retrieved', False)})")
        except Exception as e:
            print(f"[WARN] Backend Agent: Error - {e}")
        
    except Exception as e:
        print(f"[ERROR] Orchestrator: Error - {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)
    print("TEST COMPLETE")
    print("="*60)
    print("\nNext Steps:")
    print("1. Set OPENAI_API_KEY if not set")
    print("2. Populate KB: python scripts/ingest_knowledge_base.py --local-only")
    print("3. Run full tests: See docs/TESTING_ORCHESTRATOR.md")

if __name__ == "__main__":
    quick_test()

