file_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts\line_gemini_webhook.py"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

target_block = '''LOBBY_PATH = os.path.join(DATA_DIR, "lobby_applicants.json")
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

content_norm = content.replace("\r\n", "\n")
target_norm = target_block.replace("\r\n", "\n")

content_norm = content_norm.replace(target_norm, '')
class_def = 'class WebhookHandler(http.server.BaseHTTPRequestHandler):'
content_norm = content_norm.replace(class_def, target_norm + '\n\n' + class_def)

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content_norm)

print("Moved helper functions before class definition successfully!")
