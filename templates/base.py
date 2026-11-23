"""
Base Layout, ERPNext Desk Shell, and CSS Design System
"""
import config
from core.rbac import get_role_label, get_role_badge

CSS_STYLES = """
:root {
  --z-navy: #0F172A;
  --z-navy-light: #1E293B;
  --z-navy-dark: #0B1120;
  --z-gold: #C59B27;
  --z-gold-light: #FBF4DC;
  --z-gold-dark: #9A7513;
  --z-blue: #2563EB;
  --z-blue-light: #EFF6FF;
  --z-green: #16A34A;
  --z-green-light: #DCFCE7;
  --z-slate: #64748B;
  --z-border: #E2E8F0;
  --z-border-subtle: #F1F5F9;
  --z-bg: #F8FAFC;
  --card-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06);
  --card-shadow-hover: 0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
  --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}
* { box-sizing: border-box; margin: 0; padding: 0; }
body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; color: #1E293B; background: #FFFFFF; line-height: 1.5; -webkit-font-smoothing: antialiased; }
a { text-decoration: none; color: inherit; }
.container { max-width: 1240px; margin: 0 auto; padding: 0 24px; }

/* Topbar & Navbar */
.z-topbar { background: #0B1120; color: #94A3B8; font-size: 12px; padding: 8px 0; border-bottom: 1px solid rgba(255,255,255,0.08); }
.z-topbar-inner { display: flex; justify-content: space-between; align-items: center; }
.z-nav { background: #0F172A; padding: 14px 0; border-bottom: 2px solid var(--z-gold); position: sticky; top: 0; z-index: 1000; box-shadow: 0 4px 20px rgba(0,0,0,0.25); }
.z-nav-inner { display: flex; justify-content: space-between; align-items: center; }
.z-brand { display: flex; align-items: center; gap: 12px; font-weight: 800; font-size: 20px; color: #FFFFFF; }
.z-brand img { height: 38px; width: 38px; }
.z-brand span { color: var(--z-gold); }
.z-nav-links { display: flex; align-items: center; gap: 24px; }
.z-nav-link { color: #CBD5E1; font-weight: 600; font-size: 14px; transition: var(--transition); }
.z-nav-link:hover, .z-nav-link.active { color: var(--z-gold); }
.z-nav-desk-btn { background: var(--z-gold); color: #0F172A !important; font-weight: 800; font-size: 13.5px; padding: 8px 18px; border-radius: 6px; transition: var(--transition); display: inline-flex; align-items: center; gap: 6px; }
.z-nav-desk-btn:hover { background: #d4a933; transform: translateY(-1px); }

/* ERPNext Desk Shell */
.desk-body { background: #F8FAFC; min-height: 100vh; display: flex; flex-direction: column; }
.desk-navbar { background: #0F172A; color: #FFFFFF; height: 56px; display: flex; align-items: center; justify-content: space-between; padding: 0 24px; border-bottom: 2px solid var(--z-gold); position: sticky; top: 0; z-index: 999; }
.desk-navbar-brand { display: flex; align-items: center; gap: 12px; font-weight: 800; font-size: 16px; color: #FFFFFF; }
.desk-navbar-brand img { height: 30px; width: 30px; }
.awesomebar-wrap { position: relative; width: 420px; }
.awesomebar { background: #1E293B; border: 1px solid #334155; border-radius: 8px; padding: 7px 16px 7px 36px; width: 100%; color: #F8FAFC; font-size: 13px; outline: none; transition: var(--transition); }
.awesomebar:focus { border-color: var(--z-gold); background: #0F172A; box-shadow: 0 0 0 3px rgba(197,155,39,0.25); }
.awesomebar-icon { position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #94A3B8; font-size: 14px; pointer-events: none; }
.awesomebar-kbd { position: absolute; right: 10px; top: 50%; transform: translateY(-50%); background: #334155; color: #CBD5E1; font-size: 10px; font-weight: 700; padding: 2px 6px; border-radius: 4px; pointer-events: none; }
.desk-user-chip { display: flex; align-items: center; gap: 12px; }
.desk-avatar { width: 34px; height: 34px; border-radius: 50%; background: var(--z-gold); color: #0F172A; font-weight: 800; display: flex; align-items: center; justify-content: center; font-size: 13.5px; border: 2px solid #FFFFFF; }

.desk-layout { display: flex; flex: 1; }
.desk-sidebar { width: 260px; background: #FFFFFF; border-right: 1px solid var(--z-border); padding: 20px 0; display: flex; flex-direction: column; flex-shrink: 0; }
.desk-sidebar-title { font-size: 11px; font-weight: 800; text-transform: uppercase; color: var(--z-slate); padding: 8px 24px; letter-spacing: 0.8px; display: flex; align-items: center; justify-content: space-between; }
.desk-sidebar-link { display: flex; align-items: center; justify-content: space-between; padding: 9px 24px; font-size: 13.5px; font-weight: 600; color: #475569; border-left: 3px solid transparent; transition: var(--transition); }
.desk-sidebar-link:hover { background: #F8FAFC; color: #0F172A; border-left-color: var(--z-border); }
.desk-sidebar-link.active { background: #F1F5F9; color: #0F172A; font-weight: 700; border-left-color: var(--z-gold); }
.desk-sidebar-count { background: #F1F5F9; color: #475569; font-size: 11px; font-weight: 700; padding: 2px 8px; border-radius: 12px; }
.desk-main { flex: 1; padding: 28px 36px; max-width: calc(100vw - 260px); }

/* ERP Page Header & Breadcrumbs */
.erp-breadcrumb { display: flex; align-items: center; gap: 8px; font-size: 12.5px; color: #64748B; margin-bottom: 8px; }
.erp-breadcrumb a:hover { color: var(--z-navy); text-decoration: underline; }
.erp-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 24px; }
.erp-title { font-size: 24px; font-weight: 800; color: #0F172A; }
.erp-subtitle { font-size: 13.5px; color: #64748B; margin-top: 2px; }
.erp-actions { display: flex; align-items: center; gap: 10px; }

/* ERP Cards, Tables & Badges */
.card-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 24px; }
.z-card { background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 12px; padding: 26px; display: flex; flex-direction: column; box-shadow: var(--card-shadow); transition: var(--transition); }
.z-card:hover { transform: translateY(-4px); box-shadow: var(--card-shadow-hover); border-color: #CBD5E1; }
.z-title { font-size: 17px; font-weight: 800; color: var(--z-navy); margin-bottom: 8px; }
.z-desc { font-size: 13.5px; color: var(--z-slate); line-height: 1.6; margin-bottom: 16px; flex-grow: 1; }
.z-badge { display: inline-block; font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.6px; padding: 3px 10px; border-radius: 14px; background: #F1F5F9; color: var(--z-navy); }

.table-wrap { background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 10px; overflow: hidden; box-shadow: var(--card-shadow); }
.z-table { width: 100%; border-collapse: collapse; text-align: left; font-size: 13.5px; }
.z-table th { background: #F8FAFC; padding: 12px 18px; font-weight: 700; color: #475569; border-bottom: 1px solid var(--z-border); text-transform: uppercase; font-size: 11px; letter-spacing: 0.6px; }
.z-table td { padding: 13px 18px; border-bottom: 1px solid var(--z-border); color: #1E293B; vertical-align: middle; }
.z-table tr:last-child td { border-bottom: none; }
.z-table tr:hover td { background: #F8FAFC; }

/* Buttons & Badges */
.btn { display: inline-flex; align-items: center; justify-content: center; gap: 7px; font-weight: 700; font-size: 13.5px; padding: 8px 16px; border-radius: 6px; border: 1px solid transparent; cursor: pointer; transition: var(--transition); outline: none; }
.btn-gold { background: var(--z-gold); color: #0F172A; }
.btn-gold:hover { background: #d4a933; transform: translateY(-1px); }
.btn-navy { background: #0F172A; color: #FFFFFF; }
.btn-navy:hover { background: #1E293B; }
.btn-outline { background: #FFFFFF; border-color: var(--z-border); color: #334155; }
.btn-outline:hover { background: #F8FAFC; border-color: #CBD5E1; color: #0F172A; }
.btn-sm { font-size: 12px; padding: 5px 12px; }

/* Status Indicators (ERPNext Standard) */
.indicator-pill { display: inline-flex; align-items: center; gap: 6px; padding: 3px 10px; border-radius: 20px; font-size: 11.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px; }
.indicator-dot { width: 7px; height: 7px; border-radius: 50%; }
.indicator-paid, .indicator-approved, .indicator-completed { background: #DCFCE7; color: #166534; }
.indicator-paid .indicator-dot, .indicator-approved .indicator-dot, .indicator-completed .indicator-dot { background: #16A34A; }
.indicator-draft { background: #F1F5F9; color: #475569; }
.indicator-draft .indicator-dot { background: #94A3B8; }
.indicator-unpaid, .indicator-submitted { background: #DBEAFE; color: #1E40AF; }
.indicator-unpaid .indicator-dot, .indicator-submitted .indicator-dot { background: #2563EB; }
.indicator-overdue, .indicator-cancelled { background: #FEE2E2; color: #991B1B; }
.indicator-overdue .indicator-dot, .indicator-cancelled .indicator-dot { background: #DC2626; }

/* Modal Backdrop */
.modal-overlay { display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(15, 23, 42, 0.6); backdrop-filter: blur(4px); z-index: 2000; align-items: center; justify-content: center; }
.modal-overlay.open { display: flex; }
.modal-card { background: #FFFFFF; border-radius: 12px; width: 100%; max-width: 640px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); overflow: hidden; animation: modalPop 0.2s cubic-bezier(0.16, 1, 0.3, 1); }
@keyframes modalPop { from { transform: scale(0.95); opacity: 0; } to { transform: scale(1); opacity: 1; } }
.modal-header { padding: 18px 24px; border-bottom: 1px solid var(--z-border); display: flex; justify-content: space-between; align-items: center; background: #F8FAFC; }
.modal-title { font-size: 16px; font-weight: 800; color: #0F172A; }
.modal-close { background: none; border: none; font-size: 20px; cursor: pointer; color: #64748B; padding: 4px; line-height: 1; }
.modal-close:hover { color: #0F172A; }
.modal-body { padding: 24px; max-height: 80vh; overflow-y: auto; }
.modal-footer { padding: 16px 24px; border-top: 1px solid var(--z-border); display: flex; justify-content: flex-end; gap: 12px; background: #F8FAFC; }
"""

