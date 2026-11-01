import os
import sys

sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
from overnight_r2_crawler import put_object_r2

HUB_PATH = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\executive_quick_hub.html"

with open(HUB_PATH, "r", encoding="utf-8") as f:
    html = f.read()

matrix_block = """
            <!-- ============================================================== -->
            <!-- 5-PILLAR OFFICE PERMISSION & ACCESS MATRIX (RBAC) -->
            <!-- ============================================================== -->
            <div style="background: rgba(15, 23, 42, 0.85); border: 1px solid rgba(245, 158, 11, 0.35); border-radius: 16px; padding: 16px; margin-top: 14px;">
                <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; border-bottom: 1px solid rgba(255,255,255,0.08); padding-bottom: 8px;">
                    <div>
                        <div style="font-size: 13px; font-weight: 800; color: #FFFFFF; display: flex; align-items: center; gap: 6px;">
                            <span>🛡️ โครงสร้างสิทธิ์ทีมงานออฟฟิศ 5 เสาหลัก (Role-Based Access Control)</span>
                        </div>
                        <div style="font-size: 11px; color: #94A3B8;">ทุกคนมี Standard Admin เป็นฐาน + สิทธิ์เฉพาะทางที่ติ๊กมอบหมายเพิ่มเติม</div>
                    </div>
                    <a href="https://assets.siwasup.com/agent_registration.html" target="_blank" style="background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.3); color: #F59E0B; font-size: 11px; font-weight: 700; padding: 4px 12px; border-radius: 8px; text-decoration: none;">
                        จัดการสิทธิ์ทีมงาน &rarr;
                    </a>
                </div>

                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 10px; font-size: 11px;">
                    
                    <!-- 1. Gool & Bua -->
                    <div style="background: #090D16; border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 12px; padding: 12px;">
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
                            <span style="font-weight: 800; color: #F59E0B; font-size: 12px;">👑 คุณกูล & คุณบัว</span>
                            <span style="background: rgba(245, 158, 11, 0.2); color: #FCD34D; font-size: 9px; font-weight: 800; padding: 2px 6px; border-radius: 6px;">บอสใหญ่ / บัวทำแทน</span>
                        </div>
                        <div style="color: #CBD5E1; line-height: 1.5; font-size: 10.5px;">
                            • <strong>Standard Admin:</strong> สิทธิ์องค์กรเต็มรูปแบบ<br>
                            • <strong style="color: #F59E0B;">💰 สิทธิ์เคาะแก้ราคาบ้าน & ส่วนลดพิเศษ</strong><br>
                            • <strong>👑 สิทธิ์ผู้บริหาร:</strong> ดูยอด KPI & คอมมิชชัน<br>
                            • <strong>📊 ตรวจลีด:</strong> เช็กแชทและประวัติลูกค้า<br>
                            • <strong>🏷️ สิทธิ์คัดทรัพย์เด่น:</strong> คัด NPA ขึ้นหน้าแรก
                        </div>
                    </div>

                    <!-- 2. P'Lily -->
                    <div style="background: #090D16; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 12px;">
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
                            <span style="font-weight: 800; color: #10B981; font-size: 12px;">🔑 พี่ลิลลี่ (ท่าข้าม 12)</span>
                            <span style="background: rgba(16, 185, 129, 0.2); color: #6EE7B7; font-size: 9px; font-weight: 800; padding: 2px 6px; border-radius: 6px;">Head of Viewing</span>
                        </div>
                        <div style="color: #CBD5E1; line-height: 1.5; font-size: 10.5px;">
                            • <strong>Standard Admin:</strong> ตรวจดูข้อมูลทรัพย์ทั้งหมด<br>
                            • <strong style="color: #10B981;">🔑 คุมกุญแจ 100%:</strong> อนุมัติรหัส OTP ใน 3 วินาที<br>
                            • <strong>📅 เลื่อนนัด:</strong> สลาย OTP เดิม & ออก OTP ใหม่<br>
                            • <strong>🚫 ยกเลิกฉุกเฉิน:</strong> รับมือฝนตกน้ำท่วม/นิติปิดไฟ<br>
                            • <em>*ล็อกเมนูเทคนิคและแก้ราคา เพื่อความรวดเร็ว*</em>
                        </div>
                    </div>

                    <!-- 3. Khun Jeab -->
                    <div style="background: #090D16; border: 1px solid rgba(59, 130, 246, 0.3); border-radius: 12px; padding: 12px;">
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
                            <span style="font-weight: 800; color: #60A5FA; font-size: 12px;">📋 คุณเจี๊ยบ</span>
                            <span style="background: rgba(59, 130, 246, 0.2); color: #93C5FD; font-size: 9px; font-weight: 800; padding: 2px 6px; border-radius: 6px;">Co-Broker Lead</span>
                        </div>
                        <div style="color: #CBD5E1; line-height: 1.5; font-size: 10.5px;">
                            • <strong>Standard Admin:</strong> ดูแลทีมงาน & ตัวแทน<br>
                            • <strong style="color: #60A5FA;">📊 ตรวจลีด & แชท:</strong> อนุมัติตัวแทนใหม่<br>
                            • <strong>🔑 สำรองกุญแจ OTP:</strong> ช่วยอนุมัติแทนเมื่อลิลลี่ติดงาน<br>
                            • <strong>🏷️ ประสานทรัพย์เด่น:</strong> เช็กสต๊อกบ้านพร้อมขาย<br>
                            • <em>*ล็อกเมนูเซิร์ฟเวอร์และแก้ราคา*</em>
                        </div>
                    </div>

                    <!-- 4. Khun Ton -->
                    <div style="background: #090D16; border: 1px solid rgba(244, 63, 94, 0.3); border-radius: 12px; padding: 12px;">
                        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px;">
                            <span style="font-weight: 800; color: #FB7185; font-size: 12px;">💻 คุณต้น (NASSTY)</span>
                            <span style="background: rgba(244, 63, 94, 0.2); color: #FDA4AF; font-size: 9px; font-weight: 800; padding: 2px 6px; border-radius: 6px;">Tech Architect</span>
                        </div>
                        <div style="color: #CBD5E1; line-height: 1.5; font-size: 10.5px;">
                            • <strong>Standard Admin:</strong> สิทธิ์องค์กรเต็มรูปแบบ<br>
                            • <strong style="color: #FB7185;">⚙️ Super Tech Admin:</strong> คุม Render & LINE Bot<br>
                            • <strong>💰 สิทธิ์แก้ราคา:</strong> คอนฟิกตัวเลขและคอมมิชชัน<br>
                            • <strong>🏦 ท่อดูด NPA:</strong> คุมคลังทรัพย์ 59,000 หลัง<br>
                            • <strong>🗑️ Data Cleansing:</strong> ควบคุมความปลอดภัย 90 วัน
                        </div>
                    </div>

                </div>
            </div>
"""

target = '<span>📝 ฟอร์มลงทะเบียนทีมงานออฟฟิศ & นามบัตร</span>\n                </a>'
if target in html and "โครงสร้างสิทธิ์ทีมงานออฟฟิศ 5 เสาหลัก" not in html:
    html = html.replace(target, target + "\n            </div>" + matrix_block + "<div>", 1)
    # clean up wrapping if needed
    with open(HUB_PATH, "w", encoding="utf-8") as f:
        f.write(html)
    print("[*] Successfully patched executive_quick_hub.html!")
    
    # Upload to R2
    print("[*] Uploading updated executive_quick_hub.html to Cloudflare R2...")
    st = put_object_r2("executive_quick_hub.html", html.encode("utf-8"), "text/html; charset=utf-8")
    print(f"[OK] Upload Status: {st}")
else:
    print("[!] Target marker not found or already patched")
