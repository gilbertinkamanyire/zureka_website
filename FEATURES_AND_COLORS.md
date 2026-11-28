# Zureka Solutions Limited — ERPNext Desk
## Application Design System, Color Palette & Features Specification

> **Platform Version:** 2.0  
> **Architecture:** Modular Python Standard Library Backend with Dual Storage Engine (PostgreSQL / JSON Store)  
> **Target Deployment:** Render Cloud / On-Premise Ubuntu / Windows Server  
> **Brand Identity:** Enterprise Digital Transformation & ERP Solutions  

---

## 1. Color Palette & Visual Design System

The application uses an enterprise-grade color hierarchy inspired by ERPNext and modern fintech dashboards, balancing a commanding midnight navy with a prestigious warm gold accent and clear semantic feedback colors.

### 1.1 Brand & Core Palette

| Variable Name | Hex Code | RGB | Role / Usage |
| :--- | :--- | :--- | :--- |
| `--z-navy` | `#0F172A` | `rgb(15, 23, 42)` | **Primary Brand Color**: Navbar background, modal titles, primary headings (`h1`, `h2`), desk branding text. |
| `--z-navy-light` | `#1E293B` | `rgb(30, 41, 59)` | **Elevated Dark Surface**: Awesomebar search background, dark buttons hover state, table head text emphasis. |
| `--z-navy-dark` | `#0B1120` | `rgb(11, 17, 32)` | **Deep Background**: Topbar strip, login screen backdrop canvas, high-contrast modal backdrops. |
| `--z-gold` | `#C59B27` | `rgb(197, 155, 39)` | **Primary Accent**: Core call-to-action buttons (`.btn-gold`), active navigation indicators, logo accent, navbar bottom border. |
| `--z-gold-light` | `#FBF4DC` | `rgb(251, 244, 220)` | **Gold Tint**: Admin badge backgrounds, highlighted quotation values, card selection accents. |
| `--z-gold-dark` | `#9A7513` | `rgb(154, 117, 19)` | **Gold Shadow & Hover**: Pressed states for gold CTA buttons, focused border highlights. |

### 1.2 Semantic & Status Indicators

The platform adheres to standardized ERP status conventions (Draft, Submitted, Paid, Unpaid, Approved, Overdue):

| Status / Role | Background Hex | Text Hex | Accent Dot Hex | Semantic Meaning |
| :--- | :--- | :--- | :--- | :--- |
| **Paid / Approved / Completed** | `#DCFCE7` | `#166534` | `#16A34A` | Fully settled invoices, signed-off proposals, delivered projects. |
| **Unpaid / Submitted** | `#DBEAFE` | `#1E40AF` | `#2563EB` | Official invoices pending settlement, submitted vouchers. |
| **Draft / Pending** | `#F1F5F9` | `#475569` | `#94A3B8` | Proposals and records undergoing initial authoring. |
| **Overdue / Cancelled / Error** | `#FEE2E2` | `#991B1B` | `#DC2626` | Overdue receivables, voided transactions, alert messages. |
| **Practice Lead: Data & AI** | `#FAF5FF` | `#6B21A8` | `#9333EA` | Fiona Atuhaire persona badges and data pillar indicators. |
| **Practice Lead: OpEx** | `#FEF3C7` | `#92400E` | `#D97706` | Dennis Mugisha persona badges and governance tags. |

### 1.3 Neutrals, Typography & Canvas Surfaces

| Variable / Token | Hex Code | Purpose |
| :--- | :--- | :--- |
| Canvas Background (`--z-bg`) | `#F8FAFC` | Main Desk body canvas, secondary container fills, table alternating hover rows. |
| Surface White | `#FFFFFF` | Form cards, modal containers, data tables, active sidebar item backgrounds. |
| Border Default (`--z-border`) | `#E2E8F0` | Clean container dividers, input field outlines, card borders. |
| Border Subtle (`--z-border-subtle`) | `#F1F5F9` | Inner table cell borders, section separators. |
| Text Primary | `#0F172A` | Core body content, data values, table text, user titles. |
| Text Secondary (`--z-slate`) | `#64748B` | Helper captions, breadcrumbs, timestamps, subtitle notes. |
| Text Muted | `#94A3B8` | Input placeholder labels, inactive icons, keyboard shortcut tags (`<kbd>`). |

### 1.4 Shadows & Transitions

- **Card Shadow:** `0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)`
- **Card Hover Shadow:** `0 10px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)`
- **Modal Pop Animation:** `transform: scale(0.95) -> scale(1)` with cubic-bezier timing (`0.2s`)
- **Transitions:** `all 0.2s cubic-bezier(0.4, 0, 0.2, 1)`

