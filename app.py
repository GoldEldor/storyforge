import os
from flask import Flask, render_template_string, request
from google import genai

app = Flask(__name__)

# Initialize the official Google GenAI client securely via environment variables
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>StoryForge AI - Gemini</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; padding: 20px; background: #0f172a; color: #f8fafc; }
        textarea { width: 100%; height: 120px; padding: 12px; background: #1e293b; color: white; border: 1px solid #334155; border-radius: 6px; font-size: 16px; margin-top: 10px; box-sizing: border-box; }
        input[type="file"] { background: #1e293b; color: white; padding: 10px; border: 1px solid #334155; border-radius: 6px; width: 100%; margin-top: 10px; box-sizing: border-box; }
        button { background: #10b981; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 6px; cursor: pointer; margin-top: 15px; font-weight: bold; }
        button:hover { background: #059669; }
        .response { background: #1e293b; padding: 15px; border-radius: 6px; margin-top: 20px; border: 1px solid #334155; white-space: pre-wrap; word-break: break-word; }
        label { font-weight: bold; color: #94a3b8; }
    </style>
</head>
<body>
    <h1>StoryForge AI (Google Gemini)</h1>
    <form method="POST" enctype="multipart/form-data">
        <label>Upload a file (optional):</label><br>
        <input type="file" name="file"><br><br>
        
        <label>What do you want Gemini to do?</label><br>
        <textarea name="prompt" placeholder="Ask Gemini to write code, analyze a file, or create a story..."></textarea><br>
        
        <button type="submit">Process with Gemini</button>
    </form>
    
    {% if response %}
        <div class="response"><strong>AI Response:</strong><br>{{ response }}</div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    response_text = ""
    if request.method == "POST":
        user_prompt = request.form.get("prompt", "")
        file_content = ""

        # Handle uploaded file reading safely
        uploaded_file = request.files.get("file")
        if uploaded_file and uploaded_file.filename != "":
            try:
                file_content = uploaded_file.read().decode("utf-8")
            except Exception as e:
                file_content = f"[Error reading file: {str(e)}]"

        # Combine file contents and prompt if a file was attached
        full_message = user_prompt
        if file_content:
            full_message = f"Uploaded File Content:\n\n{file_content}\n\nUser Instruction: {user_prompt}"

        if full_message.strip():
            try:
                # Call Gemini Flash model
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=full_message,
                )
                response_text = response.text
            except Exception as e:
                response_text = f"Error generating response: {str(e)}"
                
    return render_template_string(HTML_TEMPLATE, response=response_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    
