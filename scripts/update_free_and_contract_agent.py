import os

ROOT = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"

# ==============================================================================
# 1. UPDATE admin_lobby_manager.html
# ==============================================================================
lobby_path = os.path.join(ROOT, "admin_lobby_manager.html")
with open(lobby_path, "r", encoding="utf-8") as f:
    lobby_html = f.read()

# 1A. Replace Drag & Drop Role Station (7 boxes -> 8 boxes with Contract Agent #ffa8B6 & Free Agent #786ea1)
old_drop_station = """      <!-- ============================================================== -->
      <!-- DRAG & DROP ROLE STATION (กล่องรับการลากวาง 7 กล่อง) -->
      <!-- ============================================================== -->
      <div class="pt-2 border-t border-slate-200 space-y-2.5">
        <div class="flex items-center justify-between">
          <label class="text-xs font-bold text-slate-800 flex items-center gap-1.5">
            <i data-lucide="mouse-pointer-click" class="w-4 h-4 text-[#ed1c24]"></i>
            <span>แท่นลากวางแต่งตั้งบทบาท (Drag & Drop Role Station)</span>
          </label>
          <span class="text-[10px] text-slate-400">ลากการ์ดมาปล่อยลงในช่องที่ต้องการ</span>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2.5 text-xs">

          <!-- Drop Zone 1: Gool -->
          <div class="drop-zone p-3 rounded-2xl bg-amber-50/50 hover:bg-amber-50 border-2 border-dashed border-amber-300 text-center space-y-1"
               ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event, 'gool')">
            <div class="text-base">👑</div>
            <div class="font-bold text-amber-900 leading-tight">เจี๊ยบ(กูล)</div>
            <div class="text-[9px] text-amber-700">CEO / เคาะราคา</div>
            <div class="text-[8px] text-slate-400 pt-0.5">ปล่อยเพื่อแต่งตั้ง</div>
          </div>

          <!-- Drop Zone 2: Bua -->
          <div class="drop-zone p-3 rounded-2xl bg-amber-50/50 hover:bg-amber-50 border-2 border-dashed border-amber-300 text-center space-y-1"
               ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event, 'bua')">
            <div class="text-base">👑</div>
            <div class="font-bold text-amber-900 leading-tight">คุณบัว</div>
            <div class="text-[9px] text-amber-700">แทนเจี๊ยบ 100%</div>
            <div class="text-[8px] text-slate-400 pt-0.5">ปล่อยเพื่อแต่งตั้ง</div>
          </div>

          <!-- Drop Zone 3: Lily -->
          <div class="drop-zone p-3 rounded-2xl bg-emerald-50/50 hover:bg-emerald-50 border-2 border-dashed border-emerald-300 text-center space-y-1"
               ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event, 'lily')">
            <div class="text-base">🔑</div>
            <div class="font-bold text-emerald-900 leading-tight">พี่ลิลลี่</div>
            <div class="text-[9px] text-emerald-700">คุมกุญแจ OTP</div>
            <div class="text-[8px] text-slate-400 pt-0.5">ปล่อยเพื่อแต่งตั้ง</div>
          </div>

          <!-- Drop Zone 4: Ton -->
          <div class="drop-zone p-3 rounded-2xl bg-rose-50/50 hover:bg-rose-50 border-2 border-dashed border-rose-300 text-center space-y-1"
               ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event, 'ton')">
            <div class="text-base">💻</div>
            <div class="font-bold text-rose-900 leading-tight">คุณต้น</div>
            <div class="text-[9px] text-rose-700">Tech Architect</div>
            <div class="text-[8px] text-slate-400 pt-0.5">ปล่อยเพื่อแต่งตั้ง</div>
          </div>

          <!-- Drop Zone 5: Support -->
          <div class="drop-zone p-3 rounded-2xl bg-blue-50/50 hover:bg-blue-50 border-2 border-dashed border-blue-300 text-center space-y-1"
               ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event, 'support')">
            <div class="text-base">🏢</div>
            <div class="font-bold text-blue-900 leading-tight">ซัพพอร์ต</div>
            <div class="text-[9px] text-blue-700">Standard Admin</div>
            <div class="text-[8px] text-slate-400 pt-0.5">ปล่อยเพื่อแต่งตั้ง</div>
          </div>

          <!-- Drop Zone 6: Co-Broker -->
          <div class="drop-zone p-3 rounded-2xl bg-emerald-50/50 hover:bg-emerald-50 border-2 border-dashed border-emerald-400 text-center space-y-1"
               ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event, 'agent')">
            <div class="text-base">🤝</div>
            <div class="font-bold text-emerald-900 leading-tight">Co-Broker</div>
            <div class="text-[9px] text-emerald-700">พันธมิตรรับรอง</div>
            <div class="text-[8px] text-slate-400 pt-0.5">ปล่อยเพื่อแต่งตั้ง</div>
          </div>

          <!-- Drop Zone 7: Reject Trash -->
          <div class="drop-zone p-3 rounded-2xl bg-red-50/50 hover:bg-red-50 border-2 border-dashed border-red-300 text-center space-y-1"
               ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event, 'reject')">
            <div class="text-base">🗑️</div>
            <div class="font-bold text-red-900 leading-tight">ดีดออก</div>
            <div class="text-[9px] text-red-600">ปฏิเสธใบสมัคร</div>
            <div class="text-[8px] text-slate-400 pt-0.5">ปล่อยเพื่อดีดทิ้ง</div>
          </div>

        </div>
      </div>"""

