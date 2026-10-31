import re

html_path = 'C:/Users/ITss-Advice/Documents/GitHub/siwasup-cobroker-os/property_curator.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# Replace Quick Filter Pills HTML to include group buttons
old_pills = """        <button onclick="setTabFilter('all')" id="tab-all" class="tab-btn px-3.5 py-2 rounded-xl bg-slate-900 text-white whitespace-nowrap shadow-sm">
          ทั้งหมด (<span id="tab-count-all">0</span>)
        </button>
        <button onclick="setTabFilter('selected')" id="tab-selected" class="tab-btn px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 whitespace-nowrap transition">
          ❤️ คัดเลือกแล้ว (<span id="tab-count-selected">0</span>)
        </button>
        <button onclick="setTabFilter('unselected')" id="tab-unselected" class="tab-btn px-3.5 py-2 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 whitespace-nowrap transition">
          🤍 ยังไม่เลือก (<span id="tab-count-unselected">0</span>)
        </button>"""

new_pills = """        <button onclick="setTabFilter('all')" id="tab-all" class="tab-btn px-3 py-1.5 rounded-xl bg-slate-900 text-white whitespace-nowrap shadow-sm font-semibold">
          ทั้งหมด (<span id="tab-count-all">0</span>)
        </button>
        <button onclick="setGroupFilter('flagged_red')" id="btn-group-red" class="group-btn px-3 py-1.5 rounded-xl bg-rose-100 hover:bg-rose-200 text-rose-800 whitespace-nowrap transition font-semibold flex items-center gap-1 border border-rose-200">
          <span>🔴 ทบทวนด่วน (8)</span>
        </button>
        <button onclick="setGroupFilter('new_green')" id="btn-group-green" class="group-btn px-3 py-1.5 rounded-xl bg-emerald-100 hover:bg-emerald-200 text-emerald-800 whitespace-nowrap transition font-semibold flex items-center gap-1 border border-emerald-200">
          <span>🟢 ของเข้าใหม่ (12)</span>
        </button>
        <button onclick="setGroupFilter('npa_vault')" id="btn-group-npa" class="group-btn px-3 py-1.5 rounded-xl bg-indigo-100 hover:bg-indigo-200 text-indigo-800 whitespace-nowrap transition font-semibold flex items-center gap-1 border border-indigo-200">
          <span>💎 ทรัพย์ NPA (671)</span>
        </button>
        <button onclick="setTabFilter('selected')" id="tab-selected" class="tab-btn px-3 py-1.5 rounded-xl bg-rose-50 hover:bg-rose-100 text-rose-700 whitespace-nowrap transition font-bold border border-rose-200">
          ❤️ คัดเลือกแล้ว (<span id="tab-count-selected">0</span>)
        </button>"""

if old_pills in html:
    html = html.replace(old_pills, new_pills)
    print("Replaced filter pills successfully.")
else:
    print("Could not find old pills exactly, checking regex...")

# Update JS data loading to check ALL_CURATION_DATA
old_loader = """      // 2. Read dataset from siwasup_all_properties.js
      if (typeof ALL_PROPERTIES_DATA !== 'undefined' && Array.isArray(ALL_PROPERTIES_DATA)) {
        allProperties = ALL_PROPERTIES_DATA;
      } else {
        console.warn('ALL_PROPERTIES_DATA not found. Trying fetch or dummy data.');
        allProperties = [];
      }"""

new_loader = """      // 2. Read dataset from all_curation_properties.js (801 items) or fallback
      if (typeof ALL_CURATION_DATA !== 'undefined' && Array.isArray(ALL_CURATION_DATA)) {
        allProperties = ALL_CURATION_DATA;
      } else if (typeof ALL_PROPERTIES_DATA !== 'undefined' && Array.isArray(ALL_PROPERTIES_DATA)) {
        allProperties = ALL_PROPERTIES_DATA;
      } else {
        allProperties = [];
      }"""

