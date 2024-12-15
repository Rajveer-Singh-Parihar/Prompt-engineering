import os
from flask import Flask, Response, render_template_string

app = Flask(__name__)

# FFmpeg Command to Capture and Stream Video
def generate_stream():
    ffmpeg_command = "ffmpeg -re -f v4l2 -i /dev/video0 -c:v libx264 -preset ultrafast -tune zerolatency -f mpegts pipe:1"
    process = os.popen(ffmpeg_command, 'rb')  # Run FFmpeg as a pipe
    while True:
        data = process.read(1024)  # Read the video stream in chunks
        if not data:
            break
        yield data

# Route to Serve the Video Stream
@app.route('/video')
def video_feed():
    return Response(generate_stream(), mimetype='video/mp4')

# Route to Serve the HTML Page
@app.route('/')
def index():
    # HTML Code Embedded Directly
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Live Video Stream</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                text-align: center;
                margin: 0;
                padding: 0;
                background-color: #f4f4f9;
            }
            h1 {
                color: #333;
                margin-top: 20px;
            }
            video {
                margin-top: 20px;
                border: 2px solid #0078d7;
                border-radius: 10px;
                width: 80%;
                max-width: 800px;
                height: auto;
            }
        </style>
    </head>
    <body>
        <h1>Live Video Stream</h1>
        <video id="video" autoplay controls>
            <source src="/video" type="video/mp4">
            Your browser does not support video playback.
        </video>
    </body>
    </html>
    """
    return render_template_string(html_content)

if __name__ == '__main__':
    print("Starting Flask Video Streaming Server...")
    app.run(host='0.0.0.0', port=5000, debug=True)