AWESOMEBAR_SCRIPT = """
<script>
document.addEventListener('DOMContentLoaded', function() {
  const bar = document.getElementById('awesomebar');
  if (!bar) return;
  
  // Shortcut Ctrl+K
  document.addEventListener('keydown', function(e) {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      bar.focus();
      bar.select();
    }
  });

  bar.addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
      const q = bar.value.trim().toLowerCase();
      if (q.includes('inv') || q.includes('bill')) window.location.href = '/desk/invoices';
      else if (q.includes('gl') || q.includes('ledger')) window.location.href = '/desk/general-ledger';
      else if (q.includes('chart') || q.includes('coa') || q.includes('account')) window.location.href = '/desk/chart-of-accounts';
      else if (q.includes('pay') || q.includes('receipt')) window.location.href = '/desk/payments';
      else if (q.includes('quote') || q.includes('prop')) window.location.href = '/desk/quotations';
      else if (q.includes('proj')) window.location.href = '/desk/projects';
      else if (q.includes('client') || q.includes('cust')) window.location.href = '/desk/clients';
      else if (q.includes('sms')) window.location.href = '/desk/sms';
      else if (q.includes('perm') || q.includes('rbac')) window.location.href = '/desk/permissions';
      else if (q.includes('user')) window.location.href = '/desk/users';
      else if (q.includes('sys') || q.includes('sol')) window.location.href = '/desk/systems';
      else window.location.href = '/desk';
    }
  });
});

function openModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.add('open');
}
function closeModal(id) {
  const el = document.getElementById(id);
  if (el) el.classList.remove('open');
}
</script>
"""

