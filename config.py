"""
Zureka Solutions Limited - Configuration Module
"""
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR = os.path.join(BASE_DIR, 'public')
DATA_FILE = os.path.join(BASE_DIR, 'offline_store.json')

PORT = int(os.environ.get("PORT", 8080))

# Pandora Networks SMS Gateway Configuration
SMS_API_URL = "https://www.sms.thepandoranetworks.com/API/send_sms/"
SMS_USERNAME = os.environ.get("PANDORA_SMS_USER", "0773245712")
SMS_PASSWORD = os.environ.get("PANDORA_SMS_PASS", "Tantum@123")
SMS_SENDER_ID = os.environ.get("PANDORA_SMS_SENDER", "ZUREKA")
SMS_ADMIN_ALERT_PHONE = "256773245712"

COMPANY_NAME = "Zureka Solutions Limited"
TAGLINE = "Building Better Businesses. Together."
LOCATION = "Kampala, Uganda"
PHONE = "+256 773 245 712"
EMAIL = "contact@zurekasolutions.com"
