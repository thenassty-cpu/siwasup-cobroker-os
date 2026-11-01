import os
import re

FILE_PATH = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\siwasup_keybox_interactive_roleplay.html"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Add Reschedule Modal HTML before </body>
modal_html = """
  <!-- ============================================================== -->
  <!-- MODAL: RESCHEDULE & SLOT ADJUSTMENT (เมนูจัดการเลื่อนวัน/รอบ)    -->
  <!-- ============================================================== -->
  <div id="rescheduleModal" class="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4 hidden">
    <div class="card-glass rounded-3xl max-w-md w-full p-5 sm:p-6 border border-amber-500/40 space-y-4 shadow-2xl animate-fade-in">
      <div class="flex items-center justify-between pb-3 border-b border-slate-800">
        <div class="flex items-center gap-2.5">
          <div class="w-9 h-9 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center">
            <i data-lucide="calendar-clock" class="w-5 h-5"></i>
          </div>
          <div>
            <h3 class="text-sm font-bold text-white">เมนูจัดการเลื่อนวัน / รอบเวลาเปิดบ้าน</h3>
            <p class="text-[11px] text-slate-400">Master Key Ops @ ท่าข้าม 12</p>
          </div>
        </div>
        <button onclick="closeRescheduleModal()" class="w-8 h-8 rounded-full bg-slate-800 hover:bg-slate-700 text-slate-400 hover:text-white flex items-center justify-center text-sm font-bold transition">
          ✕
        </button>
      </div>

      <!-- Case Info Summary -->
      <div class="bg-slate-950 p-3 rounded-xl border border-slate-800 text-xs space-y-1">
        <div class="flex justify-between">
          <span class="text-slate-400">ตัวแทน:</span>
          <span id="modalReschedAgent" class="font-bold text-white">-</span>
        </div>
        <div class="flex justify-between">
          <span class="text-slate-400">รหัสทรัพย์:</span>
          <span id="modalReschedProp" class="font-bold text-amber-400">-</span>
        </div>
        <div class="flex justify-between">
          <span class="text-slate-400">รอบเวลาปัจจุบัน:</span>
          <span id="modalReschedOldSlot" class="font-bold text-slate-300">-</span>
        </div>
        <div class="flex justify-between">
          <span class="text-slate-400">รหัส OTP เดิม:</span>
          <span id="modalReschedOldOtp" class="font-mono text-red-400 font-bold line-through">-</span>
        </div>
      </div>

      <!-- Selection for New Slot -->
      <div class="space-y-1.5 text-xs">
        <label class="text-[11px] font-bold text-slate-300">เลือกรอบเวลาใหม่ที่ต้องการเปลี่ยน:</label>
        <div class="space-y-1.5" id="newSlotRadioGroup">
          <label class="p-2.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-amber-500 cursor-pointer flex items-center justify-between">
            <div class="flex items-center gap-2">
              <input type="radio" name="reschedNewSlot" value="วันนี้ รอบบ่าย (13:30 - 17:00 น.)" checked class="text-amber-500 focus:ring-amber-500" />
              <span class="text-slate-200 font-medium">🌇 วันนี้ รอบบ่าย (13:30 - 17:00 น.)</span>
            </div>
            <span class="text-[10px] text-emerald-400 font-bold">คิวว่าง</span>
          </label>

          <label class="p-2.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-amber-500 cursor-pointer flex items-center justify-between">
            <div class="flex items-center gap-2">
              <input type="radio" name="reschedNewSlot" value="พรุ่งนี้ รอบเช้า (09:00 - 12:30 น.)" class="text-amber-500 focus:ring-amber-500" />
              <span class="text-slate-200 font-medium">🌅 พรุ่งนี้ รอบเช้า (09:00 - 12:30 น.)</span>
            </div>
            <span class="text-[10px] text-emerald-400 font-bold">คิวว่าง</span>
          </label>

          <label class="p-2.5 rounded-xl bg-slate-900 border border-slate-800 hover:border-amber-500 cursor-pointer flex items-center justify-between">
            <div class="flex items-center gap-2">
              <input type="radio" name="reschedNewSlot" value="พรุ่งนี้ รอบบ่าย (13:30 - 17:00 น.)" class="text-amber-500 focus:ring-amber-500" />
              <span class="text-slate-200 font-medium">🌇 พรุ่งนี้ รอบบ่าย (13:30 - 17:00 น.)</span>
            </div>
            <span class="text-[10px] text-emerald-400 font-bold">คิวว่าง</span>
          </label>
        </div>
      </div>

      <!-- Reschedule Reason -->
      <div class="space-y-1 text-xs">
        <label class="text-[11px] text-slate-400">เหตุผลการเลื่อนนัด:</label>
        <select id="selectReschedReason" class="w-full p-2.5 rounded-xl bg-slate-950 border border-slate-700 text-white text-xs">
          <option value="ลูกค้าติดประชุมด่วน ขอเลื่อนเวลา">ลูกค้าติดประชุมด่วน ขอเลื่อนเวลา</option>
          <option value="ฝนตกหนัก/การจราจรติดขัด ขอสลับรอบบ่าย">ฝนตกหนัก/การจราจรติดขัด ขอสลับรอบบ่าย</option>
          <option value="ลูกค้าขอพาครอบครัวมาเพิ่มรอบวันถัดไป">ลูกค้าขอพาครอบครัวมาเพิ่มรอบวันถัดไป</option>
          <option value="เหตุสุดวิสัยอื่นๆ">เหตุสุดวิสัยอื่นๆ</option>
        </select>
      </div>

      <!-- Action Policy Warning -->
      <div class="p-2.5 rounded-xl bg-amber-500/10 border border-amber-500/30 text-[10.5px] text-amber-300 space-y-1">
        <div class="font-bold flex items-center gap-1">
          <i data-lucide="shield-alert" class="w-3.5 h-3.5"></i>
          กฎความปลอดภัย Smart Keybox:
        </div>
        <p class="text-slate-300">
          เมื่อกดยืนยัน ระบบจะ <strong>ยกเลิกรหัส OTP เดิมทันที</strong> และออกรหัส OTP ใหม่พร้อมแจ้งเตือน Agent ผ่าน LINE รวมถึง <strong>ปลดสล็อตเดิมคืนระบบ</strong> เพื่อให้ตัวแทนท่านอื่นจองต่อได้ทันที
        </p>
      </div>

      <!-- Modal Action Buttons -->
      <div class="pt-2 flex items-center gap-2">
        <button onclick="closeRescheduleModal()" class="flex-1 py-2.5 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold transition">
          ยกเลิก
        </button>
        <button onclick="confirmReschedule()" class="flex-2 py-2.5 rounded-xl gold-gradient hover:brightness-110 text-slate-950 text-xs font-bold flex items-center justify-center gap-1.5 shadow-lg shadow-amber-500/20 transition active:scale-95">
          <i data-lucide="check" class="w-3.5 h-3.5"></i>
          <span>ยืนยันการเลื่อน &amp; ออก OTP ใหม่</span>
        </button>
      </div>
    </div>
  </div>
"""

