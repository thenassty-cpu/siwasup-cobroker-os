import urllib.request
import json
import os
import hashlib
import hmac
from datetime import datetime

LINE_TOKEN = "nsjrJajD/02mW2tXzVo3+aJqo9VTIb6GAZF6xJfddGSTYhPdTBiV9u96/87adVQdQWAPQULuzfX2JIgwNl3CRvUGPlZU+R/6Wt2VN/CZlWCmIN8q+N7diGkWdW/+4nnOJLW57QmAHkTGTBztPeiwHgdB04t89/1O/w1cDnyilFU="
IMAGE_PATH = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\assets\rich_menu_heavy_red_gold.jpg"

headers = {
    "Authorization": f"Bearer {LINE_TOKEN}",
    "Content-Type": "application/json"
}

# 1. Check existing rich menus
req = urllib.request.Request("https://api.line.me/v2/bot/richmenu/list", headers=headers)
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode("utf-8"))
    existing_menus = data.get("richmenus", [])
    print(f"Existing menus found: {len(existing_menus)}")
    for m in existing_menus:
        print(f" - {m['richMenuId']}: {m['name']}")

# 2. Define New Heavy Red & Gold Rich Menu structure (2500x843, 3 columns)
# Col 1: x:0, y:0, w:833, h:843 -> Action: ค้นหาทรัพย์ / Search
# Col 2: x:833, y:0, w:834, h:843 -> Action: กฎเหล็ก & เรตคอม 100%
# Col 3: x:1667, y:0, w:833, h:843 -> Action: รีวิวรับสิทธิ์ Voucher
menu_payload = {
    "size": {"width": 2500, "height": 843},
    "selected": True,
    "name": "Siwasup Heavy Red-Gold",
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
                "text": "กฎเหล็ก & เรตคอม 100%"
            }
        },
        {
            "bounds": {"x": 1667, "y": 0, "width": 833, "height": 843},
            "action": {
                "type": "message",
                "text": "ส่งลิงก์คลิปรีวิวสะสมแต้ม Voucher"
            }
        }
    ]
}

# 3. Create Rich Menu
create_req = urllib.request.Request(
    "https://api.line.me/v2/bot/richmenu",
    data=json.dumps(menu_payload).encode("utf-8"),
    headers=headers,
    method="POST"
)
with urllib.request.urlopen(create_req) as resp:
    res = json.loads(resp.read().decode("utf-8"))
    new_menu_id = res["richMenuId"]
    print(f"[OK] Created new Rich Menu: {new_menu_id}")

# 4. Upload Image
with open(IMAGE_PATH, "rb") as f:
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
    print(f"[OK] Uploaded image to {new_menu_id} (Status: {resp.status})")

# 5. Set as default rich menu for all users
default_req = urllib.request.Request(
    f"https://api.line.me/v2/bot/user/all/richmenu/{new_menu_id}",
    headers=headers,
    method="POST"
)
with urllib.request.urlopen(default_req) as resp:
    print(f"[OK] Set {new_menu_id} as default Rich Menu! (Status: {resp.status})")

# 6. Delete old menus
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
                print(f"[OK] Deleted old menu: {old_id}")
        except Exception as e:
            print(f"Error deleting old menu {old_id}: {e}")

# 7. Upload to Cloudflare R2
try:
    import sys
    sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
    from overnight_r2_crawler import put_object_r2
    with open(IMAGE_PATH, "rb") as f:
        img_bytes = f.read()
    status = put_object_r2("rich_menu_heavy_red_gold.jpg", img_bytes, "image/jpeg")
    print(f"[OK] Uploaded rich_menu_heavy_red_gold.jpg to Cloudflare R2! Status: {status}")
    print("URL: https://assets.siwasup.com/rich_menu_heavy_red_gold.jpg")
except Exception as e:
    print(f"R2 upload error: {e}")

print("=== DEPLOYMENT COMPLETE ===")