if old_loader in html:
    html = html.replace(old_loader, new_loader)
    print("Updated JS dataset loader.")

# Add currentGroup state and filter handling
old_state = "    let currentTab = 'all'; // 'all' | 'selected' | 'unselected'\n    let currentSearch = '';"
new_state = "    let currentTab = 'all'; // 'all' | 'selected' | 'unselected'\n    let currentGroup = 'all'; // 'all' | 'flagged_red' | 'new_green' | 'npa_vault' | 'general'\n    let currentSearch = '';"

if old_state in html:
    html = html.replace(old_state, new_state)

# Add setGroupFilter function
set_group_fn = """
    function setGroupFilter(group) {
      currentGroup = (currentGroup === group) ? 'all' : group;
      currentTab = 'all'; // reset tab
      
      // Update UI buttons
      document.querySelectorAll('.group-btn').forEach(btn => {
        btn.classList.remove('ring-2', 'ring-offset-1', 'scale-105');
      });
      document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('bg-slate-900', 'text-white');
        btn.classList.add('bg-slate-100', 'text-slate-700');
      });
      
      if (currentGroup !== 'all') {
        const activeBtn = document.getElementById(`btn-group-${group.replace('flagged_', '').replace('new_', '').replace('_vault', '')}`);
        if (activeBtn) {
          activeBtn.classList.add('ring-2', 'ring-offset-1', 'scale-105');
        }
      } else {
        document.getElementById('tab-all').classList.add('bg-slate-900', 'text-white');
      }
      
      applyFilters();
    }
"""

if "function setTabFilter(tab) {" in html:
    html = html.replace("function setTabFilter(tab) {", set_group_fn + "\n    function setTabFilter(tab) {")
    print("Injected setGroupFilter function.")

# Update getFilteredProperties to include currentGroup check
old_filter_check = """        // Tab filter
        if (currentTab === 'selected' && !isSelected) return false;
        if (currentTab === 'unselected' && isSelected) return false;"""

new_filter_check = """        // Tab filter
        if (currentTab === 'selected' && !isSelected) return false;
        if (currentTab === 'unselected' && isSelected) return false;

        // Group filter (Red / Green / NPA)
        if (currentGroup !== 'all' && item.group !== currentGroup) return false;"""

if old_filter_check in html:
    html = html.replace(old_filter_check, new_filter_check)
    print("Updated getFilteredProperties filter checks.")

# Update card rendering to display beautiful colored ribbons & captions
old_card_badge = """              <!-- Category Badge -->
              <div class="absolute top-3 left-3 flex flex-wrap gap-1.5">
                <span class="bg-slate-900/80 backdrop-blur-md text-white text-[11px] px-2.5 py-0.5 rounded-lg font-medium">
                  ${item.category || 'อสังหาฯ'}
                </span>
                ${isSoldout ? `
                  <span class="bg-red-600/90 backdrop-blur-md text-white text-[11px] px-2.5 py-0.5 rounded-lg font-semibold shadow-sm">
                    ขายแล้ว
                  </span>
                ` : ''}
              </div>"""

new_card_badge = """              <!-- Category & Colored Status Ribbons -->
              <div class="absolute top-3 left-3 flex flex-col gap-1 z-10">
                <div class="flex items-center gap-1.5 flex-wrap">
                  <span class="bg-slate-950/80 backdrop-blur-md text-white text-[11px] px-2.5 py-0.5 rounded-lg font-semibold border border-white/20 shadow-xs">
                    ${item.category || 'อสังหาฯ'}
                  </span>
                  ${item.ribbon === 'red' ? `
                    <span class="bg-rose-600 text-white text-[10px] px-2 py-0.5 rounded-lg font-black shadow-md flex items-center gap-1 animate-pulse">
                      <span>🔴</span><span>ทบทวน: เว็บเดิมถอดออก</span>
                    </span>
                  ` : item.ribbon === 'green' ? `
                    <span class="bg-emerald-600 text-white text-[10px] px-2 py-0.5 rounded-lg font-black shadow-md flex items-center gap-1">
                      <span>🟢</span><span>ใหม่ล่าสุด (New In)</span>
                    </span>
                  ` : item.ribbon === 'blue' ? `
                    <span class="bg-indigo-600 text-white text-[10px] px-2 py-0.5 rounded-lg font-bold shadow-xs">
                      <span>💎</span><span>NPA แบงก์</span>
                    </span>
                  ` : ''}
                </div>
              </div>"""

