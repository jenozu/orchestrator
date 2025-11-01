"""Debugger tool for fixing errors."""
import json
from mcp_codegen.agents.debug_agent import DebugAgent


class DebuggerTool:
    """Debug and fix code errors."""
    
    def __init__(self, rag_store):
        self.debugger = DebugAgent(rag_store)
    
    async def fix(self, code: str, error: str, context: dict = None) -> str:
        """Analyze error and propose fix."""
        fix_result = await self.debugger.fix_error(code, error, context or {})
        return json.dumps(fix_result, indent=2)

