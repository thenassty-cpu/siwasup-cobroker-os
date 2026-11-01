file_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts\line_gemini_webhook.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add lobby helper functions
lobby_helpers = '''
LOBBY_PATH = os.path.join(DATA_DIR, "lobby_applicants.json")
LOBBY_LOCK = threading.Lock()

def load_lobby_data():
    if os.path.exists(LOBBY_PATH):
        try:
            with open(LOBBY_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Warn] Failed to read lobby_applicants.json: {e}")
    return {"updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "pending": [], "approved": []}

def save_lobby_data(store):
    with LOBBY_LOCK:
        store["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_bytes = json.dumps(store, ensure_ascii=False, indent=2).encode("utf-8")
        try:
            with open(LOBBY_PATH, "wb") as f:
                f.write(data_bytes)
        except Exception as e:
            print(f"[Error] Failed to save lobby local: {e}")
'''

# Insert lobby helpers before do_OPTIONS
options_anchor = '    def do_OPTIONS(self):'
assert options_anchor in content, "options_anchor not found"
content = content.replace(options_anchor, lobby_helpers + "\n" + options_anchor, 1)

# 2. Add lobby routes to do_GET
get_anchor = '    def do_GET(self):\n        parsed_url = urllib.parse.urlparse(self.path)\n        path = parsed_url.path\n        query = urllib.parse.parse_qs(parsed_url.query)\n'
# Also support CRLF
get_anchor_crlf = '    def do_GET(self):\r\n        parsed_url = urllib.parse.urlparse(self.path)\r\n        path = parsed_url.path\r\n        query = urllib.parse.parse_qs(parsed_url.query)\r\n'

lobby_get_routes = '''        if path == "/api/lobby/list":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            data = load_lobby_data()
            self.wfile.write(json.dumps(data, ensure_ascii=False, indent=2).encode('utf-8'))
            return

        if path == "/api/lobby/status":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            app_id = query.get("id", [""])[0]
            phone = query.get("phone", [""])[0]
            data = load_lobby_data()
            approved_item = None
            for a in data.get("approved", []):
                if (app_id and a.get("id") == app_id) or (phone and a.get("phone") == phone):
                    approved_item = a
                    break
            if approved_item:
                resp = {"status": "approved", "applicant": approved_item}
            else:
                resp = {"status": "pending"}
            self.wfile.write(json.dumps(resp, ensure_ascii=False).encode('utf-8'))
            return
'''

if get_anchor in content:
    content = content.replace(get_anchor, get_anchor + lobby_get_routes, 1)
    print("Added lobby routes to do_GET (LF)")
elif get_anchor_crlf in content:
    content = content.replace(get_anchor_crlf, get_anchor_crlf + lobby_get_routes.replace('\n', '\r\n'), 1)
    print("Added lobby routes to do_GET (CRLF)")
else:
    print("Warning: get_anchor not found")

# 3. Add lobby routes to do_POST
post_anchor = '    def do_POST(self):\n'
post_anchor_crlf = '    def do_POST(self):\r\n'

lobby_post_routes = '''        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path == "/api/lobby/register":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode('utf-8'))
                store = load_lobby_data()
                phone = payload.get("phone", "")
                if phone:
                    store["pending"] = [p for p in store.get("pending", []) if p.get("phone") != phone]
                store.setdefault("pending", []).insert(0, payload)
                save_lobby_data(store)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "applicant": payload}, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return

        if path == "/api/lobby/approve":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode('utf-8'))
                app_id = payload.get("applicantId")
                store = load_lobby_data()
                target_idx = -1
                for idx, p in enumerate(store.get("pending", [])):
                    if p.get("id") == app_id:
                        target_idx = idx
                        break
                if target_idx != -1:
                    applicant = store["pending"].pop(target_idx)
                    approved_item = {
                        "id": applicant.get("id"),
                        "name": applicant.get("name"),
                        "nickname": applicant.get("nickname"),
                        "phone": applicant.get("phone"),
                        "line_id": applicant.get("line_id"),
                        "zone": applicant.get("zone"),
                        "role": payload.get("role", "Co-Broker Partner"),
                        "title": payload.get("title", ""),
                        "badges": payload.get("badges", []),
                        "permissions": payload.get("permissions", {}),
                        "approved_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    store.setdefault("approved", []).insert(0, approved_item)
                    save_lobby_data(store)
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "success", "approved": approved_item}, ensure_ascii=False).encode('utf-8'))
                else:
                    self.send_response(404)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Applicant not found"}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return

        if path == "/api/lobby/reject":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode('utf-8'))
                app_id = payload.get("applicantId")
                store = load_lobby_data()
                store["pending"] = [p for p in store.get("pending", []) if p.get("id") != app_id]
                save_lobby_data(store)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success"}, ensure_ascii=False).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return
'''

if post_anchor in content:
    content = content.replace(post_anchor, post_anchor + lobby_post_routes, 1)
    print("Added lobby routes to do_POST (LF)")
elif post_anchor_crlf in content:
    content = content.replace(post_anchor_crlf, post_anchor_crlf + lobby_post_routes.replace('\n', '\r\n'), 1)
    print("Added lobby routes to do_POST (CRLF)")
else:
    print("Warning: post_anchor not found")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Finished patching line_gemini_webhook.py with Lobby REST APIs!")
