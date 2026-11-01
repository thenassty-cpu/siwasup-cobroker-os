import re

file_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\agent_registration.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add QR button in Header
old_header_right = '''      <a href="https://assets.siwasup.com/executive_quick_hub.html" class="text-[10px] font-bold px-2.5 py-1 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 flex items-center gap-1 transition">
        <i data-lucide="layout-grid" class="w-3 h-3 text-amber-400"></i>
        <span>Quick Hub</span>
      </a>'''

new_header_right = '''      <div class="flex items-center gap-1.5">
        <button type="button" onclick="openQrModal()" class="text-[10px] font-bold px-2.5 py-1 rounded-xl bg-emerald-600/30 hover:bg-emerald-600/50 text-emerald-300 border border-emerald-500/40 flex items-center gap-1 transition">
          <i data-lucide="qr-code" class="w-3.5 h-3.5 text-emerald-400"></i>
          <span>ยื่น QR ให้สแกน</span>
        </button>
        <a href="https://assets.siwasup.com/agent_onboarding_qr.html" class="text-[10px] font-bold px-2.5 py-1 rounded-xl bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 border border-amber-500/30 flex items-center gap-1 transition">
          <i data-lucide="sparkles" class="w-3 h-3 text-amber-400"></i>
          <span>ป้าย Standee</span>
        </a>
      </div>'''

content = content.replace(old_header_right, new_header_right)

# 2. Add QR Modal before </body>
qr_modal_html = '''  <!-- QR CODE MODAL POPUP -->
  <div id="qrModal" class="fixed inset-0 z-50 bg-slate-950/85 backdrop-blur-md flex items-center justify-center p-4 hidden">
    <div class="card-glass rounded-3xl p-6 border border-amber-500/40 max-w-sm w-full text-center space-y-4 shadow-2xl relative">
      <button onclick="closeQrModal()" class="absolute top-4 right-4 text-slate-400 hover:text-white p-1 rounded-xl bg-slate-800/80">
        <i data-lucide="x" class="w-5 h-5"></i>
      </button>

      <div class="space-y-1">
        <div class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-amber-500/10 border border-amber-500/30 text-amber-400 text-[10px] font-bold">
          <i data-lucide="scan" class="w-3 h-3"></i>
          <span>สแกนลงทะเบียนหน้างาน</span>
        </div>
        <h3 class="text-base font-bold text-white">ยื่น QR Code ให้เพื่อนร่วมงานสแกน</h3>
        <p class="text-[11px] text-slate-300">ใช้กล้องมือถือหรือแอป LINE สแกนเพื่อเปิดฟอร์มสมัครทันที</p>
      </div>

      <div class="bg-white p-4 rounded-2xl shadow-xl inline-block border-2 border-amber-400/80">
        <img src="https://api.qrserver.com/v1/create-qr-code/?size=300x300&margin=8&data=https%3A%2F%2Fassets.siwasup.com%2Fagent_registration.html" 
             alt="Registration QR Code" 
             class="w-52 h-52 object-contain mx-auto rounded-lg">
        <div class="mt-2 pt-1 border-t border-slate-200 text-[11px] font-black text-slate-900">
          Siwasup Co-Broker Registration
        </div>
      </div>

      <div class="flex items-center justify-center gap-2 pt-1">
        <a href="https://assets.siwasup.com/agent_onboarding_qr.html" class="w-full py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-bold border border-slate-700 flex items-center justify-center gap-1.5 transition">
          <i data-lucide="monitor" class="w-3.5 h-3.5 text-amber-400"></i>
          <span>เปิดหน้าจอ Kiosk / พิมพ์ป้าย</span>
        </a>
      </div>
    </div>
  </div>

  <script>
    function openQrModal() {
      document.getElementById('qrModal').classList.remove('hidden');
      if (window.lucide) lucide.createIcons();
    }
    function closeQrModal() {
      document.getElementById('qrModal').classList.add('hidden');
    }
  </script>
'''

content = content.replace("</body>", qr_modal_html + "\n</body>")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Patched agent_registration.html with QR modal successfully!")
