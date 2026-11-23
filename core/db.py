"""
Data Layer & Offline JSON Store with ERP Accounting & General Ledger
"""
import os
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

import config
from core.auth import hash_password

DEFAULT_COA = [
    {"account_number": "1110", "account_name": "Stanbic Bank Uganda (UGX Operating)", "root_type": "Asset", "account_type": "Bank", "balance": 185000000},
    {"account_number": "1120", "account_name": "MTN Mobile Money Corporate Merchant", "root_type": "Asset", "account_type": "Bank", "balance": 34200000},
    {"account_number": "1200", "account_name": "Accounts Receivable (Debtors)", "root_type": "Asset", "account_type": "Receivable", "balance": 92500000},
    {"account_number": "2100", "account_name": "Accounts Payable (Creditors)", "root_type": "Liability", "account_type": "Payable", "balance": 24000000},
    {"account_number": "2210", "account_name": "URA VAT Payable (18%)", "root_type": "Liability", "account_type": "Tax", "balance": 16650000},
    {"account_number": "2220", "account_name": "Withholding Tax (WHT 6%) Payable", "root_type": "Liability", "account_type": "Tax", "balance": 5550000},
    {"account_number": "3100", "account_name": "Partner Capital & Retained Earnings", "root_type": "Equity", "account_type": "Equity", "balance": 200000000},
    {"account_number": "4100", "account_name": "ERPNext Implementation & Consulting Revenue", "root_type": "Income", "account_type": "Direct Income", "balance": 320000000},
    {"account_number": "4200", "account_name": "Data, AI & Business Intelligence Revenue", "root_type": "Income", "account_type": "Direct Income", "balance": 145000000},
    {"account_number": "4300", "account_name": "Annual SLA Support & Cloud Hosting Revenue", "root_type": "Income", "account_type": "Direct Income", "balance": 78000000},
    {"account_number": "5100", "account_name": "Cloud Infrastructure & Server Hosting Expense", "root_type": "Expense", "account_type": "Direct Expense", "balance": 42000000},
    {"account_number": "5200", "account_name": "Specialist Delivery & Engineering Compensation", "root_type": "Expense", "account_type": "Direct Expense", "balance": 115000000}
]

def _load_data() -> dict:
    if os.path.exists(config.DATA_FILE):
        try:
            with open(config.DATA_FILE, 'r', encoding='utf-8') as f:
                d = json.load(f)
                d.setdefault('coa', DEFAULT_COA)
                d.setdefault('gl_entries', [])
                d.setdefault('payments', [])
                d.setdefault('activity_logs', [])
                return d
        except Exception:
            pass
    return {
        "users": [],
        "systems": [],
        "clients": [],
        "quotations": [],
        "invoices": [],
        "projects": [],
        "inquiries": [],
        "coa": DEFAULT_COA,
        "gl_entries": [],
        "payments": [],
        "activity_logs": []
    }

