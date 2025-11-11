import os
import dotenv

dotenv.load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TARGET_CHAT_ID = os.getenv("TARGET_CHAT_ID")

STRIPE_WEBHOOK_HOST=os.getenv("STRIPE_WEBHOOK_HOST", "localhost")
STRIPE_WEBHOOK_PORT=os.getenv("STRIPE_WEBHOOK_PORT", "8000")