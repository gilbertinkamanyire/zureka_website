"""
Zureka Solutions Limited - Python Enterprise Desk Backend
Running natively on Python 3.15 | 100% Offline | Modular Architecture | Pandora SMS
"""
import sys
from http.server import ThreadingHTTPServer

import config
from routes.handler import ZurekaRequestHandler
from integrations import sms

def run_server():
    server_address = ('', config.PORT)
    try:
        httpd = ThreadingHTTPServer(server_address, ZurekaRequestHandler)
        print("==================================================================")
        print("     ZUREKA SOLUTIONS LIMITED - MODULAR ENTERPRISE BACKEND")
        print(f"     Running at: http://localhost:{config.PORT}")
        print("     [Engine] Python 3.15 Standard Library (Zero Package Dependencies)")
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
