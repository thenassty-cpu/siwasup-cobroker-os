import urllib.request
import ssl
import json
import hashlib
import hmac
from datetime import datetime
import os
import sys
import time

# Ensure UTF-8 output
if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# R2 Config
ACCESS_KEY = "21ea6725b31de7a08eb4e15c89181c56"
SECRET_KEY = "ec0b53061b1ca77e0f87b534194dd247949ed82679a591d5eda9752fa14f784a"
ACCOUNT_ID = "b2f4f44870ea14a9a5114dfb6163b48c"
BUCKET = "siwasup-npa-assets"
ENDPOINT = f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com"
CDN_BASE = "https://assets.siwasup.com"

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://homerunplatform.com',
    'Referer': 'https://homerunplatform.com/'
}

def sign(key, msg):
    return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

def get_signature_key(key, date_stamp, region_name, service_name):
    k_date = sign(('AWS4' + key).encode('utf-8'), date_stamp)
    k_region = sign(k_date, region_name)
    k_service = sign(k_region, service_name)
    k_signing = sign(k_service, 'aws4_request')
    return k_signing

def put_object_r2(object_key, data_bytes, content_type="image/jpeg"):
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
    
    with urllib.request.urlopen(req, context=ctx, timeout=20) as resp:
        return resp.status

def run_scb_snatcher(limit=50):
    data_dir = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\data"
    all_props_file = os.path.join(data_dir, "homerun_all_properties_10k.json")
    state_file = os.path.join(data_dir, "scb_images_sync_state.json")
    manifest_file = os.path.join(data_dir, "scb_assets_manifest.json")
    
    if not os.path.exists(all_props_file):
        print("[-] Error: homerun_all_properties_10k.json not found!")
        return

    with open(all_props_file, 'r', encoding='utf-8') as f:
        items = json.load(f)

    scb_items = [it for it in items if it.get('bank_pool') == 'SCB']
    print(f"[*] Total SCB Properties available: {len(scb_items)}")

    state = {}
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
        except Exception:
            state = {}

    manifest = {}
    if os.path.exists(manifest_file):
        try:
            with open(manifest_file, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
        except Exception:
            manifest = {}

    to_process = [it for it in scb_items if it['id'] not in state]
    print(f"[*] Remaining SCB properties to process: {len(to_process)}")
    print(f"[*] Processing batch limit: {limit} properties...\n")

    count = 0
    total_images_uploaded = 0

    for item in to_process[:limit]:
        p_id = item['id']
        title = item.get('title', 'Unknown')
        code = item.get('code', 'N/A')
        print(f"[{count+1}/{limit}] Processing: {code} - {title[:35]}...")

        # 1. Fetch detail with media
        detail_url = f"https://homerun-platform-api-prod-645188686833.asia-southeast1.run.app/api/web/group-buy/scb/properties/{p_id}?include=media"
        detail_data = {}
        for retry in range(3):
            try:
                req = urllib.request.Request(detail_url, headers=HEADERS)
                with urllib.request.urlopen(req, context=ctx, timeout=12) as r:
                    if r.status == 200:
                        detail_data = json.loads(r.read().decode('utf-8')).get('data', {})
                        break
            except Exception:
                time.sleep(1.0)

        thumb_url = detail_data.get('thumbnailUrl')
        gallery = detail_data.get('gallery', [])

        property_assets = {
            "id": p_id,
            "code": code,
            "title": title,
            "price": item.get('price'),
            "thumbnail": None,
            "gallery": []
        }

        # 2. Upload Thumbnail
        if thumb_url:
            try:
                t_req = urllib.request.Request(thumb_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(t_req, context=ctx, timeout=15) as r:
                    img_bytes = r.read()
                    ctype = r.headers.get('content-type', 'image/jpeg')
                    ext = "png" if "png" in ctype else "jpg"
                    r2_key = f"scb/{p_id}/thumb.{ext}"
                    put_object_r2(r2_key, img_bytes, ctype)
                    property_assets["thumbnail"] = f"{CDN_BASE}/{r2_key}"
                    total_images_uploaded += 1
            except Exception as e:
                pass

        # 3. Upload Gallery (up to 4 key images per property)
        for idx, g in enumerate(gallery[:4]):
            g_url = g.get('url')
            if g_url:
                try:
                    g_req = urllib.request.Request(g_url, headers={'User-Agent': 'Mozilla/5.0'})
                    with urllib.request.urlopen(g_req, context=ctx, timeout=15) as r:
                        img_bytes = r.read()
                        ctype = r.headers.get('content-type', 'image/jpeg')
                        ext = "png" if "png" in ctype else "jpg"
                        r2_key = f"scb/{p_id}/gallery_{idx}.{ext}"
                        put_object_r2(r2_key, img_bytes, ctype)
                        property_assets["gallery"].append(f"{CDN_BASE}/{r2_key}")
                        total_images_uploaded += 1
                except Exception as e:
                    pass

        # Save to state and manifest
        state[p_id] = {
            "synced_at": datetime.now().isoformat(),
            "images_count": (1 if property_assets["thumbnail"] else 0) + len(property_assets["gallery"])
        }
        manifest[p_id] = property_assets
        count += 1

        print(f"   -> [OK] Uploaded {state[p_id]['images_count']} images to R2 CDN")
        # Friendly stealth delay (0.2s)
        time.sleep(0.2)

        # Save progress every 10 properties
        if count % 10 == 0:
            with open(state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, ensure_ascii=False, indent=2)
            with open(manifest_file, 'w', encoding='utf-8') as f:
                json.dump(manifest, f, ensure_ascii=False, indent=2)

    # Final save
    with open(state_file, 'w', encoding='utf-8') as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    with open(manifest_file, 'w', encoding='utf-8') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)

    print(f"\n================ BATCH COMPLETED ================")
    print(f"Properties Processed : {count}")
    print(f"Total Images in R2   : {total_images_uploaded}")
    print(f"Total SCB Done So Far: {len(state)}/{len(scb_items)}")
    print(f"Manifest File Saved  : {manifest_file}")
    print("=================================================")

if __name__ == "__main__":
    lim = 30
    if len(sys.argv) > 1:
        try:
            lim = int(sys.argv[1])
        except Exception:
            pass
    run_scb_snatcher(limit=lim)