new_drop_station = """      <!-- ============================================================== -->
      <!-- DRAG & DROP ROLE STATION (กล่องรับการลากวาง 8 กล่อง) -->
      <!-- ============================================================== -->
      <div class="pt-2 border-t border-slate-200 space-y-2.5">
        <div class="flex items-center justify-between">
          <label class="text-xs font-bold text-slate-800 flex items-center gap-1.5">
            <i data-lucide="mouse-pointer-click" class="w-4 h-4 text-[#ed1c24]"></i>
            <span>แท่นลากวางแต่งตั้งบทบาท (Drag & Drop Role Station)</span>
          </label>
          <span class="text-[10px] text-slate-400">ลากการ์ดมาปล่อยลงในช่องที่ต้องการ</span>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2 text-xs">

          <!-- Drop Zone 1: Gool -->
          <div class="drop-zone p-3 rounded-2xl bg-amber-50/50 hover:bg-amber-50 border-2 border-dashed border-amber-300 text-center space-y-1"
               ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event, 'gool')">
            <div class="text-base">👑</div>
            <div class="font-bold text-amber-900 leading-tight">เจี๊ยบ(กูล)</div>
            <div class="text-[9px] text-amber-700">CEO / เคาะราคา</div>
            <div class="text-[8px] text-slate-400 pt-0.5">ปล่อยเพื่อแต่งตั้ง</div>
          </div>

          <!-- Drop Zone 2: Bua -->
          <div class="drop-zone p-3 rounded-2xl bg-amber-50/50 hover:bg-amber-50 border-2 border-dashed border-amber-300 text-center space-y-1"
               ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event, 'bua')">
            <div class="text-base">👑</div>
            <div class="font-bold text-amber-900 leading-tight">คุณบัว</div>
            <div class="text-[9px] text-amber-700">แทนเจี๊ยบ 100%</div>
            <div class="text-[8px] text-slate-400 pt-0.5">ปล่อยเพื่อแต่งตั้ง</div>
          </div>

          <!-- Drop Zone 3: Lily -->
          <div class="drop-zone p-3 rounded-2xl bg-emerald-50/50 hover:bg-emerald-50 border-2 border-dashed border-emerald-300 text-center space-y-1"
               ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event, 'lily')">
            <div class="text-base">🔑</div>
            <div class="font-bold text-emerald-900 leading-tight">พี่ลิลลี่</div>
            <div class="text-[9px] text-emerald-700">คุมกุญแจ OTP</div>
            <div class="text-[8px] text-slate-400 pt-0.5">ปล่อยเพื่อแต่งตั้ง</div>
          </div>

          <!-- Drop Zone 4: Ton -->
          <div class="drop-zone p-3 rounded-2xl bg-rose-50/50 hover:bg-rose-50 border-2 border-dashed border-rose-300 text-center space-y-1"
               ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event, 'ton')">
            <div class="text-base">💻</div>
            <div class="font-bold text-rose-900 leading-tight">คุณต้น</div>
            <div class="text-[9px] text-rose-700">Tech Architect</div>
            <div class="text-[8px] text-slate-400 pt-0.5">ปล่อยเพื่อแต่งตั้ง</div>
          </div>

          <!-- Drop Zone 5: Support -->
          <div class="drop-zone p-3 rounded-2xl bg-blue-50/50 hover:bg-blue-50 border-2 border-dashed border-blue-300 text-center space-y-1"
               ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event, 'support')">
            <div class="text-base">🏢</div>
            <div class="font-bold text-blue-900 leading-tight">ซัพพอร์ต</div>
            <div class="text-[9px] text-blue-700">Standard Admin</div>
            <div class="text-[8px] text-slate-400 pt-0.5">ปล่อยเพื่อแต่งตั้ง</div>
          </div>

          <!-- Drop Zone 6: Contract Agent (Pink Sand #ffa8B6) -->
          <div class="drop-zone p-3 rounded-2xl bg-[#ffa8b6]/20 hover:bg-[#ffa8b6]/35 border-2 border-dashed border-[#ffa8b6] text-center space-y-1"
               ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event, 'contract_agent')">
            <div class="text-base">📑</div>
            <div class="font-bold text-[#9e3b4f] leading-tight">Contract Agent</div>
            <div class="text-[9px] text-[#b84a60] font-semibold">ตัวแทนสัญญาสังกัด</div>
            <div class="text-[8px] text-slate-400 pt-0.5">ปล่อยเพื่อแต่งตั้ง</div>
          </div>

          <!-- Drop Zone 7: Free Agent (Kimberly #786ea1) -->
          <div class="drop-zone p-3 rounded-2xl bg-[#786ea1]/15 hover:bg-[#786ea1]/25 border-2 border-dashed border-[#786ea1] text-center space-y-1"
               ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event, 'free_agent')">
            <div class="text-base">🤝</div>
            <div class="font-bold text-[#4a4269] leading-tight">Free Agent</div>
            <div class="text-[9px] text-[#5e5485] font-semibold">ตัวแทนอิสระ</div>
            <div class="text-[8px] text-slate-400 pt-0.5">ปล่อยเพื่อแต่งตั้ง</div>
          </div>

          <!-- Drop Zone 8: Reject Trash -->
          <div class="drop-zone p-3 rounded-2xl bg-red-50/50 hover:bg-red-50 border-2 border-dashed border-red-300 text-center space-y-1"
               ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event, 'reject')">
            <div class="text-base">🗑️</div>
            <div class="font-bold text-red-900 leading-tight">ดีดออก</div>
            <div class="text-[9px] text-red-600">ปฏิเสธใบสมัคร</div>
            <div class="text-[8px] text-slate-400 pt-0.5">ปล่อยเพื่อดีดทิ้ง</div>
          </div>

        </div>
      </div>"""

assert old_drop_station in lobby_html, "old_drop_station not found"
lobby_html = lobby_html.replace(old_drop_station, new_drop_station, 1)

# 1B. Replace Filter Buttons
old_filter_btns = """          <button onclick="setRosterFilter('agent')" id="filterBtn_agent" 
                  class="roster-filter-btn px-3 py-1.5 rounded-xl text-xs font-semibold transition bg-slate-100 text-slate-600 hover:bg-slate-200">
            🤝 Co-Broker (<span id="count_agent">0</span>)
          </button>"""

new_filter_btns = """          <button onclick="setRosterFilter('contract_agent')" id="filterBtn_contract_agent" 
                  class="roster-filter-btn px-3 py-1.5 rounded-xl text-xs font-semibold transition bg-slate-100 text-slate-600 hover:bg-slate-200">
            📑 Contract Agent (<span id="count_contract_agent">0</span>)
          </button>

          <button onclick="setRosterFilter('free_agent')" id="filterBtn_free_agent" 
                  class="roster-filter-btn px-3 py-1.5 rounded-xl text-xs font-semibold transition bg-slate-100 text-slate-600 hover:bg-slate-200">
            🤝 Free Agent (<span id="count_free_agent">0</span>)
          </button>"""

assert old_filter_btns in lobby_html, "old_filter_btns not found"
lobby_html = lobby_html.replace(old_filter_btns, new_filter_btns, 1)

# 1C. Add Contract Agent badge to Draggable Badges Palette
old_palette_start = """        <!-- Draggable Badges Palette -->
        <div class="flex items-center gap-1.5 sm:gap-2 flex-wrap pt-1.5 border-t border-slate-700/60">
          <span class="text-[10px] text-slate-400 font-semibold mr-1">🖐️ สิทธิ์ที่พร้อมลากมอบ:</span>"""

new_palette_start = """        <!-- Draggable Badges Palette -->
        <div class="flex items-center gap-1.5 sm:gap-2 flex-wrap pt-1.5 border-t border-slate-700/60">
          <span class="text-[10px] text-slate-400 font-semibold mr-1">🖐️ สิทธิ์ที่พร้อมลากมอบ:</span>

          <div draggable="true" ondragstart="handleBadgePaletteDragStart(event, '📑 สัญญาสังกัดทางการ')" 
               class="cursor-grab active:cursor-grabbing px-2.5 py-1 rounded-xl text-[#6e1d2c] border-2 font-bold text-[11px] shadow-sm hover:scale-105 transition flex items-center gap-1 select-none"
               style="background-color: #ffa8b6; border-color: #e58e9c;">
            <span>📑 สัญญาสังกัดทางการ (Contract Agent)</span>
          </div>"""

assert old_palette_start in lobby_html, "old_palette_start not found"
lobby_html = lobby_html.replace(old_palette_start, new_palette_start, 1)

