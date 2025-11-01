"""Debugger agent for fixing code errors with learning."""
from typing import Dict, Any, Optional
from openai import OpenAI
from mcp_codegen.config import OPENAI_API_KEY, CODE_MODEL
from mcp_codegen.rag.store import RAGStore

try:
    from agents.learning_memory import get_learning_memory
    LEARNING_AVAILABLE = True
except ImportError:
    LEARNING_AVAILABLE = False


class DebugAgent:
    """Debug and fix code errors using LLM with RAG and learning."""
    
    def __init__(self, rag_store: RAGStore):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        self.rag = rag_store
        self.learning_memory = get_learning_memory() if LEARNING_AVAILABLE else None
    
    async def fix_error(
        self,
        code: str,
        error: str,
        context: Dict[str, Any] = None,
        record_learning: bool = True
    ) -> Dict[str, Any]:
        """Analyze error and propose fix with learning support.
        
        Args:
            code: The problematic code
            error: Error message
            context: Additional context
            record_learning: Whether to learn from this fix
        
        Returns:
            Dict with fixed_code, explanation, and changes
        """
        context = context or {}
        similar_solutions = []
        
        # 1. Search learned solutions from LangGraph Store
        if self.learning_memory:
            similar_solutions = await self.learning_memory.search_solutions(
                category="error_fixes",
                query=f"Error: {error}\nCode: {code[:200]}",
                limit=3
            )
        
        # 2. Search RAG store for code patterns
        rag_results = self.rag.retrieve_similar(f"Error: {error}", n_results=3)
        
        # 3. Combine search results for context
        all_context = {
            "similar_solutions": similar_solutions,
            "rag_examples": rag_results.get('examples', []),
            "metadata": rag_results.get('metadata', [])
        }
        
        # 4. Generate fix with context
        fix_result = await self._generate_fix(code, error, all_context)
        
        # 5. If successful, learn from it
        if record_learning and self.learning_memory:
            success = await self._validate_fix(fix_result)
            if success:
                await self._learn_from_fix(error, fix_result, context)
        
        return fix_result
    
    async def _generate_fix(
        self,
        code: str,
        error: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Generate fix using LLM with context."""
        # Build context string
        context_str = ""
        if context.get("similar_solutions"):
            context_str += "\n\nSimilar solutions I've seen before:\n"
            for sol in context["similar_solutions"][:3]:
                context_str += f"- {sol.get('solution', '')}\n"
        
        if context.get("rag_examples"):
            context_str += "\n\nSimilar code patterns:\n"
            for ex in context["rag_examples"][:2]:
                context_str += f"- {ex[:150]}...\n"
        
        # TODO: Implement actual LLM call
        # For now, return skeleton with context
        return {
            "fixed_code": code,
            "explanation": f"TODO: Implement fix with LLM. Context: {len(context_str)} chars of similar solutions",
            "changes": [],
            "context_used": len(context.get("similar_solutions", [])) > 0
        }
    
    async def _validate_fix(self, fix_result: Dict[str, Any]) -> bool:
        """Validate that the fix is correct."""
        # TODO: Implement actual validation (run code, check for errors)
        return True  # Placeholder
    
    async def _learn_from_fix(
        self,
        error: str,
        fix_result: Dict[str, Any],
        context: Dict[str, Any]
    ) -> None:
        """Learn from successful fix."""
        if not self.learning_memory:
            return
        
        await self.learning_memory.learn_from_success(
            category="error_fixes",
            error=error,
            solution=fix_result.get("fixed_code", ""),
            context={
                **context,
                "explanation": fix_result.get("explanation", ""),
                "changes": fix_result.get("changes", [])
            },
            success=True
        )
        
        # Also add to RAG store for deep semantic search
        self.rag.add_code_example(
            code=fix_result.get("fixed_code", ""),
            metadata={
                "type": "error_fix",
                "error_pattern": error[:100],
                "successful": True,
                "learned": True
            }
        )

