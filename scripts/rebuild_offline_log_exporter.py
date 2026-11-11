import os
import json

HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Siwasup OS - เครื่องมือดูดและวิเคราะห์ Chat Log ออฟไลน์ (Offline Log Exporter)</title>
  <link rel="icon" type="image/png" href="assets/siwasup_logo.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  <style>
    body {
      font-family: 'Prompt', sans-serif;
      background: #090D16;
      color: #F8FAFC;
    }
    .gold-gradient {
      background: linear-gradient(135deg, #F59E0B 0%, #D97706 100%);
    }
    .card-glass {
      background: rgba(17, 24, 39, 0.75);
      backdrop-filter: blur(12px);
      border: 1px solid rgba(245, 158, 11, 0.2);
    }
    /* ใช้ฟอนต์มีหัว (Tahoma) เฉพาะในตารางข้อมูลเพื่อให้อ่านข้อความยาวๆ ได้สบายตา ไม่สับสน ตามกฎ Learned Rule */
    #tablePanel table, #tablePanel th, #tablePanel td {
      font-family: 'Tahoma', 'Segoe UI', sans-serif !important;
      line-height: 1.6;
    }
  </style>
</head>
<body class="min-h-screen p-4 sm:p-8">

  <div class="max-w-6xl mx-auto space-y-6">

    <!-- Header Bar -->
    <div class="card-glass rounded-3xl p-5 sm:p-6 shadow-2xl flex flex-col md:flex-row items-center justify-between gap-4 border border-amber-500/30">
      <div class="flex items-center gap-3.5">
        <div class="w-12 h-12 rounded-2xl bg-amber-500/10 border border-amber-500/30 flex items-center justify-center text-amber-400 shrink-0 shadow-inner">
          <i data-lucide="shield-check" class="w-6 h-6"></i>
        </div>
        <div>
          <div class="flex items-center gap-2 flex-wrap">
            <h1 class="text-lg sm:text-xl font-bold tracking-tight text-white">เครื่องมือดูดและวิเคราะห์ Chat Log ออฟไลน์</h1>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/30">
              PDPA Shield 100%
            </span>
            <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-500/10 text-amber-300 border border-amber-500/30">
              v2.5 High-Speed
            </span>
          </div>
          <p class="text-xs text-slate-400 mt-0.5">ดูดข้อมูลจากบอทน้องศิวาลงเครื่องส่วนตัวได้ทันที รองรับทั้ง Render Cloud, Cloudflare R2 สำรอง, และ Localhost</p>
        </div>
      </div>

      <!-- Quick Server Selector (3 Presets) -->
      <div class="flex items-center gap-1.5 bg-slate-900/90 p-1.5 rounded-2xl border border-slate-800 text-xs w-full md:w-auto flex-wrap">
        <button id="btnCloud" onclick="setServerPreset('cloud')" class="px-3 py-1.5 rounded-xl bg-amber-500 text-slate-950 font-bold transition shadow-sm cursor-pointer">
          ☁️ Render Cloud (Live 24 ชม.)
        </button>
        <button id="btnR2" onclick="setServerPreset('r2')" class="px-3 py-1.5 rounded-xl text-slate-300 hover:text-white transition cursor-pointer">
          ⚡ Cloudflare R2 (สำรองเสี้ยววิ)
        </button>
        <button id="btnLocal" onclick="setServerPreset('local')" class="px-3 py-1.5 rounded-xl text-slate-300 hover:text-white transition cursor-pointer">
          💻 Local:5005
        </button>
      </div>
    </div>

    <!-- Configuration & Filter Panel -->
    <div class="card-glass rounded-3xl p-5 sm:p-6 space-y-4">
      <div class="flex items-center justify-between flex-wrap gap-2">
        <h2 class="text-xs font-bold uppercase tracking-wider text-amber-400 flex items-center gap-2">
          <i data-lucide="sliders" class="w-4 h-4"></i>
          1. ตั้งค่าเป้าหมายและเงื่อนไขการดูดข้อมูล (Filter Criteria)
        </h2>
        <span id="connectionBadge" class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-[11px] bg-slate-800 border border-slate-700 text-slate-300">
          <span id="connectionDot" class="w-2 h-2 rounded-full bg-emerald-400"></span>
          <span id="connectionBadgeText">พร้อมทำงาน (แคชในเครื่อง)</span>
        </span>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-12 gap-3 sm:gap-4">
        <!-- Server Endpoint Input -->
        <div class="md:col-span-7 space-y-1">
          <label class="text-[11px] font-medium text-slate-300 flex items-center justify-between">
            <span>Server Endpoint URL</span>
            <span class="text-[10px] text-slate-500 font-mono">API หรือ JSON URL</span>
          </label>
          <input type="text" id="serverUrl" value="https://siwasup-cobroker-os.onrender.com" placeholder="https://siwasup-cobroker-os.onrender.com หรือ https://assets.siwasup.com/data/line_chat_logs.json" 
            class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700 text-white text-xs font-mono focus:border-amber-500 focus:outline-hidden transition" />
        </div>

        <!-- Secret Key -->
        <div class="md:col-span-5 space-y-1">
          <label class="text-[11px] font-medium text-slate-300">Admin Secret Key (กุญแจลับเฉพาะผู้บริหาร)</label>
          <input type="password" id="secretKey" value="" 
            class="w-full px-3.5 py-2.5 rounded-xl bg-slate-900/90 border border-slate-700 text-white text-xs font-mono focus:border-amber-500 focus:outline-hidden transition" />
        </div>
      </div>

      <!-- Filters: Time & Category -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-3 pt-2 border-t border-slate-800 text-xs">
        <!-- Days Filter -->
        <div class="space-y-1.5">
          <label class="text-[11px] font-medium text-slate-400">ช่วงเวลาย้อนหลัง</label>
          <div class="grid grid-cols-3 gap-1.5">
            <button onclick="setDays('7', this)" class="btn-days py-2 rounded-xl bg-slate-800 hover:bg-slate-700 font-medium transition cursor-pointer">7 วัน</button>
            <button onclick="setDays('30', this)" class="btn-days py-2 rounded-xl bg-slate-800 hover:bg-slate-700 font-medium transition cursor-pointer">30 วัน</button>
            <button onclick="setDays('all', this)" class="btn-days py-2 rounded-xl bg-amber-500 text-slate-950 font-bold active-day transition shadow-xs cursor-pointer">ทั้งหมด</button>
          </div>
        </div>

        <!-- Category Filter -->
        <div class="space-y-1.5">
          <label class="text-[11px] font-medium text-slate-400">หมวดหมู่บทสนทนา</label>
          <select id="categoryFilter" onchange="applyClientFilters()" class="w-full py-2 px-3 rounded-xl bg-slate-900 border border-slate-700 text-white font-medium focus:border-amber-500 focus:outline-hidden cursor-pointer">
            <option value="all">ทั้งหมด ทุกข้อความ</option>
            <option value="property">🏠 เฉพาะสอบถามค้นหาบ้าน/คอนโด</option>
            <option value="workflow">🔑 เฉพาะสอบถามเปิดบ้าน & รับกุญแจ</option>
          </select>
        </div>

        <!-- PDPA Privacy Shield Option -->
        <div class="space-y-1.5 flex flex-col justify-end">
          <label class="inline-flex items-center gap-2 cursor-pointer bg-slate-900/60 p-2.5 rounded-xl border border-slate-800 hover:border-amber-500/40 transition select-none">
            <input type="checkbox" id="maskPhone" checked onchange="applyClientFilters()" class="w-4 h-4 rounded-sm text-amber-500 focus:ring-amber-500 bg-slate-800 border-slate-700" />
            <span class="text-[11px] text-slate-300 font-medium">
              🛡️ ปิดบังเบอร์โทรศัพท์ (081-XXX-XXXX) ตาม PDPA
            </span>
          </label>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="pt-3 border-t border-slate-800/80 flex flex-wrap items-center gap-3">
        <button id="btnFetch" onclick="fetchLogs()" class="px-5 py-2.5 rounded-2xl gold-gradient hover:brightness-110 text-slate-950 font-bold text-xs flex items-center gap-2 shadow-lg shadow-amber-500/20 active:scale-95 transition cursor-pointer">
          <i data-lucide="cloud-download" class="w-4 h-4"></i>
          <span>ดูด Log จากเซิร์ฟเวอร์ทันที</span>
        </button>

        <button id="btnDownloadCsv" onclick="downloadCsv()" class="px-4 py-2.5 rounded-2xl bg-emerald-700 hover:bg-emerald-600 disabled:opacity-30 disabled:cursor-not-allowed text-white font-semibold text-xs flex items-center gap-2 transition active:scale-95 cursor-pointer shadow-md">
          <i data-lucide="file-spreadsheet" class="w-4 h-4 text-emerald-300"></i>
          <span>ส่งออกเป็น Excel / CSV</span>
        </button>

        <button id="btnDownloadJson" onclick="downloadJson()" class="px-4 py-2.5 rounded-2xl bg-slate-800 hover:bg-slate-700 disabled:opacity-30 disabled:cursor-not-allowed text-slate-200 font-semibold text-xs flex items-center gap-2 transition active:scale-95 cursor-pointer border border-slate-700">
          <i data-lucide="file-code" class="w-4 h-4 text-amber-400"></i>
          <span>ส่งออกเป็น JSON</span>
        </button>

        <button id="btnCopyJson" onclick="copyJson()" class="px-3.5 py-2.5 rounded-2xl bg-slate-900 hover:bg-slate-800 text-slate-300 font-medium text-xs flex items-center gap-1.5 transition active:scale-95 cursor-pointer border border-slate-800">
          <i data-lucide="copy" class="w-3.5 h-3.5 text-slate-400"></i>
          <span id="copyJsonText">คัดลอก JSON</span>
        </button>

        <span id="fetchStatus" class="text-xs text-slate-400 ml-auto flex items-center gap-1.5"></span>
      </div>
    </div>

    <!-- Real-time Stats Cards -->
    <div id="statsPanel" class="grid grid-cols-2 sm:grid-cols-4 gap-3.5">
      <div class="card-glass rounded-2xl p-4 space-y-1 shadow-md border-amber-500/20">
        <span class="text-[10.5px] text-slate-400 flex items-center gap-1.5">
          <i data-lucide="message-square" class="w-3.5 h-3.5 text-amber-400"></i> ข้อความที่ดูดมาได้
        </span>
        <div id="statTotal" class="text-2xl font-bold text-amber-400">0</div>
      </div>
      <div class="card-glass rounded-2xl p-4 space-y-1 shadow-md border-emerald-500/20">
        <span class="text-[10.5px] text-slate-400 flex items-center gap-1.5">
          <i data-lucide="users" class="w-3.5 h-3.5 text-emerald-400"></i> ผู้ใช้งานจริง (LINE)
        </span>
        <div id="statUsers" class="text-2xl font-bold text-emerald-400">0</div>
      </div>
      <div class="card-glass rounded-2xl p-4 space-y-1 shadow-md border-blue-500/20">
        <span class="text-[10.5px] text-slate-400 flex items-center gap-1.5">
          <i data-lucide="home" class="w-3.5 h-3.5 text-blue-400"></i> ค้นหาบ้าน/คอนโด
        </span>
        <div id="statProps" class="text-2xl font-bold text-blue-400">0</div>
      </div>
      <div class="card-glass rounded-2xl p-4 space-y-1 shadow-md border-purple-500/20">
        <span class="text-[10.5px] text-slate-400 flex items-center gap-1.5">
          <i data-lucide="key" class="w-3.5 h-3.5 text-purple-400"></i> สอบถามเปิดบ้าน/กุญแจ
        </span>
        <div id="statWorkflow" class="text-2xl font-bold text-purple-400">0</div>
      </div>
    </div>

    <!-- Data Preview Table -->
    <div id="tablePanel" class="card-glass rounded-3xl p-5 space-y-4 shadow-xl">
      <div class="flex items-center justify-between gap-3 flex-wrap">
        <div class="flex items-center gap-2.5">
          <h2 class="text-xs font-bold uppercase tracking-wider text-amber-400 flex items-center gap-2">
            <i data-lucide="table" class="w-4 h-4"></i>
            2. พรีวิวบทสนทนาที่ดูดลงมา (Local Preview)
          </h2>
          <span id="rowCountBadge" class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-800 text-slate-300 border border-slate-700">0 รายการ</span>
        </div>
        <div class="relative w-full sm:w-72">
          <i data-lucide="search" class="w-3.5 h-3.5 absolute left-3 top-3 text-slate-500"></i>
          <input type="text" id="searchTable" oninput="applyClientFilters()" placeholder="ค้นหาชื่อ, คำถาม, คำตอบ, รหัสทรัพย์..." 
            class="w-full pl-9 pr-3 py-1.5 rounded-xl bg-slate-900 border border-slate-700 text-xs text-white focus:outline-hidden focus:border-amber-500 transition" />
        </div>
      </div>

      <div class="overflow-x-auto rounded-2xl border border-slate-800">
        <table class="w-full text-left text-xs border-collapse">
          <thead>
            <tr class="bg-slate-900/90 text-slate-400 border-b border-slate-800">
              <th class="p-3.5 w-36 whitespace-nowrap">เวลา</th>
              <th class="p-3.5 w-48 whitespace-nowrap">ผู้ใช้ (LINE)</th>
              <th class="p-3.5 w-72">คำถามของผู้ใช้</th>
              <th class="p-3.5">คำตอบของน้องศิวา</th>
              <th class="p-3.5 w-32 text-center whitespace-nowrap">รหัสทรัพย์ที่แมทช์</th>
            </tr>
          </thead>
          <tbody id="tableBody" class="divide-y divide-slate-800/60 font-normal">
            <!-- Dynamic rows -->
          </tbody>
        </table>
      </div>
    </div>

  </div>

  <script>
    // Embedded cached logs securely serialized with JSON.parse to guarantee 0% syntax errors
    const EMBEDDED_CACHED_LOGS = JSON.parse(__EMBEDDED_JSON__);

    let rawFetchedLogs = Array.isArray(EMBEDDED_CACHED_LOGS) ? [...EMBEDDED_CACHED_LOGS] : [];
    let currentLogs = [...rawFetchedLogs];
    let selectedDays = 'all';

    function setServerPreset(mode) {
      const urlInput = document.getElementById('serverUrl');
      const btnLocal = document.getElementById('btnLocal');
      const btnCloud = document.getElementById('btnCloud');
      const btnR2 = document.getElementById('btnR2');

      [btnLocal, btnCloud, btnR2].forEach(b => {
        if (b) b.className = 'px-3 py-1.5 rounded-xl text-slate-300 hover:text-white transition cursor-pointer';
      });

      if (mode === 'local') {
        urlInput.value = 'http://127.0.0.1:5005';
        btnLocal.className = 'px-3 py-1.5 rounded-xl bg-amber-500 text-slate-950 font-bold transition shadow-xs cursor-pointer';
      } else if (mode === 'r2') {
        urlInput.value = 'https://assets.siwasup.com/data/line_chat_logs.json';
        btnR2.className = 'px-3 py-1.5 rounded-xl bg-amber-500 text-slate-950 font-bold transition shadow-xs cursor-pointer';
      } else {
        urlInput.value = 'https://siwasup-cobroker-os.onrender.com';
        btnCloud.className = 'px-3 py-1.5 rounded-xl bg-amber-500 text-slate-950 font-bold transition shadow-xs cursor-pointer';
      }
    }

    function setDays(days, btn) {
      selectedDays = days;
      document.querySelectorAll('.btn-days').forEach(b => {
        b.className = 'btn-days py-2 rounded-xl bg-slate-800 hover:bg-slate-700 font-medium transition cursor-pointer';
      });
      btn.className = 'btn-days py-2 rounded-xl bg-amber-500 text-slate-950 font-bold active-day transition shadow-xs cursor-pointer';
      applyClientFilters();
    }

    function applyClientFilters() {
      if (!rawFetchedLogs) rawFetchedLogs = [];
      const cat = document.getElementById('categoryFilter') ? document.getElementById('categoryFilter').value : 'all';
      const maskPhone = document.getElementById('maskPhone') ? document.getElementById('maskPhone').checked : true;
      const searchInput = document.getElementById('searchTable');
      const q = searchInput ? searchInput.value.toLowerCase().trim() : '';

      let filtered = [...rawFetchedLogs];

      // 1. Time Filter (days)
      if (selectedDays === '7' || selectedDays === '30') {
        const maxDays = parseInt(selectedDays, 10);
        const cutoff = Date.now() - (maxDays * 86400 * 1000);
        filtered = filtered.filter(c => {
          if (!c.timestamp) return true;
          const t = new Date(c.timestamp.replace(' ', 'T')).getTime();
          return isNaN(t) || t >= cutoff;
        });
      }

      // 2. Category Filter
      if (cat === 'property') {
        filtered = filtered.filter(c => (c.matched_codes && c.matched_codes.length > 0) || (c.user_text || '').includes('บ้าน') || (c.user_text || '').includes('คอนโด') || (c.user_text || '').includes('ที่ดิน'));
      } else if (cat === 'workflow') {
        filtered = filtered.filter(c => ['เปิดบ้าน', 'กุญแจ', 'จองคิว', 'otp', 'keybox', 'นัด'].some(w => (c.user_text || '').includes(w)));
      }

      // 3. Search keyword
      if (q) {
        filtered = filtered.filter(c => {
          const uText = (c.user_text || '').toLowerCase();
          const aReply = (c.ai_reply || '').toLowerCase();
          const uName = (c.user_name || '').toLowerCase();
          const codes = Array.isArray(c.matched_codes) ? c.matched_codes.join(' ').toLowerCase() : '';
          const tStamp = (c.timestamp || '').toLowerCase();
          return uText.includes(q) || aReply.includes(q) || uName.includes(q) || codes.includes(q) || tStamp.includes(q);
        });
      }

      // 4. PDPA PII Masking
      if (maskPhone) {
        filtered = filtered.map(c => {
          const cp = { ...c };
          if (cp.user_text) cp.user_text = cp.user_text.replace(/\\b(0\\d{2})[-.\\s]?(\\d{3,4})[-.\\s]?(\\d{4})\\b/g, '$1-XXX-$3');
          if (cp.ai_reply) cp.ai_reply = cp.ai_reply.replace(/\\b(0\\d{2})[-.\\s]?(\\d{3,4})[-.\\s]?(\\d{4})\\b/g, '$1-XXX-$3');
          return cp;
        });
      }

      currentLogs = filtered;
      renderStats(currentLogs);
      renderTable(currentLogs);

      const btnCsv = document.getElementById('btnDownloadCsv');
      const btnJson = document.getElementById('btnDownloadJson');
      if (btnCsv) btnCsv.disabled = currentLogs.length === 0;
      if (btnJson) btnJson.disabled = currentLogs.length === 0;

      const badge = document.getElementById('rowCountBadge');
      if (badge) badge.innerText = `${currentLogs.length} รายการ`;
    }

    async function fetchLogs() {
      const baseUrl = document.getElementById('serverUrl').value.trim().replace(/\\/+$/, '');
      const secret = document.getElementById('secretKey').value.trim();
      const statusEl = document.getElementById('fetchStatus');
      const connBadge = document.getElementById('connectionBadgeText');
      const connDot = document.getElementById('connectionDot');

      if (statusEl) {
        statusEl.innerHTML = '<span class="text-amber-400 animate-pulse flex items-center gap-1.5">⏳ กำลังเชื่อมต่อไปยัง ' + baseUrl.replace('https://', '') + '...</span>';
      }
      if (connBadge) connBadge.innerText = 'กำลังเชื่อมต่อ...';
      if (connDot) connDot.className = 'w-2 h-2 rounded-full bg-amber-400 animate-pulse';

      let targetUrl = '';
      if (baseUrl.endsWith('.json')) {
        targetUrl = baseUrl + '?t=' + Date.now();
      } else {
        targetUrl = `${baseUrl}/api/export-logs?secret=${encodeURIComponent(secret)}&days=all&category=all&mask_pii=false`;
      }

      let fetchSuccess = false;

      // 1. Try Primary Endpoint with 6-second timeout
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), 6000);
        const resp = await fetch(targetUrl, { cache: 'no-store', signal: controller.signal });
        clearTimeout(timeoutId);

        if (resp.ok) {
          const data = await resp.json();
          const items = Array.isArray(data) ? data : (data.conversations || data.logs || []);
          if (items && items.length > 0) {
            rawFetchedLogs = items;
            fetchSuccess = true;
            if (statusEl) {
              statusEl.innerHTML = '<span class="text-emerald-400 font-medium">✓ ดูดข้อมูลสำเร็จ (' + rawFetchedLogs.length + ' ข้อความล่าสุด)</span>';
            }
            if (connBadge) connBadge.innerText = 'ออนไลน์ (Render)';
            if (connDot) connDot.className = 'w-2 h-2 rounded-full bg-emerald-400';
          }
        }
      } catch (err) {
        console.warn('Primary fetch failed, switching to fast R2 backup:', err.message);
      }

      // 2. Fallback to Cloudflare R2 backup if primary failed
      if (!fetchSuccess && !baseUrl.includes('line_chat_logs.json')) {
        if (statusEl) {
          statusEl.innerHTML = '<span class="text-blue-400 animate-pulse">⚡ Render กำลังตื่น ดึงสำรองจาก Cloudflare R2 แทน...</span>';
        }
        try {
          const r2Url = 'https://assets.siwasup.com/data/line_chat_logs.json?t=' + Date.now();
          const r2Resp = await fetch(r2Url, { cache: 'no-store' });
          if (r2Resp.ok) {
            const data = await r2Resp.json();
            const items = Array.isArray(data) ? data : (data.conversations || data.logs || []);
            if (items && items.length > 0) {
              rawFetchedLogs = items;
              fetchSuccess = true;
              if (statusEl) {
                statusEl.innerHTML = '<span class="text-emerald-400 font-medium">✓ โหลดจาก Cloudflare R2 สำรองสำเร็จ (' + rawFetchedLogs.length + ' ข้อความ)</span>';
              }
              if (connBadge) connBadge.innerText = 'ออนไลน์ (R2 Backup)';
              if (connDot) connDot.className = 'w-2 h-2 rounded-full bg-emerald-400';
            }
          }
        } catch (r2Err) {
          console.warn('R2 fallback error:', r2Err);
        }
      }

      if (fetchSuccess) {
        applyClientFilters();
      } else {
        if (rawFetchedLogs && rawFetchedLogs.length > 0) {
          applyClientFilters();
          if (statusEl) {
            statusEl.innerHTML = '<span class="text-amber-400 font-medium">⚠️ ใช้ข้อมูลแคชล่าสุด (' + rawFetchedLogs.length + ' ข้อความ)</span>';
          }
          if (connBadge) connBadge.innerText = 'ใช้งานแคชออฟไลน์';
          if (connDot) connDot.className = 'w-2 h-2 rounded-full bg-amber-400';
        } else {
          if (statusEl) {
            statusEl.innerHTML = '<span class="text-red-400 font-medium">✕ ไม่สามารถเชื่อมต่อเซิร์ฟเวอร์ได้</span>';
          }
          if (connBadge) connBadge.innerText = 'ออฟไลน์';
          if (connDot) connDot.className = 'w-2 h-2 rounded-full bg-red-400';
        }
      }
    }

    function renderStats(logs) {
      const statTotal = document.getElementById('statTotal');
      const statUsers = document.getElementById('statUsers');
      const statProps = document.getElementById('statProps');
      const statWorkflow = document.getElementById('statWorkflow');

      if (!logs) logs = [];

      if (statTotal) statTotal.innerText = logs.length;

      const users = new Set(logs.map(l => (l.user_name || l.user_id_tail || 'User').trim())).size;
      if (statUsers) statUsers.innerText = users;

      const propCount = logs.filter(l => (l.matched_codes && l.matched_codes.length > 0) || ['บ้าน', 'คอนโด', 'ที่ดิน'].some(w => (l.user_text || '').includes(w))).length;
      if (statProps) statProps.innerText = propCount;

      const wfCount = logs.filter(l => {
        const txt = (l.user_text || '').toLowerCase();
        return ['เปิดบ้าน', 'กุญแจ', 'จองคิว', 'otp', 'นัด'].some(w => txt.includes(w));
      }).length;
      if (statWorkflow) statWorkflow.innerText = wfCount;
    }

    function renderTable(logs) {
      const tbody = document.getElementById('tableBody');
      if (!tbody) return;

      if (!logs || logs.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="p-8 text-center text-slate-500">ไม่พบข้อมูลตามเงื่อนไขที่เลือกในขณะนี้</td></tr>';
        return;
      }

      let html = '';
      logs.forEach((c, idx) => {
        const pic = c.user_pic || 'assets/siwasup_logo.png';
        const codes = (c.matched_codes || []).map(code => 
          `<a href="https://assets.siwasup.com/catalog.html?code=${encodeURIComponent(code)}" target="_blank" title="คลิกเพื่อเปิดดูทรัพย์แปลงนี้ใน Catalog" class="inline-block px-1.5 py-0.5 rounded-sm bg-amber-500/20 hover:bg-amber-500/40 text-amber-300 font-mono text-[10px] m-0.5 border border-amber-500/30 transition">#${code}</a>`
        ).join('');

        const formattedReply = (c.ai_reply || '-')
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;')
          .replace(/\\*\\*(.*?)\\*\\*/g, '<strong class="text-amber-300 font-semibold">$1</strong>')
          .replace(/\\n/g, '<br>');

        const formattedText = (c.user_text || '-')
          .replace(/&/g, '&amp;')
          .replace(/</g, '&lt;')
          .replace(/>/g, '&gt;')
          .replace(/\\n/g, '<br>');

        html += `
          <tr class="hover:bg-slate-800/40 transition border-b border-slate-800/60">
            <td class="p-3.5 text-slate-400 font-mono text-[11px] whitespace-nowrap align-top">
              <div class="font-semibold text-slate-300">${c.timestamp ? c.timestamp.split(' ')[1] : '-'}</div>
              <div class="text-[10px] text-slate-500">${c.timestamp ? c.timestamp.split(' ')[0] : ''}</div>
              <div class="text-[9.5px] text-emerald-400 font-sans mt-0.5">#${idx + 1}</div>
            </td>
            <td class="p-3.5 align-top">
              <div class="flex items-center gap-2.5">
                <img src="${pic}" class="w-7 h-7 rounded-full object-cover bg-slate-800 border border-slate-700 shrink-0 shadow-xs" onerror="this.src='assets/siwasup_logo.png'">
                <div class="min-w-0">
                  <div class="font-medium text-slate-200 text-xs truncate max-w-[130px]" title="${c.user_name || 'ไม่ระบุชื่อ'}">${c.user_name || 'ไม่ระบุชื่อ'}</div>
                  <div class="text-[9.5px] text-slate-500 font-mono truncate max-w-[130px]">ID: ${c.user_id_tail || '-'}</div>
                </div>
              </div>
            </td>
            <td class="p-3.5 text-white max-w-xs break-words align-top leading-relaxed bg-slate-900/30 rounded-lg">
              ${formattedText}
            </td>
            <td class="p-3.5 text-slate-300 max-w-md break-words leading-relaxed align-top text-xs">
              ${formattedReply}
            </td>
            <td class="p-3.5 text-center align-top whitespace-nowrap">
              ${codes || '<span class="text-slate-600 font-mono text-xs">-</span>'}
            </td>
          </tr>
        `;
      });

      tbody.innerHTML = html;
      if (window.lucide) lucide.createIcons();
    }

    function downloadJson() {
      if (!currentLogs.length) return;
      const dataStr = 'data:text/json;charset=utf-8,' + encodeURIComponent(JSON.stringify(currentLogs, null, 2));
      const a = document.createElement('a');
      a.setAttribute('href', dataStr);
      a.setAttribute('download', `siwasup_chat_logs_${new Date().toISOString().slice(0, 10)}.json`);
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    function downloadCsv() {
      if (!currentLogs.length) return;
      const headers = ['ลำดับ', 'Log_ID', 'วัน-เวลา', 'ชื่อผู้ใช้ (LINE)', 'Line_ID', 'คำถามของผู้ใช้', 'คำตอบของน้องศิวา', 'รหัสทรัพย์ที่แมทช์', 'ความเร็ว (ms)'];
      const rows = currentLogs.map((c, i) => [
        `"${i + 1}"`,
        `"${(c.id || '').replace(/"/g, '""')}"`,
        `"${(c.timestamp || '').replace(/"/g, '""')}"`,
        `"${(c.user_name || '').replace(/"/g, '""')}"`,
        `"${(c.user_id_tail || '').replace(/"/g, '""')}"`,
        `"${(c.user_text || '').replace(/"/g, '""').replace(/\\r?\\n/g, ' ')}"`,
        `"${(c.ai_reply || '').replace(/"/g, '""').replace(/\\r?\\n/g, ' ')}"`,
        `"${((c.matched_codes || []).join('; ')).replace(/"/g, '""')}"`,
        `"${c.latency_ms || ''}"`
      ]);

      const csvContent = '\\uFEFF' + [headers.join(','), ...rows.map(e => e.join(','))].join('\\r\\n');
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.setAttribute('href', url);
      a.setAttribute('download', `siwasup_chat_logs_${new Date().toISOString().slice(0, 10)}.csv`);
      document.body.appendChild(a);
      a.click();
      a.remove();
    }

    function copyJson() {
      if (!currentLogs.length) return;
      const jsonStr = JSON.stringify(currentLogs, null, 2);
      navigator.clipboard.writeText(jsonStr).then(() => {
        const textEl = document.getElementById('copyJsonText');
        if (textEl) {
          textEl.innerText = '✓ คัดลอกสำเร็จ';
          setTimeout(() => { textEl.innerText = 'คัดลอก JSON'; }, 2000);
        }
      }).catch(err => {
        console.error('Copy failed:', err);
      });
    }

    window.addEventListener('DOMContentLoaded', () => {
      if (window.lucide) lucide.createIcons();
      // Render embedded logs immediately in 0.01s so screen is NEVER blank
      applyClientFilters();
      // Auto-fetch latest updates from live server or R2
      fetchLogs();
    });
  </script>
</body>
</html>
'''

def main():
    json_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\data\line_chat_logs.json"
    with open(json_path, "r", encoding="utf-8") as f:
        logs_data = json.load(f)

    conversations = logs_data.get("conversations", [])
    # Double json.dumps so that it produces a valid JS string literal that JSON.parse reads safely
    serialized_json = json.dumps(json.dumps(conversations, ensure_ascii=False))

    output_html = HTML_TEMPLATE.replace("__EMBEDDED_JSON__", serialized_json)

    out_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\offline_log_exporter.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(output_html)

    print(f"[SUCCESS] Rebuilt {out_path} with {len(conversations)} embedded conversations. File size: {len(output_html):,} bytes")

if __name__ == "__main__":
    main()