# 1D. Update ROLE_PRESETS, getRoleTierBadge, filter logic
old_presets_and_filter = """      support: {
        role: "🏢 เจ้าหน้าที่ซัพพอร์ตออฟฟิศ",
        title: "Office Property Coordinator",
        badges: ["🛡️ Standard Admin", "🏷️ ช่วยคัดสต๊อก", "🚫 ล็อกแก้ราคา"],
        permissions: { standardAdmin: true, editPrice: false, keyboxAdmin: false, leadInspector: false, executiveAuthority: false, catalogCurator: true, systemAdmin: false }
      },
      agent: {
        role: "🤝 Co-Broker พันธมิตรทางการ",
        title: "Certified Co-Broker Partner",
        badges: ["📜 บัตรดิจิทัลทางการ", "🔒 ล็อกค่านายหน้า 60 วัน", "📅 จองเปิดบ้าน", "🚫 ล็อกแอดมิน"],
        permissions: { standardAdmin: false, editPrice: false, keyboxAdmin: false, leadInspector: false, executiveAuthority: false, catalogCurator: false, systemAdmin: false }
      }
    };

    
    function getRoleTierBadge(item) {
      const role = (item.role || "").toLowerCase();
      const perms = item.permissions || {};
      if (perms.systemAdmin || role.includes("tech") || role.includes("ต้น")) {
        return `<span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-rose-100 text-rose-800 border border-rose-300 shadow-2xs">💻 SUPER TECH</span>`;
      }
      if (role.includes("ceo") || role.includes("partner") || role.includes("กูล") || role.includes("บัว") || perms.executiveAuthority) {
        return `<span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-gradient-to-r from-amber-100 to-red-100 text-amber-900 border border-amber-400 shadow-2xs">👑 SUPREME EXEC</span>`;
      }
      if (perms.keyboxAdmin || role.includes("viewing") || role.includes("กุญแจ") || role.includes("ลิลลี่")) {
        return `<span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-emerald-100 text-emerald-800 border border-emerald-400 shadow-2xs">🔑 KEYBOX MASTER</span>`;
      }
      if (perms.standardAdmin) {
        return `<span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-blue-100 text-blue-800 border border-blue-300 shadow-2xs">🏢 OFFICE ADMIN</span>`;
      }
      return `<span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-slate-100 text-slate-700 border border-slate-300 shadow-2xs">🤝 CO-BROKER</span>`;
    }

    let currentRosterViewMode = 'cards';
    let currentRosterFilter = 'all'; // 'all' | 'admin' | 'agent'
    let currentRosterSort = 'tier';   // 'tier' | 'name' | 'zone' | 'newest'
    let currentRosterSearch = '';

    function setRosterFilter(filter) {
      currentRosterFilter = filter;
      ['all', 'admin', 'agent'].forEach(k => {
        const btn = document.getElementById('filterBtn_' + k);
        if (!btn) return;
        if (k === filter) {
          btn.className = "roster-filter-btn px-3 py-1.5 rounded-xl text-xs font-bold transition shadow-2xs bg-slate-900 text-white";
        } else {
          btn.className = "roster-filter-btn px-3 py-1.5 rounded-xl text-xs font-semibold transition bg-slate-100 text-slate-600 hover:bg-slate-200";
        }
      });
      renderApprovedRoster();
      lucide.createIcons();
    }

    function setRosterSort(sortVal) {
      currentRosterSort = sortVal;
      renderApprovedRoster();
      lucide.createIcons();
    }

    function handleRosterSearch(val) {
      currentRosterSearch = (val || '').trim().toLowerCase();
      renderApprovedRoster();
      lucide.createIcons();
    }

    function getFilteredAndSortedApproved() {
      let list = [...(lobbyData.approved || [])];

      // 1) Filter by category
      if (currentRosterFilter === 'admin') {
        list = list.filter(item => {
          const role = (item.role || '').toLowerCase();
          const perms = item.permissions || {};
          return perms.systemAdmin || perms.standardAdmin || perms.executiveAuthority || perms.keyboxAdmin ||
                 role.includes('tech') || role.includes('ceo') || role.includes('partner') ||
                 role.includes('viewing') || role.includes('admin') || role.includes('ซัพพอร์ต') ||
                 item.id === 'app_office_004' || item.is_leader || item.is_keybox;
        });
      } else if (currentRosterFilter === 'agent') {
        list = list.filter(item => {
          const role = (item.role || '').toLowerCase();
          const perms = item.permissions || {};
          return !(perms.systemAdmin || perms.standardAdmin || perms.executiveAuthority || perms.keyboxAdmin ||
                 role.includes('tech') || role.includes('ceo') || role.includes('partner') ||
                 role.includes('viewing') || role.includes('admin') || role.includes('ซัพพอร์ต') ||
                 item.id === 'app_office_004' || item.is_leader || item.is_keybox);
        });
      }

      // 2) Live search query
      if (currentRosterSearch) {
        list = list.filter(item => {
          const text = `${item.name} ${item.nickname || ''} ${item.phone} ${item.zone} ${item.role} ${item.title || ''}`.toLowerCase();
          return text.includes(currentRosterSearch);
        });
      }

      // 3) Sorting
      if (currentRosterSort === 'name') {
        list.sort((a, b) => (a.name || '').localeCompare(b.name || '', 'th'));
      } else if (currentRosterSort === 'zone') {
        list.sort((a, b) => (a.zone || '').localeCompare(b.zone || '', 'th'));
      } else if (currentRosterSort === 'newest') {
        list.reverse();
      } else {
        // Default 'tier': Tech / Supreme -> Key Master -> Admin -> Agent
        const getTierScore = (it) => {
          const th = getCardTheme(it);
          if (th.key === 'tech') return 100;
          if (th.key === 'supreme') return 90;
          if (th.key === 'keymaster') return 80;
          if (th.key === 'admin') return 70;
          return 10;
        };
        list.sort((a, b) => getTierScore(b) - getTierScore(a));
      }

      return list;
    }"""

