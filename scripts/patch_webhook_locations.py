# -*- coding: utf-8 -*-
import os, re

path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts\line_gemini_webhook.py"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

new_loc_map = """LOC_MAP = {
    # โซนตะวันออก & มีนบุรี & กรุงเทพฯ ตะวันออก (เน้นย้ำความแม่นยำ 100%)
    "มีนบุรี": ["Min Buri", "มีนบุรี", "Khlong Sam Wa", "คลองสามวา"],
    "คลองสามวา": ["Khlong Sam Wa", "คลองสามวา", "Min Buri", "มีนบุรี"],
    "หนองจอก": ["Nong Chok", "หนองจอก", "Min Buri", "มีนบุรี"],
    "คันนายาว": ["Khan Na Yao", "Khanna Yao", "คันนายาว", "รามอินทรา"],
    "รามอินทรา": ["Khan Na Yao", "Min Buri", "Bang Khen", "Khlong Sam Wa", "รามอินทรา", "บางชัน"],
    "บางชัน": ["Khlong Sam Wa", "Khan Na Yao", "บางชัน", "รามอินทรา"],
    "ลาดกระบัง": ["Lat Krabang", "ลาดกระบัง", "สุวรรณภูมิ"],
    "สะพานสูง": ["Saphan Sung", "สะพานสูง"],
    "บึงกุ่ม": ["Bung Kum", "บึงกุ่ม", "นวมินทร์"],
    "นวมินทร์": ["Bung Kum", "Lat Phrao", "นวมินทร์"],
    "บางกะปิ": ["Bang Kapi", "บางกะปิ", "เสรีไทย"],
    "เสรีไทย": ["Bang Kapi", "Bung Kum", "เสรีไทย"],
    "ประเวศ": ["Prawet", "ประเวศ", "ศรีนครินทร์", "สวนหลวง"],
    "สวนหลวง": ["Suan Luang", "สวนหลวง", "พัฒนาการ"],
    "พัฒนาการ": ["Suan Luang", "Prawet", "พัฒนาการ"],
    "บางนา": ["Bang Na", "Bang Phli", "Prawet", "บางนา"],
    "อุดมสุข": ["Bang Na", "Phra Khanong", "อุดมสุข"],
    "พระโขนง": ["Phra Khanong", "พระโขนง", "อ่อนนุช"],
    "อ่อนนุช": ["Phra Khanong", "Suan Luang", "Prawet", "อ่อนนุช"],

    # โซนเหนือ & ดอนเมือง & หลักสี่ & พหลโยธิน
    "ดอนเมือง": ["Don Mueang", "ดอนเมือง"],
    "หลักสี่": ["Lak Si", "หลักสี่", "แจ้งวัฒนะ"],
    "สายไหม": ["Sai Mai", "สายไหม", "สุขาภิบาล 5", "วัชรพล"],
    "วัชรพล": ["Sai Mai", "Bang Khen", "วัชรพล"],
    "บางเขน": ["Bang Khen", "บางเขน", "รามอินทรา", "หลักสี่"],
    "จตุจักร": ["Chatuchak", "จตุจักร", "พหลโยธิน"],
    "ลาดพร้าว": ["Lat Phrao", "ลาดพร้าว", "โชคชัย 4"],
    "วังทองหลาง": ["Wang Thong Lang", "วังทองหลาง", "ทาวน์อินทาวน์"],
    "ห้วยขวาง": ["Huai Khwang", "ห้วยขวาง", "รัชดา", "พระราม 9"],
    "รัชดา": ["Huai Khwang", "Din Daeng", "Chatuchak", "รัชดา"],
    "ดินแดง": ["Din Daeng", "ดินแดง"],
    "พญาไท": ["Phaya Thai", "พญาไท", "อารีย์", "สะพานควาย"],
    "อารีย์": ["Phaya Thai", "อารีย์"],
    "ราชเทวี": ["Rat Thewi", "ราชเทวี", "ประตูน้ำ"],
    "ปทุมวัน": ["Pathum Wan", "ปทุมวัน", "สยาม"],
    "บางซื่อ": ["Bang Su", "บางซื่อ", "เตาปูน", "วงศ์สว่าง"],
    "เตาปูน": ["Bang Su", "เตาปูน"],
    "ดุสิต": ["Dusit", "ดุสิต", "ศรีย่าน", "สามเสน"],
    "พระนคร": ["Phra Nakhon", "พระนคร", "เกาะรัตนโกสินทร์"],
    "สัมพันธวงศ์": ["Samphanthawong", "สัมพันธวงศ์", "เยาวราช"],
    "ป้อมปราบ": ["Pom Prap", "ป้อมปราบศัตรูพ่าย"],

    # โซนสุขุมวิท & เมืองชั้นใน & พระราม 3-4
    "วัฒนา": ["Watthana", "วัฒนา", "สุขุมวิท", "ทองหล่อ", "เอกมัย", "พร้อมพงษ์"],
    "ทองหล่อ": ["Watthana", "ทองหล่อ", "สุขุมวิท 55"],
    "เอกมัย": ["Watthana", "เอกมัย", "สุขุมวิท 63"],
    "คลองเตย": ["Khlong Toei", "คลองเตย", "พระราม 4"],
    "สาทร": ["Sa Thon", "สาทร", "Sathon", "สีลม"],
    "สีลม": ["Bang Rak", "สีลม", "Bangrak"],
    "บางรัก": ["Bang Rak", "บางรัก", "สีลม"],
    "ยานนาวา": ["Yannawa", "ยานนาวา", "พระราม 3", "ช่องนนทรี"],
    "พระราม 3": ["Yannawa", "Bang Kho Laem", "พระราม 3"],
    "บางคอแหลม": ["Bang Kho Laem", "บางคอแหลม", "เจริญกรุง"],
    "เจริญกรุง": ["Bang Kho Laem", "Bang Rak", "Khlong San", "เจริญกรุง"],

    # ฝั่งธนบุรี & ศิริราช & โซนตะวันตก (เดินทางเชื่อมต่อศิริราชได้สะดวกรวดเร็ว)
    "ศิริราช": ["Bangkok Noi", "Bang Phlat", "Taling Chan", "Thon Buri", "บางกอกน้อย", "บางพลัด", "ตลิ่งชัน", "ธนบุรี"],
    "พรานนก": ["Bangkok Noi", "Bang Phlat", "Taling Chan", "บางกอกน้อย", "บางพลัด", "ตลิ่งชัน"],
    "บางกอกน้อย": ["Bangkok Noi", "Bang Phlat", "Taling Chan", "บางกอกน้อย", "บางพลัด", "ตลิ่งชัน"],
    "บางกอกใหญ่": ["Bangkok Yai", "Thon Buri", "บางกอกใหญ่", "ธนบุรี"],
    "บางขุนนนท์": ["Bangkok Noi", "Taling Chan", "Bang Phlat", "บางกอกน้อย", "ตลิ่งชัน", "บางพลัด"],
    "ไฟฉาย": ["Bangkok Noi", "Taling Chan", "บางกอกน้อย", "ตลิ่งชัน"],
    "จรัญ": ["Bang Phlat", "Bangkok Noi", "บางพลัด", "บางกอกน้อย"],
    "จรัญสนิทวงศ์": ["Bang Phlat", "Bangkok Noi", "บางพลัด", "บางกอกน้อย"],
    "บางพลัด": ["Bang Phlat", "บางพลัด", "บางกอกน้อย"],
    "ปิ่นเกล้า": ["Bangkok Noi", "Bang Phlat", "Taling Chan", "บางกอกน้อย", "บางพลัด", "ตลิ่งชัน"],
    "บรมราชชนนี": ["Taling Chan", "Thawi Watthana", "Bang Phlat", "ตลิ่งชัน", "ทวีวัฒนา", "บางพลัด"],
    "พุทธมณฑล": ["Taling Chan", "Thawi Watthana", "ตลิ่งชัน", "ทวีวัฒนา"],
    "พุทธมณฑลสาย 1": ["Taling Chan", "Phasi Charoen", "ตลิ่งชัน", "ภาษีเจริญ"],
    "พุทธมณฑลสาย 2": ["Thawi Watthana", "Bang Khae", "ทวีวัฒนา", "บางแค"],
    "พุทธมณฑลสาย 3": ["Thawi Watthana", "Nong Khaem", "ทวีวัฒนา", "หนองแขม"],
    "พุทธมณฑลสาย 4": ["Nong Khaem", "Sam Phran", "กระทุ่มแบน"],
    "ราชพฤกษ์": ["Taling Chan", "Phasi Charoen", "ตลิ่งชัน", "ภาษีเจริญ"],
    "ธนบุรี": ["Thon Buri", "Bangkok Yai", "Khlong San", "ธนบุรี", "คลองสาน"],
    "คลองสาน": ["Khlong San", "Thon Buri", "คลองสาน", "ธนบุรี"],
    "ภาษีเจริญ": ["Phasi Charoen", "ภาษีเจริญ", "บางแค"],
    "บางแค": ["Bang Khae", "Phasi Charoen", "บางแค", "ภาษีเจริญ"],
    "บางบอน": ["Bang Bon", "บางบอน", "บางขุนเทียน"],
    "หนองแขม": ["Nong Khaem", "Bang Khae", "หนองแขม", "บางแค"],
    "ตลิ่งชัน": ["Taling Chan", "ตลิ่งชัน"],
    "ทวีวัฒนา": ["Thawi Watthana", "ทวีวัฒนา"],
    "พระราม 2": ["Bang Khun Thian", "Chom Thong", "พระราม 2", "ท่าข้าม", "บางขุนเทียน"],
    "ท่าข้าม": ["Bang Khun Thian", "ท่าข้าม", "พระราม 2"],
    "บางขุนเทียน": ["Bang Khun Thian", "บางขุนเทียน", "พระราม 2", "ท่าข้าม"],
    "จอมทอง": ["Chom Thong", "จอมทอง", "ดาวคะนอง"],
    "ราษฎร์บูรณะ": ["Rat Burana", "ราษฎร์บูรณะ", "สุขสวัสดิ์"],
    "ทุ่งครุ": ["Thung Khu", "ทุ่งครุ", "ประชาอุทิศ"],
    "ประชาอุทิศ": ["Thung Khu", "Rat Burana", "ประชาอุทิศ"],

    # โซนปริมณฑล & นนทบุรี & ปทุมธานี & สมุทรปราการ
    "นนทบุรี": ["Nonthaburi", "Mueang Nonthaburi", "Bang Kruai", "Bang Yai", "Pak Kret", "นนทบุรี"],
    "บางใหญ่": ["Bang Yai", "Nonthaburi", "บางใหญ่"],
    "บางกรวย": ["Bang Kruai", "Nonthaburi", "บางกรวย"],
    "บางบัวทอง": ["Bang Bua Thong", "Nonthaburi", "บางบัวทอง"],
    "ปากเกร็ด": ["Pak Kret", "Nonthaburi", "ปากเกร็ด"],
    "เมืองทอง": ["Pak Kret", "Nonthaburi", "ปากเกร็ด", "เมืองทอง"],
    "สมุทรปราการ": ["Samut Prakan", "Mueang Samut Prakan", "สมุทรปราการ"],
    "บางพลี": ["Bang Phli", "Samut Prakan", "บางพลี"],
    "บางบ่อ": ["Bang Bo", "Samut Prakan", "บางบ่อ"],
    "บางเสาธง": ["Bang Sao Thong", "Samut Prakan", "บางเสาธง"],
    "ปทุมธานี": ["Pathum Thani", "Khlong Luang", "Thanyaburi", "Lam Luk Ka", "ปทุมธานี"],
    "ลำลูกกา": ["Lam Luk Ka", "Pathum Thani", "ลำลูกกา"],
    "ธัญบุรี": ["Thanyaburi", "Pathum Thani", "ธัญบุรี"],
    "รังสิต": ["Thanyaburi", "Khlong Luang", "รังสิต", "ปทุมธานี"],
    "คลองหลวง": ["Khlong Luang", "Pathum Thani", "คลองหลวง"],
    "เชียงใหม่": ["Chiang Mai", "Mueang Chiang Mai", "เชียงใหม่"],
    "พัทยา": ["Bang Lamung", "Chon Buri", "พัทยา"],
    "ชลบุรี": ["Chon Buri", "Mueang Chon Buri", "Si Racha", "ชลบุรี"]
}"""

