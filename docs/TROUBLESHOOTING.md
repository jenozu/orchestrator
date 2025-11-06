# Troubleshooting Guide

## Common Issues and Solutions

### Issue: "Connection error" when running tests

**Symptoms:**
- `IntentParser Error: Connection error`
- `Failed to retrieve knowledge: Connection error`

**Solutions:**

#### 1. Check API Key is Set in Current Session

PowerShell environment variables only last for the current session. Make sure you set it in the SAME terminal where you run the test:

```powershell
# Set in current session
$env:OPENAI_API_KEY="your-key-here"

# Then immediately run test
python quick_test.py
```

#### 2. Verify API Key Format

- Should start with `sk-`
- Should be your full API key from OpenAI dashboard
- No extra spaces or quotes

#### 3. Test Connection Directly

```powershell
python test_connection_diagnostic.py
```

This will test the API connection and provide specific troubleshooting.

#### 4. Check Network Connection

```powershell
# Test internet connectivity
ping api.openai.com

# Check OpenAI status
# Visit: https://status.openai.com/
```

#### 5. Firewall/Proxy Issues

- Check if firewall is blocking OpenAI API
- If behind corporate proxy, may need proxy configuration
- Check VPN settings

#### 6. Rate Limiting

- If you hit rate limits, wait a few minutes
- Check your OpenAI usage dashboard
- May need to upgrade plan

### Issue: "OPENAI_API_KEY not set"

**Solution:**

Set the environment variable:

```powershell
# Temporary (current session only)
$env:OPENAI_API_KEY="your-key-here"

# Permanent (requires restart)
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your-key-here", "User")
```

### Issue: "RAG store not initialized"

**Cause:** API key not set or ChromaDB initialization failed

**Solution:**
1. Set OPENAI_API_KEY
2. Verify ChromaDB is installed: `pip install chromadb`
3. Check ChromaDB directory permissions

### Issue: "No documents retrieved"

**Cause:** Knowledge base not populated

**Solution:**
```powershell
# After setting API key
python scripts/ingest_knowledge_base.py --local-only
```

### Issue: "Parsed intent is None"

**Cause:** IntentParser failed to call OpenAI API

**Solutions:**
1. Check API key is set
2. Test connection: `python test_connection_diagnostic.py`
3. Check internet connection
4. Verify API key has proper permissions

## Diagnostic Commands

### Test 1: Check API Key
```powershell
python -c "import os; print('API Key:', 'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET')"
```

### Test 2: Test API Connection
```powershell
python test_connection_diagnostic.py
```

### Test 3: Test Quick Test
```powershell
python quick_test.py
```

### Test 4: Verify Dependencies
```powershell
python -c "import openai, chromadb, langchain; print('All dependencies OK')"
```

## Environment Variable Setup

### Option 1: Session-Specific (Temporary)

**PowerShell:**
```powershell
$env:OPENAI_API_KEY="your-key-here"
```

**Bash/Linux:**
```bash
export OPENAI_API_KEY="your-key-here"
```

**Windows CMD:**
```cmd
set OPENAI_API_KEY=your-key-here
```

### Option 2: Permanent (User Environment)

**PowerShell (Admin):**
```powershell
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your-key-here", "User")
```

**Windows GUI:**
1. Search "Environment Variables" in Windows
2. Edit User variables
3. Add `OPENAI_API_KEY` with your key
4. Restart terminal

**Linux/Mac:**
Add to `~/.bashrc` or `~/.zshrc`:
```bash
export OPENAI_API_KEY="your-key-here"
```

### Option 3: .env File (Recommended for Development)

Create `.env` file in project root:
```
OPENAI_API_KEY=your-key-here
```

Then install python-dotenv:
```bash
pip install python-dotenv
```

And load in code:
```python
from dotenv import load_dotenv
load_dotenv()
```

## Getting Help

If issues persist:

1. **Run diagnostics**: `python test_connection_diagnostic.py`
2. **Check logs**: Look for detailed error messages
3. **Verify setup**: See `docs/READY_FOR_TESTING.md`
4. **Test components**: Run individual component tests

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `Connection error` | Network/API issue | Check internet, test connection |
| `api_key not set` | Missing API key | Set OPENAI_API_KEY |
| `RAG store not initialized` | API key or ChromaDB issue | Set API key, check ChromaDB |
| `No documents retrieved` | KB not populated | Run ingestion script |
| `Parsed intent is None` | IntentParser failed | Check API key and connection |

