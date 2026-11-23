"""
ERPNext Desk Home Workspace View with Role-Specific Permissions & Number Cards
"""
from templates.base import render_desk_base
from core.rbac import get_role_label, has_permission
from core.db import get_activity_logs, get_inquiries, get_quotations, get_clients

def render_desk_workspace(user: dict, stats: dict) -> str:
    role = user.get('role', 'client')
    role_label = get_role_label(role)

    total_invoiced = stats.get('total_invoiced_ugx', 0.0)
    total_collected = stats.get('total_collected_ugx', 0.0)
    total_outstanding = stats.get('total_outstanding_ugx', 0.0)
    active_projects = stats.get('active_projects', 0)
    
    can_read_invoices = has_permission(role, 'Sales Invoice', 'read')
    can_read_quotes = has_permission(role, 'Quotation', 'read')
    can_read_gl = has_permission(role, 'General Ledger', 'read')
    can_read_coa = has_permission(role, 'Chart of Accounts', 'read')
    can_read_sms = has_permission(role, 'SMS Gateway', 'read')
    can_read_customers = has_permission(role, 'Customer', 'read')
    can_read_inquiries = has_permission(role, 'Inquiry', 'read')

    # Header action buttons
    header_buttons_html = ""
    if can_read_invoices:
        header_buttons_html += '<a href="/desk/invoices" class="btn btn-navy" style="font-size: 13px;">💰 Billing Center</a>\n'
    if can_read_quotes:
        header_buttons_html += '<a href="/desk/quotations" class="btn btn-gold" style="font-size: 13px;">+ New Proposal</a>\n'

    # Number Cards Grid based on role access
    if can_read_invoices:
        cards_html = f"""
        <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 10px; padding: 20px; box-shadow: var(--card-shadow); border-top: 3px solid var(--z-gold);">
          <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px;">Total Invoiced (UGX)</div>
          <div style="font-size: 22px; font-weight: 900; color: #0F172A; margin-top: 6px;">UGX {total_invoiced:,.0f}</div>
          <div style="font-size: 11.5px; color: var(--z-gold-dark); font-weight: 700; margin-top: 4px;">Commercial Billings</div>
        </div>

        <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 10px; padding: 20px; box-shadow: var(--card-shadow); border-top: 3px solid #16A34A;">
          <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px;">Collections Settled</div>
          <div style="font-size: 22px; font-weight: 900; color: #16A34A; margin-top: 6px;">UGX {total_collected:,.0f}</div>
          <div style="font-size: 11.5px; color: #166534; font-weight: 700; margin-top: 4px;">Bank & MoMo Receipts</div>
        </div>

        <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 10px; padding: 20px; box-shadow: var(--card-shadow); border-top: 3px solid #DC2626;">
          <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px;">Outstanding Debt</div>
          <div style="font-size: 22px; font-weight: 900; color: #DC2626; margin-top: 6px;">UGX {total_outstanding:,.0f}</div>
          <div style="font-size: 11.5px; color: #991B1B; font-weight: 700; margin-top: 4px;">Accounts Receivable</div>
        </div>

        <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 10px; padding: 20px; box-shadow: var(--card-shadow); border-top: 3px solid var(--z-blue);">
          <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px;">Active Projects</div>
          <div style="font-size: 22px; font-weight: 900; color: var(--z-blue); margin-top: 6px;">{active_projects} Deliveries</div>
          <div style="font-size: 11.5px; color: #1E40AF; font-weight: 700; margin-top: 4px;">Work in Progress (WIP)</div>
        </div>
        """
    else:
        # Non-finance view (e.g., Sales, Client, etc.)
        quotes_count = len(get_quotations()) if can_read_quotes else 0
        inquiries_count = len(get_inquiries()) if can_read_inquiries else 0
        clients_count = len(get_clients()) if can_read_customers else 0
        cards_html = f"""
        <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 10px; padding: 20px; box-shadow: var(--card-shadow); border-top: 3px solid var(--z-gold);">
          <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px;">Active Proposals</div>
          <div style="font-size: 22px; font-weight: 900; color: #0F172A; margin-top: 6px;">{quotes_count} Scoped</div>
          <div style="font-size: 11.5px; color: var(--z-gold-dark); font-weight: 700; margin-top: 4px;">Tailored Architecture</div>
        </div>

        <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 10px; padding: 20px; box-shadow: var(--card-shadow); border-top: 3px solid #16A34A;">
          <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px;">Inquiries & Leads</div>
          <div style="font-size: 22px; font-weight: 900; color: #16A34A; margin-top: 6px;">{inquiries_count} Received</div>
          <div style="font-size: 11.5px; color: #166534; font-weight: 700; margin-top: 4px;">Discovery Pipeline</div>
        </div>

        <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 10px; padding: 20px; box-shadow: var(--card-shadow); border-top: 3px solid var(--z-blue);">
          <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px;">Enterprise Clients</div>
          <div style="font-size: 22px; font-weight: 900; color: var(--z-blue); margin-top: 6px;">{clients_count} Accounts</div>
          <div style="font-size: 11.5px; color: #1E40AF; font-weight: 700; margin-top: 4px;">Customer Accounts</div>
        </div>

        <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 10px; padding: 20px; box-shadow: var(--card-shadow); border-top: 3px solid #6366F1;">
          <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase; letter-spacing: 0.5px;">Delivery Projects</div>
          <div style="font-size: 22px; font-weight: 900; color: #6366F1; margin-top: 6px;">{active_projects} Deliveries</div>
          <div style="font-size: 11.5px; color: #4338CA; font-weight: 700; margin-top: 4px;">Work in Progress (WIP)</div>
        </div>
        """

    # Quick Shortcuts Toolbar based on role access
    shortcut_links = []
    if can_read_invoices:
        shortcut_links.append('<a href="/desk/invoices" class="btn btn-outline btn-sm">💰 New Sales Invoice</a>')
    if can_read_quotes:
        shortcut_links.append('<a href="/desk/quotations" class="btn btn-outline btn-sm">📄 Build Proposal</a>')
    if can_read_gl:
        shortcut_links.append('<a href="/desk/general-ledger" class="btn btn-outline btn-sm">📒 General Ledger</a>')
    if can_read_coa:
        shortcut_links.append('<a href="/desk/chart-of-accounts" class="btn btn-outline btn-sm">🌳 Chart of Accounts</a>')
    if can_read_sms:
        shortcut_links.append('<a href="/desk/sms" class="btn btn-outline btn-sm">📱 SMS Dispatch</a>')
    if has_permission(role, 'Delivery Project', 'read'):
        shortcut_links.append('<a href="/desk/projects" class="btn btn-outline btn-sm">🚀 Projects</a>')

    shortcuts_bar_html = ""
    if shortcut_links:
        shortcuts_bar_html = f"""
        <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 10px; padding: 18px 24px; box-shadow: var(--card-shadow); margin-bottom: 28px; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 12px;">
          <div style="display: flex; align-items: center; gap: 12px; font-size: 13px; font-weight: 700; color: #0F172A; flex-wrap: wrap;">
            <span>⚡ Quick ERP Actions:</span>
            {' '.join(shortcut_links)}
          </div>
          <div style="font-size: 12px; color: #64748B;">
            Press <kbd style="background: #F1F5F9; border: 1px solid #CBD5E1; padding: 2px 6px; border-radius: 4px; font-weight: 700;">Ctrl + K</kbd> to search DocTypes
          </div>
        </div>
        """

    logs = get_activity_logs(8)
    activity_html = ""
    for log in logs:
        activity_html += f"""
        <div style="display: flex; gap: 12px; padding: 10px 0; border-bottom: 1px solid var(--z-border); font-size: 13px;">
          <div style="font-size: 16px;">📌</div>
          <div style="flex: 1;">
            <div style="font-weight: 700; color: #0F172A;">{log.get('action')} &bull; <span style="font-weight: 400; color: #64748B; font-size: 11.5px;">{log.get('timestamp')}</span></div>
            <div style="color: #475569; font-size: 12.5px; margin-top: 2px;">{log.get('details')}</div>
          </div>
        </div>
        """
    if not activity_html:
        activity_html = "<div style='color: #94A3B8; font-size: 13px; padding: 20px 0;'>No recent audit actions logged. All operations will record here.</div>"

    content = f"""
    <div style="margin-bottom: 24px;">
      <div style="display: flex; justify-content: space-between; align-items: flex-end;">
        <div>
          <span style="color: var(--z-gold-dark); font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.8px;">ERPNext Enterprise Desk</span>
          <h1 style="font-size: 26px; font-weight: 900; color: #0F172A; margin-top: 4px;">Welcome back, {user.get('full_name')}</h1>
          <p style="color: #64748B; font-size: 13.5px;">Assigned Role: <strong>{role_label}</strong> &bull; Practice: {user.get('department', 'Zureka Solutions')}</p>
        </div>
        <div style="display: flex; gap: 10px;">
          {header_buttons_html}
        </div>
      </div>
    </div>

    <!-- ERP Number Cards Grid -->
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; margin-bottom: 28px;">
      {cards_html}
    </div>

    <!-- Quick Shortcuts Toolbar -->
    {shortcuts_bar_html}

    <!-- Workspaces & Audit Trail Grid -->
    <div style="display: grid; grid-template-columns: 1.3fr 1fr; gap: 24px;">
      
      <!-- Practices Card -->
      <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 10px; padding: 24px; box-shadow: var(--card-shadow);">
        <h3 style="font-size: 16px; font-weight: 800; color: #0F172A; margin-bottom: 16px;">Core Enterprise Practice Operations</h3>
        <div style="display: flex; flex-direction: column; gap: 14px;">
          
          <div style="padding: 16px; background: #F8FAFC; border-radius: 8px; border-left: 4px solid var(--z-gold);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
              <div style="font-weight: 800; font-size: 14px; color: #0F172A;">Practice 1: Enterprise Solutions (ERPNext, Odoo, SAP B1)</div>
              <span class="z-badge">Active</span>
            </div>
            <div style="color: #64748B; font-size: 12.5px; margin-top: 4px;">Practice Lead: Eng. Brian Mukasa &bull; Manufacturing, Supply Chain, POS, Chart of Accounts & EFRIS</div>
          </div>

          <div style="padding: 16px; background: #F8FAFC; border-radius: 8px; border-left: 4px solid var(--z-blue);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
              <div style="font-weight: 800; font-size: 14px; color: #0F172A;">Practice 2: Data, Intelligence & Innovation</div>
              <span class="z-badge">Active</span>
            </div>
            <div style="color: #64748B; font-size: 12.5px; margin-top: 4px;">Practice Lead: Fiona Atuhaire, MSc &bull; PostgreSQL 16 Data Warehousing, Metabase Analytics & AI</div>
          </div>

          <div style="padding: 16px; background: #F8FAFC; border-radius: 8px; border-left: 4px solid #16A34A);">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
              <div style="font-weight: 800; font-size: 14px; color: #0F172A;">Practice 3: Operational Excellence & Process Advisory</div>
              <span class="z-badge">Active</span>
            </div>
            <div style="color: #64748B; font-size: 12.5px; margin-top: 4px;">Practice Lead: Dennis Mugisha &bull; Business Process Re-engineering (BPR), SOPs & ISO 9001</div>
          </div>

        </div>
      </div>

      <!-- Activity Stream -->
      <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 10px; padding: 24px; box-shadow: var(--card-shadow); display: flex; flex-direction: column;">
        <h3 style="font-size: 16px; font-weight: 800; color: #0F172A; margin-bottom: 14px;">Recent Financial & Operations Audit</h3>
        <div style="flex: 1; overflow-y: auto; max-height: 380px;">
          {activity_html}
        </div>
      </div>

    </div>
    """
    return render_desk_base("Desk Workspace", user, content, active_tab='workspace', breadcrumbs=[("Workspaces", None)])
