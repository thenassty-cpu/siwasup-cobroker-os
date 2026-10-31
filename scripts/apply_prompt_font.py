import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from overnight_r2_crawler import put_object_r2

BASE_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"

for fname in ["index.html", "catalog.html"]:
    fpath = os.path.join(BASE_DIR, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        html = f.read().replace("\r\n", "\n")

    # 1. Add Google Fonts Prompt with preconnect
    old_font_link = '<link href="https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700;800;900&family=Tahoma&display=swap" rel="stylesheet">'
    new_font_link = """  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Prompt:ital,wght@0,300;0,400;0,500;0,600;0,700;0,800;1,400&family=Kanit:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">"""

    if old_font_link in html:
        html = html.replace(old_font_link, new_font_link)
        print(f"Updated font link in {fname}")

    # 2. Update Tailwind config right after cdn.tailwindcss.com
    old_tw = '<script src="https://cdn.tailwindcss.com"></script>'
    new_tw = """<script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          fontFamily: {
            sans: ['Prompt', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'Roboto', 'sans-serif'],
          }
        }
      }
    };
  </script>"""

    if old_tw in html and "tailwind.config" not in html:
        html = html.replace(old_tw, new_tw)
        print(f"Added Tailwind Prompt config in {fname}")

    # 3. Apply Prompt globally in style
    old_style = "html, body { overflow-x: hidden; max-width: 100%; width: 100%; font-family: 'Kanit', 'Tahoma', sans-serif; -webkit-tap-highlight-color: transparent; }"
    new_style = """* { font-family: 'Prompt', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
    html, body, button, input, select, textarea { overflow-x: hidden; max-width: 100%; width: 100%; font-family: 'Prompt', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important; -webkit-tap-highlight-color: transparent; }"""

    if old_style in html:
        html = html.replace(old_style, new_style)
        print(f"Applied Prompt CSS rule in {fname}")

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html)

    res = put_object_r2(fname, html.encode("utf-8"), "text/html; charset=utf-8")
    print(f"Uploaded {fname} to Cloudflare R2 (status={res})")
