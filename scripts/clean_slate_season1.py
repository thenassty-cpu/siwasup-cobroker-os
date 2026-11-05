# -*- coding: utf-8 -*-
import json
import re
import shutil
from pathlib import Path

ROOT = Path(r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os")

# ==============================================================================
# 1. CLEAN SLATE IN siwasup_agents.js (All 0 Points, Alpha 6 at Top)
# ==============================================================================
agents_path = ROOT / "siwasup_agents.js"
text = agents_path.read_text(encoding="utf-8")

m = re.search(
    r"const SIWASUP_AGENTS_SEED = (\[.*?\]);\s*\n\s*// 4\. IN-MEMORY STATE",
    text,
    flags=re.DOTALL,
)
if not m:
    raise RuntimeError("Could not find SIWASUP_AGENTS_SEED in siwasup_agents.js")

agents = json.loads(m.group(1))
alpha_codes = {"S90", "S94", "S98", "S113", "S117", "S120"}

for a in agents:
    a["activityPoints"] = 0
    a["performancePoints"] = 0
    a["totalPoints"] = 0
    a["tierId"] = "trainee"
    a["tierName"] = "Trainee"
    a["tierIcon"] = "🌱"
    if a["code"] in alpha_codes:
        a["isAlpha"] = True
        a["group"] = "Siwasup Alpha Agent"

def sort_key(a):
    num = int(re.sub(r"\D", "", a["code"]) or 999)
    return (0 if a.get("isAlpha") else 1, num)

agents.sort(key=sort_key)

new_seed_json = json.dumps(agents, ensure_ascii=False, indent=2)
new_seed_str = "const SIWASUP_AGENTS_SEED = " + new_seed_json + ";\n\n  // 4. IN-MEMORY STATE"
text = text[: m.start()] + new_seed_str + text[m.end() :]

# Replace initAgents & storage keys to force Clean Slate on all browsers
text = re.sub(
    r"const STORAGE_KEY_AGENTS = '[^']+';\s*const STORAGE_KEY_TXS = '[^']+';\s*function initAgents\(\) \{.*?\n  \}",
    """const STORAGE_KEY_AGENTS = 'siwasup_agents_season1_clean_v3';
  const STORAGE_KEY_TXS = 'siwasup_point_txs_season1_clean_v3';

  function initAgents() {
    try {
      // ล้างกระดานข้อมูลจำลองเก่าทั้งหมดอัตโนมัติ (Clean Slate Migration)
      localStorage.removeItem('siwasup_agents_cache_v1');
      localStorage.removeItem('siwasup_point_transactions_v1');
      if (localStorage.getItem('siwasup_my_agent_ref') === 'S22') {
        localStorage.setItem('siwasup_my_agent_ref', 'S90');
      }
    } catch (e) {}

    // โหลดฐานข้อมูลเริ่มต้นที่ 0 แต้ม แล้วคำนวณเฉพาะธุรกรรมจริงที่เกิดขึ้นใน Season 1
    currentAgents = JSON.parse(JSON.stringify(SIWASUP_AGENTS_SEED));
    applyTransactionsToAgents();
    saveAgentsToCache();
  }""",
    text,
    flags=re.DOTALL,
)

# Sort leaderboard so Alpha 6 are on top when tied at 0 points
old_lb = """    list.sort((a, b) => {
      if (sortBy === 'activity') return (b.activityPoints || 0) - (a.activityPoints || 0);
      if (sortBy === 'performance') return (b.performancePoints || 0) - (a.performancePoints || 0);
      return (b.totalPoints || 0) - (a.totalPoints || 0);
    });"""

new_lb = """    list.sort((a, b) => {
      let diff = 0;
      if (sortBy === 'activity') diff = (b.activityPoints || 0) - (a.activityPoints || 0);
      else if (sortBy === 'performance') diff = (b.performancePoints || 0) - (a.performancePoints || 0);
      else diff = (b.totalPoints || 0) - (a.totalPoints || 0);
      if (diff !== 0) return diff;
      // กรณีแต้มเท่ากัน (เริ่มต้น Season 1 ที่ 0 แต้ม) ให้แสดงกลุ่ม Alpha Squad 6 ท่านขึ้นก่อนเสมอ
      const alphaDiff = (b.isAlpha ? 1 : 0) - (a.isAlpha ? 1 : 0);
      if (alphaDiff !== 0) return alphaDiff;
      return (parseInt(a.code.replace(/\\D/g, '')) || 999) - (parseInt(b.code.replace(/\\D/g, '')) || 999);
    });"""

if old_lb in text:
    text = text.replace(old_lb, new_lb)

agents_path.write_text(text, encoding="utf-8")
print("[1/3] Updated siwasup_agents.js -> Clean Slate 0 pts, Top 6:", [a["code"] for a in agents[:6]])

# ==============================================================================
# 2. UPDATE modals.js (Remove fake simulator buttons, set clean 0 state & S90)
# ==============================================================================
modals_path = ROOT / "modals.js"
mtext = modals_path.read_text(encoding="utf-8")

mtext = mtext.replace("🥇 S22 - เจ็ม", "🌱 S90 - นัญ")
mtext = mtext.replace('id="agent-ref-input" value="S22"', 'id="agent-ref-input" value="S90"')
mtext = mtext.replace('id="vinyl-agent-search" value="S22"', 'id="vinyl-agent-search" value="S90"')
mtext = mtext.replace("เหยี่ยว S22", "เหยี่ยวเวหา")

# Replace initial profile hero card default in modals.js
old_hero = """              <div class="relative shrink-0">
                <img id="profile-3d-badge-img" src="assets/characters/badge_eagle.png" alt="Badge" class="w-16 h-16 object-contain drop-shadow-md">
                <div id="profile-avatar-circle" class=" -bottom-1 -right-1 px-1.5 py-0.5 rounded-full bg-slate-900 text-amber-300 font-mono font-black text-[10px] border border-amber-400 shadow-xs">
                  S22
                </div>
              </div>
              <div class="min-w-0 flex-1">
                <div class="flex items-center gap-1.5 flex-wrap">
                  <span id="profile-nickname" class="font-black text-base text-gray-900">เจ็ม</span>
                  <span id="profile-code" class="text-xs font-mono font-bold bg-neutral-900 text-white px-2 py-0.5 rounded-md shadow-2xs">S22</span>
                  <span id="profile-tier-badge" class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800 border border-amber-300">Gold</span>
                </div>
                <div id="profile-fullname" class="text-xs text-gray-600 truncate mt-0.5">นางสาวกัญญา คำทรศิริวัฒน์</div>
                <div class="flex items-center gap-2 text-[10px] text-gray-500 mt-1">
                  <span>📅 เริ่มงาน: <strong id="profile-start-date" class="text-gray-700">8/3/2566</strong></span>
                  <span>•</span>
                  <span>💬 LINE: <strong id="profile-line" class="text-gray-700">ggemmie</strong></span>
                </div>
              </div>"""

new_hero = """              <div class="relative shrink-0">
                <img id="profile-3d-badge-img" src="assets/characters/badge_bear.png" alt="Badge" class="w-16 h-16 object-contain drop-shadow-md">
                <div id="profile-avatar-circle" class=" -bottom-1 -right-1 px-1.5 py-0.5 rounded-full bg-slate-900 text-amber-300 font-mono font-black text-[10px] border border-amber-400 shadow-xs">
                  S90
                </div>
              </div>
              <div class="min-w-0 flex-1">
                <div class="flex items-center gap-1.5 flex-wrap">
                  <span id="profile-nickname" class="font-black text-base text-gray-900">นัญ</span>
                  <span id="profile-code" class="text-xs font-mono font-bold bg-neutral-900 text-white px-2 py-0.5 rounded-md shadow-2xs">S90</span>
                  <span id="profile-tier-badge" class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-slate-100 text-slate-800 border border-slate-300">🌱 Trainee</span>
                </div>
                <div id="profile-fullname" class="text-xs text-gray-600 truncate mt-0.5">นางสาว อนัญญา สาททอง</div>
                <div class="flex items-center gap-2 text-[10px] text-gray-500 mt-1">
                  <span>📅 เริ่มงาน: <strong id="profile-start-date" class="text-gray-700">29.05.2568</strong></span>
                  <span>•</span>
                  <span>💬 LINE: <strong id="profile-line" class="text-gray-700">Run4536</strong></span>
                </div>
              </div>"""

if old_hero in mtext:
    mtext = mtext.replace(old_hero, new_hero)

mtext = mtext.replace(
    '<span id="profile-active-tier-name" class="text-emerald-400 font-mono font-bold">🦅 พญาอินทรี</span>',
    '<span id="profile-active-tier-name" class="text-emerald-400 font-mono font-bold">🐻 หมีตื่นตัว</span>',
)
mtext = mtext.replace(
    '<span id="profile-act-checkpoint-label" class="font-mono font-bold text-emerald-300">75 / 100 แต้ม</span>',
    '<span id="profile-act-checkpoint-label" class="font-mono font-bold text-emerald-300">0 / 100 แต้ม</span>',
)
mtext = mtext.replace(
    'id="profile-act-evo-bar" class="bg-gradient-to-r from-emerald-500 to-teal-400 h-full rounded-full transition-all duration-500" style="width: 75%;"',
    'id="profile-act-evo-bar" class="bg-gradient-to-r from-emerald-500 to-teal-400 h-full rounded-full transition-all duration-500" style="width: 0%;"',
)
mtext = mtext.replace(
    '<span id="profile-perf-checkpoint-label" class="font-mono font-bold text-amber-300">210 / 300 แต้ม</span>',
    '<span id="profile-perf-checkpoint-label" class="font-mono font-bold text-amber-300">0 / 300 แต้ม</span>',
)
mtext = mtext.replace(
    'id="profile-perf-evo-bar" class="bg-gradient-to-r from-amber-500 via-yellow-400 to-orange-400 h-full rounded-full transition-all duration-500" style="width: 70%;"',
    'id="profile-perf-evo-bar" class="bg-gradient-to-r from-amber-500 via-yellow-400 to-orange-400 h-full rounded-full transition-all duration-500" style="width: 0%;"',
)
mtext = mtext.replace(
    '<div id="profile-act-pts" class="text-xl font-black text-emerald-800 font-mono">75</div>',
    '<div id="profile-act-pts" class="text-xl font-black text-emerald-800 font-mono">0</div>',
)
mtext = mtext.replace(
    '<div id="profile-perf-pts" class="text-xl font-black text-blue-800 font-mono">210</div>',
    '<div id="profile-perf-pts" class="text-xl font-black text-blue-800 font-mono">0</div>',
)
mtext = mtext.replace(
    '<div id="profile-total-pts" class="text-2xl font-black font-mono text-amber-300">285</div>',
    '<div id="profile-total-pts" class="text-2xl font-black font-mono text-amber-300">0</div>',
)

# Remove the fake simulator button panel in modals.js and replace with authentic automated tracking notice
sim_block_pattern = r"<!-- ⚡ Live Activity & Evolution Simulator -->\s*<div class=\"pt-2 border-t border-slate-800 space-y-1\.5\">.*?</div>\s*</div>"
clean_tracking_notice = """<!-- 🛡️ Automated Real-Action Scoring Notice -->
            <div class="pt-2 border-t border-slate-800">
              <div class="p-2 rounded-lg bg-slate-900/90 border border-slate-700/80 text-[9.5px] text-slate-300 leading-relaxed flex items-start gap-2">
                <span class="text-amber-400 shrink-0 mt-0.5">🛡️</span>
                <div>
                  <strong class="text-amber-300">ระบบคำนวณแต้มอัตโนมัติ (Verified Action Only):</strong> คะแนนจะเพิ่มขึ้นตามกิจกรรมจริงในระบบเท่านั้น เช่น สแกนเข้าประชุม (+10), แชร์ลิงก์บ้านให้ลูกค้า (+5), ส่งภาพติดป้าย GPS (+15), พาชมบ้าน (+50) และปิดใบจอง (+100)
                </div>
              </div>
            </div>"""

mtext, n_sub = re.subn(sim_block_pattern, clean_tracking_notice, mtext, flags=re.DOTALL)
print(f"[2/3] Updated modals.js (removed simulator block: {n_sub})")
modals_path.write_text(mtext, encoding="utf-8")

# ==============================================================================
# 3. UPDATE index.html & catalog.html
# ==============================================================================
index_path = ROOT / "index.html"
itext = index_path.read_text(encoding="utf-8")

# Header button default S22 -> S90 (นัญ)
old_hdr_btn = """              <img id="header-profile-3d-badge" src="assets/characters/badge_eagle.png" alt="Badge" class="w-3.5 h-3.5 object-contain">
              <span class="px-1 py-0.2 rounded bg-[#C2A460]/20 text-[#E5C985] text-[9px] font-bold" id="header-profile-avatar">S22</span>
              <span id="bar-profile-btn-text" class="hidden sm:inline font-medium">เจ็ม</span>"""

new_hdr_btn = """              <img id="header-profile-3d-badge" src="assets/characters/badge_bear.png" alt="Badge" class="w-3.5 h-3.5 object-contain">
              <span class="px-1 py-0.2 rounded bg-[#C2A460]/20 text-[#E5C985] text-[9px] font-bold" id="header-profile-avatar">S90</span>
              <span id="bar-profile-btn-text" class="hidden sm:inline font-medium">นัญ</span>"""

if old_hdr_btn in itext:
    itext = itext.replace(old_hdr_btn, new_hdr_btn)

# Group dropdown options in renderMyProfile so Alpha 6 are clearly grouped at the top
old_switcher_js = """      // Populate Switcher Dropdown
      const switcher = document.getElementById('profile-agent-switcher');
      if (switcher) {
        const all = window.SiwasupAgents.getActive();
        switcher.innerHTML = all.map(a => `
          <option value="${a.code}" ${a.code === agent.code ? 'selected' : ''}>
            ${a.code} - ${a.nickname || a.name} (${a.tierIcon} ${a.totalPoints} แต้ม)
          </option>
        `).join('');
      }"""

new_switcher_js = """      // Populate Switcher Dropdown (Alpha 6 Pioneers grouped at Top)
      const switcher = document.getElementById('profile-agent-switcher');
      if (switcher) {
        const all = window.SiwasupAgents.getActive();
        const alphas = all.filter(a => a.isAlpha);
        const others = all.filter(a => !a.isAlpha);
        const renderOpt = (a) => `
          <option value="${a.code}" ${a.code === agent.code ? 'selected' : ''}>
            ${a.code} - ${a.nickname || a.name} (${a.tierIcon} ${a.totalPoints} แต้ม)
          </option>
        `;
        switcher.innerHTML = `
          <optgroup label="🌟 ทีมบุกเบิก (Alpha Squad 6 ท่าน)">
            ${alphas.map(renderOpt).join('')}
          </optgroup>
          <optgroup label="📋 ทำเนียบตัวแทนศิวาทรัพย์ทั้งหมด (Season 1)">
            ${others.map(renderOpt).join('')}
          </optgroup>
        `;
      }"""

if old_switcher_js in itext:
    itext = itext.replace(old_switcher_js, new_switcher_js)

# Fix element ID mismatches in renderMyProfile so all fields update cleanly
itext = itext.replace(
    "const codePill = document.getElementById('profile-code-pill');",
    "const codePill = document.getElementById('profile-code-pill') || document.getElementById('profile-code');",
)
itext = itext.replace(
    "const actEl = document.getElementById('profile-activity-pts');",
    "const actEl = document.getElementById('profile-activity-pts') || document.getElementById('profile-act-pts');",
)
itext = itext.replace(
    "const badgeEl = document.getElementById('profile-animal-badge');",
    "const badgeEl = document.getElementById('profile-animal-badge'); const activeTierNameEl = document.getElementById('profile-active-tier-name'); if (activeTierNameEl) activeTierNameEl.textContent = `${arch.icon} ${arch.shortName || arch.name}`;",
)

# Replace fallback 'S22' with 'S90' in JS logic
itext = itext.replace("window.SiwasupAgents.find('S22')", "window.SiwasupAgents.find('S90')")
itext = itext.replace("localStorage.getItem('siwasup_my_agent_ref') || 'S22'", "localStorage.getItem('siwasup_my_agent_ref') || 'S90'")
itext = itext.replace("refInput ? refInput.value.trim() : 'S22'", "refInput ? refInput.value.trim() : 'S90'")
itext = itext.replace("encodeURIComponent(rawRef || 'S22')", "encodeURIComponent(rawRef || 'S90')")
itext = itext.replace("select ? select.value : 'S22'", "select ? select.value : 'S90'")

index_path.write_text(itext, encoding="utf-8")
shutil.copy2(index_path, ROOT / "catalog.html")
print("[3/3] Updated index.html and synced catalog.html!")
