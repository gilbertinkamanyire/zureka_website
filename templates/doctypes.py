"""
ERPNext DocType Views: Quotations, Delivery Projects, CRM Customers 360, Solutions Catalog
"""
from typing import List
from templates.base import render_desk_base

def render_desk_quotations(user: dict, quotations: List[dict], can_create: bool, can_submit: bool) -> str:
    rows = ""
    for q in quotations:
        status = q.get('status', 'Draft')
        pill_cls = 'indicator-approved' if status == 'Approved' else 'indicator-draft'
        
        actions_html = f"""
        <div style="display: flex; gap: 6px; justify-content: flex-end;">
          <a href="/desk/quotations/{q.get('quote_no')}" class="btn btn-navy btn-sm">View & Print</a>
        """
        if status == 'Draft' and can_submit:
            actions_html += f"""
            <form action="/api/quotations/{q.get('quote_no')}/approve" method="POST" style="display: inline;">
              <button type="submit" class="btn btn-gold btn-sm">Approve & SMS &rarr;</button>
            </form>
            """
        elif status == 'Approved' and user.get('role') in ['admin', 'lead_erp', 'sales']:
            actions_html += f"""
            <form action="/api/quotations/{q.get('quote_no')}/convert-invoice" method="POST" style="display: inline;">
              <button type="submit" class="btn btn-outline btn-sm" title="Generate 40% Milestone Sales Invoice">💰 Make Invoice</button>
            </form>
            <form action="/api/quotations/{q.get('quote_no')}/convert-project" method="POST" style="display: inline;">
              <button type="submit" class="btn btn-outline btn-sm" title="Start Delivery Project">🚀 Start Project</button>
            </form>
            """
        actions_html += "</div>"

        rows += f"""
        <tr>
          <td style="font-weight: 800; font-family: monospace; color: #0F172A;">
            <a href="/desk/quotations/{q.get('quote_no')}" style="color: var(--z-blue); text-decoration: underline;">
              {q.get('quote_no')}
            </a>
          </td>
          <td style="font-size: 12.5px; color: #475569;">{q.get('date')}</td>
          <td style="font-weight: 700; color: #1E293B;">
            {q.get('client_name')}<br>
            <span style="font-size: 11px; color: #64748B;">{q.get('client_phone', '')}</span>
          </td>
          <td style="font-weight: 600; color: var(--z-navy);">{q.get('system_name')}</td>
          <td style="font-size: 12.5px; color: #64748B;">{q.get('timeline_weeks', '8-12 Weeks')}</td>
          <td>
            <span class="indicator-pill {pill_cls}">
              <span class="indicator-dot"></span>
              {status}
            </span>
          </td>
          <td style="font-size: 11.5px; font-weight: 800; color: var(--z-gold-dark); text-transform: uppercase;">Tailored Scope</td>
          <td>{actions_html}</td>
        </tr>
        """

    create_modal = f"""
    <div id="newQuoteModal" class="modal-overlay">
      <div class="modal-card">
        <div class="modal-header">
          <div class="modal-title">New Architectural Quotation & Scope Proposal</div>
          <button class="modal-close" onclick="closeModal('newQuoteModal')">&times;</button>
        </div>
        <form action="/api/quotations" method="POST">
          <div class="modal-body">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Client Enterprise Name *</label>
                <input type="text" name="client_name" required placeholder="e.g. Uganda Grain Processors Ltd" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Client Official Email *</label>
                <input type="email" name="client_email" required placeholder="ops@grainprocessors.ug" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Client Phone (for Instant SMS Alert) *</label>
                <input type="text" name="client_phone" required placeholder="+256 772 000 000" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Platform Code</label>
                <select name="system_code" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
                  <option value="ERP-001">ERP-001 • ERPNext Manufacturing & Supply Chain</option>
                  <option value="ERP-002">ERP-002 • ERPNext Multi-Branch Retail & POS</option>
                  <option value="DAT-001">DAT-001 • PostgreSQL Data Warehouse & Metabase BI</option>
                  <option value="OPX-001">OPX-001 • Business Process Re-Engineering (BPR)</option>
                  <option value="FIN-001">FIN-001 • Microfinance & Lending Management Suite</option>
                </select>
              </div>
            </div>

            <div style="margin-bottom: 16px;">
              <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Delivery Timeline</label>
              <input type="text" name="timeline_weeks" value="8-12 Weeks" placeholder="e.g. 8-12 Weeks" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
            </div>

            <div style="margin-bottom: 16px;">
              <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Scope Summary & Transformation Architecture *</label>
              <textarea name="scope_summary" rows="3" required placeholder="Describe module rollouts (General Ledger, Stock Valuation, Payroll, EFRIS API, Multi-warehouse distribution)..." style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;"></textarea>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline" onclick="closeModal('newQuoteModal')">Cancel</button>
            <button type="submit" class="btn btn-gold">Generate Proposal & Send SMS Alert &rarr;</button>
          </div>
        </form>
      </div>
    </div>
    """

    content = f"""
    <div class="erp-header">
      <div>
        <h1 class="erp-title">Quotations & Proposals</h1>
        <div class="erp-subtitle">Tailored scope architectural proposals with Pandora SMS triggers and one-click billing conversion</div>
      </div>
      <div class="erp-actions">
        {'<button class="btn btn-gold" onclick="openModal(\'newQuoteModal\')">+ New Proposal</button>' if can_create else ''}
      </div>
    </div>

    <div class="table-wrap">
      <table class="z-table">
        <thead>
          <tr>
            <th>Proposal No</th>
            <th>Date</th>
            <th>Client Enterprise</th>
            <th>Platform</th>
            <th>Timeline</th>
            <th>DocStatus</th>
            <th>Pricing Model</th>
            <th style="text-align: right;">Actions</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </div>

    {create_modal}
    """
    return render_desk_base("Quotations", user, content, active_tab='quotations', breadcrumbs=[("Selling", "/desk/quotations"), ("Quotations", None)])

