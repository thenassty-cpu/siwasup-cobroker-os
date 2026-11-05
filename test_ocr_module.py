import json, os, urllib.request

cfg = json.load(open(r'C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\config.json', 'r', encoding='utf-8'))
api_key = cfg.get("gemini_api", {}).get("api_key", "")

def run_ocr_test(prompt_text, b64_img, mime_type="image/jpeg"):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-lite-latest:generateContent?key={api_key}"
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_text},
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": b64_img
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
    req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        res = json.loads(resp.read().decode('utf-8'))
        return json.loads(res["candidates"][0]["content"]["parts"][0]["text"])

print("OCR Test module defined successfully")
