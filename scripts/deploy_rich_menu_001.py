import urllib.request
import json
import os
import sys
from PIL import Image

sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
from overnight_r2_crawler import put_object_r2

LINE_TOKEN = "nsjrJajD/02mW2tXzVo3+aJqo9VTIb6GAZF6xJfddGSTYhPdTBiV9u96/87adVQdQWAPQULuzfX2JIgwNl3CRvUGPlZU+R/6Wt2VN/CZlWCmIN8q+N7diGkWdW/+4nnOJLW57QmAHkTGTBztPeiwHgdB04t89/1O/w1cDnyilFU="

SRC_PNG = r"E:\TON\#Siwasub\ป้ายขาย_บัว\Rich Menu_001_Folder\Rich Menu_001.png"
DEST_DIR_TON = r"E:\TON\#Siwasub\ป้ายขาย_บัว\Rich Menu_001_Folder"
DEST_DIR_REPO = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\assets"

print("[1] Resizing image to LINE standard 2500x843...")
im = Image.open(SRC_PNG)
im_resized = im.resize((2500, 843), Image.Resampling.LANCZOS)

out_ton_png = os.path.join(DEST_DIR_TON, "Rich Menu_001_2500x843.png")
out_ton_jpg = os.path.join(DEST_DIR_TON, "Rich Menu_001_2500x843.jpg")
out_repo_png = os.path.join(DEST_DIR_REPO, "Rich Menu_001_2500x843.png")
out_repo_jpg = os.path.join(DEST_DIR_REPO, "Rich Menu_001_2500x843.jpg")

im_resized.save(out_ton_png, optimize=True)
im_resized.save(out_repo_png, optimize=True)

im_rgb = im_resized.convert("RGB")
im_rgb.save(out_ton_jpg, quality=95, optimize=True)
im_rgb.save(out_repo_jpg, quality=95, optimize=True)

print(f"    - Saved PNG: {os.path.getsize(out_ton_png)/1024:.1f} KB")
print(f"    - Saved JPG: {os.path.getsize(out_ton_jpg)/1024:.1f} KB")

# LINE API Headers
headers = {
    "Authorization": f"Bearer {LINE_TOKEN}",
    "Content-Type": "application/json"
}

# 2. Check existing menus
print("\n[2] Checking existing LINE rich menus...")
req = urllib.request.Request("https://api.line.me/v2/bot/richmenu/list", headers=headers)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode("utf-8"))
    existing_menus = data.get("richmenus", [])
    print(f"    Found {len(existing_menus)} existing menus:")
    for m in existing_menus:
        print(f"    - {m['richMenuId']}: {m['name']}")

# 3. Create New Rich Menu
print("\n[3] Creating new Rich Menu on LINE OA...")
menu_payload = {
    "size": {"width": 2500, "height": 843},
    "selected": True,
    "name": "Siwasup Rich Menu 001 (Updated 31 Oct)",
    "chatBarText": "เมนูตัวแทน",
    "areas": [
        {
            "bounds": {"x": 0, "y": 0, "width": 833, "height": 843},
            "action": {
                "type": "message",
                "text": "ค้นหาทรัพย์พร้อมขาย"
            }
        },
        {
            "bounds": {"x": 833, "y": 0, "width": 834, "height": 843},
            "action": {
                "type": "message",
                "text": "กฎเหล็ก & ค่าคอม"
            }
        },
        {
            "bounds": {"x": 1667, "y": 0, "width": 833, "height": 843},
            "action": {
                "type": "message",
                "text": "ส่งคลิป-รีวิว สะสมแต้ม"
            }
        }
    ]
}

create_req = urllib.request.Request(
    "https://api.line.me/v2/bot/richmenu",
    data=json.dumps(menu_payload).encode("utf-8"),
    headers=headers,
    method="POST"
)
with urllib.request.urlopen(create_req) as resp:
    res = json.loads(resp.read().decode("utf-8"))
    new_menu_id = res["richMenuId"]
    print(f"    [OK] Created new Rich Menu ID: {new_menu_id}")

# 4. Upload Image
print(f"\n[4] Uploading new artwork to LINE OA ({out_repo_jpg})...")
with open(out_repo_jpg, "rb") as f:
    img_data = f.read()

upload_headers = {
    "Authorization": f"Bearer {LINE_TOKEN}",
    "Content-Type": "image/jpeg"
}
upload_req = urllib.request.Request(
    f"https://api-data.line.me/v2/bot/richmenu/{new_menu_id}/content",
    data=img_data,
    headers=upload_headers,
    method="POST"
)
with urllib.request.urlopen(upload_req) as resp:
    print(f"    [OK] Uploaded image to {new_menu_id} (Status: {resp.status})")

# 5. Set as Default for all users
print(f"\n[5] Setting {new_menu_id} as default menu for all users...")
default_req = urllib.request.Request(
    f"https://api.line.me/v2/bot/user/all/richmenu/{new_menu_id}",
    headers=headers,
    method="POST"
)
with urllib.request.urlopen(default_req) as resp:
    print(f"    [OK] Set as default! (Status: {resp.status})")

# 6. Delete old menus
print("\n[6] Cleaning up old rich menus...")
for m in existing_menus:
    old_id = m["richMenuId"]
    if old_id != new_menu_id:
        try:
            del_req = urllib.request.Request(
                f"https://api.line.me/v2/bot/richmenu/{old_id}",
                headers=headers,
                method="DELETE"
            )
            with urllib.request.urlopen(del_req) as resp:
                print(f"    [OK] Deleted old menu: {old_id}")
        except Exception as e:
            print(f"    [WARN] Failed to delete {old_id}: {e}")

# 7. Upload to Cloudflare R2
print("\n[7] Uploading to Cloudflare R2...")
st1 = put_object_r2("rich_menu_001_2500x843.jpg", img_data, "image/jpeg")
with open(out_repo_png, "rb") as f:
    png_data = f.read()
st2 = put_object_r2("rich_menu_001_2500x843.png", png_data, "image/png")
print(f"    [R2] rich_menu_001_2500x843.jpg -> Status: {st1}")
print(f"    [R2] rich_menu_001_2500x843.png -> Status: {st2}")

print("\n🎉 === RICH MENU 001 LIVE DEPLOYMENT COMPLETE! ===")
