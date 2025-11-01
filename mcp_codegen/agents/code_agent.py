"""Code generation agent with RAG context."""
from typing import List, Dict, Any
from openai import OpenAI
from mcp_codegen.config import OPENAI_API_KEY, CODE_MODEL
from mcp_codegen.rag.store import RAGStore


class CodeAgent:
    """Generate code using LLM with RAG context."""
    
    def __init__(self, rag_store: RAGStore):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.rag = rag_store
    
    async def generate_project(self, requirements: Dict[str, Any], output_dir: str) -> List[str]:
        """Generate complete project from requirements."""
        # TODO: Implement actual code generation
        # For now, return empty list
        return []

