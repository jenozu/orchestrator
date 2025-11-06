# How to Run Tests - Quick Guide

## The Issue You're Experiencing

You're seeing "Connection error" because the API key needs to be set in the **same PowerShell session** where you run the test.

PowerShell environment variables set with `$env:OPENAI_API_KEY` only last for that session.

## ✅ Solution: Set API Key in Same Session

### Method 1: Set and Run in Same Command

```powershell
# Set API key AND run test in one command
$env:OPENAI_API_KEY="your-key-here"; python quick_test.py
```

### Method 2: Set, Then Immediately Run (Same Session)

```powershell
# Step 1: Set the key
$env:OPENAI_API_KEY="your-key-here"

# Step 2: Run test (in same session, don't close terminal)
python quick_test.py
```

### Method 3: Use the Test Script with Environment Check

```powershell
# Set API key first
$env:OPENAI_API_KEY="your-key-here"

# Run enhanced test
python test_with_env.py
```

## 🔍 Verify API Key is Set

Before running tests, verify the key is set:

```powershell
# Check if key is set
python -c "import os; print('API Key:', 'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET')"
```

## 🎯 Complete Testing Workflow

### Step 1: Open PowerShell in Orchestrator Folder

```powershell
cd C:\Users\andel\Desktop\orchestrator
```

### Step 2: Set API Key

```powershell
$env:OPENAI_API_KEY="your-actual-api-key-here"
```

### Step 3: Verify Connection

```powershell
python test_connection_diagnostic.py
```

Should show: `[OK] API call successful!`

### Step 4: Run Quick Test

```powershell
python quick_test.py
```

### Step 5: (Optional) Populate Knowledge Base

```powershell
python scripts/ingest_knowledge_base.py --local-only
```

### Step 6: Test Again with KB

```powershell
python quick_test.py
```

Now should show: `knowledge_retrieved: True`

## 📋 Quick Reference Commands

```powershell
# All in one session:

# 1. Navigate
cd C:\Users\andel\Desktop\orchestrator

# 2. Set API key
$env:OPENAI_API_KEY="your-key-here"

# 3. Test connection
python test_connection_diagnostic.py

# 4. Run orchestrator test
python quick_test.py

# 5. Populate KB (optional)
python scripts/ingest_knowledge_base.py --local-only

# 6. Test again
python quick_test.py
```

## ⚠️ Common Mistakes

1. **Closing terminal between setting key and running test**
   - Set key and run test in same session

2. **Setting key in different terminal**
   - Each PowerShell window is a separate session

3. **Forgetting to set key after restart**
   - Environment variables don't persist unless set permanently

## 🎉 Success Indicators

When everything works, you should see:

```
[OK] OPENAI_API_KEY: Set
[OK] RAG Store: Initialized
[OK] Orchestrator: Created and graph built
[OK] IntentParser: Executed successfully!
   Project: Build a simple todo app...
   Features: 3 features
[OK] Backend Agent: Executed
   Knowledge Retrieved: True
   Context Length: 1234 chars
```

## 💡 Pro Tip: Make It Permanent

To avoid setting the key every time:

```powershell
# Set permanently (requires restart)
[System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your-key-here", "User")
```

Then restart PowerShell and it will be available automatically.

