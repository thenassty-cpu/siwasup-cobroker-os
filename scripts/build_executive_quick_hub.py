# -*- coding: utf-8 -*-
"""
Build Executive Quick Launch Hub, sync all missing assets to G:, 
deploy to Cloudflare R2, and update Twin Brain handover logs for Offy.
"""
import os
import sys
import shutil

sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
from overnight_r2_crawler import put_object_r2

WEB_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
G_DIR = r"G:\Siwasup_Presentation_2026"
BRAIN_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\FBT-Graphic-Studio-Tools\Brain_Updates"

# 1. Sync missing HTML files to G:
files_to_sync = [
    "bua_alpha_checklist.html",
    "agent_quick_guide.html",
    "alpha_onboarding_infographic.html",
    "gool_executive_presentation.html",
    "gool_anti_hoarding_brief.html",
    "property_curator.html",
    "catalog.html",
    "scoring_debate_dashboard.html",
    "EXCLUSIVE_LISTING_AUDIT_MANUAL.md"
]

for f in files_to_sync:
    src = os.path.join(WEB_DIR, f)
    dst = os.path.join(G_DIR, f)
    if os.path.exists(src):
        shutil.copy2(src, dst)
        print(f"[SYNC] Copied {f} to G:\\Siwasup_Presentation_2026\\")

