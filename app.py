import os
from flask import Flask, render_template_string, request
from huggingface_hub import InferenceClient

app = Flask(__name__)

# Initialize the Hugging Face client using your HF_TOKEN environment variable
client = InferenceClient(
    model="Qwen/Qwen2.5-Coder-7B-Instruct",
    token=os.environ.get("HF_TOKEN")
)

# Simple HTML template with a chat/prompt interface
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>StoryForge AI</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 700px; margin: 40px auto; padding: 20px; background: #0f172a; color: #f8fafc; }
        textarea { width: 100%; height: 120px; padding: 12px; background: #1e293b; color: white; border: 1px solid #334155; border-radius: 6px; font-size: 16px; }
        button { background: #6366f1; color: white; border: none; padding: 10px 20px; font-size: 16px; border-radius: 6px; cursor: pointer; margin-top: 10px; }
        button:hover { background: #4f46e5; }
        .response { background: #1e293b; padding: 15px; border-radius: 6px; margin-top: 20px; border: 1px solid #334155; white-space: pre-wrap; }
    </style>
</head>
<body>
    <h1>StoryForge AI (Qwen 2.5 Coder)</h1>
    <form method="POST">
        <textarea name="prompt" placeholder="Ask Qwen to write a story or code..."></textarea><br>
        <button type="submit">Generate</button>
    </form>
    {% if response %}
        <div class="response"><strong>Response:</strong><br>{{ response }}</div>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    response_text = ""
    if request.method == "POST":
        user_prompt = request.form.get("prompt")
        if user_prompt:
            try:
                # Call Qwen via Hugging Face Inference API (fixed method name)
                messages = [{"role": "user", "content": user_prompt}]
                completion = client.chat_completion(
                    model="Qwen/Qwen2.5-Coder-7B-Instruct",
                    messages=messages,
                    max_tokens=500,
                )
                response_text = completion.choices[0].message.content
            except Exception as e:
                response_text = f"Error generating response: {str(e)}"
                
    return render_template_string(HTML_TEMPLATE, response=response_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    
