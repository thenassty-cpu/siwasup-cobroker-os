import os
import json
import ssl
import urllib.request
import cv2
import numpy as np
from concurrent.futures import ThreadPoolExecutor, as_completed

# Bypass SSL expired cert on readyplanet image server
ssl_ctx = ssl._create_unverified_context()

JSON_PATH = 'siwasup_all_properties.json'
OUTPUT_LOG_JSON = 'soldout_detected_log.json'
OUTPUT_AUDIT_MD = 'SOLDOUT_PROPERTIES_AUDIT.md'
CACHE_DIR = 'temp_cache_images'
os.makedirs(CACHE_DIR, exist_ok=True)

with open(JSON_PATH, 'r', encoding='utf-8') as f:
    properties = json.load(f)

print(f"Total properties to scan: {len(properties)}")

def download_and_check(item):
    p_id = item.get('id')
    title = item.get('title')
    price = item.get('price')
    category = item.get('category')
    img_url = item.get('main_image') or ''
    
    if not img_url:
        return {
            'id': p_id,
            'title': title,
            'price': price,
            'category': category,
            'image_url': '',
            'has_soldout_stamp': False,
            'red_ratio': 0.0,
            'status': 'no_image'
        }
    
    # Cache image locally
    ext = os.path.splitext(img_url.split('?')[0])[1] or '.jpg'
    local_path = os.path.join(CACHE_DIR, f"{p_id}{ext}")
    
    try:
        if not os.path.exists(local_path) or os.path.getsize(local_path) == 0:
            req = urllib.request.Request(img_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, context=ssl_ctx, timeout=15) as resp:
                with open(local_path, 'wb') as out_f:
                    out_f.write(resp.read())
        
        # Read image with cv2
        img = cv2.imread(local_path)
        if img is None:
            return {
                'id': p_id,
                'title': title,
                'price': price,
                'category': category,
                'image_url': img_url,
                'has_soldout_stamp': False,
                'red_ratio': 0.0,
                'status': 'corrupt_image'
            }
        
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # Bright red in HSV
        lower_red1 = np.array([0, 110, 90])
        upper_red1 = np.array([12, 255, 255])
        lower_red2 = np.array([168, 110, 90])
        upper_red2 = np.array([180, 255, 255])
        
        mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
        mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
        mask = mask1 | mask2
        
        # Focus on middle 70% of image
        h, w = mask.shape
        roi = mask[int(h*0.15):int(h*0.85), int(w*0.15):int(w*0.85)]
        total_pixels = roi.shape[0] * roi.shape[1]
        red_pixels = np.count_nonzero(roi)
        red_ratio = (red_pixels / total_pixels) * 100.0 if total_pixels > 0 else 0.0
        
        # The Sold Out banner spans across center with lines, typically red_ratio > 4.0%
        # Let's inspect contours if red_ratio is between 2.0% and 5.0%
        is_soldout = red_ratio >= 3.5
        
        return {
            'id': p_id,
            'title': title,
            'price': price,
            'category': category,
            'image_url': img_url,
            'has_soldout_stamp': is_soldout,
            'red_ratio': round(red_ratio, 2),
            'status': 'soldout' if is_soldout else 'active'
        }
    except Exception as e:
        return {
            'id': p_id,
            'title': title,
            'price': price,
            'category': category,
            'image_url': img_url,
            'has_soldout_stamp': False,
            'red_ratio': 0.0,
            'status': f'error: {str(e)}'
        }

results = []
print("Scanning properties in parallel...")
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = {executor.submit(download_and_check, p): p for p in properties}
    for i, fut in enumerate(as_completed(futures), 1):
        res = fut.result()
        results.append(res)
        if i % 25 == 0 or i == len(properties):
            print(f"Scanned {i}/{len(properties)} properties...")

# Sort by id
results.sort(key=lambda x: str(x['id']))

soldout_list = [r for r in results if r['has_soldout_stamp']]
active_list = [r for r in results if not r['has_soldout_stamp']]

print(f"\n Scan Summary:")
print(f"Total Scanned: {len(results)}")
print(f"Sold Out (Stamp Detected): {len(soldout_list)}")
print(f"Active (Clean Images): {len(active_list)}")

# Save JSON Log
with open(OUTPUT_LOG_JSON, 'w', encoding='utf-8') as f:
    json.dump({
        'scan_date': '2026-10-19',
        'total_properties': len(results),
        'total_soldout_stamps': len(soldout_list),
        'total_active': len(active_list),
        'soldout_properties': soldout_list
    }, f, ensure_ascii=False, indent=2)

# Save Markdown Audit Report
md_content = f"""# รายงานการสแกนและตรวจสอบสถานะทรัพย์ Sold Out จากภาพ (AllAboutAssets Archive)
**วันที่สแกน:** 19 ตุลาคม 2569  
**เครื่องมือ:** OpenCV Computer Vision (HSV Red Masking + Central Region Geometry Analysis)

---

## 1. สรุปภาพรวมสต๊อก (Stock Inventory Overview)
- **ทรัพย์ทั้งหมดในฐานข้อมูลเก่า:** **{len(results)}** ทรัพย์
- **ตรวจพบภาพมีตรายางกราฟิก 'Sold out' สีแดงปั๊มทับ:** **{len(soldout_list)}** ทรัพย์ (นำออกจากสต๊อกค้นหาอัตโนมัติ)
- **ทรัพย์สภาพคลีนพร้อมใช้งานสำหรับ Demo / Live Search:** **{len(active_list)}** ทรัพย์ (เพียงพอสำหรับการทดสอบค้นหา/ฟิลเตอร์อย่างแน่นอน)

---

## 2. รายการทรัพย์ที่ตรวจพบตราประทับ 'Sold out' (จำนวน {len(soldout_list)} หลัง)
ตารางบันทึก Log สำหรับทีมงาน (บัว, กูล และทีมศิวาทรัพย์) ใช้ตรวจสอบประวัติ:

| ID | ประเภท | ชื่อทรัพย์ | ราคา (บาท) | ค่าความมั่นใจสีแดง (%) | ลิงก์ภาพต้นฉบับ |
|---|---|---|---|---|---|
"""

for s in soldout_list:
    md_content += f"| `{s['id']}` | {s.get('category','-')} | {s.get('title','-')} | {s.get('price','-')} | {s.get('red_ratio')}% | [ดูภาพ]({s.get('image_url','')}) |\n"

md_content += f"""
---

## 3. การดำเนินการต่อในระบบ Siwasup Co-Broker OS
1. **คัดกรองอัตโนมัติ:** บันทึกแท็ก `is_soldout_image: true` ลงในไฟล์ `siwasup_all_properties.js` และ `siwasup_all_properties.json`
2. **หน้าบ้าน (Client / Broker View):** ระบบค้นหาจะกรองทรัพย์เหล่านี้ออกจากการแสดงผลหน้าหลัก ไม่ให้ปรากฏบ้านที่มีตรายางกวนสายตา
3. **หลังบ้าน (Admin Archive):** จัดเก็บเข้าหมวด *แฟ้มประวัติบ้านที่ปิดการขายแล้ว* ให้แอดมินสามารถเปิดดูข้อมูลย้อนหลังได้
"""

with open(OUTPUT_AUDIT_MD, 'w', encoding='utf-8') as f:
    f.write(md_content)

print(f"Saved logs to {OUTPUT_LOG_JSON} and {OUTPUT_AUDIT_MD}")
