"""
PostgreSQL Storage Engine for Zureka ERPNext Core
Compatible with Render PostgreSQL, Supabase, Neon, AWS RDS, and Local PostgreSQL
"""
import json
from datetime import datetime
from typing import List, Dict, Any, Optional

import config

_PG_AVAILABLE = False
try:
    import psycopg2
    import psycopg2.extras
    _PG_AVAILABLE = True
except ImportError:
    _PG_AVAILABLE = False


def is_postgres_enabled() -> bool:
    """Return True if DATABASE_URL is configured and psycopg2 is installed."""
    return bool(_PG_AVAILABLE and config.DATABASE_URL)


def get_connection():
    """Create and return a new PostgreSQL connection with autocommit or session handling."""
    if not is_postgres_enabled():
        raise RuntimeError("PostgreSQL is not configured or psycopg2 is not installed.")
    return psycopg2.connect(config.DATABASE_URL)


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS users (
    email VARCHAR(255) PRIMARY KEY,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    title VARCHAR(255),
    role VARCHAR(50) NOT NULL,
    department VARCHAR(255),
    phone VARCHAR(50),
    status VARCHAR(50) DEFAULT 'Active',
    avatar VARCHAR(10) DEFAULT 'U',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS accounts (
    account_number VARCHAR(50) PRIMARY KEY,
    account_name VARCHAR(255) NOT NULL,
    root_type VARCHAR(50) NOT NULL,
    account_type VARCHAR(50) NOT NULL,
    balance NUMERIC(18, 2) DEFAULT 0.00
);

CREATE TABLE IF NOT EXISTS gl_entries (
    id VARCHAR(50) PRIMARY KEY,
    voucher_no VARCHAR(100),
    posting_date VARCHAR(50),
    account VARCHAR(255),
    party VARCHAR(255),
    debit NUMERIC(18, 2) DEFAULT 0.00,
    credit NUMERIC(18, 2) DEFAULT 0.00,
    remarks TEXT,
    timestamp VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS invoices (
    invoice_no VARCHAR(100) PRIMARY KEY,
    client_name VARCHAR(255) NOT NULL,
    client_email VARCHAR(255),
    system_name VARCHAR(255),
    issue_date VARCHAR(50),
    due_date VARCHAR(50),
    total_amount NUMERIC(18, 2) DEFAULT 0.00,
    balance_due NUMERIC(18, 2) DEFAULT 0.00,
    status VARCHAR(50) DEFAULT 'Draft',
    lines JSONB DEFAULT '[]'::jsonb,
    payment_history JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS payments (
    payment_no VARCHAR(100) PRIMARY KEY,
    invoice_no VARCHAR(100),
    client_name VARCHAR(255),
    amount NUMERIC(18, 2) DEFAULT 0.00,
    payment_mode VARCHAR(100),
    reference_no VARCHAR(100),
    date VARCHAR(50),
    status VARCHAR(50) DEFAULT 'Cleared',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS projects (
    code VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    client VARCHAR(255),
    status VARCHAR(50) DEFAULT 'Planning',
    progress INT DEFAULT 0,
    target_date VARCHAR(50),
    lead VARCHAR(255),
    scope TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS quotations (
    quote_no VARCHAR(100) PRIMARY KEY,
    client_name VARCHAR(255) NOT NULL,
    client_email VARCHAR(255),
    client_phone VARCHAR(50),
    system_name VARCHAR(255),
    total_amount NUMERIC(18, 2) DEFAULT 0.00,
    validity_date VARCHAR(50),
    status VARCHAR(50) DEFAULT 'Draft',
    scope JSONB DEFAULT '[]'::jsonb,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS clients (
    id VARCHAR(50) PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    contact_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    industry VARCHAR(100),
    status VARCHAR(50) DEFAULT 'Active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS inquiries (
    id VARCHAR(50) PRIMARY KEY,
    company_name VARCHAR(255) NOT NULL,
    contact_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(50),
    system_interest VARCHAR(255),
    scope_summary TEXT,
    created_at VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS systems (
    code VARCHAR(100) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    pillar VARCHAR(100),
    tier VARCHAR(100),
    description TEXT,
    features JSONB DEFAULT '[]'::jsonb
);

CREATE TABLE IF NOT EXISTS activity_logs (
    id VARCHAR(50) PRIMARY KEY,
    timestamp VARCHAR(50),
    user_email VARCHAR(255),
    action VARCHAR(255),
    details TEXT
);
"""


def init_db(seed_data: Optional[dict] = None) -> bool:
    """Initialize PostgreSQL tables and auto-seed initial data if tables are empty."""
    if not is_postgres_enabled():
        return False

    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(SCHEMA_SQL)
                conn.commit()

                # Check if seeding is needed
                cur.execute("SELECT COUNT(*) FROM users;")
                count = cur.fetchone()[0]
                if count == 0 and seed_data:
                    seed_from_dict(conn, seed_data)
        return True
    except Exception as e:
        print(f"[PostgreSQL Warning] Failed to initialize PostgreSQL: {e}")
        return False


def seed_from_dict(conn, seed: dict) -> None:
    """Seed initial records into PostgreSQL from json dict."""
    with conn.cursor() as cur:
        # Users
        for u in seed.get('users', []):
            cur.execute("""
                INSERT INTO users (email, password_hash, full_name, title, role, department, phone, status, avatar)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (email) DO NOTHING;
            """, (
                u.get('email', '').lower(),
                u.get('password_hash', ''),
                u.get('full_name', ''),
                u.get('title', ''),
                u.get('role', 'client'),
                u.get('department', ''),
                u.get('phone', ''),
                u.get('status', 'Active'),
                u.get('avatar', 'U')
            ))

        # Chart of Accounts
        for a in seed.get('coa', []):
            cur.execute("""
                INSERT INTO accounts (account_number, account_name, root_type, account_type, balance)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (account_number) DO NOTHING;
            """, (
                str(a.get('account_number')),
                a.get('account_name', ''),
                a.get('root_type', 'Asset'),
                a.get('account_type', ''),
                float(a.get('balance', 0.0))
            ))

        # GL Entries
        for gl in seed.get('gl_entries', []):
            cur.execute("""
                INSERT INTO gl_entries (id, voucher_no, posting_date, account, party, debit, credit, remarks, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (
                gl.get('id', ''),
                gl.get('voucher_no', ''),
                gl.get('posting_date', ''),
                gl.get('account', ''),
                gl.get('party', ''),
                float(gl.get('debit', 0.0)),
                float(gl.get('credit', 0.0)),
                gl.get('remarks', ''),
                gl.get('timestamp', '')
            ))

        # Invoices
        for inv in seed.get('invoices', []):
            cur.execute("""
                INSERT INTO invoices (invoice_no, client_name, client_email, system_name, issue_date, due_date, total_amount, balance_due, status, lines, payment_history)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (invoice_no) DO NOTHING;
            """, (
                inv.get('invoice_no', ''),
                inv.get('client_name', ''),
                inv.get('client_email', ''),
                inv.get('system_name', ''),
                inv.get('issue_date', ''),
                inv.get('due_date', ''),
                float(inv.get('total_amount', 0.0)),
                float(inv.get('balance_due', 0.0)),
                inv.get('status', 'Draft'),
                json.dumps(inv.get('lines', [])),
                json.dumps(inv.get('payment_history', []))
            ))

        # Payments
        for p in seed.get('payments', []):
            cur.execute("""
                INSERT INTO payments (payment_no, invoice_no, client_name, amount, payment_mode, reference_no, date, status, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (payment_no) DO NOTHING;
            """, (
                p.get('payment_no', ''),
                p.get('invoice_no', ''),
                p.get('client_name', ''),
                float(p.get('amount', 0.0)),
                p.get('payment_mode', 'Bank Wire'),
                p.get('reference_no', ''),
                p.get('date', ''),
                p.get('status', 'Cleared'),
                p.get('notes', '')
            ))

        # Projects
        for prj in seed.get('projects', []):
            code = prj.get('code') or prj.get('id', '')
            name = prj.get('name') or prj.get('project_name', '')
            cur.execute("""
                INSERT INTO projects (code, name, client, status, progress, target_date, lead, scope)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (code) DO NOTHING;
            """, (
                code,
                name,
                prj.get('client', ''),
                prj.get('status', 'Planning'),
                int(prj.get('progress', 0)),
                prj.get('target_date', ''),
                prj.get('lead', ''),
                prj.get('scope', '')
            ))

        # Quotations
        for q in seed.get('quotations', []):
            cur.execute("""
                INSERT INTO quotations (quote_no, client_name, client_email, client_phone, system_name, total_amount, validity_date, status, scope)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (quote_no) DO NOTHING;
            """, (
                q.get('quote_no', ''),
                q.get('client_name', ''),
                q.get('client_email', ''),
                q.get('client_phone', ''),
                q.get('system_name', ''),
                float(q.get('total_amount', 0.0)),
                q.get('validity_date', ''),
                q.get('status', 'Draft'),
                json.dumps(q.get('scope', []))
            ))

        # Clients
        for c in seed.get('clients', []):
            cur.execute("""
                INSERT INTO clients (id, company_name, contact_name, email, phone, industry, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (
                c.get('id', ''),
                c.get('company_name', ''),
                c.get('contact_name', ''),
                c.get('email', ''),
                c.get('phone', ''),
                c.get('industry', ''),
                c.get('status', 'Active')
            ))

        # Inquiries
        for inq in seed.get('inquiries', []):
            cur.execute("""
                INSERT INTO inquiries (id, company_name, contact_name, email, phone, system_interest, scope_summary, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (
                inq.get('id', ''),
                inq.get('company_name', ''),
                inq.get('contact_name', ''),
                inq.get('email', ''),
                inq.get('phone', ''),
                inq.get('system_interest', ''),
                inq.get('scope_summary', ''),
                inq.get('created_at', '')
            ))

        # Systems
        for s in seed.get('systems', []):
            cur.execute("""
                INSERT INTO systems (code, name, pillar, tier, description, features)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (code) DO NOTHING;
            """, (
                s.get('code', ''),
                s.get('name', ''),
                s.get('pillar', ''),
                s.get('tier', ''),
                s.get('description', ''),
                json.dumps(s.get('features', []))
            ))

        # Activity Logs
        for act in seed.get('activity_logs', []):
            cur.execute("""
                INSERT INTO activity_logs (id, timestamp, user_email, action, details)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """, (
                act.get('id', ''),
                act.get('timestamp', ''),
                act.get('user_email', ''),
                act.get('action', ''),
                act.get('details', '')
            ))

        conn.commit()


# ─── DATABASE QUERY & MUTATION APIS ───

def pg_authenticate_user(email: str, password_hash: str) -> Optional[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(%s) AND password_hash = %s;", (email.strip(), password_hash))
            row = cur.fetchone()
            if row:
                u = dict(row)
                u.pop('password_hash', None)
                return u
    return None

def pg_get_all_users() -> List[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM users ORDER BY full_name ASC;")
            users = []
            for row in cur.fetchall():
                u = dict(row)
                u.pop('password_hash', None)
                users.append(u)
            return users

def pg_get_user_by_email(email: str) -> Optional[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(%s);", (email.strip(),))
            row = cur.fetchone()
            if row:
                u = dict(row)
                u.pop('password_hash', None)
                return u
    return None

def pg_update_user_profile(email: str, form_data: dict) -> Optional[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(%s);", (email.strip(),))
            row = cur.fetchone()
            if not row:
                return None
            full_name = form_data.get('full_name', row['full_name']).strip() or row['full_name']
            avatar = full_name[0].upper()
            phone = form_data.get('phone', row['phone']).strip()
            title = form_data.get('title', row['title']).strip()
            dept = form_data.get('department', row['department']).strip()
            cur.execute("""
                UPDATE users SET full_name = %s, avatar = %s, phone = %s, title = %s, department = %s
                WHERE LOWER(email) = LOWER(%s);
            """, (full_name, avatar, phone, title, dept, email.strip()))
            conn.commit()
            return pg_get_user_by_email(email)

def pg_update_user_password(email: str, old_hash: str, new_hash: str) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT password_hash FROM users WHERE LOWER(email) = LOWER(%s);", (email.strip(),))
            row = cur.fetchone()
            if row and row[0] == old_hash:
                cur.execute("UPDATE users SET password_hash = %s WHERE LOWER(email) = LOWER(%s);", (new_hash, email.strip()))
                conn.commit()
                return True
    return False

def pg_admin_update_user(target_email: str, form_data: dict, admin_email: str, new_hash: Optional[str] = None) -> Optional[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM users WHERE LOWER(email) = LOWER(%s);", (target_email.strip(),))
            row = cur.fetchone()
            if not row:
                return None
            full_name = form_data.get('full_name', row['full_name']).strip() or row['full_name']
            avatar = full_name[0].upper()
            role = form_data.get('role', row['role'])
            status = form_data.get('status', row['status'])
            title = form_data.get('title', row['title']).strip()
            dept = form_data.get('department', row['department']).strip()
            phone = form_data.get('phone', row['phone']).strip()
            new_email = form_data.get('new_email', target_email).strip().lower()

            if new_hash:
                cur.execute("""
                    UPDATE users SET email = %s, full_name = %s, avatar = %s, role = %s, status = %s, title = %s, department = %s, phone = %s, password_hash = %s
                    WHERE LOWER(email) = LOWER(%s);
                """, (new_email, full_name, avatar, role, status, title, dept, phone, new_hash, target_email.strip()))
            else:
                cur.execute("""
                    UPDATE users SET email = %s, full_name = %s, avatar = %s, role = %s, status = %s, title = %s, department = %s, phone = %s
                    WHERE LOWER(email) = LOWER(%s);
                """, (new_email, full_name, avatar, role, status, title, dept, phone, target_email.strip()))
            conn.commit()
            return pg_get_user_by_email(new_email)

def pg_admin_reset_password(target_email: str, new_hash: str, admin_email: str) -> bool:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users SET password_hash = %s WHERE LOWER(email) = LOWER(%s);", (new_hash, target_email.strip()))
            conn.commit()
            return cur.rowcount > 0

def pg_create_user(form_data: dict, admin_email: str, pwd_hash: str) -> dict:
    email = form_data.get('email', '').strip().lower()
    full_name = form_data.get('full_name', 'System User').strip()
    avatar = full_name[0].upper() if full_name else 'U'
    role = form_data.get('role', 'sales')
    title = form_data.get('title', 'Specialist')
    dept = form_data.get('department', 'Consulting Services')
    phone = form_data.get('phone', '')

    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("""
                INSERT INTO users (email, password_hash, full_name, title, role, department, phone, status, avatar)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'Active', %s)
                ON CONFLICT (email) DO UPDATE SET full_name = EXCLUDED.full_name
                RETURNING *;
            """, (email, pwd_hash, full_name, title, role, dept, phone, avatar))
            conn.commit()
            row = cur.fetchone()
            u = dict(row)
            u.pop('password_hash', None)
            return u

def pg_delete_user(target_email: str, admin_email: str) -> str:
    if target_email.strip().lower() == admin_email.strip().lower():
        return "self"

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("LOCK TABLE users IN SHARE ROW EXCLUSIVE MODE;")
            cur.execute(
                "SELECT email, role FROM users WHERE LOWER(email) = LOWER(%s);",
                (target_email.strip(),)
            )
            target = cur.fetchone()
            if not target:
                return "not_found"

            if target[1].lower() == 'admin':
                cur.execute("SELECT COUNT(*) FROM users WHERE LOWER(role) = 'admin';")
                if cur.fetchone()[0] <= 1:
                    return "last_admin"

            cur.execute("DELETE FROM users WHERE LOWER(email) = LOWER(%s);", (target_email.strip(),))
            if cur.rowcount != 1:
                return "not_found"
            conn.commit()
            return "deleted"

# Systems
def pg_get_systems() -> List[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM systems ORDER BY code ASC;")
            res = []
            for r in cur.fetchall():
                d = dict(r)
                if isinstance(d.get('features'), str):
                    d['features'] = json.loads(d['features'])
                res.append(d)
            return res

def pg_get_system_by_code(code: str) -> Optional[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM systems WHERE LOWER(code) = LOWER(%s);", (code.strip(),))
            row = cur.fetchone()
            if row:
                d = dict(row)
                if isinstance(d.get('features'), str):
                    d['features'] = json.loads(d['features'])
                return d
    return None

def pg_add_system(system_data: dict) -> dict:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("""
                INSERT INTO systems (code, name, pillar, tier, description, features)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (code) DO UPDATE SET name = EXCLUDED.name, description = EXCLUDED.description
                RETURNING *;
            """, (
                system_data.get('code'),
                system_data.get('name'),
                system_data.get('pillar'),
                system_data.get('tier'),
                system_data.get('description'),
                json.dumps(system_data.get('features', []))
            ))
            conn.commit()
            d = dict(cur.fetchone())
            if isinstance(d.get('features'), str):
                d['features'] = json.loads(d['features'])
            return d

# Clients
def pg_get_clients() -> List[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM clients ORDER BY created_at DESC;")
            return [dict(r) for r in cur.fetchall()]

def pg_add_client(client_data: dict) -> dict:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT COUNT(*) FROM clients;")
            cid = f"CLT-{cur.fetchone()[0] + 1:04d}"
            client_data['id'] = cid
            cur.execute("""
                INSERT INTO clients (id, company_name, contact_name, email, phone, industry, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                RETURNING *;
            """, (
                cid,
                client_data.get('company_name'),
                client_data.get('contact_name'),
                client_data.get('email'),
                client_data.get('phone'),
                client_data.get('industry'),
                client_data.get('status', 'Active')
            ))
            conn.commit()
            return dict(cur.fetchone())

# Quotations
def pg_get_quotations() -> List[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM quotations ORDER BY created_at DESC;")
            res = []
            for r in cur.fetchall():
                d = dict(r)
                if isinstance(d.get('scope'), str):
                    d['scope'] = json.loads(d['scope'])
                res.append(d)
            return res

def pg_get_quotation_by_no(quote_no: str) -> Optional[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM quotations WHERE quote_no = %s;", (quote_no,))
            row = cur.fetchone()
            if row:
                d = dict(row)
                if isinstance(d.get('scope'), str):
                    d['scope'] = json.loads(d['scope'])
                return d
    return None

def pg_add_quotation(quote_data: dict) -> dict:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT COUNT(*) FROM quotations;")
            q_no = f"ZUR-QT-2026-{cur.fetchone()[0] + 1:04d}"
            quote_data['quote_no'] = q_no
            cur.execute("""
                INSERT INTO quotations (quote_no, client_name, client_email, client_phone, system_name, total_amount, validity_date, status, scope)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *;
            """, (
                q_no,
                quote_data.get('client_name'),
                quote_data.get('client_email'),
                quote_data.get('client_phone'),
                quote_data.get('system_name'),
                float(quote_data.get('total_amount', 0.0)),
                quote_data.get('validity_date'),
                quote_data.get('status', 'Draft'),
                json.dumps(quote_data.get('scope', []))
            ))
            conn.commit()
            d = dict(cur.fetchone())
            if isinstance(d.get('scope'), str):
                d['scope'] = json.loads(d['scope'])
            return d

def pg_approve_quotation(quote_no: str) -> Optional[dict]:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE quotations SET status = 'Approved' WHERE quote_no = %s;", (quote_no,))
            conn.commit()
            return pg_get_quotation_by_no(quote_no)

# Invoices
def pg_get_invoices() -> List[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM invoices ORDER BY created_at DESC;")
            res = []
            for r in cur.fetchall():
                d = dict(r)
                if isinstance(d.get('lines'), str):
                    d['lines'] = json.loads(d['lines'])
                if isinstance(d.get('payment_history'), str):
                    d['payment_history'] = json.loads(d['payment_history'])
                res.append(d)
            return res

def pg_get_invoice_by_no(invoice_no: str) -> Optional[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM invoices WHERE invoice_no = %s;", (invoice_no,))
            row = cur.fetchone()
            if row:
                d = dict(row)
                if isinstance(d.get('lines'), str):
                    d['lines'] = json.loads(d['lines'])
                if isinstance(d.get('payment_history'), str):
                    d['payment_history'] = json.loads(d['payment_history'])
                return d
    return None

def pg_add_invoice(inv_data: dict) -> dict:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT COUNT(*) FROM invoices;")
            inv_no = f"ZUR-INV-2026-{cur.fetchone()[0] + 1:04d}"
            inv_data['invoice_no'] = inv_no
            total = float(inv_data.get('total_amount', 0.0))
            bal = float(inv_data.get('balance_due', total))
            cur.execute("""
                INSERT INTO invoices (invoice_no, client_name, client_email, system_name, issue_date, due_date, total_amount, balance_due, status, lines, payment_history)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *;
            """, (
                inv_no,
                inv_data.get('client_name'),
                inv_data.get('client_email'),
                inv_data.get('system_name'),
                inv_data.get('issue_date'),
                inv_data.get('due_date'),
                total,
                bal,
                inv_data.get('status', 'Unpaid'),
                json.dumps(inv_data.get('lines', [])),
                json.dumps(inv_data.get('payment_history', []))
            ))
            conn.commit()
            d = dict(cur.fetchone())
            if isinstance(d.get('lines'), str):
                d['lines'] = json.loads(d['lines'])
            if isinstance(d.get('payment_history'), str):
                d['payment_history'] = json.loads(d['payment_history'])
            return d

# Payments
def pg_get_payments() -> List[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM payments ORDER BY created_at DESC;")
            return [dict(r) for r in cur.fetchall()]

def pg_make_payment_entry(form_data: dict) -> dict:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT COUNT(*) FROM payments;")
            pay_no = f"PAY-2026-{cur.fetchone()[0] + 1:04d}"
            amount = float(form_data.get('amount', 0.0))
            inv_no = form_data.get('invoice_no')
            date_str = form_data.get('date', datetime.now().strftime("%Y-%m-%d"))

            cur.execute("""
                INSERT INTO payments (payment_no, invoice_no, client_name, amount, payment_mode, reference_no, date, status, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, 'Cleared', %s)
                RETURNING *;
            """, (
                pay_no,
                inv_no,
                form_data.get('client_name'),
                amount,
                form_data.get('payment_mode', 'Bank Wire'),
                form_data.get('reference_no', ''),
                date_str,
                form_data.get('notes', '')
            ))
            pay_entry = dict(cur.fetchone())

            # Update Invoice
            cur.execute("SELECT * FROM invoices WHERE invoice_no = %s;", (inv_no,))
            inv_row = cur.fetchone()
            if inv_row:
                bal = float(inv_row['balance_due']) - amount
                if bal < 0:
                    bal = 0.0
                new_status = 'Paid' if bal <= 0 else 'Partially Paid'
                hist = inv_row['payment_history']
                if isinstance(hist, str):
                    hist = json.loads(hist)
                hist.append({
                    "payment_no": pay_no,
                    "date": date_str,
                    "amount": amount,
                    "mode": form_data.get('payment_mode')
                })
                cur.execute("""
                    UPDATE invoices SET balance_due = %s, status = %s, payment_history = %s
                    WHERE invoice_no = %s;
                """, (bal, new_status, json.dumps(hist), inv_no))

            conn.commit()
            return pay_entry

# COA & GL
def pg_get_chart_of_accounts() -> List[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM accounts ORDER BY account_number ASC;")
            return [dict(r) for r in cur.fetchall()]

def pg_get_gl_entries() -> List[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM gl_entries ORDER BY id DESC;")
            return [dict(r) for r in cur.fetchall()]

def pg_post_gl_entry(voucher_no: str, posting_date: str, account: str, party: str, debit: float, credit: float, remarks: str) -> dict:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT COUNT(*) FROM gl_entries;")
            gl_id = f"GL-2026-{cur.fetchone()[0] + 1:05d}"
            cur.execute("""
                INSERT INTO gl_entries (id, voucher_no, posting_date, account, party, debit, credit, remarks, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *;
            """, (
                gl_id,
                voucher_no,
                posting_date,
                account,
                party,
                float(debit),
                float(credit),
                remarks,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            ))

            # Update account balance
            diff = float(debit) - float(credit)
            cur.execute("""
                UPDATE accounts SET balance = balance + %s WHERE account_name = %s;
            """, (diff, account))

            conn.commit()
            return dict(cur.fetchone())

# Projects
def pg_get_projects() -> List[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM projects ORDER BY created_at DESC;")
            return [dict(r) for r in cur.fetchall()]

def pg_add_project(project_data: dict) -> dict:
    code = project_data.get('code') or project_data.get('id', '')
    name = project_data.get('name') or project_data.get('project_name', '')
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("""
                INSERT INTO projects (code, name, client, status, progress, target_date, lead, scope)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *;
            """, (
                code,
                name,
                project_data.get('client', ''),
                project_data.get('status', 'Planning'),
                int(project_data.get('progress', 0)),
                project_data.get('target_date', ''),
                project_data.get('lead', ''),
                project_data.get('scope', '')
            ))
            conn.commit()
            return dict(cur.fetchone())

def pg_update_project_progress(code: str, progress: int, status: str) -> Optional[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("""
                UPDATE projects SET progress = %s, status = %s WHERE code = %s
                RETURNING *;
            """, (progress, status, code))
            conn.commit()
            row = cur.fetchone()
            return dict(row) if row else None

# Inquiries
def pg_get_inquiries() -> List[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM inquiries ORDER BY id DESC;")
            return [dict(r) for r in cur.fetchall()]

def pg_add_inquiry(inq_data: dict) -> dict:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT COUNT(*) FROM inquiries;")
            inq_id = f"INQ-{cur.fetchone()[0] + 1:04d}"
            inq_data['id'] = inq_id
            created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
            cur.execute("""
                INSERT INTO inquiries (id, company_name, contact_name, email, phone, system_interest, scope_summary, created_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING *;
            """, (
                inq_id,
                inq_data.get('company_name'),
                inq_data.get('contact_name'),
                inq_data.get('email'),
                inq_data.get('phone'),
                inq_data.get('system_interest'),
                inq_data.get('scope_summary'),
                created_at
            ))
            conn.commit()
            return dict(cur.fetchone())

# Activity Logs
def pg_log_activity(user_email: str, action: str, details: str) -> None:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COUNT(*) FROM activity_logs;")
            act_id = f"ACT-{cur.fetchone()[0] + 1:05d}"
            ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cur.execute("""
                INSERT INTO activity_logs (id, timestamp, user_email, action, details)
                VALUES (%s, %s, %s, %s, %s);
            """, (act_id, ts, user_email, action, details))
            conn.commit()

def pg_get_activity_logs(limit: int = 20) -> List[dict]:
    with get_connection() as conn:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute("SELECT * FROM activity_logs ORDER BY id DESC LIMIT %s;", (limit,))
            return [dict(r) for r in cur.fetchall()]

# Stats
def pg_get_stats() -> dict:
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT COALESCE(SUM(total_amount), 0), COALESCE(SUM(balance_due), 0) FROM invoices;")
            row_inv = cur.fetchone()
            total_inv = float(row_inv[0])
            outst = float(row_inv[1])
            coll = total_inv - outst
            if coll < 0:
                coll = 0.0

            cur.execute("SELECT COUNT(*) FROM projects WHERE status != 'Completed';")
            active_p = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM inquiries;")
            leads = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM quotations WHERE status = 'Approved';")
            deals = cur.fetchone()[0]

            return {
                "total_invoiced_ugx": total_inv,
                "total_collected_ugx": coll,
                "total_outstanding_ugx": outst,
                "active_projects": active_p,
                "leads_pipeline": leads,
                "deals_closed": deals
            }
