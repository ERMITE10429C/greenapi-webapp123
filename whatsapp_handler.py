import os
import logging
import requests
from colorama import Fore

# Load secrets from environment
GREEN_MEDIA_URL = os.getenv("GREEN_MEDIA_URL")
INSTANCE_ID = os.getenv("GREEN_INSTANCE_ID")
API_TOKEN = os.getenv("GREEN_API_TOKEN")

def send_whatsapp_video(phone_number: str, video_path: str, caption: str = None) -> bool:
    """
    Send a video to WhatsApp using Green API.
    """
    try:
        if not os.path.exists(video_path):
            logging.error(f"{Fore.RED}❌ Video not found: {video_path}")
            return False

        chat_id = f"{phone_number}@c.us"
        filename = os.path.basename(video_path)

        url = f"{GREEN_MEDIA_URL}/waInstance{INSTANCE_ID}/sendFileByUpload/{API_TOKEN}"

        data = {"chatId": chat_id}
        if caption:
            data["caption"] = caption

        with open(video_path, "rb") as f:
            files = [("file", (filename, f, "video/mp4"))]
            logging.info(f"{Fore.YELLOW}📤 Uploading video...")
            resp = requests.post(url, data=data, files=files, timeout=300)

        if resp.status_code == 200:
            logging.info(f"{Fore.GREEN}✅ Sent video to {phone_number}")
            return True
        else:
            logging.error(f"{Fore.RED}❌ Send failed: {resp.status_code} - {resp.text}")
            return False

    except requests.exceptions.RequestException as e:
        logging.error(f"{Fore.RED}❌ Request error: {e}")
        return False
