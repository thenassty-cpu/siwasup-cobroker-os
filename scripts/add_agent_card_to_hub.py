import os
import sys

sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
from overnight_r2_crawler import put_object_r2

path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\executive_quick_hub.html"
with open(path, "r", encoding="utf-8") as f:
    content = f.read()

target = "<!-- Card 4: Agent Quick Guide -->"
new_card = """        <!-- Card: Agent Digital Profile Card -->
        <div class="card">
            <div>
                <div class="card-top">
                    <div class="icon-box">👤</div>
                    <div class="card-meta">
                        <div class="card-title">Agent Profile Card (นามบัตรดิจิทัล)</div>
                        <div class="card-role">นามบัตรตัวแทนสไตล์เรียบง่าย & ยืนยันรูป LINE</div>
                    </div>
                </div>
                <div class="card-desc">
                    การ์ดโปรไฟล์ตัวแทนดีไซน์เรียบง่าย (Clean Minimal) ดึงรูปจาก LINE อัตโนมัติ พร้อมระบบ Smart Preview ให้กดยืนยันหรือเปลี่ยนรูป และปุ่มแชร์ 1 คลิก
                </div>
            </div>
            <div>
                <div class="card-actions">
                    <a href="https://assets.siwasup.com/agent_profile.html" target="_blank" class="btn btn-live">🌐 เปิด Live (R2)</a>
                    <a href="agent_profile.html" class="btn btn-local">💾 เปิดในเครื่อง (G:\\)</a>
                </div>
                <span class="copy-pill" onclick="copyUrl('https://assets.siwasup.com/agent_profile.html')">คัดลอกลิงก์</span>
            </div>
        </div>

        <!-- Card 4: Agent Quick Guide -->"""

if target in content:
    content = content.replace(target, new_card)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated executive_quick_hub.html!")
    
    # Upload to R2
    with open(path, "rb") as f:
        st = put_object_r2("executive_quick_hub.html", f.read(), "text/html; charset=utf-8")
    print("Uploaded executive_quick_hub.html to R2 -> Status:", st)
else:
    print("Target not found!")