if old_card_badge in html:
    html = html.replace(old_card_badge, new_card_badge)
    print("Updated card badge rendering.")

# Add flag_reason caption callout below title if flagged
old_card_title = """                <h3 class="text-sm font-semibold text-slate-900 line-clamp-2 leading-snug group-hover:text-amber-600 transition-colors" title="${item.title}">
                  ${item.title}
                </h3>"""

new_card_title = """                <h3 class="text-sm font-semibold text-slate-900 line-clamp-2 leading-snug group-hover:text-amber-600 transition-colors" title="${item.title}">
                  ${item.title}
                </h3>
                ${item.ribbon === 'red' ? `
                  <div class="mt-2 p-2 rounded-xl bg-rose-50 border border-rose-200 text-[10.5px] text-rose-800 leading-snug font-medium">
                    <span class="font-bold">⚠️ แจ้งเตือน:</span> ${item.flag_reason || 'เว็บเดิมถอดออกแล้ว โปรดตรวจสถานะว่ายังขายได้ไหม'}
                  </div>
                ` : item.ribbon === 'green' ? `
                  <div class="mt-2 p-1.5 rounded-xl bg-emerald-50 border border-emerald-200 text-[10.5px] text-emerald-800 leading-snug font-medium">
                    <span class="font-bold">✨ ของเข้าใหม่:</span> เพิ่งลงในเว็บ กด ❤️ เพื่อดึงเข้าพอร์ตใหม่
                  </div>
                ` : ''}"""

if old_card_title in html:
    html = html.replace(old_card_title, new_card_title)
    print("Added card title callouts.")

# Add image fallback
html = html.replace(
    "onerror=\"this.src='https://via.placeholder.com/400x300?text=Image+Unavailable'\"",
    "onerror=\"this.onerror=null; this.src='https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=600';\""
)

# Update dynamic counts in updateHeaderBadges
old_badges = """      document.getElementById('selected-count-badge').textContent = selectedCount;
      document.getElementById('total-count-badge').textContent = totalCount;

      document.getElementById('tab-count-all').textContent = totalCount;
      document.getElementById('tab-count-selected').textContent = selectedCount;
      document.getElementById('tab-count-unselected').textContent = unselectedCount;"""

new_badges = """      document.getElementById('selected-count-badge').textContent = selectedCount;
      document.getElementById('total-count-badge').textContent = totalCount;

      document.getElementById('tab-count-all').textContent = totalCount;
      document.getElementById('tab-count-selected').textContent = selectedCount;
      
      const redCount = allProperties.filter(p => p.group === 'flagged_red').length;
      const greenCount = allProperties.filter(p => p.group === 'new_green').length;
      const npaCount = allProperties.filter(p => p.group === 'npa_vault').length;
      
      const bRed = document.getElementById('badge-count-red');
      if (bRed) bRed.textContent = redCount;
      const bGreen = document.getElementById('badge-count-green');
      if (bGreen) bGreen.textContent = greenCount;
      const bNpa = document.getElementById('badge-count-npa');
      if (bNpa) bNpa.textContent = npaCount;"""

if old_badges in html:
    html = html.replace(old_badges, new_badges)
    print("Updated dynamic header badges.")

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("property_curator.html fully patched with Master Guidance & Ribbons!")
