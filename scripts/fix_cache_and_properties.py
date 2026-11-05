import os
import sys

REPO_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
JS_PATH = os.path.join(REPO_DIR, "siwasup_all_properties.js")
CATALOG_PATH = os.path.join(REPO_DIR, "catalog.html")
INDEX_PATH = os.path.join(REPO_DIR, "index.html")
SW_PATH = os.path.join(REPO_DIR, "sw.js")

# 1. Update siwasup_all_properties.js
print("[1] Updating siwasup_all_properties.js header...")
with open(JS_PATH, "r", encoding="utf-8") as f:
    js_content = f.read()

prefix = "window.SIWASUP_ALL_PROPERTIES = "
if js_content.startswith(prefix):
    json_part = js_content[len(prefix):].rstrip().rstrip(";")
    new_js = f"window.ALL_PROPERTIES_DATA = {json_part};\nwindow.SIWASUP_PROPERTIES = window.ALL_PROPERTIES_DATA;\nwindow.SIWASUP_ALL_PROPERTIES = window.ALL_PROPERTIES_DATA;\n"
    with open(JS_PATH, "w", encoding="utf-8") as f:
        f.write(new_js)
    print(" -> Successfully updated siwasup_all_properties.js header with all 3 global aliases!")
else:
    print(f" -> Current start: {js_content[:60]}")

# 2. Update catalog.html
print("[2] Updating catalog.html cache busters and variable fallback...")
with open(CATALOG_PATH, "r", encoding="utf-8") as f:
    cat_content = f.read()

# Replace script tags with new timestamp
old_script = 'src="siwasup_all_properties.js?v=20261104-1300"'
new_script = 'src="siwasup_all_properties.js?v=20261106-0130"'
cat_content = cat_content.replace(old_script, new_script)

# Also ensure loadProperties checks SIWASUP_ALL_PROPERTIES and has cache bust for fetch
old_fallback = """    async function loadProperties() {
      if (typeof ALL_PROPERTIES_DATA !== 'undefined' && ALL_PROPERTIES_DATA.length > 0) {
        allProperties = ALL_PROPERTIES_DATA;
      } else if (window.SIWASUP_PROPERTIES && window.SIWASUP_PROPERTIES.length > 0) {
        allProperties = window.SIWASUP_PROPERTIES;
      } else {
        try {
          const resp = await fetch('siwasup_all_properties.json');
          if (resp.ok) {
            allProperties = await resp.json();
          }
        } catch (e) {
          console.log("Using fallback sample properties");
        }
      }"""

new_fallback = """    async function loadProperties() {
      if (typeof ALL_PROPERTIES_DATA !== 'undefined' && ALL_PROPERTIES_DATA.length > 0) {
        allProperties = ALL_PROPERTIES_DATA;
      } else if (window.SIWASUP_ALL_PROPERTIES && window.SIWASUP_ALL_PROPERTIES.length > 0) {
        allProperties = window.SIWASUP_ALL_PROPERTIES;
      } else if (window.SIWASUP_PROPERTIES && window.SIWASUP_PROPERTIES.length > 0) {
        allProperties = window.SIWASUP_PROPERTIES;
      } else {
        try {
          const resp = await fetch('siwasup_all_properties.json?v=20261106-0130');
          if (resp.ok) {
            allProperties = await resp.json();
          }
        } catch (e) {
          console.log("Using fallback sample properties");
        }
      }"""

cat_content = cat_content.replace(old_fallback, new_fallback)

# Update allProperties inline declaration
old_decl = "let allProperties = (typeof ALL_PROPERTIES_DATA !== 'undefined' && Array.isArray(ALL_PROPERTIES_DATA)) ? ALL_PROPERTIES_DATA : [];"
new_decl = "let allProperties = (typeof ALL_PROPERTIES_DATA !== 'undefined' && Array.isArray(ALL_PROPERTIES_DATA)) ? ALL_PROPERTIES_DATA : ((typeof window !== 'undefined' && (window.SIWASUP_ALL_PROPERTIES || window.SIWASUP_PROPERTIES)) ? (window.SIWASUP_ALL_PROPERTIES || window.SIWASUP_PROPERTIES) : []);"
cat_content = cat_content.replace(old_decl, new_decl)

with open(CATALOG_PATH, "w", encoding="utf-8") as f:
    f.write(cat_content)
print(" -> Successfully updated catalog.html!")

# 3. Update index.html
print("[3] Updating index.html cache busters and variable fallback...")
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    idx_content = f.read()

idx_content = idx_content.replace(old_script, new_script)
idx_content = idx_content.replace(old_fallback, new_fallback)
idx_content = idx_content.replace(old_decl, new_decl)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(idx_content)
print(" -> Successfully updated index.html!")

# 4. Update sw.js cache name
print("[4] Updating sw.js cache version...")
with open(SW_PATH, "r", encoding="utf-8") as f:
    sw_content = f.read()

old_cache = "const CACHE_NAME = 'siwasup-os-v20261104-2215';"
new_cache = "const CACHE_NAME = 'siwasup-os-v20261106-0130';"
sw_content = sw_content.replace(old_cache, new_cache)

with open(SW_PATH, "w", encoding="utf-8") as f:
    f.write(sw_content)
print(" -> Successfully updated sw.js cache name!")

print("=== ALL LOCAL UPDATES FINISHED ===")
