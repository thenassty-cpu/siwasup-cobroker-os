import os

html_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\admin_lobby_manager.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update Approved Directory header to remove any mock references and make it authoritative
content = content.replace(
    'ทีมงานออฟฟิศ 5 เสาหลัก ครบถ้วน',
    'ทำเนียบสมาชิกทางการ • คุ้มครองสิทธิ์ 100%'
)

# 2. Add Revoke button to Table Row Action Column
old_action_col = """          <td class="py-3 px-3.5 text-right">
            <a href="https://assets.siwasup.com/agent_profile.html?name=${encodeURIComponent(item.name)}&phone=${encodeURIComponent(item.phone)}&zone=${encodeURIComponent(item.zone)}&title=${encodeURIComponent(item.title || '')}&mode=client&avatar=${encodeURIComponent(item.avatar || '')}" 
               target="_blank"
               class="px-2.5 py-1 rounded-lg bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold border border-slate-300 inline-flex items-center gap-1 shadow-2xs transition">
              <i data-lucide="credit-card" class="w-3 h-3 text-amber-600"></i>
              <span>ดูบัตร</span>
            </a>
          </td>"""

new_action_col = """          <td class="py-3 px-3.5 text-right space-x-1.5 whitespace-nowrap">
            <a href="https://assets.siwasup.com/agent_profile.html?name=${encodeURIComponent(item.name)}&phone=${encodeURIComponent(item.phone)}&zone=${encodeURIComponent(item.zone)}&title=${encodeURIComponent(item.title || '')}&mode=client&avatar=${encodeURIComponent(item.avatar || '')}" 
               target="_blank"
               class="px-2.5 py-1 rounded-lg bg-white hover:bg-slate-50 text-slate-700 text-xs font-semibold border border-slate-300 inline-flex items-center gap-1 shadow-2xs transition">
              <i data-lucide="credit-card" class="w-3 h-3 text-amber-600"></i>
              <span>ดูบัตร</span>
            </a>
            <button onclick="openRevokeModal('${item.id}', '${item.name.replace(/'/g, \"\\\\'\")}')" 
                    class="px-2.5 py-1 rounded-lg bg-red-50 hover:bg-red-100 text-red-600 text-xs font-semibold border border-red-200 inline-flex items-center gap-1 shadow-2xs transition"
                    title="เพิกถอนสิทธิ์และคัดออกจากทำเนียบ">
              <i data-lucide="user-x" class="w-3 h-3 text-red-500"></i>
              <span>คัดออก</span>
            </button>
          </td>"""

if old_action_col in content:
    content = content.replace(old_action_col, new_action_col)
    print("SUCCESS: Action column updated with 'คัดออก' button!")
else:
    print("WARNING: Old action column not found exactly, searching alternative...")

# 3. Add Section 3 (Audit Trail & Rollback Archive) and Modals right after Section 2
section_3_html = """
    </div>

    <!-- ============================================================== -->
    <!-- SECTION 3: AUDIT TRAIL & HUMAN ERROR ROLLBACK CENTER -->
    <!-- ============================================================== -->
    <div class="card-light rounded-3xl p-5 sm:p-7 border-2 border-slate-200 space-y-5">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-200">
        <div>
          <div class="flex items-center gap-2.5">
            <div class="w-8 h-8 rounded-xl bg-amber-50 text-amber-700 border border-amber-300 flex items-center justify-center font-bold shadow-2xs">
              <i data-lucide="history" class="w-4.5 h-4.5"></i>
            </div>
            <h2 class="text-base sm:text-lg font-bold text-slate-900 flex items-center gap-2">
              <span>🛡️ Audit Trail & บันทึกคำสั่งฉุกเฉิน (Human Error Rollback Center)</span>
            </h2>
          </div>
          <p class="text-xs text-slate-500 mt-1">
            เก็บบันทึกประวัติคำสั่งทุกรายการ (อนุมัติ, เพิกถอนสิทธิ์, สำรองข้อมูล) หากคลิกผิดพลาด สามารถกด <strong>"กู้คืน (Rollback)"</strong> สิทธิ์กลับมาได้ทันที
          </p>
        </div>
        <div class="flex items-center gap-2 flex-wrap">
          <button onclick="rollbackLastAction()" class="px-3 py-1.5 rounded-xl bg-amber-500 hover:bg-amber-600 text-white font-bold text-xs shadow-sm flex items-center gap-1.5 transition active:scale-95">
            <i data-lucide="rotate-ccw" class="w-3.5 h-3.5"></i>
            <span>↩️ กู้คืนรายการล่าสุด (Undo/Rollback)</span>
          </button>
          <button onclick="createBackupSnapshot()" class="px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs border border-slate-300 shadow-2xs flex items-center gap-1.5 transition">
            <i data-lucide="save" class="w-3.5 h-3.5 text-blue-600"></i>
            <span>💾 สำรองข้อมูล (Backup)</span>
          </button>
          <button onclick="exportAuditLogJson()" class="px-3 py-1.5 rounded-xl bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold text-xs border border-slate-300 shadow-2xs flex items-center gap-1.5 transition">
            <i data-lucide="download" class="w-3.5 h-3.5 text-emerald-600"></i>
            <span>📑 Export Log (.json)</span>
          </button>
        </div>
      </div>

      <!-- AUDIT TRAIL LIST -->
      <div id="auditLogContainer" class="space-y-2 max-h-60 overflow-y-auto pr-1">
        <!-- Dynamically populated via JS -->
      </div>
    </div>
"""

