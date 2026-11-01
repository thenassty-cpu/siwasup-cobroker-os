import os

FILE_PATH = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\siwasup_keybox_interactive_roleplay.html"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add #voidCaseModal right before </body>
void_modal_html = """
  <!-- ============================================================== -->
  <!-- MODAL: FORCE MAJEURE CANCELLATION (ยกเลิกเคสฉุกเฉิน/ฝนตกน้ำท่วม) -->
  <!-- ============================================================== -->
  <div id="voidCaseModal" class="fixed inset-0 bg-slate-950/85 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
    <div class="card-glass rounded-3xl max-w-md w-full p-5 sm:p-6 border border-red-500/40 space-y-4 shadow-2xl animate-fade-in">
      <div class="flex items-center justify-between pb-3 border-b border-slate-800">
        <div class="flex items-center gap-2.5">
          <div class="w-9 h-9 rounded-xl bg-red-500/20 text-red-400 flex items-center justify-center">
            <i data-lucide="cloud-rain" class="w-5 h-5"></i>
          </div>
          <div>
            <h3 class="text-sm font-bold text-white">ยกเลิกเคสฉุกเฉิน / เหตุสุดวิสัย (พี่ลิลลี่)</h3>
            <p class="text-[11px] text-slate-400">Master Key Force Majeure Cancellation</p>
          </div>
        </div>
        <button onclick="closeVoidModal()" class="w-8 h-8 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center text-sm font-bold transition">
          ✕
        </button>
      </div>

      <!-- Case Info Summary -->
      <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 text-xs space-y-1">
        <div class="flex justify-between">
          <span class="text-slate-400">ตัวแทน:</span>
          <span id="voidModalAgent" class="font-bold text-white">-</span>
        </div>
        <div class="flex justify-between">
          <span class="text-slate-400">รหัสทรัพย์:</span>
          <span id="voidModalProp" class="font-bold text-amber-400">-</span>
        </div>
        <div class="flex justify-between">
          <span class="text-slate-400">รอบเวลา:</span>
          <span id="voidModalSlot" class="font-bold text-slate-300">-</span>
        </div>
        <div class="flex justify-between">
          <span class="text-slate-400">รหัส OTP ที่จะถูกทำลาย:</span>
          <span id="voidModalOtp" class="font-mono text-red-400 font-bold line-through">-</span>
        </div>
      </div>

      <!-- Force Majeure Reason Selection -->
      <div class="space-y-1.5 text-xs">
        <label class="text-[11px] font-bold text-slate-300">เลือกสาเหตุสุดวิสัยที่ต้องยกเลิกนัด:</label>
        <div class="space-y-1.5">
          <label class="p-2.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-red-500 cursor-pointer flex items-center justify-between">
            <div class="flex items-center gap-2">
              <input type="radio" name="voidReasonRadio" value="ฝนตกหนัก น้ำท่วมขังถนนทางเข้าโครงการ (เดินทางไม่ได้)" checked class="text-red-500 focus:ring-red-500" />
              <span class="text-slate-200 font-medium">🌧️ ฝนตกหนัก น้ำท่วมขังทางเข้าโครงการ</span>
            </div>
            <span class="text-[10px] text-red-400 font-bold">เหตุธรรมชาติ</span>
          </label>

          <label class="p-2.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-red-500 cursor-pointer flex items-center justify-between">
            <div class="flex items-center gap-2">
              <input type="radio" name="voidReasonRadio" value="นิติบุคคลโครงการแจ้งปิดปรับปรุงไฟฟ้า/ตัดน้ำกะทันหัน" class="text-red-500 focus:ring-red-500" />
              <span class="text-slate-200 font-medium">🏛️ นิติโครงการ/เจ้าของบ้านแจ้งฉุกเฉิน</span>
            </div>
            <span class="text-[10px] text-amber-400 font-bold">เหตุส่วนกลาง</span>
          </label>

          <label class="p-2.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-red-500 cursor-pointer flex items-center justify-between">
            <div class="flex items-center gap-2">
              <input type="radio" name="voidReasonRadio" value="กลอนตู้ Smart Keybox ขัดข้อง ไม่สามารถเปิดตู้ได้" class="text-red-500 focus:ring-red-500" />
              <span class="text-slate-200 font-medium">🔒 ตู้ Smart Keybox หน้าบ้านขัดข้อง</span>
            </div>
            <span class="text-[10px] text-blue-400 font-bold">ฮาร์ดแวร์</span>
          </label>

          <label class="p-2.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-red-500 cursor-pointer flex items-center justify-between">
            <div class="flex items-center gap-2">
              <input type="radio" name="voidReasonRadio" value="ลูกค้าผู้ซื้อติดภารกิจด่วน แจ้งขอยกเลิกนัด" class="text-red-500 focus:ring-red-500" />
              <span class="text-slate-200 font-medium">👤 ลูกค้าขอยกเลิกนัดกะทันหัน</span>
            </div>
            <span class="text-[10px] text-slate-400 font-bold">ลูกค้า</span>
          </label>
        </div>
      </div>

      <!-- Agent Protection Checklist -->
      <div class="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/30 text-[10.5px] text-emerald-300 space-y-1">
        <div class="font-bold text-emerald-400 flex items-center gap-1.5">
          <i data-lucide="shield-check" class="w-4 h-4"></i>
          <span>มาตรการคุ้มครองตัวแทนอัตโนมัติ 100%:</span>
        </div>
        <div class="grid grid-cols-2 gap-1 text-[10px] text-slate-300 pt-1">
          <div>✓ คืนโควต้าเปิดบ้านให้ตัวแทน</div>
          <div>✓ คืนสล็อตว่างให้ระบบทันที</div>
          <div>✓ ล็อกสิทธิ์คอม 60 วันคงเดิม</div>
          <div>✓ ทำลายรหัส OTP ทันที (Void)</div>
        </div>
      </div>

      <!-- Action Buttons -->
      <div class="pt-2 flex items-center gap-2">
        <button onclick="closeVoidModal()" class="flex-1 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold transition">
          ปิด
        </button>
        <button onclick="confirmVoidCase()" class="flex-2 py-2.5 rounded-xl bg-red-600 hover:bg-red-500 text-white text-xs font-bold flex items-center justify-center gap-1.5 shadow-lg shadow-red-500/25 transition active:scale-95">
          <i data-lucide="x-circle" class="w-3.5 h-3.5"></i>
          <span>ยืนยันยกเลิกเคส &amp; ส่งหนังสือแจ้งเตือน</span>
        </button>
      </div>
    </div>
  </div>
"""