def render_public_base(title: str, content: str, active_tab: str = 'home') -> str:
    """Render public-facing website shell with Zero-Pricing commitment."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} • {config.COMPANY_NAME}</title>
  <link rel="icon" href="/public/images/z_logo.svg" type="image/svg+xml">
  <style>{CSS_STYLES}</style>
</head>
<body>
  <div class="z-topbar">
    <div class="container z-topbar-inner">
      <div>📍 {config.LOCATION} &nbsp;|&nbsp; 📞 {config.PHONE} &nbsp;|&nbsp; ✉️ {config.EMAIL}</div>
      <div>100% Offline Python Architecture &nbsp;•&nbsp; Pandora Networks SMS Gateway</div>
    </div>
  </div>

  <nav class="z-nav">
    <div class="container z-nav-inner">
      <a href="/" class="z-brand">
        <img src="/public/images/z_logo.svg" alt="Zureka Logo">
        <div>ZUREKA <span>SOLUTIONS</span></div>
      </a>
      <div class="z-nav-links">
        <a href="/" class="z-nav-link {'active' if active_tab == 'home' else ''}">Overview</a>
        <a href="/systems" class="z-nav-link {'active' if active_tab == 'systems' else ''}">Enterprise Systems (16)</a>
        <a href="/tailored-scope" class="z-nav-link {'active' if active_tab == 'scope' else ''}">Tailored Scope</a>
        <a href="/login" class="z-nav-desk-btn">
          <span>Desk Portal</span> &rarr;
        </a>
      </div>
    </div>
  </nav>

  {content}

  <footer style="background: #0B1120; color: #94A3B8; padding: 60px 0 30px; border-top: 3px solid var(--z-gold); margin-top: 80px;">
    <div class="container">
      <div style="display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 40px; margin-bottom: 40px;">
        <div>
          <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 16px;">
            <img src="/public/images/z_logo.svg" style="height: 32px; width: 32px;" alt="Logo">
            <h3 style="color: #FFFFFF; font-size: 18px;">{config.COMPANY_NAME}</h3>
          </div>
          <p style="font-size: 13.5px; line-height: 1.7; max-width: 440px;">
            {config.TAGLINE} Delivering enterprise ERPNext platforms, business intelligence, operational excellence, and mission-critical systems across East Africa.
          </p>
        </div>
        <div>
          <h4 style="color: #FFFFFF; font-size: 14px; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 16px;">Practices</h4>
          <p style="font-size: 13px; line-height: 2;">Enterprise Solutions (ERPNext)<br>Data, Intelligence & AI<br>Operational Excellence & BPR</p>
        </div>
        <div>
          <h4 style="color: #FFFFFF; font-size: 14px; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 16px;">Direct Contact</h4>
          <p style="font-size: 13px; line-height: 2;">{config.LOCATION}<br>{config.PHONE}<br>{config.EMAIL}</p>
        </div>
      </div>
      <div style="border-top: 1px solid rgba(255,255,255,0.08); padding-top: 24px; text-align: center; font-size: 12.5px;">
        &copy; {config.COMPANY_NAME}. Zero Public Sticker Pricing — All Enterprise Deployments Are Scope-Engineered.
      </div>
    </div>
  </footer>
</body>
</html>"""

