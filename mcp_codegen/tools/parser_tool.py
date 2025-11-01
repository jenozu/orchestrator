"""Parser tool for extracting requirements from documents."""
import json
from mcp_codegen.agents.parser_agent import ParserAgent


class ParserTool:
    """Parse PRD/README documents into structured requirements."""
    
    def __init__(self):
        self.parser = ParserAgent()
    
    async def parse(self, doc_path: str) -> str:
        """Parse document and return structured requirements."""
        requirements = await self.parser.parse_prd(doc_path)
        return json.dumps(requirements, indent=2)

