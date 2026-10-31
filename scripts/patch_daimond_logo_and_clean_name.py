path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\agent_profile.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Header Logo: Use assets/daimond.svg with company name beside it (Red & Black text)
old_logo_block = '''        <div class="flex items-center gap-2 min-w-0">
          <img src="assets/siwasup_logo.png" alt="Siwasup Asset Logo" class="h-7 sm:h-8 w-auto shrink-0 object-contain" onerror="this.onerror=null; this.src='assets/siwasup_logo.svg';" />
          <div class="min-w-0">
            <h1 class="text-[11px] sm:text-xs font-bold text-slate-900 tracking-wider uppercase truncate">SIWASUP ASSET</h1>
            <p class="text-[9px] sm:text-[10px] text-slate-400 truncate">Co-Broker Partner Network</p>
          </div>
        </div>'''

new_logo_block = '''<div class="flex items-center gap-2.5 min-w-0">
          <!-- Official Red Diamond Crest from daimond.svg -->
          <img src="assets/daimond.svg" alt="Siwasup Diamond Crest" class="h-8 sm:h-9 w-auto shrink-0 object-contain drop-shadow-xs" />
          <div class="min-w-0 leading-tight">
            <div class="flex items-center gap-1">
              <span class="text-xs sm:text-[13px] font-extrabold tracking-wider text-[#ed2027] uppercase">SIWASUP</span>
              <span class="text-xs sm:text-[13px] font-extrabold tracking-wider text-slate-950 uppercase">ASSET</span>
            </div>
            <p class="text-[9px] sm:text-[9.5px] text-slate-400 font-medium tracking-wide truncate">ศิวาทรัพย์ แอสเซท</p>
          </div>
        </div>'''

if old_logo_block in html:
    html = html.replace(old_logo_block, new_logo_block)
    print("Replaced main header logo successfully!")
else:
    print("Warning: old_logo_block not matched directly")

# Also modal logo
old_modal_logo = '''          <div class="flex items-center gap-1.5">
            <img src="assets/siwasup_logo.png" alt="Siwasup Logo" class="h-4 sm:h-5 w-auto object-contain" onerror="this.onerror=null; this.src='assets/siwasup_logo.svg';" />
            <span class="text-[9.5px] font-bold text-slate-800 tracking-wider uppercase">SIWASUP ASSET</span>
          </div>'''

new_modal_logo = '''<div class="flex items-center gap-1.5">
            <img src="assets/daimond.svg" alt="Siwasup Diamond Crest" class="h-5 sm:h-5.5 w-auto shrink-0 object-contain" />
            <div class="leading-tight">
              <span class="text-[9.5px] font-extrabold tracking-wider text-[#ed2027]">SIWASUP</span>
              <span class="text-[9.5px] font-extrabold tracking-wider text-slate-950">ASSET</span>
            </div>
          </div>'''

if old_modal_logo in html:
    html = html.replace(old_modal_logo, new_modal_logo)
    print("Replaced modal logo successfully!")

# 2. Update Info Section:
# Enlarge name to text-lg sm:text-xl with font-medium
# Position directly underneath name without capsule
# Remove redundant contact pills next to name
old_info_block = '''        <!-- Info (Right Side) -->
        <div class="space-y-1 flex-1 min-w-0">
          <div class="flex items-center gap-1.5 flex-wrap">
            <span id="agentCode" class="text-[10.5px] font-mono font-bold px-2 py-0.5 rounded-md bg-red-50 text-red-700 border border-red-200/80 shadow-2xs">S98</span>
            <span id="zoneBadge" class="text-[11px] font-medium text-slate-500 truncate">📍 โซนวัชรพล-สายไหม</span>
          </div>
          <h2 id="agentName" class="text-base sm:text-lg font-bold text-slate-900 truncate">คุณนภชกร วรพัทธ์ภูดิท</h2>
          <p id="agentTitle" class="text-[10.5px] sm:text-xs text-slate-400 truncate">ที่ปรึกษาด้านการซื้อ-ขายอสังหาริมทรัพย์มืออาชีพ</p>

          <!-- Action Contact Pills (NO "โทร", Formatted 10-digit number with spacing) -->
          <div class="pt-1.5 flex flex-wrap items-center gap-1.5 sm:gap-2">
            <a id="btnCall" href="tel:0966458994" class="inline-flex items-center gap-1.5 text-[11px] sm:text-xs font-semibold px-3 py-1.5 rounded-full bg-[#120808] hover:bg-[#251010] text-white border border-amber-500/40 transition shadow-xs">
              <i data-lucide="phone" class="w-3 h-3 sm:w-3.5 sm:h-3.5 text-white"></i>
              <span id="txtPhone" class="font-mono tracking-tight font-bold">096 645 8994</span>
            </a>
            <a id="btnLine" href="https://line.me/ti/p/~" target="_blank" class="inline-flex items-center gap-1.5 text-[11px] sm:text-xs font-semibold px-3 py-1.5 rounded-full bg-white text-[#06C755] border border-[#06C755] hover:bg-emerald-50 transition shadow-xs">
              <i data-lucide="message-circle" class="w-3 h-3 sm:w-3.5 sm:h-3.5"></i>
              <span id="txtLine">LINE OA</span>
            </a>
          </div>
        </div>'''

