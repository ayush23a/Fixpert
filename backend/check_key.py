import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print(" Error: GEMINI_API_KEY is not found in environment or .env file.")
    exit(1)

print(f" Found API Key: {api_key[:5]}...{api_key[-5:]}")

genai.configure(api_key=api_key)

print("\nAttempting to list available models...")
try:
    models = list(genai.list_models())
    print(f" Success! Found {len(models)} models.")
    print("Available Gemini Models:")
    for m in models:
        if 'gemini' in m.name:
            print(f" - {m.name}")
except Exception as e:
    print(f"\n API Call Failed: {e}")
