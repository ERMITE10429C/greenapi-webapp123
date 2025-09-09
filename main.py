import os
import requests
import yt_dlp
import logging
from dotenv import load_dotenv
from colorama import Fore, Style, init

# Init colorama
init(autoreset=True)

# Load environment variables
load_dotenv()

GREEN_MEDIA_URL = os.getenv("GREEN_MEDIA_URL")
INSTANCE_ID = os.getenv("GREEN_INSTANCE_ID")
API_TOKEN = os.getenv("GREEN_API_TOKEN")

# Setup logging format
logging.basicConfig(
    level=logging.INFO,
    format=f"{Fore.CYAN}%(asctime)s{Style.RESET_ALL} - %(levelname)s - %(message)s",
    datefmt="%H:%M:%S",
)

DOWNLOADS_DIR = "downloads"
os.makedirs(DOWNLOADS_DIR, exist_ok=True)


def banner():
    print(Fore.GREEN + "=" * 50)
    print(Fore.YELLOW + "   🚀 YouTube → WhatsApp Sender (Green API)")
    print(Fore.GREEN + "=" * 50 + Style.RESET_ALL)


def check_env():
    """Verify environment variables are loaded"""
    if not all([GREEN_MEDIA_URL, INSTANCE_ID, API_TOKEN]):
        logging.error(
            f"{Fore.RED}Missing environment variables! "
            f"Check your .env file or Key Vault in Azure."
        )
        return False
    logging.info(f"{Fore.GREEN}✅ Environment variables loaded successfully")
    return True


def download_youtube_video(url: str) -> str | None:
    """Download YouTube video and return file path"""
    logging.info(f"{Fore.CYAN}📥 Downloading: {url}")
    ydl_opts = {
        "format": "mp4",
        "outtmpl": os.path.join(DOWNLOADS_DIR, "%(title)s.%(ext)s"),
        "noplaylist": True,
        "quiet": False,  # show yt-dlp progress
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = ydl.prepare_filename(info)
        abs_path = os.path.abspath(file_path)
        logging.info(f"{Fore.GREEN}✅ Video downloaded: {abs_path}")
        return abs_path
    except Exception as e:
        logging.error(f"{Fore.RED}❌ Download error: {e}")
        return None


def send_whatsapp_video(phone_number: str, video_path: str, caption: str = None) -> bool:
    """Send video file to WhatsApp via Green API"""
    if not os.path.exists(video_path):
        logging.error(f"{Fore.RED}❌ File not found: {video_path}")
        return False

    url = f"{GREEN_MEDIA_URL}/waInstance{INSTANCE_ID}/sendFileByUpload/{API_TOKEN}"
    chat_id = f"{phone_number}@c.us"

    data = {"chatId": chat_id}
    if caption:
        data["caption"] = caption

    logging.info(f"{Fore.YELLOW}📤 Sending video to WhatsApp...")

    try:
        with open(video_path, "rb") as f:
            files = [("file", (os.path.basename(video_path), f, "video/mp4"))]
            resp = requests.post(url, data=data, files=files, timeout=120)

        if resp.status_code == 200:
            logging.info(f"{Fore.GREEN}✅ Sent to {phone_number}")
            return True
        else:
            logging.error(
                f"{Fore.RED}❌ Failed: {resp.status_code} - {resp.text}"
            )
            return False
    except Exception as e:
        logging.error(f"{Fore.RED}❌ Exception: {e}")
        return False


def main():
    banner()

    if not check_env():
        return

    # Ask user inputs
    youtube_url = input(Fore.CYAN + "👉 Enter YouTube video URL: " + Style.RESET_ALL).strip()
    phone_number = input(Fore.CYAN + "👉 Enter recipient phone (int'l, no '+'): " + Style.RESET_ALL).strip()
    caption = input(Fore.CYAN + "👉 Optional caption (press Enter to skip): " + Style.RESET_ALL).strip() or None

    # Download + send
    video_path = download_youtube_video(youtube_url)
    if video_path:
        send_whatsapp_video(phone_number, video_path, caption)


if __name__ == "__main__":
    main()