new_info_block = '''        <!-- Info (Right Side) -->
        <div class="space-y-1 sm:space-y-1.5 flex-1 min-w-0">
          <div class="flex items-center gap-1.5 flex-wrap">
            <span id="agentCode" class="text-[10px] sm:text-[10.5px] font-mono font-bold px-2 py-0.5 rounded-md bg-red-50 text-red-700 border border-red-200/80 shadow-2xs">S98</span>
            <span id="zoneBadge" class="text-[11px] font-medium text-slate-500 truncate">📍 โซนวัชรพล-สายไหม</span>
          </div>

          <!-- Enlarged Name with Lighter/Balanced Weight (font-medium text-lg sm:text-xl) -->
          <h2 id="agentName" class="text-lg sm:text-xl font-medium tracking-tight text-slate-900 truncate">คุณนภชกร วรพัทธ์ภูดิท</h2>

          <!-- Position directly under name without capsule -->
          <p id="agentTitle" class="text-[11.5px] sm:text-xs text-slate-500 font-normal leading-relaxed truncate">ที่ปรึกษาด้านการซื้อ-ขายอสังหาริมทรัพย์มืออาชีพ</p>
        </div>'''

if old_info_block in html:
    html = html.replace(old_info_block, new_info_block)
    print("Replaced main info block successfully!")
else:
    print("Warning: old_info_block not matched directly")

# 3. Update Preview Modal info section
old_modal_info_block = '''          <div class="space-y-0.5 min-w-0 flex-1">
            <div id="modalAgentName" class="text-xs sm:text-sm font-bold text-slate-900 truncate">คุณนภชกร วรพัทธ์ภูดิท</div>
            <div id="modalZone" class="text-[9.5px] text-slate-500 truncate">📍 โซนวัชรพล-สายไหม</div>
            <!-- Matching Agent Only Action Pills with Lucide Icons -->
            <div class="pt-1 flex items-center gap-1.5 flex-wrap">
              <a id="modalCallLink" href="tel:0966458994" class="inline-flex items-center gap-1 text-[9.5px] font-semibold px-2 py-1 rounded-full bg-[#120808] text-white border border-amber-500/40 shadow-2xs">
                <i data-lucide="phone" class="w-2.5 h-2.5 text-emerald-400"></i>
                <span id="modalPhone" class="font-mono font-bold">096 645 8994</span>
              </a>
              <a id="modalLineLink" href="https://line.me/ti/p/~" target="_blank" class="inline-flex items-center gap-1 text-[9.5px] font-semibold px-2 py-1 rounded-full bg-white text-[#06C755] border border-[#06C755] shadow-2xs">
                <i data-lucide="message-circle" class="w-2.5 h-2.5"></i>
                <span>LINE OA</span>
              </a>
            </div>
          </div>'''

new_modal_info_block = '''          <div class="space-y-0.5 min-w-0 flex-1">
            <div id="modalAgentName" class="text-sm sm:text-base font-medium text-slate-900 truncate">คุณนภชกร วรพัทธ์ภูดิท</div>
            <p id="modalAgentTitle" class="text-[10.5px] text-slate-500 font-normal leading-tight truncate">ที่ปรึกษาด้านการซื้อ-ขายอสังหาริมทรัพย์มืออาชีพ</p>
            <div id="modalZone" class="text-[9.5px] text-slate-400 truncate pt-0.5">📍 โซนวัชรพล-สายไหม</div>
          </div>'''

if old_modal_info_block in html:
    html = html.replace(old_modal_info_block, new_modal_info_block)
    print("Replaced modal info block successfully!")

# 4. Safe JS updates for btnCall and btnLine (avoid null pointer exceptions)
html = html.replace(
    'document.getElementById("btnCall").href = `tel:${a.phoneRaw}`;',
    'const btnCall = document.getElementById("btnCall"); if (btnCall) btnCall.href = `tel:${a.phoneRaw}`;'
)
html = html.replace(
    'document.getElementById("txtPhone").innerText = a.phoneFormatted;',
    'const txtPhone = document.getElementById("txtPhone"); if (txtPhone) txtPhone.innerText = a.phoneFormatted;'
)
html = html.replace(
    'document.getElementById("txtLine").innerText = `LINE OA`;',
    'const txtLine = document.getElementById("txtLine"); if (txtLine) txtLine.innerText = `LINE OA`;'
)

# Modal title in openPreviewModal
html = html.replace(
    'document.getElementById("modalZone").innerText = a.zone;',
    '''document.getElementById("modalZone").innerText = a.zone;
      const modalAgentTitle = document.getElementById("modalAgentTitle");
      if (modalAgentTitle) modalAgentTitle.innerText = a.clientTitle || "ที่ปรึกษาด้านการซื้อ-ขายอสังหาริมทรัพย์มืออาชีพ";'''
)
html = html.replace(
    'document.getElementById("modalPhone").innerText = a.phoneFormatted;',
    'const modalPhone = document.getElementById("modalPhone"); if (modalPhone) modalPhone.innerText = a.phoneFormatted;'
)

with open(path, "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: Daimond.svg and clean typography updated without errors!")
