"""Helper script to create .env file for API keys."""
import os
from pathlib import Path

def create_env_file():
    """Create .env file with OpenAI API key."""
    env_path = Path(".env")
    
    if env_path.exists():
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/n): ")
        if response.lower() != 'y':
            print("Cancelled.")
            return
    
    print("="*60)
    print("CREATE .ENV FILE FOR API KEYS")
    print("="*60)
    print("\nThis will create a .env file to store your OpenAI API key.")
    print("The .env file is already in .gitignore, so it won't be committed.\n")
    
    # Get API key from user
    api_key = input("Enter your OpenAI API key (or press Enter to skip): ").strip()
    
    if not api_key:
        print("\n⚠️  No API key provided. Creating template .env file.")
        api_key = "sk-your-openai-api-key-here"
    
    # Create .env content
    env_content = f"""# OpenAI API Configuration
# This file is in .gitignore and won't be committed
OPENAI_API_KEY={api_key}

# Optional: Other environment variables
# LANGSMITH_API_KEY=your-langsmith-key-here
# LANGSMITH_TRACING=true
"""
    
    # Write .env file
    try:
        env_path.write_text(env_content, encoding='utf-8')
        print(f"\n✅ Created .env file at: {env_path.absolute()}")
        
        if api_key.startswith("sk-"):
            print("✅ API key looks valid!")
        
        print("\n📝 Next steps:")
        print("   1. Verify the .env file was created correctly")
        print("   2. Run: python quick_test.py")
        print("   3. The API key will be loaded automatically from .env")
        
    except Exception as e:
        print(f"\n❌ Error creating .env file: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    create_env_file()

