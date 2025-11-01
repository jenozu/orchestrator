"""RAG tool for retrieving similar code patterns."""
import json
from mcp_codegen.rag.store import RAGStore


class RAGTool:
    """Retrieve similar code examples via RAG."""
    
    def __init__(self):
        self.rag_store = RAGStore()
    
    async def retrieve(self, query: str, k: int = 5) -> str:
        """Retrieve k similar code examples."""
        results = self.rag_store.retrieve_similar(query, k)
        return json.dumps(results, indent=2)

