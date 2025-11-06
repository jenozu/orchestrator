# Environment Setup - Quick Guide

## ✅ .env File Support Now Enabled!

The project now automatically loads environment variables from a `.env` file. You don't need to set `OPENAI_API_KEY` each time you open a new terminal!

## 🚀 Quick Setup

### Option 1: Use the Setup Script (Easiest)

```powershell
python setup_env.py
```

This will:
1. Prompt you for your OpenAI API key
2. Create a `.env` file automatically
3. Store your key securely (file is in .gitignore)

### Option 2: Create .env Manually

1. **Create the file:**
   ```powershell
   New-Item -Path .env -ItemType File
   ```

2. **Add your API key:**
   ```powershell
   @"
   OPENAI_API_KEY=sk-your-actual-api-key-here
   "@ | Out-File -FilePath .env -Encoding utf8
   ```

3. **Or edit manually:**
   Open `.env` in your editor and add:
   ```
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

## ✅ Verify It Works

```powershell
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('✅ API Key:', 'SET' if os.getenv('OPENAI_API_KEY') else 'NOT SET')"
```

## 📝 What Changed

- ✅ Added `python-dotenv` to `requirements.txt`
- ✅ Updated `agents/rag_retrieval.py` to auto-load `.env`
- ✅ Updated `quick_test.py` to auto-load `.env`
- ✅ Created `setup_env.py` helper script
- ✅ `.env` is already in `.gitignore` (won't be committed)

## 🔒 Security

- ✅ `.env` file is in `.gitignore` - **never committed to git**
- ✅ Keep your API key secret
- ✅ Don't share your `.env` file

## 🎯 Usage

Once you create `.env`, you can just run:

```powershell
python quick_test.py
python scripts/ingest_knowledge_base.py --local-only
```

No need to set `$env:OPENAI_API_KEY` each time! 🎉

