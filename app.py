import os
from flask import Flask, render_template, request, jsonify
from google import genai
from google.genai import types

app = Flask(__name__)

# SECURE: Get key from Environment Variable
API_KEY = os.environ.get("GOOGLE_API_KEY")

if not API_KEY:
    print("CRITICAL ERROR: GOOGLE_API_KEY not found in environment.")

client = None
if API_KEY:
    client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
You are a retro game developer. Write a SINGLE FILE HTML5 game.
RULES:
1. Canvas size: 160x144.
2. Palette: #0f380f, #306230, #8bac0f, #9bbc0f.
3. Controls: Arrow keys + Z/X.
4. Scale: CSS transform scale(3).
5. Output: ONLY the raw HTML code. No markdown.
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    if not client:
        return jsonify({"success": False, "error": "Server API Key is missing."})

    user_prompt = request.json.get('prompt')
    try:
        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
            contents=user_prompt
        )
        return jsonify({"success": True, "code": response.text})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
