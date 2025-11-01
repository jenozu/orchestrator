"""Code generator tool with RAG context."""
import json
from mcp_codegen.agents.code_agent import CodeAgent


class GeneratorTool:
    """Generate projects from requirements using RAG."""
    
    def __init__(self, rag_store):
        self.generator = CodeAgent(rag_store)
    
    async def generate(self, requirements: dict, output_dir: str) -> str:
        """Generate project files."""
        files = await self.generator.generate_project(requirements, output_dir)
        return json.dumps({"files_created": files}, indent=2)

