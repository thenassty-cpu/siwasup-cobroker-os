import re

# 1. Patch admin_lobby_manager.html
admin_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\admin_lobby_manager.html"
with open(admin_path, "r", encoding="utf-8") as f:
    admin_content = f.read()

old_script_start = "// Load from LocalStorage or use Default\n    let lobbyData = JSON.parse(localStorage.getItem('siwasup_lobby_data')) || DEFAULT_DATA;"

new_script_start = '''    const API_BASE = 'https://siwasup-cobroker-os.onrender.com';
    let lobbyData = JSON.parse(localStorage.getItem('siwasup_lobby_data')) || DEFAULT_DATA;

    async function fetchCloudLobby() {
      try {
        const res = await fetch(`${API_BASE}/api/lobby/list`, { cache: 'no-store' });
        if (res.ok) {
          const cloudData = await res.json();
          if (cloudData && (cloudData.pending || cloudData.approved)) {
            lobbyData = cloudData;
            localStorage.setItem('siwasup_lobby_data', JSON.stringify(lobbyData));
            renderLobby();
            return;
          }
        }
      } catch (err) {
        console.log('[Lobby] Cloud sync connecting:', err);
      }
      lobbyData = JSON.parse(localStorage.getItem('siwasup_lobby_data')) || DEFAULT_DATA;
      renderLobby();
    }'''

admin_content_norm = admin_content.replace("\r\n", "\n")
old_start_norm = old_script_start.replace("\r\n", "\n")

if old_start_norm in admin_content_norm:
    admin_content_norm = admin_content_norm.replace(old_start_norm, new_script_start)
    print("Patched admin_lobby_manager start")
else:
    print("Warning: old_start_norm not found")

# Patch approveWithPreset
old_approve = '''    function approveWithPreset(applicantId, presetKey) {
      const idx = lobbyData.pending.findIndex(a => a.id === applicantId);
      if (idx === -1) return;

      const applicant = lobbyData.pending[idx];
      const preset = ROLE_PRESETS[presetKey];'''

new_approve = '''    async function approveWithPreset(applicantId, presetKey) {
      const idx = lobbyData.pending.findIndex(a => a.id === applicantId);
      if (idx === -1) return;

      const applicant = lobbyData.pending[idx];
      const preset = ROLE_PRESETS[presetKey];

      // Notify Cloud Backend
      try {
        await fetch(`${API_BASE}/api/lobby/approve`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            applicantId: applicantId,
            role: preset.role,
            title: preset.title,
            badges: preset.badges,
            permissions: preset.permissions
          })
        });
      } catch(e) {
        console.error('Cloud approve error:', e);
      }'''

old_approve_norm = old_approve.replace("\r\n", "\n")
if old_approve_norm in admin_content_norm:
    admin_content_norm = admin_content_norm.replace(old_approve_norm, new_approve)
    print("Patched approveWithPreset in admin")
else:
    print("Warning: old_approve_norm not found")

# Patch rejectApplicant
old_reject = '''    function rejectApplicant(applicantId) {
      if (!confirm("คุณต้องการปฏิเสธและดีดรายชื่อนี้ออกจาก Lobby ใช่หรือไม่?")) return;
      lobbyData.pending = lobbyData.pending.filter(a => a.id !== applicantId);'''

new_reject = '''    async function rejectApplicant(applicantId) {
      if (!confirm("คุณต้องการปฏิเสธและดีดรายชื่อนี้ออกจาก Lobby ใช่หรือไม่?")) return;
      try {
        await fetch(`${API_BASE}/api/lobby/reject`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ applicantId })
        });
      } catch(e) {}
      lobbyData.pending = lobbyData.pending.filter(a => a.id !== applicantId);'''

old_reject_norm = old_reject.replace("\r\n", "\n")
if old_reject_norm in admin_content_norm:
    admin_content_norm = admin_content_norm.replace(old_reject_norm, new_reject)
    print("Patched rejectApplicant in admin")
else:
    print("Warning: old_reject_norm not found")

