"""
User Profile & Account Settings View (ERPNext Style)
"""
from templates.base import render_desk_base
from core.rbac import get_role_label, get_role_badge

def render_profile_page(user: dict, updated: bool = False, pwd_success: bool = False, pwd_error: bool = False) -> str:
    role = user.get('role', 'client')
    role_label = get_role_label(role)
    role_badge = get_role_badge(role)

    notice_html = ""
    if updated:
        notice_html = """
        <div style="background: #DCFCE7; border: 1px solid #86EFAC; color: #166534; padding: 12px 18px; border-radius: 8px; font-size: 13.5px; font-weight: 600; margin-bottom: 24px; display: flex; align-items: center; gap: 8px;">
          <span>✓</span> Your personal profile and contact details have been updated successfully!
        </div>
        """
    elif pwd_success:
        notice_html = """
        <div style="background: #DCFCE7; border: 1px solid #86EFAC; color: #166534; padding: 12px 18px; border-radius: 8px; font-size: 13.5px; font-weight: 600; margin-bottom: 24px; display: flex; align-items: center; gap: 8px;">
          <span>✓</span> Your security password has been changed successfully.
        </div>
        """
    elif pwd_error:
        notice_html = """
        <div style="background: #FEE2E2; border: 1px solid #FCA5A5; color: #991B1B; padding: 12px 18px; border-radius: 8px; font-size: 13.5px; font-weight: 600; margin-bottom: 24px; display: flex; align-items: center; gap: 8px;">
          <span>⚠️</span> Could not update password. Please ensure your current password is correct and your new passwords match.
        </div>
        """

    content = f"""
    <div class="erp-header">
      <div>
        <h1 class="erp-title">My Account Settings</h1>
        <div class="erp-subtitle">Manage your personal identity, contact telecommunications, and security credentials</div>
      </div>
      <div class="erp-actions">
        <a href="/desk" class="btn btn-navy">&larr; Back to Desk</a>
      </div>
    </div>

    {notice_html}

    <!-- User Identity Card -->
    <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 12px; padding: 24px 30px; box-shadow: var(--card-shadow); margin-bottom: 28px; display: flex; align-items: center; justify-content: space-between;">
      <div style="display: flex; align-items: center; gap: 18px;">
        <div class="desk-avatar" style="width: 56px; height: 56px; font-size: 22px; background: var(--z-gold); color: #0F172A; border: 3px solid #F1F5F9;">
          {user.get('avatar', 'U')}
        </div>
        <div>
          <div style="display: flex; align-items: center; gap: 10px;">
            <h2 style="font-size: 20px; font-weight: 900; color: #0F172A;">{user.get('full_name')}</h2>
            <span class="z-badge" style="background: var(--z-gold-light); color: var(--z-gold-dark); font-weight: 800;">{role_badge}</span>
          </div>
          <div style="color: #64748B; font-size: 13.5px; margin-top: 3px;">
            {user.get('email')} &bull; {role_label}
          </div>
          <div style="color: var(--z-navy); font-size: 12.5px; font-weight: 600; margin-top: 3px;">
            Department: {user.get('department', 'Zureka Solutions')}
          </div>
        </div>
      </div>

      <div style="text-align: right; border-left: 1px solid var(--z-border); padding-left: 28px;">
        <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase;">SMS Gateway Alerts</div>
        <div style="font-size: 14px; font-weight: 800; color: #16A34A; margin-top: 3px;">● Enabled</div>
        <div style="font-size: 12px; color: #64748B; margin-top: 2px;">{user.get('phone', '+256 ...')}</div>
      </div>
    </div>

    <!-- Edit Profile & Password Two-Column Grid -->
    <div style="display: grid; grid-template-columns: 1.4fr 1fr; gap: 28px; align-items: flex-start;">
      
      <!-- Section 1: Profile Information -->
      <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 12px; padding: 32px; box-shadow: var(--card-shadow);">
        <h3 style="font-size: 16px; font-weight: 800; color: #0F172A; margin-bottom: 6px;">Profile & Professional Details</h3>
        <p style="font-size: 13px; color: #64748B; margin-bottom: 24px;">Update how your name, designation, and phone number appear across ERPNext.</p>

        <form action="/api/profile/update" method="POST">
          <div style="margin-bottom: 18px;">
            <label style="display: block; font-size: 12.5px; font-weight: 700; color: #334155; margin-bottom: 6px;">Full Name *</label>
            <input type="text" name="full_name" required value="{user.get('full_name', '')}" style="width: 100%; padding: 10px 14px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13.5px; font-weight: 600;">
          </div>

          <div style="margin-bottom: 18px;">
            <label style="display: block; font-size: 12.5px; font-weight: 700; color: #334155; margin-bottom: 6px;">Official Email (Corporate ID)</label>
            <input type="email" readonly value="{user.get('email', '')}" style="width: 100%; padding: 10px 14px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13.5px; background: #F8FAFC; color: #64748B; cursor: not-allowed;">
            <span style="font-size: 11px; color: #94A3B8;">Email address serves as your primary system identity and cannot be altered directly.</span>
          </div>

          <div style="margin-bottom: 18px;">
            <label style="display: block; font-size: 12.5px; font-weight: 700; color: #334155; margin-bottom: 6px;">Phone Number (Pandora SMS Gateway) *</label>
            <input type="text" name="phone" required value="{user.get('phone', '')}" placeholder="+256 772 000 000" style="width: 100%; padding: 10px 14px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13.5px; font-weight: 600;">
            <span style="font-size: 11px; color: #94A3B8;">Used to receive real-time SMS notifications for proposal approvals and invoice payments.</span>
          </div>

          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px;">
            <div>
              <label style="display: block; font-size: 12.5px; font-weight: 700; color: #334155; margin-bottom: 6px;">Job Title / Designation</label>
              <input type="text" name="title" value="{user.get('title', '')}" placeholder="e.g. Managing Partner / Senior Consultant" style="width: 100%; padding: 10px 14px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13.5px;">
            </div>
            <div>
              <label style="display: block; font-size: 12.5px; font-weight: 700; color: #334155; margin-bottom: 6px;">Department / Practice</label>
              <input type="text" name="department" value="{user.get('department', '')}" placeholder="e.g. Enterprise Solutions Practice" style="width: 100%; padding: 10px 14px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13.5px;">
            </div>
          </div>

          <button type="submit" class="btn btn-gold" style="font-size: 14px; padding: 10px 24px;">
            Save Profile Changes &rarr;
          </button>
        </form>
      </div>

      <!-- Section 2: Security & Password -->
      <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 12px; padding: 32px; box-shadow: var(--card-shadow);">
        <h3 style="font-size: 16px; font-weight: 800; color: #0F172A; margin-bottom: 6px;">Security & Password</h3>
        <p style="font-size: 13px; color: #64748B; margin-bottom: 24px;">Change your login password. Must be at least 6 characters.</p>

        <form action="/api/profile/change-password" method="POST">
          <div style="margin-bottom: 18px;">
            <label style="display: block; font-size: 12.5px; font-weight: 700; color: #334155; margin-bottom: 6px;">Current Password *</label>
            <input type="password" name="current_password" required placeholder="••••••••" style="width: 100%; padding: 10px 14px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13.5px;">
          </div>

          <div style="margin-bottom: 18px;">
            <label style="display: block; font-size: 12.5px; font-weight: 700; color: #334155; margin-bottom: 6px;">New Password *</label>
            <input type="password" name="new_password" required minlength="6" placeholder="••••••••" style="width: 100%; padding: 10px 14px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13.5px;">
          </div>

          <div style="margin-bottom: 24px;">
            <label style="display: block; font-size: 12.5px; font-weight: 700; color: #334155; margin-bottom: 6px;">Confirm New Password *</label>
            <input type="password" name="confirm_password" required minlength="6" placeholder="••••••••" style="width: 100%; padding: 10px 14px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13.5px;">
          </div>

          <button type="submit" class="btn btn-navy" style="width: 100%; font-size: 14px; padding: 10px 20px;">
            Update Security Password &rarr;
          </button>
        </form>
      </div>

    </div>
    """
    return render_desk_base("My Profile", user, content, active_tab='profile', breadcrumbs=[("Settings", None), ("My Profile", None)])
