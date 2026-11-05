import os
import re

REPO_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
CATALOG_PATH = os.path.join(REPO_DIR, "catalog.html")
INDEX_PATH = os.path.join(REPO_DIR, "index.html")

def fix_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Target the problematic block around line 5712
    old_block_pattern = re.compile(
        r'// Auto-run \(Load properties FIRST so allProperties is populated before checkUrlParameters / setMode!\)\s*'
        r'loadProperties\(\);\s*'
        r'checkUrlParameters\(\);\s*'
        r'if \(typeof checkPdpaConsent === \'function\'\) checkPdpaConsent\(\);\s*'
        r'initModalScrollLockObserver\(\);\s*'
        r'if \(typeof updateProfileButtons === \'function\' && typeof getActiveAgentRef === \'function\'\) \{\s*'
        r'updateProfileButtons\(getActiveAgentRef\(\)\);\s*'
        r'\}\s*'
        r'document\.addEventListener\(\'DOMContentLoaded\', \(\) => \{\s*'
        r'initModalScrollLockObserver\(\);\s*'
        r'if \(typeof updateProfileButtons === \'function\' && typeof getActiveAgentRef === \'function\'\) \{\s*'
        r'updateProfileButtons\(getActiveAgentRef\(\)\);\s*'
        r'\}\s*'
        r'if \(window\.lucide\) \{ lucide\.createIcons\(\); \}\s*'
        r'\}\);',
        re.DOTALL
    )

    new_block = """    // Robust Auto-run & Guaranteed Instant Render (No White/Skeleton Screen!)
    async function initCatalogApp() {
      try {
        await loadProperties();
      } catch (err) {
        console.warn("loadProperties fallback:", err);
      }
      
      if (typeof renderProperties === 'function') {
        renderProperties();
      }
      if (typeof checkAndOpenTargetProperty === 'function') {
        checkAndOpenTargetProperty();
      }
      if (typeof checkPdpaConsent === 'function') {
        checkPdpaConsent();
      }
      if (typeof initModalScrollLockObserver === 'function') {
        initModalScrollLockObserver();
      }
      if (typeof updateProfileButtons === 'function' && typeof getActiveAgentRef === 'function') {
        updateProfileButtons(getActiveAgentRef());
      }
      if (window.lucide) {
        lucide.createIcons();
      }
    }

    // Execute immediately and on DOM/Window ready
    initCatalogApp();
    document.addEventListener('DOMContentLoaded', () => {
      initCatalogApp();
    });
    window.addEventListener('load', () => {
      const plist = document.getElementById('property-list');
      if (!plist || plist.innerHTML.includes('Skeleton') || plist.children.length === 0) {
        if (typeof renderProperties === 'function') renderProperties();
      }
    });"""

    if old_block_pattern.search(content):
        content = old_block_pattern.sub(new_block, content)
        print(f"[OK] Replaced problematic auto-run block in {file_path}")
    else:
        # Fallback replacement
        content = content.replace("checkUrlParameters();", "// checkUrlParameters removed (use checkAndOpenTargetProperty)")
        print(f"[OK] Fallback replaced checkUrlParameters in {file_path}")

    # Bump cache buster
    content = re.sub(r'v=20261106-\d+', 'v=20261106-0150', content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

fix_file(CATALOG_PATH)
fix_file(INDEX_PATH)

# Bump sw.js
SW_PATH = os.path.join(REPO_DIR, "sw.js")
with open(SW_PATH, "r", encoding="utf-8") as f:
    sw_c = f.read()
sw_c = re.sub(r"const CACHE_NAME = 'siwasup-os-v[^']+';", "const CACHE_NAME = 'siwasup-os-v20261106-0150';", sw_c)
with open(SW_PATH, "w", encoding="utf-8") as f:
    f.write(sw_c)
print("[OK] Bumped sw.js to v20261106-0150")
