import os

FILE_PATH = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\siwasup_keybox_interactive_roleplay.html"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Replace the inner modal body of #rescheduleModal with enhanced Force Majeure features
old_reason_block = """      <!-- Reschedule Reason -->
      <div class="space-y-1 text-xs">
        <label class="text-[11px] text-slate-400">เหตุผลการเลื่อนนัด:</label>
        <select id="selectReschedReason" class="w-full p-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-xs">
          <option value="ลูกค้าติดประชุมด่วน ขอเลื่อนเวลา">ลูกค้าติดประชุมด่วน ขอเลื่อนเวลา</option>
          <option value="ฝนตกหนัก/การจราจรติดขัด ขอสลับรอบบ่าย">ฝนตกหนัก/การจราจรติดขัด ขอสลับรอบบ่าย</option>
          <option value="ลูกค้าขอพาครอบครัวมาเพิ่มรอบวันถัดไป">ลูกค้าขอพาครอบครัวมาเพิ่มรอบวันถัดไป</option>
          <option value="เหตุสุดวิสัยอื่นๆ">เหตุสุดวิสัยอื่นๆ</option>
        </select>
      </div>"""

new_reason_block = """      <!-- Reschedule Origin & Force Majeure Category -->
      <div class="space-y-1.5 text-xs">
        <label class="text-[11px] font-bold text-slate-300">ต้นเหตุของการเลื่อนนัด (Trigger Origin):</label>
        <select id="selectReschedOrigin" onchange="handleRescheduleOriginChange(this.value)" class="w-full p-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-xs font-medium focus:border-amber-500 focus:outline-hidden">
          <option value="AGENT_CLIENT">👤 เอเจนต์ / ลูกค้าขอเลื่อน (ปกติ)</option>
          <option value="HOA_OWNER">🏛️ เหตุสุดวิสัย: นิติโครงการ / เจ้าของบ้านแจ้งฉุกเฉิน (ซ่อมบำรุง/ตัดน้ำไฟ)</option>
          <option value="WEATHER_FORCE">🌧️ เหตุสุดวิสัย: สภาพอากาศ / ฝนตกหนักน้ำท่วมทางเข้าโครงการ</option>
          <option value="KEYBOX_FAIL">🔒 เหตุสุดวิสัย: ตู้ Smart Keybox ขัดข้อง / แบตหมด (ส่ง Messenger แทน)</option>
        </select>
      </div>

      <!-- Specific Details / Note -->
      <div class="space-y-1 text-xs">
        <label class="text-[11px] text-slate-400">บันทึกรายละเอียดเหตุผล:</label>
        <input type="text" id="inputReschedDetail" value="ลูกค้าติดประชุมด่วน ขอเลื่อนเวลา" 
          class="w-full px-3 py-2 rounded-xl bg-slate-950 border border-slate-700 text-white text-xs focus:border-amber-500 focus:outline-hidden" />
      </div>

      <!-- Force Majeure Agent Protection Banner (Appears when not agent's fault) -->
      <div id="forceMajeureBanner" class="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/40 text-[10.5px] text-emerald-300 space-y-1 hidden">
        <div class="font-bold flex items-center gap-1.5 text-emerald-400">
          <i data-lucide="shield-check" class="w-4 h-4"></i>
          <span>กฎคุ้มครองสิทธิ์เอเจนต์ 100% (Force Majeure Guarantee):</span>
        </div>
        <ul class="space-y-0.5 pl-4 list-disc text-slate-300">
          <li><strong>ไม่หักโควต้าตัวแทน:</strong> ถือเป็นเหตุจากส่วนกลาง คืนสิทธิ์โควต้าเต็ม 2 หลัง</li>
          <li><strong>ล็อกสิทธิ์คอม 60 วันคงเดิม:</strong> ลูกค้าท่านนี้ยังคงเป็นสิทธิ์ของตัวแทน 100%</li>
          <li><strong>Fast-Track Priority:</strong> ได้รับสิทธิ์จองสล็อตรอบถัดไปเป็นคิวแรกทันที</li>
          <li><strong>ออกหนังสือชี้แจงทางการ:</strong> ระบบออกข้อความรับรองจากบริษัท ให้ Forward แจ้งลูกค้าได้ทันที ไม่เสียเครดิต</li>
        </ul>
      </div>"""

html = html.replace(old_reason_block, new_reason_block)

# 2. Update modal buttons to include Messenger option for Keybox failure
old_buttons = """      <!-- Modal Action Buttons -->
      <div class="pt-2 flex items-center gap-2">
        <button onclick="closeRescheduleModal()" class="flex-1 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold transition">
          ยกเลิก
        </button>
        <button onclick="confirmReschedule()" class="flex-2 py-2.5 rounded-xl gold-gradient hover:brightness-110 text-slate-950 text-xs font-bold flex items-center justify-center gap-1.5 shadow-lg shadow-amber-500/20 transition active:scale-95">
          <i data-lucide="check" class="w-3.5 h-3.5"></i>
          <span>ยืนยันการเลื่อน &amp; ออก OTP ใหม่</span>
        </button>
      </div>"""

