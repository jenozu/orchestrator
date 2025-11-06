"""Check knowledge base status and document count."""
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def check_kb_status():
    """Check if knowledge base has documents."""
    print("="*60)
    print("KNOWLEDGE BASE STATUS CHECK")
    print("="*60)
    
    try:
        from agents.rag_retrieval import get_rag_store
        
        rag_store = get_rag_store()
        
        if not rag_store.initialized:
            print("[WARN] RAG Store: Not initialized")
            print("   -> Set OPENAI_API_KEY and try again")
            return
        
        print(f"[OK] RAG Store: Initialized")
        print(f"   Collection: {rag_store.collection_name}")
        print(f"   Location: {rag_store.chroma_dir}")
        
        # Check document count
        if rag_store.collection:
            try:
                # Count documents in collection
                count_result = rag_store.collection.count()
                print(f"\n[INFO] Documents in KB: {count_result}")
                
                if count_result == 0:
                    print("\n[WARN] Knowledge base is EMPTY!")
                    print("   -> Run: python scripts/ingest_knowledge_base.py --local-only")
                    print("   -> This will populate the KB with local documentation")
                else:
                    print(f"\n[OK] Knowledge base has {count_result} documents")
                    
                    # Show domain breakdown
                    print("\n[INFO] Checking domain distribution...")
                    try:
                        # Get all documents to check metadata
                        all_docs = rag_store.collection.get()
                        if all_docs and all_docs.get('metadatas'):
                            domains = {}
                            for metadata in all_docs['metadatas']:
                                domain = metadata.get('domain', 'unknown')
                                domains[domain] = domains.get(domain, 0) + 1
                            
                            print("\n   Documents by domain:")
                            for domain, count in sorted(domains.items()):
                                print(f"     {domain}: {count}")
                        else:
                            print("   [WARN] Could not retrieve metadata")
                    except Exception as e:
                        print(f"   [WARN] Could not check domain distribution: {e}")
                
            except Exception as e:
                print(f"\n[ERROR] Could not count documents: {e}")
        else:
            print("\n[WARN] Collection not available")
            
    except Exception as e:
        print(f"[ERROR] Error checking KB status: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "="*60)

if __name__ == "__main__":
    check_kb_status()

