import os
import dotenv

dotenv.load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN_PROD")
TARGET_CHAT_ID = os.getenv("TARGET_CHAT_ID")
TELEGRAM_CHAT_LINK = os.getenv("TELEGRAM_CHAT_LINK")

STRIPE_WEBHOOK_HOST=os.getenv("STRIPE_WEBHOOK_HOST", "localhost")
STRIPE_WEBHOOK_PORT=os.getenv("STRIPE_WEBHOOK_PORT")