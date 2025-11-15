# PowerShell script to stop MCP Codegen server managed by pm2
# Usage: .\scripts\stop_mcp_server.ps1

Write-Host "Stopping MCP Codegen Server..." -ForegroundColor Yellow

# Check if pm2 is installed
$pm2Installed = Get-Command pm2 -ErrorAction SilentlyContinue
if (-not $pm2Installed) {
    Write-Error "pm2 is not installed. Cannot stop the server."
    exit 1
}

# Stop the server
pm2 stop mcp-codegen-server

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ MCP server stopped successfully!" -ForegroundColor Green
    
    # Display status
    pm2 status
    
    Write-Host "`nTo completely remove the server from pm2:" -ForegroundColor Yellow
    Write-Host "  pm2 delete mcp-codegen-server" -ForegroundColor Cyan
} else {
    Write-Error "Failed to stop MCP server. It may not be running."
    Write-Host "Run 'pm2 status' to check the server status." -ForegroundColor Yellow
}

