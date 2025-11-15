"""Diagnostic test for OpenAI connection issues."""
from dotenv import load_dotenv
load_dotenv()

import os
import sys

def diagnose_connection():
    """Diagnose OpenAI connection issues."""
    print("="*60)
    print("OpenAI Connection Diagnostic")
    print("="*60)
    
    # Check API key
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[ERROR] OPENAI_API_KEY not found in environment")
        print("\nSolutions:")
        print("1. Set in current PowerShell session:")
        print('   $env:OPENAI_API_KEY="your-key-here"')
        print("\n2. Set permanently (PowerShell):")
        print('   [System.Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your-key-here", "User")')
        print("   (Then restart PowerShell)")
        print("\n3. Create .env file (recommended for development):")
        print("   Create .env file with: OPENAI_API_KEY=your-key-here")
        print("   Then use python-dotenv to load it")
        return False
    
    print(f"[OK] API Key found: {api_key[:10]}...{api_key[-4:]}")
    
    # Test connection
    try:
        from openai import OpenAI
        client = OpenAI()
        
        print("\nTesting API call...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        
        print("[OK] API call successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        
        print(f"\n[ERROR] Connection failed!")
        print(f"Error Type: {error_type}")
        print(f"Error Message: {error_msg}")
        
        # Specific troubleshooting
        if "Connection" in error_type:
            print("\nConnection Error Troubleshooting:")
            print("  1. Check internet connection")
            print("  2. Check firewall/proxy settings")
            print("  3. Try: ping api.openai.com")
            print("  4. Check OpenAI status: https://status.openai.com/")
        elif "APIConnectionError" in error_type:
            print("\nAPI Connection Error:")
            print("  - Network connectivity issue")
            print("  - OpenAI API may be down")
            print("  - Check proxy/VPN settings")
        elif "AuthenticationError" in error_type or "api_key" in error_msg.lower():
            print("\nAuthentication Error:")
            print("  - Verify API key is correct")
            print("  - Check key starts with 'sk-'")
            print("  - Ensure key has proper permissions")
        elif "RateLimitError" in error_type:
            print("\nRate Limit Error:")
            print("  - You've hit API rate limits")
            print("  - Wait a few minutes and try again")
        
        return False

if __name__ == "__main__":
    success = diagnose_connection()
    print("\n" + "="*60)
    if success:
        print("Diagnostic: PASSED - API is working")
    else:
        print("Diagnostic: FAILED - See troubleshooting above")
    print("="*60)

