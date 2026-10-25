# -*- coding: utf-8 -*-
"""
Patch launchpad.html to embed the 7-Dimension Behavioral KPI Matrix and Rollout Blueprint.
"""
import sys
import io

FILE_PATH = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\launchpad.html"

CSS_PATCH = """
        /* 7-Dimension KPI & Rollout Blueprint Styles */
        .kpi-section {
            margin-top: 35px;
            margin-bottom: 35px;
        }
        .rollout-blueprint-card {
            background: linear-gradient(135deg, rgba(20, 27, 45, 0.95), rgba(10, 15, 29, 0.98));
            border: 1px solid rgba(212, 175, 55, 0.4);
            border-radius: 14px;
            padding: 24px;
            margin-bottom: 24px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            position: relative;
            overflow: hidden;
        }
        .rollout-blueprint-card::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0; height: 3px;
            background: linear-gradient(90deg, #D4AF37, #F3E3B6, #D4AF37);
        }
        .rollout-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 18px;
        }
        @media (max-width: 800px) {
            .rollout-grid {
                grid-template-columns: 1fr;
            }
        }
        .rollout-column {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 10px;
            padding: 16px 18px;
        }
        .rollout-column.highlight {
            border-color: rgba(212, 175, 55, 0.35);
            background: rgba(212, 175, 55, 0.04);
        }
        .rollout-column h4 {
            font-size: 15px;
            font-weight: bold;
            margin-bottom: 10px;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .rollout-column p {
            font-size: 13px;
            color: #cbd5e1;
            line-height: 1.6;
            margin-bottom: 8px;
        }
        .rollout-column ul {
            margin: 0;
            padding-left: 18px;
            font-size: 12.5px;
            color: #94a3b8;
            line-height: 1.6;
        }
        .kpi-table-wrapper {
            background: rgba(15, 23, 42, 0.8);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            overflow-x: auto;
            margin-top: 16px;
        }
        .kpi-table {
            width: 100%;
            border-collapse: collapse;
            text-align: left;
            font-size: 13px;
        }
        .kpi-table th {
            background: rgba(20, 30, 55, 0.95);
            color: #F3E3B6;
            padding: 14px 16px;
            font-weight: 600;
            font-size: 12.5px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            border-bottom: 2px solid rgba(212, 175, 55, 0.3);
            white-space: nowrap;
        }
        .kpi-table td {
            padding: 12px 16px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.05);
            color: #cbd5e1;
            vertical-align: middle;
            line-height: 1.5;
        }
        .kpi-table tr:hover td {
            background: rgba(255, 255, 255, 0.02);
        }
        .kpi-tag {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            padding: 3px 9px;
            border-radius: 6px;
            font-size: 11.5px;
            font-weight: 600;
            white-space: nowrap;
        }
        .tag-bear { background: rgba(59, 130, 246, 0.15); color: #93c5fd; border: 1px solid rgba(59, 130, 246, 0.3); }
        .tag-wolf { background: rgba(16, 185, 129, 0.15); color: #6ee7b7; border: 1px solid rgba(16, 185, 129, 0.3); }
        .tag-lion { background: rgba(245, 158, 11, 0.15); color: #fcd34d; border: 1px solid rgba(245, 158, 11, 0.3); }
        .tag-falcon { background: rgba(14, 165, 233, 0.15); color: #7dd3fc; border: 1px solid rgba(14, 165, 233, 0.3); }
        .tag-eagle { background: rgba(217, 119, 6, 0.15); color: #fbbf24; border: 1px solid rgba(217, 119, 6, 0.3); }
        .tag-gryphon { background: rgba(168, 85, 247, 0.15); color: #d8b4fe; border: 1px solid rgba(168, 85, 247, 0.3); }
        .zero-overhead-pill {
            display: inline-block;
            background: rgba(16, 185, 129, 0.12);
            color: #34d399;
            border: 1px solid rgba(16, 185, 129, 0.3);
            border-radius: 4px;
            padding: 2px 7px;
            font-size: 11px;
            font-weight: 500;
            margin-top: 4px;
        }
"""

