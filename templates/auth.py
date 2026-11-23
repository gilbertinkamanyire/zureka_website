"""
Authentication Views: Production Clean Login Screen
"""
import config
from templates.base import CSS_STYLES

def render_login(error: bool = False, next_url: str = '') -> str:
    err_banner = """
    <div style="background: #FEE2E2; border: 1px solid #FCA5A5; color: #991B1B; padding: 12px 16px; border-radius: 6px; font-size: 13px; margin-bottom: 20px;">
      ⚠️ Invalid email or password. Please verify your credentials.
    </div>
    """ if error else ""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sign In • {config.COMPANY_NAME}</title>
  <link rel="icon" href="/public/images/z_logo.svg" type="image/svg+xml">
  <style>
    {CSS_STYLES}
  </style>
</head>
<body style="background: #0B1120; min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 40px 20px;">
  <div style="background: #FFFFFF; border-radius: 14px; max-width: 440px; width: 100%; box-shadow: 0 25px 60px rgba(0,0,0,0.45); padding: 44px; border: 1px solid #1E293B;">
    
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 28px;">
      <img src="/public/images/z_logo.svg" style="height: 40px; width: 40px;" alt="Logo">
      <div>
        <div style="font-weight: 900; font-size: 20px; color: var(--z-navy); line-height: 1.1;">ZUREKA <span style="color: var(--z-gold);">DESK</span></div>
        <div style="font-size: 11px; color: var(--z-slate); font-weight: 600;">Enterprise ERP Portal</div>
      </div>
    </div>

    <h2 style="font-size: 22px; font-weight: 800; color: #0F172A; margin-bottom: 6px;">Sign In</h2>
    <p style="color: #64748B; font-size: 13.5px; margin-bottom: 24px;">Enter your organizational credentials to continue.</p>

    {err_banner}

    <form id="loginForm" action="/api/login" method="POST">
      <input type="hidden" name="nextUrl" value="{next_url}">
      <div style="margin-bottom: 18px;">
        <label style="display: block; font-size: 12.5px; font-weight: 700; color: #334155; margin-bottom: 6px;">Email Address</label>
        <input type="email" id="email" name="email" required placeholder="you@zurekasolutions.com" style="width: 100%; padding: 11px 14px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13.5px; outline: none; transition: var(--transition);" onfocus="this.style.borderColor='var(--z-gold)'" onblur="this.style.borderColor='var(--z-border)'">
      </div>

      <div style="margin-bottom: 24px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
          <label style="font-size: 12.5px; font-weight: 700; color: #334155;">Password</label>
        </div>
        <input type="password" id="password" name="password" required placeholder="••••••••" style="width: 100%; padding: 11px 14px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13.5px; outline: none; transition: var(--transition);" onfocus="this.style.borderColor='var(--z-gold)'" onblur="this.style.borderColor='var(--z-border)'">
      </div>

      <button type="submit" class="btn btn-gold" style="width: 100%; padding: 12px; font-size: 14px; font-weight: 800;">Sign In &rarr;</button>
    </form>

    <div style="margin-top: 28px; text-align: center; border-top: 1px solid var(--z-border); padding-top: 20px;">
      <a href="/" style="font-size: 13px; color: var(--z-slate); font-weight: 600;">&larr; Return to Public Website</a>
    </div>

  </div>
</body>
</html>"""