---

## 2. Complete Application Features Specification

The platform is divided into two major layers: the **Public Commercial Portal** and the authenticated **ERPNext Enterprise Desk**.

---

### 2.1 Core Architecture & Deployment Capabilities

1. **Zero External Python Dependencies (Core Standard Library):**
   - Built natively on Python `http.server.ThreadingHTTPServer`, utilizing standard library modules (`os`, `json`, `datetime`, `urllib.parse`, `hashlib`, `mimetypes`, `http.cookies`).
   - Runs fast with immediate cold-starts (< 200ms) on Render or bare-metal servers.
2. **Dual-Mode Storage Engine (PostgreSQL / JSON Store):**
   - **PostgreSQL Mode:** When `DATABASE_URL` is configured, all transactions execute against PostgreSQL tables (`users`, `accounts`, `gl_entries`, `invoices`, `payments`, `projects`, `quotations`, `clients`, `inquiries`, `systems`, `activity_logs`).
   - **Render-Proofing:** Automatically rewrites Render's legacy `postgres://` connection string prefix to `postgresql://` for `psycopg2`.
   - **Offline / Local Fallback:** In the absence of a database connection, the application seamlessly uses `offline_store.json` without failing.
   - **Auto-Migration & Seeding:** PostgreSQL automatically creates all relational tables and seeds existing records from JSON on initial boot.
3. **Environment & Configuration:**
   - Pure Python `.env` file parser supporting Render production environment variables (`PORT`, `DATABASE_URL`, SMS API credentials).

---

### 2.2 Security, Authentication & Role-Based Access Control (RBAC)

1. **Authentication Engine:**
   - SHA-256 salted password hashing (`core/auth.py`).
   - Secure HTTP session management via `zureka_session` cookies with `HttpOnly` and `SameSite=Lax` protection.
   - Profile management enabling users to update personal details, job titles, and change their own password.
2. **Strict RBAC Enforcement:**
   - 6 Standard System Roles:
     - `admin`: Full system governance, user directory management, and financial oversight.
     - `lead_erp`: Practice Lead for ERPNext, Odoo, SAP B1 delivery and proposals.
     - `lead_data`: Practice Lead for Data Engineering, BI, and AI platforms.
     - `lead_opex`: Practice Lead for Business Process Re-engineering and Governance.
     - `sales`: Business development, quotation creation, and client pipeline management.
     - `finance`: Billing, invoice generation, payment receipts, Chart of Accounts, and General Ledger.
     - `client`: Client portal access restricted strictly to their organization's own invoices, statements, and projects.
3. **Dynamic Sidebar & View Filtering:**
   - Navigation links are rendered dynamically according to role permissions; unauthorized links are hidden from the user's interface.
   - Direct URL access to unauthorized resources triggers an ERP-styled `403 Permission Denied` screen.
4. **Administrator User Directory:**
   - Provisioning new user accounts with automated role assignment.
   - In-modal user editing (full name, email, department, phone, title, role, status).
   - In-modal password resets with minimum security length validation.
   - Self-deletion protection (administrators cannot accidentally delete their own active account).

---

### 2.3 Financial Accounting & General Ledger (ERP Core)

1. **Chart of Accounts (COA):**
   - Uganda-compliant Chart of Accounts structure with Root Types:
     - **Assets:** Stanbic Bank Uganda (UGX Operating), MTN Mobile Money Corporate Merchant, Accounts Receivable (Debtors).
     - **Liabilities:** Accounts Payable (Creditors), URA VAT Payable (18%), Withholding Tax (WHT 6%) Payable.
     - **Equity:** Partner Capital & Retained Earnings.
     - **Income:** ERPNext Consulting Revenue, Data & AI Revenue, SLA Support & Cloud Hosting Revenue.
     - **Expenses:** Cloud Infrastructure & Server Hosting Expense, Engineering Compensation.
2. **Double-Entry General Ledger (`gl_entries`):**
   - Every invoice and payment automatically posts balanced debit and credit entries to the General Ledger.
   - Real-time balance recalculation across affected accounts.
   - Audit trail tracking Voucher Type, Voucher No, Posting Date, Party, Debit, Credit, and Remarks.
3. **Sales Invoices & Taxation:**
   - Automated invoice numbering (`ZUR-INV-YYYY-XXXX`).
   - Uganda Revenue Authority (URA) 18% Output VAT calculation and simulated EFRIS Fiscal Document Numbers (`ZUR-EFRIS-YYYY-XXXXXX`).
   - Automatically posts:
     - **Debit:** Accounts Receivable (Grand Total)
     - **Credit:** Consulting Revenue (Subtotal)
     - **Credit:** URA VAT Payable (18% VAT Amount)
