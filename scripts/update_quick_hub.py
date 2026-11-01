import os
import re

HUB_PATH = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\executive_quick_hub.html"

with open(HUB_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# We want to replace the entire ACTIVE TEST ZONE div with the new upgraded version
active_zone_pattern = r"(<!-- =+ -->\s*<!-- 🔴 ACTIVE TEST ZONE.*?-->\s*<div style=\"background: linear-gradient\(135deg, rgba\(239, 68, 68, 0\.16\).*?<!-- SECTION 0: PERSONALIZED SQUAD HUB SYSTEM)"

new_active_zone = """<!-- ============================================================ -->
    <!-- 🔴 ACTIVE TEST ZONE (ทดสอบเรื่องนี้: เปิดบนมือถือ 1 คลิก ไม่ต้องก๊อปเข้า LINE) -->
    <!-- ============================================================ -->
    <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.16) 0%, rgba(15, 23, 42, 0.95) 100%); border: 2px solid #EF4444; border-radius: 24px; padding: 22px 20px; margin-bottom: 30px; box-shadow: 0 12px 36px rgba(239, 68, 68, 0.25);">
        
        <!-- Header with RED Badge -->
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; margin-bottom: 16px; border-bottom: 1px solid rgba(239, 68, 68, 0.25); padding-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                <span style="display: inline-flex; align-items: center; gap: 6px; background: #EF4444; color: #FFFFFF; font-size: 11.5px; font-weight: 700; padding: 5px 14px; border-radius: 9999px; letter-spacing: 0.5px; box-shadow: 0 2px 10px rgba(239, 68, 68, 0.6);">
                    <span style="display: inline-block; width: 8px; height: 8px; background: #FFF; border-radius: 50%; animation: pulse 1.5s infinite;"></span>
                    <span>ทดสอบเรื่องนี้บนมือถือ (ACTIVE MOBILE TEST)</span>
                </span>
                <span style="font-size: 15px; font-weight: 700; color: #F8FAFC;">
                    ศูนย์ทดสอบด่วน: ตู้กุญแจ Keybox • นามบัตร Alpha 6 คน • น้องศิวา AI 24 ชม.
                </span>
            </div>
            <span style="font-size: 12px; color: #FCA5A5; font-weight: 500;">
                ⚡ เปิด 1 คลิกบนมือถือ ไม่ต้องก๊อปลิงก์ลง LINE ให้แชทดันหาย
            </span>
        </div>

        <!-- Spotlight Card: 🔑 Keybox Interactive Sandbox & Stress Tester -->
        <div style="background: linear-gradient(135deg, rgba(245, 158, 11, 0.18) 0%, rgba(15, 23, 42, 0.8) 100%); border: 1.5px solid #F59E0B; border-radius: 18px; padding: 14px 16px; margin-bottom: 16px; display: flex; flex-direction: column; gap: 10px;">
            <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 8px;">
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span style="font-size: 22px;">🔑</span>
                    <div>
                        <div style="font-size: 13.5px; font-weight: 700; color: #F8FAFC;">
                            Siwasup Smart Keybox Live Roleplay &amp; Stress Tester (เปิดเทสต์บนโต๊ะวันเปิดตัว)
                        </div>
                        <div style="font-size: 11px; color: #CBD5E1;">
                            ทดสอบคอขวด 1-6 คน • ลองเป็นพี่ลิลลี่ตรวจสิทธิ์ • ลองเป็น Agent กดรหัส OTP ปลดล็อกตู้จริง
                        </div>
                    </div>
                </div>
                <a href="https://assets.siwasup.com/siwasup_keybox_interactive_roleplay.html" target="_blank" style="background: linear-gradient(135deg, #F59E0B, #D97706); color: #0F172A; font-size: 12px; font-weight: 800; padding: 8px 18px; border-radius: 12px; text-decoration: none; box-shadow: 0 4px 14px rgba(245, 158, 11, 0.4); display: inline-flex; align-items: center; gap: 6px;">
                    <span>🚀 เปิดทดสอบสด (Live Sandbox)</span>
                </a>
            </div>
            <!-- Sub Quick Links for the 3 modes -->
            <div style="display: flex; flex-wrap: wrap; gap: 6px; padding-top: 6px; border-top: 1px solid rgba(245, 158, 11, 0.25); font-size: 11px;">
                <span style="color: #E6CA85; font-weight: 600;">โหมดในระบบ:</span>
                <span style="background: rgba(255,255,255,0.06); padding: 3px 8px; border-radius: 6px; color: #E2E8F0;">🏢 1. สวมบทพี่ลิลลี่ (เทสต์คอขวด 1 - 6 คน / Batch Approve)</span>
                <span style="background: rgba(255,255,255,0.06); padding: 3px 8px; border-radius: 6px; color: #E2E8F0;">📱 2. สวมบท Agent 6 คน (กดปุ่มตู้กุญแจ OTP จริง)</span>
                <span style="background: rgba(255,255,255,0.06); padding: 3px 8px; border-radius: 6px; color: #E2E8F0;">🖥️ 3. Dual Screen (ฉายสองจอโปรเจกเตอร์)</span>
            </div>
        </div>

        <!-- Section 1: 📇 Agent Cards for Alpha Agents -->
        <div style="margin-bottom: 14px;">
            <div style="font-size: 12px; font-weight: 600; color: #E2E8F0; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
                <span>📇</span>
                <span>1. นามบัตรตัวแทน Alpha 6 คน (เปิดดู Golden Emblem บนมือถือ):</span>
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                <a href="https://assets.siwasup.com/agent_profile.html?code=S98" target="_blank" style="background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); color: #FCA5A5; font-size: 12px; font-weight: 600; padding: 8px 14px; border-radius: 12px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; transition: all 0.2s;">
                    <span>🦁 S98 คุณแป้ง (วัชรพล-สายไหม)</span>
                </a>
                <a href="https://assets.siwasup.com/agent_profile.html?code=S120" target="_blank" style="background: rgba(194, 164, 96, 0.15); border: 1px solid rgba(194, 164, 96, 0.4); color: #E6CA85; font-size: 12px; font-weight: 600; padding: 8px 14px; border-radius: 12px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; transition: all 0.2s;">
                    <span>🦅 S120 คุณอ้อน (นนทบุรี-บางใหญ่)</span>
                </a>
                <a href="https://assets.siwasup.com/agent_profile.html?code=S117" target="_blank" style="background: rgba(239, 68, 68, 0.15); border: 1px solid rgba(239, 68, 68, 0.4); color: #FCA5A5; font-size: 12px; font-weight: 600; padding: 8px 14px; border-radius: 12px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; transition: all 0.2s;">
                    <span>🦁 S117 คุณแอ๊ด (บางนา-สมุทรปราการ)</span>
                </a>
                <a href="https://assets.siwasup.com/agent_profile.html?code=S90" target="_blank" style="background: rgba(148, 163, 184, 0.15); border: 1px solid rgba(148, 163, 184, 0.35); color: #CBD5E1; font-size: 12px; font-weight: 600; padding: 8px 14px; border-radius: 12px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; transition: all 0.2s;">
                    <span>🐺 S90 คุณนัท (ตลิ่งชัน)</span>
                </a>
                <a href="https://assets.siwasup.com/agent_profile.html?code=S94" target="_blank" style="background: rgba(148, 163, 184, 0.15); border: 1px solid rgba(148, 163, 184, 0.35); color: #CBD5E1; font-size: 12px; font-weight: 600; padding: 8px 14px; border-radius: 12px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; transition: all 0.2s;">
                    <span>🐺 S94 คุณหลิว (พุทธมณฑลสาย 2)</span>
                </a>
                <a href="https://assets.siwasup.com/agent_profile.html?code=S113" target="_blank" style="background: rgba(148, 163, 184, 0.15); border: 1px solid rgba(148, 163, 184, 0.35); color: #CBD5E1; font-size: 12px; font-weight: 600; padding: 8px 14px; border-radius: 12px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; transition: all 0.2s;">
                    <span>🐺 S113 คุณไห้ (ดาวคะนอง-ธนบุรี)</span>
                </a>
                <a href="https://assets.siwasup.com/agent_profile.html?code=S98&mode=client" target="_blank" style="background: linear-gradient(135deg, #10B981, #059669); color: #FFFFFF; font-size: 12px; font-weight: 700; padding: 8px 16px; border-radius: 12px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; box-shadow: 0 4px 12px rgba(16, 185, 129, 0.35);">
                    <span>👥 พรีวิวมุมมองลูกค้า (Client View - ไร้สัตว์ 100%)</span>
                </a>
            </div>
        </div>

        <!-- Section 2: 📊 3 Metric Options for Gool -->
        <div style="margin-bottom: 14px;">
            <div style="font-size: 12px; font-weight: 600; color: #E2E8F0; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
                <span>📊</span>
                <span>2. สลับดูตัวเลข 3 แบบ (สำหรับให้กูลเลือก):</span>
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                <a href="https://assets.siwasup.com/agent_profile.html?code=S98&metric=opt1" target="_blank" style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); color: #6EE7B7; font-size: 11.5px; font-weight: 600; padding: 7px 13px; border-radius: 10px; text-decoration: none;">
                    🌟 แบบ 1: สบายใจ/ฟรี/สินเชื่อ (แนะนำ 👍)
                </a>
                <a href="https://assets.siwasup.com/agent_profile.html?code=S98&metric=opt2" target="_blank" style="background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.2); color: #E2E8F0; font-size: 11.5px; font-weight: 600; padding: 7px 13px; border-radius: 10px; text-decoration: none;">
                    🏆 แบบ 2: สายโปร/ปิดสำเร็จ/ตอบไว
                </a>
                <a href="https://assets.siwasup.com/agent_profile.html?code=S98&metric=opt3" target="_blank" style="background: rgba(255, 255, 255, 0.08); border: 1px solid rgba(255, 255, 255, 0.2); color: #E2E8F0; font-size: 11.5px; font-weight: 600; padding: 7px 13px; border-radius: 10px; text-decoration: none;">
                    🏡 แบบ 3: ปรับคำซอฟต์ (ตามร่างคุณต้น)
                </a>
            </div>
        </div>

        <!-- Section 3: 💬 LINE Bot น้องศิวา & เครื่องมือดูด Log -->
        <div>
            <div style="font-size: 12px; font-weight: 600; color: #E2E8F0; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
                <span>💬</span>
                <span>3. น้องศิวา AI (Cloud Server 24 ชม.) &amp; ตรวจสอบ Log:</span>
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                <a href="https://line.me/R/ti/p/@813nyyia" target="_blank" style="background: linear-gradient(135deg, #06C755, #059669); color: #FFFFFF; font-size: 12px; font-weight: 700; padding: 8px 16px; border-radius: 12px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px; box-shadow: 0 4px 12px rgba(6, 199, 85, 0.35);">
                    <span>📲 ทักคุย LINE OA น้องศิวา (@813nyyia)</span>
                </a>
                <a href="https://assets.siwasup.com/offline_log_exporter.html" target="_blank" style="background: rgba(245, 158, 11, 0.15); border: 1px solid rgba(245, 158, 11, 0.4); color: #FCD34D; font-size: 11.5px; font-weight: 700; padding: 7px 14px; border-radius: 10px; text-decoration: none; display: inline-flex; align-items: center; gap: 6px;">
                    <span>📋 ตัวดูด Chat Log ออฟไลน์ (Cloud • ฟอนต์ Tahoma)</span>
                </a>
                <a href="https://assets.siwasup.com/line_chat_monitor.html" target="_blank" style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); color: #6EE7B7; font-size: 11.5px; font-weight: 600; padding: 7px 13px; border-radius: 10px; text-decoration: none;">
                    <span>💬 มอนิเตอร์แชทน้องศิวา AI (Live)</span>
                </a>
                <a href="https://assets.siwasup.com/scoring_debate_dashboard.html" target="_blank" style="background: rgba(194, 164, 96, 0.15); border: 1px solid rgba(194, 164, 96, 0.4); color: #E6CA85; font-size: 11.5px; font-weight: 600; padding: 7px 13px; border-radius: 10px; text-decoration: none;">
                    <span>📊 แดชบอร์ดเกณฑ์คะแนน 2-Track</span>
                </a>
            </div>
        </div>

    </div>

    <!-- SECTION 0: PERSONALIZED SQUAD HUB SYSTEM"""

match = re.search(active_zone_pattern, content, re.DOTALL)
if match:
    updated = content[:match.start()] + new_active_zone + content[match.end():]
    with open(HUB_PATH, "w", encoding="utf-8") as f:
        f.write(updated)
    print("[OK] Successfully updated ACTIVE TEST ZONE in executive_quick_hub.html!")
else:
    print("[ERROR] Pattern not found in executive_quick_hub.html")
