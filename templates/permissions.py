"""
RBAC Role Permissions Manager View (ERPNext Style)
"""
from typing import List, Dict, Any
from templates.base import render_desk_base
from core.rbac import ROLES

def render_desk_permissions(user: dict, matrix: List[Dict[str, Any]]) -> str:
    role_headers = "".join([f"<th style='text-align: center;'>{ROLES[r]['badge']}</th>" for r in ROLES])

    rows = ""
    for item in matrix:
        doctype = item['doctype']
        role_cells = ""
        for role_key in ROLES:
            perms = item['roles'].get(role_key, {})
            badges = []
            if perms.get('read'): badges.append("<span style='color: #166534; font-weight: 700; font-size: 11px;'>Read</span>")
            if perms.get('create'): badges.append("<span style='color: #1E40AF; font-weight: 700; font-size: 11px;'>Create</span>")
            if perms.get('write'): badges.append("<span style='color: #854D0E; font-weight: 700; font-size: 11px;'>Write</span>")
            if perms.get('submit'): badges.append("<span style='color: #6B21A8; font-weight: 700; font-size: 11px;'>Submit</span>")
            if perms.get('cancel'): badges.append("<span style='color: #991B1B; font-weight: 700; font-size: 11px;'>Cancel</span>")
            if perms.get('broadcast'): badges.append("<span style='color: #C59B27; font-weight: 700; font-size: 11px;'>Broadcast</span>")

            cell_content = "<br>".join(badges) if badges else "<span style='color: #CBD5E1;'>&mdash;</span>"
            role_cells += f"<td style='text-align: center; vertical-align: top; padding: 10px 8px; font-size: 11.5px;'>{cell_content}</td>"

        rows += f"""
        <tr>
          <td style='font-weight: 800; color: #0F172A;'>{doctype}</td>
          {role_cells}
        </tr>
        """

    content = f"""
    <div style="margin-bottom: 24px;">
      <span style="color: var(--z-gold); font-size: 12px; font-weight: 800; text-transform: uppercase; letter-spacing: 0.8px;">System Governance</span>
      <h1 style="font-size: 24px; font-weight: 800; color: #0F172A; margin-top: 4px;">Role Permissions Manager (RBAC Matrix)</h1>
      <p style="color: #64748B; font-size: 13.5px;">
        Granular permission matrix across DocTypes. Unauthorized attempts trigger HTTP 403 enforcement.
      </p>
    </div>

    <div class="table-wrap">
      <table class="z-table">
        <thead>
          <tr>
            <th style="width: 180px;">DocType</th>
            {role_headers}
          </tr>
        </thead>
        <tbody>
          {rows}
        </tbody>
      </table>
    </div>
    """
    return render_desk_base("Role Permissions Manager", user, content, active_tab='permissions')
