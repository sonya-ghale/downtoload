import os
from yt_dlp import YoutubeDL
from django.conf import settings

# need progress_data to be dictinoary that stores the dowload pogress
progress_data = {}


# TODO: use temperory for downloading then move the file, moviing like this avoide conflicts
def download_video(video_url: str, save_path=None, filename=None, extract_flat=False):
    """
    Downloads video from YouTube, Facebook, or other supported sites.
    Returns the full path to the downloaded video.
    """
    # Define download folder
    output_dir = save_path or os.path.join(settings.BASE_DIR, "downtoload", "media")
    os.makedirs(output_dir, exist_ok=True)

    if filename:
        outtmpl = os.path.join(output_dir, filename)
    else:
        outtmpl = os.path.join(output_dir, "%(title)s.%(ext)s")

    # bestVudeo+basteaudio/best download the highest-quality video stream And the heighest-quality audio stream separately

    #========= yt_dlp options ==========
    ydl_opts = {
        "outtmpl": outtmpl,
        # "merge_output_format": "mp4",  # Only needed if you want to force mp4
        # "format": "best",
        "format": "bestvideo+bestaudio/best",
        "quiet": True,
        "no_warnings": True,
        "ffmpeg_location": r"D:\Applications\ffmpeg\bin\ffmpeg.exe",
        "concurrent_fragment_downloads": 8,  # Parallel fragment downloads (try 5-10)
        "external_downloader": "aria2c",  # Use aria2c if installed
        "external_downloader_args": ["-x", "16", "-k", "1M"],  # 16 connections, 1MB segments
        # delete it to download all the paylist not one
        "noplaylist": True,
        # "nonplaylist": not extract_flat,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=not extract_flat)

        if extract_flat:
            if "entries" in info:      # playlist
                return info["entries"]
            else:                      # single video
                return [info]

        file_path = ydl.prepare_filename(info)
        if not file_path.endswith(".mp4"):
            file_path = os.path.splitext(file_path)[0] + ".mp4"
        return file_path


    # this directly in the django view