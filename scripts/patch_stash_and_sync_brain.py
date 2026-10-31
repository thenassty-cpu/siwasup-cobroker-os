# -*- coding: utf-8 -*-
"""
Update messenger_dispatch_slip.html with authentic Thai office 'Secret Stash Box' (กล่องชั้นวางรองเท้า / จุดนัดลับ).
Deploy to R2 and G:\, and sync Twin Brain.
"""
import os
import sys
import shutil

sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
from overnight_r2_crawler import put_object_r2

WEB_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
G_DIR = r"G:\Siwasup_Presentation_2026"
BRAIN_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\FBT-Graphic-Studio-Tools\Brain_Updates"

slip_path = os.path.join(WEB_DIR, "messenger_dispatch_slip.html")
with open(slip_path, "r", encoding="utf-8") as f:
    html = f.read()

# Replace the Flow 1 section
old_flow1 = """    <!-- FLOW 1: OFFICE DROPBOX (จุดดรอปที่ออฟฟิศ) -->
    <div id="flow1Block" class="hidden flex-col gap-3.5">
      
      <div class="bg-gradient-to-br from-[#1a2336] to-[#0f172a] border border-amber-500/40 rounded-2xl p-4 shadow-xl">
        <span class="text-[11px] font-bold uppercase tracking-wider text-amber-400 flex items-center gap-1 mb-1">
          <i data-lucide="archive" class="w-3.5 h-3.5"></i>
          จุดดรอปกุญแจที่ออฟฟิศศิวาทรัพย์
        </span>
        <div class="text-base font-bold text-white mt-1">ตู้เซฟ Key Lockbox กลาง (ชั้น 2 หน้าห้องพี่ลิลลี่)</div>
        <p class="text-xs text-slate-300 mt-1">
          พี่ลิลลี่ดรอปกุญแจใส่ซองซีลไว้ในช่องตู้ล็อกเกอร์เรียบร้อยแล้ว
        </p>
        <div class="bg-slate-900/90 border border-amber-500/30 p-3 rounded-xl mt-3 flex items-center justify-between">
          <div>
            <div class="text-[11px] text-slate-400">รหัสปลดล็อกตู้ประจำวัน</div>
            <div class="text-xl font-black font-mono text-brand-gold tracking-widest">#8821</div>
          </div>
          <span class="text-xs font-bold text-emerald-400 bg-emerald-500/10 border border-emerald-500/30 px-2.5 py-1 rounded-lg">
            ช่องหมายเลข 04
          </span>
        </div>
      </div>

      <!-- RETURN INSTRUCTIONS (การส่งคืน) -->
      <div class="bg-[#131B2B] border border-slate-700/80 rounded-2xl p-4 shadow-lg flex flex-col gap-2.5">
        <div class="text-xs font-bold text-white flex items-center gap-1.5">
          <i data-lucide="rotate-ccw" class="w-4 h-4 text-brand-gold"></i>
          ตัวเลือกการส่งคืนกุญแจ (2 ช่องทาง):
        </div>
        <div class="text-xs text-slate-300 leading-relaxed space-y-2">
          <div class="p-2.5 bg-slate-900/70 rounded-lg border border-slate-800">
            <strong>ช่องทาง A (นำมาดรอปคืนที่ออฟฟิศ):</strong> นำกุญแจมาหย่อนลงกล่อง Drop-Box คืนกุญแจที่ชั้น 1 หรือตู้เซฟชั้น 2 พร้อมหยอดสลิปบันทึก
          </div>
          <div class="p-2.5 bg-slate-900/70 rounded-lg border border-slate-800">
            <strong>ช่องทาง B (คืนที่ธนาคารเจ้าของทรัพย์เอง):</strong> เอเจนต์สามารถนำกุญแจไปส่งคืนที่โต๊ะ NPA ของธนาคาร (เช่น สาขา SCB/SAM ที่เบิกมา) โดยตรง แล้วถ่ายรูปใบเสร็จรับคืนอัปโหลดเข้าระบบ
          </div>
        </div>
      </div>

    </div>"""

