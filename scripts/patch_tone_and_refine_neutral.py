import os

# 1. Update agent_profile.html
profile_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\agent_profile.html"
with open(profile_path, "r", encoding="utf-8") as f:
    text = f.read()

old_badge = """      <!-- Security Notice -->
      <div class="bg-emerald-50 border border-emerald-200 rounded-xl p-2 text-[10.5px] text-emerald-800 flex items-center gap-2">
        <i data-lucide="shield-check" class="w-4 h-4 text-emerald-600 shrink-0"></i>
        <span>ปลอดภัย 100%: ไม่มีชื่อหรือรูปสัตว์ ลูกค้าเห็นเฉพาะป้ายทองคำทางการ</span>
      </div>"""

new_badge = """      <!-- Security Notice -->
      <div class="bg-emerald-50 border border-emerald-200 rounded-xl p-2.5 text-[11px] text-emerald-800 flex items-center gap-2">
        <i data-lucide="shield-check" class="w-4 h-4 text-emerald-600 shrink-0"></i>
        <span>ตรวจสอบและรับรองมาตรฐานเรียบร้อย: แสดงเฉพาะข้อมูลทางการและเครื่องหมายวิชาชีพ</span>
      </div>"""

if "ไม่มีชื่อหรือรูปสัตว์" in text:
    # replace lines containing it
    lines = text.splitlines(keepends=True)
    new_lines = []
    for line in lines:
        if "ไม่มีชื่อหรือรูปสัตว์" in line:
            new_lines.append('        <span>ตรวจสอบและรับรองมาตรฐานเรียบร้อย: แสดงเฉพาะข้อมูลทางการและเครื่องหมายวิชาชีพ</span>\n')
        else:
            new_lines.append(line)
    text = "".join(new_lines)
    with open(profile_path, "w", encoding="utf-8") as f:
        f.write(text)
    print("[OK] Updated agent_profile.html")
else:
    print("[WARN] Phrase not found in agent_profile.html")

# 2. Update executive_quick_hub.html
hub_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\executive_quick_hub.html"
with open(hub_path, "r", encoding="utf-8") as f:
    hub_text = f.read()

if "ไร้สัตว์ 100%" in hub_text:
    hub_text = hub_text.replace("ไร้สัตว์ 100%", "ฉบับทางการ")
    with open(hub_path, "w", encoding="utf-8") as f:
        f.write(hub_text)
    print("[OK] Updated executive_quick_hub.html")
else:
    print("[WARN] Phrase not found in executive_quick_hub.html")