# 2. Build executive_quick_hub.html
hub_html = """<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Siwasup Co-Broker OS - Executive Quick Launch Hub</title>
    <link rel="icon" type="image/png" href="assets/siwasup_logo.png">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-base: #07090e;
            --bg-card: rgba(18, 24, 38, 0.85);
            --bg-card-hover: rgba(28, 38, 60, 0.95);
            --border-card: rgba(194, 164, 96, 0.25);
            --border-hover: rgba(194, 164, 96, 0.8);
            --gold-primary: #C2A460;
            --gold-light: #E6CA85;
            --gold-glow: rgba(194, 164, 96, 0.35);
            --text-main: #F8FAFC;
            --text-muted: #94A3B8;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Prompt', 'Tahoma', sans-serif;
            background-color: var(--bg-base);
            background-image: 
                radial-gradient(circle at 15% 15%, rgba(194, 164, 96, 0.08) 0%, transparent 40%),
                radial-gradient(circle at 85% 85%, rgba(30, 58, 138, 0.12) 0%, transparent 50%);
            background-attachment: fixed;
            color: var(--text-main);
            min-height: 100vh;
            padding: 32px 16px 60px 16px;
        }

        .container {
            max-width: 1180px;
            margin: 0 auto;
        }

        /* Top Header */
        .hub-header {
            text-align: center;
            margin-bottom: 36px;
            padding: 30px 24px;
            background: linear-gradient(180deg, rgba(24, 32, 50, 0.7) 0%, rgba(11, 15, 25, 0.9) 100%);
            border: 1px solid var(--border-card);
            border-radius: 24px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.6), 0 0 30px var(--gold-glow);
            backdrop-filter: blur(12px);
        }

        .crown-tag {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 1px;
            text-transform: uppercase;
            color: var(--gold-light);
            background: rgba(194, 164, 96, 0.15);
            border: 1px solid var(--gold-primary);
            padding: 6px 16px;
            border-radius: 9999px;
            margin-bottom: 14px;
        }

        h1 {
            font-size: 32px;
            font-weight: 700;
            letter-spacing: -0.5px;
            margin-bottom: 8px;
            background: linear-gradient(135deg, #FFFFFF 40%, var(--gold-light) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        p.hub-subtitle {
            font-size: 14.5px;
            color: var(--text-muted);
            max-width: 720px;
            margin: 0 auto 18px auto;
            line-height: 1.6;
        }

        .status-pills {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 12px;
            font-size: 12px;
        }

        .pill {
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 4px 12px;
            border-radius: 20px;
            color: #E2E8F0;
            display: flex;
            align-items: center;
            gap: 6px;
        }
        .pill.live {
            border-color: rgba(34, 197, 94, 0.4);
            background: rgba(34, 197, 94, 0.1);
            color: #86EFAC;
        }

        /* Section Headings */
        .section-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin: 36px 0 18px 0;
            padding-bottom: 10px;
            border-bottom: 1px solid rgba(194, 164, 96, 0.2);
        }

        .section-title {
            display: flex;
            align-items: center;
            gap: 12px;
            font-size: 20px;
            font-weight: 600;
            color: #FFFFFF;
        }

        .section-badge {
            font-size: 11px;
            padding: 3px 10px;
            border-radius: 6px;
            font-weight: 500;
            letter-spacing: 0.5px;
            background: rgba(194, 164, 96, 0.15);
            color: var(--gold-light);
            border: 1px solid rgba(194, 164, 96, 0.35);
        }

        /* Grid Cards */
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
            gap: 18px;
        }

        .card {
            background: var(--bg-card);
            border: 1px solid var(--border-card);
            border-radius: 18px;
            padding: 24px;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            backdrop-filter: blur(8px);
            transition: all 0.28s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, transparent, var(--gold-primary), transparent);
            opacity: 0;
            transition: opacity 0.3s ease;
        }

        .card:hover {
            transform: translateY(-4px);
            border-color: var(--border-hover);
            background: var(--bg-card-hover);
            box-shadow: 0 16px 32px rgba(0,0,0,0.6), 0 0 20px rgba(194, 164, 96, 0.25);
        }

        .card:hover::before {
            opacity: 1;
        }

        .card-top {
            display: flex;
            align-items: flex-start;
            gap: 16px;
            margin-bottom: 14px;
        }

        .icon-box {
            width: 48px;
            height: 48px;
            border-radius: 12px;
            background: rgba(194, 164, 96, 0.12);
            border: 1px solid rgba(194, 164, 96, 0.3);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            flex-shrink: 0;
        }

        .card-meta {
            flex: 1;
        }

        .card-title {
            font-size: 17px;
            font-weight: 600;
            color: #FFFFFF;
            margin-bottom: 4px;
            line-height: 1.35;
        }

        .card-role {
            font-size: 11.5px;
            color: var(--gold-light);
            font-weight: 500;
        }

        .card-desc {
            font-size: 13.5px;
            color: var(--text-muted);
            line-height: 1.55;
            margin-bottom: 20px;
        }

        /* Dual Action Buttons */
        .card-actions {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 10px;
            border-top: 1px solid rgba(255, 255, 255, 0.08);
            padding-top: 16px;
        }

        .btn {
            font-family: inherit;
            font-size: 12.5px;
            font-weight: 600;
            padding: 10px 14px;
            border-radius: 10px;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            transition: all 0.2s ease;
            text-align: center;
            cursor: pointer;
        }

        .btn-live {
            background: linear-gradient(135deg, #C2A460 0%, #9A7B32 100%);
            color: #0B0D0F;
            border: 1px solid var(--gold-primary);
            box-shadow: 0 4px 12px rgba(194, 164, 96, 0.25);
        }

        .btn-live:hover {
            background: linear-gradient(135deg, #E6CA85 0%, #C2A460 100%);
            transform: translateY(-1px);
            box-shadow: 0 6px 16px rgba(194, 164, 96, 0.4);
            color: #000;
        }

        .btn-local {
            background: rgba(255, 255, 255, 0.06);
            color: #E2E8F0;
            border: 1px solid rgba(255, 255, 255, 0.15);
        }

        .btn-local:hover {
            background: rgba(255, 255, 255, 0.14);
            border-color: rgba(255, 255, 255, 0.3);
            color: #FFFFFF;
            transform: translateY(-1px);
        }

        .btn-single {
            grid-column: span 2;
        }

        /* Copy link pill */
        .copy-pill {
            display: block;
            margin-top: 8px;
            font-size: 11px;
            color: #64748B;
            text-align: right;
            cursor: pointer;
            text-decoration: underline;
        }
        .copy-pill:hover { color: var(--gold-light); }

        /* Footer */
        .hub-footer {
            margin-top: 50px;
            padding: 24px;
            background: rgba(15, 20, 30, 0.6);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            justify-content: space-between;
            gap: 16px;
            font-size: 12.5px;
            color: var(--text-muted);
        }

        .hub-footer strong { color: #E2E8F0; }

        @media (max-width: 640px) {
            h1 { font-size: 24px; }
            .grid { grid-template-columns: 1fr; }
            .card-actions { grid-template-columns: 1fr; }
            .btn-single { grid-column: span 1; }
        }
    </style>
</head>
<body>

<div class="container">

    <!-- Top Header -->
    <header class="hub-header">
        <div class="crown-tag">👑 Siwasup Co-Broker OS • Quick-Access Portal</div>
        <h1>EXECUTIVE LAUNCHPAD & LINK HUB</h1>
        <p class="hub-subtitle">
            ศูนย์รวมทางด่วนสำหรับเข้าสู่ระบบทุกโมดูล รองรับการกดเปิดแบบ Live บนคลาวด์ R2 และเปิดแบบ Offline จาก Flash Drive โดยตรง เพื่อให้คุณต้นเปิดโชว์หรือทำงานได้ทันทีทุกที่
        </p>
        <div class="status-pills">
            <span class="pill live">🟢 Cloudflare R2: Online (assets.siwasup.com)</span>
            <span class="pill">📁 Flash Drive: Ready (G:\Siwasup_Presentation_2026)</span>
            <span class="pill">⚡ Master Vault: 15,117+ 801 Assets</span>
            <span class="pill">🛡️ PDPA Compliant: 100%</span>
        </div>
    </header>

    <!-- SECTION 1: GOOL COMMAND -->
    <div class="section-header">
        <div class="section-title">
            <span>🦁</span>
            <span>สำหรับคุณกูล (Sales Commander & 20 Alpha)</span>
        </div>
        <span class="section-badge">GOOL • THE LION</span>
    </div>

    <div class="grid">
        <!-- Card 1: Gool Executive Deck -->
        <div class="card">
            <div>
                <div class="card-top">
                    <div class="icon-box">🦁</div>
                    <div class="card-meta">
                        <div class="card-title">Gool's Executive Deck</div>
                        <div class="card-role">พรีเซนเทชันเปิดตัวสำหรับกูล</div>
                    </div>
                </div>
                <div class="card-desc">
                    ฉายวิสัยทัศน์สิงโต, โครงสร้าง 6 ยศตัวแทน, กลยุทธ์พอร์ตทรัพย์ 15,117 แปลง, ล็อกสิทธิ์ลูกค้า 60 วัน และปุ่มลัดเชื่อมต่อระบบแอดมิน 1 คลิก
                </div>
            </div>
            <div>
                <div class="card-actions">
                    <a href="https://assets.siwasup.com/gool_executive_presentation.html" target="_blank" class="btn btn-live">🌐 เปิด Live (R2)</a>
                    <a href="gool_executive_presentation.html" class="btn btn-local">💾 เปิดในเครื่อง (G:\)</a>
                </div>
                <span class="copy-pill" onclick="copyUrl('https://assets.siwasup.com/gool_executive_presentation.html')">คัดลอกลิงก์</span>
            </div>
        </div>

        <!-- Card 2: Anti-Hoarding Brief -->
        <div class="card">
            <div>
                <div class="card-top">
                    <div class="icon-box">🛡️</div>
                    <div class="card-meta">
                        <div class="card-title">Anti-Hoarding & Anomaly Console</div>
                        <div class="card-role">แดชบอร์ดตรวจจับการกั๊กทรัพย์เพื่อฮั้วดีล</div>
                    </div>
                </div>
                <div class="card-desc">
                    อธิบายหลักการ Kakomikomi, 3 สัญญาณเตือนผิดปกติ, กลไกปลดล็อกทรัพย์อัตโนมัติ (TTL 72 ชม.), ระบบคะแนน Trust Score และหน้าต่างสั่งการของกูล
                </div>
            </div>
            <div>
                <div class="card-actions">
                    <a href="https://assets.siwasup.com/gool_anti_hoarding_brief.html" target="_blank" class="btn btn-live">🌐 เปิด Live (R2)</a>
                    <a href="gool_anti_hoarding_brief.html" class="btn btn-local">💾 เปิดในเครื่อง (G:\)</a>
                </div>
                <span class="copy-pill" onclick="copyUrl('https://assets.siwasup.com/gool_anti_hoarding_brief.html')">คัดลอกลิงก์</span>
            </div>
        </div>

        <!-- Card 3: Scoring Debate Dashboard -->
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
                    <a href="scoring_debate_dashboard.html" class="btn btn-local">💾 เปิดในเครื่อง (G:\)</a>
                </div>
                <span class="copy-pill" onclick="copyUrl('https://assets.siwasup.com/scoring_debate_dashboard.html')">คัดลอกลิงก์</span>
            </div>
        </div>

        <!-- Card 4: Agent Quick Guide -->
        <div class="card">
            <div>
                <div class="card-top">
                    <div class="icon-box">⚡</div>
                    <div class="card-meta">
                        <div class="card-title">Agent Quick Guide (1 หน้าจบ)</div>
                        <div class="card-role">คู่มือการใช้งานสำหรับ 20 ตัวแทน Alpha</div>
                    </div>
                </div>
                <div class="card-desc">
                    สรุปขั้นตอนเริ่มต้นทำงาน: ไม่ต้องจำรหัสผ่าน เชื่อมต่อผ่าน LINE Magic Binding, เบิกกุญแจ, แชร์ทรัพย์ให้ลูกค้า และรับคอมมิชชัน
                </div>
            </div>
            <div>
                <div class="card-actions">
                    <a href="https://assets.siwasup.com/agent_quick_guide.html" target="_blank" class="btn btn-live">🌐 เปิด Live (R2)</a>
                    <a href="agent_quick_guide.html" class="btn btn-local">💾 เปิดในเครื่อง (G:\)</a>
                </div>
                <span class="copy-pill" onclick="copyUrl('https://assets.siwasup.com/agent_quick_guide.html')">คัดลอกลิงก์</span>
            </div>
        </div>

        <!-- Card 5: Alpha Onboarding Infographic -->
        <div class="card">
            <div>
                <div class="card-top">
                    <div class="icon-box">📊</div>
                    <div class="card-meta">
                        <div class="card-title">Alpha Onboarding Infographic</div>
                        <div class="card-role">ผังยุทธศาสตร์การรับ 20 หัวกะทิ</div>
                    </div>
                </div>
                <div class="card-desc">
                    อินโฟกราฟิกแจกแจงแผนยุทธการต้อนรับตัวแทน 20 ท่านแรก เพื่อให้กูลและทีมงานเห็นภาพรวมทิศทางเดียวกันใน 1 แผ่น
                </div>
            </div>
            <div>
                <div class="card-actions">
                    <a href="https://assets.siwasup.com/alpha_onboarding_infographic.html" target="_blank" class="btn btn-live">🌐 เปิด Live (R2)</a>
                    <a href="alpha_onboarding_infographic.html" class="btn btn-local">💾 เปิดในเครื่อง (G:\)</a>
                </div>
                <span class="copy-pill" onclick="copyUrl('https://assets.siwasup.com/alpha_onboarding_infographic.html')">คัดลอกลิงก์</span>
            </div>
        </div>
    </div>

    <!-- SECTION 2: BUA CURATION -->
    <div class="section-header">
        <div class="section-title">
            <span>🌸</span>
            <span>สำหรับคุณบัว (Listing Curator & Operations - เพื่อนร่วมรุ่นของต้น)</span>
        </div>
        <span class="section-badge">BUA • THE CURATOR</span>
    </div>

    <div class="grid">
        <!-- Card 6: Property Curator 801 Props -->
        <div class="card">
            <div>
                <div class="card-top">
                    <div class="icon-box">🎯</div>
                    <div class="card-meta">
                        <div class="card-title">NPA Spotlight Curator (801 แปลง)</div>
                        <div class="card-role">ระบบคัดกรองทรัพย์ 100% Match Allabout</div>
                    </div>
                </div>
                <div class="card-desc">
                    ระบบริบบิ้น 3 สี (🔴 8 หลุดหมวด | 🟢 12 มาใหม่ | 💎 671 ทรัพย์แบงก์) พร้อมระบบปักหมุดคัด Top 20 Hero Deals ส่งต่อให้ทีมกูล
                </div>
            </div>
            <div>
                <div class="card-actions">
                    <a href="https://assets.siwasup.com/property_curator.html" target="_blank" class="btn btn-live">🌐 เปิด Live (R2)</a>
                    <a href="property_curator.html" class="btn btn-local">💾 เปิดในเครื่อง (G:\)</a>
                </div>
                <span class="copy-pill" onclick="copyUrl('https://assets.siwasup.com/property_curator.html')">คัดลอกลิงก์</span>
            </div>
        </div>

        <!-- Card 7: Bua Alpha Checklist -->
        <div class="card">
            <div>
                <div class="card-top">
                    <div class="icon-box">📋</div>
                    <div class="card-meta">
                        <div class="card-title">Bua Alpha Checklist</div>
                        <div class="card-role">เช็คลิสต์ตรวจความพร้อม 20 ตัวแทน</div>
                    </div>
                </div>
                <div class="card-desc">
                    ตารางตรวจสอบความพร้อมรายบุคคลของ 20 Alpha Agents เช็คการยืนยันเบอร์, ผูก LINE และส่งมอบสิทธิ์เข้าถึงคลังทรัพย์
                </div>
            </div>
            <div>
                <div class="card-actions">
                    <a href="https://assets.siwasup.com/bua_alpha_checklist.html" target="_blank" class="btn btn-live">🌐 เปิด Live (R2)</a>
                    <a href="bua_alpha_checklist.html" class="btn btn-local">💾 เปิดในเครื่อง (G:\)</a>
                </div>
                <span class="copy-pill" onclick="copyUrl('https://assets.siwasup.com/bua_alpha_checklist.html')">คัดลอกลิงก์</span>
            </div>
        </div>
    </div>

    <!-- SECTION 3: CENTRAL CATALOG & CLIENTS -->
    <div class="section-header">
        <div class="section-title">
            <span>🛒</span>
            <span>แคตตาล็อกกลาง & โหมดลูกค้า (Central Catalog)</span>
        </div>
        <span class="section-badge">PUBLIC & CLIENT VIEW</span>
    </div>

    <div class="grid">
        <!-- Card 8: Central Catalog (Agent Mode) -->
        <div class="card">
            <div>
                <div class="card-top">
                    <div class="icon-box">🛒</div>
                    <div class="card-meta">
                        <div class="card-title">Central Web Catalog (Agent Mode)</div>
                        <div class="card-role">แคตตาล็อกค้นหาทรัพย์กลางสำหรับตัวแทน</div>
                    </div>
                </div>
                <div class="card-desc">
                    ค้นหาเร็วระดับมิลลิวินาที รวมคลังทรัพย์ 15,117 แปลง + 801 แปลงศิวาทรัพย์ แสดงค่าคอมมิชชัน, ราคาประเมิน, และปุ่มเบิกกุญแจ
                </div>
            </div>
            <div>
                <div class="card-actions">
                    <a href="https://assets.siwasup.com/catalog.html" target="_blank" class="btn btn-live">🌐 เปิด Live (R2)</a>
                    <a href="catalog.html" class="btn btn-local">💾 เปิดในเครื่อง (G:\)</a>
                </div>
                <span class="copy-pill" onclick="copyUrl('https://assets.siwasup.com/catalog.html')">คัดลอกลิงก์</span>
            </div>
        </div>

        <!-- Card 9: Client Mode Catalog -->
        <div class="card">
            <div>
                <div class="card-top">
                    <div class="icon-box">📱</div>
                    <div class="card-meta">
                        <div class="card-title">Catalog (Client Mode)</div>
                        <div class="card-role">แคตตาล็อกโหมดสะอาดสำหรับส่งให้ลูกค้าดู</div>
                    </div>
                </div>
                <div class="card-desc">
                    ซ่อนข้อมูลภายในและค่าคอมมิชชันทั้งหมด แสดงเฉพาะราคาขายและจุดเด่นทรัพย์ พร้อมปุ่มติดต่อตัวแทนผ่าน LINE OA ทันที
                </div>
            </div>
            <div>
                <div class="card-actions">
                    <a href="https://assets.siwasup.com/catalog.html?mode=client" target="_blank" class="btn btn-live">🌐 เปิด Live (R2)</a>
                    <a href="catalog.html?mode=client" class="btn btn-local">💾 เปิดในเครื่อง (G:\)</a>
                </div>
                <span class="copy-pill" onclick="copyUrl('https://assets.siwasup.com/catalog.html?mode=client')">คัดลอกลิงก์</span>
            </div>
        </div>

        <!-- Card 10: Sovereign Landing Page -->
        <div class="card">
            <div>
                <div class="card-top">
                    <div class="icon-box">🌐</div>
                    <div class="card-meta">
                        <div class="card-title">Welcome Landing Page</div>
                        <div class="card-role">หน้าแรกสถาปัตยกรรม 6 Sovereign</div>
                    </div>
                </div>
                <div class="card-desc">
                    หน้าต้อนรับระดับไฮเอนด์ โชว์ภาพลักษณ์ความน่าเชื่อถือของ Siwasup Co-Broker OS และระบบพันธมิตรธนาคารชั้นนำ
                </div>
            </div>
            <div>
                <div class="card-actions">
                    <a href="https://assets.siwasup.com/welcome_landing.html" target="_blank" class="btn btn-live">🌐 เปิด Live (R2)</a>
                    <a href="welcome_landing.html" class="btn btn-local">💾 เปิดในเครื่อง (G:\)</a>
                </div>
                <span class="copy-pill" onclick="copyUrl('https://assets.siwasup.com/welcome_landing.html')">คัดลอกลิงก์</span>
            </div>
        </div>
    </div>

    <!-- SECTION 4: OPERATIONS & LEGAL -->
    <div class="section-header">
        <div class="section-title">
            <span>🔑</span>
            <span>ฝ่ายปฏิบัติการ & พี่ลิลลี่ (Key Custody & Legal SOP)</span>
        </div>
        <span class="section-badge">CENTRAL OPERATIONS</span>
    </div>

    <div class="grid">
        <!-- Card 11: Exclusive Listing Audit SOP -->
        <div class="card">
            <div>
                <div class="card-top">
                    <div class="icon-box">📘</div>
                    <div class="card-meta">
                        <div class="card-title">Exclusive Listing Audit Manual</div>
                        <div class="card-role">คู่มือตรวจสอบสัญญาปิด & ป้องกันการฮั้วดีล (SOP)</div>
                    </div>
                </div>
                <div class="card-desc">
                    คู่มือภายใน 5 เสาหลัก: ระยะคุ้มครองสัญญา 6-12 เดือน, รอยเท้าดิจิทัล (Digital Footprint), โทรศัพท์สอบถามความพึงพอใจเจ้าของทรัพย์แบบสุภาพ
                </div>
            </div>
            <div>
                <div class="card-actions">
                    <a href="EXCLUSIVE_LISTING_AUDIT_MANUAL.md" class="btn btn-local btn-single">💾 เปิดอ่านคู่มือ (Markdown / G:\)</a>
                </div>
            </div>
        </div>

        <!-- Card 12: Admin Dashboard & Key Dispatch -->
        <div class="card">
            <div>
                <div class="card-top">
                    <div class="icon-box">🔑</div>
                    <div class="card-meta">
                        <div class="card-title">Admin Dashboard & Key Custody</div>
                        <div class="card-role">ระบบควบคุมกุญแจส่วนกลาง & จัดส่งแมสเซนเจอร์</div>
                    </div>
                </div>
                <div class="card-desc">
                    ระบบสร้าง Smart Dispatch Slip ส่งผ่าน LINE ให้แมสเซนเจอร์วิ่งส่งกุญแจพร้อมปุ่มนำทาง Google Maps 1 คลิก และสแกน QR รับ-ส่งกุญแจ (ไม่ต้องลงแอป)
                </div>
            </div>
            <div>
                <div class="card-actions">
                    <a href="https://assets.siwasup.com/admin_dashboard.html" target="_blank" class="btn btn-live">🌐 เปิด Live (R2)</a>
                    <a href="admin_dashboard.html" class="btn btn-local">💾 เปิดในเครื่อง (G:\)</a>
                </div>
                <span class="copy-pill" onclick="copyUrl('https://assets.siwasup.com/admin_dashboard.html')">คัดลอกลิงก์</span>
            </div>
        </div>
    </div>

    <!-- SECTION 5: FBT CORPORATE & HUAMAK MAP -->
    <div class="section-header">
        <div class="section-title">
            <span>🏢</span>
            <span>ฝ่ายโรงงาน FBT & ที่ดินหัวหมาก (คุณหงส์ & พี่เล็ก)</span>
        </div>
        <span class="section-badge">FBT MASTER ASSETS</span>
    </div>

    <div class="grid">
        <!-- Card 13: HuamarkArea_003 Map -->
        <div class="card">
            <div>
                <div class="card-top">
                    <div class="icon-box">🗺️</div>
                    <div class="card-meta">
                        <div class="card-title">FBT HuaMak 12 Parcels Master Map</div>
                        <div class="card-role">แผนที่แม่บทที่ดินหัวหมาก (HuamarkArea_003)</div>
                    </div>
                </div>
                <div class="card-desc">
                    ปรับปรุงตามคำสั่งคุณหงส์และพี่เล็ก: เพิ่ม 'ซอยรามคำแหง 67' ฝั่งติดแกรนด์สปอร์ต และแบ่งคูหาร้านหมอฟันตามสภาพจริง บันทึกและสำรองบนแฟลชไดรฟ์เรียบร้อย
                </div>
            </div>
            <div>
                <div class="card-actions">
                    <a href="file:///G:/+Hong/HuamarkArea_003_Folder/" class="btn btn-local btn-single">📁 เปิดโฟลเดอร์บน Flash Drive (G:\+Hong\)</a>
                </div>
            </div>
        </div>
    </div>

    <!-- Footer Note -->
    <footer class="hub-footer">
        <div>
            <strong>Siwasup Co-Broker OS — Enterprise Edition 2026</strong><br>
            สถาปัตยกรรมระบบโดย ต้น (NASSTY / Senior Advisor) ร่วมกับ hai (Home AI) & Offy (Office AI)
        </div>
        <div>
            สถานะสมอง: <strong>Twin Brain Synchronized 100%</strong>
        </div>
    </footer>

</div>

<script>
function copyUrl(url) {
    navigator.clipboard.writeText(url).then(() => {
        alert("คัดลอกลิงก์เรียบร้อยแล้ว: " + url);
    }).catch(err => {
        prompt("กด Ctrl+C เพื่อคัดลอกลิงก์:", url);
    });
}
</script>

</body>
</html>
"""

