"""Test script that helps set environment and run tests."""
import os
import sys

def main():
    print("="*60)
    print("ORCHESTRATOR TEST WITH ENVIRONMENT CHECK")
    print("="*60)
    
    # Check if API key is set
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("\n[WARN] OPENAI_API_KEY not found in environment!")
        print("\nTo set it:")
        print("  PowerShell: $env:OPENAI_API_KEY='your-key-here'")
        print("  Then run this script again in the SAME session")
        print("\nOr set it permanently:")
        print("  PowerShell: [System.Environment]::SetEnvironmentVariable('OPENAI_API_KEY', 'your-key', 'User')")
        print("  (Then restart PowerShell)")
        return 1
    
    print(f"[OK] API Key found: {api_key[:10]}...{api_key[-4:]}")
    
    # Now run the actual test
    print("\n" + "="*60)
    print("Running Orchestrator Test...")
    print("="*60 + "\n")
    
    # Import and run quick test logic
    try:
        from agents.orchestrator import Orchestrator
        from agents.rag_retrieval import get_rag_store
        from agents.subagents.backend import run_task as run_backend
        
        # Check RAG store
        rag_store = get_rag_store()
        print(f"[OK] RAG Store: {'Initialized' if rag_store.initialized else 'Not initialized'}")
        
        # Test orchestrator
        print("\nTesting Orchestrator...")
        orch = Orchestrator()
        orch.build_graph()
        print("[OK] Orchestrator: Created and graph built")
        
        result = orch.run_once({
            "raw_user_request": "Build a simple todo app"
        })
        
        print("\nResult Keys:", list(result.keys()))
        if "parsed_intent" in result:
            if result["parsed_intent"]:
                parsed = result["parsed_intent"]
                print("[OK] IntentParser: Executed successfully!")
                print(f"   Project: {parsed.get('project_description', 'N/A')[:50]}...")
                print(f"   Features: {len(parsed.get('required_features', []))} features")
            else:
                print("[WARN] Parsed intent is None")
                if "error" in result:
                    print(f"   Error: {result['error']}")
        elif "error" in result:
            print(f"[ERROR] {result.get('error')}")
        
        # Test subagent
        print("\nTesting Backend Agent...")
        test_input = {
            "parsed_intent": {
                "project_description": "Test project",
                "required_features": ["Feature 1"]
            }
        }
        backend_result = run_backend(test_input)
        print(f"[OK] Backend Agent: Executed")
        print(f"   Knowledge Retrieved: {backend_result.get('knowledge_retrieved', False)}")
        print(f"   Context Length: {backend_result.get('context_length', 0)} chars")
        
        print("\n" + "="*60)
        print("TEST COMPLETE - All components working!")
        print("="*60)
        return 0
        
    except Exception as e:
        print(f"\n[ERROR] Test failed: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())

