# -*- coding: utf-8 -*-
"""
Generate messenger_dispatch_slip.html - Rider-Optimized No-App Dispatch Web Slip.
"""
import os
import sys
import shutil

sys.path.append(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\scripts")
from overnight_r2_crawler import put_object_r2

WEB_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
G_DIR = r"G:\Siwasup_Presentation_2026"

slip_html = """<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <title>Siwasup Smart Dispatch Slip - ใบส่งมอบกุญแจ NPA</title>
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
    
    /* Rider touch optimizations */
    .touch-target {
      min-height: 54px;
    }

    /* Pulse animation */
    @keyframes pulse-ring {
      0% { transform: scale(0.95); opacity: 0.8; }
      50% { transform: scale(1.05); opacity: 0.4; }
      100% { transform: scale(0.95); opacity: 0.8; }
    }
    .pulsing-badge {
      animation: pulse-ring 2.5s infinite ease-in-out;
    }
  </style>
</head>
<body class="min-h-screen bg-[#070A10] flex flex-col items-center justify-start pb-20">

  <!-- TOP APP BAR -->
  <header class="w-full bg-[#0D131F]/90 backdrop-blur-md border-b border-brand-gold/30 sticky top-0 z-50 px-4 py-3 shadow-lg">
    <div class="max-w-md mx-auto flex items-center justify-between">
      <div class="flex items-center gap-2.5">
        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-brand-gold to-brand-goldDark flex items-center justify-center shadow-md shadow-brand-gold/20">
          <i data-lucide="key" class="w-5 h-5 text-slate-950 stroke-[2.5]"></i>
        </div>
        <div>
          <div class="text-[10px] tracking-widest uppercase font-mono text-brand-gold font-bold">SIWASUP DISPATCH SLIP</div>
          <div class="text-sm font-bold text-white tracking-tight flex items-center gap-1.5">
            ใบส่งมอบกุญแจ NPA
            <span class="inline-block w-2 h-2 rounded-full bg-emerald-400 animate-ping"></span>
          </div>
        </div>
      </div>
      <div class="text-right">
        <span class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-xs font-semibold bg-amber-500/15 text-amber-300 border border-amber-500/30 font-mono">
          <i data-lucide="bike" class="w-3.5 h-3.5"></i>
          #MS-8842
        </span>
      </div>
    </div>
  </header>

  <!-- MAIN CONTAINER (Mobile-First 430px max width) -->
  <main class="w-full max-w-md px-4 pt-4 flex flex-col gap-4">

    <!-- URGENCY & TIMELINE CARD -->
    <div class="bg-gradient-to-br from-[#162032] to-[#0E1524] border border-brand-gold/35 rounded-2xl p-4 shadow-xl relative overflow-hidden">
      <!-- Glow background -->
      <div class="absolute -right-8 -top-8 w-32 h-32 bg-brand-gold/10 rounded-full blur-2xl pointer-events-none"></div>

      <div class="flex items-center justify-between mb-3">
        <span class="text-xs font-medium text-slate-400 flex items-center gap-1.5">
          <i data-lucide="clock" class="w-3.5 h-3.5 text-brand-gold"></i>
          เวลานัดส่งมอบกับเอเจนต์
        </span>
        <span class="text-xs font-bold font-mono px-2 py-0.5 rounded bg-emerald-500/20 text-emerald-300 border border-emerald-500/40">
          เหลือเวลา 32 นาที
        </span>
      </div>

      <div class="flex items-baseline justify-between mb-1">
        <div class="text-2xl font-black text-white tracking-tight">14:30 น. <span class="text-sm font-normal text-slate-400">(วันนี้)</span></div>
        <div class="text-xs font-mono text-brand-gold font-semibold">กุญแจถุงซีล #SEC-9901</div>
      </div>

      <!-- Progress bar -->
      <div class="w-full bg-slate-800 h-2 rounded-full mt-3 overflow-hidden">
        <div class="bg-gradient-to-r from-brand-gold to-emerald-400 h-full rounded-full transition-all duration-500" style="width: 65%;"></div>
      </div>
      <div class="flex justify-between text-[11px] text-slate-400 mt-1.5 font-medium">
        <span>1. รับกุญแจแล้ว ✓</span>
        <span class="text-brand-gold font-bold">2. กำลังนำส่ง...</span>
        <span>3. ส่งมอบเอเจนต์</span>
      </div>
    </div>

    <!-- DESTINATION & MAP CARD (BIG ACTION) -->
    <div class="bg-[#131B2B] border border-slate-700/80 rounded-2xl p-4 shadow-lg flex flex-col gap-3">
      <div class="flex items-start justify-between">
        <div>
          <span class="text-[11px] font-bold uppercase tracking-wider text-brand-gold flex items-center gap-1 mb-1">
            <i data-lucide="map-pin" class="w-3.5 h-3.5"></i>
            จุดหมายปลายทาง (หน้าบ้าน NPA)
          </span>
          <h2 class="text-base font-bold text-white leading-snug">
            ม.มัณฑนา บางนา-วงแหวน ซอย 14/2
          </h2>
          <p class="text-xs text-slate-300 mt-0.5">
            บ้านเดี่ยว 2 ชั้น แปลงมุม • รหัสทรัพย์ <span class="font-mono text-brand-gold font-bold">#SCB-4021</span>
          </p>
          <p class="text-[11px] text-slate-400 mt-1">
            กม.8 ถนนบางนา-ตราด ต.บางแก้ว อ.บางพลี จ.สมุทรปราการ
          </p>
        </div>
      </div>

      <!-- BIG NAVIGATION BUTTON (Google Maps 1-Tap) -->
      <a href="https://maps.google.com/?q=13.6625,100.6780" target="_blank"
         class="touch-target w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 text-white font-bold rounded-xl flex items-center justify-center gap-2.5 shadow-lg shadow-blue-600/30 transition-all active:scale-[0.98]">
        <i data-lucide="navigation" class="w-5 h-5 fill-white"></i>
        <span class="text-base">กดเปิด Google Maps นำทางทันที</span>
      </a>
      <div class="text-[11px] text-center text-slate-400">
        ระยะทางจากจุดปัจจุบัน: ประมาณ <strong class="text-white">4.8 กม. (12 นาที)</strong>
      </div>
    </div>

    <!-- AGENT RECIPIENT CARD (CALL 1-TAP) -->
    <div class="bg-[#131B2B] border border-slate-700/80 rounded-2xl p-4 shadow-lg flex flex-col gap-3">
      <span class="text-[11px] font-bold uppercase tracking-wider text-brand-gold flex items-center gap-1">
        <i data-lucide="user-check" class="w-3.5 h-3.5"></i>
        เอเจนต์ผู้รับมอบกุญแจหน้างาน
      </span>

      <div class="flex items-center gap-3.5 bg-slate-900/60 p-3 rounded-xl border border-slate-800">
        <div class="w-12 h-12 rounded-full bg-gradient-to-br from-amber-400/20 to-brand-gold/30 border border-brand-gold/40 flex items-center justify-center text-lg font-black text-brand-gold flex-shrink-0">
          นท
        </div>
        <div class="flex-1 min-w-0">
          <div class="text-sm font-bold text-white flex items-center gap-2">
            คุณนัทธมน ภาคินัย
            <span class="text-[10px] bg-brand-gold/20 text-brand-gold px-1.5 py-0.5 rounded font-mono font-bold">Alpha #S02</span>
          </div>
          <div class="text-xs text-slate-400 mt-0.5 font-mono">081-999-8888</div>
          <div class="text-[11px] text-emerald-400 mt-0.5 flex items-center gap-1">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
            ยืนยันรอลูกค้าหน้าบ้านแล้ว
          </div>
        </div>
      </div>

      <!-- CALL AGENT 1-TAP BUTTON -->
      <a href="tel:0819998888"
         class="touch-target w-full bg-gradient-to-r from-emerald-600 to-teal-600 hover:from-emerald-500 hover:to-teal-500 text-white font-bold rounded-xl flex items-center justify-center gap-2 shadow-lg shadow-emerald-600/25 transition-all active:scale-[0.98]">
        <i data-lucide="phone-call" class="w-5 h-5"></i>
        <span class="text-base">โทรหาเอเจนต์คุณนัทธมน (081-999-8888)</span>
      </a>
    </div>

    <!-- HANDOVER VERIFICATION MODES -->
    <div class="bg-[#131B2B] border border-brand-gold/30 rounded-2xl p-4 shadow-lg flex flex-col gap-3">
      <div class="flex items-center justify-between">
        <span class="text-[11px] font-bold uppercase tracking-wider text-brand-gold flex items-center gap-1">
          <i data-lucide="shield-check" class="w-3.5 h-3.5"></i>
          ขั้นตอนยืนยันการส่งมอบกุญแจ
        </span>
        <span class="text-[10px] text-slate-400">เลือก 1 ใน 2 วิธี</span>
      </div>

      <!-- Option Tabs -->
      <div class="grid grid-cols-2 gap-2 p-1 bg-slate-900 rounded-xl border border-slate-800">
        <button id="tabQrBtn" onclick="switchMode('qr')" class="py-2 text-xs font-bold rounded-lg bg-brand-gold text-slate-950 transition-all flex items-center justify-center gap-1.5 shadow">
          <i data-lucide="qr-code" class="w-3.5 h-3.5"></i>
          ยื่น QR ให้สแกน
        </button>
        <button id="tabPhotoBtn" onclick="switchMode('photo')" class="py-2 text-xs font-medium rounded-lg text-slate-400 hover:text-white transition-all flex items-center justify-center gap-1.5">
          <i data-lucide="camera" class="w-3.5 h-3.5"></i>
          ถ่ายรูปส่งมอบ
        </button>
      </div>

      <!-- Mode 1: QR Display -->
      <div id="qrModeBlock" class="flex flex-col items-center justify-center py-4 bg-slate-900/80 rounded-xl border border-slate-800">
        <div class="bg-white p-3.5 rounded-2xl shadow-xl border-4 border-brand-gold mb-3">
          <!-- Dynamic SVG QR Placeholder -->
          <svg class="w-40 h-40" viewBox="0 0 120 120" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect width="120" height="120" fill="white"/>
            <!-- Corner Markers -->
            <rect x="10" y="10" width="30" height="30" fill="black"/>
            <rect x="15" y="15" width="20" height="20" fill="white"/>
            <rect x="20" y="20" width="10" height="10" fill="black"/>
            <rect x="80" y="10" width="30" height="30" fill="black"/>
            <rect x="85" y="15" width="20" height="20" fill="white"/>
            <rect x="90" y="20" width="10" height="10" fill="black"/>
            <rect x="10" y="80" width="30" height="30" fill="black"/>
            <rect x="15" y="85" width="20" height="20" fill="white"/>
            <rect x="20" y="90" width="10" height="10" fill="black"/>
            <!-- Data pattern -->
            <rect x="45" y="15" width="8" height="8" fill="black"/>
            <rect x="58" y="15" width="12" height="8" fill="black"/>
            <rect x="45" y="30" width="15" height="10" fill="black"/>
            <rect x="65" y="28" width="8" height="12" fill="black"/>
            <rect x="20" y="45" width="8" height="15" fill="black"/>
            <rect x="35" y="45" width="10" height="8" fill="black"/>
            <rect x="50" y="45" width="20" height="20" fill="black"/>
            <rect x="75" y="45" width="10" height="12" fill="black"/>
            <rect x="90" y="45" width="15" height="8" fill="black"/>
            <rect x="15" y="65" width="15" height="8" fill="black"/>
            <rect x="35" y="60" width="8" height="15" fill="black"/>
            <rect x="75" y="62" width="12" height="10" fill="black"/>
            <rect x="95" y="60" width="8" height="15" fill="black"/>
            <rect x="45" y="70" width="15" height="12" fill="black"/>
            <rect x="65" y="75" width="10" height="8" fill="black"/>
            <rect x="45" y="88" width="10" height="15" fill="black"/>
            <rect x="60" y="88" width="25" height="8" fill="black"/>
            <rect x="90" y="80" width="15" height="12" fill="black"/>
            <rect x="70" y="100" width="18" height="8" fill="black"/>
            <rect x="92" y="96" width="12" height="12" fill="black"/>
          </svg>
        </div>
        <p class="text-xs font-semibold text-white">ยื่นหน้าจอนี้ให้เอเจนต์สแกนผ่านแชท LINE</p>
        <p class="text-[11px] text-slate-400 mt-0.5">ระบบจะบันทึกสถานะจบงานทันทีที่เอเจนต์สแกน</p>
      </div>

      <!-- Mode 2: Photo Capture (Hidden by default) -->
      <div id="photoModeBlock" class="hidden flex-col items-center justify-center p-4 bg-slate-900/80 rounded-xl border border-slate-800 gap-3 text-center">
        <div class="w-16 h-16 rounded-full bg-slate-800 flex items-center justify-center border border-slate-700">
          <i data-lucide="camera" class="w-8 h-8 text-slate-300"></i>
        </div>
        <div>
          <p class="text-xs font-semibold text-white">ถ่ายรูปถุงซีลกุญแจคู่กับเอเจนต์/ป้ายบ้าน</p>
          <p class="text-[11px] text-slate-400 mt-0.5">กรณีเอเจนต์มือถือแบตหมดหรือไม่สะดวกสแกน QR</p>
        </div>
        <label class="w-full touch-target bg-slate-800 hover:bg-slate-700 border border-slate-600 text-white font-bold rounded-xl flex items-center justify-center gap-2 cursor-pointer transition-all active:scale-98">
          <i data-lucide="camera" class="w-5 h-5 text-brand-gold"></i>
          <span>กดถ่ายรูปหรือเลือกรูปจากกล้อง</span>
          <input type="file" accept="image/*" capture="environment" class="hidden" onchange="handlePhotoUpload(this)">
        </label>
        <div id="photoPreviewWrap" class="hidden w-full text-left bg-slate-950 p-2 rounded-lg border border-emerald-500/50">
          <span class="text-[11px] text-emerald-400 font-bold flex items-center gap-1">
            <i data-lucide="check-circle" class="w-3.5 h-3.5"></i>
            แนบรูปถ่ายเรียบร้อยแล้ว
          </span>
        </div>
      </div>

      <!-- BIG SLIDE TO COMPLETE -->
      <button id="completeBtn" onclick="confirmDelivery()"
              class="touch-target w-full mt-1 bg-gradient-to-r from-brand-gold to-brand-goldDark text-slate-950 font-black text-base rounded-xl flex items-center justify-center gap-2 shadow-lg shadow-brand-gold/30 hover:brightness-110 active:scale-[0.98] transition-all">
        <i data-lucide="check-circle-2" class="w-5 h-5 stroke-[2.5]"></i>
        <span>กดเพื่อจบงานและส่งมอบสำเร็จ ✓</span>
      </button>
    </div>

    <!-- EMERGENCY CONTACT (P'LILY) -->
    <div class="bg-slate-900/60 border border-slate-800 rounded-2xl p-3.5 flex items-center justify-between text-xs">
      <div class="flex items-center gap-2.5">
        <div class="w-8 h-8 rounded-full bg-rose-500/20 text-rose-400 flex items-center justify-center border border-rose-500/30">
          <i data-lucide="help-circle" class="w-4 h-4"></i>
        </div>
        <div>
          <div class="text-white font-semibold">พบปัญหา / หาบ้านไม่เจอ?</div>
          <div class="text-[11px] text-slate-400">ติดต่อ พี่ลิลลี่ (ห้องเซฟกุญแจ)</div>
        </div>
      </div>
      <a href="tel:021234567" class="px-3 py-2 rounded-lg bg-rose-500/15 border border-rose-500/30 text-rose-300 font-bold flex items-center gap-1 active:scale-95 transition-all">
        <i data-lucide="phone" class="w-3.5 h-3.5"></i>
        โทรด่วน
      </a>
    </div>

  </main>

  <!-- SUCCESS MODAL (Hidden by default) -->
  <div id="successModal" class="hidden fixed inset-0 z-50 bg-black/85 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-gradient-to-b from-[#182338] to-[#0D1424] border-2 border-emerald-500 rounded-3xl p-6 max-w-sm w-full text-center shadow-2xl relative">
      <div class="w-16 h-16 rounded-full bg-emerald-500/20 border-2 border-emerald-400 flex items-center justify-center mx-auto mb-4 shadow-lg shadow-emerald-500/40">
        <i data-lucide="check" class="w-8 h-8 text-emerald-400 stroke-[3]"></i>
      </div>
      <h3 class="text-xl font-black text-white mb-1">ส่งมอบกุญแจสำเร็จแล้ว!</h3>
      <p class="text-xs text-slate-300 mb-4 leading-relaxed">
        ระบบบันทึกเวลา GPS และแจ้งเตือนห้องเซฟของพี่ลิลลี่เรียบร้อยแล้ว ขอบคุณสำหรับการปฏิบัติงานอย่างรวดเร็วและปลอดภัยครับ
      </p>
      <div class="bg-slate-900/80 p-3 rounded-xl border border-slate-800 text-[11px] text-slate-300 mb-5 font-mono">
        <div>รหัสงาน: #MS-8842</div>
        <div>เวลาส่งมอบ: <span id="finishTimeText">14:15:30 น.</span></div>
        <div class="text-emerald-400 font-bold mt-1">สถานะ: Delivered ✓</div>
      </div>
      <button onclick="closeModal()" class="w-full touch-target bg-emerald-500 hover:bg-emerald-400 text-slate-950 font-black rounded-xl text-sm transition-all shadow-lg shadow-emerald-500/30">
        ตกลง / ปิดหน้าต่างนี้
      </button>
    </div>
  </div>

  <script>
    lucide.createIcons();

    function switchMode(mode) {
      const qrBtn = document.getElementById('tabQrBtn');
      const photoBtn = document.getElementById('tabPhotoBtn');
      const qrBlock = document.getElementById('qrModeBlock');
      const photoBlock = document.getElementById('photoModeBlock');

      if (mode === 'qr') {
        qrBtn.className = "py-2 text-xs font-bold rounded-lg bg-brand-gold text-slate-950 transition-all flex items-center justify-center gap-1.5 shadow";
        photoBtn.className = "py-2 text-xs font-medium rounded-lg text-slate-400 hover:text-white transition-all flex items-center justify-center gap-1.5";
        qrBlock.classList.remove('hidden');
        qrBlock.classList.add('flex');
        photoBlock.classList.add('hidden');
        photoBlock.classList.remove('flex');
      } else {
        photoBtn.className = "py-2 text-xs font-bold rounded-lg bg-brand-gold text-slate-950 transition-all flex items-center justify-center gap-1.5 shadow";
        qrBtn.className = "py-2 text-xs font-medium rounded-lg text-slate-400 hover:text-white transition-all flex items-center justify-center gap-1.5";
        photoBlock.classList.remove('hidden');
        photoBlock.classList.add('flex');
        qrBlock.classList.add('hidden');
        qrBlock.classList.remove('flex');
      }
      lucide.createIcons();
    }

    function handlePhotoUpload(input) {
      if (input.files && input.files[0]) {
        document.getElementById('photoPreviewWrap').classList.remove('hidden');
      }
    }

    function confirmDelivery() {
      const now = new Date();
      const timeStr = now.toLocaleTimeString('th-TH') + ' น.';
      document.getElementById('finishTimeText').innerText = timeStr;
      document.getElementById('successModal').classList.remove('hidden');
    }

    function closeModal() {
      document.getElementById('successModal').classList.add('hidden');
    }
  </script>
</body>
</html>
"""

# Save locally to repo
slip_path_web = os.path.join(WEB_DIR, "messenger_dispatch_slip.html")
with open(slip_path_web, "w", encoding="utf-8") as f:
    f.write(slip_html)
print(f"[LOCAL] Saved {slip_path_web}")

# Save to G:
slip_path_g = os.path.join(G_DIR, "messenger_dispatch_slip.html")
with open(slip_path_g, "w", encoding="utf-8") as f:
    f.write(slip_html)
print(f"[G:\\] Saved {slip_path_g}")

# Deploy to Cloudflare R2
with open(slip_path_web, "rb") as f:
    data = f.read()
st = put_object_r2("messenger_dispatch_slip.html", data, "text/html; charset=utf-8")
print(f"[R2] Deployed messenger_dispatch_slip.html ({len(data)} bytes) -> Status: {st}")

print("=== MESSENGER DISPATCH SLIP CREATED & DEPLOYED ===")
