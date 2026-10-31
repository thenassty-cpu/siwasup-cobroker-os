# -*- coding: utf-8 -*-
import os
import sys

HTML_CONTENT = '''<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <title>Siwasup Asset - นามบัตรที่ปรึกษาอสังหาริมทรัพย์ (Property Consultant Card)</title>
  <link rel="icon" type="image/png" href="assets/siwasup_logo.png" />
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet" />
  <style>
    body {
      font-family: 'Prompt', 'Tahoma', sans-serif;
      background-color: #f1f5f9;
      color: #0f172a;
      -webkit-font-smoothing: antialiased;
    }
    .squircle-37 {
      border-radius: 37px;
    }
    @media (max-width: 400px) {
      .squircle-37 {
        border-radius: 30px;
      }
    }
  </style>
</head>
<body class="min-h-screen flex flex-col justify-between p-2.5 sm:p-5 lg:p-8">

  <div class="max-w-md mx-auto w-full space-y-3 sm:space-y-4">

    <!-- Top Mode Switcher (Visible ONLY for internal testing/setup) -->
    <div id="internalControlBar" class="bg-white border border-slate-200 rounded-2xl p-2.5 sm:p-3 shadow-xs space-y-2 text-xs">
      <div class="flex items-center justify-between gap-2">
        <span class="text-slate-500 font-medium">สลับดูตัวแทน Alpha:</span>
        <select id="agentSelect" onchange="changeAgent(this.value)" class="bg-slate-50 border border-slate-300 rounded-lg px-2 py-1 font-semibold text-slate-800 text-[11px] sm:text-xs focus:outline-none focus:border-slate-500">
          <option value="S98">S98 - คุณแป้ง (วัชรพล-สายไหม)</option>
          <option value="S120">S120 - คุณอ้อน (นนทบุรี-บางใหญ่)</option>
          <option value="S117">S117 - คุณแอ๊ด (บางนา-สมุทรปราการ)</option>
          <option value="S90">S90 - คุณนัท (ตลิ่งชัน)</option>
          <option value="S94">S94 - คุณหลิว (พุทธมณฑลสาย 2)</option>
          <option value="S113">S113 - คุณไห้ (ธนบุรี-ดาวคะนอง)</option>
        </select>
      </div>

      <div class="flex items-center justify-between pt-1 border-t border-slate-100">
        <span class="text-[10.5px] text-slate-400">มุมมองหน้าจอ:</span>
        <div class="inline-flex rounded-lg bg-slate-100 p-0.5 font-semibold text-[10.5px]">
          <button id="btnModeAgent" onclick="setMode('agent')" class="px-2 py-1 rounded-md bg-white shadow-xs text-slate-800">
            ตั้งค่าภายใน
          </button>
          <button id="btnModeClient" onclick="openPreviewModal()" class="px-2 py-1 rounded-md text-slate-600 hover:text-slate-900 flex items-center gap-1">
            <i data-lucide="eye" class="w-3 h-3"></i>
            <span>พรีวิวมุมมองลูกค้า</span>
          </button>
        </div>
      </div>
    </div>

    <!-- MAIN PROFILE CARD (Minimal, Clean, Pixel-Perfect Mobile Layout) -->
    <div class="bg-white border border-slate-200/90 rounded-[28px] sm:rounded-[36px] p-4 sm:p-6 shadow-sm space-y-4">

      <!-- Header & Brand -->
      <div class="flex items-center justify-between border-b border-slate-100 pb-3 gap-2">
        <div class="flex items-center gap-2 min-w-0">
          <img src="assets/siwasup_logo.png" alt="Siwasup Asset Logo" class="h-7 sm:h-8 w-auto shrink-0 object-contain" onerror="this.onerror=null; this.src='assets/siwasup_logo.svg';" />
          <div class="min-w-0">
            <h1 class="text-[11px] sm:text-xs font-bold text-slate-900 tracking-wider uppercase truncate">SIWASUP ASSET</h1>
            <p class="text-[9px] sm:text-[10px] text-slate-400 truncate">Co-Broker Partner Network</p>
          </div>
        </div>

        <!-- Official Golden Emblem Badge (From E:\TON\#Siwasub\images\Golden Emblem) -->
        <div id="tierBadge" class="inline-flex items-center gap-1.5 pl-1.5 pr-2.5 sm:pr-3 py-0.5 sm:py-1 rounded-full bg-[#E5B54F] border border-black shadow-xs shrink-0">
          <img id="tierEmblemImg" src="assets/badges/Golden__001_lion_web.png" alt="Golden Emblem" class="w-5 h-5 sm:w-6 sm:h-6 object-contain rounded-full shadow-2xs" onerror="this.onerror=null; this.src='assets/badges/Golden__001_lion.png';" />
          <span id="tierTitleText" class="text-[10px] sm:text-[11px] font-bold text-slate-950 tracking-tight whitespace-nowrap">Senior Property Advisor</span>
        </div>
      </div>

      <!-- Avatar & Name Section (Always Horizontal Side-by-Side as in Illustrator) -->
      <div class="flex items-start gap-3 sm:gap-4">
        <!-- Avatar Wrapper with 37px Rounded Corners -->
        <div class="relative shrink-0">
          <img id="agentAvatar" 
               src="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80" 
               alt="Agent Profile" 
               class="w-[86px] h-[86px] sm:w-24 sm:h-24 squircle-37 object-cover bg-slate-100 border border-slate-200/90 shadow-xs" />
          <!-- Small Verified Checkmark -->
          <span class="absolute -bottom-1 -right-1 w-5 h-5 rounded-full bg-emerald-500 border-2 border-white flex items-center justify-center text-[10px] text-white font-bold shadow-xs" title="ที่ปรึกษาที่ผ่านการรับรอง">✓</span>
        </div>

        <!-- Info (Right Side) -->
        <div class="space-y-1 flex-1 min-w-0">
          <div class="flex items-center gap-1.5 flex-wrap">
            <span id="agentCode" class="text-[10.5px] font-mono font-bold px-1.5 py-0.5 rounded bg-slate-100 text-slate-700">S98</span>
            <span id="zoneBadge" class="text-[11px] font-medium text-slate-500 truncate">📍 โซนวัชรพล-สายไหม</span>
          </div>
          <h2 id="agentName" class="text-base sm:text-lg font-bold text-slate-900 truncate">คุณนภชกร วรพัทธ์ภูดิท</h2>
          <p id="agentTitle" class="text-[10.5px] sm:text-xs text-slate-400 truncate">ที่ปรึกษาด้านการซื้อ-ขายอสังหาริมทรัพย์มืออาชีพ</p>

          <!-- Action Contact Pills (NO "โทร", Formatted 10-digit number with spacing) -->
          <div class="pt-1.5 flex flex-wrap items-center gap-1.5 sm:gap-2">
            <a id="btnCall" href="tel:0966458994" class="inline-flex items-center gap-1.5 text-[11px] sm:text-xs font-semibold px-3 py-1.5 rounded-full bg-slate-950 hover:bg-slate-800 text-white transition shadow-xs">
              <i data-lucide="phone" class="w-3 h-3 sm:w-3.5 sm:h-3.5 text-white"></i>
              <span id="txtPhone" class="font-mono tracking-tight font-bold">096 645 8994</span>
            </a>
            <a id="btnLine" href="https://line.me/ti/p/~" target="_blank" class="inline-flex items-center gap-1.5 text-[11px] sm:text-xs font-semibold px-3 py-1.5 rounded-full bg-white text-[#06C755] border border-[#06C755] hover:bg-emerald-50 transition shadow-xs">
              <i data-lucide="message-circle" class="w-3 h-3 sm:w-3.5 sm:h-3.5"></i>
              <span id="txtLine">LINE OA</span>
            </a>
          </div>
        </div>
      </div>

      <!-- SMART PREVIEW & 1-CLICK CONFIRM BANNER (Visible ONLY in Agent Mode) -->
      <div id="consentBox" class="bg-slate-50/80 border border-slate-200/80 rounded-2xl p-3 space-y-2.5">
        <div class="flex items-start gap-2">
          <div class="w-6 h-6 rounded-lg bg-emerald-50 text-emerald-600 border border-emerald-200 flex items-center justify-center shrink-0 mt-0.5">
            <i data-lucide="shield-check" class="w-3.5 h-3.5"></i>
          </div>
          <div class="space-y-0.5 text-xs">
            <div class="font-bold text-slate-900 text-[11.5px]">ระบบความปลอดภัยและ Golden Emblem ทางการ</div>
            <p class="text-slate-500 leading-relaxed text-[10.5px]">
              🔒 แสดงตรา Golden Emblem ประจำยศทางการ (เมื่อส่งให้ลูกค้า จะแสดงเฉพาะตำแหน่งทางการ <em>"Senior Property Advisor"</em> ไม่แสดงชื่อสัตว์)
            </p>
          </div>
        </div>

        <div class="flex items-center gap-2 pt-0.5">
          <button id="btnConfirmPhoto" onclick="confirmPhoto()" class="flex-1 py-1.5 px-3 rounded-xl bg-slate-900 hover:bg-slate-800 text-white text-[11px] font-semibold transition text-center shadow-xs">
            ✓ ยืนยันใช้รูปนี้
          </button>
          <label for="customPhotoInput" class="py-1.5 px-3 rounded-xl bg-white hover:bg-slate-100 text-slate-700 text-[11px] font-semibold border border-slate-300 transition text-center cursor-pointer">
            📷 เปลี่ยนรูปใหม่
          </label>
          <input type="file" id="customPhotoInput" accept="image/*" class="hidden" onchange="handleCustomPhoto(event)" />
        </div>
      </div>

      <!-- Confirmed Notice (Hidden by default in agent mode, never in client mode) -->
      <div id="confirmedAlert" class="hidden bg-emerald-50 border border-emerald-200 rounded-2xl p-2.5 text-[11px] text-emerald-800 flex items-center justify-between">
        <div class="flex items-center gap-2">
          <i data-lucide="check-circle" class="w-3.5 h-3.5 text-emerald-600"></i>
          <span class="font-medium">รูปโปรไฟล์ได้รับการยืนยันและพร้อมแชร์ให้ลูกค้าแล้ว</span>
        </div>
        <button onclick="resetConfirm()" class="text-[10px] text-slate-500 underline hover:text-slate-700">แก้ไข</button>
      </div>

      <!-- Quick Metrics Grid (4 คอลัมน์ ออกแบบให้คมชัด ไม่เบียดบนจอมือถือ) -->
      <div id="metricsContainer" class="pt-1">
        <div id="metricsGrid" class="grid grid-cols-4 gap-1.5 sm:gap-2 text-center">
          <!-- Dynamic JS Render -->
        </div>
      </div>

      <!-- Action Buttons for Client Sharing -->
      <div class="space-y-2 pt-2 border-t border-slate-100">
        <!-- Button 1: Preview & Share (Agent Mode) -->
        <button id="btnShareToClient" onclick="openPreviewModal()" class="w-full py-2.5 sm:py-3 rounded-2xl bg-slate-900 hover:bg-slate-800 text-white font-semibold text-xs flex items-center justify-center gap-2 transition shadow-xs active:scale-95">
          <i data-lucide="eye" class="w-4 h-4 text-amber-400"></i>
          <span>ดูพรีวิวมุมมองลูกค้าก่อนแชร์ & รับลิงก์</span>
        </button>

        <!-- Button 2: Direct call for client (Client Mode) -->
        <a id="btnClientCall" href="tel:0966458994" class="hidden w-full py-2.5 sm:py-3 rounded-2xl bg-slate-900 hover:bg-slate-800 text-white font-semibold text-xs flex items-center justify-center gap-2 transition shadow-xs active:scale-95">
          <i data-lucide="phone-call" class="w-4 h-4 text-emerald-400"></i>
          <span id="btnClientCallText">ติดต่อ 096 645 8994</span>
        </a>

        <!-- Button 3: Browse Catalog -->
        <a id="btnBrowseCatalog" href="https://assets.siwasup.com/catalog.html" target="_blank" class="w-full py-2 sm:py-2.5 rounded-2xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs flex items-center justify-center gap-2 transition border border-slate-200">
          <i data-lucide="home" class="w-3.5 h-3.5"></i>
          <span>เลือกดูรายการบ้านพร้อมขายในทำเลนี้</span>
        </a>
      </div>

    </div>

    <!-- ============================================================ -->
    <!-- EXECUTIVE METRIC SWITCHER (สำหรับกูล & ผู้บริหารพิจารณา 3 ตัวเลือก) -->
    <!-- ============================================================ -->
    <div id="executiveSelectorBox" class="bg-white border border-slate-200 rounded-3xl p-4 sm:p-5 shadow-xs space-y-3 text-xs">
      <div class="flex items-center justify-between border-b border-slate-100 pb-2">
        <div class="flex items-center gap-2">
          <span class="w-6 h-6 rounded-lg bg-amber-100 text-amber-700 flex items-center justify-center font-bold">
            <i data-lucide="sliders" class="w-3.5 h-3.5"></i>
          </span>
          <span class="font-bold text-slate-900 text-xs sm:text-sm">ทดลองสลับ 3 ตัวเลือก (ให้ CEO กูลเลือก)</span>
        </div>
        <span id="currentOptionBadge" class="text-[9.5px] sm:text-[10px] font-bold px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-800">
          แบบที่ 1 (แนะนำ)
        </span>
      </div>

      <!-- Tab Buttons -->
      <div class="grid grid-cols-3 gap-1 p-1 bg-slate-100 rounded-xl text-[10.5px] sm:text-[11px] font-semibold">
        <button id="tabOpt1" onclick="selectMetricOption('opt1')" class="py-1.5 px-1 rounded-lg bg-white text-slate-900 shadow-xs transition text-center font-bold truncate">
          แบบ 1: สบายใจ/ฟรี
        </button>
        <button id="tabOpt2" onclick="selectMetricOption('opt2')" class="py-1.5 px-1 rounded-lg text-slate-600 hover:text-slate-900 transition text-center font-medium truncate">
          แบบ 2: โปร/ปิดสำเร็จ
        </button>
        <button id="tabOpt3" onclick="selectMetricOption('opt3')" class="py-1.5 px-1 rounded-lg text-slate-600 hover:text-slate-900 transition text-center font-medium truncate">
          แบบ 3: ปรับคำซอฟต์
        </button>
      </div>

      <!-- Real-time Explanation of Selected Option -->
      <div id="optionExplainBox" class="p-3 rounded-2xl bg-slate-50 border border-slate-200/80 space-y-1">
        <div class="flex items-center justify-between">
          <span id="explainTitle" class="font-bold text-slate-900 text-[11px]">🌟 แบบที่ 1: "สลายกังวล & ช่วยดันสินเชื่อ"</span>
          <span id="explainTag" class="text-[9.5px] font-semibold text-emerald-700 bg-emerald-50 px-1.5 py-0.5 rounded border border-emerald-200">
            Conversion สูงสุด
          </span>
        </div>
        <p id="explainDesc" class="text-slate-600 text-[10.5px] leading-relaxed">
          คนซื้อบ้านกลัว 2 เรื่อง: 1. กลัวโดนเก็บค่านายหน้า 2. กลัวยื่นกู้ไม่ผ่าน เมื่อใส่ <strong>พานำชม ฟรี + ปิดสำเร็จ 45+ หลัง + ดันสินเชื่อผ่าน 98%</strong> ลูกค้าจะกล้ากดแอด LINE ทันที และตัดเรตติ้งดาวออกเพื่อกันการแกล้งรีวิว 100%
        </p>
      </div>

      <!-- Executive Decision Matrix: Compare All 3 Side-by-Side -->
      <div class="space-y-2 pt-1 border-t border-slate-100">
        <div class="font-bold text-slate-800 text-[11px] flex items-center justify-between">
          <span>ตารางสรุปเปรียบเทียบ 3 ตัวเลือก:</span>
          <span class="text-[9.5px] text-slate-400 font-normal">คลิกเพื่อดูผลบนการ์ด</span>
        </div>
        
        <!-- Card 1 -->
        <div onclick="selectMetricOption('opt1')" class="p-2.5 sm:p-3 rounded-xl border border-emerald-200 bg-emerald-50/50 hover:bg-emerald-50 cursor-pointer transition space-y-1">
          <div class="flex items-center justify-between">
            <span class="font-bold text-emerald-900 text-[11px]">1. สลายกังวล & สินเชื่อ (แนะนำที่สุด 🏆)</span>
            <span class="text-[10px] font-semibold text-emerald-700">คลิกดู</span>
          </div>
          <div class="grid grid-cols-4 gap-1 text-center bg-white rounded-lg p-1.5 border border-emerald-100 text-[10px]">
            <div><span class="text-slate-400 block text-[8.5px]">ทรัพย์ในพื้นที่</span><strong class="text-slate-900 text-xs">850+</strong></div>
            <div><span class="text-slate-400 block text-[8.5px]">พานำชม</span><strong class="text-emerald-600 text-xs">ฟรี</strong></div>
            <div><span class="text-slate-400 block text-[8.5px]">ปิดสำเร็จ</span><strong class="text-emerald-600 text-xs">45+</strong></div>
            <div><span class="text-slate-400 block text-[8.5px]">ดันสินเชื่อผ่าน</span><strong class="text-slate-900 text-xs">98%</strong></div>
          </div>
        </div>

        <!-- Card 2 -->
        <div onclick="selectMetricOption('opt2')" class="p-2.5 sm:p-3 rounded-xl border border-slate-200 bg-slate-50 hover:bg-slate-100/80 cursor-pointer transition space-y-1">
          <div class="flex items-center justify-between">
            <span class="font-bold text-slate-900 text-[11px]">2. สายโปร ปิดไว โชว์พลัง (Track Record)</span>
            <span class="text-[10px] font-semibold text-slate-500">คลิกดู</span>
          </div>
          <div class="grid grid-cols-4 gap-1 text-center bg-white rounded-lg p-1.5 border border-slate-200 text-[10px]">
            <div><span class="text-slate-400 block text-[8.5px]">ทรัพย์ในพื้นที่</span><strong class="text-slate-900 text-xs">850+</strong></div>
            <div><span class="text-slate-400 block text-[8.5px]">พาชมจริง</span><strong class="text-emerald-600 text-xs">120+</strong></div>
            <div><span class="text-slate-400 block text-[8.5px]">ปิดสำเร็จ</span><strong class="text-slate-900 text-xs">45+</strong></div>
            <div><span class="text-slate-400 block text-[8.5px]">ตอบกลับเฉลี่ย</span><strong class="text-slate-900 text-xs">15 นาที</strong></div>
          </div>
        </div>

        <!-- Card 3 -->
        <div onclick="selectMetricOption('opt3')" class="p-2.5 sm:p-3 rounded-xl border border-slate-200 bg-slate-50 hover:bg-slate-100/80 cursor-pointer transition space-y-1">
          <div class="flex items-center justify-between">
            <span class="font-bold text-slate-900 text-[11px]">3. ปรับคำซอฟต์ (ตามร่างคุณต้น)</span>
            <span class="text-[10px] font-semibold text-slate-500">คลิกดู</span>
          </div>
          <div class="grid grid-cols-4 gap-1 text-center bg-white rounded-lg p-1.5 border border-slate-200 text-[10px]">
            <div><span class="text-slate-400 block text-[8.5px]">ทรัพย์ในโซน</span><strong class="text-slate-900 text-xs">850+</strong></div>
            <div><span class="text-slate-400 block text-[8.5px]">บ้านราคาพิเศษ</span><strong class="text-emerald-600 text-xs">10</strong></div>
            <div><span class="text-slate-400 block text-[8.5px]">นัดชมได้ทันที</span><strong class="text-slate-900 text-xs">3</strong></div>
            <div><span class="text-slate-400 block text-[8.5px]">ดูแลใกล้ชิด</span><strong class="text-slate-900 text-xs">50</strong></div>
          </div>
        </div>

      </div>

      <!-- Security / Anti-Trolling Note -->
      <div class="bg-amber-50 border border-amber-200 rounded-xl p-2.5 text-[10.5px] text-amber-900 flex items-start gap-2">
        <i data-lucide="alert-triangle" class="w-3.5 h-3.5 text-amber-600 shrink-0 mt-0.5"></i>
        <span><strong>ข้อสังเกตจากคุณต้น:</strong> ใช้ Golden Emblem จากโฟลเดอร์ <code>Golden__001_Folder</code> ตัดคำว่า "โทร" ออก, และปรับขอบรูปมน 37px ตาม Illustrator</span>
      </div>

    </div>

    <!-- Simple Toast Notification -->
    <div id="toast" class="fixed bottom-6 left-1/2 -translate-x-1/2 bg-slate-900 text-white text-xs px-4 py-2.5 rounded-xl shadow-lg transition-all opacity-0 pointer-events-none duration-300 z-50">
      คัดลอกลิงก์เรียบร้อยแล้ว
    </div>

  </div>

  <!-- ============================================================ -->
  <!-- PREVIEW MODAL BEFORE SHARING (มุมมองเสมือนจริงที่ลูกค้าจะเห็น) -->
  <!-- ============================================================ -->
  <div id="previewModal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-xs flex items-center justify-center p-3">
    <div class="bg-white border border-slate-200 rounded-[28px] max-w-sm w-full p-4 sm:p-5 shadow-2xl space-y-3.5 max-h-[92vh] overflow-y-auto">
      
      <!-- Modal Header -->
      <div class="flex items-center justify-between border-b border-slate-100 pb-2.5">
        <div class="flex items-center gap-2">
          <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span class="text-xs font-bold text-slate-900">ตัวอย่างที่ลูกค้าจะเห็นจริง</span>
        </div>
        <button onclick="closePreviewModal()" class="w-7 h-7 rounded-full bg-slate-100 text-slate-500 hover:bg-slate-200 flex items-center justify-center text-sm font-bold">
          ✕
        </button>
      </div>

      <!-- Security Notice -->
      <div class="bg-emerald-50 border border-emerald-200 rounded-xl p-2 text-[10.5px] text-emerald-800 flex items-center gap-2">
        <i data-lucide="shield-check" class="w-4 h-4 text-emerald-600 shrink-0"></i>
        <span>ปลอดภัย 100%: ไม่มีชื่อหรือรูปสัตว์ ลูกค้าเห็นเฉพาะป้ายทองคำทางการ</span>
      </div>

      <!-- Mini Mockup of Client Card (Clean & Responsive) -->
      <div class="border border-slate-200 rounded-2xl p-3 bg-slate-50/50 space-y-3">
        <!-- Mini Header -->
        <div class="flex items-center justify-between">
          <div class="flex items-center gap-1.5">
            <img src="assets/siwasup_logo.png" alt="Siwasup Logo" class="h-4 sm:h-5 w-auto object-contain" onerror="this.onerror=null; this.src='assets/siwasup_logo.svg';" />
            <span class="text-[9.5px] font-bold text-slate-800 tracking-wider uppercase">SIWASUP ASSET</span>
          </div>
          <!-- Clean Prestige Gold Pill (No Animal) -->
          <div class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-[#E5B54F] border border-black text-[9px] font-bold text-slate-950 shadow-2xs">
            <span class="text-slate-950">✦</span>
            <span id="modalTierTitle">Senior Property Advisor</span>
          </div>
        </div>

        <!-- Mini Info (Horizontal) -->
        <div class="flex items-center gap-2.5">
          <img id="modalAvatar" src="" class="w-14 h-14 rounded-[24px] object-cover border border-slate-200 bg-white shrink-0" />
          <div class="space-y-0.5 min-w-0 flex-1">
            <div id="modalAgentName" class="text-xs sm:text-sm font-bold text-slate-900 truncate">คุณนภชกร วรพัทธ์ภูดิท</div>
            <div id="modalZone" class="text-[9.5px] text-slate-500 truncate">📍 โซนวัชรพล-สายไหม</div>
            <div id="modalPhone" class="text-[10.5px] font-mono font-bold text-slate-800">096 645 8994</div>
          </div>
        </div>

        <!-- Mini Metrics in Modal -->
        <div id="modalMetricsGrid" class="grid grid-cols-4 gap-1 text-center bg-white rounded-xl p-1.5 border border-slate-200">
          <!-- Dynamic -->
        </div>

        <!-- Mini Actions -->
        <div class="grid grid-cols-2 gap-1.5 text-center text-[10px] font-semibold">
          <div id="modalCallBtn" class="p-1.5 rounded-xl bg-slate-950 text-white font-mono">096 645 8994</div>
          <div class="p-1.5 rounded-xl bg-white text-[#06C755] border border-[#06C755]">💬 LINE OA</div>
        </div>
      </div>

      <!-- Share Action Buttons -->
      <div class="space-y-2 pt-0.5">
        <button onclick="copyClientLinkFromModal()" class="w-full py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs flex items-center justify-center gap-2 transition shadow-md active:scale-95">
          <i data-lucide="copy" class="w-3.5 h-3.5 text-amber-400"></i>
          <span>คัดลอกลิงก์นามบัตร (ส่งให้ลูกค้า)</span>
        </button>

        <a id="btnShareLineDirect" href="#" target="_blank" class="w-full py-2 rounded-xl bg-[#06C755] hover:bg-[#05b34c] text-white font-bold text-xs flex items-center justify-center gap-2 transition shadow-2xs text-center">
          <i data-lucide="send" class="w-3.5 h-3.5"></i>
          <span>ส่งแชร์เข้า LINE ลูกค้าทันที</span>
        </a>
      </div>

    </div>
  </div>

  <script>
    // 6 Alpha Agents Data with Golden Emblems from Golden__001_Folder
    const AGENTS = {
      S98: {
        code: "S98",
        name: "คุณนภชกร วรพัทธ์ภูดิท",
        nickname: "คุณแป้ง",
        phoneRaw: "0966458994",
        phoneFormatted: "096 645 8994",
        lineId: "",
        zone: "📍 โซนวัชรพล-สายไหม",
        clientTitle: "Senior Property Advisor",
        goldBadge: "assets/badges/Golden__001_lion_web.png",
        avatar: "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80"
      },
      S120: {
        code: "S120",
        name: "คุณสุทัย ปานทอง",
        nickname: "คุณอ้อน",
        phoneRaw: "0614428555",
        phoneFormatted: "061 442 8555",
        lineId: "Jaidee0902",
        zone: "📍 โซนนนทบุรี-บางใหญ่",
        clientTitle: "Senior Property Consultant",
        goldBadge: "assets/badges/Golden__001_eagle_web.png",
        avatar: "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=300&auto=format&fit=crop&q=80"
      },
      S117: {
        code: "S117",
        name: "คุณพรทิพย์ นวนกะสัง",
        nickname: "คุณแอ๊ด",
        phoneRaw: "0869925627",
        phoneFormatted: "086 992 5627",
        lineId: "086-9925627",
        zone: "📍 โซนบางนา-สมุทรปราการ",
        clientTitle: "Senior Property Advisor",
        goldBadge: "assets/badges/Golden__001_lion_web.png",
        avatar: "https://images.unsplash.com/photo-1567532939604-b6b5b0db2604?w=300&auto=format&fit=crop&q=80"
      },
      S90: {
        code: "S90",
        name: "คุณอนัญญา สาธทอง",
        nickname: "คุณนัท",
        phoneRaw: "0930615356",
        phoneFormatted: "093 061 5356",
        lineId: "Run4536",
        zone: "📍 โซนตลิ่งชัน-ฝั่งธน",
        clientTitle: "Verified Property Specialist",
        goldBadge: "assets/badges/Golden__001_wolf_web.png",
        avatar: "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=300&auto=format&fit=crop&q=80"
      },
      S94: {
        code: "S94",
        name: "คุณพัณณ์นิกา เอื้อประโยชน์กิจ",
        nickname: "คุณหลิว",
        phoneRaw: "0870999297",
        phoneFormatted: "087 099 9297",
        lineId: "liew2557",
        zone: "📍 โซนพุทธมณฑลสาย 2-ทวีวัฒนา",
        clientTitle: "Verified Property Specialist",
        goldBadge: "assets/badges/Golden__001_wolf_web.png",
        avatar: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=300&auto=format&fit=crop&q=80"
      },
      S113: {
        code: "S113",
        name: "คุณสิทธิชัย มกุลพานิช",
        nickname: "คุณไห้",
        phoneRaw: "0957823593",
        phoneFormatted: "095 782 3593",
        lineId: "",
        zone: "📍 โซนดาวคะนอง-ธนบุรี",
        clientTitle: "Verified Property Specialist",
        goldBadge: "assets/badges/Golden__001_wolf_web.png",
        avatar: "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=300&auto=format&fit=crop&q=80"
      }
    };

    // 3 Refined Metric Options
    const METRIC_OPTIONS = {
      opt1: {
        id: "opt1",
        name: "แบบที่ 1: สบายใจ สลายความกังวล",
        badge: "แนะนำที่สุด 🏆",
        tag: "Conversion สูงสุด",
        desc: "คนซื้อบ้านกลัว 2 เรื่อง: 1. กลัวโดนเก็บค่านายหน้า 2. กลัวยื่นกู้ไม่ผ่าน เมื่อใส่ <strong>พานำชม ฟรี + ปิดสำเร็จ 45+ หลัง + ดันสินเชื่อผ่าน 98%</strong> ลูกค้าจะกล้ากดแอด LINE ทันที และตัดเรตติ้งดาวออกเพื่อกันการแกล้งรีวิว 100%",
        metrics: [
          { label: "ทรัพย์ในพื้นที่", value: "850+", isHighlight: false },
          { label: "พานำชม", value: "ฟรี", isHighlight: true },
          { label: "ปิดสำเร็จ", value: "45+", isHighlight: true },
          { label: "ดันสินเชื่อผ่าน", value: "98%", isHighlight: false }
        ]
      },
      opt2: {
        id: "opt2",
        name: "แบบที่ 2: สายโปร ปิดไว โชว์พลัง (Track Record)",
        badge: "Trust & Speed",
        tag: "โชว์สถิติงานจริง",
        desc: "เน้นโชว์ว่าตัวแทนทำงานจริง พาชมมาแล้ว 120+ เคส ปิดการขายสำเร็จ 45+ หลัง และตอบกลับรวดเร็วภายใน 15 นาที เหมาะกับกลุ่ม Alpha ที่มีงานสม่ำเสมอ",
        metrics: [
          { label: "ทรัพย์ในพื้นที่", value: "850+", isHighlight: false },
          { label: "พาชมจริง", value: "120+", isHighlight: true },
          { label: "ปิดสำเร็จ", value: "45+", isHighlight: false },
          { label: "ตอบกลับเฉลี่ย", value: "15 นาที", isHighlight: false }
        ]
      },
      opt3: {
        id: "opt3",
        name: "แบบที่ 3: ปรับคำซอฟต์ (ตามร่างคุณต้น)",
        badge: "Friendly Jargon",
        tag: "ดัดแปลงจากร่างเดิม",
        desc: "นำตัวเลขจริงในมือคุณต้น (สัญญาปิด 10, เปิดบ้าน 3, ดูแล 50) มาเปลี่ยนคำให้เป็นศัพท์ที่ผู้ซื้อบ้านเข้าใจง่าย และรู้สึกได้สิทธิ์พิเศษ Exclusive",
        metrics: [
          { label: "ทรัพย์ในโซน", value: "850+", isHighlight: false },
          { label: "บ้านราคาพิเศษ", value: "10", isHighlight: true },
          { label: "นัดชมได้ทันที", value: "3", isHighlight: false },
          { label: "ดูแลใกล้ชิด", value: "50", isHighlight: false }
        ]
      }
    };

    let currentAgent = "S98";
    let currentMode = "agent"; // 'agent' or 'client'
    let currentMetricOpt = "opt1";

    function getParam(param) {
      const urlParams = new URLSearchParams(window.location.search);
      return urlParams.get(param);
    }

    function init() {
      const code = (getParam("code") || "S98").toUpperCase();
      const mode = (getParam("mode") || "").toLowerCase();
      const metric = (getParam("metric") || "opt1").toLowerCase();

      changeAgent(code);
      if (METRIC_OPTIONS[metric]) {
        selectMetricOption(metric);
      } else {
        selectMetricOption("opt1");
      }

      if (mode === "client") {
        setMode("client");
      } else {
        setMode("agent");
      }

      if (window.lucide) lucide.createIcons();
    }

    function changeAgent(code) {
      const a = AGENTS[code] || AGENTS["S98"];
      currentAgent = a.code;

      document.getElementById("agentSelect").value = a.code;
      document.getElementById("agentCode").innerText = a.code;
      document.getElementById("agentName").innerText = a.name;
      document.getElementById("zoneBadge").innerText = a.zone;
      document.getElementById("tierTitleText").innerText = a.clientTitle;
      
      const emblemEl = document.getElementById("tierEmblemImg");
      if (emblemEl) emblemEl.src = a.goldBadge;

      const avatarEl = document.getElementById("agentAvatar");
      avatarEl.src = a.avatar;

      document.getElementById("btnCall").href = `tel:${a.phoneRaw}`;
      document.getElementById("txtPhone").innerText = a.phoneFormatted;
      document.getElementById("btnClientCall").href = `tel:${a.phoneRaw}`;
      document.getElementById("btnClientCallText").innerText = `ติดต่อ ${a.phoneFormatted}`;

      const btnLine = document.getElementById("btnLine");
      if (a.lineId) {
        btnLine.href = `https://line.me/ti/p/~${a.lineId}`;
      } else {
        btnLine.href = `https://line.me/R/ti/p/@813nyyia`;
      }
      document.getElementById("txtLine").innerText = `LINE OA`;

      document.getElementById("btnBrowseCatalog").href = `https://assets.siwasup.com/catalog.html?agent=${a.code}`;

      resetConfirm();
    }

    function selectMetricOption(optKey) {
      if (!METRIC_OPTIONS[optKey]) return;
      currentMetricOpt = optKey;
      const opt = METRIC_OPTIONS[optKey];

      // Update Tabs styling
      ['opt1', 'opt2', 'opt3'].forEach(k => {
        const tab = document.getElementById(`tab${k.charAt(0).toUpperCase() + k.slice(1)}`);
        if (tab) {
          if (k === optKey) {
            tab.className = "py-1.5 px-1 rounded-lg bg-white text-slate-900 shadow-xs transition text-center font-bold truncate";
          } else {
            tab.className = "py-1.5 px-1 rounded-lg text-slate-600 hover:text-slate-900 transition text-center font-medium truncate";
          }
        }
      });

      // Update Explanation text
      document.getElementById("currentOptionBadge").innerText = opt.name.split(":")[0];
      document.getElementById("explainTitle").innerHTML = opt.name;
      document.getElementById("explainTag").innerText = opt.tag;
      document.getElementById("explainDesc").innerHTML = opt.desc;

      // Render 4 metrics on card
      renderMetrics(opt.metrics);
    }

    function renderMetrics(metrics) {
      const container = document.getElementById("metricsGrid");
      const modalContainer = document.getElementById("modalMetricsGrid");

      let html = "";
      metrics.forEach(m => {
        const valColor = m.isHighlight ? "text-emerald-600" : "text-slate-900";
        html += `
          <div class="p-1.5 sm:p-2 rounded-2xl bg-slate-50/80 border border-slate-100 flex flex-col justify-center min-w-0">
            <span class="text-[9px] sm:text-[10px] text-slate-400 font-medium leading-tight truncate px-0.5">${m.label}</span>
            <span class="text-sm sm:text-base font-extrabold ${valColor} mt-0.5 truncate">${m.value}</span>
          </div>
        `;
      });
      container.innerHTML = html;

      let modalHtml = "";
      metrics.forEach(m => {
        const valColor = m.isHighlight ? "text-emerald-600" : "text-slate-900";
        modalHtml += `
          <div>
            <span class="text-[8.5px] text-slate-400 block leading-tight truncate">${m.label}</span>
            <strong class="text-[11px] font-extrabold ${valColor}">${m.value}</strong>
          </div>
        `;
      });
      modalContainer.innerHTML = modalHtml;
    }

    function setMode(mode) {
      currentMode = mode;
      const ctrlBar = document.getElementById("internalControlBar");
      const consentBox = document.getElementById("consentBox");
      const confirmedAlert = document.getElementById("confirmedAlert");
      const btnShare = document.getElementById("btnShareToClient");
      const btnClientCall = document.getElementById("btnClientCall");
      const execBox = document.getElementById("executiveSelectorBox");
      const tierEmblemImg = document.getElementById("tierEmblemImg");

      if (mode === "client") {
        // CLIENT VIEW: Hide internal tools, hide consent box, show client call button
        if (ctrlBar) ctrlBar.classList.add("hidden");
        if (execBox) execBox.classList.add("hidden");
        consentBox.classList.add("hidden");
        confirmedAlert.classList.add("hidden");
        btnShare.classList.add("hidden");
        btnClientCall.classList.remove("hidden");

        // Hide animal emblem on client view
        if (tierEmblemImg) tierEmblemImg.classList.add("hidden");
      } else {
        // AGENT VIEW: Show consent box, show share button, hide client call
        if (ctrlBar) ctrlBar.classList.remove("hidden");
        if (execBox) execBox.classList.remove("hidden");
        consentBox.classList.remove("hidden");
        btnShare.classList.remove("hidden");
        btnClientCall.classList.add("hidden");

        // Show Golden Emblem for agent view
        if (tierEmblemImg) tierEmblemImg.classList.remove("hidden");
      }
    }

    function confirmPhoto() {
      document.getElementById("consentBox").classList.add("hidden");
      document.getElementById("confirmedAlert").classList.remove("hidden");
      showToast("✓ ยืนยันใช้รูปโปรไฟล์เรียบร้อยแล้ว");
    }

    function resetConfirm() {
      if (currentMode === "agent") {
        document.getElementById("consentBox").classList.remove("hidden");
        document.getElementById("confirmedAlert").classList.add("hidden");
      }
    }

    function handleCustomPhoto(e) {
      const file = e.target.files[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = function(evt) {
          document.getElementById("agentAvatar").src = evt.target.result;
          confirmPhoto();
          showToast("อัปโหลดรูปใหม่สำเร็จแล้ว");
        };
        reader.readAsDataURL(file);
      }
    }

    // Modal Preview Logic (Client Perspective)
    function openPreviewModal() {
      const a = AGENTS[currentAgent];
      document.getElementById("modalAvatar").src = document.getElementById("agentAvatar").src;
      document.getElementById("modalTierTitle").innerText = a.clientTitle;
      document.getElementById("modalAgentName").innerText = a.name;
      document.getElementById("modalZone").innerText = a.zone;
      document.getElementById("modalPhone").innerText = a.phoneFormatted;
      document.getElementById("modalCallBtn").innerText = a.phoneFormatted;

      const clientUrl = getClientUrl();
      const lineShareText = encodeURIComponent(`สวัสดีครับ/ค่ะ ขอแนะนำนามบัตรที่ปรึกษาอสังหาริมทรัพย์ ศิวาทรัพย์ แอสเซท (${a.name})\\nเปิดดูข้อมูลและรายการบ้านพร้อมขายได้ที่: ${clientUrl}`);
      document.getElementById("btnShareLineDirect").href = `https://line.me/R/msg/text/?${lineShareText}`;

      document.getElementById("previewModal").classList.remove("hidden");
      if (window.lucide) lucide.createIcons();
    }

    function closePreviewModal() {
      document.getElementById("previewModal").classList.add("hidden");
    }

    function getClientUrl() {
      const baseUrl = window.location.origin + window.location.pathname;
      return `${baseUrl}?code=${currentAgent}&mode=client&metric=${currentMetricOpt}`;
    }

    function copyClientLinkFromModal() {
      const clientUrl = getClientUrl();
      if (navigator.clipboard) {
        navigator.clipboard.writeText(clientUrl).then(() => {
          showToast("คัดลอกลิงก์นามบัตรสำหรับส่งให้ลูกค้าแล้ว");
          closePreviewModal();
        });
      } else {
        prompt("ลิงก์สำหรับส่งให้ลูกค้า:", clientUrl);
      }
    }

    function showToast(msg) {
      const t = document.getElementById("toast");
      t.innerText = msg;
      t.classList.remove("opacity-0", "pointer-events-none");
      setTimeout(() => {
        t.classList.add("opacity-0", "pointer-events-none");
      }, 2500);
    }

    window.addEventListener("DOMContentLoaded", init);
  </script>
</body>
</html>'''

TARGET_PATH = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\agent_profile.html"
with open(TARGET_PATH, "w", encoding="utf-8") as f:
    f.write(HTML_CONTENT)

print(f"Successfully generated agent_profile.html with Golden Emblems ({len(HTML_CONTENT):,} bytes)")
