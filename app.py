import os
from flask import Flask, render_template_string, request
from openai import OpenAI

app = Flask(__name__)

# Initialize the OpenAI client using your OPENAI_API_KEY environment variable
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# HTML template with file upload support and GPT-4o branding
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>StoryForge AI</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; padding: 20px; background: #0f172a; color: #f8fafc; }
        textarea { width: 100%; height: 120px; padding: 12px; background: #1e293b; color: white; border: 1px solid #334155; border-radius: 6px; font-size: 16px; margin-top: 10px; box-sizing: border-box; }
        input[type="file"] { background: #1e293b; color: white; padding: 10px; border: 1px solid #334155; border-radius: 6px; width: 100%; margin-top: 10px; box-sizing: border-box; }
        button { background: #6366f1; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 6px; cursor: pointer; margin-top: 15px; }
        button:hover { background: #4f46e5; }
        .response { background: #1e293b; padding: 15px; border-radius: 6px; margin-top: 20px; border: 1px solid #334155; white-space: pre-wrap; word-break: break-word; }
        label { font-weight: bold; color: #94a3b8; }
    </style>
</head>
<body>
    <h1>StoryForge AI (OpenAI GPT-4o)</h1>
    <form method="POST" enctype="multipart/form-data">
        <label>Upload a file (optional):</label><br>
        <input type="file" name="file"><br><br>
        
        <label>What do you want the AI to do?</label><br>
        <textarea name="prompt" placeholder="Ask GPT-4o to write code, analyze a file, or create a story..."></textarea><br>
        
        <button type="submit">Process with GPT-4o</button>
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

        # Check if a file was uploaded by the user
        uploaded_file = request.files.get("file")
        if uploaded_file and uploaded_file.filename != "":
            try:
                file_content = uploaded_file.read().decode("utf-8")
            except Exception as e:
                file_content = f"[Error reading file: {str(e)}]"

        # Bundle the file text and user prompt together for GPT-4o
        full_message = user_prompt
        if file_content:
            full_message = f"Here is the content of the file uploaded by the user:\n\n{file_content}\n\nUser Instruction: {user_prompt}"

        if full_message.strip():
            try:
                # Call OpenAI's flagship gpt-4o model with an expanded token limit
                completion = client.chat.completions.create(
                    model="gpt-4o",
                    messages=[{"role": "user", "content": full_message}],
                    max_tokens=2000,
                )
                response_text = completion.choices[0].message.content
            except Exception as e:
                response_text = f"Error generating response: {str(e)}"
                
    return render_template_string(HTML_TEMPLATE, response=response_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    
