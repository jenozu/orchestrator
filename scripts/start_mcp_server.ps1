# PowerShell script to start MCP Codegen server with pm2
# Usage: .\scripts\start_mcp_server.ps1

Write-Host "Starting MCP Codegen Server with pm2..." -ForegroundColor Green

# Get the root directory of the project
$ProjectRoot = Split-Path -Parent $PSScriptRoot

# Change to project root
Push-Location $ProjectRoot

try {
    # Check if pm2 is installed
    $pm2Installed = Get-Command pm2 -ErrorAction SilentlyContinue
    if (-not $pm2Installed) {
        Write-Host "pm2 is not installed. Installing pm2 globally..." -ForegroundColor Yellow
        npm install -g pm2
        if ($LASTEXITCODE -ne 0) {
            Write-Error "Failed to install pm2. Please install Node.js first."
            exit 1
        }
    }

    # Start the server with pm2
    Write-Host "Starting MCP server..." -ForegroundColor Cyan
    $serverScript = Join-Path $ProjectRoot "scripts\run_mcp_server.py"
    pm2 start python --name "mcp-codegen-server" -- "$serverScript"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ MCP server started successfully!" -ForegroundColor Green
        
        # Save the pm2 process list
        pm2 save
        Write-Host "✓ Process list saved" -ForegroundColor Green
        
        # Display status
        pm2 status
        
        Write-Host "`nTo configure auto-start on system boot, run:" -ForegroundColor Yellow
        Write-Host "  pm2 startup" -ForegroundColor Cyan
        Write-Host "  Then follow the instructions provided by pm2" -ForegroundColor Yellow
        
        Write-Host "`nUseful pm2 commands:" -ForegroundColor Yellow
        Write-Host "  pm2 status              - View server status" -ForegroundColor White
        Write-Host "  pm2 logs mcp-codegen-server    - View server logs" -ForegroundColor White
        Write-Host "  pm2 restart mcp-codegen-server - Restart the server" -ForegroundColor White
        Write-Host "  pm2 stop mcp-codegen-server    - Stop the server" -ForegroundColor White
        Write-Host "  pm2 delete mcp-codegen-server  - Remove from pm2" -ForegroundColor White
    } else {
        Write-Error "Failed to start MCP server"
        exit 1
    }
} finally {
    Pop-Location
}

