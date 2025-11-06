"""Quick test to demonstrate MCP and Knowledge Base integration."""
import os
import sys
from pathlib import Path

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

from agents.rag_retrieval import get_rag_store, retrieve_knowledge

def test_knowledge_base():
    """Test the knowledge base retrieval."""
    print("="*60)
    print("MCP & KNOWLEDGE BASE TEST")
    print("="*60)
    
    # Initialize RAG store
    print("\n1. Initializing RAG store...")
    rag_store = get_rag_store()
    
    if not rag_store.initialized:
        print("❌ RAG store failed to initialize. Check OPENAI_API_KEY in .env")
        return False
    
    print("✅ RAG store initialized")
    print(f"   Location: {rag_store.chroma_dir}")
    print(f"   Documents: {rag_store.collection.count() if rag_store.collection else 0}")
    
    # Test knowledge retrieval for different domains
    print("\n2. Testing knowledge retrieval...")
    
    test_queries = [
        ("backend", "How do I create a FastAPI route?"),
        ("frontend", "How do I use React hooks?"),
        ("qa", "How do I write a Playwright test?"),
        ("orchestrator", "How do I use LangChain agents?"),
    ]
    
    for domain, query in test_queries:
        print(f"\n   Query ({domain}): {query}")
        context = retrieve_knowledge(query, domain, top_k=2)
        
        if context:
            print(f"   ✅ Retrieved {len(context)} characters of context")
            print(f"   Preview: {context[:150]}...")
        else:
            print(f"   ⚠️  No context retrieved (might be normal if query doesn't match)")
    
    print("\n3. Testing domain-scoped filtering...")
    
    # Test that backend queries don't return frontend docs
    backend_context = retrieve_knowledge("React components", "backend", top_k=3)
    frontend_context = retrieve_knowledge("React components", "frontend", top_k=3)
    
    print(f"\n   Backend query for 'React components':")
    print(f"   Retrieved: {len(backend_context)} chars (should be minimal/shared only)")
    
    print(f"\n   Frontend query for 'React components':")
    print(f"   Retrieved: {len(frontend_context)} chars (should include React docs)")
    
    print("\n" + "="*60)
    print("✅ KNOWLEDGE BASE TEST COMPLETE")
    print("="*60)
    print("\nThe MCP server can now use this knowledge base when:")
    print("  - Generating code (retrieve_context tool)")
    print("  - Debugging errors (RAG-powered suggestions)")
    print("  - Creating projects (domain-specific knowledge)")
    print("\nTo test MCP tools directly, ask me in Cursor chat:")
    print("  'Parse docs/my_todo_prd.md'")
    print("  'Generate a PRD for a budget tracking app'")
    print("  'Retrieve context about FastAPI routing'")
    
    return True

if __name__ == "__main__":
    success = test_knowledge_base()
    sys.exit(0 if success else 1)