# Insert modal before </body>
content = content.replace("</body>", modal_html + "\n</body>")

# 2. Add Reschedule button on Agent Voucher Card
voucher_card_needle = """                <div class="text-center py-2.5 bg-slate-950/90 rounded-xl border border-amber-500/40">
                  <span class="text-[10px] text-slate-400">รหัส Smart Keybox OTP (ใช้ได้รอบ 09:00 - 12:30 น.)</span>
                  <div id="agentOtpDisplay" class="text-3xl font-black font-mono tracking-widest text-amber-400 my-1">839210</div>
                  <span class="text-[10px] text-emerald-400 font-medium">👉 นำรหัส 6 หลักนี้ไปกดที่ตู้กุญแจหน้าบ้าน (ฝั่งขวา)</span>
                </div>"""

voucher_card_replacement = """                <div class="text-center py-2.5 bg-slate-950/90 rounded-xl border border-amber-500/40">
                  <span id="agentOtpSlotLabel" class="text-[10px] text-slate-400">รหัส Smart Keybox OTP (ใช้ได้รอบ 09:00 - 12:30 น.)</span>
                  <div id="agentOtpDisplay" class="text-3xl font-black font-mono tracking-widest text-amber-400 my-1">839210</div>
                  <span class="text-[10px] text-emerald-400 font-medium">👉 นำรหัส 6 หลักนี้ไปกดที่ตู้กุญแจหน้าบ้าน (ฝั่งขวา)</span>
                </div>

                <!-- Agent Quick Reschedule / Cancel Utility -->
                <div class="flex items-center justify-between p-2 rounded-xl bg-slate-950/80 border border-slate-800 text-[11px]">
                  <button onclick="agentRequestReschedule()" class="text-amber-400 hover:text-amber-300 font-bold flex items-center gap-1 transition">
                    <i data-lucide="calendar-clock" class="w-3.5 h-3.5"></i>
                    <span>ลูกค้าขอเลื่อนวัน/รอบ</span>
                  </button>
                  <button onclick="agentRequestCancel()" class="text-red-400 hover:text-red-300 font-medium transition">
                    ขอยกเลิกนัด
                  </button>
                </div>"""

