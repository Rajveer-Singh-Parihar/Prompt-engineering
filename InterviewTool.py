from flask import Flask, request, jsonify, render_template_string
from moviepy.editor import AudioFileClip
import openai
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Replace with your OpenAI API key
openai.api_key = "YOUR_OPENAI_API_KEY"

# Allowed file extensions
ALLOWED_EXTENSIONS = {"webm", "mp4", "wav"}

# Check for valid file extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to transcribe audio using Whisper
def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = openai.Audio.transcribe("whisper-1", audio_file)
    return transcript["text"]

# Function to summarize text using GPT-4
def summarize_text(text):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Summarize the given interview response briefly."},
            {"role": "user", "content": text}
        ]
    )
    return response['choices'][0]['message']['content']

# Route for the main page
@app.route('/')
def index():
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Interview Tool</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            background-color: #f4f4f9;
        }
        h1 {
            color: #333;
        }
        video {
            width: 80%;
            max-width: 600px;
            margin-top: 20px;
        }
        button {
            margin: 10px;
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
        }
        #result {
            margin-top: 20px;
            white-space: pre-wrap;
        }
    </style>
</head>
<body>
    <h1>Interview Tool</h1>
    <p>Record your answer for 1 minute:</p>
    <video id="preview" autoplay muted></video>
    <button id="start">Start Recording</button>
    <button id="stop" disabled>Stop Recording</button>

    <div id="result"></div>

    <script>
        let mediaRecorder;
        let recordedChunks = [];

        // Start Webcam Preview
        const preview = document.getElementById("preview");
        navigator.mediaDevices.getUserMedia({ video: true, audio: true })
            .then(stream => {
                preview.srcObject = stream;
                mediaRecorder = new MediaRecorder(stream);

                // Record Data Chunks
                mediaRecorder.ondataavailable = event => recordedChunks.push(event.data);

                // Upload Video on Stop
                mediaRecorder.onstop = () => {
                    const blob = new Blob(recordedChunks, { type: "video/webm" });
                    const formData = new FormData();
                    formData.append("file", blob, "recording.webm");

                    fetch("/upload", {
                        method: "POST",
                        body: formData
                    })
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById("result").innerHTML = `
                            <h3>Transcription:</h3>
                            <p>${data.transcription}</p>
                            <h3>Summary:</h3>
                            <p>${data.summary}</p>
                        `;
                    });
                };
            });

        // Button Logic
        document.getElementById("start").onclick = () => {
            recordedChunks = [];
            mediaRecorder.start();
            document.getElementById("start").disabled = true;
            document.getElementById("stop").disabled = false;

            setTimeout(() => {
                mediaRecorder.stop();
                document.getElementById("start").disabled = false;
                document.getElementById("stop").disabled = true;
            }, 60000); // 1 minute
        };

        document.getElementById("stop").onclick = () => {
            mediaRecorder.stop();
            document.getElementById("start").disabled = false;
            document.getElementById("stop").disabled = true;
        };
    </script>
</body>
</html>
    """)

# Route to handle video upload, transcription, and summarization
@app.route('/upload', methods=['POST'])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part"})

    file = request.files["file"]

    if file and allowed_file(file.filename):
        filename = os.path.join(UPLOAD_FOLDER, "recording.webm")
        file.save(filename)

        # Extract audio from video
        audio_path = filename.replace(".webm", ".wav")
        AudioFileClip(filename).write_audiofile(audio_path, codec='pcm_s16le')

        # Transcribe audio
        transcription = transcribe_audio(audio_path)

        # Summarize transcription
        summary = summarize_text(transcription)

        # Return results
        return jsonify({
            "transcription": transcription,
            "summary": summary
        })

    return jsonify({"error": "Invalid file format"})

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
