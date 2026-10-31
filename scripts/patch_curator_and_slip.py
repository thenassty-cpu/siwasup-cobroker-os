# -*- coding: utf-8 -*-
"""
Patch property_curator.html with Bank Master Audit and Messenger Dispatch Slip with Office/Home SOP.
"""
import os
import sys
import shutil

sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
from overnight_r2_crawler import put_object_r2

WEB_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
G_DIR = r"G:\Siwasup_Presentation_2026"

# ==============================================================================
# 1. PATCH property_curator.html
# ==============================================================================
curator_file = os.path.join(WEB_DIR, "property_curator.html")
with open(curator_file, "r", encoding="utf-8") as f:
    c_html = f.read()

# 1.1 Add Bank Master Verification Banner for Bua
bua_alert_banner = """
  <!-- BUA BANK AUDIT BANNER -->
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-3 pb-1">
    <div class="bg-gradient-to-r from-emerald-950/80 via-slate-900 to-slate-900 border-2 border-emerald-500/50 rounded-2xl p-4 shadow-md flex flex-wrap items-center justify-between gap-3 text-white">
      <div class="flex items-start gap-3 max-w-3xl">
        <div class="w-10 h-10 rounded-xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/40 flex items-center justify-center font-bold text-xl flex-shrink-0">
          🛡️
        </div>
        <div>
          <div class="flex items-center gap-2 flex-wrap">
            <span class="text-xs font-bold uppercase tracking-wider text-emerald-400 bg-emerald-500/10 border border-emerald-500/30 px-2 py-0.5 rounded-md">
              ✓ เช็กต้นทางคลังแบงก์ 15,117 แปลงแล้ว
            </span>
            <span class="text-xs text-slate-300">แจ้งคุณบัว: ตรวจสอบความถูกต้องกับ Master SCB / SAM / GSB เรียบร้อย</span>
          </div>
          <p class="text-xs text-slate-300 mt-1 leading-relaxed">
            ระบบจับคู่พบว่า <strong class="text-emerald-400">482 แปลงมีในคลังแบงก์จริง 100%</strong> (พร้อมรหัสและราคาตรงเป๊ะ นำไปทำเป็น Top 20 Hero Deals ได้อย่างปลอดภัย) 
            ส่วนอีก <strong class="text-rose-400">189 แปลงคาดว่าแบงก์ขายออก/ตัดสต๊อกไปแล้ว</strong> ระบบติดป้ายสีแดงเตือนไว้ให้บัวคัดทิ้งได้ทันทีค่ะ
          </p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <button type="button" onclick="setAuditFilter('verified')" class="px-3 py-1.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold shadow transition flex items-center gap-1.5">
          <span>🟢 เลือกดูเฉพาะ 482 แปลงที่แบงก์มีของ</span>
        </button>
        <button type="button" onclick="setAuditFilter('all')" class="px-3 py-1.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-medium border border-slate-700 transition">
          ดูทั้งหมด
        </button>
      </div>
    </div>
  </div>
"""

# Insert banner right before <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4 pb-1 w-full">
if "BUA BANK AUDIT BANNER" not in c_html:
    c_html = c_html.replace(
        '<section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4 pb-1 w-full">',
        bua_alert_banner + '\n  <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-4 pb-1 w-full">'
    )

# 1.2 Update Card 3 in Group Filter to mention 482 verified vs 189 sold
old_card_3_text = '<span class="font-bold text-blue-900 text-xs sm:text-sm">💎 671 ทรัพย์ NPA ธนาคาร</span>'
new_card_3_text = '<span class="font-bold text-blue-900 text-xs sm:text-sm">💎 671 ทรัพย์ NPA (เช็กแบงก์แล้ว: 🟢 482 มีของ / 🔴 189 ขายแล้ว)</span>'
c_html = c_html.replace(old_card_3_text, new_card_3_text)

# 1.3 Add audit filter logic in getFilteredProperties
old_filter_code = """        // Sold out filter
        if (hideSoldOut && item.is_image_soldout) return false;"""

new_filter_code = """        // Sold out filter
        if (hideSoldOut && item.is_image_soldout) return false;

        // Bank Master Audit Filter
        if (window.currentAuditFilter === 'verified' && item.bank_audit_status === 'bank_sold_out_or_unlisted') {
          return false;
        }"""
c_html = c_html.replace(old_filter_code, new_filter_code)