def render_quotation_detail(user: dict, quotation: dict) -> str:
    """Official Printable Executive Proposal View."""
    q_no = quotation.get('quote_no')
    status = quotation.get('status', 'Draft')
    pill_cls = 'indicator-approved' if status == 'Approved' else 'indicator-draft'

    content = f"""
    <div class="erp-header">
      <div>
        <h1 class="erp-title">{q_no}</h1>
        <div class="erp-subtitle">Document Status: <span class="indicator-pill {pill_cls}"><span class="indicator-dot"></span>{status}</span></div>
      </div>
      <div class="erp-actions">
        <button class="btn btn-outline" onclick="window.print()">🖨️ Print Formal Proposal</button>
        <a href="/desk/quotations" class="btn btn-navy">&larr; Back to Quotations</a>
      </div>
    </div>

    <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 12px; padding: 48px; box-shadow: var(--card-shadow);">
      
      <!-- Letterhead -->
      <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid var(--z-gold); padding-bottom: 24px; margin-bottom: 28px;">
        <div style="display: flex; align-items: center; gap: 14px;">
          <img src="/public/images/z_logo.svg" style="height: 48px; width: 48px;" alt="Logo">
          <div>
            <h2 style="font-size: 22px; font-weight: 900; color: #0F172A;">ZUREKA SOLUTIONS LIMITED</h2>
            <div style="font-size: 12.5px; color: #64748B;">Plot 14 Lumumba Avenue, Kampala, Uganda &bull; Tel: +256 773 245 712</div>
            <div style="font-size: 11.5px; color: var(--z-gold-dark); font-weight: 700;">Executive Strategy & Enterprise Systems Engineering</div>
          </div>
        </div>
        <div style="text-align: right;">
          <div style="font-size: 20px; font-weight: 900; color: #0F172A;">ENTERPRISE ARCHITECTURE PROPOSAL</div>
          <div style="font-family: monospace; font-size: 14px; font-weight: 800; color: var(--z-gold);">{q_no}</div>
          <div style="font-size: 12px; color: #64748B; margin-top: 4px;">Date: {quotation.get('date')}</div>
        </div>
      </div>

      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 32px; background: #F8FAFC; padding: 20px; border-radius: 8px; border: 1px solid var(--z-border);">
        <div>
          <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; color: #64748B;">Client Partner:</div>
          <div style="font-size: 16px; font-weight: 800; color: #0F172A; margin-top: 4px;">{quotation.get('client_name')}</div>
          <div style="font-size: 13px; color: #475569; margin-top: 2px;">Contact: {quotation.get('client_email', '')} &bull; {quotation.get('client_phone', '')}</div>
        </div>
        <div>
          <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; color: #64748B;">Target Platform:</div>
          <div style="font-size: 16px; font-weight: 800; color: var(--z-navy); margin-top: 4px;">{quotation.get('system_name')}</div>
          <div style="font-size: 13px; color: #475569; margin-top: 2px;">Estimated Implementation Horizon: <strong>{quotation.get('timeline_weeks', '8-12 Weeks')}</strong></div>
        </div>
      </div>

      <div style="margin-bottom: 32px;">
        <h3 style="font-size: 16px; font-weight: 800; color: #0F172A; margin-bottom: 10px;">Transformation Scope Statement</h3>
        <p style="font-size: 14px; line-height: 1.8; color: #334155; background: #FFFFFF; border-left: 4px solid var(--z-gold); padding: 12px 18px; border: 1px solid var(--z-border); border-left-width: 4px; border-radius: 6px;">
          {quotation.get('scope_summary')}
        </p>
      </div>

      <div style="margin-bottom: 32px;">
        <h3 style="font-size: 16px; font-weight: 800; color: #0F172A; margin-bottom: 12px;">Deployment Milestones & Governance Schedule</h3>
        <table class="z-table">
          <thead>
            <tr>
              <th style="width: 80px;">Phase</th>
              <th>Milestone Stage</th>
              <th>Deliverables</th>
              <th style="width: 140px; text-align: right;">Payment Split</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td style="font-weight: 700;">Phase 1</td>
              <td style="font-weight: 700; color: #0F172A;">Discovery & SOP Gap Analysis</td>
              <td style="color: #475569;">Business process blueprints, Chart of Accounts mapping & infrastructure provisioning</td>
              <td style="text-align: right; font-weight: 700; color: var(--z-gold-dark);">40% Mobilization</td>
            </tr>
            <tr>
              <td style="font-weight: 700;">Phase 2</td>
              <td style="font-weight: 700; color: #0F172A;">Configuration & Data Migration</td>
              <td style="color: #475569;">ERPNext DocType setup, opening balances, historical data migration & integration</td>
              <td style="text-align: right; font-weight: 700; color: var(--z-gold-dark);">40% UAT Sign-off</td>
            </tr>
            <tr>
              <td style="font-weight: 700;">Phase 3</td>
              <td style="font-weight: 700; color: #0F172A;">Go-Live & Staff Training</td>
              <td style="color: #475569;">Super-user certification, cutover execution, SLA support onboarding</td>
              <td style="text-align: right; font-weight: 700; color: var(--z-gold-dark);">20% Handover</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div style="border-top: 1px solid var(--z-border); padding-top: 24px; display: flex; justify-content: space-between; align-items: flex-end;">
        <div>
          <div style="font-size: 12px; color: #64748B;">Prepared by Practice Lead:</div>
          <div style="font-weight: 800; color: #0F172A; margin-top: 4px;">Eng. Brian Mukasa &bull; Enterprise Solutions Practice</div>
          <div style="font-size: 11.5px; color: #64748B;">Zureka Solutions Limited &bull; Kampala, Uganda</div>
        </div>
        <div style="text-align: right;">
          <div style="font-size: 12px; color: #64748B;">Pricing Model:</div>
          <div style="font-size: 15px; font-weight: 800; color: var(--z-gold-dark);">Tailored Scope & Engineering Architecture</div>
        </div>
      </div>

    </div>
    """
    return render_desk_base(f"Proposal {q_no}", user, content, active_tab='quotations', breadcrumbs=[("Selling", "/desk/quotations"), ("Quotations", "/desk/quotations"), (q_no, None)])

