import os
from yt_dlp import YoutubeDL
from django.conf import settings

# TODO: use temperory for downloading then move the file, moviing like this avoide conflicts

def download_video(video_url: str):
    """
    Downloads video from YouTube, Facebook, or other supported sites.
    Returns the full path to the downloaded video.
    """
    # Define download folder
    output_dir = os.path.join(settings.BASE_DIR, "downtoload", "downloads")
    os.makedirs(output_dir, exist_ok=True)

# bestVudeo+basteaudio/best download the highest-quality video stream And the heighest-quality audio stream separately

    # yt_dlp options
    ydl_opts = {
        "outtmpl": os.path.join(output_dir, "%(title)s.%(ext)s"),
        # "merge_output_format": "mp4",  # Only needed if you want to force mp4
        "format": "best",
        "quiet": True,
        "no_warnings": True,
        "ffmpeg_location": r"D:\Applications\ffmpeg\bin\ffmpeg.exe",
        "concurrent_fragment_downloads": 8,  # Parallel fragment downloads (try 5-10)
        "external_downloader": "aria2c",  # Use aria2c if installed
        "external_downloader_args": ["-x", "16", "-k", "1M"],  # 16 connections, 1MB segments
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
        file_path = ydl.prepare_filename(info)
        if not file_path.endswith(".mp4"):
            file_path = os.path.splitext(file_path)[0] + ".mp4"
        return file_path

# this directly in the django view