import json
import csv
import os

REPO_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
PAMCO_PATH = os.path.join(REPO_DIR, "data", "pamco_property_master.json")
G_TARGET_DIR = r"G:\Twin_Brain"
LOCAL_TARGET_DIR = os.path.join(REPO_DIR, "data")

if not os.path.exists(G_TARGET_DIR):
    try:
        os.makedirs(G_TARGET_DIR)
    except:
        pass

with open(PAMCO_PATH, "r", encoding="utf-8") as f:
    pamco_raw = json.load(f)

if isinstance(pamco_raw, dict):
    pamco_items = list(pamco_raw.values())
else:
    pamco_items = pamco_raw

csv_rows = []
for p in pamco_items:
    pid = p.get("id") or p.get("code") or ""
    pcode = p.get("code") or ""
    title = p.get("title") or ""
    cat = p.get("category") or ""
    price = p.get("price") or ""
    prov = p.get("province") or ""
    dist = p.get("district") or ""
    tel = p.get("telAO") or ""
    landid = p.get("landid") or ""
    houseid = p.get("houseid") or ""
    lat = p.get("latitude") or ""
    lng = p.get("longitude") or ""

    csv_rows.append({
        "รหัสทรัพย์": pid,
        "รหัสย่อ": pcode,
        "ชื่อทรัพย์": title,
        "ประเภท": cat,
        "ราคา": price,
        "จังหวัด": prov,
        "อำเภอ/เขต": dist,
        "เบอร์เจ้าหน้าที่_AMC": tel,
        "เลขโฉนด": landid,
        "บ้านเลขที่": houseid,
        "พิกัด_Lat": lat,
        "พิกัด_Lng": lng
    })

fieldnames = ["รหัสทรัพย์", "รหัสย่อ", "ชื่อทรัพย์", "ประเภท", "ราคา", "จังหวัด", "อำเภอ/เขต", "เบอร์เจ้าหน้าที่_AMC", "เลขโฉนด", "บ้านเลขที่", "พิกัด_Lat", "พิกัด_Lng"]

# Save Local
local_csv = os.path.join(LOCAL_TARGET_DIR, "PAMCO_Officer_Directory.csv")
with open(local_csv, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(csv_rows)
print(f"[OK] Exported {len(csv_rows)} rows to {local_csv}")

# Save G: Drive
if os.path.exists("G:\\"):
    g_csv = os.path.join(G_TARGET_DIR, "PAMCO_Officer_Directory.csv")
    with open(g_csv, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"[OK] Exported to Flash Drive: {g_csv}")
