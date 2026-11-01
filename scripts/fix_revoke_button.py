import os

html_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\admin_lobby_manager.html"

with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

# All JS functions for Revoke, Rollback, Backup, Audit Log
all_functions = """
    // ==========================================
    // REVOKE & ROLLBACK FUNCTIONS
    // ==========================================
    let pendingRevokeTarget = null;

    function openRevokeModal(id, name) {
      pendingRevokeTarget = { id: id, name: name };
      const el = document.getElementById('revokeTargetName');
      if (el) el.innerText = name;
      const modal = document.getElementById('revokeModal');
      if (modal) modal.classList.remove('hidden');
      if (window.lucide) lucide.createIcons();
    }

    function closeRevokeModal() {
      pendingRevokeTarget = null;
      const modal = document.getElementById('revokeModal');
      if (modal) modal.classList.add('hidden');
    }

    async function executeRevokeMember() {
      if (!pendingRevokeTarget) return;
      const targetId = pendingRevokeTarget.id;
      const targetName = pendingRevokeTarget.name;
      closeRevokeModal();

      const memberIdx = lobbyData.approved.findIndex(m => m.id === targetId);
      if (memberIdx === -1) {
        alert('ไม่พบรายชื่อในทำเนียบสมาชิก');
        return;
      }
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
      lobbyData.audit_log.unshift(`[${rollbackRecord.timestamp}] 🔴 คัดออก/เพิกถอนสิทธิ์: ${member.name} (${member.role || ''})`);

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
      if (!toast) return;
      const msgEl = document.getElementById('toastUndoMsg');
      if (msgEl) msgEl.innerText = msg;
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
        lobbyData.audit_log = lobbyData.audit_log || [];
        lobbyData.audit_log.unshift(`[${new Date().toLocaleString('th-TH')}] ↩️ Rollback คืนสิทธิ์: ${rb.member.name} สำเร็จ`);
        saveLobbyData();
        renderLobby();
        const toast = document.getElementById('toastUndo');
        if (toast) toast.classList.add('hidden');
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

      alert(`💾 สำรองข้อมูลเรียบร้อย!\\nบันทึกสถานะ snapshot ณ เวลาปัจจุบันไว้ในระบบ`);
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
      container.innerHTML = logs.slice(0, 30).map((log) => {
        const isRevoke = log.includes('คัดออก') || log.includes('เพิกถอน');
        const isApprove = log.includes('อนุมัติ');
        const isRollback = log.includes('Rollback') || log.includes('คืนสิทธิ์');
        const isBackup = log.includes('สำรองข้อมูล');
        
        let badge = '<span class="px-2 py-0.5 rounded text-[10px] bg-slate-100 text-slate-700 font-bold">INFO</span>';
        if (isRevoke) badge = '<span class="px-2 py-0.5 rounded text-[10px] bg-red-100 text-red-700 font-bold">🔴 REVOKE</span>';
        if (isApprove) badge = '<span class="px-2 py-0.5 rounded text-[10px] bg-emerald-100 text-emerald-700 font-bold">🟢 APPROVE</span>';
        if (isRollback) badge = '<span class="px-2 py-0.5 rounded text-[10px] bg-amber-100 text-amber-800 font-bold">↩️ ROLLBACK</span>';
        if (isBackup) badge = '<span class="px-2 py-0.5 rounded text-[10px] bg-blue-100 text-blue-700 font-bold">💾 BACKUP</span>';

        let rollbackBtn = '';
        if (isRevoke && lobbyData.rollback_history) {
          const matchRb = lobbyData.rollback_history.find(rb => rb && rb.member && log.includes(rb.member.name));
          if (matchRb) {
            rollbackBtn = `<button onclick="rollbackSpecific('${matchRb.rollback_id}')" class="ml-auto text-[11px] font-bold text-amber-600 hover:text-amber-800 underline shrink-0">↩️ กู้คืนสิทธิ์</button>`;
          }
        }

        return `
          <div class="flex items-center gap-2 p-2 rounded-xl bg-slate-50 hover:bg-slate-100 border border-slate-200 text-xs transition">
            ${badge}
            <span class="text-slate-700 flex-1 truncate font-mono text-[11px]">${log}</span>
            ${rollbackBtn}
          </div>
        `;
      }).join('');
    }
"""

# Cut modals from end of file if they are after </script>
modal_marker = "<!-- REVOKE CONFIRMATION MODAL -->"
if modal_marker in content:
    idx = content.find(modal_marker)
    modals_html = content[idx:]
    # Remove modals from end
    content = content[:idx].rstrip()
    if content.endswith("</body>"):
        content = content[:-7].rstrip()
    if content.endswith("</html>"):
        content = content[:-7].rstrip()
else:
    modals_html = ""

# Now insert all_functions before `fetchCloudLobby();`
target_insert = "fetchCloudLobby();\n    setInterval(fetchCloudLobby, 3000);"
if target_insert in content:
    content = content.replace(target_insert, all_functions + "\n    " + target_insert)
    print("SUCCESS: Inserted all JS functions before fetchCloudLobby!")
else:
    print("ERROR: target_insert not found")

# Now re-append modals HTML before </body></html>
content = content + "\n\n" + modals_html + "\n</body>\n</html>\n"

with open(html_path, "w", encoding="utf-8") as f:
    f.write(content)

print("FILE SAVED! Now verifying JavaScript syntax...")
