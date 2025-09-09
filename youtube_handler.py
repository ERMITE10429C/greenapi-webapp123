import os
import yt_dlp
import logging
from colorama import Fore

DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)

def download_youtube_video(url: str) -> str | None:
    """
    Download a YouTube video and return its file path.
    """
    try:
        logging.info(f"{Fore.CYAN}📥 Downloading: {url}")

        ydl_opts = {
            "format": "mp4",
            "outtmpl": os.path.join(DOWNLOADS_DIR, "%(title)s.%(ext)s"),
            "noplaylist": True,
            "quiet": False,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)

        abs_path = os.path.abspath(file_path)
        logging.info(f"{Fore.GREEN}✅ Downloaded: {abs_path}")
        return abs_path

    except Exception as e:
        logging.error(f"{Fore.RED}❌ Download error: {e}")
        return None
