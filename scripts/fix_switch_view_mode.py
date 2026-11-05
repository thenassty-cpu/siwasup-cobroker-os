import os

REPO_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
CATALOG_PATH = os.path.join(REPO_DIR, "catalog.html")
INDEX_PATH = os.path.join(REPO_DIR, "index.html")

def fix_switch_view(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    old_func = """    function switchViewMode(mode) {
      currentViewMode = mode;
      renderPropertyCards();
    }"""

    new_func = """    function switchViewMode(mode) {
      currentViewMode = mode;
      if (typeof renderProperties === 'function') {
        renderProperties();
      } else if (typeof renderPropertyCards === 'function') {
        renderPropertyCards();
      }
    }"""

    if old_func in content:
        content = content.replace(old_func, new_func)
        print(f"[OK] Fixed switchViewMode in {file_path}")
    else:
        # Fallback regex
        content = content.replace("renderPropertyCards();", "renderProperties();")
        print(f"[OK] Replaced renderPropertyCards with renderProperties in {file_path}")

    # Also update cache busters to make sure fresh code runs
    content = content.replace('v=20261106-0130', 'v=20261106-0140')

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

fix_switch_view(CATALOG_PATH)
fix_switch_view(INDEX_PATH)

# Also bump sw.js cache name
SW_PATH = os.path.join(REPO_DIR, "sw.js")
with open(SW_PATH, "r", encoding="utf-8") as f:
    sw_c = f.read()
sw_c = sw_c.replace('siwasup-os-v20261106-0130', 'siwasup-os-v20261106-0140')
with open(SW_PATH, "w", encoding="utf-8") as f:
    f.write(sw_c)
print("[OK] Bumped sw.js cache version!")
