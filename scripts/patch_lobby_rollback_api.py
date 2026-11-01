import os
import sys

webhook_file = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts\line_gemini_webhook.py"
with open(webhook_file, 'r', encoding='utf-8') as f:
    text = f.read()

target = """        if path == "/api/lobby/reject":
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
            return"""

replacement = target + """

        if path == "/api/lobby/revoke":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode('utf-8'))
                app_id = payload.get("applicantId")
                reason = payload.get("reason", "Revoked by admin")
                store = load_lobby_data()
                target_idx = -1
                for idx, a in enumerate(store.get("approved", [])):
                    if a.get("id") == app_id:
                        target_idx = idx
                        break
                if target_idx != -1:
                    revoked_member = store["approved"].pop(target_idx)
                    rollback_id = f"rb_{int(time.time()*1000)}"
                    rollback_record = {
                        "rollback_id": rollback_id,
                        "action": "REVOKE",
                        "member": revoked_member,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "reason": reason
                    }
                    store.setdefault("rollback_history", []).insert(0, rollback_record)
                    store["rollback_history"] = store["rollback_history"][:50]
                    audit_entry = f"[{rollback_record['timestamp']}] คัดออก/เพิกถอนสิทธิ์: {revoked_member.get('name')} ({revoked_member.get('role')})"
                    store.setdefault("audit_log", []).insert(0, audit_entry)
                    store["audit_log"] = store["audit_log"][:100]
                    save_lobby_data(store)
                    self.send_response(200)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"status": "success", "revoked": revoked_member, "rollback_id": rollback_id}, ensure_ascii=False).encode('utf-8'))
                    return
                else:
                    self.send_response(404)
                    self.send_header('Content-Type', 'application/json; charset=utf-8')
                    self.send_header('Access-Control-Allow-Origin', '*')
                    self.end_headers()
                    self.wfile.write(json.dumps({"error": "Member not found in approved list"}).encode('utf-8'))
                    return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return

        if path == "/api/lobby/rollback":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode('utf-8'))
                rollback_id = payload.get("rollbackId")
                store = load_lobby_data()
                rb_list = store.get("rollback_history", [])
                target_idx = -1
                if rollback_id:
                    for idx, rb in enumerate(rb_list):
                        if rb.get("rollback_id") == rollback_id:
                            target_idx = idx
                            break
                elif rb_list:
                    target_idx = 0
                
                if target_idx != -1:
                    rb_item = rb_list.pop(target_idx)
                    if rb_item.get("action") == "REVOKE":
                        restored_member = rb_item.get("member")
                        store.setdefault("approved", []).insert(0, restored_member)
                        audit_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ↩️ Rollback คืนสิทธิ์: {restored_member.get('name')}"
                        store.setdefault("audit_log", []).insert(0, audit_entry)
                        save_lobby_data(store)
                        self.send_response(200)
                        self.send_header('Content-Type', 'application/json; charset=utf-8')
                        self.send_header('Access-Control-Allow-Origin', '*')
                        self.end_headers()
                        self.wfile.write(json.dumps({"status": "success", "restored": restored_member}, ensure_ascii=False).encode('utf-8'))
                        return
                self.send_response(404)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": "No rollback record found"}).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return

        if path == "/api/lobby/backup":
            try:
                store = load_lobby_data()
                backup_name = f"lobby_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
                backup_dir = os.path.join(os.path.dirname(LOBBY_PATH), "backups")
                os.makedirs(backup_dir, exist_ok=True)
                backup_file = os.path.join(backup_dir, backup_name)
                with open(backup_file, "w", encoding="utf-8") as bf:
                    json.dump(store, bf, ensure_ascii=False, indent=2)
                audit_entry = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 💾 สำรองข้อมูลสถานะ: {backup_name}"
                store.setdefault("audit_log", []).insert(0, audit_entry)
                save_lobby_data(store)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"status": "success", "backup_file": backup_name}, ensure_ascii=False).encode('utf-8'))
                return
            except Exception as e:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            return"""

if target in text:
    new_text = text.replace(target, replacement, 1)
    with open(webhook_file, 'w', encoding='utf-8') as f:
        f.write(new_text)
    print("SUCCESS: line_gemini_webhook.py patched with revoke, rollback, and backup endpoints!")
else:
    print("ERROR: Target string not found in line_gemini_webhook.py")
