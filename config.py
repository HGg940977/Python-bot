import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot configuration
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN found in .env file")

# Sticker configuration
MAX_STICKER_SIZE = (512, 512)  # Telegram requires 512x512 pixels
ALLOWED_FORMATS = ['PNG', 'JPEG', 'JPG']