import json
import re

# Read index.html to extract the exact head, styles, and scripts
with open(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\index.html", "r", encoding="utf-8") as f:
    index_html = f.read()

# Extract styles from index.html
style_match = re.search(r'(<style>.*?</style>)', index_html, re.DOTALL)
styles = style_match.group(1) if style_match else ""

catalog_code = f"""<!DOCTYPE html>
<html lang="th" class="overflow-x-hidden">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
  <meta name="theme-color" content="#8B0000">
  <title>Siwasup Co-Broker OS - แคตตาล็อกทรัพย์ NPA 10,672 รายการ</title>
  
  <!-- Tailwind CSS & Lucide Icons -->
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://unpkg.com/lucide@latest"></script>
  
  <!-- Fonts: Kanit & Sarabun -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Kanit:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Sarabun:wght@300;400;500;600;700&display=swap" rel="stylesheet">
  
  {styles}
  
  <style>
    body {{
      background-color: #FAF7F2 !important; /* The 75% Warm Sand / Ivory from Ton's presentation */
      color: #171717;
      font-family: 'Kanit', -apple-system, BlinkMacSystemFont, Tahoma, sans-serif;
    }}
  </style>
</head>
<body class="min-h-screen text-gray-800 pb-16 overflow-x-hidden w-full max-w-full">

  <!-- Responsive App Container -->
  <div class="w-full max-w-7xl mx-auto bg-white min-h-screen shadow-xl relative flex flex-col border-x border-neutral-200/70">
    
    <!-- 🏛️ Top Header (Sticky, Backdrop-blur) -->
    <header class="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-neutral-200/80 shadow-xs">
      
      <!-- 1. Top Role Utility Bar: ปรับเพิ่มสีแดง Heritage Red ลดสีดำด้านตามคำสั่งคุณต้น -->
      <div class="bg-gradient-to-r from-[#8B0000] via-[#700000] to-[#8B0000] text-neutral-100 text-xs py-1.5 px-3 sm:px-4 border-b border-[#C2A460]/40 shadow-xs">
        <div class="max-w-7xl mx-auto flex items-center justify-between gap-1.5 sm:gap-2">
          
          <!-- ซ้าย: โหมดตัวแทน -->
          <div class="flex items-center gap-1.5 shrink-0 z-10">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 shrink-0 animate-pulse"></span>
            <span class="text-white font-semibold text-[11px] whitespace-nowrap">Siwasup Co-Broker Hub</span>
            <span class="text-[10px] font-semibold px-2 py-0.5 rounded-full bg-[#FFE885]/20 text-[#FFE885] border border-[#FFE885]/30">
              ฐานข้อมูล NPA 10,672 ทรัพย์
            </span>
          </div>

          <!-- ขวา: ปุ่มเครื่องมือเชื่อมต่อ LINE & แคตตาล็อก -->
          <div class="flex items-center gap-1.5 shrink-0 text-[11px]">
            <a href="https://line.me/R/ti/p/@813nyyia" target="_blank" class="h-6 px-2.5 rounded-md bg-[#5C0000] hover:bg-[#780000] border border-[#C2A460]/40 text-[#FFE885] font-semibold flex items-center gap-1 transition active:scale-95">
              <span>💬</span>
              <span>LINE ตัวแทน</span>
            </a>
            <a href="index.html" class="h-6 px-2.5 rounded-md bg-[#5C0000] hover:bg-[#780000] border border-[#C2A460]/40 text-white flex items-center gap-1 transition active:scale-95">
              <span>🏠</span>
              <span class="hidden sm:inline">หน้าหลัก OS</span>
            </a>
          </div>

        </div>
      </div>

      <!-- 2. Main Header: จัด โลโก้ (ซ้าย) + Floating Pill Search (กลาง) + ปุ่มฝากขาย (ขวา) -->
      <div class="max-w-7xl mx-auto px-3 sm:px-4 py-2.5">
        <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-2.5 sm:gap-3">
          
          <!-- โลโก้จริงศิวาทรัพย์ -->
          <div class="flex items-center justify-between lg:justify-start gap-2.5 sm:gap-3.5 shrink-0 py-0.5">
            <a href="catalog.html" class="flex items-center gap-2 sm:gap-3 group transition-transform active:scale-98">
              <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-[#8B0000] to-[#5C0000] border border-[#C2A460]/50 flex items-center justify-center text-[#FFE885] font-bold text-xl shadow-xs shrink-0">
                S
              </div>
              <div>
                <div class="flex items-center gap-1.5 sm:gap-2">
                  <span class="font-extrabold text-neutral-900 text-sm sm:text-base lg:text-lg tracking-tight whitespace-nowrap block leading-tight group-hover:text-[#8B0000] transition-colors">
                    ศิวาทรัพย์ <span class="text-[#8B0000] font-bold">แอสเซท</span>
                  </span>
                  <span class="text-[9px] sm:text-[10px] font-semibold px-2 py-0.5 rounded-full bg-[#8B0000]/10 text-[#8B0000] border border-[#8B0000]/20 whitespace-nowrap">
                    Co-Broker OS
                  </span>
                </div>
                <p class="hidden sm:block text-[11px] text-neutral-500 font-normal whitespace-nowrap mt-0.5 font-sarabun">
                  แคตตาล็อกทรัพย์ NPA ราคาทุนธนาคารทั่วประเทศ
                </p>
              </div>
            </a>

            <!-- ปุ่ม LINE บนมือถือ -->
            <a href="https://line.me/R/ti/p/@813nyyia" target="_blank" class="lg:hidden px-3 py-1.5 rounded-full bg-[#06C755] text-white text-[11px] font-semibold flex items-center gap-1 shadow-xs shrink-0 transition-transform active:scale-95">
              <span>💬</span>
              <span>LINE</span>
            </a>
          </div>

          <!-- กลาง: Unified Floating Pill Search ทรงแคปซูลตามธีมเป๊ะๆ -->
          <div class="flex-1 w-full lg:max-w-3xl">
            <div class="bg-neutral-50/95 rounded-2xl lg:rounded-full border border-neutral-200/90 p-2 lg:py-1 lg:px-2 shadow-xs transition-all">
              <div class="grid grid-cols-2 lg:grid-cols-[1.4fr_1fr_1fr_1fr_auto] items-center gap-1.5 lg:gap-0">
                
                <!-- ช่องที่ 1: ค้นหาทรัพย์ -->
                <div class="col-span-2 lg:col-span-1 px-3 py-1 relative">
                  <label class="block text-[9px] font-semibold text-neutral-400 uppercase tracking-wider">ค้นหาทรัพย์</label>
                  <div class="flex items-center">
                    <input type="text" id="searchInput" 
                           placeholder="รหัส NPA, โครงการ, เขต, จังหวัด..." 
                           class="w-full bg-transparent text-xs font-medium text-neutral-800 placeholder-neutral-400 focus:outline-none truncate pr-5" />
                    <button id="clearSearch" class="hidden text-neutral-400 hover:text-neutral-600 text-sm font-bold leading-none pr-1">&times;</button>
                  </div>
                </div>

                <!-- ช่องที่ 2: ธนาคาร (SCB, SAM, TTB) -->
                <div class="px-3 py-1 lg:border-l border-neutral-200/70">
                  <label class="block text-[9px] font-semibold text-neutral-400 uppercase tracking-wider">ธนาคาร NPA</label>
                  <select id="bankSelect" class="w-full bg-transparent text-xs font-semibold text-neutral-800 focus:outline-none cursor-pointer truncate">
                    <option value="ALL">ทุกธนาคาร (10,672)</option>
                    <option value="SCB">SCB ไทยพาณิชย์ (4,207)</option>
                    <option value="SAM">SAM สุขุมวิท (5,100)</option>
                    <option value="TTB">TTB ทีทีบี (1,365)</option>
                  </select>
                </div>

                <!-- ช่องที่ 3: ประเภททรัพย์ -->
                <div class="px-3 py-1 lg:border-l border-neutral-200/70">
                  <label class="block text-[9px] font-semibold text-neutral-400 uppercase tracking-wider">ประเภท</label>
                  <select id="typeSelect" class="w-full bg-transparent text-xs font-semibold text-neutral-800 focus:outline-none cursor-pointer truncate">
                    <option value="ALL">ทุกประเภท</option>
                    <option value="SDH">บ้านเดี่ยว</option>
                    <option value="TH">ทาวน์เฮ้าส์</option>
                    <option value="CD">คอนโด</option>
                    <option value="CH">อาคารพาณิชย์</option>
                    <option value="LD">ที่ดินเปล่า</option>
                    <option value="TWH">บ้านแฝด</option>
                  </select>
                </div>

                <!-- ช่องที่ 4: งบประมาณ -->
                <div class="px-3 py-1 lg:border-l border-neutral-200/70">
                  <label class="block text-[9px] font-semibold text-neutral-400 uppercase tracking-wider">งบประมาณ</label>
                  <select id="priceSelect" class="w-full bg-transparent text-xs font-semibold text-neutral-800 focus:outline-none cursor-pointer truncate">
                    <option value="ALL">ทุกช่วงราคา</option>
                    <option value="0-1000000">ต่ำกว่า 1 ล้าน</option>
                    <option value="1000000-3000000">1 - 3 ล้าน</option>
                    <option value="3000000-5000000">3 - 5 ล้าน</option>
                    <option value="5000000-10000000">5 - 10 ล้าน</option>
                    <option value="10000000-999999999">มากกว่า 10 ล้าน</option>
                  </select>
                </div>

                <!-- ปุ่มค้นหา -->
                <div class="col-span-2 lg:col-span-1 p-1 flex justify-end">
                  <button type="button" class="w-full lg:w-8 h-8 rounded-full bg-[#8B0000] hover:bg-[#6B0000] text-white flex items-center justify-center text-xs shadow-xs transition active:scale-95">
                    <span>🔍</span>
                  </button>
                </div>

              </div>
            </div>
          </div>

        </div>

        <!-- แถบชิปคัดกรองด่วน (Quick Filter Chips) สีแดงและทองซาติน -->
        <div class="flex items-center gap-2 overflow-x-auto no-scrollbar pt-2.5 pb-0.5 text-xs">
          <span class="text-[11px] font-medium text-neutral-400 whitespace-nowrap font-sarabun">คัดกรองด่วน:</span>
          <button class="chip-filter px-3 py-1 rounded-full bg-[#8B0000] text-white font-semibold text-[11px] border border-[#8B0000] shadow-2xs whitespace-nowrap active" data-bank="ALL">
            ทั้งหมด (10,672)
          </button>
          <button class="chip-filter px-3 py-1 rounded-full bg-white text-neutral-600 hover:text-[#8B0000] font-medium text-[11px] border border-neutral-200/80 whitespace-nowrap" data-bank="SCB">
            🏦 SCB (4,207)
          </button>
          <button class="chip-filter px-3 py-1 rounded-full bg-white text-neutral-600 hover:text-[#8B0000] font-medium text-[11px] border border-neutral-200/80 whitespace-nowrap" data-bank="SAM">
            🏛️ SAM (5,100)
          </button>
          <button class="chip-filter px-3 py-1 rounded-full bg-white text-neutral-600 hover:text-[#8B0000] font-medium text-[11px] border border-neutral-200/80 whitespace-nowrap" data-bank="TTB">
            🏢 TTB (1,365)
          </button>
          <div class="h-4 w-px bg-neutral-200 mx-1 shrink-0"></div>
          <button class="chip-type px-3 py-1 rounded-full bg-white text-neutral-600 hover:text-[#8B0000] font-medium text-[11px] border border-neutral-200/80 whitespace-nowrap" data-type="SDH">
            🏡 บ้านเดี่ยว
          </button>
          <button class="chip-type px-3 py-1 rounded-full bg-white text-neutral-600 hover:text-[#8B0000] font-medium text-[11px] border border-neutral-200/80 whitespace-nowrap" data-type="TH">
            🏘️ ทาวน์เฮ้าส์
          </button>
          <button class="chip-type px-3 py-1 rounded-full bg-white text-neutral-600 hover:text-[#8B0000] font-medium text-[11px] border border-neutral-200/80 whitespace-nowrap" data-type="CD">
            🏢 คอนโด
          </button>
        </div>

      </div>

    </header>

    <!-- Main Content Area: พื้นขาวนวล Warm Sand (#FAF7F2) ขับรูปทรัพย์เด่น -->
    <div class="bg-[#FAF7F2] flex-1 px-3 sm:px-6 py-5">
      
      <!-- Stats bar -->
      <div class="max-w-7xl mx-auto flex items-center justify-between text-xs text-neutral-500 font-sarabun mb-4">
        <div>
          พบทรัพย์คัดพิเศษ <span id="filteredCount" class="font-bold text-[#8B0000] text-sm">0</span> รายการ
        </div>
        <div class="flex items-center gap-2">
          <span>เรียงตาม:</span>
          <select id="sortSelect" class="bg-white border border-neutral-200 rounded-md px-2 py-1 text-xs font-medium text-neutral-700 outline-none">
            <option value="default">⚡ แนะนำล่าสุด</option>
            <option value="price_asc">💵 ราคา ต่ำ ➡️ สูง</option>
            <option value="price_desc">💎 ราคา สูง ➡️ ต่ำ</option>
          </select>
        </div>
      </div>

      <!-- Property Grid (Luxury White Cards from Ton's presentation) -->
      <div id="cardsGrid" class="max-w-7xl mx-auto grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
        <!-- Injected via JS -->
      </div>

      <!-- Load More -->
      <div class="text-center mt-8 mb-6" id="loadMoreWrap" style="display: none;">
        <button id="loadMoreBtn" class="px-8 py-3 rounded-full bg-white hover:bg-[#8B0000] text-[#8B0000] hover:text-white font-bold text-sm border-2 border-[#8B0000] shadow-sm hover:shadow-md transition-all active:scale-95">
          โหลดทรัพย์เพิ่มเติม ❯
        </button>
      </div>

    </div>

    <!-- Footer -->
    <footer class="bg-white border-t border-neutral-200 py-6 px-4 text-center text-xs text-neutral-500 font-sarabun">
      <div class="max-w-7xl mx-auto">
        <p class="font-semibold text-neutral-700">SIWASUP ASSET CO., LTD. | The Digital Luxury Co-Broker OS</p>
        <p class="mt-1">ระบบฐานข้อมูล NPA 10,672 ทรัพย์ พร้อมคลังภาพความละเอียดสูงบน Cloudflare R2 Egress $0</p>
        <p class="mt-2 text-[#8B0000] font-semibold">LINE OA: @813nyyia</p>
      </div>
    </footer>

  </div>

  <!-- Lightbox Gallery Modal -->
  <div id="galleryModal" class="modal-backdrop hidden">
    <div class="modal-card max-w-lg bg-white rounded-2xl shadow-2xl border border-neutral-200 overflow-hidden flex flex-col p-0">
      <div class="p-3.5 bg-gradient-to-r from-[#8B0000] to-[#6B0000] text-white flex items-center justify-between">
        <div>
          <h3 id="modalTitle" class="font-bold text-sm text-[#FFE885]">-</h3>
          <p id="modalSub" class="text-[11px] text-red-100 font-sarabun">-</p>
        </div>
        <button id="modalClose" class="text-white hover:text-red-200 text-2xl font-bold leading-none">&times;</button>
      </div>
      <div class="h-64 sm:h-72 bg-neutral-900 flex items-center justify-center overflow-hidden">
        <img id="modalMainImg" src="" alt="Gallery" class="max-h-full max-w-full object-contain">
      </div>
      <div id="modalThumbsRow" class="flex gap-2 p-2.5 bg-neutral-100 overflow-x-auto border-t border-neutral-200">
        <!-- Thumbs -->
      </div>
      <div class="p-4 bg-white flex items-center justify-between border-t border-neutral-200">
        <div>
          <span class="text-[10px] text-neutral-400 font-sarabun">ราคาทุนธนาคาร</span>
          <div id="modalPrice" class="text-xl font-extrabold text-[#8B0000]">฿0</div>
        </div>
        <a href="#" id="modalLineDealBtn" target="_blank" class="px-4 py-2 rounded-xl bg-[#06C755] hover:bg-[#05a847] text-white font-bold text-xs flex items-center gap-1.5 shadow-sm transition active:scale-95">
          <span>💬</span>
          <span>นัดดู/จองสิทธิ์ผ่าน LINE</span>
        </a>
      </div>
    </div>
  </div>

  <script>
    let allProperties = [];
    let filteredList = [];
    let pageSize = 24;
    let currentPage = 1;

    let currentBank = 'ALL';
    let currentType = 'ALL';
    let currentPriceRange = 'ALL';
    let currentSort = 'default';
    let currentSearch = '';

    async function initCatalog() {{
      const grid = document.getElementById('cardsGrid');
      grid.innerHTML = '<div class="col-span-full py-20 text-center text-neutral-400 font-sarabun"><div class="text-3xl mb-2">⏳</div>กำลังโหลดแคตตาล็อกทรัพย์ 10,672 รายการ...</div>';

      try {{
        const resp = await fetch('data/catalog_index.json?v=' + Date.now());
        if (!resp.ok) {{
          const fallbackResp = await fetch('catalog_index.json?v=' + Date.now());
          allProperties = await fallbackResp.json();
        }} else {{
          allProperties = await resp.json();
        }}

        applyFilters();
        setupEventListeners();
      }} catch (err) {{
        grid.innerHTML = `<div class="col-span-full py-20 text-center text-neutral-400 font-sarabun"><div class="text-3xl mb-2">⚠️</div>ไม่สามารถโหลดข้อมูลได้: ${{err.message}}</div>`;
      }}
    }}

    function applyFilters() {{
      filteredList = allProperties.filter(item => {{
        if (currentBank !== 'ALL' && item.b !== currentBank) return false;
        if (currentType !== 'ALL' && item.t !== currentType) return false;
        
        if (currentPriceRange !== 'ALL') {{
          const [min, max] = currentPriceRange.split('-').map(Number);
          if (item.pr < min || item.pr > max) return false;
        }}

        if (currentSearch.trim() !== '') {{
          const q = currentSearch.toLowerCase().trim();
          const matchCode = (item.c || '').toLowerCase().includes(q);
          const matchProv = (item.p || '').toLowerCase().includes(q);
          const matchProvEn = (item.pe || '').toLowerCase().includes(q);
          const matchDist = (item.d || '').toLowerCase().includes(q);
          const matchType = (item.tn || '').toLowerCase().includes(q);
          if (!matchCode && !matchProv && !matchProvEn && !matchDist && !matchType) return false;
        }}

        return true;
      }});

      if (currentSort === 'price_asc') {{
        filteredList.sort((a, b) => a.pr - b.pr);
      }} else if (currentSort === 'price_desc') {{
        filteredList.sort((a, b) => b.pr - a.pr);
      }}

      currentPage = 1;
      renderGrid();
    }}

    function renderGrid() {{
      const grid = document.getElementById('cardsGrid');
      const filteredCountEl = document.getElementById('filteredCount');
      const loadMoreWrap = document.getElementById('loadMoreWrap');

      filteredCountEl.innerText = filteredList.length.toLocaleString();

      if (filteredList.length === 0) {{
        grid.innerHTML = `
          <div class="col-span-full py-20 text-center text-neutral-400 font-sarabun">
            <div class="text-4xl mb-2">🔍</div>
            <h3 class="font-bold text-neutral-700 text-base">ไม่พบทรัพย์ที่ตรงกับเงื่อนไข</h3>
            <p class="text-xs mt-1">ลองเปลี่ยนคำค้นหา หรือเลือกช่วงราคา/ธนาคารอื่นดูนะครับ</p>
          </div>
        `;
        loadMoreWrap.style.display = 'none';
        return;
      }}

      const totalToShow = Math.min(currentPage * pageSize, filteredList.length);
      const itemsToRender = filteredList.slice(0, totalToShow);

      let html = '';
      itemsToRender.forEach(p => {{
        const formattedPrice = '฿' + (p.pr || 0).toLocaleString();
        const distName = p.d ? `${{p.d}}, ` : '';
        const locStr = `${{distName}}${{p.p}}`;
        
        let specsHtml = '';
        if (p.bed > 0) specsHtml += `<span>🛏️ ${{p.bed}} นอน</span>`;
        if (p.bath > 0) specsHtml += `<span>🚿 ${{p.bath}} น้ำ</span>`;
        if (p.sqm > 0) specsHtml += `<span>📐 ${{p.sqm}} ตร.ม.</span>`;
        if (p.sqw > 0) specsHtml += `<span>🏡 ${{p.sqw}} ตร.ว.</span>`;
        if (!specsHtml) specsHtml = `<span>✨ ทรัพย์พร้อมโอนกรรมสิทธิ์</span>`;

        const lineText = encodeURIComponent(`สวัสดีครับ สนใจทรัพย์รหัส: ${{p.c}} (${{p.tn}}) ราคา ${{formattedPrice}} ทำเล ${{locStr}} (ธนาคาร ${{p.b}}) ขอข้อมูลเพิ่มเติมครับ`);
        const lineUrl = `https://line.me/R/ti/p/@813nyyia?text=${{lineText}}`;

        let bankBadgeColor = 'bg-[#4E2A84]';
        if (p.b === 'SAM') bankBadgeColor = 'bg-[#8B0000]';
        else if (p.b === 'TTB') bankBadgeColor = 'bg-[#002D62]';

        html += `
          <div class="bg-white rounded-2xl border border-neutral-200/90 hover:border-[#C2A460] shadow-xs hover:shadow-md transition-all duration-200 overflow-hidden flex flex-col group">
            
            <!-- Thumbnail Box -->
            <div class="w-full h-48 bg-neutral-100 relative overflow-hidden">
              <img src="${{p.thumb}}" class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" loading="lazy" onerror="this.src='https://assets.siwasup.com/rich_menu_ton.jpg'" alt="${{p.c}}">
              
              <div class="absolute top-2.5 left-2.5 flex items-center gap-1.5 z-10">
                <span class="${{bankBadgeColor}} text-white font-extrabold text-[10px] px-2 py-0.5 rounded shadow-xs tracking-wider">
                  ${{p.b}}
                </span>
                <span class="bg-white/90 backdrop-blur-xs text-neutral-800 font-semibold text-[10px] px-2 py-0.5 rounded shadow-xs border border-neutral-200/50">
                  ${{p.tn}}
                </span>
              </div>

              <div class="absolute bottom-2.5 right-2.5 bg-neutral-900/80 backdrop-blur-xs text-white text-[10px] font-medium px-2 py-0.5 rounded-full flex items-center gap-1">
                <span>📷</span>
                <span>${{p.gc || 5}} รูป</span>
              </div>
            </div>

            <!-- Content Box -->
            <div class="p-4 flex flex-col flex-1 justify-between gap-3 bg-white">
              <div>
                <div class="flex items-baseline justify-between gap-2">
                  <div class="text-xl font-extrabold text-[#8B0000] tracking-tight">${{formattedPrice}}</div>
                  <span class="text-[10px] font-mono text-neutral-500 bg-neutral-100 px-1.5 py-0.5 rounded border border-neutral-200/80">${{p.c}}</span>
                </div>
                
                <div class="text-xs text-neutral-700 font-medium flex items-center gap-1 mt-1 truncate" title="${{locStr}}">
                  <span class="text-neutral-400">📍</span>
                  <span class="truncate">${{locStr}}</span>
                </div>
              </div>

              <div class="flex items-center gap-2.5 text-[11px] text-neutral-500 font-sarabun py-2 border-y border-neutral-100">
                ${{specsHtml}}
              </div>

              <div class="grid grid-cols-2 gap-2 pt-1">
                <button onclick="openGallery('${{p.id}}', '${{p.c}}', '${{p.b}}', '${{p.tn}}', ${{p.pr}}, '${{p.p}}')" class="py-2 px-2.5 rounded-xl bg-white hover:bg-neutral-50 border border-[#C2A460] text-[#8A6A1F] font-semibold text-xs flex items-center justify-center gap-1 transition active:scale-95">
                  <span>🖼️</span> ดูรูป
                </button>
                <a href="${{lineUrl}}" target="_blank" class="py-2 px-2.5 rounded-xl bg-[#8B0000] hover:bg-[#6B0000] text-white font-semibold text-xs flex items-center justify-center gap-1 shadow-2xs transition active:scale-95">
                  <span>💬</span> จองสิทธิ์
                </a>
              </div>
            </div>

          </div>
        `;
      }});

      grid.innerHTML = html;

      if (totalToShow < filteredList.length) {{
        loadMoreWrap.style.display = 'block';
      }} else {{
        loadMoreWrap.style.display = 'none';
      }}
    }}

    function openGallery(id, code, bank, typeName, price, province) {{
      const modal = document.getElementById('galleryModal');
      const titleEl = document.getElementById('modalTitle');
      const subEl = document.getElementById('modalSub');
      const priceEl = document.getElementById('modalPrice');
      const mainImg = document.getElementById('modalMainImg');
      const thumbsRow = document.getElementById('modalThumbsRow');
      const lineBtn = document.getElementById('modalLineDealBtn');

      titleEl.innerText = `รหัสทรัพย์: ${{code}} (${{typeName}})`;
      subEl.innerText = `ธนาคาร ${{bank}} • ทำเล ${{province}}`;
      priceEl.innerText = '฿' + price.toLocaleString();

      const lineText = encodeURIComponent(`สวัสดีครับ สนใจทรัพย์รหัส: ${{code}} (${{typeName}}) ราคา ฿${{price.toLocaleString()}} ทำเล ${{province}} (ธนาคาร ${{bank}}) ขอข้อมูลเพิ่มเติมครับ`);
      lineBtn.href = `https://line.me/R/ti/p/@813nyyia?text=${{lineText}}`;

      const ext = 'jpg';
      const galleryUrls = [];
      for (let i = 0; i < 5; i++) {{
        galleryUrls.push(`https://assets.siwasup.com/${{bank.toLowerCase()}}/${{id}}/gallery_${{i}}.${{ext}}`);
      }}

      mainImg.src = galleryUrls[0];
      mainImg.onerror = function() {{
        this.src = `https://assets.siwasup.com/${{bank.toLowerCase()}}/${{id}}/thumb.jpg`;
      }};

      let thumbsHtml = '';
      galleryUrls.forEach((url, idx) => {{
        thumbsHtml += `
          <img src="${{url}}" class="w-14 h-10 rounded object-cover cursor-pointer border-2 ${{idx === 0 ? 'border-[#8B0000]' : 'border-transparent opacity-60'}} hover:opacity-100 transition" 
               onclick="selectModalImg(this, '${{url}}')" 
               onerror="this.style.display='none'">
        `;
      }});
      thumbsRow.innerHTML = thumbsHtml;

      modal.classList.remove('hidden');
      document.body.classList.add('modal-open');
    }}

    function selectModalImg(el, url) {{
      document.getElementById('modalMainImg').src = url;
      document.querySelectorAll('#modalThumbsRow img').forEach(t => {{
        t.classList.remove('border-[#8B0000]');
        t.classList.add('border-transparent', 'opacity-60');
      }});
      el.classList.remove('border-transparent', 'opacity-60');
      el.classList.add('border-[#8B0000]');
    }}

    function closeModal() {{
      const modal = document.getElementById('galleryModal');
      modal.classList.add('hidden');
      document.body.classList.remove('modal-open');
    }}

    function setupEventListeners() {{
      // Bank Select & Chips
      document.getElementById('bankSelect').addEventListener('change', (e) => {{
        currentBank = e.target.value;
        syncBankChips(currentBank);
        applyFilters();
      }});

      document.querySelectorAll('.chip-filter').forEach(btn => {{
        btn.addEventListener('click', () => {{
          currentBank = btn.dataset.bank;
          document.getElementById('bankSelect').value = currentBank;
          syncBankChips(currentBank);
          applyFilters();
        }});
      }});

      // Type Select & Chips
      document.getElementById('typeSelect').addEventListener('change', (e) => {{
        currentType = e.target.value;
        syncTypeChips(currentType);
        applyFilters();
      }});

      document.querySelectorAll('.chip-type').forEach(btn => {{
        btn.addEventListener('click', () => {{
          currentType = (currentType === btn.dataset.type) ? 'ALL' : btn.dataset.type;
          document.getElementById('typeSelect').value = currentType;
          syncTypeChips(currentType);
          applyFilters();
        }});
      }});

      document.getElementById('priceSelect').addEventListener('change', (e) => {{
        currentPriceRange = e.target.value;
        applyFilters();
      }});

      document.getElementById('sortSelect').addEventListener('change', (e) => {{
        currentSort = e.target.value;
        applyFilters();
      }});

      const searchInput = document.getElementById('searchInput');
      const clearBtn = document.getElementById('clearSearch');
      let debounceTimer = null;

      searchInput.addEventListener('input', (e) => {{
        const val = e.target.value;
        clearBtn.classList.toggle('hidden', !val);
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {{
          currentSearch = val;
          applyFilters();
        }}, 200);
      }});

      clearBtn.addEventListener('click', () => {{
        searchInput.value = '';
        clearBtn.classList.add('hidden');
        currentSearch = '';
        applyFilters();
      }});

      document.getElementById('loadMoreBtn').addEventListener('click', () => {{
        currentPage++;
        renderGrid();
      }});

      document.getElementById('modalClose').addEventListener('click', closeModal);
      document.getElementById('galleryModal').addEventListener('click', (e) => {{
        if (e.target.id === 'galleryModal') closeModal();
      }});
    }}

    function syncBankChips(bankVal) {{
      document.querySelectorAll('.chip-filter').forEach(b => {{
        if (b.dataset.bank === bankVal) {{
          b.className = 'chip-filter px-3 py-1 rounded-full bg-[#8B0000] text-white font-semibold text-[11px] border border-[#8B0000] shadow-2xs whitespace-nowrap active';
        }} else {{
          b.className = 'chip-filter px-3 py-1 rounded-full bg-white text-neutral-600 hover:text-[#8B0000] font-medium text-[11px] border border-neutral-200/80 whitespace-nowrap';
        }}
      }});
    }}

    function syncTypeChips(typeVal) {{
      document.querySelectorAll('.chip-type').forEach(b => {{
        if (b.dataset.type === typeVal) {{
          b.className = 'chip-type px-3 py-1 rounded-full bg-[#8B0000] text-white font-semibold text-[11px] border border-[#8B0000] shadow-2xs whitespace-nowrap active';
        }} else {{
          b.className = 'chip-type px-3 py-1 rounded-full bg-white text-neutral-600 hover:text-[#8B0000] font-medium text-[11px] border border-neutral-200/80 whitespace-nowrap';
        }}
      }});
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      initCatalog();
      if (window.lucide) lucide.createIcons();
    }});
  </script>
</body>
</html>
"""

with open(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\catalog.html", "w", encoding="utf-8") as f:
    f.write(catalog_code)

print("[OK] Generated catalog.html exactly matching thenassty-cpu.github.io/siwasup-cobroker-os theme with increased Heritage Red and reduced black!")
