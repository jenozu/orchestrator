"""Test OpenAI API connection."""
import os
from openai import OpenAI

def test_openai_connection():
    """Test basic OpenAI API connectivity."""
    print("="*60)
    print("OpenAI API Connection Test")
    print("="*60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[ERROR] OPENAI_API_KEY not set")
        return False
    
    print(f"[OK] API Key found: {api_key[:10]}...")
    
    try:
        client = OpenAI()
        
        print("\nTesting API call...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": "Say 'test successful'"}
            ],
            max_tokens=10
        )
        
        result = response.choices[0].message.content
        print(f"[OK] API call successful!")
        print(f"Response: {result}")
        return True
        
    except Exception as e:
        error_type = type(e).__name__
        error_msg = str(e)
        print(f"\n[ERROR] Connection failed!")
        print(f"Error Type: {error_type}")
        print(f"Error Message: {error_msg}")
        
        # Provide troubleshooting tips
        print("\nTroubleshooting:")
        if "connection" in error_msg.lower():
            print("  - Check your internet connection")
            print("  - Check if OpenAI API is accessible")
            print("  - Try: curl https://api.openai.com/v1/models")
        elif "api_key" in error_msg.lower() or "authentication" in error_msg.lower():
            print("  - Verify API key is correct")
            print("  - Check if API key has proper permissions")
            print("  - Ensure key starts with 'sk-'")
        elif "rate" in error_msg.lower() or "limit" in error_msg.lower():
            print("  - You may have hit rate limits")
            print("  - Wait a moment and try again")
        else:
            print("  - Check OpenAI status page")
            print("  - Verify API key format")
        
        return False

if __name__ == "__main__":
    success = test_openai_connection()
    print("\n" + "="*60)
    if success:
        print("Connection test: PASSED")
    else:
        print("Connection test: FAILED")
    print("="*60)