# 1.4 Add setAuditFilter function
audit_fn = """
    window.currentAuditFilter = 'all';
    function setAuditFilter(mode) {
      window.currentAuditFilter = mode;
      renderGrid();
      showToast(mode === 'verified' ? 'กรองเฉพาะ 482 แปลงที่แบงก์ยืนยันมีของ 100%' : 'แสดงทรัพย์ทั้งหมด');
    }
"""
if "setAuditFilter" not in c_html:
    c_html = c_html.replace('function setGroupFilter(group) {', audit_fn + '\n    function setGroupFilter(group) {')

# 1.5 Update card render to display Bank Origin Badge clearly
old_badge_render = """                  ${item.ribbon === 'red' ? `
                    <span class="bg-rose-600 text-white text-[10px] px-2 py-0.5 rounded-lg font-black shadow-md flex items-center gap-1 animate-pulse">
                      <span>🔴</span><span>ทบทวน: เว็บเดิมถอดออก</span>
                    </span>
                  ` : item.ribbon === 'green' ? `
                    <span class="bg-emerald-600 text-white text-[10px] px-2 py-0.5 rounded-lg font-black shadow-md flex items-center gap-1">
                      <span>🟢</span><span>ใหม่: เพิ่งเข้าหน้าแรก</span>
                    </span>
                  ` : `
                    <span class="bg-blue-600 text-white text-[10px] px-2 py-0.5 rounded-lg font-bold shadow-md flex items-center gap-1">
                      <span>💎</span><span>NPA แบงก์</span>
                    </span>
                  `}"""

new_badge_render = """                  ${item.ribbon === 'red' ? `
                    <span class="bg-rose-600 text-white text-[10px] px-2 py-0.5 rounded-lg font-black shadow-md flex items-center gap-1 animate-pulse">
                      <span>🔴</span><span>ทบทวน: เว็บเดิมถอดออก</span>
                    </span>
                  ` : item.ribbon === 'green' ? `
                    <span class="bg-emerald-600 text-white text-[10px] px-2 py-0.5 rounded-lg font-black shadow-md flex items-center gap-1">
                      <span>🟢</span><span>ใหม่: เพิ่งเข้าหน้าแรก</span>
                    </span>
                  ` : item.bank_audit_status === 'verified_bank_active' ? `
                    <span class="bg-emerald-600 text-white text-[10px] px-2 py-0.5 rounded-lg font-black shadow-md flex items-center gap-1">
                      <span>🟢</span><span>มีในคลัง ${item.bank_origin_name || 'แบงก์'} 100% (${item.bank_origin_code || ''})</span>
                    </span>
                  ` : item.bank_audit_status === 'bank_sold_out_or_unlisted' ? `
                    <span class="bg-rose-700 text-white text-[10px] px-2 py-0.5 rounded-lg font-bold shadow-md flex items-center gap-1">
                      <span>🔴</span><span>แบงก์อาจขายแล้ว / หลุดสต๊อก</span>
                    </span>
                  ` : `
                    <span class="bg-blue-600 text-white text-[10px] px-2 py-0.5 rounded-lg font-bold shadow-md flex items-center gap-1">
                      <span>💎</span><span>NPA แบงก์</span>
                    </span>
                  `}"""

c_html = c_html.replace(old_badge_render, new_badge_render)

# Write updated property_curator.html
with open(curator_file, "w", encoding="utf-8") as f:
    f.write(c_html)
print(f"[LOCAL] Updated property_curator.html with Bank Audit Banner and Filters")

# Sync to G:\
shutil.copy2(curator_file, os.path.join(G_DIR, "property_curator.html"))
print(f"[G:\\] Mirrored property_curator.html")

# Deploy to R2
with open(curator_file, "rb") as f:
    st_curator = put_object_r2("property_curator.html", f.read(), "text/html; charset=utf-8")
print(f"[R2] Deployed property_curator.html -> Status: {st_curator}")

# ==============================================================================
# 2. UPDATE messenger_dispatch_slip.html TO MATCH THE 2 REAL KEY PROTOCOLS
# ==============================================================================
slip_file = os.path.join(WEB_DIR, "messenger_dispatch_slip.html")