new_presets_and_filter = """      support: {
        role: "🏢 เจ้าหน้าที่ซัพพอร์ตออฟฟิศ",
        title: "Office Property Coordinator",
        badges: ["🛡️ Standard Admin", "🏷️ ช่วยคัดสต๊อก", "🚫 ล็อกแก้ราคา"],
        permissions: { standardAdmin: true, editPrice: false, keyboxAdmin: false, leadInspector: false, executiveAuthority: false, catalogCurator: true, systemAdmin: false }
      },
      contract_agent: {
        role: "📑 Contract Agent (ตัวแทนสัญญา)",
        title: "Official Contract Agent",
        role_code: "CONTRACT_AGENT",
        badges: ["📑 สัญญาสังกัดทางการ", "🎯 รับลีดกลางบริษัท", "📜 บัตรดิจิทัลทางการ", "📅 จองเปิดบ้าน"],
        permissions: { standardAdmin: false, editPrice: false, keyboxAdmin: false, leadInspector: false, executiveAuthority: false, catalogCurator: false, systemAdmin: false, contractAgent: true }
      },
      free_agent: {
        role: "🤝 Free Agent (ตัวแทนอิสระ)",
        title: "Certified Free Agent Partner",
        role_code: "FREE_AGENT",
        badges: ["📜 บัตรดิจิทัลทางการ", "🔒 ล็อกค่านายหน้า 60 วัน", "📅 จองเปิดบ้าน", "🚫 ล็อกแอดมิน"],
        permissions: { standardAdmin: false, editPrice: false, keyboxAdmin: false, leadInspector: false, executiveAuthority: false, catalogCurator: false, systemAdmin: false, contractAgent: false }
      },
      agent: {
        role: "🤝 Free Agent (ตัวแทนอิสระ)",
        title: "Certified Free Agent Partner",
        role_code: "FREE_AGENT",
        badges: ["📜 บัตรดิจิทัลทางการ", "🔒 ล็อกค่านายหน้า 60 วัน", "📅 จองเปิดบ้าน", "🚫 ล็อกแอดมิน"],
        permissions: { standardAdmin: false, editPrice: false, keyboxAdmin: false, leadInspector: false, executiveAuthority: false, catalogCurator: false, systemAdmin: false, contractAgent: false }
      }
    };

    function isAdminItem(item) {
      const role = (item.role || '').toLowerCase();
      const perms = item.permissions || {};
      return !!(perms.systemAdmin || perms.standardAdmin || perms.executiveAuthority || perms.keyboxAdmin ||
             role.includes('tech') || role.includes('ceo') || (role.includes('partner') && !role.includes('free agent')) ||
             role.includes('viewing') || role.includes('admin') || role.includes('ซัพพอร์ต') ||
             item.id === 'app_office_004' || item.is_leader || item.is_keybox);
    }

    function isContractAgentItem(item) {
      if (isAdminItem(item)) return false;
      const role = (item.role || '').toLowerCase();
      const title = (item.title || '').toLowerCase();
      const perms = item.permissions || {};
      const badges = item.badges || [];
      return !!(perms.contractAgent || item.role_code === 'CONTRACT_AGENT' ||
             role.includes('contract') || role.includes('สัญญา') ||
             title.includes('contract') || badges.some(b => b.includes('สัญญา')));
    }

    function getRoleTierBadge(item) {
      const role = (item.role || "").toLowerCase();
      const perms = item.permissions || {};
      if (perms.systemAdmin || role.includes("tech") || role.includes("ต้น")) {
        return `<span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-rose-100 text-rose-800 border border-rose-300 shadow-2xs">💻 SUPER TECH</span>`;
      }
      if (role.includes("ceo") || (role.includes("partner") && !role.includes("free agent")) || role.includes("กูล") || role.includes("บัว") || perms.executiveAuthority) {
        return `<span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-gradient-to-r from-amber-100 to-red-100 text-amber-900 border border-amber-400 shadow-2xs">👑 SUPREME EXEC</span>`;
      }
      if (perms.keyboxAdmin || role.includes("viewing") || role.includes("กุญแจ") || role.includes("ลิลลี่")) {
        return `<span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-emerald-100 text-emerald-800 border border-emerald-400 shadow-2xs">🔑 KEYBOX MASTER</span>`;
      }
      if (perms.standardAdmin) {
        return `<span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-blue-100 text-blue-800 border border-blue-300 shadow-2xs">🏢 OFFICE ADMIN</span>`;
      }
      if (isContractAgentItem(item)) {
        return `<span class="px-2 py-0.5 rounded-full text-[10px] font-black text-white border shadow-2xs" style="background-color: #ffa8b6; border-color: #e58e9c;">📑 CONTRACT AGENT</span>`;
      }
      return `<span class="px-2 py-0.5 rounded-full text-[10px] font-black text-white border shadow-2xs" style="background-color: #786ea1; border-color: #5e5485;">🤝 FREE AGENT</span>`;
    }

    let currentRosterViewMode = 'cards';
    let currentRosterFilter = 'all'; // 'all' | 'admin' | 'contract_agent' | 'free_agent'
    let currentRosterSort = 'tier';   // 'tier' | 'name' | 'zone' | 'newest'
    let currentRosterSearch = '';

    function setRosterFilter(filter) {
      currentRosterFilter = filter;
      ['all', 'admin', 'contract_agent', 'free_agent'].forEach(k => {
        const btn = document.getElementById('filterBtn_' + k);
        if (!btn) return;
        if (k === filter) {
          btn.className = "roster-filter-btn px-3 py-1.5 rounded-xl text-xs font-bold transition shadow-2xs bg-slate-900 text-white";
        } else {
          btn.className = "roster-filter-btn px-3 py-1.5 rounded-xl text-xs font-semibold transition bg-slate-100 text-slate-600 hover:bg-slate-200";
        }
      });
      renderApprovedRoster();
      lucide.createIcons();
    }

    function setRosterSort(sortVal) {
      currentRosterSort = sortVal;
      renderApprovedRoster();
      lucide.createIcons();
    }

    function handleRosterSearch(val) {
      currentRosterSearch = (val || '').trim().toLowerCase();
      renderApprovedRoster();
      lucide.createIcons();
    }

    function getFilteredAndSortedApproved() {
      let list = [...(lobbyData.approved || [])];

      // 1) Filter by category
      if (currentRosterFilter === 'admin') {
        list = list.filter(item => isAdminItem(item));
      } else if (currentRosterFilter === 'contract_agent') {
        list = list.filter(item => isContractAgentItem(item));
      } else if (currentRosterFilter === 'free_agent' || currentRosterFilter === 'agent') {
        list = list.filter(item => !isAdminItem(item) && !isContractAgentItem(item));
      }

      // 2) Live search query
      if (currentRosterSearch) {
        list = list.filter(item => {
          const text = `${item.name} ${item.nickname || ''} ${item.phone} ${item.zone} ${item.role} ${item.title || ''}`.toLowerCase();
          return text.includes(currentRosterSearch);
        });
      }

      // 3) Sorting
      if (currentRosterSort === 'name') {
        list.sort((a, b) => (a.name || '').localeCompare(b.name || '', 'th'));
      } else if (currentRosterSort === 'zone') {
        list.sort((a, b) => (a.zone || '').localeCompare(b.zone || '', 'th'));
      } else if (currentRosterSort === 'newest') {
        list.reverse();
      } else {
        // Default 'tier': Tech / Supreme -> Key Master -> Admin -> Contract Agent -> Free Agent
        const getTierScore = (it) => {
          const th = getCardTheme(it);
          if (th.key === 'tech') return 100;
          if (th.key === 'supreme') return 90;
          if (th.key === 'keymaster') return 80;
          if (th.key === 'admin') return 70;
          if (th.key === 'contract_agent') return 30;
          return 10;
        };
        list.sort((a, b) => getTierScore(b) - getTierScore(a));
      }

      return list;
    }"""

assert old_presets_and_filter in lobby_html, "old_presets_and_filter not found"
lobby_html = lobby_html.replace(old_presets_and_filter, new_presets_and_filter, 1)

# 1E. Update syncMemberPermissionsFromBadges
old_sync_badges = """    function syncMemberPermissionsFromBadges(member) {
      const bList = member.badges || [];
      member.permissions = member.permissions || {};
      if (bList.some(b => b.includes('เคาะราคา'))) member.permissions.editPrice = true;
      if (bList.some(b => b.includes('กุญแจ'))) member.permissions.keyboxAdmin = true;
      if (bList.some(b => b.includes('สิทธิ์บริหาร'))) member.permissions.executiveAuthority = true;
      if (bList.some(b => b.includes('ดูแชทลีด'))) member.permissions.leadInspector = true;
      if (bList.some(b => b.includes('Standard Admin'))) member.permissions.standardAdmin = true;
      if (bList.some(b => b.includes('ช่วยคัดสต๊อก'))) member.permissions.catalogCurator = true;
      if (bList.some(b => b.includes('Technical'))) member.permissions.systemAdmin = true;
    }"""

