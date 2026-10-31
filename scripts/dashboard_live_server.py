import json
import os
import time
import http.server
import socketserver
import threading
from datetime import datetime, timedelta
import urllib.request
import ssl
import hashlib
import hmac

WEB_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
DATA_DIR = os.path.join(WEB_DIR, "data")
STATE_FILE = os.path.join(DATA_DIR, "r2_images_sync_state.json")
MANIFEST_FILE = os.path.join(DATA_DIR, "r2_assets_manifest.json")
JS_STATE_FILE = os.path.join(DATA_DIR, "crawler_live_state.js")
LOG_FILE = os.path.join(DATA_DIR, "overnight_crawler.log")
MEMO_FILE = os.path.join(DATA_DIR, "hai_executive_memo.json")

TOTALS = {
    "SAM": 5100,
    "TTB": 1365,
    "SCB": 4207,
    "GSB": 4446
}

# R2 Cloudflare Credentials
ACCESS_KEY = "21ea6725b31de7a08eb4e15c89181c56"
SECRET_KEY = "ec0b53061b1ca77e0f87b534194dd247949ed82679a591d5eda9752fa14f784a"
ACCOUNT_ID = "b2f4f44870ea14a9a5114dfb6163b48c"
BUCKET = "siwasup-npa-assets"
ENDPOINT = f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com"
CDN_BASE = "https://assets.siwasup.com"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def get_signature_key(key, date_stamp, region_name, service_name):
    k_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    k_region = sign(k_date, region_name)
    k_service = sign(k_region, service_name)
    k_signing = sign(k_service, 'aws4_request')
    return k_signing

def put_object_r2(object_key, data_bytes, content_type="application/javascript"):
    now = datetime.utcnow()
    amz_date = now.strftime('%Y%m%dT%H%M%SZ')
    date_stamp = now.strftime('%Y%m%d')
    region = "auto"
    service = "s3"
    
    host = f"{ACCOUNT_ID}.r2.cloudflarestorage.com"
    payload_hash = hashlib.sha256(data_bytes).hexdigest()
    
    canonical_uri = f"/{BUCKET}/{object_key}"
    canonical_querystring = ""
    canonical_headers = f"content-type:{content_type}\nhost:{host}\nx-amz-content-sha256:{payload_hash}\nx-amz-date:{amz_date}\n"
    signed_headers = "content-type;host;x-amz-content-sha256;x-amz-date"
    
    canonical_request = f"PUT\n{canonical_uri}\n{canonical_querystring}\n{canonical_headers}\n{signed_headers}\n{payload_hash}"
    algorithm = "AWS4-HMAC-SHA256"
    credential_scope = f"{date_stamp}/{region}/{service}/aws4_request"
    string_to_sign = f"{algorithm}\n{amz_date}\n{credential_scope}\n{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"
    
    signing_key = get_signature_key(SECRET_KEY, date_stamp, region, service)
    signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()
    authorization_header = f"{algorithm} Credential={ACCESS_KEY}/{credential_scope}, SignedHeaders={signed_headers}, Signature={signature}"
    
    url = f"{ENDPOINT}/{BUCKET}/{object_key}"
    req = urllib.request.Request(url, data=data_bytes, method="PUT")
    req.add_header('Host', host)
    req.add_header('Content-Type', content_type)
    req.add_header('x-amz-date', amz_date)
    req.add_header('x-amz-content-sha256', payload_hash)
    req.add_header('Authorization', authorization_header)
    
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        return resp.status

def sync_html_to_r2():
    html_path = os.path.join(WEB_DIR, "crawler_dashboard.html")
    if os.path.exists(html_path):
        try:
            with open(html_path, 'r', encoding='utf-8') as f:
                content = f.read()
            html_bytes = content.encode('utf-8')
            put_object_r2("dashboard.html", html_bytes, "text/html; charset=utf-8")
            put_object_r2("crawler_dashboard.html", html_bytes, "text/html; charset=utf-8")
            print("[*] Successfully synced dashboard.html to Cloudflare R2")
        except Exception as e:
            print(f"[-] Error syncing dashboard.html to R2: {e}")