content = content.replace(voucher_card_needle, voucher_card_replacement)

# 3. Update renderLilyActiveViewing in script
old_render_viewing = """        let statusBadge = `<span class="px-2 py-0.5 rounded-full text-[10px] bg-blue-500/20 text-blue-300 font-bold">กำลังชมบ้าน (OTP: ${c.otp})</span>`;
        let actionBtn = `<span class="text-[10px] text-slate-500">รอส่งรูปคืนกุญแจ...</span>`;

        if (c.status === "HANDOVER_READY") {
          statusBadge = `<span class="px-2 py-0.5 rounded-full text-[10px] bg-amber-500 text-slate-950 font-bold animate-pulse">ส่งรูปคืนแล้ว</span>`;
          actionBtn = `
            <button onclick="lilyCloseSingle('${c.id}')" class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center gap-1 transition">
              <i data-lucide="check" class="w-3 h-3"></i>
              <span>ตรวจรับ &amp; ปิดเคส</span>
            </button>
          `;
        } else if (c.status === "CLOSED") {
          statusBadge = `<span class="px-2 py-0.5 rounded-full text-[10px] bg-emerald-500/20 text-emerald-300 font-bold">ปิดเคสสำเร็จ 100%</span>`;
          actionBtn = `<span class="text-[10px] text-emerald-400 font-bold">✓ กุญแจอยู่ในตู้</span>`;
        }"""

