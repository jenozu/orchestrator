# Environment Setup Guide

## Using .env File for API Keys

You can store your OpenAI API key in a `.env` file so you don't have to set it each time.

### Step 1: Install python-dotenv

```powershell
pip install python-dotenv
```

Or add it to requirements:
```powershell
pip install -r requirements.txt
```

### Step 2: Create .env File

Create a file named `.env` in the project root directory (`C:\Users\andel\Desktop\orchestrator\.env`):

```powershell
# Create .env file
New-Item -Path .env -ItemType File
```

Then add your API key to the file:
```
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Important:** The `.env` file is already in `.gitignore`, so it won't be committed to git.

### Step 3: Verify It Works

The code automatically loads `.env` files when you import modules. Test it:

```powershell
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('API Key:', 'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET')"
```

### Example .env File

Create `.env` with this content:

```env
# OpenAI API Configuration
OPENAI_API_KEY=sk-your-actual-api-key-here

# Optional: Other API keys
# LANGSMITH_API_KEY=your-langsmith-key
# LANGSMITH_TRACING=true
```

### Security Notes

- ✅ `.env` is already in `.gitignore` - won't be committed
- ✅ Never share your `.env` file
- ✅ Keep your API key secret
- ✅ Use different keys for development vs production

### Alternative: System Environment Variable

If you prefer to set it system-wide (Windows):

```powershell
# Set permanently (User-level)
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your-key-here", "User")

# Restart PowerShell after setting
```

## Quick Setup Commands

```powershell
# 1. Install python-dotenv
pip install python-dotenv

# 2. Create .env file (replace with your actual key)
@"
OPENAI_API_KEY=sk-your-actual-key-here
"@ | Out-File -FilePath .env -Encoding utf8

# 3. Verify it works
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key:', 'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET')"
```

