"""
HTTP Request Handler & Dispatcher with Complete ERP Operations
"""
import os
import sys
import mimetypes
from urllib.parse import urlparse, parse_qs, unquote
from http.server import BaseHTTPRequestHandler
from http.cookies import SimpleCookie
from datetime import datetime

import config
from core import auth, rbac, db
from integrations import sms
from templates import (
    public as public_tmpl,
    auth as auth_tmpl,
    desk as desk_tmpl,
    permissions as perm_tmpl,
    users as users_tmpl,
    sms_view as sms_tmpl,
    doctypes as doc_tmpl,
    finance_views as fin_tmpl,
    profile as profile_tmpl,
    base as base_tmpl
)

class ZurekaRequestHandler(BaseHTTPRequestHandler):

    def send_html(self, html: str, status: int = 200, cookie_set: str = None):
        body = html.encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', str(len(body)))
        if cookie_set:
            self.send_header('Set-Cookie', cookie_set)
        self.end_headers()
        self.wfile.write(body)

    def redirect(self, url: str, cookie_set: str = None):
        self.send_response(302)
        self.send_header('Location', url)
        if cookie_set:
            self.send_header('Set-Cookie', cookie_set)
        self.end_headers()

    def get_user(self):
        cookie_header = self.headers.get('Cookie')
        if not cookie_header:
            return None
        cookie = SimpleCookie()
        try:
            cookie.load(cookie_header)
            if 'zureka_session' in cookie:
                token = cookie['zureka_session'].value
                return auth.get_session_user(token)
        except Exception:
            pass
        return None

    def parse_post_data(self) -> dict:
        content_length = int(self.headers.get('Content-Length', 0))
        if content_length == 0:
            return {}
        post_body = self.rfile.read(content_length).decode('utf-8')
        parsed = parse_qs(post_body)
        return {k: v[0] if len(v) == 1 else v for k, v in parsed.items()}

    def do_GET(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query = parse_qs(parsed_url.query)

        # 1. Static Files (/public/...)
        if path.startswith('/public/'):
            rel_path = path[8:].lstrip('/')
            file_path = os.path.join(config.PUBLIC_DIR, rel_path)
            if os.path.exists(file_path) and os.path.isfile(file_path):
                mime, _ = mimetypes.guess_type(file_path)
                with open(file_path, 'rb') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-Type', mime or 'application/octet-stream')
                self.send_header('Content-Length', str(len(content)))
                self.end_headers()
                self.wfile.write(content)
                return
            self.send_error(404, "File Not Found")
            return

        # 2. Public Pages
        if path == '/':
            systems = db.get_systems()
            self.send_html(public_tmpl.render_home(systems))
            return

        elif path == '/systems':
            systems = db.get_systems()
            self.send_html(public_tmpl.render_public_systems(systems))
            return

        elif path == '/tailored-scope':
            sys_code = query.get('system', [''])[0]
            self.send_html(public_tmpl.render_tailored_scope_page(sys_code))
            return

        elif path == '/login':
            user = self.get_user()
            if user:
                self.redirect('/desk')
                return
            err = query.get('error', ['0'])[0] == '1'
            nxt = query.get('next', [''])[0]
            self.send_html(auth_tmpl.render_login(error=err, next_url=nxt))
            return

        elif path == '/logout':
            cookie_header = self.headers.get('Cookie')
            if cookie_header:
                cookie = SimpleCookie()
                try:
                    cookie.load(cookie_header)
                    if 'zureka_session' in cookie:
                        auth.destroy_session(cookie['zureka_session'].value)
                except Exception:
                    pass
            self.redirect('/login', cookie_set='zureka_session=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT')
            return

        # 3. Authenticated Desk Pages
        if path.startswith('/desk') or path.startswith('/portal'):
            user = self.get_user()
            if not user:
                self.redirect(f'/login?next={path}')
                return

            role = user.get('role', 'client')

            # Workspace Home
            if path in ['/desk', '/desk/', '/portal']:
                stats = db.get_stats(role, user['email'])
                self.send_html(desk_tmpl.render_desk_workspace(user, stats))
                return

            # User Profile Settings
            elif path in ['/desk/profile', '/portal/profile']:
                fresh_user = db.get_user_by_email(user['email']) or user
                updated = query.get('updated', ['0'])[0] == '1'
                p_success = query.get('pwd_success', ['0'])[0] == '1'
                p_error = query.get('pwd_error', ['0'])[0] == '1'
                self.send_html(profile_tmpl.render_profile_page(fresh_user, updated=updated, pwd_success=p_success, pwd_error=p_error))
                return

            # Quotations List & Detail
            elif path.startswith('/desk/quotations/') or path.startswith('/portal/quotations/'):
                if not rbac.has_permission(role, 'Quotation', 'read'):
                    self.send_html(base_tmpl.render_permission_denied(user, 'Quotation', 'read'), 403)
                    return
                quote_no = path.split('/')[-1]
                quote = db.get_quotation_by_no(quote_no)
                if not quote:
                    self.send_error(404, "Quotation Not Found")
                    return
                self.send_html(doc_tmpl.render_quotation_detail(user, quote))
                return

            elif path in ['/desk/quotations', '/portal/quotations']:
                if not rbac.has_permission(role, 'Quotation', 'read'):
                    self.send_html(base_tmpl.render_permission_denied(user, 'Quotation', 'read'), 403)
                    return
                quotes = db.get_quotations(role, user['email'])
                can_create = rbac.has_permission(role, 'Quotation', 'create')
                can_submit = rbac.has_permission(role, 'Quotation', 'submit')
                self.send_html(doc_tmpl.render_desk_quotations(user, quotes, can_create, can_submit))
                return

            # Sales Invoices List & Detail
            elif path.startswith('/desk/invoices/') or path.startswith('/portal/invoices/'):
                if not rbac.has_permission(role, 'Sales Invoice', 'read'):
                    self.send_html(base_tmpl.render_permission_denied(user, 'Sales Invoice', 'read'), 403)
                    return
                inv_no = path.split('/')[-1]
                inv = db.get_invoice_by_no(inv_no)
                if not inv:
                    self.send_error(404, "Invoice Not Found")
                    return
                gl_postings = db.get_gl_entries(voucher_no=inv_no)
                self.send_html(fin_tmpl.render_invoice_detail(user, inv, gl_postings))
                return

            elif path in ['/desk/invoices', '/portal/invoices']:
                if not rbac.has_permission(role, 'Sales Invoice', 'read'):
                    self.send_html(base_tmpl.render_permission_denied(user, 'Sales Invoice', 'read'), 403)
                    return
                invoices = db.get_invoices(role, user['email'])
                can_create = rbac.has_permission(role, 'Sales Invoice', 'create')
                self.send_html(fin_tmpl.render_invoice_list(user, invoices, can_create))
                return

            # General Ledger
            elif path in ['/desk/general-ledger', '/portal/general-ledger']:
                if not rbac.has_permission(role, 'General Ledger', 'read'):
                    self.send_html(base_tmpl.render_permission_denied(user, 'General Ledger', 'read'), 403)
                    return
                entries = db.get_gl_entries()
                self.send_html(fin_tmpl.render_general_ledger(user, entries))
                return

            # Chart of Accounts
            elif path in ['/desk/chart-of-accounts', '/portal/chart-of-accounts']:
                if not rbac.has_permission(role, 'Chart of Accounts', 'read'):
                    self.send_html(base_tmpl.render_permission_denied(user, 'Chart of Accounts', 'read'), 403)
                    return
                coa = db.get_chart_of_accounts()
                self.send_html(fin_tmpl.render_chart_of_accounts(user, coa))
                return

            # Payment Entries
            elif path in ['/desk/payments', '/portal/payments']:
                if not rbac.has_permission(role, 'Payment Entry', 'read'):
                    self.send_html(base_tmpl.render_permission_denied(user, 'Payment Entry', 'read'), 403)
                    return
                payments = db.get_payments(role, user['email'])
                can_create = rbac.has_permission(role, 'Payment Entry', 'create')
                self.send_html(fin_tmpl.render_payment_entries(user, payments, can_create))
                return

            # Delivery Projects
            elif path in ['/desk/projects', '/portal/projects']:
                if not rbac.has_permission(role, 'Delivery Project', 'read'):
                    self.send_html(base_tmpl.render_permission_denied(user, 'Delivery Project', 'read'), 403)
                    return
                projects = db.get_projects(role, user['email'])
                can_create = rbac.has_permission(role, 'Delivery Project', 'create')
                self.send_html(doc_tmpl.render_desk_projects(user, projects, can_create))
                return

            # CRM Clients
            elif path in ['/desk/clients', '/portal/clients']:
                if not rbac.has_permission(role, 'Customer', 'read'):
                    self.send_html(base_tmpl.render_permission_denied(user, 'Customer', 'read'), 403)
                    return
                clients = db.get_clients()
                can_create = rbac.has_permission(role, 'Customer', 'create')
                self.send_html(doc_tmpl.render_desk_clients(user, clients, can_create))
                return

            # Solutions (16 Systems)
            elif path in ['/desk/systems', '/portal/systems']:
                if not rbac.has_permission(role, 'Solution', 'read'):
                    self.send_html(base_tmpl.render_permission_denied(user, 'Solution', 'read'), 403)
                    return
                systems = db.get_systems()
                can_create = rbac.has_permission(role, 'Solution', 'create')
                self.send_html(doc_tmpl.render_desk_systems(user, systems, can_create))
                return

            # SMS Gateway
            elif path in ['/desk/sms', '/portal/sms']:
                if not rbac.has_permission(role, 'SMS Gateway', 'read'):
                    self.send_html(base_tmpl.render_permission_denied(user, 'SMS Gateway', 'read'), 403)
                    return
                logs = sms.get_sms_logs()
                cfg = sms.get_sms_config()
                can_broadcast = rbac.has_permission(role, 'SMS Gateway', 'broadcast')
                to_val = query.get('to', [''])[0]
                self.send_html(sms_tmpl.render_desk_sms(user, logs, cfg, can_broadcast, query.get('sent', ['0'])[0] == '1', default_to=to_val))
                return

            # RBAC Permissions Matrix
            elif path in ['/desk/permissions', '/portal/permissions']:
                if not rbac.has_permission(role, 'Role Permission', 'read'):
                    self.send_html(base_tmpl.render_permission_denied(user, 'Role Permission', 'read'), 403)
                    return
                matrix = rbac.get_role_permissions_matrix()
                self.send_html(perm_tmpl.render_desk_permissions(user, matrix))
                return

            # User Directory
            elif path in ['/desk/users', '/portal/users']:
                if not rbac.has_permission(role, 'User', 'read'):
                    self.send_html(base_tmpl.render_permission_denied(user, 'User', 'read'), 403)
                    return
                users = db.get_all_users()
                created = query.get('created', ['0'])[0] == '1'
                updated = query.get('updated', ['0'])[0] == '1'
                reset = query.get('reset', ['0'])[0] == '1'
                deleted = query.get('deleted', ['0'])[0] == '1'
                delete_error = query.get('delete_error', [''])[0]
                self.send_html(users_tmpl.render_desk_users(
                    user, users, created_notice=created, updated_notice=updated,
                    reset_notice=reset, deleted_notice=deleted, delete_error=delete_error
                ))
                return

        self.send_error(404, "Page Not Found")

    def do_POST(self):
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        user = self.get_user()
        data = self.parse_post_data()

        # Public Login
        if path == '/api/login':
            email = data.get('email', '')
            password = data.get('password', '')
            next_url = data.get('nextUrl', '')
            auth_user = db.authenticate_user(email, password)
            if not auth_user:
                self.redirect('/login?error=1' + (f'&next={next_url}' if next_url else ''))
                return
            token = auth.create_session(auth_user)
            db.log_activity(auth_user['email'], "User Signed In", f"User {auth_user['full_name']} ({auth_user['role']}) authenticated successfully.")
            cookie = f'zureka_session={token}; Path=/; HttpOnly; SameSite=Lax'
            self.redirect(next_url or '/desk', cookie_set=cookie)
            return

        # Public Discovery Inquiry
        elif path == '/api/inquiries':
            db.add_inquiry(data)
            try:
                sms.notify_new_inquiry(data)
            except Exception:
                pass
            msg = "<script>alert('Thank you! Your discovery request has been received. Our practice team will contact you shortly.'); window.location.href='/';</script>"
            self.send_html(msg)
            return

        # Protected Desk Actions
        if not user:
            self.redirect('/login')
            return

        role = user.get('role', 'client')

        # Profile Update
        if path == '/api/profile/update':
            updated_user = db.update_user_profile(user['email'], data)
            if updated_user:
                auth.update_session_user(user['email'], updated_user)
            self.redirect('/desk/profile?updated=1')
            return

        # Password Update
        elif path == '/api/profile/change-password':
            curr_pwd = data.get('current_password', '')
            new_pwd = data.get('new_password', '')
            conf_pwd = data.get('confirm_password', '')
            if not new_pwd or new_pwd != conf_pwd or len(new_pwd) < 6:
                self.redirect('/desk/profile?pwd_error=1')
                return
            success = db.update_user_password(user['email'], curr_pwd, new_pwd)
            if success:
                self.redirect('/desk/profile?pwd_success=1')
            else:
                self.redirect('/desk/profile?pwd_error=1')
            return

        # Create Quotation
        if path == '/api/quotations':
            if not rbac.has_permission(role, 'Quotation', 'create'):
                self.send_html(base_tmpl.render_permission_denied(user, 'Quotation', 'create'), 403)
                return
            sys_code = data.get('system_code')
            system = db.get_system_by_code(sys_code)
            data['system_name'] = system.get('name') if system else 'Enterprise Solution'
            quote = db.add_quotation(data)
            db.log_activity(user['email'], "Quotation Created", f"Drafted proposal {quote['quote_no']} for {quote['client_name']}")
            if quote.get('client_phone'):
                try:
                    sms.notify_quotation_created(quote)
                except Exception:
                    pass
            self.redirect('/desk/quotations?success=1')
            return

        # Approve Quotation
        elif path.startswith('/api/quotations/') and path.endswith('/approve'):
            if not rbac.has_permission(role, 'Quotation', 'submit'):
                self.send_html(base_tmpl.render_permission_denied(user, 'Quotation', 'submit'), 403)
                return
            parts = path.split('/')
            quote_no = parts[3]
            quote = db.approve_quotation(quote_no)
            db.log_activity(user['email'], "Quotation Approved", f"Proposal {quote_no} approved and signed off.")
            if quote and quote.get('client_phone'):
                try:
                    sms.send_sms(
                        quote['client_phone'],
                        f"ZUREKA: Proposal {quote['quote_no']} for {quote['system_name']} has been officially APPROVED. Project onboarding starting shortly. Info: +256 773 245 712."
                    )
                except Exception:
                    pass
            self.redirect('/desk/quotations?success=1')
            return

        # Convert Quotation to Invoice
        elif path.startswith('/api/quotations/') and path.endswith('/convert-invoice'):
            if not rbac.has_permission(role, 'Sales Invoice', 'create'):
                self.send_html(base_tmpl.render_permission_denied(user, 'Sales Invoice', 'create'), 403)
                return
            parts = path.split('/')
            quote_no = parts[3]
            inv = db.convert_quotation_to_invoice(quote_no, user['email'])
            self.redirect(f"/desk/invoices/{inv['invoice_no']}" if inv else "/desk/invoices")
            return

        # Convert Quotation to Project
        elif path.startswith('/api/quotations/') and path.endswith('/convert-project'):
            if not rbac.has_permission(role, 'Delivery Project', 'create'):
                self.send_html(base_tmpl.render_permission_denied(user, 'Delivery Project', 'create'), 403)
                return
            parts = path.split('/')
            quote_no = parts[3]
            proj = db.convert_quotation_to_project(quote_no, user['email'])
            self.redirect("/desk/projects")
            return

        # Create Invoice
        elif path == '/api/invoices':
            if not rbac.has_permission(role, 'Sales Invoice', 'create'):
                self.send_html(base_tmpl.render_permission_denied(user, 'Sales Invoice', 'create'), 403)
                return
            inv = db.add_invoice(data)
            db.log_activity(user['email'], "Invoice Created", f"Issued Sales Invoice {inv['invoice_no']} for UGX {inv['grand_total']:,.0f}")
            self.redirect(f"/desk/invoices/{inv['invoice_no']}")
            return

        # Record Payment Entry against Invoice
        elif path == '/api/payments':
            if not rbac.has_permission(role, 'Payment Entry', 'create'):
                self.send_html(base_tmpl.render_permission_denied(user, 'Payment Entry', 'create'), 403)
                return
            payment = db.make_payment_entry(data, user['email'])
            self.redirect(f"/desk/invoices/{data.get('invoice_no')}" if payment else "/desk/invoices")
            return

        # Update Project Stage
        elif path == '/api/projects/update':
            if not rbac.has_permission(role, 'Delivery Project', 'write'):
                self.send_html(base_tmpl.render_permission_denied(user, 'Delivery Project', 'write'), 403)
                return
            p_code = data.get('project_code')
            p_status = data.get('status')
            p_pct = data.get('completion_pct', 0)
            p_milestone = data.get('current_milestone', '')
            db.update_project_progress(p_code, p_status, p_pct, p_milestone, user['email'])
            self.redirect("/desk/projects")
            return

        # Send SMS Broadcast
        elif path == '/api/sms/send':
            if not rbac.has_permission(role, 'SMS Gateway', 'broadcast'):
                self.send_html(base_tmpl.render_permission_denied(user, 'SMS Gateway', 'broadcast'), 403)
                return
            sms.send_sms(data.get('to', ''), data.get('message', ''))
            db.log_activity(user['email'], "SMS Dispatched", f"Broadcasted message to {data.get('to')}")
            self.redirect('/desk/sms?sent=1')
            return

        # Create Customer
        elif path == '/api/clients':
            if not rbac.has_permission(role, 'Customer', 'create'):
                self.send_html(base_tmpl.render_permission_denied(user, 'Customer', 'create'), 403)
                return
            c = db.add_client(data)
            db.log_activity(user['email'], "Customer Created", f"Registered new client partner {c['name']}")
            self.redirect('/desk/clients?success=1')
            return

        # Create System
        elif path == '/api/systems':
            if not rbac.has_permission(role, 'Solution', 'create'):
                self.send_html(base_tmpl.render_permission_denied(user, 'Solution', 'create'), 403)
                return
            db.add_system(data)
            self.redirect('/desk/systems?success=1')
            return

        # Create User (Admin only)
        elif path == '/api/users':
            if role != 'admin' or not rbac.has_permission(role, 'User', 'create'):
                self.send_html(base_tmpl.render_permission_denied(user, 'User', 'create'), 403)
                return
            db.create_user(data, admin_email=user['email'])
            self.redirect('/desk/users?created=1')
            return

        # Update User (Admin only)
        elif path == '/api/users/update':
            if role != 'admin' or not rbac.has_permission(role, 'User', 'write'):
                self.send_html(base_tmpl.render_permission_denied(user, 'User', 'write'), 403)
                return
            target_email = data.get('target_email')
            db.admin_update_user(target_email, data, admin_email=user['email'])
            self.redirect('/desk/users?updated=1')
            return

        # Reset Password (Admin only)
        elif path == '/api/users/reset-password':
            if role != 'admin' or not rbac.has_permission(role, 'User', 'write'):
                self.send_html(base_tmpl.render_permission_denied(user, 'User', 'write'), 403)
                return
            target_email = data.get('target_email')
            new_pwd = data.get('new_password', '')
            if new_pwd and len(new_pwd) >= 6:
                db.admin_reset_password(target_email, new_pwd, admin_email=user['email'])
                self.redirect('/desk/users?reset=1')
            else:
                self.redirect('/desk/users?error=1')
            return

        # Delete User (Admin only)
        elif path == '/api/users/delete':
            if role != 'admin' or not rbac.has_permission(role, 'User', 'write'):
                self.send_html(base_tmpl.render_permission_denied(user, 'User', 'write'), 403)
                return

            target_email = data.get('target_email', '').strip()
            result = db.delete_user_account(target_email, user['email'])
            if result == "deleted":
                auth.destroy_sessions_for_user(target_email)
                self.redirect('/desk/users?deleted=1')
            else:
                self.redirect(f'/desk/users?delete_error={result}')
            return

        self.send_error(404, "Endpoint Not Found")

    def log_message(self, format, *args):
        try:
            sys.stderr.write(f"[{datetime.now().strftime('%H:%M:%S')}] {self.address_string()} - {format % args}\n")
        except Exception:
            pass