new_sync_badges = """    function syncMemberPermissionsFromBadges(member) {
      const bList = member.badges || [];
      member.permissions = member.permissions || {};
      member.permissions.editPrice = bList.some(b => b.includes('เคาะราคา'));
      member.permissions.keyboxAdmin = bList.some(b => b.includes('กุญแจ'));
      member.permissions.executiveAuthority = bList.some(b => b.includes('สิทธิ์บริหาร'));
      member.permissions.leadInspector = bList.some(b => b.includes('ดูแชทลีด'));
      member.permissions.standardAdmin = bList.some(b => b.includes('Standard Admin'));
      member.permissions.catalogCurator = bList.some(b => b.includes('ช่วยคัดสต๊อก'));
      member.permissions.systemAdmin = bList.some(b => b.includes('Technical'));
      member.permissions.contractAgent = bList.some(b => b.includes('สัญญา'));
      if (!isAdminItem(member)) {
        if (member.permissions.contractAgent) {
          member.role = "📑 Contract Agent (ตัวแทนสัญญา)";
          member.title = "Official Contract Agent";
          member.role_code = "CONTRACT_AGENT";
        } else {
          member.role = "🤝 Free Agent (ตัวแทนอิสระ)";
          member.title = "Certified Free Agent Partner";
          member.role_code = "FREE_AGENT";
        }
      }
    }"""

assert old_sync_badges in lobby_html, "old_sync_badges not found"
lobby_html = lobby_html.replace(old_sync_badges, new_sync_badges, 1)

# 1F. Update getCardTheme (Pink Sand #ffa8B6 for Contract Agent, Kimberly #786ea1 for Free Agent)
old_card_theme = """      // 2) Supreme EXE (เจี๊ยบ, บัว / CEO & Executive Partner) -> ส้มแดง/Terracotta (#e15b42) ตาม admin_001_Supreme EXE.jpg
      if (role.includes("ceo") || role.includes("partner") || role.includes("supreme") || perms.executiveAuthority || item.is_leader) {"""

new_card_theme_supreme = """      // 2) Supreme EXE (เจี๊ยบ, บัว / CEO & Executive Partner) -> ส้มแดง/Terracotta (#e15b42) ตาม admin_001_Supreme EXE.jpg
      if (role.includes("ceo") || (role.includes("partner") && !role.includes("free agent") && !title.includes("free agent")) || role.includes("supreme") || perms.executiveAuthority || item.is_leader) {"""

assert old_card_theme in lobby_html, "old_card_theme not found"
lobby_html = lobby_html.replace(old_card_theme, new_card_theme_supreme, 1)

old_agent_theme = """      // 5) Co-Broker พันธมิตรทางการ -> สีเทาสโมสร
      return {
        key: 'agent',
        roleBadgeText: 'Co-Broker',
        icon: 'handshake',
        primaryHex: '#64748b',
        bannerHex: '#64748b',
        badgeBg: '#64748b',
        badgeBorder: '#475569',
        badgeTextColor: '#ffffff',
        badgeIconBg: '#475569',
        badgeIconColor: '#ffffff',
        titleColor: '#475569',
        bottomBarHex: '#64748b',
        isLocked: false
      };"""

new_agent_theme = """      // 5) Contract Agent (ตัวแทนสัญญาสังกัด) -> สีชมพู Pink Sand (#ffa8B6)
      if (isContractAgentItem(item)) {
        return {
          key: 'contract_agent',
          roleBadgeText: 'Contract Agent',
          icon: 'award',
          primaryHex: '#ffa8b6',
          bannerHex: '#ffa8b6',
          badgeBg: '#ffa8b6',
          badgeBorder: '#e58e9c',
          badgeTextColor: '#ffffff',
          badgeIconBg: '#e58e9c',
          badgeIconColor: '#ffffff',
          titleColor: '#d46a7e',
          bottomBarHex: '#ffa8b6',
          isLocked: false
        };
      }

      // 6) Free Agent (ตัวแทนอิสระ / พันธมิตร) -> สีม่วง Kimberly (#786ea1)
      return {
        key: 'free_agent',
        roleBadgeText: 'Free Agent',
        icon: 'handshake',
        primaryHex: '#786ea1',
        bannerHex: '#786ea1',
        badgeBg: '#786ea1',
        badgeBorder: '#5e5485',
        badgeTextColor: '#ffffff',
        badgeIconBg: '#5e5485',
        badgeIconColor: '#ffffff',
        titleColor: '#786ea1',
        bottomBarHex: '#786ea1',
        isLocked: false
      };"""

assert old_agent_theme in lobby_html, "old_agent_theme not found"
lobby_html = lobby_html.replace(old_agent_theme, new_agent_theme, 1)

# 1G. Update 1-Click Buttons on Pending Cards & Count calculation in renderApprovedRoster
old_pending_buttons = """              <div class="grid grid-cols-2 sm:grid-cols-6 gap-2 text-xs">
                <button onclick="approveWithPreset('${item.id}', 'gool')" class="p-2 rounded-xl bg-slate-50 hover:bg-amber-50 hover:border-amber-400 border border-slate-200 text-left transition space-y-0.5 shadow-2xs active:scale-95">
                  <div class="font-bold text-amber-900">👑 เจี๊ยบ(กูล)</div>
                  <div class="text-[9px] text-slate-500">CEO / เคาะราคา</div>
                </button>
                <button onclick="approveWithPreset('${item.id}', 'bua')" class="p-2 rounded-xl bg-slate-50 hover:bg-amber-50 hover:border-amber-400 border border-slate-200 text-left transition space-y-0.5 shadow-2xs active:scale-95">
                  <div class="font-bold text-amber-900">👑 คุณบัว</div>
                  <div class="text-[9px] text-slate-500">แทนเจี๊ยบ 100%</div>
                </button>
                <button onclick="approveWithPreset('${item.id}', 'lily')" class="p-2 rounded-xl bg-slate-50 hover:bg-emerald-50 hover:border-emerald-400 border border-slate-200 text-left transition space-y-0.5 shadow-2xs active:scale-95">
                  <div class="font-bold text-emerald-900">🔑 พี่ลิลลี่</div>
                  <div class="text-[9px] text-slate-500">คุมกุญแจ OTP 100%</div>
                </button>
                <button onclick="approveWithPreset('${item.id}', 'ton')" class="p-2 rounded-xl bg-slate-50 hover:bg-rose-50 hover:border-rose-400 border border-slate-200 text-left transition space-y-0.5 shadow-2xs active:scale-95">
                  <div class="font-bold text-rose-900">💻 คุณต้น</div>
                  <div class="text-[9px] text-slate-500">Tech Lead / สิทธิ์เต็ม</div>
                </button>
                <button onclick="approveWithPreset('${item.id}', 'support')" class="p-2 rounded-xl bg-slate-50 hover:bg-blue-50 hover:border-blue-400 border border-slate-200 text-left transition space-y-0.5 shadow-2xs active:scale-95">
                  <div class="font-bold text-blue-900">🏢 ซัพพอร์ต</div>
                  <div class="text-[9px] text-slate-500">Standard Admin</div>
                </button>
                <button onclick="approveWithPreset('${item.id}', 'agent')" class="p-2 rounded-xl bg-slate-50 hover:bg-emerald-50 hover:border-emerald-400 border border-slate-200 text-left transition space-y-0.5 shadow-2xs active:scale-95">
                  <div class="font-bold text-emerald-800">🤝 Co-Broker</div>
                  <div class="text-[9px] text-slate-500">พันธมิตรรับรอง</div>
                </button>
              </div>"""