# Add auto-poll at the end
old_render_call = "// Initial render\n    renderLobby();"
new_render_call = """// Initial cloud fetch and 3-second auto-polling
    fetchCloudLobby();
    setInterval(fetchCloudLobby, 3000);"""

old_render_norm = old_render_call.replace("\r\n", "\n")
if old_render_norm in admin_content_norm:
    admin_content_norm = admin_content_norm.replace(old_render_norm, new_render_call)
    print("Patched initial render & polling in admin")
else:
    print("Warning: old_render_norm not found")

with open(admin_path, "w", encoding="utf-8") as f:
    f.write(admin_content_norm)


# 2. Patch agent_registration.html
reg_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\agent_registration.html"
with open(reg_path, "r", encoding="utf-8") as f:
    reg_content = f.read()

reg_content_norm = reg_content.replace("\r\n", "\n")

old_submit = """      // 1. Save to LocalStorage & Broadcast to Admin Tab
      const rawData = localStorage.getItem('siwasup_lobby_data');
      let lobbyData = rawData ? JSON.parse(rawData) : { pending: [], approved: [] };
      lobbyData.pending.unshift(currentApplicant);
      localStorage.setItem('siwasup_lobby_data', JSON.stringify(lobbyData));"""

new_submit = """      // 1. Sync to Cloud Server & LocalStorage
      try {
        fetch('https://siwasup-cobroker-os.onrender.com/api/lobby/register', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(currentApplicant)
        }).catch(err => console.error('Cloud register error:', err));
      } catch(e) {}

      const rawData = localStorage.getItem('siwasup_lobby_data');
      let lobbyData = rawData ? JSON.parse(rawData) : { pending: [], approved: [] };
      lobbyData.pending.unshift(currentApplicant);
      localStorage.setItem('siwasup_lobby_data', JSON.stringify(lobbyData));"""

old_submit_norm = old_submit.replace("\r\n", "\n")
if old_submit_norm in reg_content_norm:
    reg_content_norm = reg_content_norm.replace(old_submit_norm, new_submit)
    print("Patched submit in agent_registration")
else:
    print("Warning: old_submit_norm not found")

# Patch checkApprovalStatus
old_check = """    function checkApprovalStatus() {
      if (!currentApplicant) return;

      const rawData = localStorage.getItem('siwasup_lobby_data');
      if (!rawData) return;
      const lobbyData = JSON.parse(rawData);

      // Check if current applicant exists in approved list
      const approved = lobbyData.approved.find(a => a.id === currentApplicant.id || a.phone === currentApplicant.phone);
      if (approved) {
        clearInterval(pollInterval);
        handleApplicantApproved(approved);
      }
    }"""

new_check = """    async function checkApprovalStatus() {
      if (!currentApplicant) return;

      // Check Cloud Server First
      try {
        const res = await fetch(`https://siwasup-cobroker-os.onrender.com/api/lobby/status?id=${encodeURIComponent(currentApplicant.id)}&phone=${encodeURIComponent(currentApplicant.phone)}`, { cache: 'no-store' });
        if (res.ok) {
          const data = await res.json();
          if (data.status === 'approved' && data.applicant) {
            clearInterval(pollInterval);
            handleApplicantApproved(data.applicant);
            return;
          }
        }
      } catch (e) {}

      // Fallback: LocalStorage
      const rawData = localStorage.getItem('siwasup_lobby_data');
      if (!rawData) return;
      const lobbyData = JSON.parse(rawData);
      const approved = lobbyData.approved.find(a => a.id === currentApplicant.id || a.phone === currentApplicant.phone);
      if (approved) {
        clearInterval(pollInterval);
        handleApplicantApproved(approved);
      }
    }"""

old_check_norm = old_check.replace("\r\n", "\n")
if old_check_norm in reg_content_norm:
    reg_content_norm = reg_content_norm.replace(old_check_norm, new_check)
    print("Patched checkApprovalStatus in agent_registration")
else:
    print("Warning: old_check_norm not found")

with open(reg_path, "w", encoding="utf-8") as f:
    f.write(reg_content_norm)

print("Finished patching cloud sync in both frontend files!")