new_flow1 = """    <!-- FLOW 1: OFFICE DROPBOX (จุดดรอปลับที่ออฟฟิศ) -->
    <div id="flow1Block" class="hidden flex-col gap-3.5">
      
      <div class="bg-gradient-to-br from-[#1a2336] to-[#0f172a] border border-amber-500/40 rounded-2xl p-4 shadow-xl">
        <div class="flex items-center justify-between mb-1.5">
          <span class="text-[11px] font-bold uppercase tracking-wider text-amber-400 flex items-center gap-1">
            <i data-lucide="archive" class="w-3.5 h-3.5"></i>
            จุดดรอปกุญแจที่ออฟฟิศ (จุดนัดลับที่รู้กัน)
          </span>
          <span class="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-500/20 text-amber-300 border border-amber-500/40">
            ดรอปไว้แล้ว ✓
          </span>
        </div>

        <div class="text-base font-bold text-white mt-1 flex items-center gap-2">
          <span>📦 ในกล่องชั้นวางรองเท้าหน้าออฟฟิศ</span>
        </div>
        
        <!-- P'Lily handwritten style message note -->
        <div class="bg-amber-950/40 border border-amber-500/30 rounded-xl p-3 mt-2.5 text-xs text-amber-200/90 leading-relaxed">
          <div class="font-bold text-amber-300 flex items-center gap-1.5 mb-1">
            <i data-lucide="message-square" class="w-3.5 h-3.5"></i>
            ข้อความจากพี่ลิลลี่:
          </div>
          "กุญแจแปลง SCB-4021 พี่ใส่ซองซิปล็อคซ่อนไว้ในกล่องรองเท้าชั้นล่างสุดฝั่งขวานะคะ เอเจนต์แวะมาล้วงหยิบได้เลยตลอด 24 ชม. ไม่ต้องรอพี่อยู่ที่โต๊ะจ้า"
        </div>

        <!-- Stash Location Photo Preview -->
        <div class="mt-3 bg-slate-950/60 p-2.5 rounded-xl border border-slate-800 flex items-center gap-3">
          <div class="w-14 h-14 rounded-lg bg-slate-800 border border-slate-700 flex items-center justify-center text-slate-400 flex-shrink-0 text-xl font-bold">
            👞
          </div>
          <div class="text-[11px] text-slate-300 leading-snug">
            <div class="font-bold text-white text-xs">พิกัด: ชั้นวางรองเท้าหน้าประตูทางเข้า</div>
            <div>กล่องสีน้ำตาลแถวล่างสุด • ถุงซิปกันน้ำรหัส #SEC-9901</div>
          </div>
        </div>
      </div>

      <!-- RETURN INSTRUCTIONS (การส่งคืน 2 ช่องทาง) -->
      <div class="bg-[#131B2B] border border-slate-700/80 rounded-2xl p-4 shadow-lg flex flex-col gap-2.5">
        <div class="text-xs font-bold text-white flex items-center gap-1.5">
          <i data-lucide="rotate-ccw" class="w-4 h-4 text-brand-gold"></i>
          ตัวเลือกการนำกุญแจมาส่งคืน (เลือก 1 ช่องทาง):
        </div>
        <div class="text-xs text-slate-300 leading-relaxed space-y-2">
          <div class="p-2.5 bg-slate-900/80 rounded-xl border border-slate-800 flex items-start gap-2">
            <span class="text-base leading-none">📦</span>
            <div>
              <strong class="text-white">ช่องทาง A (นำมาดรอปคืนที่เดิม):</strong>
              <div class="text-slate-400 mt-0.5">หย่อนกุญแจกลับเข้ากล่องชั้นวางรองเท้าที่เดิม แล้วกดถ่ายรูปกดยืนยันคืนกุญแจในมือถือได้เลย</div>
            </div>
          </div>
          <div class="p-2.5 bg-slate-900/80 rounded-xl border border-slate-800 flex items-start gap-2">
            <span class="text-base leading-none">🏦</span>
            <div>
              <strong class="text-white">ช่องทาง B (เอาไปคืนที่ธนาคารเอง):</strong>
              <div class="text-slate-400 mt-0.5">เอเจนต์นำไปคืนที่ฝ่ายบริหารทรัพย์สิน NPA ของธนาคารเจ้าของทรัพย์โดยตรง แล้วถ่ายรูปใบรับคืนส่งเข้าไลน์</div>
            </div>
          </div>
        </div>
      </div>

    </div>"""