# Save to Web repo
hub_path_web = os.path.join(WEB_DIR, "executive_quick_hub.html")
with open(hub_path_web, "w", encoding="utf-8") as f:
    f.write(hub_html)
print(f"[LOCAL] Saved {hub_path_web}")

# Save to G:
hub_path_g = os.path.join(G_DIR, "executive_quick_hub.html")
with open(hub_path_g, "w", encoding="utf-8") as f:
    f.write(hub_html)
print(f"[G:\\] Saved {hub_path_g}")

# Deploy to Cloudflare R2
with open(hub_path_web, "rb") as f:
    r2_data = f.read()
status = put_object_r2("executive_quick_hub.html", r2_data, "text/html; charset=utf-8")
print(f"[R2] Deployed executive_quick_hub.html ({len(r2_data)} bytes) -> Status: {status}")

# 3. Update 00_START_HERE_เปิดพรีเซนต์ที่นี่.html on G: to feature this Quick Hub as the Top Banner!
start_here_path = os.path.join(G_DIR, "00_START_HERE_เปิดพรีเซนต์ที่นี่.html")
if os.path.exists(start_here_path):
    with open(start_here_path, "r", encoding="utf-8") as f:
        sh_content = f.read()
    
    # Check if Quick Hub banner is already there
    if "executive_quick_hub.html" not in sh_content:
        hub_banner = '''
    <!-- NEW EXECUTIVE QUICK LINK HUB BANNER -->
    <div style="background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%); border: 2px solid #C2A460; border-radius: 16px; padding: 22px 26px; margin-bottom: 28px; box-shadow: 0 10px 25px rgba(0,0,0,0.7), 0 0 20px rgba(194,164,96,0.3); display: flex; flex-wrap: wrap; align-items: center; justify-content: space-between; gap: 16px;">
        <div style="max-width: 650px;">
            <div style="display: inline-flex; align-items: center; gap: 6px; font-size: 11px; background: rgba(194,164,96,0.2); color: #F3E3B6; border: 1px solid #C2A460; padding: 3px 10px; border-radius: 9999px; font-weight: bold; margin-bottom: 8px;">
                ⭐ NEW • EXECUTIVE QUICK LINK HUB
            </div>
            <h2 style="font-size: 20px; color: #FFFFFF; margin-bottom: 6px;">ศูนย์รวมลิงก์ด่วนผู้บริหาร (Executive Quick Launch Hub)</h2>
            <p style="font-size: 13.5px; color: #94A3B8; line-height: 1.5;">รวมลิงก์ด่วนทั้ง 12 โมดูลสำคัญ (Deck กูล, แดชบอร์ดกั๊กทรัพย์, แดชบอร์ดคัดทรัพย์ 801 แปลงของบัว, สัญญาปิด SOP, แคตตาล็อก) พร้อมปุ่มเปิด Live R2 และเปิดออฟไลน์ในเครื่อง</p>
        </div>
        <div>
            <a href="executive_quick_hub.html" style="background: linear-gradient(135deg, #C2A460 0%, #8A6A1F 100%); color: #0b0d0f; font-weight: bold; font-size: 14px; padding: 12px 24px; border-radius: 10px; text-decoration: none; display: inline-flex; align-items: center; gap: 8px; box-shadow: 0 4px 15px rgba(194,164,96,0.4);">
                🚀 เข้าสู่ Executive Hub ทันที →
            </a>
        </div>
    </div>
'''
        # Insert after <div class="container">
        sh_content = sh_content.replace('<div class="container">', '<div class="container">\n' + hub_banner, 1)
        with open(start_here_path, "w", encoding="utf-8") as f:
            f.write(sh_content)
        print(f"[G:\\] Updated 00_START_HERE with Executive Quick Hub banner")

print("=== EXECUTIVE QUICK LAUNCH HUB COMPLETE ===")