4. **Payment Receipts & Reconciliations:**
   - Recording incoming client payments against outstanding invoices.
   - Mode of payment selection (Stanbic Bank Wire Transfer or MTN Mobile Money).
   - Automatic posting to Bank (Debit) and clearing of Accounts Receivable (Credit).
   - Dynamic invoice status updating (`Unpaid` -> `Paid` or partial balance reduction).

---

### 2.4 Sales, Proposals & Client Relationship Management (CRM)

1. **Solutions Catalog (16 Enterprise Systems):**
   - **Enterprise Solutions (ERP):** ERPNext Core, Frappe Suite, Odoo Enterprise, SAP Business One, Microsoft Dynamics 365 Business Central.
   - **Data, Intelligence & AI:** PostgreSQL High-Availability Data Warehouse, Supabase Backend, Metabase BI, Apache Superset, Custom AI & Predictive Intelligence Engines.
   - **Operational Excellence:** Camunda BPM, ProcessMaker, n8n Enterprise Workflow Automation, Paperless-ngx DMS, Snipe-IT Asset Management, ERPNext Quality Management.
2. **Tailored Quotations & Proposals:**
   - Generation of tailored scope quotations (`ZUR-QT-YYYY-XXXX`) tied to catalog systems.
   - Value estimation (UGX), implementation timeline (weeks), and scope documentation.
   - **Proposal Approval Workflow:** 1-Click approval action transitioning proposal to `Approved`.
   - **1-Click Conversion Pipeline:**
     - *Convert to Invoice:* Automatically creates a 40% Mobilization Sales Invoice.
     - *Convert to Project:* Automatically spins up an Active Delivery Project under the respective Practice Lead.
3. **Client Directory:**
   - Management of client enterprises, primary contact persons, industry classification, phone numbers, and deployed system stacks.

---

### 2.5 Project Delivery & Implementation Tracking

1. **Project Delivery Console (`PRJ-XXX`):**
   - Tracks project code, client organization, appointed Practice Lead, framework stage, and completion percentage.
   - Interactive modal to advance project stages (*Planning & Discovery*, *Architecture Design*, *Pilot Deployment*, *UAT & Training*, *Go-Live*).
   - Logs every milestone update to the central activity audit trail.

---

### 2.6 Pandora Networks SMS Gateway Integration

1. **Ugandan Telecommunications SMS Integration:**
   - Connected to **Pandora Networks SMS Gateway** (`sms.thepandoranetworks.com`).
   - Standardized Ugandan phone number sanitization (normalizes `07XX...` and `+256...` to international format `2567XXXXXXXX`).
2. **Automated Event Triggers:**
   - **New Inquiries:** Automated administrative alert sent to practice directors when a client requests discovery scoping.
   - **Quotation Drafted:** Instant SMS notification to client contact with proposal reference.
   - **Quotation Approved:** Milestone confirmation dispatched to client management.
3. **SMS Gateway Console:**
   - Direct SMS broadcast tool for client alerts.
   - Dispatch logs table tracking recipient, timestamp, message payload, and gateway delivery status.

---

### 2.7 Executive Dashboard & Audit Logging

1. **Executive Key Metrics:**
   - Real-time tally of Total Invoiced (UGX), Total Collected (UGX), and Total Outstanding Receivables (UGX).
   - Counter metrics for Active Delivery Projects, Approved Quotations, Systems, and Client Accounts.
2. **Activity Audit Trail (`ACT-XXXXX`):**
   - Chronological logging of all sensitive operations (logins, password updates, profile edits, invoicing, payments, SMS dispatches).
3. **Awesomebar Search:**
   - Universal navigation search input in the top navigation bar with keyboard shortcut (`Ctrl+K` / `/`) to jump directly to any Desk module.

---

### 2.8 Public Commercial Portal

1. **Corporate Homepage (`/`):**
   - High-impact positioning: "Enterprise Systems Architecture, Delivery & Operations".
   - Presentation of the 3 Practice Pillars.
   - 16 Systems Interactive Portfolio with technology stack badges.
   - Client discovery inquiry form with instant SMS notification.
2. **Public Systems Catalog (`/systems`):**
   - Filterable view of all platforms across ERP, Data/AI, and Operational Excellence.
3. **Tailored Scope Generator (`/tailored-scope`):**
   - Dedicated scoping questionnaire for prospective enterprise clients without sticker-price friction.
