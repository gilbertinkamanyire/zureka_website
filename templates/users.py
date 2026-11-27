"""
User Directory & Role Assignment View (Admin-Governed Account Creation & Credential Management)
"""
from html import escape
from typing import List
from templates.base import render_desk_base
from core.rbac import get_role_label, get_role_badge, ROLES

def render_desk_users(
    user: dict,
    users: List[dict],
    created_notice: bool = False,
    updated_notice: bool = False,
    reset_notice: bool = False,
    deleted_notice: bool = False,
    delete_error: str = ""
) -> str:
    is_admin = (user.get('role') == 'admin')
    current_email = user.get('email', '').strip().lower()
    admin_count = sum(1 for account in users if str(account.get('role', '')).lower() == 'admin')

    notice_html = ""
    delete_errors = {
        "self": "You cannot delete your own administrator account.",
        "last_admin": "The last administrator account cannot be deleted.",
        "not_found": "The selected user account was not found."
    }
    if delete_error in delete_errors:
        notice_html = f"""
        <div role="alert" style="background: #FEF2F2; border: 1px solid #FECACA; color: #991B1B; padding: 12px 18px; border-radius: 8px; font-size: 13.5px; font-weight: 600; margin-bottom: 24px;">
          {delete_errors[delete_error]}
        </div>
        """
    elif created_notice:
        notice_html = """
        <div style="background: #DCFCE7; border: 1px solid #86EFAC; color: #166534; padding: 12px 18px; border-radius: 8px; font-size: 13.5px; font-weight: 600; margin-bottom: 24px;">
          ✓ New user account successfully created! The user can now authenticate with their assigned role.
        </div>
        """
    elif updated_notice:
        notice_html = """
        <div style="background: #DCFCE7; border: 1px solid #86EFAC; color: #166534; padding: 12px 18px; border-radius: 8px; font-size: 13.5px; font-weight: 600; margin-bottom: 24px;">
          ✓ User account details and security credentials successfully updated.
        </div>
        """
    elif reset_notice:
        notice_html = """
        <div style="background: #DCFCE7; border: 1px solid #86EFAC; color: #166534; padding: 12px 18px; border-radius: 8px; font-size: 13.5px; font-weight: 600; margin-bottom: 24px;">
          ✓ User password successfully reset by Administrator.
        </div>
        """
    elif deleted_notice:
        notice_html = """
        <div role="status" style="background: #DCFCE7; border: 1px solid #86EFAC; color: #166534; padding: 12px 18px; border-radius: 8px; font-size: 13.5px; font-weight: 600; margin-bottom: 24px;">
          ✓ User account permanently deleted.
        </div>
        """

    rows = ""
    for u in users:
        role = u.get('role', 'client')
        status = u.get('status', 'Active')
        status_cls = 'indicator-paid' if status == 'Active' else 'indicator-draft'
        email = str(u.get('email', ''))

        admin_action = ""
        if is_admin:
            delete_action = ""
            can_delete = (
                email.strip().lower() != current_email
                and not (str(role).lower() == 'admin' and admin_count <= 1)
            )
            if can_delete:
                delete_action = f"""
                <form action="/api/users/delete" method="POST" style="display: inline;" onsubmit="return confirm('Delete this account permanently? This cannot be undone.');">
                  <input type="hidden" name="target_email" value="{escape(email, quote=True)}">
                  <button type="submit" class="btn btn-sm" style="background: #DC2626; color: #FFFFFF; white-space: nowrap; font-size: 12px; padding: 6px 14px;">
                    🗑 Delete
                  </button>
                </form>
                """
            admin_action = f"""
            <button type="button" class="btn btn-navy btn-sm" onclick="openEditUserModal('{u.get('email')}', '{u.get('full_name')}', '{u.get('role')}', '{u.get('title', '')}', '{u.get('department', '')}', '{u.get('phone', '')}', '{status}')" style="white-space: nowrap; font-size: 12px; padding: 6px 14px;">
              ✏️ Edit
            </button>
            {delete_action}
            """

        rows += f"""
        <tr>
          <td>
            <div style="display: flex; align-items: center; gap: 10px;">
              <div class="desk-avatar" style="width: 32px; height: 32px; font-size: 13px;">{u.get('avatar', 'U')}</div>
              <div>
                <div style="font-weight: 700; color: #0F172A;">{u.get('full_name')}</div>
                <div style="font-size: 12px; color: #64748B;">{u.get('email')}</div>
              </div>
            </div>
          </td>
          <td>
            <span class="z-badge" style="background: var(--z-gold-light); color: var(--z-gold-dark); font-weight: 800;">
              {get_role_badge(role)}
            </span>
          </td>
          <td style="font-size: 12.5px; color: #334155; font-weight: 600;">{u.get('title', 'N/A')}</td>
          <td style="font-size: 12.5px; color: #475569;">{u.get('department', 'Zureka Solutions')}</td>
          <td style="font-size: 12.5px; color: #0F172A; font-weight: 600;">{u.get('phone', 'N/A')}</td>
          <td>
            <span class="indicator-pill {status_cls}">
              <span class="indicator-dot"></span>
              {status}
            </span>
          </td>
          {f'<td style="text-align: right; white-space: nowrap;">{admin_action}</td>' if is_admin else ''}
        </tr>
        """

    # Admin Modals
    role_options = ""
    for r_key, r_info in ROLES.items():
        role_options += f"<option value='{r_key}'>{r_info['badge']} &bull; {r_info['name']}</option>"

    create_user_modal = f"""
    <!-- Create User Modal (Admin Exclusive) -->
    <div id="createUserModal" class="modal-overlay">
      <div class="modal-card">
        <div class="modal-header">
          <div class="modal-title">Create User Account (System Administrator)</div>
          <button class="modal-close" onclick="closeModal('createUserModal')">&times;</button>
        </div>
        <form action="/api/users" method="POST">
          <div class="modal-body">
            <div style="background: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 12px 16px; margin-bottom: 18px; font-size: 12.5px; color: #1E40AF;">
              <strong>🛡️ Governance Notice:</strong> User accounts are strictly created and provisioned by the System Administrator. The user will be assigned permissions in the RBAC matrix according to their selected role.
            </div>

            <div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 16px; margin-bottom: 16px;">
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Full Name *</label>
                <input type="text" name="full_name" required placeholder="e.g. Sarah Nabwire" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Corporate Email *</label>
                <input type="email" name="email" required placeholder="sarah@zurekasolutions.com" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Initial Password *</label>
                <input type="password" name="password" required minlength="6" placeholder="••••••••" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Phone (for Pandora SMS) *</label>
                <input type="text" name="phone" required placeholder="+256 772 000 000" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
            </div>

            <div style="margin-bottom: 16px;">
              <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Assigned RBAC Role *</label>
              <select name="role" required style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
                {role_options}
              </select>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Job Title</label>
                <input type="text" name="title" placeholder="e.g. Senior ERPNext Consultant" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Practice / Department</label>
                <input type="text" name="department" placeholder="e.g. Enterprise Solutions Practice" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline" onclick="closeModal('createUserModal')">Cancel</button>
            <button type="submit" class="btn btn-gold">Create Account & Provision Role &rarr;</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Edit User Modal (Admin Exclusive) -->
    <div id="editUserModal" class="modal-overlay">
      <div class="modal-card" style="max-width: 620px;">
        <div class="modal-header">
          <div class="modal-title">Edit User Details & Password</div>
          <button class="modal-close" onclick="closeModal('editUserModal')">&times;</button>
        </div>
        <form action="/api/users/update" method="POST">
          <input type="hidden" id="editEmail" name="target_email">
          <div class="modal-body">
            <div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 16px; margin-bottom: 16px;">
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Full Name *</label>
                <input type="text" id="editFullName" name="full_name" required style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Corporate Email *</label>
                <input type="email" id="editNewEmail" name="new_email" required style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1.2fr 1fr; gap: 16px; margin-bottom: 16px;">
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">RBAC Role *</label>
                <select id="editRole" name="role" required style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
                  {role_options}
                </select>
              </div>
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Status *</label>
                <select id="editStatus" name="status" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
                  <option value="Active">Active</option>
                  <option value="Disabled">Disabled</option>
                </select>
              </div>
            </div>

            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 16px;">
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Job Title</label>
                <input type="text" id="editTitle" name="title" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
              <div>
                <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Department</label>
                <input type="text" id="editDept" name="department" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
              </div>
            </div>

            <div style="margin-bottom: 16px;">
              <label style="display: block; font-size: 12px; font-weight: 700; color: #334155; margin-bottom: 4px;">Phone (SMS Alerts)</label>
              <input type="text" id="editPhone" name="phone" style="width: 100%; padding: 8px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px;">
            </div>

            <!-- Embedded Password Change Section -->
            <div style="background: #F8FAFC; border: 1px solid #CBD5E1; border-radius: 8px; padding: 16px; margin-top: 18px;">
              <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
                <span style="font-size: 13px; font-weight: 800; color: #0F172A; display: flex; align-items: center; gap: 6px;">
                  🔑 Change / Reset Password
                </span>
                <span style="font-size: 11px; color: #64748B; font-weight: 600;">Optional</span>
              </div>
              <p style="font-size: 12px; color: #64748B; margin-bottom: 10px;">
                Type a new password below to reset this user's password immediately. Leave empty to keep their existing password.
              </p>
              <div>
                <input type="password" id="editNewPassword" name="new_password" minlength="6" placeholder="Enter new password (min. 6 characters)" style="width: 100%; padding: 9px 12px; border: 1px solid var(--z-border); border-radius: 6px; font-size: 13px; background: #FFFFFF;">
              </div>
            </div>

          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline" onclick="closeModal('editUserModal')">Cancel</button>
            <button type="submit" class="btn btn-gold">Save Changes & Password &rarr;</button>
          </div>
        </form>
      </div>
    </div>

    <script>
    function openEditUserModal(email, name, role, title, dept, phone, status) {{
      document.getElementById('editEmail').value = email;
      document.getElementById('editNewEmail').value = email;
      document.getElementById('editFullName').value = name;
      document.getElementById('editRole').value = role;
      document.getElementById('editTitle').value = title;
      document.getElementById('editDept').value = dept;
      document.getElementById('editPhone').value = phone;
      document.getElementById('editStatus').value = status;
      const pwdEl = document.getElementById('editNewPassword');
      if (pwdEl) pwdEl.value = '';
      openModal('editUserModal');
    }}
    </script>
    """ if is_admin else ""

    content = f"""
    <div class="erp-header">
      <div>
        <h1 class="erp-title">User Directory & Roles</h1>
        <div class="erp-subtitle">System identity accounts, practice lead assignments, and RBAC governance</div>
      </div>
      <div class="erp-actions">
        {f'<button class="btn btn-gold" onclick="openModal(\'createUserModal\')">+ Create User Account</button>' if is_admin else '<span style="font-size: 12.5px; color: #64748B;">Admin-governed provisioning</span>'}
      </div>
    </div>

    {notice_html}

    <div class="table-wrap" style="overflow-x: auto;">
      <table class="z-table">
        <thead>
          <tr>
            <th>User & Identity</th>
            <th>RBAC Role</th>
            <th>Title / Designation</th>
            <th>Department / Practice</th>
            <th>Phone</th>
            <th>Status</th>
            {f'<th style="text-align: right; min-width: 100px;">Actions</th>' if is_admin else ''}
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </div>

    {create_user_modal}
    """
    return render_desk_base("User Directory", user, content, active_tab='users', breadcrumbs=[("Administration", None), ("User Directory", None)])
