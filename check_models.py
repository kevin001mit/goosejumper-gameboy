import os
from google import genai

# PASTE YOUR KEY DIRECTLY HERE TO TEST
API_KEY = "AIzaSyCkBfqEcLKoARYX3rmNZbuAoA8Ilnsq-Cw"

try:
    client = genai.Client(api_key=API_KEY)
    print("--- AVAILABLE MODELS ---")
    # List models that support content generation
    for m in client.models.list():
        if "generateContent" in m.supported_actions:
            print(m.name)
except Exception as e:
    print(f"Error: {e}")
