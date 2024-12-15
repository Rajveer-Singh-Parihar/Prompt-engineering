import os
from pytube import YouTube
from pytube.exceptions import VideoUnavailable, RegexMatchError
import sys

def download_youtube_video(video_url: str, save_path: str = "./downloads") -> None:
    """
    Downloads a YouTube video to a specified path.

    Args:
        video_url (str): The URL of the YouTube video.
        save_path (str): Directory where the video will be saved (default: './downloads').

    Returns:
        None
    """
    try:
        # Step 1: Initialize YouTube object
        print("\nInitializing video download...")
        yt = YouTube(video_url)

        # Step 2: Display video details
        print(f"Title: {yt.title}")
        print(f"Length: {yt.length} seconds")
        print(f"Author: {yt.author}")

        # Step 3: Choose video stream (highest resolution progressive stream)
        print("\nFetching available streams...")
        stream = yt.streams.filter(progressive=True, file_extension="mp4").order_by('resolution').desc().first()

        if not stream:
            print("No progressive video streams available.")
            return

        print(f"Downloading stream: {stream.resolution} - {stream.mime_type}")

        # Step 4: Ensure save directory exists
        os.makedirs(save_path, exist_ok=True)
        
        # Step 5: Download the video
        print("\nDownloading...")
        stream.download(output_path=save_path)
        print(f"Download complete! Video saved at: {os.path.join(save_path, yt.title)}.mp4")
    
    except VideoUnavailable:
        print("Error: The video is unavailable. Please check the URL.")
    except RegexMatchError:
        print("Error: Invalid YouTube URL format. Please verify the link.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Step 6: Get user input for URL and save path
    video_url = input("Enter the YouTube video URL: ").strip()
    save_path = input("Enter directory to save the video (leave blank for './downloads'): ").strip()

    if not save_path:
        save_path = "./downloads"

    download_youtube_video(video_url, save_path)