# Add modal before </body>
html = html.replace("</body>", void_modal_html + "\n</body>")

# 2. Update Lily's active case action buttons in renderLilyActiveViewing
old_buttons_in_viewing = """            <button onclick="voidCase('${c.id}')" class="px-2 py-1 rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-400 font-bold text-[11px] transition">
              ยกเลิก
            </button>"""

new_buttons_in_viewing = """            <button onclick="openVoidModal('${c.id}')" class="px-2.5 py-1 rounded-lg bg-red-500/15 hover:bg-red-600 text-red-300 hover:text-white font-bold text-[11px] flex items-center gap-1 transition shadow-sm" title="ยกเลิกฉุกเฉิน (เช่น ฝนตกน้ำท่วม/นิติสั่งปิด)">
              <i data-lucide="cloud-rain" class="w-3 h-3 text-red-400"></i>
              <span>ยกเลิกฉุกเฉิน</span>
            </button>"""

html = html.replace(old_buttons_in_viewing, new_buttons_in_viewing)

# 3. Add JavaScript functions for Void Modal
void_js = """
    // =========================================================================
    // 8. DEDICATED FORCE MAJEURE VOID MODAL (พี่ลิลลี่ยกเลิกฉุกเฉิน)
    // =========================================================================
    let activeVoidCaseId = null;

    function openVoidModal(caseId) {
      activeVoidCaseId = caseId;
      const c = approvedCases.find(item => item.id === caseId);
      if (!c) return;

      document.getElementById("voidModalAgent").innerText = `${c.agentName} (${c.agentCode})`;
      document.getElementById("voidModalProp").innerText = c.property;
      document.getElementById("voidModalSlot").innerText = c.slot;
      document.getElementById("voidModalOtp").innerText = c.otp;

      document.getElementById("voidCaseModal").classList.remove("hidden");
      playTone('notify');
      lucide.createIcons();
    }

    function closeVoidModal() {
      document.getElementById("voidCaseModal").classList.add("hidden");
      activeVoidCaseId = null;
    }

    function confirmVoidCase() {
      if (!activeVoidCaseId) return;
      const c = approvedCases.find(item => item.id === activeVoidCaseId);
      if (!c) return;

      const radios = document.getElementsByName("voidReasonRadio");
      let reason = "ฝนตกหนัก น้ำท่วมขังถนนทางเข้าโครงการ";
      for (const r of radios) {
        if (r.checked) {
          reason = r.value;
          break;
        }
      }

      c.status = "VOIDED";
      c.voidReason = reason;

      closeVoidModal();
      playTone('error');

      // Log to event bus
      logLilyBot(`🚨 <strong>พี่ลิลลี่ยกเลิกเคสฉุกเฉิน:</strong> เคสเปิดบ้าน #1090965 ของ ${c.agentName} (${c.agentCode}) ถูกยกเลิกเนื่องจาก <em>"${reason}"</em> • 🔒 รหัส OTP [${c.otp}] ถูกทำลายทันที (Void) • 🛡️ <strong>คืนสิทธิ์โควต้าและล็อกสิทธิ์คอมมิชชั่น 60 วันให้ตัวแทน 100%</strong>`);

      // Update Agent screen if playing as that agent
      if (currentAgentIdentity === c.agentCode) {
        document.getElementById("agentVoucherCard").classList.add("hidden");
        document.getElementById("agentRequestFormBox").classList.remove("hidden");
        alert(`🚨 แจ้งเตือนด่วนจากพี่ลิลลี่:\\nเคสเปิดบ้านรอบนี้ถูกยกเลิกเนื่องจาก: "${reason}"\\n\\n🛡️ กฎคุ้มครอง: โควต้าของคุณได้รับการคืนสิทธิ์ 100% และสิทธิ์คอมมิชชั่น 60 วันยังคงอยู่ครบครับ`);
      }

      renderLilyActiveViewing();
    }
"""

html = html.replace("function voidCase(caseId) {", void_js + "\n    function voidCase(caseId) {")

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("[OK] Successfully added Force Majeure Void Modal and Cancellation Buttons for Lily!")
