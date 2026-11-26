import hashlib
import hmac
import os
import ssl
import sys
import urllib.request
from datetime import datetime, timezone

ACCESS_KEY = os.environ.get("R2_ACCESS_KEY_ID", "").strip()
SECRET_KEY = os.environ.get("R2_SECRET_ACCESS_KEY", "").strip()
ACCOUNT_ID = os.environ.get("R2_ACCOUNT_ID", "").strip()
BUCKET = os.environ.get("R2_BUCKET", "siwasup-npa-assets").strip()

if not (ACCESS_KEY and SECRET_KEY and ACCOUNT_ID):
    print("[R2 CI] Missing R2_ACCESS_KEY_ID / R2_SECRET_ACCESS_KEY / R2_ACCOUNT_ID secrets. Skipping R2 upload.")
    sys.exit(0)

ENDPOINT = f"https://{ACCOUNT_ID}.r2.cloudflarestorage.com"
ctx = ssl.create_default_context()


def _sign(key: bytes, msg: str) -> bytes:
    return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()


def _sig_key(key: str, date_stamp: str, region: str, service: str) -> bytes:
    k_date = _sign(("AWS4" + key).encode("utf-8"), date_stamp)
    k_region = _sign(k_date, region)
    k_service = _sign(k_region, service)
    return _sign(k_service, "aws4_request")


def put_object_r2(key_name: str, data: bytes, content_type: str) -> int:
    now = datetime.now(timezone.utc)
    amz_date = now.strftime("%Y%m%dT%H%M%SZ")
    date_stamp = now.strftime("%Y%m%d")
    payload_hash = hashlib.sha256(data).hexdigest()
    host = f"{ACCOUNT_ID}.r2.cloudflarestorage.com"
    canonical_uri = f"/{BUCKET}/{key_name}"
    canonical_headers = (
        f"content-type:{content_type}\n"
        f"host:{host}\n"
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
        req = urllib.request.Request(
            f"{ENDPOINT}{canonical_uri}",
            data=data,
            headers={
                "Content-Type": content_type,
                "x-amz-date": amz_date,
                "x-amz-content-sha256": payload_hash,
                "Authorization": auth_header,
            },
            method="PUT",
        )
        try:
            with urllib.request.urlopen(req, context=ctx, timeout=60) as resp:
                return resp.status
        except Exception:
            if attempt == 2:
                raise
    return 0


def main():
    targets = [
        ("siwasup_all_properties.json", "application/json; charset=utf-8"),
        ("siwasup_all_properties.js", "application/javascript; charset=utf-8"),
        ("data/catalog_index.json", "application/json; charset=utf-8"),
    ]
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    for fname, ctype in targets:
        fpath = os.path.join(base_dir, fname)
        if not os.path.exists(fpath):
            print(f"[R2 CI] Missing {fname}, skipping")
            continue
        with open(fpath, "rb") as f:
            raw = f.read()
        status = put_object_r2(fname, raw, ctype)
        print(f"[R2 CI] Uploaded {fname} ({len(raw)} bytes) -> HTTP {status}")


if __name__ == "__main__":
    main()