def render_desk_base(title: str, user: dict, content: str, active_tab: str = 'workspace', breadcrumbs: list = None) -> str:
    """Render ERPNext Desk shell for authenticated portal users with complete ERP navigation."""
    role = user.get('role', 'client')
    role_label = get_role_label(role)
    role_badge = get_role_badge(role)

    # Breadcrumb HTML
    crumbs_html = "<div class='erp-breadcrumb'><a href='/desk'>Desk</a>"
    if breadcrumbs:
        for b_name, b_url in breadcrumbs:
            if b_url:
                crumbs_html += f" <span>/</span> <a href='{b_url}'>{b_name}</a>"
            else:
                crumbs_html += f" <span>/</span> <span>{b_name}</span>"
    crumbs_html += "</div>"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} • Zureka ERPNext Desk</title>
  <link rel="icon" href="/public/images/z_logo.svg" type="image/svg+xml">
  <style>{CSS_STYLES}</style>
  {AWESOMEBAR_SCRIPT}
</head>
<body class="desk-body">
  <header class="desk-navbar">
    <div style="display: flex; align-items: center; gap: 30px;">
      <a href="/desk" class="desk-navbar-brand">
        <img src="/public/images/z_logo.svg" alt="Logo">
        <div>ZUREKA <span>DESK</span></div>
      </a>
      <div class="awesomebar-wrap">
        <span class="awesomebar-icon">🔍</span>
        <input type="text" class="awesomebar" placeholder="Search DocTypes, records (e.g. 'invoice', 'gl', 'quote')..." id="awesomebar">
        <span class="awesomebar-kbd">Ctrl + K</span>
      </div>
    </div>

    <div class="desk-user-chip">
      <span class="z-badge" style="background: var(--z-gold-light); color: var(--z-gold-dark); font-weight: 800;">{role_badge}</span>
      <a href="/desk/profile" style="text-align: right; font-size: 12px; display: flex; flex-direction: column; cursor: pointer;" title="Open Profile Settings">
        <span style="font-weight: 700; color: #FFFFFF;">{user.get('full_name')}</span>
        <span style="color: #94A3B8; font-size: 11px;">{role_label}</span>
      </a>
      <a href="/desk/profile" class="desk-avatar" title="My Profile Settings">{user.get('avatar', 'U')}</a>
      <a href="/logout" style="color: #F87171; font-weight: 700; font-size: 12px; margin-left: 10px; background: rgba(239,68,68,0.12); padding: 5px 12px; border-radius: 6px;">Sign Out</a>
    </div>
  </header>

  <div class="desk-layout">
    <aside class="desk-sidebar">
      <div class="desk-sidebar-title">
        <span>Workspaces</span>
      </div>
      <a href="/desk" class="desk-sidebar-link {'active' if active_tab == 'workspace' else ''}">
        <span>📊 Desk Workspace</span>
      </a>
      <a href="/desk/quotations" class="desk-sidebar-link {'active' if active_tab == 'quotations' else ''}">
        <span>📄 Quotations & Proposals</span>
      </a>
      <a href="/desk/projects" class="desk-sidebar-link {'active' if active_tab == 'projects' else ''}">
        <span>🚀 Delivery Projects</span>
      </a>
      <a href="/desk/clients" class="desk-sidebar-link {'active' if active_tab == 'clients' else ''}">
        <span>🏢 CRM Customers 360</span>
      </a>
      <a href="/desk/systems" class="desk-sidebar-link {'active' if active_tab == 'systems' else ''}">
        <span>⚙️ Solutions Catalog (16)</span>
      </a>

      <div class="desk-sidebar-title" style="margin-top: 20px;">
        <span>Accounting & Finance</span>
      </div>
      <a href="/desk/invoices" class="desk-sidebar-link {'active' if active_tab == 'invoices' else ''}">
        <span>💰 Sales Invoices</span>
      </a>
      <a href="/desk/payments" class="desk-sidebar-link {'active' if active_tab == 'payments' else ''}">
        <span>💳 Payment Receipts</span>
      </a>
      <a href="/desk/general-ledger" class="desk-sidebar-link {'active' if active_tab == 'gl' else ''}">
        <span>📒 General Ledger</span>
      </a>
      <a href="/desk/chart-of-accounts" class="desk-sidebar-link {'active' if active_tab == 'coa' else ''}">
        <span>🌳 Chart of Accounts</span>
      </a>

      <div class="desk-sidebar-title" style="margin-top: 20px;">
        <span>Administration & Comms</span>
      </div>
      <a href="/desk/profile" class="desk-sidebar-link {'active' if active_tab == 'profile' else ''}">
        <span>👤 My Profile Settings</span>
      </a>
      <a href="/desk/sms" class="desk-sidebar-link {'active' if active_tab == 'sms' else ''}">
        <span>📱 Pandora SMS Gateway</span>
      </a>
      <a href="/desk/permissions" class="desk-sidebar-link {'active' if active_tab == 'permissions' else ''}">
        <span>🔒 RBAC Matrix</span>
      </a>
      <a href="/desk/users" class="desk-sidebar-link {'active' if active_tab == 'users' else ''}">
        <span>👥 User Directory</span>
      </a>

      <div style="margin-top: auto; padding: 14px 18px; background: #F8FAFC; border-radius: 8px; margin: 24px 14px 14px; border: 1px solid var(--z-border);">
        <div style="display: flex; align-items: center; justify-content: space-between;">
          <span style="font-weight: 800; color: #0F172A; font-size: 11.5px;">SMS Gateway</span>
          <span style="color: #16A34A; font-weight: 800; font-size: 11px;">● Active</span>
        </div>
        <div style="color: var(--z-slate); font-size: 11px; margin-top: 3px;">Pandora Networks (Uganda)</div>
      </div>
    </aside>

    <main class="desk-main">
      {crumbs_html}
      {content}
    </main>
  </div>