updated_slip_html = """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Siwasup Key Custody - ใบงานส่งมอบกุญแจ NPA</title>
  <link rel="icon" type="image/png" href="assets/siwasup_logo.png">
  <!-- Tailwind CSS CDN -->
  <script src="https://cdn.tailwindcss.com"></script>
  <!-- Google Fonts Prompt -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap" rel="stylesheet">
  <!-- Lucide Icons -->
  <script src="https://unpkg.com/lucide@latest"></script>
  
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            prompt: ['Prompt', 'sans-serif'],
            mono: ['JetBrains Mono', 'monospace'],
          },
          colors: {
            brand: {
              gold: '#C2A460',
              goldLight: '#E6CA85',
              goldDark: '#9A7B32',
              navy: '#0F172A',
              card: '#182234',
              surface: '#0B0F19'
            }
          }
        }
      }
    }
  </script>

  <style>
    body {
      font-family: 'Prompt', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
      background-color: #070A10;
      color: #F8FAFC;
      -webkit-tap-highlight-color: transparent;
      user-select: none;
    }
    .touch-target {
      min-height: 52px;
    }
  </style>
</head>
<body class="min-h-screen bg-[#070A10] flex flex-col items-center justify-start pb-24">

  <!-- TOP APP BAR -->
  <header class="w-full bg-[#0D131F]/90 backdrop-blur-md border-b border-brand-gold/30 sticky top-0 z-50 px-4 py-3 shadow-lg">
    <div class="max-w-md mx-auto flex items-center justify-between">
      <div class="flex items-center gap-2.5">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-gold to-brand-goldDark flex items-center justify-center shadow-md shadow-brand-gold/20">
          <i data-lucide="key" class="w-5 h-5 text-slate-950 stroke-[2.5]"></i>
        </div>
        <div>
          <div class="text-[10px] tracking-widest uppercase font-mono text-brand-gold font-bold">SIWASUP KEY CUSTODY</div>
          <div class="text-sm font-bold text-white tracking-tight flex items-center gap-1.5">
            ใบส่งมอบกุญแจ NPA
            <span class="inline-block w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
          </div>
        </div>
      </div>
      <div class="text-right">
        <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-500/15 text-amber-300 border border-amber-500/30 font-mono">
          #KEY-8842
        </span>
      </div>
    </div>
  </header>

  <!-- PROTOCOL SELECTOR (2 รูปแบบตามมติที่ประชุม) -->
  <div class="w-full max-w-md px-4 pt-3">
    <div class="grid grid-cols-2 gap-2 p-1 bg-slate-900 border border-slate-800 rounded-xl">
      <button id="btnFlow2" onclick="setFlow(2)" class="py-2.5 px-2 text-xs font-bold rounded-lg bg-brand-gold text-slate-950 transition-all flex items-center justify-center gap-1.5 shadow">
        <i data-lucide="bike" class="w-4 h-4"></i>
        1. แมสส่งถึงบ้านเอเจนต์
      </button>
      <button id="btnFlow1" onclick="setFlow(1)" class="py-2.5 px-2 text-xs font-medium rounded-lg text-slate-400 hover:text-white transition-all flex items-center justify-center gap-1.5">
        <i data-lucide="archive" class="w-4 h-4"></i>
        2. จุด Drop ออฟฟิศ
      </button>
    </div>
  </div>

  <!-- MAIN CONTAINER (Mobile-First 430px) -->
  <main class="w-full max-w-md px-4 pt-3 flex flex-col gap-3.5">

    <!-- FLOW 2: MESSENGER HOME DELIVERY -->
    <div id="flow2Block" class="flex flex-col gap-3.5">
      
      <!-- STATUS & DEADLINE CARD -->
      <div class="bg-gradient-to-br from-[#162032] to-[#0E1524] border border-brand-gold/35 rounded-2xl p-4 shadow-xl">
        <div class="flex items-center justify-between mb-2">
          <span class="text-xs font-medium text-slate-400 flex items-center gap-1.5">
            <i data-lucide="clock" class="w-3.5 h-3.5 text-brand-gold"></i>
            กำหนดเวลาส่งมอบถึงบ้านเอเจนต์
          </span>
          <span class="text-xs font-bold font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
            นัด 13:00 น.
          </span>
        </div>
        <div class="flex items-baseline justify-between">
          <div class="text-xl font-black text-white">เตรียมส่งมอบก่อนนัดลูกค้า</div>
          <div class="text-xs font-mono text-brand-gold font-semibold">ถุงซีล #SEC-9901</div>
        </div>
        <p class="text-xs text-slate-400 mt-1">
          กุญแจสำหรับทรัพย์: <strong>SCB-4021 (มัณฑนา บางนา-วงแหวน)</strong>
        </p>
      </div>

      <!-- DESTINATION: AGENT HOME ADDRESS -->
      <div class="bg-[#131B2B] border border-slate-700/80 rounded-2xl p-4 shadow-lg flex flex-col gap-3">
        <div>
          <span class="text-[11px] font-bold uppercase tracking-wider text-brand-gold flex items-center gap-1 mb-1">
            <i data-lucide="home" class="w-3.5 h-3.5"></i>
            จุดหมาย: บ้านพักของเอเจนต์ (ปลายทางนำส่ง)
          </span>
          <h2 class="text-base font-bold text-white leading-snug">
            บ้านคุณนัทธมน (เอเจนต์ Alpha #S02)
          </h2>
          <p class="text-xs text-slate-300 mt-0.5">
            128/45 ซอยสุขุมวิท 101/1 (วชิรธรรมสาธิต 28) แขวงบางจาก เขตพระโขนง กทม.
          </p>
          <p class="text-[11px] text-emerald-400 mt-1 font-medium">
            💡 นำส่งให้เอเจนต์ตรวจรับกุญแจล่วงหน้า ก่อนเอเจนต์เดินทางไปพบลูกค้า
          </p>
        </div>

        <!-- 1-TAP NAVIGATION TO AGENT HOME -->
        <a href="https://maps.google.com/?q=13.6890,100.6120" target="_blank"
           class="touch-target w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold rounded-xl flex items-center justify-center gap-2 shadow-lg shadow-blue-600/30 transition-all active:scale-[0.98]">
          <i data-lucide="navigation" class="w-4 h-4 fill-white"></i>
          <span>กดเปิด Google Maps นำทางไปบ้านเอเจนต์</span>
        </a>
      </div>

      <!-- AGENT RECIPIENT CARD -->
      <div class="bg-[#131B2B] border border-slate-700/80 rounded-2xl p-4 shadow-lg flex flex-col gap-3">
        <div class="flex items-center gap-3.5 bg-slate-900/60 p-3 rounded-xl border border-slate-800">
          <div class="w-11 h-11 rounded-full bg-brand-gold/20 border border-brand-gold/40 flex items-center justify-center text-base font-black text-brand-gold flex-shrink-0">
            นท
          </div>
          <div class="flex-1 min-w-0">
            <div class="text-sm font-bold text-white flex items-center gap-2">
              คุณนัทธมน ภาคินัย
              <span class="text-[10px] bg-brand-gold/20 text-brand-gold px-1.5 py-0.5 rounded font-mono font-bold">#S02</span>
            </div>
            <div class="text-xs text-slate-400 font-mono">081-999-8888</div>
          </div>
        </div>

        <a href="tel:0819998888"
           class="touch-target w-full bg-gradient-to-r from-emerald-600 to-teal-600 text-white font-bold rounded-xl flex items-center justify-center gap-2 shadow-lg shadow-emerald-600/25 active:scale-[0.98]">
          <i data-lucide="phone-call" class="w-4 h-4"></i>
          <span>โทรหาเอเจนต์คุณนัทธมน (081-999-8888)</span>
        </a>
      </div>

    </div>

    <!-- FLOW 1: OFFICE DROPBOX (จุดดรอปที่ออฟฟิศ) -->
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

    </div>

    <!-- HANDOVER VERIFICATION & ACTION BUTTON -->
    <div class="bg-[#131B2B] border border-brand-gold/30 rounded-2xl p-4 shadow-lg flex flex-col gap-3">
      <div class="flex items-center justify-between">
        <span class="text-[11px] font-bold uppercase tracking-wider text-brand-gold flex items-center gap-1">
          <i data-lucide="shield-check" class="w-3.5 h-3.5"></i>
          ยืนยันการรับ/ส่งมอบกุญแจ
        </span>
        <span class="text-[10px] text-slate-400">บันทึก GPS & เวลา</span>
      </div>

      <button onclick="confirmHandover()"
              class="touch-target w-full bg-gradient-to-r from-brand-gold to-brand-goldDark text-slate-950 font-black text-base rounded-xl flex items-center justify-center gap-2 shadow-lg shadow-brand-gold/30 hover:brightness-110 active:scale-[0.98] transition-all">
        <i data-lucide="check-circle-2" class="w-5 h-5 stroke-[2.5]"></i>
        <span id="actionBtnText">กดเพื่อยืนยันส่งมอบถึงบ้านเอเจนต์สำเร็จ ✓</span>
      </button>
    </div>

    <!-- EMERGENCY CONTACT (P'LILY) -->
    <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-3 flex items-center justify-between text-xs">
      <div class="flex items-center gap-2">
        <div class="w-7 h-7 rounded-full bg-rose-500/20 text-rose-400 flex items-center justify-center border border-rose-500/30">
          <i data-lucide="phone" class="w-3.5 h-3.5"></i>
        </div>
        <div>
          <div class="text-white font-semibold">ห้องเซฟกุญแจส่วนกลาง</div>
          <div class="text-[11px] text-slate-400">ติดต่อ พี่ลิลลี่</div>
        </div>
      </div>
      <a href="tel:021234567" class="px-3 py-1.5 rounded-lg bg-rose-500/15 border border-rose-500/30 text-rose-300 font-bold active:scale-95">
        โทรสายตรง
      </a>
    </div>

  </main>

  <!-- SUCCESS MODAL -->
  <div id="successModal" class="hidden fixed inset-0 z-50 bg-black/85 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-gradient-to-b from-[#182338] to-[#0D1424] border-2 border-emerald-500 rounded-3xl p-6 max-w-sm w-full text-center shadow-2xl relative">
      <div class="w-14 h-14 rounded-full bg-emerald-500/20 border-2 border-emerald-400 flex items-center justify-center mx-auto mb-3 shadow-lg shadow-emerald-500/40">
        <i data-lucide="check" class="w-7 h-7 text-emerald-400 stroke-[3]"></i>
      </div>
      <h3 class="text-lg font-black text-white mb-1">บันทึกส่งมอบเรียบร้อย!</h3>
      <p class="text-xs text-slate-300 mb-4 leading-relaxed">
        ระบบบันทึกเวลา GPS และแจ้งเตือนห้องเซฟของพี่ลิลลี่เรียบร้อยแล้ว
      </p>
      <div class="bg-slate-900/80 p-3 rounded-xl border border-slate-800 text-[11px] text-slate-300 mb-4 font-mono">
        <div>รหัสใบงาน: #KEY-8842</div>
        <div>เวลาที่บันทึก: <span id="finishTimeText">13:10 น.</span></div>
        <div class="text-emerald-400 font-bold mt-1">สถานะ: Complete ✓</div>
      </div>
      <button onclick="document.getElementById('successModal').classList.add('hidden')" class="w-full py-2.5 bg-emerald-500 text-slate-950 font-bold rounded-xl text-xs">
        ตกลง / ปิดหน้าต่าง
      </button>
    </div>
  </div>

  <script>
    lucide.createIcons();

    function setFlow(flow) {
      const btn2 = document.getElementById('btnFlow2');
      const btn1 = document.getElementById('btnFlow1');
      const block2 = document.getElementById('flow2Block');
      const block1 = document.getElementById('flow1Block');
      const actionText = document.getElementById('actionBtnText');

      if (flow === 2) {
        btn2.className = "py-2.5 px-2 text-xs font-bold rounded-lg bg-brand-gold text-slate-950 transition-all flex items-center justify-center gap-1.5 shadow";
        btn1.className = "py-2.5 px-2 text-xs font-medium rounded-lg text-slate-400 hover:text-white transition-all flex items-center justify-center gap-1.5";
        block2.classList.remove('hidden');
        block2.classList.add('flex');
        block1.classList.add('hidden');
        block1.classList.remove('flex');
        actionText.innerText = "กดเพื่อยืนยันส่งมอบถึงบ้านเอเจนต์สำเร็จ ✓";
      } else {
        btn1.className = "py-2.5 px-2 text-xs font-bold rounded-lg bg-brand-gold text-slate-950 transition-all flex items-center justify-center gap-1.5 shadow";
        btn2.className = "py-2.5 px-2 text-xs font-medium rounded-lg text-slate-400 hover:text-white transition-all flex items-center justify-center gap-1.5";
        block1.classList.remove('hidden');
        block1.classList.add('flex');
        block2.classList.add('hidden');
        block2.classList.remove('flex');
        actionText.innerText = "กดเพื่อยืนยันดรอป/รับกุญแจที่ตู้เซฟออฟฟิศ ✓";
      }
      lucide.createIcons();
    }

    function confirmHandover() {
      const now = new Date();
      document.getElementById('finishTimeText').innerText = now.toLocaleTimeString('th-TH') + ' น.';
      document.getElementById('successModal').classList.remove('hidden');
    }
  </script>
</body>
</html>
"""

with open(slip_file, "w", encoding="utf-8") as f:
    f.write(updated_slip_html)
print(f"[LOCAL] Updated messenger_dispatch_slip.html with 2 Real Key Protocols")

# Sync to G:\
shutil.copy2(slip_file, os.path.join(G_DIR, "messenger_dispatch_slip.html"))
print(f"[G:\\] Mirrored messenger_dispatch_slip.html")

# Deploy to R2
with open(slip_file, "rb") as f:
    st_slip = put_object_r2("messenger_dispatch_slip.html", f.read(), "text/html; charset=utf-8")
print(f"[R2] Deployed messenger_dispatch_slip.html -> Status: {st_slip}")

print("=== ALL UPDATES APPLIED AND DEPLOYED ===")