old_loc_map_pattern = r'LOC_MAP\s*=\s*\{.*?\n\}'
match = re.search(old_loc_map_pattern, content, re.DOTALL)
if match:
    content = content[:match.start()] + new_loc_map + content[match.end():]
    print("[+] LOC_MAP replaced successfully!")
else:
    print("[-] LOC_MAP pattern not found!")

# 2. Dynamic regex location extraction
target_loc_detect = """    # Detect new locations in current message
    new_locs = []
    for k, v in LOC_MAP.items():
        if k in query:
            new_locs.extend(v)
    if new_locs:
        ctx["locs"] = list(set(new_locs))"""

replacement_loc_detect = """    # Detect new locations in current message
    new_locs = []
    for k, v in LOC_MAP.items():
        if k in query:
            new_locs.extend(v)

    # Dynamic regex matcher for terms like โซน..., แถว..., เขต..., ย่าน...
    zone_matches = re.findall(r'(?:โซน|แถว|เขต|ย่าน|อำเภอ)\s*([ก-๙a-zA-Z0-9]+)', query)
    for zm in zone_matches:
        zm_clean = zm.strip()
        if len(zm_clean) >= 3 and zm_clean not in ["บ้าน", "คอนโด", "ที่ดิน", "ไหน", "นี้", "ราคา", "งบ"]:
            for cp in CATALOG:
                d_val = str(cp.get('d', ''))
                p_val = str(cp.get('p', ''))
                if zm_clean.lower() in d_val.lower() or zm_clean in p_val:
                    if d_val and d_val not in new_locs:
                        new_locs.append(d_val)
                    if zm_clean not in new_locs:
                        new_locs.append(zm_clean)
                    break

    if new_locs:
        ctx["locs"] = list(set(new_locs))"""