new_pending_buttons = """              <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-2 text-xs">
                <button onclick="approveWithPreset('${item.id}', 'gool')" class="p-2 rounded-xl bg-slate-50 hover:bg-amber-50 hover:border-amber-400 border border-slate-200 text-left transition space-y-0.5 shadow-2xs active:scale-95">
                  <div class="font-bold text-amber-900">👑 เจี๊ยบ(กูล)</div>
                  <div class="text-[9px] text-slate-500">CEO / เคาะราคา</div>
                </button>
                <button onclick="approveWithPreset('${item.id}', 'bua')" class="p-2 rounded-xl bg-slate-50 hover:bg-amber-50 hover:border-amber-400 border border-slate-200 text-left transition space-y-0.5 shadow-2xs active:scale-95">
                  <div class="font-bold text-amber-900">👑 คุณบัว</div>
                  <div class="text-[9px] text-slate-500">แทนเจี๊ยบ 100%</div>
                </button>
                <button onclick="approveWithPreset('${item.id}', 'lily')" class="p-2 rounded-xl bg-slate-50 hover:bg-emerald-50 hover:border-emerald-400 border border-slate-200 text-left transition space-y-0.5 shadow-2xs active:scale-95">
                  <div class="font-bold text-emerald-900">🔑 พี่ลิลลี่</div>
                  <div class="text-[9px] text-slate-500">คุมกุญแจ OTP 100%</div>
                </button>
                <button onclick="approveWithPreset('${item.id}', 'ton')" class="p-2 rounded-xl bg-slate-50 hover:bg-rose-50 hover:border-rose-400 border border-slate-200 text-left transition space-y-0.5 shadow-2xs active:scale-95">
                  <div class="font-bold text-rose-900">💻 คุณต้น</div>
                  <div class="text-[9px] text-slate-500">Tech Lead / สิทธิ์เต็ม</div>
                </button>
                <button onclick="approveWithPreset('${item.id}', 'support')" class="p-2 rounded-xl bg-slate-50 hover:bg-blue-50 hover:border-blue-400 border border-slate-200 text-left transition space-y-0.5 shadow-2xs active:scale-95">
                  <div class="font-bold text-blue-900">🏢 ซัพพอร์ต</div>
                  <div class="text-[9px] text-slate-500">Standard Admin</div>
                </button>
                <button onclick="approveWithPreset('${item.id}', 'contract_agent')" class="p-2 rounded-xl bg-[#ffa8b6]/15 hover:bg-[#ffa8b6]/30 border border-[#ffa8b6] text-left transition space-y-0.5 shadow-2xs active:scale-95">
                  <div class="font-bold text-[#9e3b4f]">📑 Contract Agent</div>
                  <div class="text-[9px] text-[#b84a60]">ตัวแทนสัญญาสังกัด</div>
                </button>
                <button onclick="approveWithPreset('${item.id}', 'free_agent')" class="p-2 rounded-xl bg-[#786ea1]/15 hover:bg-[#786ea1]/25 border border-[#786ea1] text-left transition space-y-0.5 shadow-2xs active:scale-95">
                  <div class="font-bold text-[#4a4269]">🤝 Free Agent</div>
                  <div class="text-[9px] text-[#5e5485]">ตัวแทนอิสระ</div>
                </button>
              </div>"""

assert old_pending_buttons in lobby_html, "old_pending_buttons not found"
lobby_html = lobby_html.replace(old_pending_buttons, new_pending_buttons, 1)

old_counts = """        // Update counts
        const allList = lobbyData.approved || [];
        const adminCount = allList.filter(item => {
          const role = (item.role || '').toLowerCase();
          const perms = item.permissions || {};
          return perms.systemAdmin || perms.standardAdmin || perms.executiveAuthority || perms.keyboxAdmin ||
                 role.includes('tech') || role.includes('ceo') || role.includes('partner') ||
                 role.includes('viewing') || role.includes('admin') || role.includes('ซัพพอร์ต') ||
                 item.id === 'app_office_004' || item.is_leader || item.is_keybox;
        }).length;
        const agentCount = allList.length - adminCount;

        const countAllEl = document.getElementById('count_all');
        const countAdminEl = document.getElementById('count_admin');
        const countAgentEl = document.getElementById('count_agent');
        if (countAllEl) countAllEl.innerText = allList.length;
        if (countAdminEl) countAdminEl.innerText = adminCount;
        if (countAgentEl) countAgentEl.innerText = agentCount;"""

new_counts = """        // Update counts
        const allList = lobbyData.approved || [];
        const adminCount = allList.filter(item => isAdminItem(item)).length;
        const contractAgentCount = allList.filter(item => isContractAgentItem(item)).length;
        const freeAgentCount = allList.filter(item => !isAdminItem(item) && !isContractAgentItem(item)).length;

        const countAllEl = document.getElementById('count_all');
        const countAdminEl = document.getElementById('count_admin');
        const countContractEl = document.getElementById('count_contract_agent');
        const countFreeEl = document.getElementById('count_free_agent');
        if (countAllEl) countAllEl.innerText = allList.length;
        if (countAdminEl) countAdminEl.innerText = adminCount;
        if (countContractEl) countContractEl.innerText = contractAgentCount;
        if (countFreeEl) countFreeEl.innerText = freeAgentCount;"""

assert old_counts in lobby_html, "old_counts not found"
lobby_html = lobby_html.replace(old_counts, new_counts, 1)

# 1H. Badge color in card rendering for Contract Agent badge
old_badge_cls = """                          let badgeCls = 'bg-slate-100 text-slate-700 border border-slate-200';
                          if (b.includes('เคาะราคา')) badgeCls = 'bg-amber-50 text-amber-900 border-2 border-amber-300 font-bold';
                          else if (b.includes('กุญแจ')) badgeCls = 'bg-emerald-50 text-emerald-900 border-2 border-emerald-300 font-bold';
                          else if (b.includes('Technical') || b.includes('Tech')) badgeCls = 'bg-rose-50 text-rose-900 border-2 border-rose-300 font-bold';"""

new_badge_cls = """                          let badgeCls = 'bg-slate-100 text-slate-700 border border-slate-200';
                          if (b.includes('สัญญา')) badgeCls = 'bg-[#ffa8b6]/25 text-[#9e3b4f] border-2 border-[#ffa8b6] font-bold';
                          else if (b.includes('เคาะราคา')) badgeCls = 'bg-amber-50 text-amber-900 border-2 border-amber-300 font-bold';
                          else if (b.includes('กุญแจ')) badgeCls = 'bg-emerald-50 text-emerald-900 border-2 border-emerald-300 font-bold';
                          else if (b.includes('Technical') || b.includes('Tech')) badgeCls = 'bg-rose-50 text-rose-900 border-2 border-rose-300 font-bold';"""

assert old_badge_cls in lobby_html, "old_badge_cls not found"
lobby_html = lobby_html.replace(old_badge_cls, new_badge_cls, 1)

# 1I. Update Edit Permission Modal to include Contract Agent checkbox
old_modal_checkbox = """          <div class="space-y-2 text-xs">
            <label class="flex items-start gap-2.5 p-2 rounded-xl bg-slate-50 hover:bg-slate-100 cursor-pointer border border-slate-200">"""

new_modal_checkbox = """          <div class="space-y-2 text-xs">
            <label class="flex items-start gap-2.5 p-2 rounded-xl bg-[#ffa8b6]/20 hover:bg-[#ffa8b6]/30 cursor-pointer border border-[#ffa8b6]">
              <input type="checkbox" id="chk_contractAgent" class="mt-0.5 rounded text-pink-500 focus:ring-0">
              <div>
                <strong class="text-[#9e3b4f]">📑 Contract Agent (ตัวแทนสัญญาสังกัดทางการ - Pink Sand #ffa8B6)</strong>
                <p class="text-[11px] text-[#b84a60]">ตัวแทนที่มีสัญญาแต่งตั้ง รับสิทธิ์ลีดกลางบริษัท (หากไม่ติ๊กและไม่ได้เป็น Admin จะเป็น Free Agent สีม่วง #786ea1)</p>
              </div>
            </label>

            <label class="flex items-start gap-2.5 p-2 rounded-xl bg-slate-50 hover:bg-slate-100 cursor-pointer border border-slate-200">"""

