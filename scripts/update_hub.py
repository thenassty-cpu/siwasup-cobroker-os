import os

path = r'C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\executive_quick_hub.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update status pills
old_pills = '<span class="pill live">🟢 Cloudflare R2: Online (assets.siwasup.com)</span>'
new_pills = '<span class="pill live">🟢 Cloudflare R2: Online (assets.siwasup.com)</span>\n            <span class="pill live">🤖 น้องศิวา AI: Active (@813nyyia)</span>'
content = content.replace(old_pills, new_pills)

# 2. Update Bua header
old_bua = '<span>สำหรับคุณบัว (Listing Curator & Operations - เพื่อนร่วมรุ่นของต้น)</span>'
new_bua = '<span>สำหรับบัว (Listing Curator & Operations Division)</span>'
content = content.replace(old_bua, new_bua)

# 3. Add Nong Siwa Card and update Scoring card
old_card3 = '''        <!-- Card 3: Scoring Debate Dashboard -->
        <div class="card">
            <div>
                <div class="card-top">
                    <div class="icon-box">⚖️</div>
                    <div class="card-meta">
                        <div class="card-title">2-Track Scoring Debate</div>
                        <div class="card-role">แดชบอร์ดดีเบตโครงสร้างคะแนนตัวแทน</div>
                    </div>
                </div>
                <div class="card-desc">
                    เปรียบเทียบแนวคิดโมเดลคะแนนกูล (เน้นยอดปิดเร็ว) vs แนวคิดต้น/บัว (เน้นความถูกต้องและคุณภาพข้อมูล) เพื่อปรับจูนระบบให้เป็นธรรมที่สุด
                </div>
            </div>
            <div>
                <div class="card-actions">
                    <a href="https://assets.siwasup.com/scoring_debate_dashboard.html" target="_blank" class="btn btn-live">🌐 เปิด Live (R2)</a>
                    <a href="scoring_debate_dashboard.html" class="btn btn-local">💾 เปิดในเครื่อง (G:\\)</a>
                </div>
                <span class="copy-pill" onclick="copyUrl('https://assets.siwasup.com/scoring_debate_dashboard.html')">คัดลอกลิงก์</span>
            </div>
        </div>'''

new_cards = '''        <!-- Card: Nong Siwa AI Chat Monitor -->
        <div class="card" style="border-color: rgba(34, 197, 94, 0.4); background: rgba(18, 38, 28, 0.65);">
            <div>
                <div class="card-top">
                    <div class="icon-box" style="background: rgba(34, 197, 94, 0.15); border-color: rgba(34, 197, 94, 0.4);">💬</div>
                    <div class="card-meta">
                        <div class="card-title" style="color: #86EFAC;">น้องศิวา AI (LINE OA Chat Monitor)</div>
                        <div class="card-role" style="color: #4ADE80;">ระบบส่องประวัติถาม-ตอบ LINE OA & AI ผู้ช่วย 24 ชม.</div>
                    </div>
                </div>
                <div class="card-desc">
                    มอนิเตอร์แชทสดว่าตัวแทนหรือลูกค้าถามอะไรเข้ามา และน้องศิวา AI ช่วยแนะนำทรัพย์หรือตอบข้อสงสัยอย่างไร พร้อมทางลัดแอดคุยบน LINE (@813nyyia)
                </div>
            </div>
            <div>
                <div class="card-actions">
                    <a href="https://assets.siwasup.com/line_chat_monitor.html" target="_blank" class="btn btn-live" style="background: linear-gradient(135deg, #10B981, #059669); color: white;">🌐 ส่องแชทสด (Monitor)</a>
                    <a href="https://line.me/R/ti/p/@813nyyia" target="_blank" class="btn btn-local" style="background: rgba(6, 199, 85, 0.15); border-color: rgba(6, 199, 85, 0.4); color: #4ADE80;">📲 แอดคุยบน LINE</a>
                </div>
                <span class="copy-pill" onclick="copyUrl('https://assets.siwasup.com/line_chat_monitor.html')">คัดลอกลิงก์มอนิเตอร์</span>
            </div>
        </div>

        <!-- Card 3: 2-Track Scoring Engine -->
        <div class="card">
            <div>
                <div class="card-top">
                    <div class="icon-box">⚖️</div>
                    <div class="card-meta">
                        <div class="card-title">2-Track Scoring Engine (เกณฑ์คะแนน)</div>
                        <div class="card-role">โครงสร้างเกณฑ์คะแนนตัวแทนขายฉบับสมบูรณ์</div>
                    </div>
                </div>
                <div class="card-desc">
                    แยก 2 ถังอิสระ: ถังผลงานขายจริง (ปรับยศ/สิทธิ์รับ Lead) vs ถังกิจกรรม (Voucher) พร้อมกฎเหล็ก 3 ชม. ส่งคลิปรีวิวบ้านเพื่อป้องกันการดองกุญแจ
                </div>
            </div>
            <div>
                <div class="card-actions">
                    <a href="https://assets.siwasup.com/scoring_summary_light.html" target="_blank" class="btn btn-live">🌐 เปิด Live (R2)</a>
                    <a href="scoring_summary_light.html" class="btn btn-local">💾 เปิดในเครื่อง (G:\\)</a>
                </div>
                <span class="copy-pill" onclick="copyUrl('https://assets.siwasup.com/scoring_summary_light.html')">คัดลอกลิงก์</span>
            </div>
        </div>'''

content_norm = content.replace('\r\n', '\n')
old_card3_norm = old_card3.replace('\r\n', '\n')

if old_card3_norm in content_norm:
    content_norm = content_norm.replace(old_card3_norm, new_cards)
    print("Replaced Card 3 successfully!")
else:
    print("Warning: old_card3_norm not found")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content_norm)

print("Saved executive_quick_hub.html successfully!")
