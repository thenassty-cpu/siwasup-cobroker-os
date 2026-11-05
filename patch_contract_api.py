path = r'C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts\line_gemini_webhook.py'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Define extract_contract_ocr and contract data helpers
contract_helpers = '''
CONTRACTS_PATH = os.path.join(DATA_DIR, "exclusive_contracts.json")
CONTRACTS_LOCK = threading.Lock()
_R2_CONTRACTS_VAULT_KEY = "_vault/contracts_" + hmac.new(ADMIN_EXPORT_SECRET.encode("utf-8"), b"siwasup_contracts_vault_v1", hashlib.sha256).hexdigest()[:32] + ".json"

def load_contracts_data():
    if os.path.exists(CONTRACTS_PATH):
        try:
            with open(CONTRACTS_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"[Warn] Failed to read exclusive_contracts.json: {e}")
    return {"updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "contracts": []}

def save_contracts_data(store):
    with CONTRACTS_LOCK:
        store["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_bytes = json.dumps(store, ensure_ascii=False, indent=2).encode("utf-8")
        try:
            with open(CONTRACTS_PATH, "wb") as f:
                f.write(data_bytes)
        except Exception as e:
            print(f"[Error] Failed to save contracts local: {e}")
        if put_object_r2 and os.environ.get("PORT"):
            threading.Thread(target=lambda: put_object_r2(_R2_CONTRACTS_VAULT_KEY, data_bytes, "application/json"), daemon=True).start()


def extract_contract_ocr(image_base64, doc_type="id_card", mime_type="image/jpeg"):
    if "," in image_base64:
        image_base64 = image_base64.split(",", 1)[1]
    
    if doc_type == "id_card":
        prompt = """คุณคือ AI ผู้ช่วยตรวจสอบและสกัดข้อมูลจาก 'บัตรประจำตัวประชาชนไทย' (Thai National ID Card) สำหรับร่างสัญญาแต่งตั้งตัวแทนขายอสังหาริมทรัพย์
จงอ่านและสกัดข้อมูลจากภาพอย่างละเอียด ถูกต้อง 100% ตอบกลับเฉพาะ JSON ที่มีโครงสร้างดังนี้เท่านั้น:
{
  "doc_type": "id_card",
  "id_number": "เลขประจำตัวประชาชน 13 หลัก (เฉพาะตัวเลข)",
  "prefix_th": "คำนำหน้า (นาย / นาง / นางสาว)",
  "first_name_th": "ชื่อภาษาไทย",
  "last_name_th": "นามสกุลภาษาไทย",
  "full_name_th": "ชื่อ-สกุลเต็มภาษาไทยพร้อมคำนำหน้า",
  "full_name_en": "Full Name in English",
  "birth_date_th": "วันเดือนปีเกิด พ.ศ.",
  "address_no": "บ้านเลขที่",
  "moo": "หมู่ที่",
  "soi": "ตรอก/ซอย",
  "road": "ถนน",
  "subdistrict": "ตำบล/แขวง",
  "district": "อำเภอ/เขต",
  "province": "จังหวัด",
  "full_address": "ที่อยู่เต็มตามบัตรประชาชน"
}
หากมองไม่เห็นฟิลด์ใด ให้ใส่เป็นสตริงว่าง "" ห้ามเดาข้อมูล"""
    elif doc_type == "title_deed":
        prompt = """คุณคือ AI ผู้ช่วยตรวจสอบและสกัดข้อมูลจาก 'โฉนดที่ดินไทย (น.ส. 4 จ.)' สำหรับร่างสัญญาแต่งตั้งตัวแทนขายอสังหาริมทรัพย์
จงอ่านและสกัดข้อมูลจากภาพอย่างละเอียด ถูกต้อง 100% ตอบกลับเฉพาะ JSON ที่มีโครงสร้างดังนี้เท่านั้น:
{
  "doc_type": "title_deed",
  "deed_number": "โฉนดที่ดินเลขที่",
  "land_number": "เลขที่ดิน",
  "survey_page": "หน้าสำรวจ",
  "rawang": "ระวาง",
  "subdistrict": "ตำบล/แขวง",
  "district": "อำเภอ/เขต",
  "province": "จังหวัด",
  "area_rai": "จำนวนไร่ (ตัวเลข)",
  "area_ngan": "จำนวนงาน (ตัวเลข)",
  "area_sqw": "จำนวนตารางวา (ตัวเลข)",
  "area_total_sqw": "คำนวณพื้นที่รวมเป็นตารางวา เช่น 1 ไร่ 2 งาน 50 วา = 650 ตร.ว.",
  "owner_name": "ชื่อผู้ถือกรรมสิทธิ์ / ผู้ถือกรรมสิทธิ์เดิม"
}
หากมองไม่เห็นฟิลด์ใด ให้ใส่เป็นสตริงว่าง "" ห้ามเดาข้อมูล"""
    else:
        prompt = """สกัดข้อมูลสำคัญจากเอกสารอสังหาริมทรัพย์ไทยในภาพนี้ ตอบกลับเป็น JSON ที่ระบุประเภทเอกสารและข้อมูลสำคัญ"""

    models_to_try = ["gemini-flash-lite-latest", "gemini-flash-latest"]
    for m in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{m}:generateContent?key={GEMINI_API_KEY}"
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt},
                        {
                            "inline_data": {
                                "mime_type": mime_type,
                                "data": image_base64
                            }
                        }
                    ]
                }
            ],
            "generationConfig": {
                "response_mime_type": "application/json",
                "temperature": 0.1
            }
        }
        try:
            req = urllib.request.Request(
                url,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json'},
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                data = json.loads(resp.read().decode('utf-8'))
                candidates = data.get('candidates', [])
                if candidates:
                    parts = candidates[0].get('content', {}).get('parts', [])
                    if parts:
                        raw_json = parts[0].get('text', '').strip()
                        return json.loads(raw_json)
        except Exception as e:
            print(f"[OCR Error on {m}]: {e}")
            continue

    raise RuntimeError("Failed to extract OCR data with Gemini Vision API")
'''

