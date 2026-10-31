import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from overnight_r2_crawler import put_object_r2

BASE_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
INDEX_PATH = os.path.join(BASE_DIR, "index.html")
CATALOG_PATH = os.path.join(BASE_DIR, "catalog.html")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read().replace("\r\n", "\n")

NEW_HEADER_AND_BANNER = """    <!-- 🏛️ Top Header (Sticky, Ton's Master Crimson & White Logo Split Layout + Gold Agent Strip) -->
    <header class="sticky top-0 z-40 shadow-md w-full overflow-hidden">
      
      <!-- 1. Top Role Utility Bar: โทน Charcoal (#1D1D1D) + Active Red Pill -->
      <div class="bg-[#1D1D1D] text-neutral-300 text-xs py-1.5 px-2.5 sm:px-4 border-b border-neutral-800">
        <div class="max-w-7xl mx-auto flex items-center justify-between gap-1 sm:gap-2">
          
          <!-- ซ้าย: สลับโหมด -->
          <div class="flex items-center gap-1 sm:gap-1.5 shrink-0 z-10">
            <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 shrink-0"></span>
            
            <!-- Mobile Role Selector (< lg) -->
            <select 
              id="mobile-role-selector"
              onchange="setMode(this.value)" 
              class="lg:hidden bg-neutral-900 text-white font-semibold text-[11px] px-1.5 py-0.5 rounded-md border border-neutral-700 focus:outline-none shrink-0 min-w-[96px] max-w-[115px]"
            >
              <option value="owner">โหมด: Admin</option>
              <option value="free_agent" selected>โหมด: Free Agent</option>
              <option value="employee">โหมด: พนักงาน</option>
              <option value="trainee">โหมด: ฝึกหัด</option>
              <option value="client">โหมด: ลูกค้า VIP</option>
            </select>

            <!-- Desktop Role Indicator & Tabs (>= lg) -->
            <strong id="mode-text" class="hidden lg:inline text-white font-semibold text-[11px] whitespace-nowrap">Free Agent (คอม 3-5% อิสระ)</strong>
            <div class="hidden lg:flex items-center bg-[#141414] p-0.5 rounded-lg border border-neutral-800 text-[11px] ml-1">
              <button id="btn-owner-mode" onclick="setMode('owner')" class="px-2.5 py-0.5 rounded-md text-neutral-400 hover:text-white transition" title="โหมดแอดมิน">Admin</button>
              <button id="btn-freeagent-mode" onclick="setMode('free_agent')" class="px-2.5 py-0.5 rounded-md bg-[#B51218] text-white font-semibold shadow-2xs" title="โหมด Free Agent">Free</button>
              <button id="btn-employee-mode" onclick="setMode('employee')" class="px-2.5 py-0.5 rounded-md text-neutral-400 hover:text-white transition" title="โหมดพนักงานประจำ">พนักงาน</button>
              <button id="btn-trainee-mode" onclick="setMode('trainee')" class="px-2.5 py-0.5 rounded-md text-neutral-400 hover:text-white transition" title="โหมดฝึกหัด">ฝึกหัด</button>
              <button id="btn-client-mode" onclick="setMode('client')" class="px-2.5 py-0.5 rounded-md text-neutral-400 hover:text-white transition" title="โหมดลูกค้า White-label">ลูกค้า</button>
            </div>
          </div>

          <!-- ขวา: เมนูเครื่องมือ -->
          <div id="header-right-tools" class="flex items-center gap-1 sm:gap-1.5 shrink-0 text-[11px] overflow-x-auto no-scrollbar">
            <!-- กระดิ่งแจ้งเตือนทรัพย์ฝากขายใหม่ (Owner) -->
            <button id="btn-owner-leads-notify" onclick="openOwnerLeadsModal()" class="hidden h-6 px-1.5 sm:px-2.5 rounded-md bg-neutral-900 hover:bg-neutral-800 border border-neutral-800 text-neutral-300 items-center gap-1 transition cursor-pointer active:scale-95 shrink-0" title="ดูรายการทรัพย์ฝากขายใหม่">
              <span class="w-1.5 h-1.5 rounded-full bg-rose-500 shrink-0"></span>
              <span class="hidden sm:inline">ฝากขาย</span>
              <span class="text-[10px] font-mono text-rose-300">(<span id="consign-count-badge">1</span>)</span>
            </button>

            <!-- แอดมินจัดกลุ่มสัตว์ 4 กลุ่ม -->
            <button id="btn-owner-archetype-shortcut" type="button" onclick="openAgentLeaderboardModal('animal_matrix')" class="h-6 px-1.5 sm:px-2 rounded-md bg-neutral-900 hover:bg-neutral-800 border border-neutral-800 text-neutral-300 flex items-center gap-1 transition cursor-pointer active:scale-95 shrink-0" title="วิเคราะห์ศักยภาพตัวแทน 4 กลุ่มสัตว์ (Animal Matrix)">
              <img src="assets/characters/badge_eagle.png" alt="Matrix" class="w-3.5 h-3.5 object-contain">
              <span class="hidden sm:inline">4 สาย</span>
            </button>

            <!-- ปุ่มกุญแจ NPA -->
            <button id="btn-header-npa-key" type="button" onclick="openNpaKeyModal()" class="h-6 px-1.5 sm:px-2 rounded-md bg-neutral-900 hover:bg-neutral-800 border border-neutral-800 text-neutral-300 flex items-center gap-1 transition cursor-pointer active:scale-95 shrink-0" title="ระบบเบิกกุญแจ NPA & Messenger">
              <span class="text-[#D4BC8B]">🔑</span>
              <span class="hidden md:inline">กุญแจ</span>
            </button>

            <!-- ทำเนียบตัวแทน 125 -->
            <button id="btn-header-leaderboard" type="button" onclick="openAgentLeaderboardModal()" class="h-6 px-1.5 sm:px-2 rounded-md bg-neutral-900 hover:bg-neutral-800 border border-neutral-800 text-[#E5C985] font-semibold flex items-center gap-1 transition cursor-pointer active:scale-95 shrink-0" title="ทำเนียบตัวแทน 125 ท่าน">
              <span>♛</span>
              <span>125</span>
            </button>

            <!-- โปรไฟล์ตัวแทน -->
            <button type="button" onclick="openMyProfileModal()" id="btn-header-profile" class="h-6 pl-1 pr-1.5 sm:pr-2.5 rounded-md bg-neutral-900 hover:bg-neutral-800 border border-neutral-800 text-neutral-200 flex items-center gap-1 sm:gap-1.5 transition cursor-pointer active:scale-95 shrink-0" title="กระเป๋าคะแนน & โปรไฟล์">
              <img id="header-profile-3d-badge" src="assets/characters/badge_eagle.png" alt="Badge" class="w-3.5 h-3.5 object-contain">
              <span class="px-1 py-0.2 rounded bg-[#C2A460]/20 text-[#E5C985] text-[9px] font-bold" id="header-profile-avatar">S22</span>
              <span id="bar-profile-btn-text" class="hidden sm:inline font-medium">เจ็ม</span>
            </button>
          </div>

        </div>
      </div>

      <!-- 2. Main Header Split Layout: กล่องโลโก้พื้นสีขาวซ้าย (#FFFFFF) + พื้นแดงเลือดหมูขวา (#900D11 -> #59080A) -->
      <div class="flex items-stretch bg-gradient-to-r from-[#900D11] via-[#740A0D] to-[#59080A] w-full overflow-hidden">
        
        <!-- ฝั่งซ้ายสุด: กล่องโลโก้พื้นสีขาว (#FFFFFF) เต็มความสูงแบนเนอร์ -->
        <a href="welcome_landing.html" class="bg-white px-2.5 sm:px-4 lg:px-5 py-2 flex items-center justify-center shrink-0 group transition-all" title="กลับสู่หน้าต้อนรับ">
          <img 
            src="assets/siwasup_logo.svg" 
            alt="ศิวาทรัพย์ แอสเซท" 
            class="h-11 sm:h-14 lg:h-[76px] w-auto object-contain group-hover:scale-105 transition-transform duration-200"
            onerror="this.onerror=null; this.src='assets/icons/icon-512.png';"
          >
        </a>

        <!-- ฝั่งขวา: พื้นแดงเลือดหมู แบ่ง 2 แถว (แถวบน: ชื่อแบรนด์ + แคปซูลค้นหาสีขาว + ปุ่มฝากขายทอง / แถวล่าง: กรองด่วน) -->
        <div class="flex-1 min-w-0 px-2.5 sm:px-5 py-2 sm:py-2.5 flex flex-col justify-center gap-2 overflow-hidden">
          
          <!-- แถวที่ 1: ชื่อแบรนด์ + แคปซูลค้นหา + ปุ่มฝากขาย -->
          <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-2 sm:gap-3 min-w-0">
            
            <!-- ชื่อแบรนด์ ศิวาทรัพย์ แอสเซท + ปุ่มฝากขายบนมือถือ -->
            <div class="flex items-center justify-between lg:justify-start gap-1.5 sm:gap-2 min-w-0">
              <div class="min-w-0 truncate">
                <div class="flex items-center gap-1.5 sm:gap-2">
                  <span class="font-extrabold text-[15px] sm:text-lg lg:text-xl tracking-tight whitespace-nowrap leading-tight">
                    <span class="text-[#DEC084]">ศิวาทรัพย์</span><span class="text-white">แอสเซท</span>
                  </span>
                  <span class="hidden sm:inline-block text-[9px] sm:text-[10px] font-bold px-2 py-0.5 rounded-full bg-[#FAF6EE] text-[#7A5C29] shadow-2xs whitespace-nowrap shrink-0">
                    NPA & ทรัพย์คัดสรร
                  </span>
                </div>
                <p class="hidden sm:block text-[11px] lg:text-xs text-white/90 font-normal tracking-normal whitespace-nowrap mt-0.5">
                  ศูนย์รวมทรัพย์ NPA และบ้านรีโนเวทคุณภาพมาตรฐาน
                </p>
              </div>

              <!-- ปุ่มฝากขายบนมือถือ (< lg) ใช้ Lucide Tag Icon -->
              <button onclick="openConsignModal()" class="lg:hidden px-2.5 py-1 rounded-full bg-[#C0A366] hover:bg-[#B09255] text-white text-[10px] sm:text-[11px] font-bold flex items-center gap-1 shadow-sm shrink-0 whitespace-nowrap transition-transform active:scale-95">
                <i data-lucide="tag" class="w-3.5 h-3.5 stroke-[2] text-white shrink-0"></i>
                <span>ฝากขายฟรี</span>
              </button>
            </div>

            <!-- กลาง: Unified White Pill Search -->
            <div class="flex-1 w-full lg:max-w-3xl min-w-0">
              <!-- Mobile Compact Search Pill (< lg) -->
              <button 
                type="button"
                id="search-mini-bar"
                onclick="toggleMobileSearchDrawer()"
                class="lg:hidden w-full h-8 sm:h-9 px-3 rounded-full bg-white hover:bg-neutral-50 flex items-center justify-between gap-1.5 text-xs text-neutral-600 shadow-sm transition-all active:scale-[0.99] min-w-0"
              >
                <span class="flex items-center gap-1.5 truncate min-w-0">
                  <span class="text-neutral-800 shrink-0 text-[11px]">🔍</span>
                  <span id="search-mini-summary" class="truncate font-semibold text-neutral-800 text-[11px]">ค้นหาทำเล, ธนาคาร, งบประมาณ...</span>
                </span>
                <span id="mobile-filter-pill-badge" class="px-2 py-0.5 rounded-full bg-neutral-100 text-neutral-800 text-[10px] font-bold border border-neutral-200 shrink-0 whitespace-nowrap">
                  ตัวกรอง ▾
                </span>
              </button>

              <!-- Full Filter Box (ทรงแคปซูลสีขาวตามภาพต้นแบบ) -->
              <div id="search-filter-drawer" class="hidden lg:block bg-white rounded-2xl lg:rounded-full p-2.5 lg:py-1.5 lg:px-3 shadow-md transition-all">
                <div class="grid grid-cols-2 lg:grid-cols-[1.3fr_1fr_1fr_1fr_1fr_auto] items-center gap-1.5 lg:gap-0" id="search-pill-grid">
                  
                  <!-- ช่องที่ 1: ค้นหาทรัพย์ -->
                  <div class="col-span-2 lg:col-span-1 px-3 py-0.5 relative">
                    <label class="block text-[9px] font-semibold text-neutral-400 uppercase tracking-wider">ค้นหาทรัพย์</label>
                    <div class="flex items-center">
                      <input type="text" id="search-input" oninput="applyAllFilters()" 
                             placeholder="ชื่อโครงการ, รหัส NPA..." 
                             class="w-full bg-transparent text-xs font-medium text-neutral-800 placeholder-neutral-400 focus:outline-none truncate pr-5" />
                      <button id="btn-clear-search" onclick="clearFilters()" class="hidden text-neutral-400 hover:text-neutral-600 text-sm font-bold leading-none pr-1">&times;</button>
                    </div>
                  </div>

                  <!-- ช่องที่ 2: ประเภท -->
                  <div id="filter-category-wrapper" class="px-3 py-0.5 lg:border-l border-neutral-200/80">
                    <label class="block text-[9px] font-semibold text-neutral-400 uppercase tracking-wider">ประเภท</label>
                    <select id="filter-category" onchange="syncCategoryToChips(this.value); applyAllFilters()" class="w-full bg-transparent text-xs font-bold text-neutral-900 focus:outline-none cursor-pointer truncate">
                      <option value="all">ทุกประเภท</option>
                      <option value="ทาวน์โฮม">ทาวน์โฮม</option>
                      <option value="คอนโด">คอนโด</option>
                      <option value="บ้านเดี่ยว">บ้านเดี่ยว</option>
                      <option value="ที่ดิน">ที่ดิน</option>
                      <option value="อาคารพาณิชย์">อาคารพาณิชย์</option>
                    </select>
                  </div>

                  <!-- ช่องที่ 3: สถาบัน/เจ้าของ -->
                  <div id="filter-bank-wrapper" class="px-3 py-0.5 lg:border-l border-neutral-200/80">
                    <label class="block text-[9px] font-semibold text-neutral-400 uppercase tracking-wider">สถาบัน/เจ้าของ</label>
                    <select id="filter-bank" onchange="syncBankToChips(this.value); applyAllFilters()" class="w-full bg-transparent text-xs font-bold text-neutral-900 focus:outline-none cursor-pointer truncate">
                      <option value="all">ทุกธนาคาร</option>
                      <option value="Siwasup">ศิวาทรัพย์ รีโนเวท</option>
                      <option value="SAM">SAM</option>
                      <option value="SCB">SCB</option>
                      <option value="KBANK">KBank</option>
                      <option value="TTB">TTB</option>
                      <option value="KTB">KTB</option>
                      <option value="GSB">GSB</option>
                      <option value="PAMCO">PAMCO</option>
                    </select>
                  </div>

                  <!-- ช่องที่ 4: โซนทำเล -->
                  <div class="px-3 py-0.5 lg:border-l border-neutral-200/80">
                    <label class="block text-[9px] font-semibold text-neutral-400 uppercase tracking-wider">โซนทำเล</label>
                    <select id="filter-location" onchange="applyAllFilters()" class="w-full bg-transparent text-xs font-bold text-neutral-900 focus:outline-none cursor-pointer truncate">
                      <option value="all">ทุกทำเล</option>
                      <option value="บางใหญ่">บางใหญ่/นนทบุรี</option>
                      <option value="ลำลูกกา">ลำลูกกา/ปทุมธานี</option>
                      <option value="พระราม 9">รัชดา/พระราม 9</option>
                      <option value="บางนา">บางนา/สมุทรปราการ</option>
                      <option value="วิภาวดี">วิภาวดี/รัชโยธิน</option>
                      <option value="ลาดกระบัง">ลาดกระบัง/สุวินทวงศ์</option>
                      <option value="บางขุนเทียน">พระราม 2/บางขุนเทียน</option>
                    </select>
                  </div>

                  <!-- ช่องที่ 5: งบประมาณ -->
                  <div class="col-span-2 lg:col-span-1 px-3 py-0.5 lg:border-l border-neutral-200/80">
                    <label class="block text-[9px] font-semibold text-neutral-400 uppercase tracking-wider">งบประมาณ</label>
                    <select id="filter-budget" onchange="applyAllFilters()" class="w-full bg-transparent text-xs font-bold text-neutral-900 focus:outline-none cursor-pointer truncate">
                      <option value="all">ทุกช่วงราคา</option>
                      <option value="under2m">ต่ำกว่า 2 ล้าน</option>
                      <option value="2to3.5m">2 - 3.5 ล้าน</option>
                      <option value="3.5to5m">3.5 - 5 ล้าน</option>
                      <option value="above5m">5 ล้านขึ้นไป</option>
                    </select>
                  </div>

                  <!-- ช่องที่ 6: ปุ่มค้นหาสีดำกลม -->
                  <div class="col-span-2 lg:col-span-1 flex justify-end p-0.5">
                    <button 
                      onclick="applyAllFilters(); toggleMobileSearchDrawer(false);" 
                      class="w-full lg:w-8 h-8 rounded-xl lg:rounded-full bg-[#1D1D1D] hover:bg-neutral-800 text-white text-xs font-semibold flex items-center justify-center gap-1.5 transition active:scale-95 shadow-xs cursor-pointer ml-1" 
                      title="ค้นหา"
                    >
                      <svg xmlns="http://www.w3.org/2000/svg" class="h-3.5 w-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.2">
                        <path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                      </svg>
                      <span class="lg:hidden text-xs">ค้นหาและพับเก็บ</span>
                    </button>
                  </div>

                </div>
              </div>
            </div>

            <!-- ขวา: ปุ่มฝากขายฟรีสำหรับ Desktop (>= lg) ใช้ Lucide Tag Icon -->
            <button onclick="openConsignModal()" class="hidden lg:flex px-4 py-2 rounded-full bg-[#C0A366] hover:bg-[#B09255] text-white text-xs font-bold items-center gap-1.5 shadow-sm transition shrink-0 cursor-pointer active:scale-95">
              <i data-lucide="tag" class="w-4 h-4 stroke-[2] text-white shrink-0"></i>
              <span>ฝากขายฟรี</span>
            </button>

          </div>

          <!-- แถวที่ 2: แถบกรองด่วนธนาคาร (อยู่บนพื้นแดง ปุ่มขาว ตัวหนังสือเข้ม ปุ่มที่เลือกเป็นสีดำ) -->
          <div id="quick-chips-bar" class="flex items-center gap-1.5 sm:gap-2 overflow-x-auto no-scrollbar pt-0.5 min-w-0">
            <span class="text-xs font-bold text-[#DEC084] shrink-0 mr-1 hidden sm:inline">กรองด่วน:</span>
            <div id="bank-quick-chips" class="flex items-center gap-1.5 shrink-0">
              <button type="button" onclick="selectBankChip('all', this)" class="bank-chip active h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-[#1D1D1D] text-white shadow-sm shrink-0 inline-flex items-center">ทั้งหมด</button>
              <button type="button" onclick="selectBankChip('Siwasup', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-[#8C734B] hover:bg-[#FAF7F2] shadow-xs flex items-center gap-1 shrink-0 inline-flex items-center">
                <span>✦</span>
                <span>ศิวาทรัพย์ รีโนเวท</span>
              </button>
              <button type="button" onclick="selectBankChip('SAM', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-neutral-800 hover:bg-neutral-100 shadow-xs shrink-0 inline-flex items-center">SAM</button>
              <button type="button" onclick="selectBankChip('SCB', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-neutral-800 hover:bg-neutral-100 shadow-xs shrink-0 inline-flex items-center">SCB</button>
              <button type="button" onclick="selectBankChip('KBANK', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-neutral-800 hover:bg-neutral-100 shadow-xs shrink-0 inline-flex items-center">KBank</button>
              <button type="button" onclick="selectBankChip('TTB', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-neutral-800 hover:bg-neutral-100 shadow-xs shrink-0 inline-flex items-center">TTB</button>
              <button type="button" onclick="selectBankChip('KTB', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-neutral-800 hover:bg-neutral-100 shadow-xs shrink-0 inline-flex items-center">KTB</button>
              <button type="button" onclick="selectBankChip('GSB', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-neutral-800 hover:bg-neutral-100 shadow-xs shrink-0 inline-flex items-center">GSB</button>
              <button type="button" onclick="selectBankChip('PAMCO', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-neutral-800 hover:bg-neutral-100 shadow-xs shrink-0 inline-flex items-center">PAMCO</button>
            </div>
          </div>

        </div>
      </div>

      <!-- 3. แถบสีทองด้านล่างส่วนหัว (Satin Gold Agent Bar #C0A366 ตามภาพต้นแบบ) -->
      <div id="client-top-trust-banner" class="bg-[#C0A366] text-white px-3 sm:px-5 py-1.5 transition-all text-xs shrink-0 border-t border-[#965920]/40">
        <div class="max-w-7xl mx-auto flex items-center justify-between gap-2">
          <div class="flex items-center gap-2 min-w-0 overflow-x-auto no-scrollbar">
            <!-- ดาว 4 แฉกสีเหลืองทอง -->
            <svg class="w-4 h-4 text-[#FFE84D] fill-current shrink-0" viewBox="0 0 24 24">
              <path d="M12 1.5L14.6 9.4L22.5 12L14.6 14.6L12 22.5L9.4 14.6L1.5 12L9.4 9.4L12 1.5Z"/>
            </svg>
            <span class="text-white font-medium text-[11px] sm:text-xs whitespace-nowrap shrink-0">ดูแลการเข้าชมโดย</span>
            
            <!-- แคปซูลสีครีมขาว แสดงชื่อตัวแทน | รหัส -->
            <div class="inline-flex items-center gap-1.5 px-3 py-0.5 rounded-full bg-[#FAF7F2] shadow-2xs shrink-0">
              <span id="client-banner-agent-name" class="text-[#8C6D2E] font-extrabold text-xs sm:text-[13px] whitespace-nowrap">คุณณัฐ ระวังภัย</span>
              <span class="text-[#C0A366]/70 font-light">|</span>
              <span id="client-banner-agent-id" class="text-neutral-500 font-semibold text-[10px] sm:text-[11px] whitespace-nowrap">(ID: AG-09)</span>
            </div>

            <span class="hidden sm:inline text-white/95 font-medium text-[11px] sm:text-xs whitespace-nowrap">• ที่ปรึกษาอสังหาริมทรัพย์รับรองโดย ศิวาทรัพย์</span>
          </div>
        </div>
      </div>
    </header>"""

