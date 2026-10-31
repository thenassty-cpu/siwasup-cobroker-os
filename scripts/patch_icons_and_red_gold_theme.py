import re

path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\agent_profile.html"
with open(path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Preview Modal: replace raw modalPhone with phone & chat pills identical to agent only
old_modal_info_pattern = r'<div id="modalPhone"[^>]+>.*?</div>'
new_modal_info = '''<!-- Matching Agent Only Action Pills with Lucide Icons -->
            <div class="pt-1 flex items-center gap-1.5 flex-wrap">
              <a id="modalCallLink" href="tel:0966458994" class="inline-flex items-center gap-1 text-[9.5px] font-semibold px-2 py-1 rounded-full bg-[#120808] text-white border border-amber-500/40 shadow-2xs">
                <i data-lucide="phone" class="w-2.5 h-2.5 text-emerald-400"></i>
                <span id="modalPhone" class="font-mono font-bold">096 645 8994</span>
              </a>
              <a id="modalLineLink" href="https://line.me/ti/p/~" target="_blank" class="inline-flex items-center gap-1 text-[9.5px] font-semibold px-2 py-1 rounded-full bg-white text-[#06C755] border border-[#06C755] shadow-2xs">
                <i data-lucide="message-circle" class="w-2.5 h-2.5"></i>
                <span>LINE OA</span>
              </a>
            </div>'''

html = re.sub(old_modal_info_pattern, new_modal_info, html)

# 2. Update Modal Bottom Actions: replace emoji with official lucide icons
old_modal_actions = '''        <!-- Mini Actions -->
        <div class="grid grid-cols-2 gap-1.5 text-center text-[10px] font-semibold">
          <div id="modalCallBtn" class="p-1.5 rounded-xl bg-slate-950 text-white font-mono">096 645 8994</div>
          <div class="p-1.5 rounded-xl bg-white text-[#06C755] border border-[#06C755]">💬 LINE OA</div>
        </div>'''

new_modal_actions = '''<!-- Mini Actions with Phone & Chat Icons -->
        <div class="grid grid-cols-2 gap-1.5 text-center text-[10.5px] font-semibold">
          <a id="modalBottomCall" href="tel:0966458994" class="p-2 rounded-xl bg-[#120808] hover:bg-slate-800 text-white font-mono flex items-center justify-center gap-1.5 border border-amber-500/40 shadow-xs">
            <i data-lucide="phone" class="w-3.5 h-3.5 text-emerald-400"></i>
            <span id="modalCallBtn">096 645 8994</span>
          </a>
          <a id="modalBottomLine" href="https://line.me/ti/p/~" target="_blank" class="p-2 rounded-xl bg-white hover:bg-emerald-50 text-[#06C755] border border-[#06C755] flex items-center justify-center gap-1.5 font-bold shadow-xs">
            <i data-lucide="message-circle" class="w-3.5 h-3.5 text-[#06C755]"></i>
            <span>LINE OA</span>
          </a>
        </div>'''

html = html.replace(old_modal_actions, new_modal_actions)

# 3. Update Client Mode bottom action in main card: add both Phone and LINE OA side-by-side with icons
old_client_call = '''        <!-- Button 2: Direct call for client (Client Mode) -->
        <a id="btnClientCall" href="tel:0966458994" class="hidden w-full py-2.5 sm:py-3 rounded-2xl bg-slate-900 hover:bg-slate-800 text-white font-semibold text-xs flex items-center justify-center gap-2 transition shadow-xs active:scale-95">
          <i data-lucide="phone-call" class="w-4 h-4 text-emerald-400"></i>
          <span id="btnClientCallText">ติดต่อ 096 645 8994</span>
        </a>'''

new_client_actions = '''<!-- Client Mode Contact Action Grid (Phone + LINE OA side-by-side with official icons) -->
        <div id="clientContactGrid" class="hidden grid grid-cols-2 gap-2">
          <a id="btnClientCall" href="tel:0966458994" class="py-2.5 sm:py-3 rounded-2xl bg-[#120808] hover:bg-[#220d0d] text-white font-semibold text-xs flex items-center justify-center gap-2 transition border border-amber-500/40 shadow-xs active:scale-95">
            <i data-lucide="phone" class="w-4 h-4 text-emerald-400"></i>
            <span id="btnClientCallText" class="font-mono font-bold">096 645 8994</span>
          </a>
          <a id="btnClientLine" href="https://line.me/ti/p/~" target="_blank" class="py-2.5 sm:py-3 rounded-2xl bg-white hover:bg-emerald-50 text-[#06C755] border border-[#06C755] font-semibold text-xs flex items-center justify-center gap-2 transition shadow-xs active:scale-95">
            <i data-lucide="message-circle" class="w-4 h-4 text-[#06C755]"></i>
            <span>แชท LINE OA</span>
          </a>
        </div>'''

html = html.replace(old_client_call, new_client_actions)

# 4. In setMode, toggle clientContactGrid
html = re.sub(
    r'btnClientCall\.classList\.remove\("hidden"\);',
    '''const clientContactGrid = document.getElementById("clientContactGrid");
        if (clientContactGrid) clientContactGrid.classList.remove("hidden");''',
    html
)
html = re.sub(
    r'btnClientCall\.classList\.add\("hidden"\);',
    '''const clientContactGrid = document.getElementById("clientContactGrid");
        if (clientContactGrid) clientContactGrid.classList.add("hidden");''',
    html
)

# 5. In changeAgent, update btnClientLine and modal links
old_agent_links = '''      document.getElementById("btnClientCall").href = `tel:${a.phoneRaw}`;
      document.getElementById("btnClientCallText").innerText = `ติดต่อ ${a.phoneFormatted}`;'''

new_agent_links = '''      document.getElementById("btnClientCall").href = `tel:${a.phoneRaw}`;
      document.getElementById("btnClientCallText").innerText = `${a.phoneFormatted}`;
      const btnClientLine = document.getElementById("btnClientLine");
      if (btnClientLine) {
        btnClientLine.href = a.lineId ? `https://line.me/ti/p/~${a.lineId}` : `https://line.me/R/ti/p/@813nyyia`;
      }'''

html = html.replace(old_agent_links, new_agent_links)

# Also in openPreviewModal, update modal call and line links
old_modal_js = '''      document.getElementById("modalPhone").innerText = a.phoneFormatted;
      document.getElementById("modalCallBtn").innerText = a.phoneFormatted;'''

new_modal_js = '''      document.getElementById("modalPhone").innerText = a.phoneFormatted;
      document.getElementById("modalCallBtn").innerText = a.phoneFormatted;
      const modalCallLink = document.getElementById("modalCallLink");
      if (modalCallLink) modalCallLink.href = `tel:${a.phoneRaw}`;
      const modalBottomCall = document.getElementById("modalBottomCall");
      if (modalBottomCall) modalBottomCall.href = `tel:${a.phoneRaw}`;
      const lineUrl = a.lineId ? `https://line.me/ti/p/~${a.lineId}` : `https://line.me/R/ti/p/@813nyyia`;
      const modalLineLink = document.getElementById("modalLineLink");
      if (modalLineLink) modalLineLink.href = lineUrl;
      const modalBottomLine = document.getElementById("modalBottomLine");
      if (modalBottomLine) modalBottomLine.href = lineUrl;'''

html = html.replace(old_modal_js, new_modal_js)

# 6. Apply Red & Gold Luxury Theme Touches
# 6A. Card top crown: Add an Auspicious Red & Gold gradient line at the top of the main card
old_card_tag = '<div class="bg-white border border-slate-200/90 rounded-[28px] sm:rounded-[36px] p-4 sm:p-6 shadow-sm space-y-4">'
new_card_tag = '''<div class="relative bg-white border border-amber-200/80 rounded-[28px] sm:rounded-[36px] p-4 sm:p-6 shadow-md shadow-amber-950/5 space-y-4 overflow-hidden">
      <!-- Auspicious Red & Royal Gold Top Crown Bar -->
      <div class="absolute top-0 left-0 right-0 h-[4px] bg-gradient-to-r from-[#991B1B] via-[#E5B54F] to-[#991B1B]"></div>'''

html = html.replace(old_card_tag, new_card_tag)

# 6B. Agent Code badge (S98) in Auspicious Red
old_agent_code = '<span id="agentCode" class="text-[10.5px] font-mono font-bold px-1.5 py-0.5 rounded bg-slate-100 text-slate-700">S98</span>'
new_agent_code = '<span id="agentCode" class="text-[10.5px] font-mono font-bold px-2 py-0.5 rounded-md bg-red-50 text-red-700 border border-red-200/80 shadow-2xs">S98</span>'
html = html.replace(old_agent_code, new_agent_code)

# 6C. Avatar Gold Ring
old_avatar = 'class="w-[86px] h-[86px] sm:w-24 sm:h-24 squircle-37 object-cover bg-slate-100 border border-slate-200/90 shadow-xs"'
new_avatar = 'class="w-[86px] h-[86px] sm:w-24 sm:h-24 squircle-37 object-cover bg-slate-100 border-2 border-[#E5B54F]/70 shadow-xs"'
html = html.replace(old_avatar, new_avatar)

# 6D. btnCall with rich obsidian-crimson & gold border
old_btn_call = '<a id="btnCall" href="tel:0966458994" class="inline-flex items-center gap-1.5 text-[11px] sm:text-xs font-semibold px-3 py-1.5 rounded-full bg-slate-950 hover:bg-slate-800 text-white transition shadow-xs">'
new_btn_call = '<a id="btnCall" href="tel:0966458994" class="inline-flex items-center gap-1.5 text-[11px] sm:text-xs font-semibold px-3 py-1.5 rounded-full bg-[#120808] hover:bg-[#251010] text-white border border-amber-500/40 transition shadow-xs">'
html = html.replace(old_btn_call, new_btn_call)

# 6E. Browse Catalog button with warm luxury gold glow
old_btn_cat = '<a id="btnBrowseCatalog" href="https://assets.siwasup.com/catalog.html" target="_blank" class="w-full py-2 sm:py-2.5 rounded-2xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs flex items-center justify-center gap-2 transition border border-slate-200">'
new_btn_cat = '<a id="btnBrowseCatalog" href="https://assets.siwasup.com/catalog.html" target="_blank" class="w-full py-2.5 sm:py-3 rounded-2xl bg-gradient-to-r from-amber-50 via-orange-50/60 to-amber-50 hover:from-amber-100 hover:to-orange-100 text-amber-950 font-bold text-xs flex items-center justify-center gap-2 transition border border-amber-300/80 shadow-2xs">'
html = html.replace(old_btn_cat, new_btn_cat)

with open(path, "w", encoding="utf-8") as f:
    f.write(html)

print("SUCCESS: Icons for client view and Red & Gold luxury theme fully patched!")