# Insert before WebhookHandler
idx_handler = content.find('class WebhookHandler(')
assert idx_handler != -1, "WebhookHandler not found"
content = content[:idx_handler] + contract_helpers + "\n\n" + content[idx_handler:]

# 2. Add endpoints in do_GET
target_get = 'if path == "/api/bundle/flex":'
contract_get = """if path == "/api/contracts/list":
            agent_ref = query.get("agent_ref", [""])[0]
            store = load_contracts_data()
            contracts = store.get("contracts", [])
            if agent_ref:
                contracts = [c for c in contracts if c.get("agent_ref") == agent_ref or c.get("agent_id") == agent_ref]
            self._send_json(200, {"status": "success", "count": len(contracts), "contracts": contracts})
            return

        if path == "/api/bundle/flex":"""

assert target_get in content, "target_get not found"
content = content.replace(target_get, contract_get, 1)

# 3. Add endpoints in do_POST
target_post = 'if path == "/api/lobby/register":'
contract_post = """if path == "/api/ocr/contract":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode('utf-8'))
                doc_type = payload.get("doc_type", "id_card")
                img_b64 = payload.get("image_base64", "")
                mime_type = payload.get("mime_type", "image/jpeg")
                if not img_b64:
                    self._send_json(400, {"error": "Missing image_base64 parameter"})
                    return
                ocr_result = extract_contract_ocr(img_b64, doc_type=doc_type, mime_type=mime_type)
                self._send_json(200, {
                    "status": "success",
                    "doc_type": doc_type,
                    "data": ocr_result
                })
            except Exception as e:
                self._send_json(500, {"status": "error", "message": str(e)})
            return

        if path == "/api/contracts/save":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)
            try:
                payload = json.loads(body.decode('utf-8'))
                store = load_contracts_data()
                cid = payload.get("id") or f"SW-CNT-{int(time.time()*1000)%1000000}"
                payload["id"] = cid
                payload["saved_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Expiry calculation (default 90 days if not set)
                days = int(payload.get("contract_days") or 90)
                exp_ts = time.time() + (days * 86400)
                payload["expires_at"] = datetime.fromtimestamp(exp_ts).strftime("%Y-%m-%d")
                
                # Replace or prepend
                contracts = store.setdefault("contracts", [])
                contracts = [c for c in contracts if c.get("id") != cid]
                contracts.insert(0, payload)
                store["contracts"] = contracts
                save_contracts_data(store)
                self._send_json(200, {"status": "success", "contract": payload})
            except Exception as e:
                self._send_json(500, {"status": "error", "message": str(e)})
            return

        if path == "/api/lobby/register":"""

assert target_post in content, "target_post not found"
content = content.replace(target_post, contract_post, 1)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("line_gemini_webhook.py patched with Contract OCR & Management API successfully!")