new_render_viewing = """        let isRescheduled = c.rescheduled === true;
        let statusBadge = `<span class="px-2 py-0.5 rounded-full text-[10px] ${isRescheduled ? 'bg-purple-500/20 text-purple-300 border border-purple-500/40' : 'bg-blue-500/20 text-blue-300'} font-bold">${isRescheduled ? '🔄 เลื่อนนัด: ' + c.slot : 'กำลังชมบ้าน'} (OTP: ${c.otp})</span>`;
        
        let actionBtn = `
          <div class="flex items-center gap-1.5 flex-wrap justify-end">
            <button onclick="openRescheduleModal('${c.id}')" class="px-2.5 py-1 rounded-lg bg-amber-500/20 hover:bg-amber-500 text-amber-300 hover:text-slate-950 font-bold text-[11px] flex items-center gap-1 transition">
              <i data-lucide="calendar-clock" class="w-3 h-3"></i>
              <span>เลื่อนวัน/รอบ</span>
            </button>
            <button onclick="voidCase('${c.id}')" class="px-2 py-1 rounded-lg bg-red-500/10 hover:bg-red-500/20 text-red-400 font-bold text-[11px] transition">
              ยกเลิก
            </button>
            <span class="text-[10px] text-slate-500 ml-1">รอคืนกุญแจ...</span>
          </div>
        `;

        if (c.status === "HANDOVER_READY") {
          statusBadge = `<span class="px-2 py-0.5 rounded-full text-[10px] bg-amber-500 text-slate-950 font-bold animate-pulse">ส่งรูปคืนแล้ว</span>`;
          actionBtn = `
            <button onclick="lilyCloseSingle('${c.id}')" class="px-3 py-1.5 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center gap-1 transition shadow-sm">
              <i data-lucide="check" class="w-3 h-3"></i>
              <span>ตรวจรับ &amp; ปิดเคส</span>
            </button>
          `;
        } else if (c.status === "CLOSED") {
          statusBadge = `<span class="px-2 py-0.5 rounded-full text-[10px] bg-emerald-500/20 text-emerald-300 font-bold">ปิดเคสสำเร็จ 100%</span>`;
          actionBtn = `<span class="text-[10px] text-emerald-400 font-bold">✓ กุญแจอยู่ในตู้</span>`;
        } else if (c.status === "VOIDED") {
          statusBadge = `<span class="px-2 py-0.5 rounded-full text-[10px] bg-red-500/20 text-red-300 font-bold">ยกเลิกนัดแล้ว</span>`;
          actionBtn = `<span class="text-[10px] text-slate-500">คืนสิทธิ์สล็อตแล้ว</span>`;
        }"""

content = content.replace(old_render_viewing, new_render_viewing)

