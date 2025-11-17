"""
Test script to verify MCP codegen tools are accessible.
This simulates how Cursor would call the MCP tools.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from mcp_codegen.server import app
from mcp_codegen.tools.prd_tool import PRDTool
from mcp_codegen.tools.parser_tool import ParserTool
from mcp_codegen.tools.rag_tool import RAGTool


async def test_tools():
    """Test that all MCP tools are accessible."""
    print("Testing MCP Codegen Tools...")
    print("=" * 60)
    
    # Test 1: List available tools
    print("\n1. Available Tools:")
    tools = await app.list_tools()
    for tool in tools:
        print(f"   [OK] {tool.name}: {tool.description}")
    
    # Test 2: Test PRD creation
    print("\n2. Testing create_prd tool...")
    prd_tool = PRDTool()
    try:
        result = await prd_tool.create(
            "A simple todo app",
            "docs/test_prd.md"
        )
        print(f"   [OK] PRD created: {len(result)} characters")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    # Test 3: Test RAG retrieval
    print("\n3. Testing retrieve_context tool...")
    rag_tool = RAGTool()
    try:
        await rag_tool.rag_store.initialize()
        results = await rag_tool.retrieve("FastAPI authentication", k=3)
        print(f"   [OK] RAG retrieval working: {len(results)} characters")
    except Exception as e:
        print(f"   [ERROR] {e}")
    
    print("\n" + "=" * 60)
    print("[OK] MCP Tools Test Complete!")
    print("\nIn Cursor, you can now use these tools in AI chat:")
    print("   - 'Use create_prd to create a PRD for...'")
    print("   - 'Use retrieve_context to find...'")
    print("   - 'Use parse_prd to parse...'")
    print("   - etc.")


if __name__ == "__main__":
    asyncio.run(test_tools())