start_tracking_time = time.time()
start_tracking_count = 0
last_r2_upload_time = 0

def update_live_js():
    global start_tracking_time, start_tracking_count, last_r2_upload_time
    # Initial sync of HTML to R2
    sync_html_to_r2()
    
    while True:
        try:
            state = {}
            if os.path.exists(STATE_FILE):
                try:
                    with open(STATE_FILE, 'r', encoding='utf-8') as f:
                        state = json.load(f)
                except Exception:
                    pass
            
            manifest = {}
            if os.path.exists(MANIFEST_FILE):
                try:
                    with open(MANIFEST_FILE, 'r', encoding='utf-8') as f:
                        manifest = json.load(f)
                except Exception:
                    pass

            counts = {"SAM": 0, "TTB": 0, "SCB": 0}
            total_images = 0
            
            # Count by pool
            for pid, info in state.items():
                pool = info.get("pool", "SCB").upper()
                if pool in counts:
                    counts[pool] += 1
                total_images += info.get("images_count", 0)

            # Speed & ETA Calculation
            total_done = len(state)
            if start_tracking_count == 0 and total_done > 0:
                start_tracking_count = total_done
                start_tracking_time = time.time()

            elapsed_minutes = max((time.time() - start_tracking_time) / 60, 0.1)
            items_since_start = max(total_done - start_tracking_count, 1)
            speed_per_min = round(items_since_start / elapsed_minutes, 1) if elapsed_minutes > 0.5 else 8.5
            
            # Dynamic ETA based on active pool
            if counts["TTB"] < TOTALS["TTB"] and counts["SAM"] >= TOTALS["SAM"]:
                active_bank = "TTB"
                ttb_rem = max(TOTALS["TTB"] - counts["TTB"], 0)
                eta_mins = int(ttb_rem / speed_per_min) if speed_per_min > 0 else 60
                eta_time = datetime.now() + timedelta(minutes=eta_mins)
                eta_title = "TTB BATCH ETA"
                eta_str = eta_time.strftime("%H:%M น.")
                eta_sub = "In Progress ⚡"
            elif total_done >= 10672:
                eta_title = "SYNC COMPLETE"
                eta_str = "100% DONE"
                eta_sub = "All 10,672 Synced 🏆"
            else:
                eta_title = "SCB ETA"
                scb_remaining = max(TOTALS["SCB"] - counts["SCB"], 0)
                scb_eta_minutes = int(scb_remaining / speed_per_min) if speed_per_min > 0 else 420
                eta_time = datetime.now() + timedelta(minutes=scb_eta_minutes)
                eta_str = eta_time.strftime("%H:%M น.")
                eta_sub = "Morning Target 🌅"
            
            scb_eta_str = eta_str
            
            # Total ETA
            all_remaining = max(10672 - total_done, 0)
            all_eta_hours = round(all_remaining / (speed_per_min * 60), 1) if speed_per_min > 0 else 18.0

            # Estimated Storage Used (avg 60 KB per image)
            storage_mb = round((total_images * 65) / 1024, 1)
            storage_pct = round((storage_mb / 10240) * 100, 2)

            # Recent 4 properties from manifest
            recent_props = []
            m_items = list(manifest.items())
            for pid, pdata in reversed(m_items[-4:]):
                recent_props.append({
                    "id": pid,
                    "code": pdata.get("code", "N/A"),
                    "title": pdata.get("title", "Unknown"),
                    "price": pdata.get("price", 0),
                    "thumbnail": pdata.get("thumbnail"),
                    "gallery_count": len(pdata.get("gallery", []))
                })

            # Recent log lines
            recent_logs = []
            if os.path.exists(LOG_FILE):
                try:
                    with open(LOG_FILE, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                        for l in reversed(lines[-15:]):
                            if "Total R2 Done:" in l or "Starting Pool" in l:
                                recent_logs.append(l.strip())
                except Exception:
                    pass

            # GSB Progress
            gsb_file = os.path.join(DATA_DIR, "gsb_all_properties.json")
            gsb_done = 0
            if os.path.exists(gsb_file):
                try:
                    with open(gsb_file, 'r', encoding='utf-8') as gf:
                        gsb_done = len(json.load(gf))
                except Exception:
                    gsb_done = 0
            gsb_pct = round((gsb_done / TOTALS["GSB"]) * 100, 1)

            # Calculate percentages
            sam_pct = round((counts["SAM"] / TOTALS["SAM"]) * 100, 1)
            ttb_pct = round((counts["TTB"] / TOTALS["TTB"]) * 100, 1)
            scb_pct = round((counts["SCB"] / TOTALS["SCB"]) * 100, 1)
            overall_pct = round((total_done / 10672) * 100, 1)

            # Executive Memo from Hai
            executive_memo = None
            if os.path.exists(MEMO_FILE):
                try:
                    with open(MEMO_FILE, 'r', encoding='utf-8') as mf:
                        executive_memo = json.load(mf)
                except Exception:
                    pass

            payload = {
                "updated_at": datetime.now().strftime("%H:%M:%S"),
                "total_done": total_done,
                "total_target": 10672,
                "overall_pct": overall_pct,
                "total_images": total_images,
                "speed_per_min": speed_per_min,
                "eta_title": eta_title,
                "eta_str": eta_str,
                "eta_sub": eta_sub,
                "scb_eta_str": scb_eta_str,
                "all_eta_hours": all_eta_hours,
                "storage_mb": storage_mb,
                "storage_pct": storage_pct,
                "executive_memo": executive_memo,
                "sam": {
                    "done": counts["SAM"],
                    "total": TOTALS["SAM"],
                    "pct": sam_pct,
                    "status": "Waiting" if counts["SAM"] == 0 else ("Completed" if counts["SAM"] >= TOTALS["SAM"] else "Active")
                },
                "ttb": {
                    "done": counts["TTB"],
                    "total": TOTALS["TTB"],
                    "pct": ttb_pct,
                    "status": "Waiting" if counts["TTB"] == 0 else ("Completed" if counts["TTB"] >= TOTALS["TTB"] else "Active")
                },
                "scb": {
                    "done": counts["SCB"],
                    "total": TOTALS["SCB"],
                    "pct": scb_pct,
                    "status": "Completed" if counts["SCB"] >= TOTALS["SCB"] else "Active"
                },
                "gsb": {
                    "done": gsb_done,
                    "total": TOTALS["GSB"],
                    "pct": gsb_pct,
                    "status": "Active" if gsb_done > 0 else "Queued"
                },
                "recent_props": recent_props,
                "recent_logs": recent_logs[:5]
            }

            js_content = f"window.CRAWLER_LIVE_DATA = {json.dumps(payload, ensure_ascii=False, indent=2)};"
            
            # Save locally
            with open(JS_STATE_FILE, 'w', encoding='utf-8') as f:
                f.write(js_content)

            # Upload to Cloudflare R2 every 10 seconds for remote access from office/mobile
            if time.time() - last_r2_upload_time >= 10:
                try:
                    put_object_r2("crawler_live_state.js", js_content.encode('utf-8'), "application/javascript; charset=utf-8")
                    last_r2_upload_time = time.time()
                except Exception as r2_err:
                    pass
                
        except Exception:
            pass
            
        time.sleep(2)

def start_http_server(port=8080):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=WEB_DIR, **kwargs)
            
        def log_message(self, format, *args):
            pass # Silent

        def copyfile(self, source, outputfile):
            try:
                super().copyfile(source, outputfile)
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                pass # Client disconnected early, ignore cleanly

        def handle_one_request(self):
            try:
                super().handle_one_request()
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                pass # Mobile sleep / closed tab

    class SafeThreadingServer(socketserver.ThreadingMixIn, http.server.HTTPServer):
        allow_reuse_address = True
        daemon_threads = True
        
        def handle_error(self, request, client_address):
            pass # Silently drop client abort errors

    while True:
        try:
            with SafeThreadingServer(("", port), Handler) as httpd:
                print(f"[*] Dashboard HTTP Server running at: http://localhost:{port}/crawler_dashboard.html")
                httpd.serve_forever()
        except Exception as e:
            time.sleep(2)

if __name__ == "__main__":
    t1 = threading.Thread(target=update_live_js, daemon=True)
    t1.start()
    start_http_server(8080)