HTML_INJECTION = """
    <!-- Section 3.5: 7-Dimension Behavioral KPI Matrix & Rollout Blueprint -->
    <div class="section-title">
        <h2>📊 เกณฑ์ชี้วัดพฤติกรรม 7 มิติ & กลยุทธ์การเปิดตัว (Behavioral KPI Matrix & Rollout)</h2>
        <p>ยกระดับจากระบบ 2 มิติเดิม เพื่อแก้ปัญหาเพดานตัน (Ceiling Congestion) ด้วย Zero-Overhead Telemetry</p>
    </div>

    <!-- Strategic Rollout Blueprint: All-at-Once Reveal vs 2-Step Engine -->
    <div class="rollout-blueprint-card">
        <div style="display:flex; justify-content:space-between; align-items:flex-start; flex-wrap:wrap; gap:10px;">
            <div>
                <span style="background:rgba(212,175,55,0.2); color:#F3E3B6; border:1px solid rgba(212,175,55,0.4); padding:3px 10px; border-radius:12px; font-size:11px; font-weight:bold; letter-spacing:0.5px;">EXECUTIVE STRATEGY BLUEPRINT</span>
                <h3 style="color:#FFFFFF; font-size:18px; font-weight:bold; margin-top:8px;">💡 ข้อสรุปกลยุทธ์การเปิดตัว: "เปิดตัวหน้าบ้าน 6 ตัวตูมเดียว" ควบคู่ "รันระบบหลังบ้าน 2 จังหวะ"</h3>
            </div>
            <span style="color:#10b981; font-weight:bold; font-size:13px; display:flex; align-items:center; gap:6px;">
                <span style="width:8px; height:8px; background:#10b981; border-radius:50%; display:inline-block;"></span> ป้องกันปัญหาจิตวิทยา "โดนลดขั้นย้อนหลัง" 100%
            </span>
        </div>

        <p style="color:#cbd5e1; font-size:13px; line-height:1.6; margin-top:10px;">
            ข้อสงสัยเชิงกลยุทธ์: <em>"เราควรเปิดตัวเฟสแรก 4 ตัว แล้วเฟสสองค่อยเปิด 6 ตัว หรือเปิดตูมเดียวเลย?"</em> — จากการวิเคราะห์เชิงพฤติกรรมองค์กรและเอกสารวิจัย 16 หน้า คำตอบที่ดีที่สุดคือ <strong>"เปิดตัวภาพลักษณ์ 6 ตระกูลตูมเดียวทันที แต่บริหารข้อมูลหลังบ้านเป็น 2 จังหวะ"</strong> ด้วยเหตุผล 2 มิติ:
        </p>

        <div class="rollout-grid">
            <!-- Front-end Visual Column -->
            <div class="rollout-column highlight">
                <h4 style="color:#F3E3B6;">
                    <span>🎨</span> 1. หน้าบ้าน: เปิดตัว 6 ตระกูลตูมเดียว (All-at-Once Reveal)
                </h4>
                <p>
                    <strong>ทำไมต้องเปิด 6 ตัวในวันพรีเซนต์:</strong>
                </p>
                <ul>
                    <li><strong>เห็นบันไดอาชีพสูงสุด (Aspirational Horizon):</strong> ตัวแทนและนักลงทุนเห็นทันทีว่าระบบมีเส้นทางเติบโตถึงขั้นสูงสุดคือ Gryphon (ผู้ถือหุ้น/ที่ปรึกษาบอร์ด) ไม่ตันแค่ Eagle</li>
                    <li><strong>ป้องกันดราม่า "โดนลดขั้นย้อนหลัง":</strong> หากเปิด 4 ตัวก่อน เอเจนท์สายไวจะรีบขึ้น Eagle แล้วเมื่อเปิด Falcon ทีหลัง จะเกิดความรู้สึกว่าตนถูก "ลดขั้น" ลงมาเป็น Falcon ซึ่งขัดกับวัฒนธรรมไทยเรื่องการรักษาหน้า</li>
                    <li><strong>เปิดตัวแล้วสง่างาม ทรงพลัง:</strong> ตราสัญลักษณ์ 3D Crest ครบทั้ง 6 ตัวสร้างความน่าเชื่อถือระดับสถาบันการเงินทันที</li>
                </ul>
            </div>

            <!-- Back-end Engine Column -->
            <div class="rollout-column">
                <h4 style="color:#60a5fa;">
                    <span>⚙️</span> 2. หลังบ้าน: รันระบบ 2 จังหวะแบบ Zero-Overhead (Two-Step Backend)
                </h4>
                <p>
                    <strong>ขั้นตอนการจัดการข้อมูลจริง (ไม่เพิ่มงานเอกสาร):</strong>
                </p>
                <ul>
                    <li><strong>จังหวะที่ 1 (Day 1 - ทันที):</strong> แมปฐานข้อมูลตัวแทน 125 คนเดิมที่มีใน Google Sheets เข้าสู่ 4 กลุ่มรากฐาน (Bear, Wolf, Lion, Eagle) ทันที 100% จากแต้มเดิม ($A_i, P_i$) โดยยังไม่มีใครได้ Falcon หรือ Gryphon</li>
                    <li><strong>จังหวะที่ 2 (Phase 2):</strong> เริ่มเปิด Passive Telemetry เก็บสถิติความไวปิดดีล ($V_i \le 7$ วัน) และประวัติกุญแจพี่ลิลลี่ ($T_i$) ระบบจะทำการเลื่อนขั้นเป็น Falcon และ Gryphon ตามรอบประเมินจริงอย่างโปร่งใส</li>
                    <li><strong>Zero-Overhead:</strong> พี่ลิลลี่และคุณบัวไม่ต้องกรอกข้อมูลเพิ่ม อาศัยเพียง Timestamp จากการกดรับงานและสแกนกุญแจ</li>
                </ul>
            </div>
        </div>
    </div>

    <!-- 7-Dimension Behavioral KPI Matrix Table -->
    <div style="background:rgba(20,27,45,0.7); border:1px solid rgba(255,255,255,0.1); border-radius:12px; padding:20px; margin-bottom:30px;">
        <div style="display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap; gap:8px; margin-bottom:12px;">
            <h3 style="font-size:16px; color:#F3E3B6; font-weight:bold; display:flex; align-items:center; gap:8px;">
                <span>📋</span> ตารางชี้วัด 7 มิติพฤติกรรม (The 7-Dimension Behavioral Feature Vector)
            </h3>
            <span style="font-size:12px; color:#94a3b8;">สมการประเมิน: $\vec{A}_i = [A_i, P_i, V_i, K_i, C_i, T_i, N_i]$</span>
        </div>

        <div class="kpi-table-wrapper">
            <table class="kpi-table">
                <thead>
                    <tr>
                        <th style="width:14%;">มิติคะแนน (Metric)</th>
                        <th style="width:28%;">พฤติกรรมชี้วัดในโลกจริง (Observed Behavior)</th>
                        <th style="width:38%;">แหล่งข้อมูลอัตโนมัติ (Zero-Overhead Telemetry)</th>
                        <th style="width:20%;">ตระกูลที่ปลดล็อก (Target Archetype)</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            <strong style="color:#93c5fd;">$A_i$</strong><br>
                            <span style="font-size:11px; color:#64748b;">Activity Index</span>
                        </td>
                        <td>
                            <strong>ความขยันภาคสนาม & ปูพรมการตลาด:</strong><br>
                            สำรวจพื้นที่, ถ่ายรูปทรัพย์, ปักป้ายไวนิล, แชร์สื่อโซเชียลสม่ำเสมอ
                        </td>
                        <td>
                            นับยอดดาวน์โหลด Artwork ป้ายไวนิล, พิกัด Check-in ถ่ายรูปทรัพย์, ยอดคลิก Smart Share Link
                            <br><span class="zero-overhead-pill">⚡ อัตโนมัติ 100% จากระบบ</span>
                        </td>
                        <td>
                            <span class="kpi-tag tag-bear">🐻 หมี (Bear)</span>
                            <div style="font-size:11px; color:#64748b; margin-top:2px;">ฐานรากคลังทรัพย์</div>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <strong style="color:#6ee7b7;">$P_i$</strong><br>
                            <span style="font-size:11px; color:#64748b;">Performance Index</span>
                        </td>
                        <td>
                            <strong>ผลงานการปิดดีลซื้อขายจริง:</strong><br>
                            จำนวนและมูลค่าดีลที่ปิดสำเร็จ, การวางเงินมัดจำจองทรัพย์, การโอนกรรมสิทธิ์
                        </td>
                        <td>
                            บันทึกสลิปเงินมัดจำจองทรัพย์ + คุณบัวกด Approve 1-Click ผ่านระบบ LINE OA
                            <br><span class="zero-overhead-pill">⚡ บัวกดปุ่มเดียวจบ</span>
                        </td>
                        <td>
                            <span class="kpi-tag tag-wolf">🐺 หมาป่า (Wolf)</span>
                            <div style="font-size:11px; color:#64748b; margin-top:2px;">นักล่าภาคสนาม</div>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <strong style="color:#7dd3fc;">$V_i$</strong><br>
                            <span style="font-size:11px; color:#64748b;">Deal Velocity</span>
                        </td>
                        <td>
                            <strong>ความเร็วในการพิชิตดีล (Flash Closer):</strong><br>
                            ค่าเฉลี่ยระยะเวลาปิดดีลรวดเร็ว ($V_i = \frac{1}{1 + \overline{\Delta t}}$), ปิดเคสได้ภายใน $\le 7$ วัน
                        </td>
                        <td>
                            คำนวณส่วนต่างเวลาอัตโนมัติ (Timestamp): จากวินาทีที่รับ Lead ถึงวินาทีที่เซ็นสัญญาจอง
                            <br><span class="zero-overhead-pill">⚡ ระบบคำนวณเบื้องหลัง</span>
                        </td>
                        <td>
                            <span class="kpi-tag tag-falcon">🦅 เหยี่ยว (Falcon)</span>
                            <div style="font-size:11px; color:#64748b; margin-top:2px;">สไนเปอร์สายฟ้าแลบ</div>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <strong style="color:#fcd34d;">$K_i$</strong><br>
                            <span style="font-size:11px; color:#64748b;">Ticket Kurtosis</span>
                        </td>
                        <td>
                            <strong>ความสามารถปิดดีลมูลค่าสูงพิเศษ (Heavy Tail):</strong><br>
                            เชี่ยวชาญการปิดทรัพย์ไซส์ใหญ่ Super Luxury / ที่ดินแปลงใหญ่ (20M - 100M+ บาท)
                        </td>
                        <td>
                            คำนวณค่าการกระจายตัว (Kurtosis) ของมูลค่าธุรกรรมจริงในใบเสร็จการโอนกรรมสิทธิ์
                            <br><span class="zero-overhead-pill">⚡ สถิติวิเคราะห์อัตโนมัติ</span>
                        </td>
                        <td>
                            <span class="kpi-tag tag-lion">🦁 สิงโต (Lion)</span>
                            <div style="font-size:11px; color:#64748b; margin-top:2px;">เจ้าถิ่นคุมพอร์ตยักษ์</div>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <strong style="color:#fbbf24;">$C_i$</strong><br>
                            <span style="font-size:11px; color:#64748b;">Asset Complexity</span>
                        </td>
                        <td>
                            <strong>ความเชี่ยวชาญทรัพย์ซับซ้อน & กฎหมาย:</strong><br>
                            ปิดเคส NPA ธนาคาร, ทรัพย์บังคับคดี, ที่ดินติดภาระผูกพัน, จัดการภาษีโอน
                        </td>
                        <td>
                            ดึงค่าพิกัดความยาก (Weight 1.5 - 2.0x) อัตโนมัติจากประเภททรัพย์ใน Bank NPA Master Database
                            <br><span class="zero-overhead-pill">⚡ แท็กประเภททรัพย์อัตโนมัติ</span>
                        </td>
                        <td>
                            <span class="kpi-tag tag-eagle">🦅 อินทรี (Eagle)</span>
                            <div style="font-size:11px; color:#64748b; margin-top:2px;">จอมทัพดีลซับซ้อน</div>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <strong style="color:#f43f5e;">$T_i$</strong><br>
                            <span style="font-size:11px; color:#64748b;">Key Custody Trust</span>
                        </td>
                        <td>
                            <strong>วินัยความน่าเชื่อถือในการเบิก-คืนกุญแจ:</strong><br>
                            คืนตรงเวลาตามกำหนด ($\le 2$ ชม.), ไม่ทำกุญแจสูญหาย ($T_i = 100 - 10N_{late} - 50N_{lost}$)
                        </td>
                        <td>
                            สแกน QR Code ตอนเบิก-คืนกุญแจที่โต๊ะพี่ลิลลี่ บันทึก Timestamp ลงระบบทันทีใน 2 วินาที
                            <br><span class="zero-overhead-pill">⚡ พี่ลิลลี่สแกนมือถือปิ๊บเดียว</span>
                        </td>
                        <td>
                            <span style="color:#cbd5e1; font-size:12px; font-weight:bold;">🛡️ ด่านคัดกรองความปลอดภัย</span>
                            <div style="font-size:11px; color:#f87171; margin-top:2px;">บังคับใช้กับ Eagle & Gryphon</div>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <strong style="color:#d8b4fe;">$N_i$</strong><br>
                            <span style="font-size:11px; color:#64748b;">Network Centrality</span>
                        </td>
                        <td>
                            <strong>การสร้างเครือข่าย & ช่วยรุ่นน้องปิดเคส:</strong><br>
                            เป็นพี่เลี้ยง Co-Closing ให้กับ Bear/Wolf, ขยายสายงานตัวแทนข้ามโซน (MGM Network)
                        </td>
                        <td>
                            บันทึกชื่อ Mentor / Co-Agent ในระบบปิดการขาย + รหัสผู้แนะนำตัวแทนใหม่
                            <br><span class="zero-overhead-pill">⚡ ตรวจสอบสัญญาร่วมอัตโนมัติ</span>
                        </td>
                        <td>
                            <span class="kpi-tag tag-gryphon">🦅🦁 กริฟฟอน (Gryphon)</span>
                            <div style="font-size:11px; color:#64748b; margin-top:2px;">สภาสูงสุด (จำกัด 2 ที่นั่ง/ปี)</div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
"""

def main():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Insert CSS before </style>
    style_end = content.find('</style>')
    if style_end == -1:
        print("Error: </style> not found")
        sys.exit(1)

    content = content[:style_end] + CSS_PATCH + content[style_end:]

    # 2. Insert HTML Section before Section 4
    target = '    <!-- Section 4: 4-Phase Strategic Roadmap & Timeline -->'
    target_idx = content.find(target)
    if target_idx == -1:
        print("Error: Target comment not found")
        sys.exit(1)

    content = content[:target_idx] + HTML_INJECTION + content[target_idx:]

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

    print("Successfully patched launchpad.html with 7-Dimension KPI Matrix and Rollout Blueprint!")

if __name__ == '__main__':
    main()