</body>
</html>"""

def render_permission_denied(user: dict, doctype: str, action: str) -> str:
    """Render 403 Forbidden screen when RBAC check fails."""
    content = f"""
    <div style="max-width: 580px; margin: 60px auto; background: #FFFFFF; border: 1px solid #FECACA; border-radius: 12px; padding: 40px; text-align: center; box-shadow: var(--card-shadow);">
      <div style="font-size: 48px; margin-bottom: 16px;">🚫</div>
      <h2 style="color: #991B1B; font-size: 22px; font-weight: 800; margin-bottom: 12px;">403 • Permission Denied</h2>
      <p style="color: #475569; font-size: 14px; line-height: 1.6; margin-bottom: 24px;">
        Your assigned role <strong>{get_role_label(user.get('role', 'unknown'))}</strong> does not possess the
        <strong>[{action.upper()}]</strong> permission on DocType <strong>[{doctype}]</strong> in the Role Permissions Manager.
      </p>
      <div style="background: #FEF2F2; padding: 12px; border-radius: 6px; font-size: 12px; color: #991B1B; margin-bottom: 24px;">
        To request access elevation, contact the Managing Partner or System Administrator.
      </div>
      <a href="/desk" class="btn btn-navy">&larr; Return to Workspace</a>
    </div>
    """
    return render_desk_base("403 Forbidden", user, content, active_tab='workspace')
