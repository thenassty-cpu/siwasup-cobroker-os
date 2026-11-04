import os, sys

ROOT = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"

# 1. Patch scripts/line_gemini_webhook.py
wh_path = os.path.join(ROOT, "scripts", "line_gemini_webhook.py")
with open(wh_path, "r", encoding="utf-8") as f:
    wh_code = f.read()

# Add synchronous R2 save in save_lobby_data and also flush in handle_render_shutdown
old_save_lobby = """        if put_object_r2 and os.environ.get("PORT"):
            threading.Thread(target=lambda: put_object_r2(_R2_LOBBY_VAULT_KEY, data_bytes, "application/json"), daemon=True).start()"""

new_save_lobby = """        if put_object_r2 and os.environ.get("PORT"):
            try:
                put_object_r2(_R2_LOBBY_VAULT_KEY, data_bytes, "application/json")
                put_object_r2("data/lobby_applicants.json", data_bytes, "application/json; charset=utf-8")
            except Exception as e:
                print(f"[R2 Vault Sync Error]: {e}")"""

if old_save_lobby in wh_code:
    wh_code = wh_code.replace(old_save_lobby, new_save_lobby, 1)
    print("[OK] Patched save_lobby_data in line_gemini_webhook.py")

old_shutdown = """            with CONTRACTS_LOCK:
                c_store = load_contracts_data()
                c_bytes = json.dumps(c_store, ensure_ascii=False, indent=2).encode("utf-8")
                put_object_r2(_R2_CONTRACTS_VAULT_KEY, c_bytes, "application/json")
                print("[+] Exclusive contracts vault flushed to Cloudflare R2 before sleep!")"""

new_shutdown = """            with CONTRACTS_LOCK:
                c_store = load_contracts_data()
                c_bytes = json.dumps(c_store, ensure_ascii=False, indent=2).encode("utf-8")
                put_object_r2(_R2_CONTRACTS_VAULT_KEY, c_bytes, "application/json")
                print("[+] Exclusive contracts vault flushed to Cloudflare R2 before sleep!")
            with LOBBY_LOCK:
                l_store = load_lobby_data()
                l_bytes = json.dumps(l_store, ensure_ascii=False, indent=2).encode("utf-8")
                put_object_r2(_R2_LOBBY_VAULT_KEY, l_bytes, "application/json")
                put_object_r2("data/lobby_applicants.json", l_bytes, "application/json; charset=utf-8")
                print("[+] Lobby applicants vault flushed to Cloudflare R2 before sleep!")"""

if old_shutdown in wh_code:
    wh_code = wh_code.replace(old_shutdown, new_shutdown, 1)
    print("[OK] Patched handle_render_shutdown in line_gemini_webhook.py")

with open(wh_path, "w", encoding="utf-8") as f:
    f.write(wh_code)

# 2. Patch admin_lobby_manager.html fetchCloudLobby with Smart Merge
mgr_path = os.path.join(ROOT, "admin_lobby_manager.html")
with open(mgr_path, "r", encoding="utf-8") as f:
    mgr_code = f.read()

old_fetch = """    async function fetchCloudLobby() {
      try {
        const res = await fetch(`${API_BASE}/api/lobby/list`, { cache: 'no-store' });
        if (res.status === 401 || res.status === 403) { showAdminGate(res.status); return; }
        if (res.ok) {
          const cloudData = await res.json();
          if (cloudData && (cloudData.pending || cloudData.approved)) {
            normalizeNasstySeat(cloudData);
            lobbyData = cloudData;
            localStorage.setItem('siwasup_lobby_data', JSON.stringify(lobbyData));
            renderLobby();
            return;
          }
        }
      } catch (err) {
        console.log('[Lobby] Cloud sync:', err);
      }
      lobbyData = JSON.parse(localStorage.getItem('siwasup_lobby_data')) || DEFAULT_DATA;
      normalizeNasstySeat(lobbyData);
      renderLobby();
    }"""

new_fetch = """    function mergeLobbyStores(local, cloud) {
      if (!cloud) return local || DEFAULT_DATA;
      if (!local) return cloud;

      const map = new Map();
      // First populate with local
      (local.approved || []).forEach(m => { if (m && (m.id || m.phone)) map.set(m.id || m.phone, m); });
      // Then merge cloud, but don't drop members present only in local
      (cloud.approved || []).forEach(m => {
        if (!m) return;
        const k = m.id || m.phone;
        if (!map.has(k)) {
          map.set(k, m);
        } else {
          // Merge properties, prioritizing valid non-empty fields
          const existing = map.get(k);
          map.set(k, Object.assign({}, existing, m));
        }
      });

      const pMap = new Map();
      (local.pending || []).forEach(p => { if (p && (p.id || p.phone)) pMap.set(p.id || p.phone, p); });
      (cloud.pending || []).forEach(p => { if (p && (p.id || p.phone)) pMap.set(p.id || p.phone, p); });

      return {
        updated_at: cloud.updated_at || local.updated_at || new Date().toISOString(),
        pending: Array.from(pMap.values()),
        approved: Array.from(map.values()),
        audit_log: (cloud.audit_log && cloud.audit_log.length > (local.audit_log || []).length) ? cloud.audit_log : (local.audit_log || [])
      };
    }

    async function fetchCloudLobby() {
      let localStore = null;
      try {
        localStore = JSON.parse(localStorage.getItem('siwasup_lobby_data'));
      } catch (e) {}

      // Dual-path fetch: Try Render API first, then Cloudflare R2 backup
      let fetchedCloudData = null;
      try {
        const res = await fetch(`${API_BASE}/api/lobby/list`, { cache: 'no-store' });
        if (res.status === 401 || res.status === 403) { showAdminGate(res.status); return; }
        if (res.ok) {
          fetchedCloudData = await res.json();
        }
      } catch (err) {
        console.log('[Lobby] Render API offline or sleepy:', err);
      }

      // If Render gave 0 or 1 item or failed, fetch latest R2 static replica
      if (!fetchedCloudData || !fetchedCloudData.approved || fetchedCloudData.approved.length <= 1) {
        try {
          const r2Res = await fetch(`https://assets.siwasup.com/data/lobby_applicants.json?t=${Date.now()}`, { cache: 'no-store' });
          if (r2Res.ok) {
            const r2Data = await r2Res.json();
            if (r2Data && Array.isArray(r2Data.approved) && r2Data.approved.length > 1) {
              fetchedCloudData = r2Data;
              console.log('[Lobby] Successfully loaded R2 static replica with', r2Data.approved.length, 'members');
            }
          }
        } catch (r2Err) {
          console.log('[Lobby] R2 fallback note:', r2Err);
        }
      }

      // Smart Merge: NEVER overwrite a larger local roster with an empty/1-person cloud
      lobbyData = mergeLobbyStores(localStore, fetchedCloudData);
      normalizeNasstySeat(lobbyData);
      localStorage.setItem('siwasup_lobby_data', JSON.stringify(lobbyData));
      renderLobby();
    }"""

if old_fetch in mgr_code:
    mgr_code = mgr_code.replace(old_fetch, new_fetch, 1)
    print("[OK] Patched fetchCloudLobby with Smart Merge in admin_lobby_manager.html")
else:
    print("[WARN] old_fetch not found in admin_lobby_manager.html")

with open(mgr_path, "w", encoding="utf-8") as f:
    f.write(mgr_code)

print("Patching completed!")
