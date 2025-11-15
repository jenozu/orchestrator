"""MCP server for document-to-code generation with RAG and learning."""
from dotenv import load_dotenv
load_dotenv()

import asyncio
import json
from mcp.server import Server
from mcp.types import Tool, TextContent

from mcp_codegen.tools.parser_tool import ParserTool
from mcp_codegen.tools.rag_tool import RAGTool
from mcp_codegen.tools.generator_tool import GeneratorTool
from mcp_codegen.tools.debugger_tool import DebuggerTool
from mcp_codegen.tools.prd_tool import PRDTool

app = Server("codegen")

# Initialize tools
parser = ParserTool()
rag_tool = RAGTool()
generator = GeneratorTool(rag_tool.rag_store)
debugger = DebuggerTool(rag_tool.rag_store)
prd_tool = PRDTool()

# Import learning memory if available
try:
    from agents.learning_memory import get_learning_memory
    LEARNING_AVAILABLE = True
    learning_memory = get_learning_memory()
except ImportError:
    LEARNING_AVAILABLE = False
    learning_memory = None


@app.list_tools()
async def list_tools():
    """List all available tools."""
    return [
        Tool(
            name="create_prd",
            description="Create a Product Requirements Document (PRD) from an idea",
            inputSchema={
                "type": "object",
                "properties": {
                    "idea": {"type": "string"},
                    "output_path": {"type": "string", "default": "docs/generated_prd.md"}
                },
                "required": ["idea"]
            }
        ),
        Tool(
            name="parse_prd",
            description="Parse PRD or README into structured requirements",
            inputSchema={
                "type": "object",
                "properties": {
                    "document_path": {"type": "string"}
                },
                "required": ["document_path"]
            }
        ),
        Tool(
            name="retrieve_context",
            description="Retrieve similar code patterns via RAG",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "k": {"type": "integer", "default": 5}
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="generate_project",
            description="Generate complete project from requirements",
            inputSchema={
                "type": "object",
                "properties": {
                    "requirements": {"type": "object"},
                    "output_dir": {"type": "string"}
                },
                "required": ["requirements", "output_dir"]
            }
        ),
        Tool(
            name="debug_error",
            description="Analyze error and propose fix with learning",
            inputSchema={
                "type": "object",
                "properties": {
                    "code": {"type": "string"},
                    "error": {"type": "string"},
                    "context": {"type": "object", "default": {}}
                },
                "required": ["code", "error"]
            }
        ),
        # Learning tools (conditional)
        *([
            Tool(
                name="search_learned_solutions",
                description="Search for previously learned solutions to similar problems",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "query": {"type": "string"},
                        "category": {"type": "string", "default": "error_fixes"},
                        "limit": {"type": "integer", "default": 5}
                    },
                    "required": ["query"]
                }
            ),
            Tool(
                name="get_learning_stats",
                description="Get statistics about what the system has learned",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "category": {"type": "string", "default": "error_fixes"}
                    }
                }
            ),
        ] if LEARNING_AVAILABLE else [])
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict):
    """Handle tool invocations."""
    try:
        if name == "create_prd":
            result = await prd_tool.create(
                arguments["idea"],
                arguments.get("output_path", "docs/generated_prd.md")
            )
            return [TextContent(type="text", text=result)]
        
        elif name == "parse_prd":
            result = await parser.parse(arguments["document_path"])
            return [TextContent(type="text", text=result)]
        
        elif name == "retrieve_context":
            k = arguments.get("k", 5)
            results = await rag_tool.retrieve(arguments["query"], k)
            return [TextContent(type="text", text=results)]
        
        elif name == "generate_project":
            files = await generator.generate(
                arguments["requirements"],
                arguments["output_dir"]
            )
            return [TextContent(type="text", text=files)]
        
        elif name == "debug_error":
            fix = await debugger.fix(
                arguments["code"],
                arguments["error"],
                arguments.get("context", {})
            )
            return [TextContent(type="text", text=fix)]
        
        elif name == "search_learned_solutions" and LEARNING_AVAILABLE:
            results = await learning_memory.search_solutions(
                category=arguments.get("category", "error_fixes"),
                query=arguments["query"],
                limit=arguments.get("limit", 5)
            )
            return [TextContent(type="text", text=json.dumps(results, indent=2))]
        
        elif name == "get_learning_stats" and LEARNING_AVAILABLE:
            top_solutions = await learning_memory.get_top_solutions(
                category=arguments.get("category", "error_fixes"),
                limit=10
            )
            stats = {
                "total_solutions": len(top_solutions),
                "top_solutions": top_solutions[:5],
                "average_success_rate": (
                    sum(s["success_rate"] for s in top_solutions) / len(top_solutions)
                    if top_solutions else 0.0
                )
            }
            return [TextContent(type="text", text=json.dumps(stats, indent=2))]
        
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    except Exception as e:
        error_msg = f"Tool {name} failed: {str(e)}"
        return [TextContent(type="text", text=error_msg)]


async def main():
    """Run the MCP server."""
    from mcp.server.stdio import stdio_server
    
    # Initialize RAG store
    await rag_tool.rag_store.initialize()
    
    # Start server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())

