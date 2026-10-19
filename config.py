import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
API_BASE_URL = os.getenv("API_BASE_URL", "https://osmosys-api.oqsha.com").strip()
API_TOKEN = os.getenv("API_TOKEN", "").strip()
ORGANISATION_ID = os.getenv("ORGANISATION_ID", "").strip()
SITE_ID = os.getenv("SITE_ID", "").strip()
USER_ID = os.getenv("USER_ID", "").strip()
CHECKIN_LATITUDE = float(os.getenv("CHECKIN_LATITUDE", "0"))
CHECKIN_LONGITUDE = float(os.getenv("CHECKIN_LONGITUDE", "0"))
CHECKOUT_LATITUDE = float(os.getenv("CHECKOUT_LATITUDE", "0"))
CHECKOUT_LONGITUDE = float(os.getenv("CHECKOUT_LONGITUDE", "0"))
TEST_PHOTO_PATH = os.getenv("TEST_PHOTO_PATH", "photos/1.jpg").strip()
DRY_RUN = os.getenv("DRY_RUN", "true").lower() in ("1", "true", "yes", "on")
ALLOWED_TELEGRAM_USER_IDS = {
    int(value.strip())
    for value in os.getenv("ALLOWED_TELEGRAM_USER_IDS", "").split(",")
    if value.strip().isdigit()
}