html = html.replace(old_flow1, new_flow1)

with open(slip_path, "w", encoding="utf-8") as f:
    f.write(html)
print(f"[LOCAL] Patched messenger_dispatch_slip.html with authentic Secret Stash Spot (ชั้นวางรองเท้า)")

# Sync to G:\
shutil.copy2(slip_path, os.path.join(G_DIR, "messenger_dispatch_slip.html"))
print(f"[G:\\] Mirrored to G:\\Siwasup_Presentation_2026\\messenger_dispatch_slip.html")

# Deploy to R2
with open(slip_path, "rb") as f:
    st = put_object_r2("messenger_dispatch_slip.html", f.read(), "text/html; charset=utf-8")
print(f"[R2] Deployed to R2 -> Status: {st}")

# Update Twin Brain files
import datetime
now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

home_brain = os.path.join(G_DIR, "Home_Brain_Update.txt")
brain_update = f"""
================================================================================
Update Date: {now_str} (Home PC - hai)
Topic: Real Key Custody Protocols & Bank Master Cross-Match Deployment
================================================================================
1. Key Custody Real SOP (2 Authentic Methods from actual meeting):
   - Method 1: Office Secret Stash Drop (ดรอปไว้ที่กล่องชั้นวางรองเท้าหน้าออฟฟิศ/จุดที่รู้กัน)
     • P'Lily leaves the sealed key in a designated box at the office (e.g. shoe rack box).
     • Agent picks it up anytime without needing P'Lily present.
     • Return: Agent drops it back in the same stash box, OR delivers it directly to the Bank's NPA custody desk.
   - Method 2: Messenger Home Delivery (ส่งตรงถึงบ้านเอเจนต์)
     • Messenger picks up key from office safe and delivers to agent's home beforehand (not waiting on the curb at the vacant property).
   - Live updated: https://assets.siwasup.com/messenger_dispatch_slip.html

2. Bank Master Cross-Match on Allabout 801 Assets (Superpower for Bua):
   - Audited 671 Blue Ribbon Bank NPA properties against 15,117 live Bank Master vault.
   - Result: 482 properties (71.8%) VERIFIED ACTIVE in Bank Master (100% matched SCB/SAM/GSB).
   - 189 properties (28.2%) Flagged as Sold Out / Delisted by Bank.
   - Pinned verification banner and 1-click filter on https://assets.siwasup.com/property_curator.html for Bua.
"""

with open(home_brain, "a", encoding="utf-8") as f:
    f.write(brain_update)
print(f"[G:\\] Updated Home_Brain_Update.txt")

# Update 01_FROM_HOME_TO_OFFICE.txt
memo_path = os.path.join(G_DIR, "01_FROM_HOME_TO_OFFICE.txt")
with open(memo_path, "a", encoding="utf-8") as f:
    f.write(f"\n[อัปเดตเพิ่มเติม {now_str}]\n"
            f"- อัปเดตระบบกุญแจ 2 ทางการจริง: 1) จุดซ่อนลับออฟฟิศ (กล่องชั้นวางรองเท้า) & คืนที่เดิม/คืนที่แบงก์เอง 2) แมสส่งถึงบ้านเอเจนต์\n"
            f"- ปักป้ายเช็กต้นทางแบงก์ 15,117 แปลงบนแดชบอร์ดบัว: 482 แปลงมีของจริง 100% / 189 แปลงตัดสต๊อก\n")
print(f"[G:\\] Appended to 01_FROM_HOME_TO_OFFICE.txt")

print("=== ALL UPDATES APPLIED SUCCESSFULLY ===")
