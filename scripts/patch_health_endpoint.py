# -*- coding: utf-8 -*-
"""
scripts/patch_health_endpoint.py
--------------------------------
Adds a lightweight, informative /health and /ping endpoint
for the Morning / Working Hours Heartbeat Bot to keep Nong Siwa awake.
"""

import sys

WEBHOOK_PATH = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts\line_gemini_webhook.py"

with open(WEBHOOK_PATH, "r", encoding="utf-8") as f:
    code = f.read()

target = "        query = urllib.parse.parse_qs(parsed_url.query)"

health_snippet = """        query = urllib.parse.parse_qs(parsed_url.query)

        # Health & Keep-Alive Heartbeat Endpoint (Wake up Nong Siwa)
        if path in ("/health", "/api/health", "/ping"):
            store = load_lobby_data()
            approved_count = len(store.get("approved", []))
            self._send_json(200, {
                "status": "healthy",
                "service": "Siwasup Co-Broker Webhook v2",
                "server_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "approved_members": approved_count,
                "r2_sync": bool(put_object_r2),
                "anti_downgrade": "ACTIVE",
                "message": "Nong Siwa is wide awake and ready to serve!"
            })
            return"""

if target in code:
    code = code.replace(target, health_snippet, 1)
    with open(WEBHOOK_PATH, "w", encoding="utf-8") as f:
        f.write(code)
    print("[SUCCESS] Added /health and /ping endpoint to line_gemini_webhook.py")
else:
    print("[WARN] Target not found")
