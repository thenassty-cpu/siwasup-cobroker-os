import hashlib
import hmac
import json
import os
import re
import shutil
import ssl
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
JSON_PATH = os.path.join(ROOT_DIR, "siwasup_all_properties.json")
JS_PATH = os.path.join(ROOT_DIR, "siwasup_all_properties.js")
VAULT_PATH = os.path.join(ROOT_DIR, "Siwasup_Master_Credentials_Vault.md")
BACKUP_DIR = os.path.join(ROOT_DIR, "backups")

BUCKET = "siwasup-npa-assets"
CDN_BASE = "https://assets.siwasup.com"


def load_r2_creds():
    with open(VAULT_PATH, encoding="utf-8") as f:
        txt = f.read()

    def extract_block(label):
        m = re.search(rf"{re.escape(label)}.*?```text\s*([^\s`]+)\s*```", txt, re.S)
        return m.group(1).strip() if m else ""

    return (
        extract_block("Cloudflare Account ID:"),
        extract_block("R2 Access Key ID:"),
        extract_block("R2 Secret Access Key:"),
    )


ACCOUNT_ID, ACCESS_KEY, SECRET_KEY = load_r2_creds()
HOST = f"{ACCOUNT_ID}.r2.cloudflarestorage.com"
CTX = ssl.create_default_context()


def _sign(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _sig_key(key: str, date_stamp: str, region: str, service: str) -> bytes:
    return _sign(_sign(_sign(_sign(("AWS4" + key).encode("utf-8"), date_stamp), region), service), "aws4_request")


def put_object_r2(key_name: str, data: bytes, content_type: str) -> int:
    now = datetime.now(timezone.utc)
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")
    payload_hash = hashlib.sha256(data).hexdigest()
    canonical_uri = f"/{BUCKET}/{key_name}"
    canonical_headers = (
        f"content-type:{content_type}\n"
        f"host:{HOST}\n"
        f"x-amz-content-sha256:{payload_hash}\n"
        f"x-amz-date:{amz_date}\n"
    )
    signed_headers = "content-type;host;x-amz-content-sha256;x-amz-date"
    canonical_request = f"PUT\n{canonical_uri}\n\n{canonical_headers}\n{signed_headers}\n{payload_hash}"
    credential_scope = f"{date_stamp}/auto/s3/aws4_request"
    string_to_sign = (
        f"AWS4-HMAC-SHA256\n{amz_date}\n{credential_scope}\n"
        + hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    )
    signing_key = _sig_key(SECRET_KEY, date_stamp, "auto", "s3")
    signature = hmac.new(signing_key, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    auth_header = (
        f"AWS4-HMAC-SHA256 Credential={ACCESS_KEY}/{credential_scope}, "
        f"SignedHeaders={signed_headers}, Signature={signature}"
    )

    for attempt in range(3):
        try:
            req = urllib.request.Request(
                f"https://{HOST}{canonical_uri}",
                data=data,
                method="PUT",
                headers={
                    "Host": HOST,
                    "Content-Type": content_type,
                    "x-amz-content-sha256": payload_hash,
                    "x-amz-date": amz_date,
                    "Authorization": auth_header,
                },
            )
            with urllib.request.urlopen(req, context=CTX, timeout=25) as r:
                return r.status
        except Exception:
            if attempt == 2:
                raise
    return 500


def detect_ext_and_ctype(data: bytes, hdr_ctype: str) -> tuple[str, str]:
    if data[:3] == b"\xff\xd8\xff":
        return ".jpg", "image/jpeg"
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return ".png", "image/png"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return ".webp", "image/webp"
    if "png" in (hdr_ctype or "").lower():
        return ".png", "image/png"
    if "webp" in (hdr_ctype or "").lower():
        return ".webp", "image/webp"
    return ".jpg", "image/jpeg"


def mirror_one(url: str) -> tuple[str, str | None]:
    slug = url.rstrip("/").split("/")[-1]
    slug = re.sub(r"[^A-Za-z0-9_\-]", "", slug) or hashlib.sha1(url.encode()).hexdigest()[:16]
    for attempt in range(2):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = r.read()
                ctype = r.headers.get("Content-Type", "")
            if len(data) < 500:
                return url, None
            ext, final_ctype = detect_ext_and_ctype(data, ctype)
            key = f"ktb_images/{slug}{ext}"
            st = put_object_r2(key, data, final_ctype)
            if 200 <= st < 300:
                return url, f"{CDN_BASE}/{key}"
        except Exception:
            if attempt == 1:
                return url, None
    return url, None


def main():
    os.makedirs(BACKUP_DIR, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    shutil.copy2(JSON_PATH, os.path.join(BACKUP_DIR, f"siwasup_all_properties.json.bak_{ts}"))
    if os.path.exists(JS_PATH):
        shutil.copy2(JS_PATH, os.path.join(BACKUP_DIR, f"siwasup_all_properties.js.bak_{ts}"))

    with open(JSON_PATH, encoding="utf-8") as f:
        props = json.load(f)

    urls = set()
    for p in props:
        mi = str(p.get("main_image") or "")
        if "npa.krungthai.com" in mi:
            urls.add(mi)
        for g in p.get("gallery") or []:
            gs = str(g or "")
            if "npa.krungthai.com" in gs:
                urls.add(gs)

    url_list = sorted(urls)
    print(f"[KTB R2 Sync] Found {len(url_list)} unique npa.krungthai.com image URLs.")

    url_map = {}
    ok_cnt = 0
    fail_cnt = 0
    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(mirror_one, u): u for u in url_list}
        for i, fut in enumerate(as_completed(futs), 1):
            src, dst = fut.result()
            if dst:
                url_map[src] = dst
                ok_cnt += 1
            else:
                fail_cnt += 1
            if i % 200 == 0 or i == len(url_list):
                print(f"  Progress: {i}/{len(url_list)} (ok={ok_cnt}, fail={fail_cnt})")

    updated_props = 0
    for p in props:
        changed = False
        mi = str(p.get("main_image") or "")
        if mi in url_map:
            p["main_image"] = url_map[mi]
            changed = True
        gal = p.get("gallery")
        if isinstance(gal, list) and gal:
            new_gal = [url_map.get(str(g or ""), g) for g in gal]
            if new_gal != gal:
                p["gallery"] = new_gal
                changed = True
        if changed:
            updated_props += 1

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(props, f, ensure_ascii=False, indent=2)

    if os.path.exists(JS_PATH):
        with open(JS_PATH, "r", encoding="utf-8", errors="ignore") as f:
            head = f.readline()
        prefix = head if "window." in head or "const " in head or "var " in head else "window.SIWASUP_ALL_PROPERTIES = "
        prefix = re.sub(r"=\s*\[.*", "= ", prefix.strip())
        if not prefix.endswith("= "):
            prefix = "window.SIWASUP_ALL_PROPERTIES = "
        with open(JS_PATH, "w", encoding="utf-8") as f:
            f.write(prefix + json.dumps(props, ensure_ascii=False) + ";\n")

    print(f"[KTB R2 Sync] DONE! Updated {updated_props} properties ({ok_cnt} images -> R2, {fail_cnt} failed).")


if __name__ == "__main__":
    main()
