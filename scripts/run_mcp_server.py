"""Entry point to launch the MCP Codegen server.

This script exists so process managers like pm2 can reference a concrete
Python file instead of using the `-m` module flag, which some platforms
may interpret as a file path.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from mcp_codegen.server import main


if __name__ == "__main__":
    asyncio.run(main())

