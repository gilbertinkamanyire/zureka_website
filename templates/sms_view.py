"""
SMS Gateway Management & Broadcast Center
"""
from typing import List
from templates.base import render_desk_base

def render_desk_sms(user: dict, logs: List[dict], config_info: dict, can_broadcast: bool, sent_notice: bool = False, default_to: str = '') -> str:
    notice = """
    <div style="background: #DCFCE7; border: 1px solid #86EFAC; color: #166534; padding: 12px 16px; border-radius: 6px; font-size: 13.5px; margin-bottom: 20px;">
      ✓ SMS message successfully dispatched through Pandora Networks Gateway API!
    </div>
    """ if sent_notice else ""

    broadcast_form = f"""
    <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 10px; padding: 24px; box-shadow: var(--card-shadow); margin-bottom: 30px;">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 14px;">
        <h3 style="font-size: 16px; font-weight: 800; color: #0F172A;">Instant SMS Dispatch & Telephony</h3>
        <div style="font-size: 12px; color: #64748B;">Sender ID: <strong>{config_info.get('sender')}</strong></div>
      </div>
      
      <!-- Template Pills -->
      <div style="display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap;">
        <span style="font-size: 11px; font-weight: 700; color: #64748B; align-self: center;">Quick Templates:</span>
        <button type="button" class="btn btn-outline btn-sm" onclick="setTemplate('ZUREKA: Your enterprise proposal is ready for review. Kindly check your email or portal for full scope details.')">📄 Proposal Ready</button>
        <button type="button" class="btn btn-outline btn-sm" onclick="setTemplate('ZUREKA: We have received your payment for the project milestone. Thank you for partnering with Zureka Solutions.')">💰 Payment Received</button>
        <button type="button" class="btn btn-outline btn-sm" onclick="setTemplate('ZUREKA: Delivery milestone has reached 100% completion. User Acceptance Testing (UAT) is now scheduled.')">🚀 Milestone UAT</button>
        <button type="button" class="btn btn-outline btn-sm" onclick="setTemplate('ZUREKA ALERT: Scheduled maintenance on your ERPNext cloud instance tonight 11:00 PM - 12:00 AM EAT.')">⚙️ Maintenance Alert</button>
      </div>

      <form action="/api/sms/send" method="POST">
        <div style="display: grid; grid-template-columns: 1fr 2fr auto; gap: 16px; align-items: flex-end;">
          <div>
            <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 6px;">Recipient Phone Number *</label>
            <input type="text" name="to" id="smsToInput" required value="{default_to}" placeholder="0773245712 or 2567..." style="width: 100%; padding: 10px 14px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13.5px;">
          </div>
          <div>
            <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 6px;">Message Content (160 characters max) *</label>
            <input type="text" name="message" id="smsMsgInput" required maxlength="160" placeholder="ZUREKA: Your enterprise proposal is ready for review..." style="width: 100%; padding: 10px 14px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13.5px;">
          </div>
          <button type="submit" class="btn btn-gold" style="padding: 10px 20px; font-size: 13.5px;">
            Send SMS &rarr;
          </button>
        </div>
      </form>
    </div>

    <script>
    function setTemplate(msg) {{
      document.getElementById('smsMsgInput').value = msg;
    }}
    </script>
    """ if can_broadcast else """
    <div style="background: #FFFBEB; border: 1px solid #FDE68A; color: #92400E; padding: 14px 18px; border-radius: 8px; font-size: 13px; margin-bottom: 24px;">
      ℹ️ Your role has read-only access to SMS logs. Broadcaster privileges are reserved for Administrator and Practice Leads.
    </div>
    """

    log_rows = ""
    for entry in logs:
        log_rows += f"""
        <tr>
          <td style="font-family: monospace; font-size: 12px; color: #64748B;">{entry.get('id')}</td>
          <td style="font-size: 12.5px; color: #475569;">{entry.get('timestamp')}</td>
          <td style="font-weight: 700; color: #0F172A;">{entry.get('to')}</td>
          <td style="font-size: 13px; color: #334155;">{entry.get('message')}</td>
          <td><span class="indicator-pill indicator-paid"><span class="indicator-dot"></span>{entry.get('status')}</span></td>
        </tr>
        """
    if not log_rows:
        log_rows = "<tr><td colspan='5' style='text-align: center; color: #94A3B8; padding: 30px;'>No SMS messages logged yet. Use the dispatch form above to send an SMS.</td></tr>"

    content = f"""
    <div class="erp-header">
      <div>
        <h1 class="erp-title">Pandora Networks SMS Gateway</h1>
        <div class="erp-subtitle">Mission-critical enterprise telephony integrated with Pandora Networks SMS API (Uganda)</div>
      </div>
    </div>

    {notice}

    <!-- Gateway Status Card -->
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 28px;">
      <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 10px; padding: 18px; box-shadow: var(--card-shadow);">
        <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase;">Gateway Connection</div>
        <div style="font-size: 16px; font-weight: 800; color: #166534; margin-top: 6px;">● Operational & Live</div>
      </div>
      <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 10px; padding: 18px; box-shadow: var(--card-shadow);">
        <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase;">API Account Username</div>
        <div style="font-size: 15px; font-weight: 800; color: #0F172A; margin-top: 6px;">{config_info.get('username')}</div>
      </div>
      <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 10px; padding: 18px; box-shadow: var(--card-shadow);">
        <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase;">Sender Mask</div>
        <div style="font-size: 16px; font-weight: 800; color: var(--z-gold-dark); margin-top: 6px;">{config_info.get('sender')}</div>
      </div>
      <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 10px; padding: 18px; box-shadow: var(--card-shadow);">
        <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase;">Admin Notification Alert Line</div>
        <div style="font-size: 15px; font-weight: 800; color: #0F172A; margin-top: 6px;">+{config_info.get('admin_alert_phone')}</div>
      </div>
    </div>

    {broadcast_form}

    <h3 style="font-size: 16px; font-weight: 800; color: #0F172A; margin-bottom: 12px;">Transmission Logs</h3>
    <div class="table-wrap">
      <table class="z-table">
        <thead>
          <tr>
            <th>Transmission ID</th>
            <th>Timestamp</th>
            <th>Recipient MSISDN</th>
            <th>Message Payload</th>
            <th>Delivery Status</th>
          </tr>
        </thead>
        <tbody>
          {log_rows}
        </tbody>
      </table>
    </div>
    """
    return render_desk_base("SMS Gateway", user, content, active_tab='sms', breadcrumbs=[("Integrations", "/desk/sms"), ("SMS Gateway", None)])