def render_desk_projects(user: dict, projects: List[dict], can_create: bool) -> str:
    rows = ""
    for p in projects:
        pct = p.get('completion_pct', 0)
        status = p.get('status', 'Planning & Discovery')
        
        update_btn = f"""
        <button class="btn btn-outline btn-sm" onclick="openProjectModal('{p.get('code')}', '{p.get('name')}', {pct}, '{status}', '{p.get('current_milestone', '')}')">
          ✏️ Update Stage
        </button>
        """ if can_create else ""

        rows += f"""
        <tr>
          <td style="font-weight: 800; font-family: monospace; color: #0F172A;">{p.get('code')}</td>
          <td style="font-weight: 700; color: #1E293B;">
            {p.get('name')}<br>
            <span style="font-size: 11.5px; color: #64748B;">Milestone: {p.get('current_milestone', 'In Progress')}</span>
          </td>
          <td style="font-size: 13px; color: #475569;">{p.get('client_name')}</td>
          <td style="font-size: 12.5px; color: var(--z-gold-dark); font-weight: 700;">{p.get('practice_lead')}</td>
          <td><span class="indicator-pill indicator-submitted"><span class="indicator-dot"></span>{status}</span></td>
          <td style="width: 160px;">
            <div style="background: #E2E8F0; border-radius: 10px; height: 8px; width: 100%; overflow: hidden;">
              <div style="background: var(--z-gold); height: 100%; width: {pct}%;"></div>
            </div>
            <div style="font-size: 11px; font-weight: 800; color: #475569; margin-top: 4px;">{pct}% Completed</div>
          </td>
          <td style="text-align: right;">{update_btn}</td>
        </tr>
        """

    update_modal = """
    <div id="projectModal" class="modal-overlay">
      <div class="modal-card">
        <div class="modal-header">
          <div class="modal-title">Update Project Stage & Milestone</div>
          <button class="modal-close" onclick="closeModal('projectModal')">&times;</button>
        </div>
        <form action="/api/projects/update" method="POST">
          <input type="hidden" id="modalProjectCode" name="project_code">
          <div class="modal-body">
            <div style="font-size: 14px; font-weight: 800; color: #0F172A; margin-bottom: 16px;" id="modalProjectName"></div>
            
            <div style="margin-bottom: 16px;">
              <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Stage Status *</label>
              <select id="modalProjectStatus" name="status" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
                <option value="Planning & Discovery">Phase 1: Planning & Discovery</option>
                <option value="Architecture & System Design">Phase 2: Architecture & System Design</option>
                <option value="Configuration & Development">Phase 3: Configuration & Testing</option>
                <option value="Data Migration & Integration">Phase 4: Data Migration & URA Integration</option>
                <option value="UAT & Staff Training">Phase 5: User Acceptance & Training</option>
                <option value="Go-Live & Support">Phase 6: Go-Live & SLA Onboarding</option>
                <option value="Completed">Completed & Handed Over</option>
              </select>
            </div>

            <div style="margin-bottom: 16px;">
              <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Progress (0 - 100%) *</label>
              <input type="number" id="modalProjectPct" name="completion_pct" min="0" max="100" required style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
            </div>

            <div style="margin-bottom: 16px;">
              <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Current Deliverable Milestone Note *</label>
              <input type="text" id="modalProjectMilestone" name="current_milestone" required placeholder="e.g. Chart of accounts signed off; migrating inventory master data..." style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline" onclick="closeModal('projectModal')">Cancel</button>
            <button type="submit" class="btn btn-gold">Save Progress & Update Milestone &rarr;</button>
          </div>
        </form>
      </div>
    </div>

    <script>
    function openProjectModal(code, name, pct, status, milestone) {
      document.getElementById('modalProjectCode').value = code;
      document.getElementById('modalProjectName').innerText = code + ' • ' + name;
      document.getElementById('modalProjectPct').value = pct;
      document.getElementById('modalProjectStatus').value = status;
      document.getElementById('modalProjectMilestone').value = milestone;
      openModal('projectModal');
    }
    </script>
    """

    content = f"""
    <div class="erp-header">
      <div>
        <h1 class="erp-title">Delivery Projects</h1>
        <div class="erp-subtitle">Real-time enterprise transformation project stages, milestones, and governance</div>
      </div>
    </div>

    <div class="table-wrap">
      <table class="z-table">
        <thead>
          <tr>
            <th>Code</th>
            <th>Project Name & Milestone</th>
            <th>Enterprise Client</th>
            <th>Practice Lead</th>
            <th>Stage</th>
            <th>Completion</th>
            <th style="text-align: right;">Action</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </div>

    {update_modal}
    """
    return render_desk_base("Delivery Projects", user, content, active_tab='projects', breadcrumbs=[("Projects", "/desk/projects"), ("Delivery Projects", None)])