h_start = html.find("    <!-- 🏛️ Top Header")
# Replace up to the end of the old client-top-trust-banner div so we don't have duplicate banners!
b_end_marker = "    <!-- 💎 3. Contextual Banners (Compact & Clean) -->"
b_end = html.find(b_end_marker)
assert h_start != -1 and b_end > h_start, "Could not locate header and trust banner bounds"

html = html[:h_start] + NEW_HEADER_AND_BANNER + "\n\n" + html[b_end:]

# Also ensure setMode() does NOT hide #client-top-trust-banner in non-client modes, and updates the agent name/ID nicely!
old_hide_banner = "if (topBanner) topBanner.classList.add('hidden');"
new_keep_banner = """if (topBanner) {
          topBanner.classList.remove('hidden');
          const storedRef = (typeof getStoredAgentRef === 'function') ? getStoredAgentRef() : (localStorage.getItem('siwasup_referred_by') || 'AG-09');
          const agentProfile = (typeof getAgentProfile === 'function') ? getAgentProfile(storedRef) : null;
          const bName = document.getElementById('client-banner-agent-name');
          const bId = document.getElementById('client-banner-agent-id');
          if (agentProfile) {
            if (bName) bName.textContent = agentProfile.name;
            if (bId) bId.textContent = `(ID: ${agentProfile.agentId})`;
          }
        }"""

if old_hide_banner in html:
    html = html.replace(old_hide_banner, new_keep_banner)
    print("Updated setMode() to keep gold agent strip visible across all modes.")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)
with open(CATALOG_PATH, "w", encoding="utf-8") as f:
    f.write(html)

for fname in ["index.html", "catalog.html"]:
    status = put_object_r2(fname, html.encode("utf-8"), "text/html; charset=utf-8")
    print(f"Uploaded {fname} to Cloudflare R2 (status={status})")
