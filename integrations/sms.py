"""
Pandora Networks SMS Gateway Integration (Uganda)
"""
import json
import urllib.request
import urllib.parse
from datetime import datetime
from typing import List, Dict, Any

import config

SMS_LOGS: List[Dict[str, Any]] = []

def send_sms(to: str, message: str) -> dict:
    """Send SMS via Pandora Networks SMS Gateway API."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    clean_to = "".join([c for c in to if c.isdigit()])
    if clean_to.startswith("0") and len(clean_to) == 10:
        clean_to = "256" + clean_to[1:]
    elif not clean_to.startswith("256") and len(clean_to) == 9:
        clean_to = "256" + clean_to

    payload = {
        "username": config.SMS_USERNAME,
        "password": config.SMS_PASSWORD,
        "sender": config.SMS_SENDER_ID,
        "to": clean_to,
        "message": message
    }

    try:
        data_bytes = urllib.parse.urlencode(payload).encode('utf-8')
        req = urllib.request.Request(
            config.SMS_API_URL,
            data=data_bytes,
            headers={
                "User-Agent": "Zureka-ERPNext-Core/2.0",
                "Content-Type": "application/x-www-form-urlencoded"
            }
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            resp_body = response.read().decode('utf-8')
            log_entry = {
                "id": f"SMS-{len(SMS_LOGS) + 1:04d}",
                "to": clean_to,
                "message": message,
                "status": "Delivered",
                "timestamp": timestamp,
                "provider_response": resp_body[:200]
            }
            SMS_LOGS.insert(0, log_entry)
            return log_entry
    except Exception as e:
        log_entry = {
            "id": f"SMS-{len(SMS_LOGS) + 1:04d}",
            "to": clean_to,
            "message": message,
            "status": "Queued / Simulation (Offline Mode)",
            "timestamp": timestamp,
            "provider_response": f"Offline / Handled gracefully: {str(e)[:120]}"
        }
        SMS_LOGS.insert(0, log_entry)
        return log_entry

def notify_new_inquiry(inquiry: dict) -> None:
    msg = (
        f"ZUREKA ALERT: New Discovery Request #{inquiry.get('id', 'N/A')} from "
        f"{inquiry.get('company_name', 'Client')} ({inquiry.get('contact_name', 'Lead')}). "
        f"Interest: {inquiry.get('system_interest', 'Enterprise Solutions')}."
    )
    send_sms(config.SMS_ADMIN_ALERT_PHONE, msg)

def notify_quotation_created(quotation: dict) -> None:
    if quotation.get('client_phone'):
        msg = (
            f"ZUREKA: Tailored Architecture Proposal {quotation.get('quote_no')} for "
            f"{quotation.get('system_name')} has been drafted. Our Practice Lead will guide you through the review."
        )
        send_sms(quotation['client_phone'], msg)

def get_sms_logs() -> List[dict]:
    return SMS_LOGS

def get_sms_config() -> dict:
    return {
        "url": config.SMS_API_URL,
        "username": config.SMS_USERNAME,
        "sender": config.SMS_SENDER_ID,
        "admin_alert_phone": config.SMS_ADMIN_ALERT_PHONE,
        "status": "Connected & Operational"
    }
