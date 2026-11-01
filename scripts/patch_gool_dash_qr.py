file_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\gool_executive_dashboard.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace grid-cols-4 with grid-cols-5
content = content.replace('grid-cols-2 sm:grid-cols-4', 'grid-cols-2 sm:grid-cols-5', 1)

qr_button = '''
        <a href="https://assets.siwasup.com/agent_onboarding_qr.html" target="_blank" class="p-3 rounded-2xl bg-amber-500/10 hover:bg-amber-500/20 border border-amber-500/40 text-left transition space-y-1 shadow-md">
          <div class="font-bold text-amber-300 flex items-center gap-1.5">
            <i data-lucide="qr-code" class="w-4 h-4 text-amber-400"></i>
            <span>ป้ายสแกน QR หน้างาน</span>
          </div>
          <div class="text-[10px] text-amber-200/80">โชว์จอ / พิมพ์ Tent Card</div>
        </a>
'''

pos = content.rfind('</a>\n\n      </div>')
if pos != -1:
    content = content[:pos+4] + qr_button + content[pos+4:]
    print("Found anchor and inserted QR button")
else:
    pos_crlf = content.rfind('</a>\r\n\r\n      </div>')
    if pos_crlf != -1:
        content = content[:pos_crlf+4] + qr_button + content[pos_crlf+4:]
        print("Found CRLF anchor and inserted QR button")
    else:
        print("Could not find anchor")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content)

print("Done patching gool_executive_dashboard.html")
