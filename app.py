"""
Zureka Solutions Limited - Python Enterprise Desk Backend
Running natively on Python 3.15 | Modular Architecture | PostgreSQL / JSON Dual-Store | Pandora SMS
"""
import sys
import os
import json
from http.server import ThreadingHTTPServer

import config
from routes.handler import ZurekaRequestHandler
from integrations import sms

def _maybe_init_postgres():
    try:
        from core import postgres as pg
        if pg.is_postgres_enabled():
            seed = {}
            if os.path.exists(config.DATA_FILE):
                try:
                    with open(config.DATA_FILE, 'r', encoding='utf-8') as f:
                        seed = json.load(f)
                except Exception:
                    pass
            ok = pg.init_db(seed_data=seed)
            status = "Connected & Tables Initialized" if ok else "Failed to initialize"
            print(f"     [PostgreSQL] {status}")
            return True
        else:
            print("     [Storage Engine] JSON File Store (offline_store.json)")
            return False
    except Exception as e:
        print(f"     [PostgreSQL Init Note] {e} - Falling back to JSON Store")
        return False

def run_server():
    server_address = ('', config.PORT)
    try:
        httpd = ThreadingHTTPServer(server_address, ZurekaRequestHandler)
        print("==================================================================")
        print("     ZUREKA SOLUTIONS LIMITED - MODULAR ENTERPRISE BACKEND")
        print(f"     Running at: http://localhost:{config.PORT}")
        print("     [Engine] Python 3.15 Standard Library Backend")
        _maybe_init_postgres()
        print(f"     [SMS Gateway] Pandora Networks ({sms.get_sms_config()['username']}) Connected")
        print("     [Pricing Mode] Zero Public Sticker Pricing • Tailored Scope")
        print("     [RBAC Mode] Advanced ERPNext Desk Architecture with Strict Enforcement")
        print("     [Architecture] Modular Packages (core, integrations, routes, templates)")
        print("==================================================================")
        print("Press Ctrl+C to stop the server.\n")
        sys.stdout.flush()
        httpd.serve_forever()
    except OSError as e:
        if e.errno == 98 or e.errno == 10048:
            print(f"\n[Notice] Port {config.PORT} is already in use by another running instance.")
            print(f"The platform is already accessible at: http://localhost:{config.PORT}\n")
        else:
            print(f"[Error] {e}")

if __name__ == '__main__':
    run_server()
