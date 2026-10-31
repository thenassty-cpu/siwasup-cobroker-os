import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"

for fname in ["index.html", "catalog.html"]:
    fpath = os.path.join(BASE_DIR, fname)
    if not os.path.exists(fpath):
        continue

    with open(fpath, "r", encoding="utf-8") as f:
        html = f.read().replace("\r\n", "\n")

    # 1. Add TTB to bank select dropdown if not already present
    old_sel = '<option value="GSB">GSB</option>'
    new_sel = '<option value="GSB">GSB</option>\n                      <option value="TTB">TTB</option>'
    if '<option value="TTB">TTB</option>' not in html and old_sel in html:
        html = html.replace(old_sel, new_sel, 1)

    # 2. Add TTB to bank quick chips if not already present
    old_chip = """<button type="button" onclick="selectBankChip('GSB', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-neutral-800 hover:bg-neutral-100 shadow-xs shrink-0 inline-flex items-center">GSB</button>"""
    new_chip = old_chip + """\n              <button type="button" onclick="selectBankChip('TTB', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-neutral-800 hover:bg-neutral-100 shadow-xs shrink-0 inline-flex items-center">TTB</button>"""
    if "selectBankChip('TTB'" not in html and old_chip in html:
        html = html.replace(old_chip, new_chip, 1)

    # 3. Add Bua Verified badge next to property code on cards
    old_code_div = '<div class="text-[11px] text-neutral-500 font-mono text-right">รหัสทรัพย์: ${p.id}</div>'
    new_code_div = """<div class="flex items-center justify-between text-[11px]">
                  ${p.bua_verified && currentMode !== 'client' ? '<span class="px-2 py-0.5 rounded-md bg-emerald-50 text-emerald-700 border border-emerald-200 font-bold text-[10px]">✓ บัวคัดแล้ว</span>' : '<span></span>'}
                  <span class="text-neutral-500 font-mono">รหัสทรัพย์: ${p.id}</span>
                </div>"""
    if old_code_div in html:
        html = html.replace(old_code_div, new_code_div)

    # 4. Add ⭐ Alpha Agent badge & search filter in 125-agent leaderboard
    old_lb_search = """      if (currentLeaderboardQuery) {
        list = list.filter(a => 
          a.code.toLowerCase().includes(currentLeaderboardQuery) ||
          (a.nickname && a.nickname.toLowerCase().includes(currentLeaderboardQuery)) ||
          (a.name && a.name.toLowerCase().includes(currentLeaderboardQuery))
        );
      }"""
    new_lb_search = """      if (currentLeaderboardQuery) {
        list = list.filter(a => 
          a.code.toLowerCase().includes(currentLeaderboardQuery) ||
          (a.nickname && a.nickname.toLowerCase().includes(currentLeaderboardQuery)) ||
          (a.name && a.name.toLowerCase().includes(currentLeaderboardQuery)) ||
          (currentLeaderboardQuery.includes('alpha') && a.isAlpha)
        );
      }"""
    if old_lb_search in html:
        html = html.replace(old_lb_search, new_lb_search)

    old_tier_span = """                        <span class="px-1.5 py-0.2 rounded bg-[#FAF7F0] border border-[#E5DEC9] text-[#8C7038] text-[9px] font-semibold">
                          ✦ ${a.tierName}
                        </span>"""
    new_tier_span = old_tier_span + """
                        ${a.isAlpha ? `<span class="px-1.5 py-0.5 rounded-full bg-neutral-900 text-[#E5C985] border border-[#C2A460] text-[9px] font-bold">⭐ Alpha Agent</span>` : ''}"""
    if "⭐ Alpha Agent" not in html and old_tier_span in html:
        html = html.replace(old_tier_span, new_tier_span)

    # 5. Update script cache-busters so browsers immediately fetch the updated JS bundles
    import re
    html = re.sub(r'src="siwasup_all_properties\.js[^"]*"', 'src="siwasup_all_properties.js?v=20261031-npa980"', html)
    html = re.sub(r'src="modals\.js[^"]*"', 'src="modals.js?v=20261031-relay2slot"', html)
    html = re.sub(r'src="siwasup_agents\.js[^"]*"', 'src="siwasup_agents.js?v=20261031-clean"', html)

    with open(fpath, "w", encoding="utf-8", newline="\r\n") as f:
        f.write(html)

    print(f"[OK] Patched {fname} successfully!")
