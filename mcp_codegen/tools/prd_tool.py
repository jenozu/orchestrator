"""PRD tool for creating product requirements documents."""
import json
from mcp_codegen.agents.prd_agent import PRDAgent


class PRDTool:
    """Create PRD documents from user ideas."""
    
    def __init__(self):
        self.prd_agent = PRDAgent()
    
    async def create(self, idea: str, output_path: str = "docs/generated_prd.md") -> str:
        """Create a PRD document from an idea."""
        result = await self.prd_agent.create_prd(idea, output_path)
        return json.dumps(result, indent=2)

