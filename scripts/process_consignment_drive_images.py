"""Download consignment property photos from Google Drive manifest, optimize to WebP, and upload to Cloudflare R2."""

import io
import json
import os
import sys
import time
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image, ImageOps

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from overnight_r2_crawler import put_object_r2, CDN_BASE

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST_PATH = os.path.join(ROOT_DIR, "data", "consignment_drive_manifest_20261119.json")
OUTPUT_INDEX_PATH = os.path.join(ROOT_DIR, "data", "consignment_images_index_20261119.json")

MAX_DIM = 1440
WEBP_QUALITY = 82


def download_and_optimize(file_id: str) -> tuple[bytes, int, tuple[int, int]]:
    """Fetch a public Drive file by ID, resize to max 1440px, and encode as WebP."""
    url = f"https://drive.usercontent.google.com/download?id={file_id}&export=download&confirm=t"
    last_err = None
    for attempt in range(2):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            raw = urllib.request.urlopen(req, timeout=30).read()
            im = ImageOps.exif_transpose(Image.open(io.BytesIO(raw))).convert("RGB")
            im.thumbnail((MAX_DIM, MAX_DIM), Image.Resampling.LANCZOS)
            buf = io.BytesIO()
            im.save(buf, format="WEBP", quality=WEBP_QUALITY, method=4)
            return buf.getvalue(), len(raw), im.size
        except Exception as e:
            last_err = e
            time.sleep(1.0 * (attempt + 1))
    raise RuntimeError(f"Failed {file_id}: {last_err}")


def process_one_image(task):
    prop_id, idx, file_info = task
    fid = file_info["id"]
    webp_bytes, raw_len, size = download_and_optimize(fid)
    r2_key = f"consignment_images/{prop_id}/{idx:02d}.webp"
    status = put_object_r2(r2_key, webp_bytes, "image/webp")
    if status not in (200, 201, 204):
        raise RuntimeError(f"R2 upload failed ({status}) for {r2_key}")
    return {
        "prop_id": prop_id,
        "idx": idx,
        "url": f"{CDN_BASE}/{r2_key}",
        "raw_bytes": raw_len,
        "webp_bytes": len(webp_bytes),
        "dimensions": f"{size[0]}x{size[1]}",
        "source_name": file_info["name"],
    }


def main():
    with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    tasks = []
    skipped = []
    for prop in manifest["properties"]:
        pid = prop["id"]
        img_idx = 0
        for finfo in prop["files"]:
            name_low = finfo["name"].lower()
            mime = finfo.get("mime", "")
            if not mime.startswith("image/") or name_low.endswith(".crdownload"):
                skipped.append({"prop_id": pid, "name": finfo["name"], "mime": mime})
                continue
            img_idx += 1
            tasks.append((pid, img_idx, finfo))

    print(f"[*] Queued {len(tasks)} images across {len(manifest['properties'])} properties (skipped {len(skipped)} non-image/partial files).")
    results_by_prop = {p["id"]: [] for p in manifest["properties"]}
    errors = []
    total_raw = 0
    total_webp = 0
    done = 0

    with ThreadPoolExecutor(max_workers=8) as ex:
        futs = {ex.submit(process_one_image, t): t for t in tasks}
        for fut in as_completed(futs):
            t = futs[fut]
            done += 1
            try:
                res = fut.result()
                results_by_prop[res["prop_id"]].append(res)
                total_raw += res["raw_bytes"]
                total_webp += res["webp_bytes"]
            except Exception as e:
                errors.append({"prop_id": t[0], "file_id": t[2]["id"], "name": t[2]["name"], "error": str(e)})
            if done % 100 == 0 or done == len(tasks):
                print(f"    Progress: {done}/{len(tasks)} | Raw: {total_raw/1024/1024:.1f} MB -> WebP: {total_webp/1024/1024:.1f} MB | Errors: {len(errors)}", flush=True)

    for pid in results_by_prop:
        results_by_prop[pid].sort(key=lambda x: x["idx"])

    output = {
        "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_images": sum(len(v) for v in results_by_prop.values()),
        "total_raw_mb": round(total_raw / 1024 / 1024, 2),
        "total_webp_mb": round(total_webp / 1024 / 1024, 2),
        "skipped": skipped,
        "errors": errors,
        "images_by_property": {
            pid: [item["url"] for item in items]
            for pid, items in results_by_prop.items()
        },
    }
    with open(OUTPUT_INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"[+] Done! Saved index to {OUTPUT_INDEX_PATH}")


if __name__ == "__main__":
    main()