def render_desk_clients(user: dict, clients: List[dict], can_create: bool) -> str:
    rows = ""
    for c in clients:
        systems = ", ".join(c.get('systems_deployed', []))
        rows += f"""
        <tr>
          <td style="font-weight: 800; font-family: monospace; color: #0F172A;">{c.get('code')}</td>
          <td style="font-weight: 700; color: #1E293B;">{c.get('name')}</td>
          <td style="font-size: 12.5px; color: #64748B;">{c.get('industry')}</td>
          <td style="font-size: 13px; color: #334155;">
            {c.get('contact_person')}<br>
            <span style="font-size: 11px; color: #64748B;">{c.get('email')}</span>
          </td>
          <td style="font-size: 12.5px; font-weight: 600; color: #0F172A;">{c.get('phone')}</td>
          <td style="font-size: 12px; color: var(--z-navy);">{systems}</td>
          <td style="text-align: right;">
            <a href="/desk/sms?to={c.get('phone')}" class="btn btn-outline btn-sm">📱 Direct SMS</a>
          </td>
        </tr>
        """

    create_modal = """
    <div id="newClientModal" class="modal-overlay">
      <div class="modal-card">
        <div class="modal-header">
          <div class="modal-title">Register Enterprise Customer (CRM 360)</div>
          <button class="modal-close" onclick="closeModal('newClientModal')">&times;</button>
        </div>
        <form action="/api/clients" method="POST">
          <div class="modal-body">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Organization Name *</label>
                <input type="text" name="name" required placeholder="e.g. Nile Breweries Logistics Ltd" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Industry Sector *</label>
                <input type="text" name="industry" required placeholder="e.g. Fast-Moving Consumer Goods" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Primary Contact Person *</label>
                <input type="text" name="contact_person" required placeholder="e.g. Robert Kigozi" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Contact Email *</label>
                <input type="email" name="email" required placeholder="robert@nilebreweries.ug" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
            </div>

            <div style="margin-bottom: 16px;">
              <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Phone Number (for SMS Alerts) *</label>
              <input type="text" name="phone" required placeholder="+256 772 123 456" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
            </div>

            <div style="margin-bottom: 16px;">
              <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Systems Deployed (comma-separated)</label>
              <input type="text" name="systems_deployed" placeholder="ERPNext Supply Chain, Metabase BI Analytics" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline" onclick="closeModal('newClientModal')">Cancel</button>
            <button type="submit" class="btn btn-gold">Create Customer Profile &rarr;</button>
          </div>
        </form>
      </div>
    </div>
    """

    content = f"""
    <div class="erp-header">
      <div>
        <h1 class="erp-title">CRM Customers 360</h1>
        <div class="erp-subtitle">Commercial partner directory, stakeholder contacts, and deployed enterprise systems</div>
      </div>
      <div class="erp-actions">
        {'<button class="btn btn-gold" onclick="openModal(\'newClientModal\')">+ Register Customer</button>' if can_create else ''}
      </div>
    </div>

    <div class="table-wrap">
      <table class="z-table">
        <thead>
          <tr>
            <th>Customer #</th>
            <th>Enterprise Organization</th>
            <th>Industry</th>
            <th>Primary Stakeholder</th>
            <th>Phone</th>
            <th>Deployed Systems</th>
            <th style="text-align: right;">Action</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </div>

    {create_modal}
    """
    return render_desk_base("CRM Customers 360", user, content, active_tab='clients', breadcrumbs=[("CRM", "/desk/clients"), ("Customers", None)])

