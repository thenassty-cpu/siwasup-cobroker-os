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

# R2 Credentials
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

def log_msg(msg, log_fp=None):
    ts = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    if log_fp:
        try:
            with open(log_fp, 'a', encoding='utf-8') as f:
                f.write(line + "\n")
        except Exception:
            pass

def run_overnight_crawler():
    data_dir = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\data"
    all_props_file = os.path.join(data_dir, "homerun_all_properties_10k.json")
    state_file = os.path.join(data_dir, "r2_images_sync_state.json")
    manifest_file = os.path.join(data_dir, "r2_assets_manifest.json")
    log_file = os.path.join(data_dir, "overnight_crawler.log")
    
    if not os.path.exists(all_props_file):
        print("[-] Error: homerun_all_properties_10k.json not found!")
        return

    with open(all_props_file, 'r', encoding='utf-8') as f:
        all_items = json.load(f)

    log_msg(f"=== OVERNIGHT NPA IMAGE CRAWLER STARTED ===", log_file)
    log_msg(f"Total Master Properties: {len(all_items)} records", log_file)

    # Load State
    state = {}
    if os.path.exists(state_file):
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state = json.load(f)
        except Exception:
            state = {}

    # Migrate any existing SCB state
    old_scb_state_file = os.path.join(data_dir, "scb_images_sync_state.json")
    if os.path.exists(old_scb_state_file):
        try:
            with open(old_scb_state_file, 'r', encoding='utf-8') as f:
                old_scb = json.load(f)
                state.update(old_scb)
        except Exception:
            pass

    manifest = {}
    if os.path.exists(manifest_file):
        try:
            with open(manifest_file, 'r', encoding='utf-8') as f:
                manifest = json.load(f)
        except Exception:
            manifest = {}

    old_manifest_file = os.path.join(data_dir, "scb_assets_manifest.json")
    if os.path.exists(old_manifest_file):
        try:
            with open(old_manifest_file, 'r', encoding='utf-8') as f:
                old_m = json.load(f)
                manifest.update(old_m)
        except Exception:
            pass

    log_msg(f"Already synced so far: {len(state)} properties", log_file)

    # Process pools in priority order: SCB -> SAM -> TTB
    pools = ['SCB', 'SAM', 'TTB']
    total_uploaded = 0
    start_time = time.time()

    for pool in pools:
        pool_items = [it for it in all_items if it.get('bank_pool') == pool]
        pending = [it for it in pool_items if it['id'] not in state]
        log_msg(f"\n--- Starting Pool [{pool}]: {len(pending)} pending / {len(pool_items)} total ---", log_file)
        
        for idx, item in enumerate(pending):
            p_id = item['id']
            code = item.get('code', 'N/A')
            title = str(item.get('title', 'Unknown'))
            pool_lower = pool.lower()
            
            # Fetch detail with media
            detail_url = f"https://homerun-platform-api-prod-645188686833.asia-southeast1.run.app/api/web/group-buy/{pool_lower}/properties/{p_id}?include=media"
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

            # Fix SAM URL if pointing to dead npa.sam.or.th subdomain
            if thumb_url and 'npa.sam.or.th' in thumb_url:
                thumb_url = thumb_url.replace('npa.sam.or.th', 'www.sam.or.th')

            prop_assets = {
                "id": p_id,
                "pool": pool,
                "code": code,
                "title": title,
                "price": item.get('price'),
                "thumbnail": None,
                "gallery": []
            }

            img_count = 0
            browser_header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0'}

            # 1. Upload Thumbnail
            if thumb_url:
                try:
                    t_req = urllib.request.Request(thumb_url, headers=browser_header)
                    with urllib.request.urlopen(t_req, context=ctx, timeout=5) as r:
                        img_bytes = r.read()
                        if len(img_bytes) > 500:
                            ctype = r.headers.get('content-type', 'image/jpeg')
                            ext = "png" if "png" in ctype else "jpg"
                            r2_key = f"{pool_lower}/{p_id}/thumb.{ext}"
                            put_object_r2(r2_key, img_bytes, ctype)
                            prop_assets["thumbnail"] = f"{CDN_BASE}/{r2_key}"
                            img_count += 1
                            total_uploaded += 1
                except Exception:
                    pass

            # 2. Upload Gallery (up to 4 key images)
            for g_idx, g in enumerate(gallery[:4]):
                g_url = g.get('url')
                if g_url:
                    if 'npa.sam.or.th' in g_url:
                        g_url = g_url.replace('npa.sam.or.th', 'www.sam.or.th')
                    try:
                        g_req = urllib.request.Request(g_url, headers=browser_header)
                        with urllib.request.urlopen(g_req, context=ctx, timeout=5) as r:
                            img_bytes = r.read()
                            if len(img_bytes) > 500:
                                ctype = r.headers.get('content-type', 'image/jpeg')
                                ext = "png" if "png" in ctype else "jpg"
                                r2_key = f"{pool_lower}/{p_id}/gallery_{g_idx}.{ext}"
                                put_object_r2(r2_key, img_bytes, ctype)
                                prop_assets["gallery"].append(f"{CDN_BASE}/{r2_key}")
                                img_count += 1
                                total_uploaded += 1
                    except Exception:
                        pass
                time.sleep(0.12) # Gentle stealth pause between images

            # Save to state and manifest
            state[p_id] = {
                "pool": pool,
                "code": code,
                "synced_at": datetime.now().isoformat(),
                "images_count": img_count
            }
            manifest[p_id] = prop_assets

            if (idx + 1) % 10 == 0 or (idx + 1) == len(pending):
                log_msg(f"[{pool} {idx+1}/{len(pending)}] Total R2 Done: {len(state)}/10672 (Last: {code} -> {img_count} imgs)", log_file)

            # Checkpoint save state every 20 items
            if (idx + 1) % 20 == 0:
                with open(state_file, 'w', encoding='utf-8') as f:
                    json.dump(state, f, ensure_ascii=False, indent=2)
                with open(manifest_file, 'w', encoding='utf-8') as f:
                    json.dump(manifest, f, ensure_ascii=False, indent=2)

            # Stealth delay between properties (0.25s)
            time.sleep(0.25)

        # End of pool checkpoint save
        with open(state_file, 'w', encoding='utf-8') as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        with open(manifest_file, 'w', encoding='utf-8') as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)

    elapsed_h = (time.time() - start_time) / 3600
    log_msg(f"\n================ OVERNIGHT RUN COMPLETE ================", log_file)
    log_msg(f"Total Properties in R2: {len(state)}/10672", log_file)
    log_msg(f"Total Images Uploaded : {total_uploaded}", log_file)
    log_msg(f"Elapsed Time          : {elapsed_h:.2f} hours", log_file)
    log_msg(f"=========================================================", log_file)

if __name__ == "__main__":
    run_overnight_crawler()
