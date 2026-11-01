import os

FILE_PATH = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\offline_log_exporter.html"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update Server Selector buttons
old_selector = """      <!-- Quick Server Selector -->
      <div class="flex items-center gap-2 bg-slate-900/90 p-1.5 rounded-2xl border border-slate-800 text-xs w-full md:w-auto">
        <button id="btnLocal" onclick="setServerPreset('local')" class="flex-1 md:flex-initial px-3 py-1.5 rounded-xl text-slate-300 hover:text-white transition">
          💻 เครื่องนี้ (Local:5005)
        </button>
        <button id="btnCloud" onclick="setServerPreset('cloud')" class="flex-1 md:flex-initial px-3 py-1.5 rounded-xl bg-amber-500 text-slate-950 font-bold transition">
          ☁️ คลาวด์ (Render / Live)
        </button>
      </div>"""

new_selector = """      <!-- Quick Server Selector (3 Presets) -->
      <div class="flex items-center gap-1.5 bg-slate-900/90 p-1.5 rounded-2xl border border-slate-800 text-xs w-full md:w-auto flex-wrap">
        <button id="btnCloud" onclick="setServerPreset('cloud')" class="px-3 py-1.5 rounded-xl bg-amber-500 text-slate-950 font-bold transition">
          ☁️ Render Cloud (Live 24 ชม.)
        </button>
        <button id="btnR2" onclick="setServerPreset('r2')" class="px-3 py-1.5 rounded-xl text-slate-300 hover:text-white transition">
          ⚡ Cloudflare R2 (สำรองถาวร)
        </button>
        <button id="btnLocal" onclick="setServerPreset('local')" class="px-3 py-1.5 rounded-xl text-slate-300 hover:text-white transition">
          💻 Local:5005
        </button>
      </div>"""

html = html.replace(old_selector, new_selector)

# 2. Update JavaScript logic for setServerPreset and fetchLogs
old_js = """    function setServerPreset(mode) {
      const urlInput = document.getElementById("serverUrl");
      const btnLocal = document.getElementById("btnLocal");
      const btnCloud = document.getElementById("btnCloud");

      if (mode === "local") {
        urlInput.value = "http://127.0.0.1:5005";
        btnLocal.className = "flex-1 md:flex-initial px-3 py-1.5 rounded-xl bg-amber-500 text-slate-950 font-bold transition";
        btnCloud.className = "flex-1 md:flex-initial px-3 py-1.5 rounded-xl text-slate-300 hover:text-white transition";
      } else {
        urlInput.value = "https://siwasup-cobroker-os.onrender.com";
        btnCloud.className = "flex-1 md:flex-initial px-3 py-1.5 rounded-xl bg-amber-500 text-slate-950 font-bold transition";
        btnLocal.className = "flex-1 md:flex-initial px-3 py-1.5 rounded-xl text-slate-300 hover:text-white transition";
      }
    }"""

new_js = """    function setServerPreset(mode) {
      const urlInput = document.getElementById("serverUrl");
      const btnLocal = document.getElementById("btnLocal");
      const btnCloud = document.getElementById("btnCloud");
      const btnR2 = document.getElementById("btnR2");

      [btnLocal, btnCloud, btnR2].forEach(b => {
        if (b) b.className = "px-3 py-1.5 rounded-xl text-slate-300 hover:text-white transition";
      });

      if (mode === "local") {
        urlInput.value = "http://127.0.0.1:5005";
        btnLocal.className = "px-3 py-1.5 rounded-xl bg-amber-500 text-slate-950 font-bold transition";
      } else if (mode === "r2") {
        urlInput.value = "https://assets.siwasup.com/data/line_chat_logs.json";
        btnR2.className = "px-3 py-1.5 rounded-xl bg-amber-500 text-slate-950 font-bold transition";
      } else {
        urlInput.value = "https://siwasup-cobroker-os.onrender.com";
        btnCloud.className = "px-3 py-1.5 rounded-xl bg-amber-500 text-slate-950 font-bold transition";
      }
    }"""

html = html.replace(old_js, new_js)

# 3. Update fetchLogs to handle both API and static JSON
old_fetch = """      const targetUrl = `${baseUrl}/api/export-logs?secret=${encodeURIComponent(secret)}&days=${selectedDays}&category=${cat}&mask_pii=${maskPhone}`;

      try {
        const resp = await fetch(targetUrl, { cache: "no-store" });
        if (!resp.ok) {
          throw new Error(`เซิร์ฟเวอร์ตอบกลับรหัส ${resp.status} (${resp.statusText})`);
        }
        const data = await resp.json();
        currentLogs = data.conversations || [];"""

new_fetch = """      let targetUrl = "";
      if (baseUrl.endsWith(".json")) {
        targetUrl = baseUrl + "?t=" + Date.now();
      } else {
        targetUrl = `${baseUrl}/api/export-logs?secret=${encodeURIComponent(secret)}&days=${selectedDays}&category=${cat}&mask_pii=${maskPhone}`;
      }

      try {
        const resp = await fetch(targetUrl, { cache: "no-store" });
        if (!resp.ok) {
          throw new Error(`เซิร์ฟเวอร์ตอบกลับรหัส ${resp.status} (${resp.statusText})`);
        }
        const data = await resp.json();
        currentLogs = data.conversations || [];"""

html = html.replace(old_fetch, new_fetch)

# 4. Update renderTable to display Thai Time badge
old_tr = """            <td class="p-3 text-slate-400 font-mono text-[11px] whitespace-nowrap">${c.timestamp || "-"}</td>"""
new_tr = """            <td class="p-3 text-slate-400 font-mono text-[11px] whitespace-nowrap">
              <div>${c.timestamp || "-"}</div>
              <span class="text-[9.5px] text-emerald-400 font-sans">✓ ล่าสุด</span>
            </td>"""

html = html.replace(old_tr, new_tr)

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("[OK] Successfully patched offline_log_exporter.html")