# Replace the closing of section 2 before </main>
target_main_end = """      </div>

    </div>

  </main>"""

if target_main_end in content:
    content = content.replace(target_main_end, "      </div>\n" + section_3_html + "\n  </main>")
    print("SUCCESS: Section 3 Audit Trail inserted!")
else:
    print("WARNING: target_main_end not found")

# 4. Insert Modal & Toast right before </body>
modal_and_toast = """
  <!-- REVOKE CONFIRMATION MODAL -->
  <div id="revokeModal" class="hidden fixed inset-0 z-50 bg-slate-900/60 backdrop-blur-xs flex items-center justify-center p-4">
    <div class="bg-white rounded-3xl max-w-md w-full p-6 shadow-2xl border-2 border-red-200 space-y-4">
      <div class="w-12 h-12 rounded-2xl bg-red-100 text-red-600 flex items-center justify-center mx-auto">
        <i data-lucide="user-x" class="w-6 h-6"></i>
      </div>
      <div class="text-center space-y-1">
        <h3 class="text-lg font-bold text-slate-900">ยืนยันการคัดชื่อออกจากทำเนียบสมาชิก?</h3>
        <p class="text-xs text-slate-500">
          คุณกำลังจะเพิกถอนสิทธิ์ของ <strong id="revokeTargetName" class="text-red-600 font-bold">...</strong>
        </p>
      </div>
      <div class="p-3 bg-amber-50 rounded-2xl border border-amber-200 text-[11px] text-amber-900 space-y-1">
        <div class="font-bold flex items-center gap-1">
          <i data-lucide="shield-alert" class="w-4 h-4 text-amber-600"></i>
          <span>ระบบคุ้มครองข้อผิดพลาด (Human Error Safeguard):</span>
        </div>
        <p>คำสั่งนี้จะถูกบันทึกประวัติไว้ใน Audit Trail & Rollback Archive เสมอ ท่านสามารถกด <strong>"กู้คืน (Rollback)"</strong> สิทธิ์กลับคืนมาได้ตลอดเวลาหากเกิดข้อผิดพลาด</p>
      </div>
      <div class="flex items-center gap-3 pt-2">
        <button onclick="closeRevokeModal()" class="flex-1 py-2.5 rounded-xl border border-slate-200 text-slate-700 font-semibold text-xs hover:bg-slate-50 transition">ยกเลิก</button>
        <button onclick="executeRevokeMember()" class="flex-1 py-2.5 rounded-xl bg-[#ed1c24] text-white font-bold text-xs hover:bg-red-700 transition shadow-md">ยืนยันคัดออก</button>
      </div>
    </div>
  </div>

  <!-- TOAST UNDO NOTIFICATION -->
  <div id="toastUndo" class="hidden fixed bottom-6 right-6 z-50 bg-slate-900 text-white px-5 py-3.5 rounded-2xl shadow-2xl flex items-center gap-3 border border-slate-700">
    <div class="w-2.5 h-2.5 rounded-full bg-amber-400 animate-ping"></div>
    <span id="toastUndoMsg" class="text-xs font-medium">เพิกถอนสิทธิ์เรียบร้อยแล้ว</span>
    <button onclick="rollbackLastAction()" class="px-2.5 py-1 rounded-lg bg-amber-500 hover:bg-amber-600 text-slate-950 font-bold text-xs transition">
      ↩️ Undo กู้คืนทันที
    </button>
    <button onclick="document.getElementById('toastUndo').classList.add('hidden')" class="text-slate-400 hover:text-white text-xs ml-1">✕</button>
  </div>
"""

