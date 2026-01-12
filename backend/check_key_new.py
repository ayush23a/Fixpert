from google import genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
print(f"DEBUG: Key length: {len(api_key) if api_key else 0}")
print(f"DEBUG: Key starts with: {api_key[:5] if api_key else 'None'}")

if not api_key:
    print("❌ Error: No API Key found.")
    exit(1)

try:
    print("Initializing Client...")
    client = genai.Client(api_key=api_key)
    
    print("Attempting to generate content with gemini-2.5-flash...")
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents='Hello, are you working?'
    )
    print(f"✅ Success! Response: {response.text}")

except Exception as e:
    print(f"\n❌ FAILED: {e}")
    # Try listing models to see if that works
    try:
        print("\nAttempting to list models...")
        # Note: list_models might be paginated or different in new SDK
        # The new SDK structure is client.models.list() usually?
        # Let's check documentation or try standard
        pass 
    except:
        pass