def render_desk_systems(user: dict, systems: List[dict], can_create: bool) -> str:
    rows = ""
    for s in systems:
        rows += f"""
        <tr>
          <td style="font-weight: 800; font-family: monospace; color: #0F172A;">{s.get('code')}</td>
          <td style="font-weight: 700; color: #1E293B;">{s.get('name')}</td>
          <td><span class="z-badge">{s.get('pillar')}</span></td>
          <td style="font-size: 12.5px; color: #475569;">{s.get('tier')}</td>
          <td style="font-size: 12px; color: #166534; font-weight: 700;">{s.get('readiness')}</td>
          <td style="text-align: right;">
            <a href="/tailored-scope?system={s.get('code')}" class="btn btn-outline btn-sm">Scope Architecture</a>
          </td>
        </tr>
        """

    content = f"""
    <div class="erp-header">
      <div>
        <h1 class="erp-title">Solutions Registry (16 Systems)</h1>
        <div class="erp-subtitle">Master architectural platforms across Enterprise Solutions, Data Intelligence, and OPEX</div>
      </div>
    </div>

    <div class="table-wrap">
      <table class="z-table">
        <thead>
          <tr>
            <th>Code</th>
            <th>Platform Architecture</th>
            <th>Practice Pillar</th>
            <th>Deployment Tier</th>
            <th>Status</th>
            <th style="text-align: right;">Action</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </div>
    """
    return render_desk_base("Solutions Catalog", user, content, active_tab='systems', breadcrumbs=[("Settings", "/desk/systems"), ("Solutions Registry", None)])