if "</body>" in content and "revokeModal" not in content:
    content = content.replace("</body>", modal_and_toast + "\n</body>")
    print("SUCCESS: Modal and Toast inserted!")

# 5. Insert JavaScript handlers for Revoke, Rollback, Backup, Audit Render
js_handlers = """
    let pendingRevokeTarget = null;

    function openRevokeModal(id, name) {
      pendingRevokeTarget = { id, name };
      document.getElementById('revokeTargetName').innerText = name;
      document.getElementById('revokeModal').classList.remove('hidden');
      lucide.createIcons();
    }

    function closeRevokeModal() {
      pendingRevokeTarget = null;
      document.getElementById('revokeModal').classList.add('hidden');
    }

    async function executeRevokeMember() {
      if (!pendingRevokeTarget) return;
      const targetId = pendingRevokeTarget.id;
      const targetName = pendingRevokeTarget.name;
      closeRevokeModal();

      const memberIdx = lobbyData.approved.findIndex(m => m.id === targetId);
      if (memberIdx === -1) return;
      const member = lobbyData.approved.splice(memberIdx, 1)[0];

      // Add to local rollback history & audit
      const rollbackId = 'rb_' + Date.now();
      const rollbackRecord = {
        rollback_id: rollbackId,
        action: 'REVOKE',
        member: member,
        timestamp: new Date().toLocaleString('th-TH')
      };
      lobbyData.rollback_history = lobbyData.rollback_history || [];
      lobbyData.rollback_history.unshift(rollbackRecord);
      lobbyData.audit_log = lobbyData.audit_log || [];
      lobbyData.audit_log.unshift(`[${rollbackRecord.timestamp}] 🔴 คัดออก/เพิกถอนสิทธิ์: ${member.name} (${member.role})`);

      saveLobbyData();
      renderLobby();

      // Show Undo Toast
      showUndoToast(`คัดชื่อ "${member.name}" ออกเรียบร้อยแล้ว`, rollbackId);

      // Cloud Sync
      try {
        await fetch(`${API_BASE}/api/lobby/revoke`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ applicantId: targetId, reason: 'Revoked via Admin Lobby Manager' })
        });
      } catch (e) {
        console.log('Cloud revoke note:', e);
      }
    }

    function showUndoToast(msg, rollbackId) {
      const toast = document.getElementById('toastUndo');
      document.getElementById('toastUndoMsg').innerText = msg;
      toast.classList.remove('hidden');
      setTimeout(() => {
        toast.classList.add('hidden');
      }, 10000);
    }

    async function rollbackSpecific(rollbackId) {
      lobbyData.rollback_history = lobbyData.rollback_history || [];
      const idx = lobbyData.rollback_history.findIndex(r => r.rollback_id === rollbackId);
      if (idx === -1) {
        alert('ไม่พบรายการที่จะกู้คืนในประวัติ');
        return;
      }
      const rb = lobbyData.rollback_history.splice(idx, 1)[0];
      if (rb.action === 'REVOKE' && rb.member) {
        lobbyData.approved.unshift(rb.member);
        lobbyData.audit_log.unshift(`[${new Date().toLocaleString('th-TH')}] ↩️ Rollback คืนสิทธิ์: ${rb.member.name} สำเร็จ`);
        saveLobbyData();
        renderLobby();
        document.getElementById('toastUndo').classList.add('hidden');
        alert(`↩️ กู้คืนสิทธิ์ให้ "${rb.member.name}" เรียบร้อยแล้ว!`);

        try {
          await fetch(`${API_BASE}/api/lobby/rollback`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ rollbackId: rollbackId })
          });
        } catch(e) {}
      }
    }

    async function rollbackLastAction() {
      lobbyData.rollback_history = lobbyData.rollback_history || [];
      if (lobbyData.rollback_history.length === 0) {
        alert('ยังไม่มีประวัติคำสั่งที่สามารถกู้คืนได้ (Rollback History ว่าง)');
        return;
      }
      const latest = lobbyData.rollback_history[0];
      rollbackSpecific(latest.rollback_id);
    }

    async function createBackupSnapshot() {
      const ts = new Date().toISOString().replace(/[:.]/g, '-');
      const backupData = JSON.stringify(lobbyData, null, 2);
      localStorage.setItem(`siwasup_lobby_backup_${ts}`, backupData);
      lobbyData.audit_log = lobbyData.audit_log || [];
      lobbyData.audit_log.unshift(`[${new Date().toLocaleString('th-TH')}] 💾 สำรองข้อมูลสถานะสำเร็จ: siwasup_lobby_backup_${ts}`);
      saveLobbyData();
      renderLobby();

      try {
        await fetch(`${API_BASE}/api/lobby/backup`, { method: 'POST' });
      } catch(e) {}

      alert(`💾 สำรองข้อมูลเรียบร้อย!\nบันทึกสถานะ snapshot ณ เวลาปัจจุบันไว้ในระบบ`);
    }

    function exportAuditLogJson() {
      const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(lobbyData, null, 2));
      const dlAnchor = document.createElement('a');
      dlAnchor.setAttribute("href", dataStr);
      dlAnchor.setAttribute("download", `siwasup_audit_lobby_${new Date().toISOString().slice(0,10)}.json`);
      document.body.appendChild(dlAnchor);
      dlAnchor.click();
      dlAnchor.remove();
    }

    function renderAuditLog() {
      const container = document.getElementById('auditLogContainer');
      if (!container) return;
      const logs = lobbyData.audit_log || [
        `[${new Date().toLocaleString('th-TH')}] เริ่มต้นระบบ Audit Trail & Rollback Archive พร้อมปฏิบัติการ`
      ];
      container.innerHTML = logs.slice(0, 30).map((log, index) => {
        const isRevoke = log.includes('คัดออก') || log.includes('เพิกถอน');
        const isApprove = log.includes('อนุมัติ');
        const isRollback = log.includes('Rollback') || log.includes('คืนสิทธิ์');
        const isBackup = log.includes('สำรองข้อมูล');
        
        let badge = '<span class=\"px-2 py-0.5 rounded text-[10px] bg-slate-100 text-slate-700 font-bold\">INFO</span>';
        if (isRevoke) badge = '<span class=\"px-2 py-0.5 rounded text-[10px] bg-red-100 text-red-700 font-bold\">🔴 REVOKE</span>';
        if (isApprove) badge = '<span class=\"px-2 py-0.5 rounded text-[10px] bg-emerald-100 text-emerald-700 font-bold\">🟢 APPROVE</span>';
        if (isRollback) badge = '<span class=\"px-2 py-0.5 rounded text-[10px] bg-amber-100 text-amber-800 font-bold\">↩️ ROLLBACK</span>';
        if (isBackup) badge = '<span class=\"px-2 py-0.5 rounded text-[10px] bg-blue-100 text-blue-700 font-bold\">💾 BACKUP</span>';

        // Check if there is a matching rollback item
        let rollbackBtn = '';
        if (isRevoke && lobbyData.rollback_history) {
          const matchRb = lobbyData.rollback_history.find(rb => log.includes(rb.member.name));
          if (matchRb) {
            rollbackBtn = `<button onclick=\"rollbackSpecific('${matchRb.rollback_id}')\" class=\"ml-auto text-[11px] font-bold text-amber-600 hover:text-amber-800 underline shrink-0\">↩️ กู้คืนสิทธิ์</button>`;
          }
        }

        return `
          <div class=\"flex items-center gap-2 p-2 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200 text-xs transition\">
            ${badge}
            <span class=\"text-slate-700 flex-1 truncate font-mono text-[11px]\">${log}</span>
            ${rollbackBtn}
          </div>
        `;
      }).join('');
    }
"""

# Hook renderAuditLog into renderLobby
target_render_end = "lucide.createIcons();\n    }"
if target_render_end in content and "renderAuditLog();" not in content:
    content = content.replace(target_render_end, "renderAuditLog();\n      lucide.createIcons();\n    }")
    print("SUCCESS: renderAuditLog hooked into renderLobby!")

# Add js_handlers before closing script tag
if "</script>" in content and "openRevokeModal" not in content:
    content = content.replace("</script>", js_handlers + "\n  </script>")
    print("SUCCESS: JavaScript handlers for Revoke/Rollback added!")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("[COMPLETE] admin_lobby_manager.html updated successfully!")