new_buttons = """      <!-- Modal Action Buttons -->
      <div class="pt-2 space-y-2">
        <div class="flex items-center gap-2">
          <button onclick="closeRescheduleModal()" class="flex-1 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold transition">
            ปิด
          </button>
          <button onclick="confirmReschedule()" class="flex-2 py-2.5 rounded-xl gold-gradient hover:brightness-110 text-slate-950 text-xs font-bold flex items-center justify-center gap-1.5 shadow-lg shadow-amber-500/20 transition active:scale-95">
            <i data-lucide="check" class="w-3.5 h-3.5"></i>
            <span>ยืนยันการเลื่อนวัน/รอบ &amp; ออก OTP ใหม่</span>
          </button>
        </div>

        <!-- Emergency Messenger Dispatch Button (If keybox hardware issue) -->
        <button id="btnReschedMessenger" onclick="dispatchEmergencyMessenger()" class="w-full py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-emerald-400 border border-emerald-500/30 text-xs font-bold flex items-center justify-center gap-1.5 transition hidden">
          <i data-lucide="bike" class="w-4 h-4"></i>
          <span>🛵 เรียกรถมอไซค์ส่งกุญแจดอกจริงด่วนถึงหน้าบ้าน (ออฟฟิศรับผิดชอบค่าใช้จ่าย)</span>
        </button>
      </div>"""

html = html.replace(old_buttons, new_buttons)

# 3. Add JS functions for Force Majeure handling
js_patch = """
    function handleRescheduleOriginChange(val) {
      const banner = document.getElementById("forceMajeureBanner");
      const detailInput = document.getElementById("inputReschedDetail");
      const messengerBtn = document.getElementById("btnReschedMessenger");

      if (val === "AGENT_CLIENT") {
        banner.classList.add("hidden");
        messengerBtn.classList.add("hidden");
        detailInput.value = "ลูกค้าติดประชุมด่วน ขอเลื่อนเวลา";
      } else if (val === "HOA_OWNER") {
        banner.classList.remove("hidden");
        messengerBtn.classList.add("hidden");
        detailInput.value = "นิติบุคคลโครงการแจ้งปิดปรับปรุงระบบไฟฟ้า/ตัดน้ำชั่วคราว";
      } else if (val === "WEATHER_FORCE") {
        banner.classList.remove("hidden");
        messengerBtn.classList.add("hidden");
        detailInput.value = "ฝนตกหนัก มีน้ำท่วมขังถนนหน้าโครงการ รถลูกค้าเข้าไม่ได้";
      } else if (val === "KEYBOX_FAIL") {
        banner.classList.remove("hidden");
        messengerBtn.classList.remove("hidden");
        detailInput.value = "ระบบกลอนตู้ Smart Keybox หรือสัญญาณขัดข้องชั่วคราว";
      }
      lucide.createIcons();
    }

    function dispatchEmergencyMessenger() {
      if (!activeRescheduleCaseId) return;
      const c = approvedCases.find(item => item.id === activeRescheduleCaseId);
      if (!c) return;

      closeRescheduleModal();
      playTone('success');
      logLilyBot(`🛵 <strong>แก้ไขเหตุสุดวิสัย (ฉุกเฉิน):</strong> ตู้กุญแจขัดข้อง พี่ลิลลี่มอบหมาย Messenger วิ่งส่งพวงกุญแจหลักจากออฟฟิศท่าข้าม 12 ไปให้ ${c.agentName} (${c.agentCode}) ถึงหน้าบ้านโดยตรง (ฟรี ออฟฟิศดูแล 100%)`);
      alert(`พี่ลิลลี่เรียกรถ Messenger วิ่งส่งกุญแจดอกจริงให้ ${c.agentName} เรียบร้อยครับ!\\nไร้ผลกระทบต่อการพาลูกค้าชมบ้าน`);
    }
"""

html = html.replace("function confirmReschedule() {", js_patch + "\n    function confirmReschedule() {")

# 4. Enhance confirmReschedule to log Force Majeure properly
old_log_resched = """      // Log & Notify
      logLilyBot(`🔄 <strong>เลื่อนนัดสำเร็จ:</strong> พี่ลิลลี่เลื่อนนัด ${c.agentName} (${c.agentCode}) เป็น <strong>${newSlot}</strong> (เหตุผล: ${reason}) • รหัส OTP เดิม [${oldOtp}] ถูกยกเลิก ➔ ออกรหัสใหม่ <span class="text-amber-400 font-bold font-mono">${newOtp}</span> • คืนสล็อตเดิมสู่ระบบเรียบร้อย`);"""

new_log_resched = """      const origin = document.getElementById("selectReschedOrigin").value;
      const detail = document.getElementById("inputReschedDetail").value;
      const isForceMajeure = origin !== "AGENT_CLIENT";

      // Log & Notify
      if (isForceMajeure) {
        logLilyBot(`⚠️ <strong>ประกาศเหตุสุดวิสัยจากส่วนกลาง:</strong> เคสเปิดบ้าน #1090965 เลื่อนเป็น <strong>${newSlot}</strong> เนื่องจาก <em>${detail}</em> • 🛡️ <strong>คุ้มครองสิทธิ์ ${c.agentName} (${c.agentCode}) เต็ม 100%</strong> (ไม่ตัดโควต้า + ล็อกสิทธิ์คอม 60 วัน) • ออกรหัส OTP ใหม่ <span class="text-amber-400 font-bold font-mono">${newOtp}</span> พร้อมหนังสือชี้แจงทางการ`);
      } else {
        logLilyBot(`🔄 <strong>เลื่อนนัดสำเร็จ:</strong> พี่ลิลลี่เลื่อนนัด ${c.agentName} (${c.agentCode}) เป็น <strong>${newSlot}</strong> (เหตุผล: ${detail}) • รหัส OTP เดิม [${oldOtp}] ถูกยกเลิก ➔ ออกรหัสใหม่ <span class="text-amber-400 font-bold font-mono">${newOtp}</span> • คืนสล็อตเดิมสู่ระบบเรียบร้อย`);
      }"""

html = html.replace(old_log_resched, new_log_resched)

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("[OK] Successfully integrated Force Majeure & Agent Protection Policy into keybox sandbox!")
