#!/bin/bash
# Bash script to stop MCP Codegen server managed by pm2
# Usage: ./scripts/stop_mcp_server.sh

echo "Stopping MCP Codegen Server..."

# Check if pm2 is installed
if ! command -v pm2 &> /dev/null; then
    echo "Error: pm2 is not installed. Cannot stop the server."
    exit 1
fi

# Stop the server
pm2 stop mcp-codegen-server

if [ $? -eq 0 ]; then
    echo "✓ MCP server stopped successfully!"
    
    # Display status
    pm2 status
    
    echo ""
    echo "To completely remove the server from pm2:"
    echo "  pm2 delete mcp-codegen-server"
else
    echo "Error: Failed to stop MCP server. It may not be running."
    echo "Run 'pm2 status' to check the server status."
    exit 1
fi