def _save_data(data: dict) -> None:
    with open(config.DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def log_activity(user_email: str, action: str, details: str) -> None:
    data = _load_data()
    data.setdefault('activity_logs', []).insert(0, {
        "id": f"ACT-{len(data.get('activity_logs', [])) + 1:05d}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_email": user_email,
        "action": action,
        "details": details
    })
    _save_data(data)

def get_activity_logs(limit: int = 20) -> List[dict]:
    data = _load_data()
    return data.get('activity_logs', [])[:limit]

# ─── AUTHENTICATION & USERS ───

def authenticate_user(email: str, password: str) -> Optional[dict]:
    data = _load_data()
    hashed = hash_password(password)
    for u in data.get('users', []):
        if u.get('email', '').strip().lower() == email.strip().lower():
            if u.get('password_hash') == hashed:
                uc = dict(u)
                uc.pop('password_hash', None)
                return uc
    return None

def get_all_users() -> List[dict]:
    data = _load_data()
    users = []
    for u in data.get('users', []):
        uc = dict(u)
        uc.pop('password_hash', None)
        users.append(uc)
    return users

def get_user_by_email(email: str) -> Optional[dict]:
    data = _load_data()
    for u in data.get('users', []):
        if u.get('email', '').strip().lower() == email.strip().lower():
            uc = dict(u)
            uc.pop('password_hash', None)
            return uc
    return None

def update_user_profile(email: str, form_data: dict) -> Optional[dict]:
    data = _load_data()
    for u in data.get('users', []):
        if u.get('email', '').strip().lower() == email.strip().lower():
            if 'full_name' in form_data and form_data['full_name'].strip():
                u['full_name'] = form_data['full_name'].strip()
                u['avatar'] = u['full_name'][0].upper()
            if 'phone' in form_data:
                u['phone'] = form_data['phone'].strip()
            if 'title' in form_data:
                u['title'] = form_data['title'].strip()
            if 'department' in form_data:
                u['department'] = form_data['department'].strip()
            _save_data(data)
            log_activity(email, "Profile Updated", f"Personal profile and contact info updated for {email}")
            uc = dict(u)
            uc.pop('password_hash', None)
            return uc
    return None

def update_user_password(email: str, old_password: str, new_password: str) -> bool:
    data = _load_data()
    old_hash = hash_password(old_password)
    for u in data.get('users', []):
        if u.get('email', '').strip().lower() == email.strip().lower():
            if u.get('password_hash') == old_hash:
                u['password_hash'] = hash_password(new_password)
                _save_data(data)
                log_activity(email, "Password Changed", f"Security credential updated for {email}")
                return True
            return False
    return False

def admin_update_user(target_email: str, form_data: dict, admin_email: str) -> Optional[dict]:
    """Admin updates any user's role, designation, phone, or status."""
    data = _load_data()
    for u in data.get('users', []):
        if u.get('email', '').strip().lower() == target_email.strip().lower():
            if 'full_name' in form_data and form_data['full_name'].strip():
                u['full_name'] = form_data['full_name'].strip()
                u['avatar'] = u['full_name'][0].upper()
            if 'role' in form_data and form_data['role']:
                u['role'] = form_data['role']
            if 'title' in form_data:
                u['title'] = form_data['title'].strip()
            if 'department' in form_data:
                u['department'] = form_data['department'].strip()
            if 'phone' in form_data:
                u['phone'] = form_data['phone'].strip()
            if 'status' in form_data:
                u['status'] = form_data['status']
            _save_data(data)
            log_activity(admin_email, "User Account Updated", f"Administrator modified account profile for {target_email} (Role: {u.get('role')})")
            uc = dict(u)
            uc.pop('password_hash', None)
            return uc
    return None

def admin_reset_password(target_email: str, new_password: str, admin_email: str) -> bool:
    """Administrator resets password for any user account."""
    data = _load_data()
    for u in data.get('users', []):
        if u.get('email', '').strip().lower() == target_email.strip().lower():
            u['password_hash'] = hash_password(new_password)
            _save_data(data)
            log_activity(admin_email, "Password Reset by Admin", f"Administrator reset password credentials for {target_email}")
            return True
    return False

def create_user(form_data: dict, admin_email: str = 'admin@zurekasolutions.com') -> dict:
    data = _load_data()
    email = form_data.get('email', '').strip().lower()
    for u in data.get('users', []):
        if u.get('email', '').lower() == email:
            return u
    new_user = {
        "email": email,
        "password_hash": hash_password(form_data.get('password', 'zureka123')),
        "full_name": form_data.get('full_name', 'System User'),
        "title": form_data.get('title', 'Specialist'),
        "role": form_data.get('role', 'sales'),
        "department": form_data.get('department', 'Consulting Services'),
        "phone": form_data.get('phone', '+256 700 000 000'),
        "avatar": form_data.get('full_name', 'U')[0].upper(),
        "status": form_data.get('status', 'Active')
    }
    data.setdefault('users', []).append(new_user)
    _save_data(data)
    log_activity(admin_email, "User Account Created", f"Administrator created new user account {email} (Role: {new_user['role']})")
    uc = dict(new_user)
    uc.pop('password_hash', None)
    return uc

# ─── CHART OF ACCOUNTS & GENERAL LEDGER ───

def get_chart_of_accounts() -> List[dict]:
    data = _load_data()
    return data.get('coa', DEFAULT_COA)

def post_gl_entry(posting_date: str, account_name: str, debit: float, credit: float, voucher_type: str, voucher_no: str, against_account: str, remarks: str) -> dict:
    data = _load_data()
    entry = {
        "id": f"GL-{len(data.get('gl_entries', [])) + 1:06d}",
        "posting_date": posting_date,
        "account": account_name,
        "debit": float(debit),
        "credit": float(credit),
        "voucher_type": voucher_type,
        "voucher_no": voucher_no,
        "against_account": against_account,
        "remarks": remarks
    }
    data.setdefault('gl_entries', []).insert(0, entry)
    
    # Update COA balance
    for acc in data.get('coa', []):
        if acc['account_name'] == account_name:
            if acc['root_type'] in ['Asset', 'Expense']:
                acc['balance'] += (debit - credit)
            else:
                acc['balance'] += (credit - debit)
            break
            
    _save_data(data)
    return entry

def get_gl_entries(voucher_no: Optional[str] = None) -> List[dict]:
    data = _load_data()
    entries = data.get('gl_entries', [])
    if voucher_no:
        return [e for e in entries if e.get('voucher_no') == voucher_no]
    return entries

# ─── SALES INVOICES (ERP LEVEL) ───

def get_invoices(role: str, user_email: str) -> List[dict]:
    data = _load_data()
    invoices = data.get('invoices', [])
    if role == 'client':
        return [i for i in invoices if i.get('client_email', '').lower() == user_email.lower()]
    return invoices

def get_invoice_by_no(invoice_no: str) -> Optional[dict]:
    data = _load_data()
    for inv in data.get('invoices', []):
        if inv.get('invoice_no') == invoice_no:
            return inv
    return None

def add_invoice(form_data: dict) -> dict:
    data = _load_data()
    today = datetime.now().strftime('%Y-%m-%d')
    inv_no = f"ZUR-INV-{datetime.now().year}-{len(data.get('invoices', [])) + 1:04d}"
    
    # Calculate ERP line items & taxes
    subtotal = float(form_data.get('subtotal', 35000000))
    vat_rate = 0.18
    vat_amount = round(subtotal * vat_rate, 2)
    grand_total = subtotal + vat_amount
    
    items = []
    item_desc = form_data.get('description', 'Enterprise ERPNext Implementation & Architecture')
    items.append({
        "item_code": form_data.get('item_code', 'SRV-CONSULTING'),
        "description": item_desc,
        "qty": 1,
        "rate": subtotal,
        "amount": subtotal
    })

    inv = {
        "invoice_no": inv_no,
        "date": today,
        "due_date": form_data.get('due_date', today),
        "client_name": form_data.get('client_name', 'Client Enterprise'),
        "client_email": form_data.get('client_email', ''),
        "client_tin": form_data.get('client_tin', '1000293847'),
        "quotation_ref": form_data.get('quotation_ref', 'N/A'),
        "description": item_desc,
        "items": items,
        "currency": "UGX",
        "subtotal": subtotal,
        "vat_amount": vat_amount,
        "grand_total": grand_total,
        "paid_amount": 0.0,
        "outstanding_amount": grand_total,
        "status": "Unpaid",
        "docstatus": "Submitted",
        "efris_fdn": f"ZUR-EFRIS-2026-{len(data.get('invoices', [])) + 1:06d}",
        "payment_terms": form_data.get('payment_terms', 'Net 30 Days from Milestone Verification')
    }
    data.setdefault('invoices', []).append(inv)
    _save_data(data)
    
    # Automatically Post Double-Entry Journal to General Ledger
    post_gl_entry(
        posting_date=today,
        account_name="Accounts Receivable (Debtors)",
        debit=grand_total,
        credit=0.0,
        voucher_type="Sales Invoice",
        voucher_no=inv_no,
        against_account="ERPNext Implementation & Consulting Revenue",
        remarks=f"Receivable booked for {inv['client_name']} ({inv_no})"
    )
    post_gl_entry(
        posting_date=today,
        account_name="ERPNext Implementation & Consulting Revenue",
        debit=0.0,
        credit=subtotal,
        voucher_type="Sales Invoice",
        voucher_no=inv_no,
        against_account="Accounts Receivable (Debtors)",
        remarks=f"Consulting revenue recognized ({inv_no})"
    )
    post_gl_entry(
        posting_date=today,
        account_name="URA VAT Payable (18%)",
        debit=0.0,
        credit=vat_amount,
        voucher_type="Sales Invoice",
        voucher_no=inv_no,
        against_account="Accounts Receivable (Debtors)",
        remarks=f"URA Output VAT recognized 18% ({inv_no})"
    )
    
    return inv

def make_payment_entry(form_data: dict, user_email: str) -> Optional[dict]:
    """Record payment receipt against an invoice and post to Bank in General Ledger."""
    data = _load_data()
    invoice_no = form_data.get('invoice_no')
    inv = None
    for i in data.get('invoices', []):
        if i.get('invoice_no') == invoice_no:
            inv = i
            break
    if not inv:
        return None

    amount = float(form_data.get('amount', inv.get('outstanding_amount', 0)))
    mode_of_payment = form_data.get('mode_of_payment', 'Bank Transfer (Stanbic Bank)')
    bank_account = "Stanbic Bank Uganda (UGX Operating)" if "Stanbic" in mode_of_payment else "MTN Mobile Money Corporate Merchant"
    today = datetime.now().strftime('%Y-%m-%d')
    pay_no = f"ZUR-PAY-{datetime.now().year}-{len(data.get('payments', [])) + 1:04d}"

    inv['paid_amount'] = round(inv.get('paid_amount', 0.0) + amount, 2)
    inv['outstanding_amount'] = max(0.0, round(inv.get('grand_total', 0.0) - inv['paid_amount'], 2))
    if inv['outstanding_amount'] == 0:
        inv['status'] = 'Paid'

    payment_record = {
        "payment_no": pay_no,
        "date": today,
        "invoice_no": invoice_no,
        "client_name": inv['client_name'],
        "client_email": inv.get('client_email', ''),
        "amount": amount,
        "mode_of_payment": mode_of_payment,
        "reference_no": form_data.get('reference_no', f"TXN-{datetime.now().strftime('%H%M%S')}"),
        "received_by": user_email
    }
    data.setdefault('payments', []).insert(0, payment_record)
    _save_data(data)

    # Post Payment to General Ledger (Debit Bank, Credit Accounts Receivable)
    post_gl_entry(
        posting_date=today,
        account_name=bank_account,
        debit=amount,
        credit=0.0,
        voucher_type="Payment Entry",
        voucher_no=pay_no,
        against_account="Accounts Receivable (Debtors)",
        remarks=f"Payment received from {inv['client_name']} against {invoice_no}"
    )
    post_gl_entry(
        posting_date=today,
        account_name="Accounts Receivable (Debtors)",
        debit=0.0,
        credit=amount,
        voucher_type="Payment Entry",
        voucher_no=pay_no,
        against_account=bank_account,
        remarks=f"Receivable cleared for {invoice_no} via {pay_no}"
    )

    log_activity(user_email, "Payment Received", f"Received UGX {amount:,.0f} for {invoice_no} ({pay_no})")
    return payment_record

def get_payments(role: str, user_email: str) -> List[dict]:
    data = _load_data()
    payments = data.get('payments', [])
    if role == 'client':
        return [p for p in payments if p.get('client_email', '').lower() == user_email.lower()]
    return payments

# ─── PROPOSALS & QUOTATIONS ───

def get_quotations(role: str, user_email: str) -> List[dict]:
    data = _load_data()
    quotes = data.get('quotations', [])
    if role == 'client':
        return [q for q in quotes if q.get('client_email', '').lower() == user_email.lower()]
    return quotes

def get_quotation_by_no(quote_no: str) -> Optional[dict]:
    data = _load_data()
    for q in data.get('quotations', []):
        if q.get('quote_no') == quote_no:
            return q
    return None

def add_quotation(form_data: dict) -> dict:
    data = _load_data()
    today = datetime.now().strftime('%Y-%m-%d')
    quote_no = f"ZUR-QT-{datetime.now().year}-{len(data.get('quotations', [])) + 1:04d}"
    
    quote = {
        "quote_no": quote_no,
        "date": today,
        "client_name": form_data.get('client_name', 'Client Enterprise'),
        "client_email": form_data.get('client_email', ''),
        "client_phone": form_data.get('client_phone', ''),
        "system_code": form_data.get('system_code', 'ERP-001'),
        "system_name": form_data.get('system_name', 'Tailored Architecture'),
        "scope_summary": form_data.get('scope_summary', 'Enterprise discovery and solution design.'),
        "timeline_weeks": form_data.get('timeline_weeks', '8-12 Weeks'),
        "status": "Draft",
        "pricing_model": "Tailored Scope & Architecture",
        "estimated_value": float(form_data.get('estimated_value', 45000000))
    }
    data.setdefault('quotations', []).append(quote)
    _save_data(data)
    return quote

def approve_quotation(quote_no: str) -> Optional[dict]:
    data = _load_data()
    for q in data.get('quotations', []):
        if q.get('quote_no') == quote_no:
            q['status'] = 'Approved'
            _save_data(data)
            return q
    return None

def convert_quotation_to_invoice(quote_no: str, user_email: str) -> Optional[dict]:
    quote = get_quotation_by_no(quote_no)
    if not quote:
        return None
    inv_data = {
        "client_name": quote['client_name'],
        "client_email": quote['client_email'],
        "quotation_ref": quote_no,
        "description": f"Phase 1 Mobilization & Deployment: {quote['system_name']}",
        "subtotal": quote.get('estimated_value', 45000000) * 0.40  # 40% Mobilization Invoice
    }
    inv = add_invoice(inv_data)
    log_activity(user_email, "Invoice Generated", f"Created milestone invoice {inv['invoice_no']} from proposal {quote_no}")
    return inv

def convert_quotation_to_project(quote_no: str, user_email: str) -> Optional[dict]:
    quote = get_quotation_by_no(quote_no)
    if not quote:
        return None
    proj_data = {
        "name": f"Implementation: {quote['system_name']} for {quote['client_name']}",
        "client_name": quote['client_name'],
        "client_email": quote['client_email'],
        "practice_lead": "Eng. Brian Mukasa",
        "status": "Planning & Discovery",
        "completion_pct": 15
    }
    proj = add_project(proj_data)
    log_activity(user_email, "Project Initiated", f"Initiated delivery project {proj['code']} from proposal {quote_no}")
    return proj

# ─── PROJECTS & CRM ───

def get_projects(role: str, user_email: str) -> List[dict]:
    data = _load_data()
    raw_projects = data.get('projects', [])
    normalized = []
    for p in raw_projects:
        item = dict(p)
        item['code'] = p.get('code') or p.get('id', 'PRJ-001')
        item['name'] = p.get('name') or p.get('project_name', 'Digital Transformation Delivery')
        item['practice_lead'] = p.get('practice_lead') or p.get('lead_partner', 'Eng. Brian Mukasa')
        item['status'] = p.get('status') or p.get('framework_stage', 'Planning & Discovery')
        item['completion_pct'] = p.get('completion_pct', 25)
        item['current_milestone'] = p.get('current_milestone') or p.get('milestone', 'Discovery & Analysis')
        normalized.append(item)
    if role == 'client':
        return [p for p in normalized if p.get('client_email', '').lower() == user_email.lower()]
    return normalized

def add_project(form_data: dict) -> dict:
    data = _load_data()
    p_code = f"PRJ-{len(data.get('projects', [])) + 1:03d}"
    proj = {
        "code": p_code,
        "id": p_code,
        "name": form_data.get('name', 'Digital Transformation Delivery'),
        "project_name": form_data.get('name', 'Digital Transformation Delivery'),
        "client_name": form_data.get('client_name', 'Enterprise Client'),
        "client_email": form_data.get('client_email', ''),
        "practice_lead": form_data.get('practice_lead', 'Eng. Brian Mukasa'),
        "lead_partner": form_data.get('practice_lead', 'Eng. Brian Mukasa'),
        "status": form_data.get('status', 'Planning & Discovery'),
        "framework_stage": form_data.get('status', 'Planning & Discovery'),
        "completion_pct": int(form_data.get('completion_pct', 10)),
        "current_milestone": form_data.get('current_milestone', 'Discovery & Process Mapping'),
        "milestone": form_data.get('current_milestone', 'Discovery & Process Mapping')
    }
    data.setdefault('projects', []).append(proj)
    _save_data(data)
    return proj

def update_project_progress(project_code: str, status: str, pct: int, milestone: str, user_email: str) -> Optional[dict]:
    data = _load_data()
    for p in data.get('projects', []):
        if p.get('code') == project_code or p.get('id') == project_code:
            p['status'] = status
            p['framework_stage'] = status
            p['completion_pct'] = int(pct)
            p['current_milestone'] = milestone
            p['milestone'] = milestone
            _save_data(data)
            log_activity(user_email, "Project Updated", f"Project {project_code} updated to {pct}% ({status})")
            return p
    return None

def get_clients() -> List[dict]:
    data = _load_data()
    return data.get('clients', [])

def add_client(form_data: dict) -> dict:
    data = _load_data()
    client = {
        "code": f"CLI-{len(data.get('clients', [])) + 1:03d}",
        "name": form_data.get('name', 'Client Organization'),
        "industry": form_data.get('industry', 'Commercial Services'),
        "contact_person": form_data.get('contact_person', ''),
        "email": form_data.get('email', ''),
        "phone": form_data.get('phone', ''),
        "systems_deployed": [s.strip() for s in form_data.get('systems_deployed', '').split(',') if s.strip()]
    }
    data.setdefault('clients', []).append(client)
    _save_data(data)
    return client

def get_systems(pillar: Optional[str] = None) -> List[dict]:
    data = _load_data()
    systems = data.get('systems', [])
    if pillar:
        return [s for s in systems if s.get('pillar', '').lower() == pillar.lower()]
    return systems

def get_system_by_code(code: str) -> Optional[dict]:
    data = _load_data()
    for s in data.get('systems', []):
        if s.get('code') == code:
            return s
    return None

def add_system(form_data: dict) -> dict:
    data = _load_data()
    item = {
        "code": form_data.get('code', f"SYS-{len(data.get('systems', [])) + 1:03d}"),
        "name": form_data.get('name', 'Enterprise Solution'),
        "pillar": form_data.get('pillar', 'ERP'),
        "description": form_data.get('description', ''),
        "features": [f.strip() for f in form_data.get('features', '').split(',') if f.strip()],
        "readiness": form_data.get('readiness', 'Ready for Scoping'),
        "tier": form_data.get('tier', 'Enterprise Core')
    }
    data.setdefault('systems', []).append(item)
    _save_data(data)
    return item

def add_inquiry(form_data: dict) -> dict:
    data = _load_data()
    item = {
        "id": f"INQ-{len(data.get('inquiries', [])) + 1:04d}",
        "timestamp": datetime.now().isoformat(),
        "company_name": form_data.get('company_name', ''),
        "contact_name": form_data.get('contact_name', ''),
        "email": form_data.get('email', ''),
        "phone": form_data.get('phone', ''),
        "industry": form_data.get('industry', ''),
        "system_interest": form_data.get('system_interest', ''),
        "requirements": form_data.get('requirements', ''),
        "status": "New"
    }
    data.setdefault('inquiries', []).append(item)
    _save_data(data)
    return item

def get_inquiries() -> List[dict]:
    data = _load_data()
    return data.get('inquiries', [])

# ─── ERP EXECUTIVE DASHBOARD STATS ───

def get_stats(role: str, user_email: str) -> dict:
    quotes = get_quotations(role, user_email)
    invoices = get_invoices(role, user_email)
    projects = get_projects(role, user_email)
    systems = get_systems()
    clients = get_clients()
    
    total_invoiced = sum(i.get('grand_total', 0.0) for i in invoices)
    total_collected = sum(i.get('paid_amount', 0.0) for i in invoices)
    total_outstanding = sum(i.get('outstanding_amount', 0.0) for i in invoices)

    return {
        "quotations_count": len(quotes),
        "invoices_count": len(invoices),
        "projects_count": len(projects),
        "systems_count": len(systems),
        "clients_count": len(clients),
        "total_invoiced_ugx": total_invoiced,
        "total_collected_ugx": total_collected,
        "total_outstanding_ugx": total_outstanding,
        "active_projects": len([p for p in projects if p.get('status') != 'Completed'])
    }
