# MCP Codegen Server - Deployment Guide

This guide covers deploying the MCP Codegen server for persistent, 24/7 operation using pm2.

## Table of Contents

- [Overview](#overview)
- [Prerequisites](#prerequisites)
- [Manual Start (Development)](#manual-start-development)
- [Persistent Deployment (Production)](#persistent-deployment-production)
- [Management Commands](#management-commands)
- [Troubleshooting](#troubleshooting)
- [Security Considerations](#security-considerations)

## Overview

The MCP Codegen server provides:
- **PRD Generation**: Create product requirements from ideas
- **Project Generation**: Scaffold complete projects
- **Code Debugging**: AI-powered error analysis
- **Learning System**: Persistent knowledge and pattern recognition

It can run in two modes:
1. **Manual mode**: Run directly via Python (good for development)
2. **Persistent mode**: Run as a background service with pm2 (good for production)

## Prerequisites

### Required
- **Python 3.11+**: `python --version` or `python3 --version`
- **Node.js 18+**: Required for pm2 (`node --version`)
- **npm**: Comes with Node.js (`npm --version`)

### Optional
- **Virtual environment**: Recommended for Python dependency isolation

### Installation

**Install Node.js** (if not already installed):

Windows:
```powershell
# Download from https://nodejs.org/
# Or use Chocolatey:
choco install nodejs
```

Linux (Ubuntu/Debian):
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs
```

Mac:
```bash
brew install node
```

**Install pm2**:
```bash
npm install -g pm2
```

## Manual Start (Development)

Use this method when actively developing or debugging.

### Windows (PowerShell)
```powershell
# Navigate to project root
cd c:\Users\andel\Desktop\orchestrator

# Optional: Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start the server
python -m mcp_codegen.server --stdio
```

### Linux/Mac (Bash)
```bash
# Navigate to project root
cd ~/orchestrator

# Optional: Activate virtual environment
source venv/bin/activate

# Start the server
python3 -m mcp_codegen.server --stdio
```

**Important Notes:**
- Keep the terminal window open
- Don't type anything in the terminal (server uses stdin/stdout)
- Press `Ctrl+C` once to stop
- Server stops when terminal is closed

## Persistent Deployment (Production)

Use this method for 24/7 operation with automatic restart.

### Step 1: Start with pm2

**Windows (PowerShell):**
```powershell
# From project root
.\scripts\start_mcp_server.ps1
```

**Linux/Mac (Bash):**
```bash
# Make script executable (first time only)
chmod +x ./scripts/start_mcp_server.sh

# Start the server
./scripts/start_mcp_server.sh
```

### Step 2: Configure Auto-Start on Boot

After starting with pm2, configure it to restart on system reboot:

```bash
# Generate startup script
pm2 startup

# This will output a command to run (varies by OS)
# Example output (Linux):
# sudo env PATH=$PATH:/usr/bin pm2 startup systemd -u username --hp /home/username

# Copy and run the command it provides
# Then save the process list
pm2 save
```

### Step 3: Verify

```bash
# Check server status
pm2 status

# View logs
pm2 logs mcp-codegen-server

# Test restart
pm2 restart mcp-codegen-server
```

## Management Commands

### View Status
```bash
pm2 status
# Shows: name, status, CPU, memory, uptime
```

### View Logs
```bash
# Real-time logs
pm2 logs mcp-codegen-server

# Last 100 lines
pm2 logs mcp-codegen-server --lines 100

# Error logs only
pm2 logs mcp-codegen-server --err
```

### Restart Server
```bash
# Graceful restart
pm2 restart mcp-codegen-server

# Force restart (if stuck)
pm2 reload mcp-codegen-server
```

### Stop Server
```bash
# Stop (can be restarted)
pm2 stop mcp-codegen-server

# Or use the convenience script
.\scripts\stop_mcp_server.ps1  # Windows
./scripts/stop_mcp_server.sh   # Linux/Mac
```

### Remove from pm2
```bash
# Delete from pm2 (removes completely)
pm2 delete mcp-codegen-server

# Save the updated process list
pm2 save
```

### Monitor Resources
```bash
# Real-time monitoring dashboard
pm2 monit

# Detailed process info
pm2 info mcp-codegen-server
```

## Troubleshooting

### Server Won't Start

**Error: "No module named 'mcp_codegen'"**
- Ensure you're in the correct directory: `cd c:\Users\andel\Desktop\orchestrator`
- Or install the package: `pip install -e .`

**Error: "pm2: command not found"**
- Install pm2: `npm install -g pm2`
- Verify: `pm2 --version`

**Error: "python: command not found"**
- Install Python 3.11+
- Ensure Python is in PATH
- Try `python3` instead of `python`

### Server Crashes/Restarts Frequently

```bash
# View error logs
pm2 logs mcp-codegen-server --err --lines 50

# Common causes:
# 1. Missing dependencies: pip install -r requirements.txt
# 2. Port conflict: Check if another instance is running
# 3. Memory issues: pm2 info mcp-codegen-server
```

### Auto-Start Not Working After Reboot

```bash
# Check startup configuration
pm2 startup

# Verify saved process list
cat ~/.pm2/dump.pm2  # Linux/Mac
type %USERPROFILE%\.pm2\dump.pm2  # Windows

# Re-save if needed
pm2 save

# Check system service status (Linux)
systemctl status pm2-username
```

### High Memory/CPU Usage

```bash
# Monitor resource usage
pm2 monit

# Check detailed metrics
pm2 info mcp-codegen-server

# Restart if needed
pm2 restart mcp-codegen-server
```

### Logs Growing Too Large

```bash
# Install pm2-logrotate module
pm2 install pm2-logrotate

# Configure rotation (10MB max, keep 7 files)
pm2 set pm2-logrotate:max_size 10M
pm2 set pm2-logrotate:retain 7
pm2 set pm2-logrotate:compress true
```

## Security Considerations

### API Keys and Secrets
- Never commit API keys to Git
- Use environment variables: `export OPENAI_API_KEY=sk-...`
- pm2 inherits environment from the shell that starts it

### Network Access
- Server listens on stdin/stdout by default (local only)
- No network ports exposed unless explicitly configured
- Safe for local development

### File Permissions
```bash
# Ensure scripts are executable (Linux/Mac)
chmod +x scripts/*.sh

# Restrict access to sensitive files
chmod 600 ~/.pm2/dump.pm2
```

### Updates and Maintenance
```bash
# Update pm2
npm update -g pm2

# Update Python dependencies
pip install --upgrade -r requirements.txt

# Restart after updates
pm2 restart mcp-codegen-server
```

## Advanced Configuration

### Custom Environment Variables

Create a `.env` file in project root:
```bash
OPENAI_API_KEY=sk-...
LOG_LEVEL=INFO
MAX_RETRIES=3
```

Update the start script to load it:
```bash
pm2 start python --name "mcp-codegen-server" \
  --interpreter none \
  --env-file .env \
  -- -m mcp_codegen.server --stdio
```

### Multiple Instances

Run multiple servers on different ports:
```bash
pm2 start python --name "mcp-codegen-server-1" -- -m mcp_codegen.server --stdio
pm2 start python --name "mcp-codegen-server-2" -- -m mcp_codegen.server --stdio
```

### Monitoring and Alerts

Install pm2 monitoring:
```bash
# Link to pm2.io for web dashboard
pm2 link [secret] [public]

# Configure email alerts
pm2 install pm2-auto-pull
```

## Best Practices

1. **Use pm2 for production**, manual start for development
2. **Monitor logs regularly**: `pm2 logs mcp-codegen-server`
3. **Keep dependencies updated**: `pip install --upgrade -r requirements.txt`
4. **Save pm2 state after changes**: `pm2 save`
5. **Test restarts periodically**: `pm2 restart mcp-codegen-server`
6. **Enable log rotation** to prevent disk fill
7. **Use environment variables** for secrets
8. **Document custom configurations** in your README

## References

- [pm2 Documentation](https://pm2.keymetrics.io/docs/)
- [pm2 Startup Guide](https://pm2.keymetrics.io/docs/usage/startup/)
- [pm2 Log Rotation](https://github.com/keymetrics/pm2-logrotate)
- [Node.js Installation](https://nodejs.org/)

---

**Questions or Issues?** Check the main README or open an issue in the repository.

