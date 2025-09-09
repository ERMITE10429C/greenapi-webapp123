import os
import logging
from flask import Flask, render_template_string, request
from dotenv import load_dotenv
from whatsapp_handler import send_whatsapp_video
from youtube_handler import download_youtube_video

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Simple HTML template
HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>YouTube → WhatsApp</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 40px; background: #f7f9fc; }
        .container { max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        input, textarea { width: 100%; padding: 10px; margin: 8px 0; border-radius: 5px; border: 1px solid #ccc; }
        button { background: #25D366; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: pointer; }
        button:hover { background: #1ebe5d; }
    </style>
</head>
<body>
    <div class="container">
        <h2>📲 Send YouTube to WhatsApp</h2>
        <form method="POST">
            <label>📹 YouTube Link</label>
            <input type="text" name="youtube_url" placeholder="Paste YouTube URL" required>

            <label>📱 Phone Number (int'l, no '+')</label>
            <input type="text" name="phone_number" placeholder="e.g., 212687830691" required>

            <label>💬 Caption (optional)</label>
            <textarea name="caption" placeholder="Write a caption..."></textarea>

            <button type="submit">Send to WhatsApp</button>
        </form>
        {% if message %}
            <p><b>{{ message }}</b></p>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        youtube_url = request.form.get("youtube_url")
        phone_number = request.form.get("phone_number")
        caption = request.form.get("caption")

        logging.info(f"Received request: {youtube_url} -> {phone_number}")

        video_path = download_youtube_video(youtube_url)
        if not video_path:
            return render_template_string(HTML_PAGE, message="❌ Failed to download video")

        success = send_whatsapp_video(phone_number, video_path, caption)
        if success:
            return render_template_string(HTML_PAGE, message="✅ Video sent successfully!")
        else:
            return render_template_string(HTML_PAGE, message="❌ Failed to send video")

    return render_template_string(HTML_PAGE)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
