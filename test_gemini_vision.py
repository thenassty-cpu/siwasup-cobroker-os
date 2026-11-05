import json, urllib.request

cfg = json.load(open(r'C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\config.json', 'r', encoding='utf-8'))
api_key = cfg.get("gemini_api", {}).get("api_key", "")

for model_name in ["gemini-flash-latest", "gemini-2.5-flash", "gemini-flash-lite-latest"]:
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": "Reply with JSON: {\"status\": \"ok\", \"model\": \"" + model_name + "\"}"}]}],
        "generationConfig": {"response_mime_type": "application/json"}
    }
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            res = json.loads(resp.read().decode('utf-8'))
            print(f"Model {model_name} SUCCESS:", res["candidates"][0]["content"]["parts"][0]["text"])
            break
    except Exception as e:
        print(f"Model {model_name} FAILED: {e}")