# 4. Add JavaScript helper functions for Reschedule & Void
js_functions = """
    // =========================================================================
    // 7. RESCHEDULE & VOID SLOT MANAGEMENT ENGINE
    // =========================================================================
    let activeRescheduleCaseId = null;

    function openRescheduleModal(caseId) {
      activeRescheduleCaseId = caseId;
      const c = approvedCases.find(item => item.id === caseId);
      if (!c) return;

      document.getElementById("modalReschedAgent").innerText = `${c.agentName} (${c.agentCode})`;
      document.getElementById("modalReschedProp").innerText = c.property;
      document.getElementById("modalReschedOldSlot").innerText = c.slot;
      document.getElementById("modalReschedOldOtp").innerText = c.otp;

      document.getElementById("rescheduleModal").classList.remove("hidden");
      playTone('notify');
      lucide.createIcons();
    }

    function closeRescheduleModal() {
      document.getElementById("rescheduleModal").classList.add("hidden");
      activeRescheduleCaseId = null;
    }

    function confirmReschedule() {
      if (!activeRescheduleCaseId) return;
      const c = approvedCases.find(item => item.id === activeRescheduleCaseId);
      if (!c) return;

      const radios = document.getElementsByName("reschedNewSlot");
      let newSlot = "วันนี้ รอบบ่าย (13:30 - 17:00 น.)";
      for (const r of radios) {
        if (r.checked) {
          newSlot = r.value;
          break;
        }
      }

      const reason = document.getElementById("selectReschedReason").value;
      const oldOtp = c.otp;
      const newOtp = Math.floor(100000 + Math.random() * 900000);

      // Update case
      c.oldSlot = c.slot;
      c.slot = newSlot;
      c.otp = newOtp;
      c.rescheduled = true;
      c.rescheduledReason = reason;

      closeRescheduleModal();
      playTone('success');

      // Log & Notify
      logLilyBot(`🔄 <strong>เลื่อนนัดสำเร็จ:</strong> พี่ลิลลี่เลื่อนนัด ${c.agentName} (${c.agentCode}) เป็น <strong>${newSlot}</strong> (เหตุผล: ${reason}) • รหัส OTP เดิม [${oldOtp}] ถูกยกเลิก ➔ ออกรหัสใหม่ <span class="text-amber-400 font-bold font-mono">${newOtp}</span> • คืนสล็อตเดิมสู่ระบบเรียบร้อย`);

      // Update Agent screen if playing as that agent
      if (currentAgentIdentity === c.agentCode) {
        activeAgentOtp = newOtp.toString();
        const display = document.getElementById("agentOtpDisplay");
        if (display) display.innerText = newOtp;
        const slotLabel = document.getElementById("agentOtpSlotLabel");
        if (slotLabel) slotLabel.innerText = `รหัส Smart Keybox OTP (รอบใหม่: ${newSlot})`;
        alert(`พี่ลิลลี่ได้เลื่อนวัน/รอบเวลาให้คุณเรียบร้อยแล้ว!\\nรอบใหม่: ${newSlot}\\nรหัส OTP ใหม่คือ: ${newOtp}`);
      }

      renderLilyActiveViewing();
    }

    function voidCase(caseId) {
      const c = approvedCases.find(item => item.id === caseId);
      if (!c) return;

      if (!confirm(`คุณต้องการยกเลิกนัดของ ${c.agentName} (${c.agentCode}) ใช่หรือไม่?\\nระบบจะยกเลิกรหัส OTP และคืนสิทธิ์สล็อตทันที`)) {
        return;
      }

      c.status = "VOIDED";
      playTone('error');
      logLilyBot(`🚫 <strong>ยกเลิกเคส:</strong> พี่ลิลลี่ยกเลิกนัด ${c.agentName} (${c.agentCode}) เรียบร้อย • รหัส OTP [${c.otp}] ถูก Void ทันที • คืนสล็อตว่างและโควต้าให้ตัวแทนเรียบร้อย`);
      renderLilyActiveViewing();
    }

    function agentRequestReschedule() {
      playTone('notify');
      const reason = prompt("กรุณาระบุรอบเวลาใหม่ที่ลูกค้าต้องการ (เช่น วันนี้ รอบบ่าย 13:30 น. หรือ พรุ่งนี้เช้า):", "วันนี้ รอบบ่าย (13:30 - 17:00 น.)");
      if (!reason) return;

      logLilyBot(`📢 <strong>คำขอจากตัวแทน:</strong> ${ALPHA_AGENTS[currentAgentIdentity]?.nickname || 'Agent'} แจ้งขอเลื่อนเวลาเป็น: "${reason}" กรุณากดปุ่ม 'เลื่อนวัน/รอบ' บนการ์ดเพื่ออนุมัติ`);
      alert("ส่งคำขอเลื่อนเวลาถึงพี่ลิลลี่เรียบร้อยแล้วครับ! เมื่อพี่ลิลลี่กดยืนยัน รหัส OTP ใหม่จะอัปเดตลงบนบัตรดิจิทัลทันที");

      // Find if this agent has an approved case in Lily's list
      const c = approvedCases.find(item => item.agentCode === currentAgentIdentity && item.status !== "CLOSED" && item.status !== "VOIDED");
      if (c) {
        openRescheduleModal(c.id);
      }
    }

    function agentRequestCancel() {
      if (!confirm("คุณต้องการแจ้งขอยกเลิกนัดเปิดบ้านรอบนี้ใช่หรือไม่?")) return;
      playTone('error');
      logLilyBot(`⚠️ <strong>แจ้งยกเลิกนัด:</strong> ${ALPHA_AGENTS[currentAgentIdentity]?.nickname || 'Agent'} แจ้งขอยกเลิกนัดลูกค้ากะทันหัน`);
      const c = approvedCases.find(item => item.agentCode === currentAgentIdentity && item.status !== "CLOSED");
      if (c) {
        c.status = "VOIDED";
        renderLilyActiveViewing();
      }
      document.getElementById("agentVoucherCard").classList.add("hidden");
      document.getElementById("agentRequestFormBox").classList.remove("hidden");
      alert("แจ้งยกเลิกนัดเรียบร้อย คืนสิทธิ์โควต้าและสล็อตว่างให้ระบบแล้วครับ");
    }
"""

content = content.replace("// =========================================================================", js_functions + "\n    // =========================================================================")

with open(FILE_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print("[OK] Successfully integrated Reschedule & Slot Adjustment System into siwasup_keybox_interactive_roleplay.html")