assert old_modal_checkbox in lobby_html, "old_modal_checkbox not found"
lobby_html = lobby_html.replace(old_modal_checkbox, new_modal_checkbox, 1)

# Update openEditPermissionModal & executeSavePermissions
old_edit_perm_code = """      const p = member.permissions || {};
      document.getElementById('chk_standardAdmin').checked = !!p.standardAdmin;
      document.getElementById('chk_editPrice').checked = !!p.editPrice;
      document.getElementById('chk_executiveAuthority').checked = !!p.executiveAuthority;
      document.getElementById('chk_keyboxAdmin').checked = !!p.keyboxAdmin;
      document.getElementById('chk_leadInspector').checked = !!p.leadInspector;
      document.getElementById('chk_catalogCurator').checked = !!p.catalogCurator;
      document.getElementById('chk_systemAdmin').checked = !!p.systemAdmin;"""

new_edit_perm_code = """      const p = member.permissions || {};
      const chkContract = document.getElementById('chk_contractAgent');
      if (chkContract) chkContract.checked = isContractAgentItem(member);
      document.getElementById('chk_standardAdmin').checked = !!p.standardAdmin;
      document.getElementById('chk_editPrice').checked = !!p.editPrice;
      document.getElementById('chk_executiveAuthority').checked = !!p.executiveAuthority;
      document.getElementById('chk_keyboxAdmin').checked = !!p.keyboxAdmin;
      document.getElementById('chk_leadInspector').checked = !!p.leadInspector;
      document.getElementById('chk_catalogCurator').checked = !!p.catalogCurator;
      document.getElementById('chk_systemAdmin').checked = !!p.systemAdmin;"""

assert old_edit_perm_code in lobby_html, "old_edit_perm_code not found"
lobby_html = lobby_html.replace(old_edit_perm_code, new_edit_perm_code)

old_save_perm_code = """      const newPerms = {
        standardAdmin: document.getElementById('chk_standardAdmin').checked,
        editPrice: document.getElementById('chk_editPrice').checked,
        executiveAuthority: document.getElementById('chk_executiveAuthority').checked,
        keyboxAdmin: document.getElementById('chk_keyboxAdmin').checked,
        leadInspector: document.getElementById('chk_leadInspector').checked,
        catalogCurator: document.getElementById('chk_catalogCurator').checked,
        systemAdmin: document.getElementById('chk_systemAdmin').checked
      };

      // Derive badges
      const newBadges = [];
      if (newPerms.editPrice) newBadges.push("💰 เคาะราคาบ้าน");
      if (newPerms.executiveAuthority) newBadges.push("👑 สิทธิ์บริหาร");
      if (newPerms.leadInspector) newBadges.push("💬 ดูแชทลีด");
      if (newPerms.keyboxAdmin) newBadges.push("🔑 คุมกุญแจ OTP 100%");
      if (newPerms.catalogCurator) newBadges.push("🏷️ ช่วยคัดสต๊อก");
      if (newPerms.systemAdmin) newBadges.push("⚙️ Technical Admin");
      if (newPerms.standardAdmin) newBadges.push("🛡️ Standard Admin");
      if (!newPerms.editPrice) newBadges.push("🚫 ล็อกแก้ราคา");
      if (newBadges.length === 0) newBadges.push("📜 บัตรดิจิทัลทางการ");"""

new_save_perm_code = """      const isContractChecked = document.getElementById('chk_contractAgent') ? document.getElementById('chk_contractAgent').checked : false;
      const newPerms = {
        standardAdmin: document.getElementById('chk_standardAdmin').checked,
        editPrice: document.getElementById('chk_editPrice').checked,
        executiveAuthority: document.getElementById('chk_executiveAuthority').checked,
        keyboxAdmin: document.getElementById('chk_keyboxAdmin').checked,
        leadInspector: document.getElementById('chk_leadInspector').checked,
        catalogCurator: document.getElementById('chk_catalogCurator').checked,
        systemAdmin: document.getElementById('chk_systemAdmin').checked,
        contractAgent: isContractChecked
      };

      // Derive badges
      const newBadges = [];
      if (newPerms.contractAgent) {
        newBadges.push("📑 สัญญาสังกัดทางการ");
        newBadges.push("🎯 รับลีดกลางบริษัท");
      }
      if (newPerms.editPrice) newBadges.push("💰 เคาะราคาบ้าน");
      if (newPerms.executiveAuthority) newBadges.push("👑 สิทธิ์บริหาร");
      if (newPerms.leadInspector) newBadges.push("💬 ดูแชทลีด");
      if (newPerms.keyboxAdmin) newBadges.push("🔑 คุมกุญแจ OTP 100%");
      if (newPerms.catalogCurator) newBadges.push("🏷️ ช่วยคัดสต๊อก");
      if (newPerms.systemAdmin) newBadges.push("⚙️ Technical Admin");
      if (newPerms.standardAdmin) newBadges.push("🛡️ Standard Admin");
      if (!newPerms.editPrice) newBadges.push("🚫 ล็อกแก้ราคา");
      if (newBadges.length === 0) newBadges.push("📜 บัตรดิจิทัลทางการ");"""

assert old_save_perm_code in lobby_html, "old_save_perm_code not found"
lobby_html = lobby_html.replace(old_save_perm_code, new_save_perm_code)

with open(lobby_path, "w", encoding="utf-8") as f:
    f.write(lobby_html)

print("Updated admin_lobby_manager.html successfully!")

# ==============================================================================
# 2. UPDATE agent_registration.html
# ==============================================================================
reg_path = os.path.join(ROOT, "agent_registration.html")
with open(reg_path, "r", encoding="utf-8") as f:
    reg_html = f.read()

old_reg_affiliation = """        <!-- Affiliation Selection -->
        <div class="space-y-1.5">
          <label class="text-xs font-bold text-slate-700 flex items-center gap-1.5">
            <i data-lucide="briefcase" class="w-3.5 h-3.5 text-amber-600"></i>
            <span>รูปแบบการร่วมงาน *</span>
          </label>
          <div class="grid grid-cols-2 gap-2">
            <label class="flex items-center gap-2.5 p-3 rounded-2xl bg-amber-50/60 border border-amber-300 cursor-pointer hover:bg-amber-50 transition">
              <input type="radio" name="affiliation" value="agent" checked class="text-amber-600 focus:ring-0">
              <div>
                <div class="text-xs font-bold text-slate-900">🤝 Co-Broker</div>
                <div class="text-[9px] text-slate-500">ตัวแทนอิสระ / พันธมิตร</div>
              </div>
            </label>
            <label class="flex items-center gap-2.5 p-3 rounded-2xl bg-slate-50 border border-slate-200 cursor-pointer hover:bg-slate-100 transition">
              <input type="radio" name="affiliation" value="office" class="text-amber-600 focus:ring-0">
              <div>
                <div class="text-xs font-bold text-slate-900">🏢 ทีมงานออฟฟิศ</div>
                <div class="text-[9px] text-slate-500">เจ้าหน้าที่ประจำ</div>
              </div>
            </label>
          </div>
        </div>"""

