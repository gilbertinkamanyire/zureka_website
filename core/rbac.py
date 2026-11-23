"""
Role-Based Access Control (RBAC) & ERPNext DocType Permissions Matrix
"""
from typing import Dict, List, Any

ROLES = {
    'admin': {
        'name': 'System Manager (Administrator)',
        'description': 'Full administrative control, role assignment, system architecture & master records',
        'badge': 'Administrator'
    },
    'lead_erp': {
        'name': 'Practice Lead - Enterprise Solutions',
        'description': 'Full ownership of ERPNext, Odoo, SAP B1 delivery & proposal generation',
        'badge': 'Practice Lead'
    },
    'lead_data': {
        'name': 'Practice Lead - Data, Intelligence & AI',
        'description': 'PostgreSQL, BI, analytics, integrations & predictive intelligence',
        'badge': 'Practice Lead'
    },
    'lead_opex': {
        'name': 'Practice Lead - Operational Excellence',
        'description': 'Business process re-engineering, standard operating procedures, ISO alignment',
        'badge': 'Practice Lead'
    },
    'sales': {
        'name': 'Business Development & Sales Consultant',
        'description': 'Discovery inquiries, customer relationships, tailored proposals & quotation submissions',
        'badge': 'Sales & CRM'
    },
    'finance': {
        'name': 'Finance & Billing Controller',
        'description': 'General Ledger, Chart of Accounts, payment entries, tax invoicing & commercial audits',
        'badge': 'Finance'
    },
    'client': {
        'name': 'Client Portal User',
        'description': 'Customer workspace: view issued proposals, milestone tracking & approved invoices',
        'badge': 'Client Portal'
    }
}

DOCTYPES = [
    'Solution',
    'Inquiry',
    'Quotation',
    'Sales Invoice',
    'Payment Entry',
    'General Ledger',
    'Chart of Accounts',
    'Delivery Project',
    'Customer',
    'SMS Gateway',
    'Role Permission',
    'User'
]

# Permissions: read, create, write, submit, cancel, broadcast
ROLE_PERMISSIONS: Dict[str, Dict[str, List[str]]] = {
    'admin': {
        'Solution': ['read', 'create', 'write', 'submit', 'cancel'],
        'Inquiry': ['read', 'create', 'write', 'submit'],
        'Quotation': ['read', 'create', 'write', 'submit', 'cancel'],
        'Sales Invoice': ['read', 'create', 'write', 'submit', 'cancel'],
        'Payment Entry': ['read', 'create', 'write', 'submit', 'cancel'],
        'General Ledger': ['read', 'create', 'write'],
        'Chart of Accounts': ['read', 'create', 'write'],
        'Delivery Project': ['read', 'create', 'write', 'submit', 'cancel'],
        'Customer': ['read', 'create', 'write', 'submit', 'cancel'],
        'SMS Gateway': ['read', 'broadcast'],
        'Role Permission': ['read', 'write'],
        'User': ['read', 'create', 'write']
    },
    'lead_erp': {
        'Solution': ['read', 'create', 'write', 'submit'],
        'Inquiry': ['read', 'create', 'write'],
        'Quotation': ['read', 'create', 'write', 'submit'],
        'Sales Invoice': ['read'],
        'Payment Entry': ['read'],
        'General Ledger': ['read'],
        'Chart of Accounts': ['read'],
        'Delivery Project': ['read', 'create', 'write', 'submit'],
        'Customer': ['read', 'create', 'write'],
        'SMS Gateway': ['read', 'broadcast'],
        'Role Permission': ['read'],
        'User': ['read']
    },
    'lead_data': {
        'Solution': ['read', 'create', 'write', 'submit'],
        'Inquiry': ['read', 'create', 'write'],
        'Quotation': ['read', 'create', 'write', 'submit'],
        'Sales Invoice': ['read'],
        'Payment Entry': ['read'],
        'General Ledger': ['read'],
        'Chart of Accounts': ['read'],
        'Delivery Project': ['read', 'create', 'write', 'submit'],
        'Customer': ['read', 'create', 'write'],
        'SMS Gateway': ['read', 'broadcast'],
        'Role Permission': ['read'],
        'User': ['read']
    },
    'lead_opex': {
        'Solution': ['read', 'create', 'write', 'submit'],
        'Inquiry': ['read', 'create', 'write'],
        'Quotation': ['read', 'create', 'write', 'submit'],
        'Sales Invoice': ['read'],
        'Payment Entry': ['read'],
        'General Ledger': ['read'],
        'Chart of Accounts': ['read'],
        'Delivery Project': ['read', 'create', 'write', 'submit'],
        'Customer': ['read', 'create', 'write'],
        'SMS Gateway': ['read', 'broadcast'],
        'Role Permission': ['read'],
        'User': ['read']
    },
    'sales': {
        'Solution': ['read'],
        'Inquiry': ['read', 'create', 'write', 'submit'],
        'Quotation': ['read', 'create', 'write', 'submit'],
        'Sales Invoice': [],
        'Payment Entry': [],
        'General Ledger': [],
        'Chart of Accounts': [],
        'Delivery Project': ['read'],
        'Customer': ['read', 'create', 'write'],
        'SMS Gateway': ['read', 'broadcast'],
        'Role Permission': [],
        'User': []
    },
    'finance': {
        'Solution': ['read'],
        'Inquiry': ['read'],
        'Quotation': ['read'],
        'Sales Invoice': ['read', 'create', 'write', 'submit', 'cancel'],
        'Payment Entry': ['read', 'create', 'write', 'submit', 'cancel'],
        'General Ledger': ['read', 'create'],
        'Chart of Accounts': ['read', 'create', 'write'],
        'Delivery Project': ['read'],
        'Customer': ['read', 'create'],
        'SMS Gateway': ['read'],
        'Role Permission': [],
        'User': []
    },
    'client': {
        'Solution': ['read'],
        'Inquiry': ['read', 'create'],
        'Quotation': ['read'],
        'Sales Invoice': ['read'],
        'Payment Entry': ['read'],
        'General Ledger': [],
        'Chart of Accounts': [],
        'Delivery Project': ['read'],
        'Customer': ['read'],
        'SMS Gateway': [],
        'Role Permission': [],
        'User': []
    }
}

def has_permission(role: str, doctype: str, action: str) -> bool:
    """Evaluate whether a role has permission for a specific action on a DocType."""
    if not role or role not in ROLE_PERMISSIONS:
        return False
    perms = ROLE_PERMISSIONS[role].get(doctype, [])
    return action in perms

def get_role_label(role: str) -> str:
    """Return friendly title of role."""
    return ROLES.get(role, {}).get('name', role.replace('_', ' ').title())

def get_role_badge(role: str) -> str:
    """Return badge text of role."""
    return ROLES.get(role, {}).get('badge', role.title())

def get_role_permissions_matrix() -> List[Dict[str, Any]]:
    """Format full RBAC matrix for ERPNext Desk permissions inspector."""
    matrix = []
    actions = ['read', 'create', 'write', 'submit', 'cancel', 'broadcast']
    for doctype in DOCTYPES:
        row = {'doctype': doctype, 'roles': {}}
        for role_key in ROLES:
            role_perms = ROLE_PERMISSIONS.get(role_key, {}).get(doctype, [])
            row['roles'][role_key] = {act: (act in role_perms) for act in actions}
        matrix.append(row)
    return matrix
