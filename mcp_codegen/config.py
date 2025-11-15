"""Configuration for MCP CodeGen server."""
from dotenv import load_dotenv
load_dotenv()

import os
from pathlib import Path

# OpenAI API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")

# ChromaDB settings
CHROMA_DIR = Path("./chroma_db")
CHROMA_COLLECTION = "code_patterns"

# Model settings
EMBEDDING_MODEL = "text-embedding-3-small"
CODE_MODEL = "gpt-4-turbo"

# Code execution
EXECUTION_TIMEOUT = 30  # seconds
SANDBOX_ENABLED = False  # Enable Docker sandboxing

# RAG settings
RETRIEVAL_K = 5  # Number of similar results to retrieve
SIMILARITY_THRESHOLD = 0.7

# Debugging
MAX_RETRIES = 3  # Max fix attempts per error
DEBUG_MODE = os.getenv("DEBUG", "false").lower() == "true"

