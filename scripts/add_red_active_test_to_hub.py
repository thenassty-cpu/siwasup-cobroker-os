# -*- coding: utf-8 -*-
import os
import sys

TARGET_PATH = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\executive_quick_hub.html"

with open(TARGET_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Add keyframes pulse if not present
if "@keyframes pulse" not in content:
    content = content.replace("</style>", """
        @keyframes pulse {
            0%, 100% { opacity: 1; transform: scale(1); }
            50% { opacity: 0.4; transform: scale(0.85); }
        }
    </style>""")

RED_ACTIVE_TEST_HTML = """
    <!-- ============================================================ -->
    <!-- 🔴 ACTIVE TEST ZONE (ทดสอบเรื่องนี้: เปิดบนมือถือ 1 คลิก ไม่ต้องก๊อปเข้า LINE) -->
    <!-- ============================================================ -->
    <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.16) 0%, rgba(15, 23, 42, 0.95) 100%); border: 2px solid #EF4444; border-radius: 24px; padding: 22px 20px; margin-bottom: 30px; box-shadow: 0 12px 36px rgba(239, 68, 68, 0.25);">
        
        <!-- Header with RED Badge -->
        <div style="display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 10px; margin-bottom: 16px; border-bottom: 1px solid rgba(239, 68, 68, 0.25); padding-bottom: 12px;">
            <div style="display: flex; align-items: center; gap: 10px; flex-wrap: wrap;">
                <span style="display: inline-flex; align-items: center; gap: 6px; background: #EF4444; color: #FFFFFF; font-size: 11.5px; font-weight: 700; padding: 5px 14px; border-radius: 9999px; letter-spacing: 0.5px; box-shadow: 0 2px 10px rgba(239, 68, 68, 0.6);">
                    <span style="display: inline-block; width: 8px; height: 8px; background: #FFF; border-radius: 50%; animation: pulse 1.5s infinite;"></span>
                    <span>ทดสอบเรื่องนี้ (ACTIVE TEST)</span>
                </span>
                <span style="font-size: 15px; font-weight: 700; color: #F8FAFC;">
                    นามบัตรดิจิทัล Alpha & เกณฑ์คะแนน (เปิดเทสบนมือถือได้ทันที)
                </span>
            </div>
            <span style="font-size: 12px; color: #FCA5A5; font-weight: 500;">
                ⚡ เปิด 1 คลิก ไม่ต้องก๊อปลิงก์ลง LINE ให้แชทดันหาย
            </span>
        </div>

        <!-- Section 1: 📇 Agent Cards for Alpha Agents -->
        <div style="margin-bottom: 14px;">
            <div style="font-size: 12px; font-weight: 600; color: #E2E8F0; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
                <span>📇</span>
                <span>1. นามบัตรตัวแทน Alpha (คลิกดูภาพ Golden Emblem จริง):</span>
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

        <!-- Section 3: ⚖️ Scoring Engine & Nong Siwa AI -->
        <div>
            <div style="font-size: 12px; font-weight: 600; color: #E2E8F0; margin-bottom: 8px; display: flex; align-items: center; gap: 6px;">
                <span>⚖️</span>
                <span>3. เกณฑ์คะแนน 2-Track & น้องศิวา AI:</span>
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 8px;">
                <a href="https://assets.siwasup.com/scoring_summary_light.html" target="_blank" style="background: rgba(255, 255, 255, 0.95); color: #0F172A; font-size: 11.5px; font-weight: 700; padding: 7px 13px; border-radius: 10px; text-decoration: none; box-shadow: 0 2px 8px rgba(255,255,255,0.2);">
                    📄 ตารางคะแนน 2-Track (ไลท์โหมด พิมพ์/พรีเซนต์)
                </a>
                <a href="https://assets.siwasup.com/scoring_debate_dashboard.html" target="_blank" style="background: rgba(194, 164, 96, 0.15); border: 1px solid rgba(194, 164, 96, 0.4); color: #E6CA85; font-size: 11.5px; font-weight: 600; padding: 7px 13px; border-radius: 10px; text-decoration: none;">
                    📊 แดชบอร์ดเกณฑ์คะแนน (ฉบับทางการ)
                </a>
                <a href="https://assets.siwasup.com/line_chat_monitor.html" target="_blank" style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.4); color: #6EE7B7; font-size: 11.5px; font-weight: 600; padding: 7px 13px; border-radius: 10px; text-decoration: none;">
                    💬 มอนิเตอร์แชทน้องศิวา AI (Live)
                </a>
                <a href="https://line.me/R/ti/p/@813nyyia" target="_blank" style="background: rgba(6, 199, 85, 0.15); border: 1px solid rgba(6, 199, 85, 0.4); color: #4ADE80; font-size: 11.5px; font-weight: 600; padding: 7px 13px; border-radius: 10px; text-decoration: none;">
                    📲 ทักคุย LINE OA น้องศิวา (@813nyyia)
                </a>
            </div>
        </div>

    </div>
"""

# Insert right before SECTION 0
target_split = "<!-- SECTION 0: PERSONALIZED SQUAD HUB SYSTEM & TESTER -->"
if target_split in content:
    content = content.replace(target_split, RED_ACTIVE_TEST_HTML + "\n    " + target_split)
    with open(TARGET_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("Inserted RED ACTIVE TEST ZONE into executive_quick_hub.html successfully")
else:
    print("Target split not found!")
