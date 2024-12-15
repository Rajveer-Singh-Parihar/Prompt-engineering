from flask import Flask, request, jsonify, send_file
import os
import instaloader
from instaloader.exceptions import LoginRequiredException, BadResponseException

app = Flask(__name__)

# Set up the directory to store downloaded videos
DOWNLOAD_FOLDER = "./downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def download_instagram_video(video_url: str) -> str:
    """
    Downloads an Instagram video using the Instaloader library.

    Args:
        video_url (str): URL of the Instagram video.

    Returns:
        str: File path of the downloaded video.
    """
    try:
        loader = instaloader.Instaloader()

        # Extract shortcode from the Instagram video URL
        video_shortcode = video_url.strip().split("/")[-2]
        if not video_shortcode:
            raise ValueError("Invalid Instagram URL provided.")

        print(f"Extracting video with shortcode: {video_shortcode}")

        # Download the video post
        loader.download_post(instaloader.Post.from_shortcode(loader.context, video_shortcode), target=DOWNLOAD_FOLDER)

        # Find the downloaded file (latest in the download directory)
        downloaded_files = sorted(os.listdir(DOWNLOAD_FOLDER), key=lambda x: os.path.getmtime(os.path.join(DOWNLOAD_FOLDER, x)))
        video_file = [f for f in downloaded_files if f.endswith(".mp4")]
        
        if not video_file:
            raise FileNotFoundError("No video file found after downloading.")
        
        video_path = os.path.join(DOWNLOAD_FOLDER, video_file[-1])
        return video_path

    except LoginRequiredException:
        raise Exception("This video requires login to access. Please provide login credentials.")
    except BadResponseException:
        raise Exception("Instagram responded with an error. Please try again.")
    except Exception as e:
        raise Exception(f"An error occurred: {str(e)}")

@app.route("/download", methods=["POST"])
def download_video_api():
    """
    API endpoint to download an Instagram video.

    Request JSON:
    {
        "url": "Instagram video URL"
    }

    Returns:
        JSON Response or the downloaded video file.
    """
    try:
        # Parse input JSON
        data = request.get_json()
        if not data or "url" not in data:
            return jsonify({"error": "Please provide a valid 'url' field in JSON input."}), 400

        video_url = data["url"]

        print(f"Received URL: {video_url}")
        video_path = download_instagram_video(video_url)

        print(f"Video downloaded to: {video_path}")
        return send_file(video_path, as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/", methods=["GET"])
def home():
    """
    Home endpoint to check if the service is running.
    """
    return jsonify({"message": "Instagram Video Downloader API is running."})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