new_reg_affiliation = """        <!-- Affiliation Selection -->
        <div class="space-y-1.5">
          <label class="text-xs font-bold text-slate-700 flex items-center gap-1.5">
            <i data-lucide="briefcase" class="w-3.5 h-3.5 text-amber-600"></i>
            <span>รูปแบบการร่วมงาน *</span>
          </label>
          <div class="grid grid-cols-1 sm:grid-cols-3 gap-2">
            <label class="flex items-center gap-2 p-2.5 rounded-2xl bg-[#786ea1]/15 border border-[#786ea1] cursor-pointer hover:bg-[#786ea1]/25 transition">
              <input type="radio" name="affiliation" value="free_agent" checked class="text-[#786ea1] focus:ring-0">
              <div>
                <div class="text-xs font-bold text-[#4a4269]">🤝 Free Agent</div>
                <div class="text-[9px] text-[#5e5485]">ตัวแทนอิสระ / พันธมิตร</div>
              </div>
            </label>
            <label class="flex items-center gap-2 p-2.5 rounded-2xl bg-[#ffa8b6]/20 border border-[#ffa8b6] cursor-pointer hover:bg-[#ffa8b6]/30 transition">
              <input type="radio" name="affiliation" value="contract_agent" class="text-[#d46a7e] focus:ring-0">
              <div>
                <div class="text-xs font-bold text-[#9e3b4f]">📑 Contract Agent</div>
                <div class="text-[9px] text-[#b84a60]">ตัวแทนสัญญาสังกัด</div>
              </div>
            </label>
            <label class="flex items-center gap-2 p-2.5 rounded-2xl bg-slate-50 border border-slate-200 cursor-pointer hover:bg-slate-100 transition">
              <input type="radio" name="affiliation" value="office" class="text-amber-600 focus:ring-0">
              <div>
                <div class="text-xs font-bold text-slate-900">🏢 ทีมงานออฟฟิศ</div>
                <div class="text-[9px] text-slate-500">เจ้าหน้าที่ประจำ</div>
              </div>
            </label>
          </div>
        </div>"""

assert old_reg_affiliation in reg_html, "old_reg_affiliation not found"
reg_html = reg_html.replace(old_reg_affiliation, new_reg_affiliation, 1)

old_aff_label = """        affiliation: affiliation,
        affiliation_label: affiliation === 'office' ? "🏢 พนักงาน/ทีมงานออฟฟิศ" : "🤝 Co-Broker พันธมิตรภายนอก","""

new_aff_label = """        affiliation: affiliation,
        affiliation_label: affiliation === 'office' ? "🏢 พนักงาน/ทีมงานออฟฟิศ" : (affiliation === 'contract_agent' ? "📑 สมัคร Contract Agent (ตัวแทนสัญญา)" : "🤝 สมัคร Free Agent (ตัวแทนอิสระ)"),"""

assert old_aff_label in reg_html, "old_aff_label not found"
reg_html = reg_html.replace(old_aff_label, new_aff_label, 1)

old_portal_tier = """      let tierHtml = `<span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-slate-100 text-slate-700 border border-slate-300">🤝 CO-BROKER</span>`;
      if (perms.systemAdmin || roleLower.includes('tech') || roleLower.includes('ต้น')) {
        tierHtml = `<span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-rose-100 text-rose-800 border border-rose-300">💻 SUPER TECH</span>`;
      } else if (perms.executiveAuthority || roleLower.includes('ceo') || roleLower.includes('partner') || roleLower.includes('กูล') || roleLower.includes('บัว')) {
        tierHtml = `<span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-gradient-to-r from-amber-100 to-red-100 text-amber-900 border border-amber-400">👑 SUPREME EXEC</span>`;
      } else if (perms.keyboxAdmin || roleLower.includes('viewing') || roleLower.includes('กุญแจ') || roleLower.includes('ลิลลี่')) {
        tierHtml = `<span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-emerald-100 text-emerald-800 border border-emerald-400">🔑 KEYBOX MASTER</span>`;
      } else if (perms.standardAdmin) {
        tierHtml = `<span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-blue-100 text-blue-800 border border-blue-300">🏢 OFFICE ADMIN</span>`;
      }"""

new_portal_tier = """      let tierHtml = `<span class="px-2 py-0.5 rounded-full text-[10px] font-black text-white border shadow-2xs" style="background-color: #786ea1; border-color: #5e5485;">🤝 FREE AGENT</span>`;
      if (perms.systemAdmin || roleLower.includes('tech') || roleLower.includes('ต้น')) {
        tierHtml = `<span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-rose-100 text-rose-800 border border-rose-300">💻 SUPER TECH</span>`;
      } else if (perms.executiveAuthority || roleLower.includes('ceo') || (roleLower.includes('partner') && !roleLower.includes('free agent')) || roleLower.includes('กูล') || roleLower.includes('บัว')) {
        tierHtml = `<span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-gradient-to-r from-amber-100 to-red-100 text-amber-900 border border-amber-400">👑 SUPREME EXEC</span>`;
      } else if (perms.keyboxAdmin || roleLower.includes('viewing') || roleLower.includes('กุญแจ') || roleLower.includes('ลิลลี่')) {
        tierHtml = `<span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-emerald-100 text-emerald-800 border border-emerald-400">🔑 KEYBOX MASTER</span>`;
      } else if (perms.standardAdmin) {
        tierHtml = `<span class="px-2 py-0.5 rounded-full text-[10px] font-black bg-blue-100 text-blue-800 border border-blue-300">🏢 OFFICE ADMIN</span>`;
      } else if (perms.contractAgent || member.role_code === 'CONTRACT_AGENT' || roleLower.includes('contract') || roleLower.includes('สัญญา') || (member.badges || []).some(b => b.includes('สัญญา'))) {
        tierHtml = `<span class="px-2 py-0.5 rounded-full text-[10px] font-black text-white border shadow-2xs" style="background-color: #ffa8b6; border-color: #e58e9c;">📑 CONTRACT AGENT</span>`;
      }"""

assert old_portal_tier in reg_html, "old_portal_tier not found"
reg_html = reg_html.replace(old_portal_tier, new_portal_tier, 1)

with open(reg_path, "w", encoding="utf-8") as f:
    f.write(reg_html)

print("Updated agent_registration.html successfully!")

# ==============================================================================
# 3. UPDATE catalog.html
# ==============================================================================
cat_path = os.path.join(ROOT, "catalog.html")
with open(cat_path, "r", encoding="utf-8") as f:
    cat_html = f.read()

cat_html = cat_html.replace('<option value="employee">โหมด: พนักงาน</option>', '<option value="employee">โหมด: Contract Agent</option>')
cat_html = cat_html.replace('title="โหมดพนักงานประจำ">พนักงาน</button>', 'title="โหมด Contract Agent (ตัวแทนสัญญาสังกัด)">Contract</button>')
cat_html = cat_html.replace('isAdmin ? "พนักงานประจำ (คอม 1% มีเงินเดือน)" : "ระบบคลังทรัพย์ตัวแทน (Co-Broker Partner)"', 'isAdmin ? "Contract Agent (ตัวแทนสัญญาสังกัด)" : "ระบบคลังทรัพย์ตัวแทน (Contract Agent)"')

with open(cat_path, "w", encoding="utf-8") as f:
    f.write(cat_html)

print("Updated catalog.html successfully!")
