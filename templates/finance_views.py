"""
ERPNext Accounting & Finance Module: Invoices, General Ledger, Chart of Accounts, Payments
"""
from typing import List
from templates.base import render_desk_base

def render_invoice_list(user: dict, invoices: List[dict], can_create: bool) -> str:
    rows = ""
    for inv in invoices:
        status = inv.get('status', 'Unpaid')
        pill_cls = 'indicator-paid' if status == 'Paid' else ('indicator-unpaid' if status == 'Unpaid' else 'indicator-draft')
        
        grand_total = inv.get('grand_total', 0.0)
        outstanding = inv.get('outstanding_amount', grand_total)
        
        pay_btn = ""
        if outstanding > 0 and user.get('role') in ['admin', 'finance']:
            pay_btn = f"""
            <button class="btn btn-outline btn-sm" onclick="openPaymentModal('{inv.get('invoice_no')}', '{inv.get('client_name')}', {outstanding})">
              💳 Pay Entry
            </button>
            """

        rows += f"""
        <tr>
          <td style="font-weight: 800; font-family: monospace; color: #0F172A;">
            <a href="/desk/invoices/{inv.get('invoice_no')}" style="color: var(--z-blue); text-decoration: underline;">
              {inv.get('invoice_no')}
            </a>
          </td>
          <td style="font-size: 12.5px; color: #475569;">{inv.get('date')}</td>
          <td style="font-weight: 700; color: #1E293B;">
            {inv.get('client_name')}<br>
            <span style="font-size: 11px; color: #64748B;">{inv.get('client_email', '')}</span>
          </td>
          <td style="font-weight: 700; color: #0F172A; text-align: right;">UGX {grand_total:,.0f}</td>
          <td style="font-weight: 800; color: {'#16A34A' if outstanding == 0 else '#DC2626'}; text-align: right;">
            UGX {outstanding:,.0f}
          </td>
          <td>
            <span class="indicator-pill {pill_cls}">
              <span class="indicator-dot"></span>
              {status}
            </span>
          </td>
          <td style="text-align: right; white-space: nowrap;">
            <a href="/desk/invoices/{inv.get('invoice_no')}" class="btn btn-navy btn-sm">View & Print</a>
            {pay_btn}
          </td>
        </tr>
        """

    create_modal = f"""
    <div id="newInvoiceModal" class="modal-overlay">
      <div class="modal-card">
        <div class="modal-header">
          <div class="modal-title">Create Sales Invoice (ERP Standard)</div>
          <button class="modal-close" onclick="closeModal('newInvoiceModal')">&times;</button>
        </div>
        <form action="/api/invoices" method="POST">
          <div class="modal-body">
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Client / Customer *</label>
                <input type="text" name="client_name" required placeholder="e.g. Victoria Manufacturing Ltd" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Client Official Email *</label>
                <input type="email" name="client_email" required placeholder="accounts@victoriamfg.ug" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Quotation Reference</label>
                <input type="text" name="quotation_ref" placeholder="e.g. ZUR-QT-2026-0001" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Due Date</label>
                <input type="date" name="due_date" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
            </div>

            <div style="margin-bottom: 16px;">
              <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Description / Milestone Deliverable *</label>
              <input type="text" name="description" required placeholder="e.g. Phase 1 ERPNext Mobilization & Database Schema Configuration" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
            </div>

            <div style="display: grid; grid-template-columns: 1.5fr 1fr; gap: 16px; margin-bottom: 16px;">
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Net Amount (UGX, before VAT) *</label>
                <input type="number" id="subtotalInput" name="subtotal" required value="25000000" step="500000" oninput="updateTaxPreview()" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Uganda VAT (18%)</label>
                <input type="text" id="vatPreview" readonly value="UGX 4,500,000" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px; background: #F8FAFC; color: #64748B;">
              </div>
            </div>

            <div style="background: #F8FAFC; border: 1px solid var(--z-border); border-radius: 8px; padding: 12px 16px; display: flex; justify-content: space-between; align-items: center;">
              <span style="font-size: 13px; font-weight: 700; color: #334155;">Grand Total (UGX):</span>
              <span id="grandTotalPreview" style="font-size: 16px; font-weight: 800; color: #0F172A;">UGX 29,500,000</span>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline" onclick="closeModal('newInvoiceModal')">Cancel</button>
            <button type="submit" class="btn btn-gold">Submit & Post to General Ledger &rarr;</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Payment Modal -->
    <div id="paymentModal" class="modal-overlay">
      <div class="modal-card">
        <div class="modal-header">
          <div class="modal-title">Record Payment Entry (Bank Receipt)</div>
          <button class="modal-close" onclick="closeModal('paymentModal')">&times;</button>
        </div>
        <form action="/api/payments" method="POST">
          <input type="hidden" id="payInvoiceNo" name="invoice_no">
          <div class="modal-body">
            <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 12px 16px; margin-bottom: 16px;">
              <div style="font-size: 12px; color: #1E40AF; font-weight: 600;">Payment Against Invoice:</div>
              <div id="payInvoiceDisplay" style="font-size: 15px; font-weight: 800; color: #1E3A8A; margin-top: 2px;"></div>
            </div>

            <div style="margin-bottom: 16px;">
              <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Receipt Amount (UGX) *</label>
              <input type="number" id="payAmountInput" name="amount" required style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 14px; font-weight: 700;">
            </div>

            <div style="margin-bottom: 16px;">
              <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Mode of Payment *</label>
              <select name="mode_of_payment" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
                <option value="Bank Transfer (Stanbic Bank Uganda)">Bank Transfer (Stanbic Bank Uganda - A/C 903001882910)</option>
                <option value="MTN Mobile Money Corporate Merchant">MTN Mobile Money Corporate Merchant (0773245712)</option>
                <option value="Airtel Money Corporate">Airtel Money Corporate Paybill</option>
                <option value="Electronic Funds Transfer (EFT / RTGS)">Electronic Funds Transfer (EFT / RTGS)</option>
              </select>
            </div>

            <div style="margin-bottom: 16px;">
              <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Transaction Reference / Cheque No *</label>
              <input type="text" name="reference_no" required placeholder="e.g. STANBIC-FT-2026-9921 or MTN-MM-0012" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline" onclick="closeModal('paymentModal')">Cancel</button>
            <button type="submit" class="btn btn-gold">Confirm Receipt & Post Bank GL &rarr;</button>
          </div>
        </form>
      </div>
    </div>

    <script>
    function updateTaxPreview() {{
      const sub = parseFloat(document.getElementById('subtotalInput').value) || 0;
      const vat = sub * 0.18;
      const total = sub + vat;
      document.getElementById('vatPreview').value = 'UGX ' + vat.toLocaleString();
      document.getElementById('grandTotalPreview').innerText = 'UGX ' + total.toLocaleString();
    }}
    function openPaymentModal(invNo, clientName, maxAmount) {{
      document.getElementById('payInvoiceNo').value = invNo;
      document.getElementById('payInvoiceDisplay').innerText = invNo + ' • ' + clientName;
      document.getElementById('payAmountInput').value = maxAmount;
      openModal('paymentModal');
    }}
    </script>
    """

    content = f"""
    <div class="erp-header">
      <div>
        <h1 class="erp-title">Sales Invoices</h1>
        <div class="erp-subtitle">Commercial billing, URA EFRIS compliance, and milestone disbursements</div>
      </div>
      <div class="erp-actions">
        <a href="/desk/general-ledger" class="btn btn-outline">📒 General Ledger</a>
        <a href="/desk/chart-of-accounts" class="btn btn-outline">🌳 Chart of Accounts</a>
        {'<button class="btn btn-gold" onclick="openModal(\'newInvoiceModal\')">+ New Sales Invoice</button>' if can_create else ''}
      </div>
    </div>

    <div class="table-wrap">
      <table class="z-table">
        <thead>
          <tr>
            <th>Invoice No</th>
            <th>Issue Date</th>
            <th>Customer Enterprise</th>
            <th style="text-align: right;">Grand Total</th>
            <th style="text-align: right;">Outstanding</th>
            <th>DocStatus</th>
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
    return render_desk_base("Sales Invoices", user, content, active_tab='invoices', breadcrumbs=[("Accounts", "/desk/invoices"), ("Sales Invoices", None)])

def render_invoice_detail(user: dict, invoice: dict, gl_entries: List[dict]) -> str:
    """Official ERPNext-Style Printable Tax Invoice View."""
    inv_no = invoice.get('invoice_no')
    status = invoice.get('status', 'Unpaid')
    pill_cls = 'indicator-paid' if status == 'Paid' else ('indicator-unpaid' if status == 'Unpaid' else 'indicator-draft')

    items = invoice.get('items', [])
    items_rows = ""
    for idx, it in enumerate(items, 1):
        rate = it.get('rate', 0.0)
        amt = it.get('amount', 0.0)
        items_rows += f"""
        <tr>
          <td style="color: #64748B;">{idx}</td>
          <td style="font-weight: 700; color: #0F172A;">{it.get('item_code', 'SRV')}<br><span style="font-weight: 400; font-size: 12.5px; color: #475569;">{it.get('description', '')}</span></td>
          <td style="text-align: center;">{it.get('qty', 1)}</td>
          <td style="text-align: right;">UGX {rate:,.0f}</td>
          <td style="text-align: right; font-weight: 700;">UGX {amt:,.0f}</td>
        </tr>
        """

    subtotal = invoice.get('subtotal', 0.0)
    vat = invoice.get('vat_amount', subtotal * 0.18)
    grand = invoice.get('grand_total', subtotal + vat)
    paid = invoice.get('paid_amount', 0.0)
    outstanding = invoice.get('outstanding_amount', grand - paid)

    # General ledger audit table for this invoice
    gl_rows = ""
    for g in gl_entries:
        gl_rows += f"""
        <tr>
          <td style="font-size: 12px; color: #64748B;">{g.get('posting_date')}</td>
          <td style="font-weight: 700; color: #0F172A;">{g.get('account')}</td>
          <td style="text-align: right; font-weight: 700; color: {'#16A34A' if g.get('debit', 0) > 0 else '#94A3B8'};">
            {f"UGX {g.get('debit'):,.0f}" if g.get('debit', 0) > 0 else "—"}
          </td>
          <td style="text-align: right; font-weight: 700; color: {'#DC2626' if g.get('credit', 0) > 0 else '#94A3B8'};">
            {f"UGX {g.get('credit'):,.0f}" if g.get('credit', 0) > 0 else "—"}
          </td>
          <td style="font-size: 12px; color: #475569;">{g.get('against_account')}</td>
        </tr>
        """
    if not gl_rows:
        gl_rows = "<tr><td colspan='5' style='text-align: center; color: #94A3B8; padding: 20px;'>No General Ledger transactions posted yet.</td></tr>"

    content = f"""
    <div class="erp-header">
      <div>
        <h1 class="erp-title">{inv_no}</h1>
        <div class="erp-subtitle">Document Status: <span class="indicator-pill {pill_cls}"><span class="indicator-dot"></span>{status}</span></div>
      </div>
      <div class="erp-actions">
        <button class="btn btn-outline" onclick="window.print()">🖨️ Print Tax Invoice</button>
        <a href="/desk/invoices" class="btn btn-navy">&larr; Back to Invoices</a>
      </div>
    </div>

    <!-- Printable Tax Invoice Sheet -->
    <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 12px; padding: 48px; box-shadow: var(--card-shadow); margin-bottom: 32px;">
      
      <!-- Letterhead -->
      <div style="display: flex; justify-content: space-between; align-items: flex-start; border-bottom: 2px solid var(--z-gold); padding-bottom: 24px; margin-bottom: 28px;">
        <div style="display: flex; align-items: center; gap: 14px;">
          <img src="/public/images/z_logo.svg" style="height: 48px; width: 48px;" alt="Zureka Logo">
          <div>
            <h2 style="font-size: 22px; font-weight: 900; color: #0F172A; letter-spacing: -0.5px;">ZUREKA SOLUTIONS LIMITED</h2>
            <div style="font-size: 12.5px; color: #64748B;">Plot 14 Lumumba Avenue, Kampala, Uganda &bull; Tel: +256 773 245 712</div>
            <div style="font-size: 11.5px; color: var(--z-gold-dark); font-weight: 700;">TIN: 1018992019 &bull; Uganda VAT Registered Enterprise</div>
          </div>
        </div>
        <div style="text-align: right;">
          <div style="font-size: 20px; font-weight: 900; color: #0F172A;">OFFICIAL TAX INVOICE</div>
          <div style="font-family: monospace; font-size: 14px; font-weight: 800; color: var(--z-gold);">{inv_no}</div>
          <div style="font-size: 11.5px; color: #166534; font-weight: 700; margin-top: 4px;">✓ EFRIS Validated: {invoice.get('efris_fdn', 'ZUR-FDN-2026')}</div>
        </div>
      </div>

      <!-- Invoice Details Grid -->
      <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin-bottom: 32px;">
        <div>
          <div style="font-size: 11px; font-weight: 800; text-transform: uppercase; color: #64748B; letter-spacing: 0.8px; margin-bottom: 6px;">Billed To:</div>
          <div style="font-size: 16px; font-weight: 800; color: #0F172A;">{invoice.get('client_name')}</div>
          <div style="font-size: 13px; color: #475569; margin-top: 2px;">{invoice.get('client_email', '')}</div>
          <div style="font-size: 12px; color: #64748B; margin-top: 2px;">Customer TIN: {invoice.get('client_tin', '1000293847')}</div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; background: #F8FAFC; padding: 18px; border-radius: 8px; border: 1px solid var(--z-border);">
          <div>
            <div style="font-size: 11px; font-weight: 700; color: #64748B;">Posting Date</div>
            <div style="font-size: 13.5px; font-weight: 700; color: #0F172A;">{invoice.get('date')}</div>
          </div>
          <div>
            <div style="font-size: 11px; font-weight: 700; color: #64748B;">Payment Terms</div>
            <div style="font-size: 13px; font-weight: 600; color: #0F172A;">{invoice.get('payment_terms', 'Net 30 Days')}</div>
          </div>
          <div>
            <div style="font-size: 11px; font-weight: 700; color: #64748B;">Quotation Ref</div>
            <div style="font-size: 13px; font-weight: 700; color: var(--z-blue);">{invoice.get('quotation_ref', 'N/A')}</div>
          </div>
          <div>
            <div style="font-size: 11px; font-weight: 700; color: #64748B;">Currency</div>
            <div style="font-size: 13.5px; font-weight: 800; color: #0F172A;">UGX (Uganda Shillings)</div>
          </div>
        </div>
      </div>

      <!-- Items Table -->
      <table class="z-table" style="margin-bottom: 24px;">
        <thead>
          <tr>
            <th style="width: 40px;">#</th>
            <th>Item & Scope Description</th>
            <th style="width: 80px; text-align: center;">Qty</th>
            <th style="width: 160px; text-align: right;">Unit Rate (UGX)</th>
            <th style="width: 180px; text-align: right;">Amount (UGX)</th>
          </tr>
        </thead>
        <tbody>
          {items_rows}
        </tbody>
      </table>

      <!-- Totals & Payment Details -->
      <div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 40px; align-items: flex-start;">
        <div style="background: #F8FAFC; border: 1px solid var(--z-border); border-radius: 8px; padding: 20px;">
          <div style="font-size: 12px; font-weight: 800; color: #0F172A; margin-bottom: 8px;">Banking & Payment Settlement Details:</div>
          <div style="font-size: 12.5px; color: #334155; line-height: 1.7;">
            <strong>Bank Name:</strong> Stanbic Bank Uganda Limited<br>
            <strong>Account Name:</strong> Zureka Solutions Limited<br>
            <strong>Account Number (UGX):</strong> 903001882910<br>
            <strong>Branch:</strong> Forest Mall Lugogo Branch, Kampala<br>
            <strong>MTN Corporate Merchant Code:</strong> 0773245712 (Zureka)
          </div>
        </div>

        <div style="display: flex; flex-direction: column; gap: 10px;">
          <div style="display: flex; justify-content: space-between; font-size: 13.5px; color: #475569;">
            <span>Net Scope Total:</span>
            <span>UGX {subtotal:,.0f}</span>
          </div>
          <div style="display: flex; justify-content: space-between; font-size: 13.5px; color: #475569;">
            <span>Uganda VAT (18% Output Tax):</span>
            <span>UGX {vat:,.0f}</span>
          </div>
          <div style="display: flex; justify-content: space-between; font-size: 16px; font-weight: 800; color: #0F172A; border-top: 2px solid var(--z-border); padding-top: 10px;">
            <span>Grand Total (UGX):</span>
            <span style="color: var(--z-gold-dark);">UGX {grand:,.0f}</span>
          </div>
          <div style="display: flex; justify-content: space-between; font-size: 13.5px; font-weight: 700; color: #16A34A;">
            <span>Paid to Date:</span>
            <span>UGX {paid:,.0f}</span>
          </div>
          <div style="display: flex; justify-content: space-between; font-size: 15px; font-weight: 800; color: {'#16A34A' if outstanding == 0 else '#DC2626'}; border-top: 1px solid var(--z-border); padding-top: 8px;">
            <span>Outstanding Balance:</span>
            <span>UGX {outstanding:,.0f}</span>
          </div>
        </div>
      </div>

    </div>

    <!-- Double-Entry General Ledger Trail -->
    <div style="margin-top: 40px;">
      <h3 style="font-size: 16px; font-weight: 800; color: #0F172A; margin-bottom: 12px;">📒 Accounting Ledger Postings for {inv_no}</h3>
      <div class="table-wrap">
        <table class="z-table">
          <thead>
            <tr>
              <th>Posting Date</th>
              <th>Account</th>
              <th style="text-align: right;">Debit (UGX)</th>
              <th style="text-align: right;">Credit (UGX)</th>
              <th>Against Account</th>
            </tr>
          </thead>
          <tbody>
            {gl_rows}
          </tbody>
        </table>
      </div>
    </div>
    """
    return render_desk_base(f"Invoice {inv_no}", user, content, active_tab='invoices', breadcrumbs=[("Accounts", "/desk/invoices"), ("Sales Invoices", "/desk/invoices"), (inv_no, None)])

def render_general_ledger(user: dict, gl_entries: List[dict]) -> str:
    """ERP General Ledger double-entry financial audit view."""
    rows = ""
    total_debits = sum(e.get('debit', 0.0) for e in gl_entries)
    total_credits = sum(e.get('credit', 0.0) for e in gl_entries)

    for g in gl_entries:
        rows += f"""
        <tr>
          <td style="font-size: 12px; color: #64748B;">{g.get('posting_date')}</td>
          <td style="font-weight: 700; color: #0F172A;">{g.get('account')}</td>
          <td style="text-align: right; font-weight: 700; color: {'#16A34A' if g.get('debit', 0) > 0 else '#94A3B8'};">
            {f"UGX {g.get('debit'):,.0f}" if g.get('debit', 0) > 0 else "—"}
          </td>
          <td style="text-align: right; font-weight: 700; color: {'#DC2626' if g.get('credit', 0) > 0 else '#94A3B8'};">
            {f"UGX {g.get('credit'):,.0f}" if g.get('credit', 0) > 0 else "—"}
          </td>
          <td style="font-size: 12px; color: var(--z-navy); font-weight: 600;">{g.get('voucher_type')}</td>
          <td style="font-family: monospace; font-size: 12px; font-weight: 700; color: var(--z-blue);">{g.get('voucher_no')}</td>
          <td style="font-size: 12px; color: #475569;">{g.get('against_account')}</td>
          <td style="font-size: 12px; color: #64748B;">{g.get('remarks')}</td>
        </tr>
        """

    if not rows:
        rows = "<tr><td colspan='8' style='text-align: center; color: #94A3B8; padding: 30px;'>No General Ledger transactions posted yet.</td></tr>"

    content = f"""
    <div class="erp-header">
      <div>
        <h1 class="erp-title">General Ledger (GL)</h1>
        <div class="erp-subtitle">Real double-entry financial ledger recording all debit and credit journal postings</div>
      </div>
      <div class="erp-actions">
        <a href="/desk/invoices" class="btn btn-outline">💰 Sales Invoices</a>
        <a href="/desk/chart-of-accounts" class="btn btn-outline">🌳 Chart of Accounts</a>
      </div>
    </div>

    <!-- Ledger Totals Summary -->
    <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 24px;">
      <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 10px; padding: 18px; box-shadow: var(--card-shadow);">
        <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase;">Total Debits Posted</div>
        <div style="font-size: 20px; font-weight: 800; color: #16A34A; margin-top: 4px;">UGX {total_debits:,.0f}</div>
      </div>
      <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 10px; padding: 18px; box-shadow: var(--card-shadow);">
        <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase;">Total Credits Posted</div>
        <div style="font-size: 20px; font-weight: 800; color: #DC2626; margin-top: 4px;">UGX {total_credits:,.0f}</div>
      </div>
      <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 10px; padding: 18px; box-shadow: var(--card-shadow);">
        <div style="font-size: 11px; font-weight: 700; color: #64748B; text-transform: uppercase;">Ledger Balance Status</div>
        <div style="font-size: 16px; font-weight: 800; color: {'#16A34A' if abs(total_debits - total_credits) < 1 else '#DC2626'}; margin-top: 6px;">
          {'✓ Balanced (Debits == Credits)' if abs(total_debits - total_credits) < 1 else '⚠️ Out of Balance'}
        </div>
      </div>
    </div>

    <div class="table-wrap">
      <table class="z-table">
        <thead>
          <tr>
            <th>Posting Date</th>
            <th>Account</th>
            <th style="text-align: right;">Debit</th>
            <th style="text-align: right;">Credit</th>
            <th>Voucher Type</th>
            <th>Voucher No</th>
            <th>Against Account</th>
            <th>Remarks</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </div>
    """
    return render_desk_base("General Ledger", user, content, active_tab='gl', breadcrumbs=[("Accounts", "/desk/invoices"), ("General Ledger", None)])

def render_chart_of_accounts(user: dict, coa: List[dict]) -> str:
    """ERP Chart of Accounts tree and account balances view."""
    groups = {"Asset": [], "Liability": [], "Equity": [], "Income": [], "Expense": []}
    for acc in coa:
        groups.setdefault(acc.get('root_type', 'Asset'), []).append(acc)

    sections_html = ""
    for root_type, accs in groups.items():
        total_balance = sum(a.get('balance', 0.0) for a in accs)
        acc_rows = ""
        for a in accs:
            acc_rows += f"""
            <tr>
              <td style="font-family: monospace; font-size: 12.5px; font-weight: 700; color: var(--z-gold);">{a.get('account_number')}</td>
              <td style="font-weight: 700; color: #0F172A;">{a.get('account_name')}</td>
              <td style="font-size: 12px; color: #64748B;">{a.get('account_type')}</td>
              <td style="text-align: right; font-weight: 800; color: #0F172A;">UGX {a.get('balance', 0.0):,.0f}</td>
            </tr>
            """
        
        sections_html += f"""
        <div style="background: #FFFFFF; border: 1px solid var(--z-border); border-radius: 10px; overflow: hidden; margin-bottom: 24px; box-shadow: var(--card-shadow);">
          <div style="background: #F8FAFC; padding: 14px 20px; border-bottom: 1px solid var(--z-border); display: flex; justify-content: space-between; align-items: center;">
            <div style="font-weight: 800; font-size: 15px; color: #0F172A;">{root_type} Accounts</div>
            <div style="font-weight: 800; font-size: 14px; color: var(--z-gold-dark);">Total: UGX {total_balance:,.0f}</div>
          </div>
          <table class="z-table">
            <thead>
              <tr>
                <th style="width: 100px;">Account #</th>
                <th>Account Name</th>
                <th style="width: 180px;">Account Type</th>
                <th style="width: 180px; text-align: right;">Current Balance</th>
              </tr>
            </thead>
            <tbody>
              {acc_rows}
            </tbody>
          </table>
        </div>
        """

    content = f"""
    <div class="erp-header">
      <div>
        <h1 class="erp-title">Chart of Accounts (COA)</h1>
        <div class="erp-subtitle">Organizational financial account tree configured for Uganda commercial taxation</div>
      </div>
      <div class="erp-actions">
        <a href="/desk/general-ledger" class="btn btn-outline">📒 General Ledger</a>
        <a href="/desk/invoices" class="btn btn-navy">💰 Sales Invoices</a>
      </div>
    </div>

    {sections_html}
    """
    return render_desk_base("Chart of Accounts", user, content, active_tab='coa', breadcrumbs=[("Accounts", "/desk/invoices"), ("Chart of Accounts", None)])

def render_payment_entries(user: dict, payments: List[dict], can_create: bool) -> str:
    """ERP Payment Entries (Bank and Cash receipts) list."""
    rows = ""
    for p in payments:
        rows += f"""
        <tr>
          <td style="font-family: monospace; font-weight: 800; color: var(--z-blue);">{p.get('payment_no')}</td>
          <td style="font-size: 12.5px; color: #475569;">{p.get('date')}</td>
          <td style="font-weight: 700; color: #0F172A;">{p.get('client_name')}</td>
          <td style="font-family: monospace; font-size: 12px; color: #334155;">{p.get('invoice_no')}</td>
          <td style="font-weight: 800; color: #16A34A; text-align: right;">UGX {p.get('amount', 0.0):,.0f}</td>
          <td style="font-size: 12.5px; color: #475569;">{p.get('mode_of_payment')}</td>
          <td style="font-family: monospace; font-size: 12px; color: #64748B;">{p.get('reference_no')}</td>
        </tr>
        """
    if not rows:
        rows = "<tr><td colspan='7' style='text-align: center; color: #94A3B8; padding: 30px;'>No payment entries recorded yet. Open a Sales Invoice to record a payment.</td></tr>"

    content = f"""
    <div class="erp-header">
      <div>
        <h1 class="erp-title">Payment Receipts (Bank & Mobile Money)</h1>
        <div class="erp-subtitle">Recorded customer settlement entries cleared against accounts receivable</div>
      </div>
      <div class="erp-actions">
        <a href="/desk/invoices" class="btn btn-navy">+ Receive via Sales Invoices</a>
      </div>
    </div>

    <div class="table-wrap">
      <table class="z-table">
        <thead>
          <tr>
            <th>Payment Voucher #</th>
            <th>Posting Date</th>
            <th>Customer Enterprise</th>
            <th>Against Invoice</th>
            <th style="text-align: right;">Settled Amount</th>
            <th>Payment Method</th>
            <th>Transaction Reference</th>
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </div>
    """
    return render_desk_base("Payment Entries", user, content, active_tab='payments', breadcrumbs=[("Accounts", "/desk/invoices"), ("Payment Entries", None)])