# Normalize line breaks for matching
target_loc_detect_crlf = target_loc_detect.replace('\n', '\r\n')
replacement_loc_detect_crlf = replacement_loc_detect.replace('\n', '\r\n')

if target_loc_detect_crlf in content:
    content = content.replace(target_loc_detect_crlf, replacement_loc_detect_crlf)
    print("[+] Dynamic location matcher injected (CRLF)!")
elif target_loc_detect in content:
    content = content.replace(target_loc_detect, replacement_loc_detect)
    print("[+] Dynamic location matcher injected (LF)!")
else:
    print("[-] target_loc_detect not matched!")

# 3. Clean west_expand to not include Nonthaburi
old_west = "west_expand = ['Taling Chan', 'Bangkok Noi', 'Bang Phlat', 'Thawi Watthana', 'Phasi Charoen', 'Bang Khae', 'Thon Buri', 'Nonthaburi']"
new_west = "west_expand = ['Taling Chan', 'Bangkok Noi', 'Bang Phlat', 'Thawi Watthana', 'Phasi Charoen', 'Bang Khae', 'Thon Buri']"
if old_west in content:
    content = content.replace(old_west, new_west)
    print("[+] west_expand cleaned of Nonthaburi!")

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("[*] Successfully updated scripts/line_gemini_webhook.py!")
