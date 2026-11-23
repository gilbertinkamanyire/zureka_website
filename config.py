"""
Zureka Solutions Limited - Configuration Module
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')
DATA_FILE = os.path.join(BASE_DIR, 'offline_store.json')

# Pure-Python .env file loader (zero external packages)
env_path = os.path.join(BASE_DIR, '.env')
if os.path.exists(env_path):
    try:
        with open(env_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, val = line.split('=', 1)
                    key = key.strip()
                    val = val.strip().strip('"').strip("'")
                    if key and key not in os.environ:
                        os.environ[key] = val
    except Exception:
        pass

PORT = int(os.environ.get("PORT", 8080))

# PostgreSQL Database Configuration
DATABASE_URL = os.environ.get("DATABASE_URL")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Pandora Networks SMS Gateway Configuration
SMS_API_URL = "https://www.sms.thepandoranetworks.com/API/send_sms/"
SMS_USERNAME = os.environ.get("PANDORA_SMS_USER", "0773245712")
SMS_PASSWORD = os.environ.get("PANDORA_SMS_PASS", "Tantum@123")
SMS_SENDER_ID = os.environ.get("PANDORA_SMS_SENDER", "ZUREKA")
SMS_ADMIN_ALERT_PHONE = os.environ.get("PANDORA_SMS_ALERT_PHONE", "256773245712")

COMPANY_NAME = os.environ.get("COMPANY_NAME", "Zureka Solutions Limited")
TAGLINE = os.environ.get("TAGLINE", "Building Better Businesses. Together.")
LOCATION = os.environ.get("LOCATION", "Kampala, Uganda")
PHONE = os.environ.get("PHONE", "+256 773 245 712")
EMAIL = os.environ.get("EMAIL", "contact@zurekasolutions.com")
