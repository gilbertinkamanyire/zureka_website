"""
Authentication Views: Login Screen with 1-Click Role Switcher
"""
import config
from templates.base import CSS_STYLES

def render_login(error: bool = False, next_url: str = '') -> str:
    err_banner = """
    <div style="background: #FEE2E2; border: 1px solid #FCA5A5; color: #991B1B; padding: 12px 16px; border-radius: 6px; font-size: 13px; margin-bottom: 20px;">
      ⚠️ Invalid email or password. Please verify your credentials or select a role below.
    </div>
    """ if error else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sign In • Zureka ERPNext Desk</title>
  <link rel="icon" href="/public/images/z_logo.svg" type="image/svg+xml">
  <style>
    {CSS_STYLES}
    .demo-role-btn {{
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      padding: 10px 14px;
      background: #F8FAFC;
      border: 1px solid var(--z-border);
      border-radius: 8px;
      cursor: pointer;
      text-align: left;
      transition: var(--transition);
      width: 100%;
    }}
    .demo-role-btn:hover {{
      background: #F1F5F9;
      border-color: var(--z-gold);
      transform: translateY(-2px);
    }}
  </style>
  <script>
    function quickLogin(email, password) {{
      document.getElementById('email').value = email;
      document.getElementById('password').value = password;
      document.getElementById('loginForm').submit();
    }}
  </script>
</head>
<body style="background: #0B1120; min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 40px 20px;">
  <div style="background: #FFFFFF; border-radius: 16px; max-width: 900px; width: 100%; box-shadow: 0 25px 60px rgba(0,0,0,0.4); overflow: hidden; display: grid; grid-template-columns: 1fr 1.1fr;">
    
    <!-- Left: Credentials Form -->
    <div style="padding: 44px;">
      <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 24px;">
        <img src="/public/images/z_logo.svg" style="height: 36px; width: 36px;" alt="Logo">
        <div>
          <div style="font-weight: 800; font-size: 18px; color: var(--z-navy);">ZUREKA <span style="color: var(--z-gold);">DESK</span></div>
          <div style="font-size: 11px; color: var(--z-slate);">ERPNext Architecture v2.0</div>
        </div>
      </div>

      <h2 style="font-size: 22px; font-weight: 800; color: #0F172A; margin-bottom: 8px;">Portal Authentication</h2>
      <p style="color: #64748B; font-size: 13px; margin-bottom: 24px;">Sign in with your organizational role credentials.</p>

      {err_banner}

      <form id="loginForm" action="/api/login" method="POST">
        <input type="hidden" name="nextUrl" value="{next_url}">
        <div style="margin-bottom: 16px;">
          <label style="display: block; font-size: 12.5px; font-weight: 700; color: #334155; margin-bottom: 6px;">Email Address</label>
          <input type="email" id="email" name="email" required placeholder="admin@zurekasolutions.com" style="width: 100%; padding: 10px 14px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13.5px; outline: none;">
        </div>

        <div style="margin-bottom: 24px;">
          <label style="display: block; font-size: 12.5px; font-weight: 700; color: #334155; margin-bottom: 6px;">Password</label>
          <input type="password" id="password" name="password" required placeholder="••••••••" style="width: 100%; padding: 10px 14px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13.5px; outline: none;">
        </div>

        <button type="submit" class="btn btn-gold" style="width: 100%; padding: 12px; font-size: 14px;">Sign In to Desk &rarr;</button>
      </form>

      <div style="margin-top: 24px; text-align: center;">
        <a href="/" style="font-size: 13px; color: var(--z-slate); font-weight: 600;">&larr; Return to Public Site</a>
      </div>
    </div>

    <!-- Right: 1-Click Role Switcher -->
    <div style="background: #F8FAFC; border-left: 1px solid var(--z-border); padding: 40px; display: flex; flex-direction: column;">
      <div style="font-size: 12px; font-weight: 800; text-transform: uppercase; color: var(--z-gold); letter-spacing: 0.8px; margin-bottom: 6px;">
        1-Click Role Switcher
      </div>
      <h3 style="font-size: 16px; font-weight: 800; color: #0F172A; margin-bottom: 16px;">Instant Persona Testing</h3>
      <div style="display: flex; flex-direction: column; gap: 10px; overflow-y: auto; max-height: 480px; padding-right: 6px;">
        
        <button type="button" class="demo-role-btn" onclick="quickLogin('admin@zurekasolutions.com', 'admin123')">
          <div style="display: flex; justify-content: space-between; width: 100%; margin-bottom: 4px;">
            <span style="font-weight: 700; font-size: 13px; color: #0F172A;">Dr. Arthur Ssewankambo</span>
            <span class="badge badge-gold" style="font-size: 10px;">Admin</span>
          </div>
          <div style="font-size: 11.5px; color: #64748B;">Managing Partner & System Manager</div>
        </button>

        <button type="button" class="demo-role-btn" onclick="quickLogin('erp.lead@zurekasolutions.com', 'zureka123')">
          <div style="display: flex; justify-content: space-between; width: 100%; margin-bottom: 4px;">
            <span style="font-weight: 700; font-size: 13px; color: #0F172A;">Eng. Brian Mukasa</span>
            <span class="badge badge-blue" style="font-size: 10px;">Lead ERP</span>
          </div>
          <div style="font-size: 11.5px; color: #64748B;">Practice Lead - Enterprise Solutions</div>
        </button>

        <button type="button" class="demo-role-btn" onclick="quickLogin('data.lead@zurekasolutions.com', 'zureka123')">
          <div style="display: flex; justify-content: space-between; width: 100%; margin-bottom: 4px;">
            <span style="font-weight: 700; font-size: 13px; color: #0F172A;">Fiona Atuhaire, MSc</span>
            <span class="badge badge-purple" style="font-size: 10px;">Lead Data</span>
          </div>
          <div style="font-size: 11.5px; color: #64748B;">Practice Lead - Data, BI & AI</div>
        </button>

        <button type="button" class="demo-role-btn" onclick="quickLogin('sales@zurekasolutions.com', 'zureka123')">
          <div style="display: flex; justify-content: space-between; width: 100%; margin-bottom: 4px;">
            <span style="font-weight: 700; font-size: 13px; color: #0F172A;">Patricia Namubiru</span>
            <span class="badge badge-green" style="font-size: 10px;">Sales</span>
          </div>
          <div style="font-size: 11.5px; color: #64748B;">Business Development & CRM</div>
        </button>

        <button type="button" class="demo-role-btn" onclick="quickLogin('finance@zurekasolutions.com', 'zureka123')">
          <div style="display: flex; justify-content: space-between; width: 100%; margin-bottom: 4px;">
            <span style="font-weight: 700; font-size: 13px; color: #0F172A;">David Ochieng, CPA</span>
            <span class="badge badge-gold" style="font-size: 10px;">Finance</span>
          </div>
          <div style="font-size: 11.5px; color: #64748B;">Finance & Billing Controller</div>
        </button>

        <button type="button" class="demo-role-btn" onclick="quickLogin('client@victoriamfg.ug', 'client123')">
          <div style="display: flex; justify-content: space-between; width: 100%; margin-bottom: 4px;">
            <span style="font-weight: 700; font-size: 13px; color: #0F172A;">Grace Nakalema</span>
            <span class="badge badge-blue" style="font-size: 10px;">Client</span>
          </div>
          <div style="font-size: 11.5px; color: #64748B;">Victoria Manufacturing Ltd (Customer)</div>
        </button>

      </div>
    </div>

  </div>
</body>
</html>"""
