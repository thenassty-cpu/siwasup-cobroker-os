import re

FILE_PATH = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\agent_profile.html"

with open(FILE_PATH, "r", encoding="utf-8") as f:
    content = f.read()

target = '    function init() {\n      const code = (getParam("code") || "S98").toUpperCase();\n      const mode = (getParam("mode") || "").toLowerCase();\n      const metric = (getParam("metric") || "opt1").toLowerCase();'

target_crlf = target.replace('\n', '\r\n')

replacement = '''    function init() {
      const customName = getParam("name");
      const customPhone = getParam("phone") || getParam("tel");
      const customZone = getParam("zone");
      const customTitle = getParam("title");
      const customNickname = getParam("nickname");
      const customCode = (getParam("code") || "STAFF").toUpperCase();

      if (customName) {
        AGENTS[customCode] = {
          code: customCode,
          name: customName,
          nickname: customNickname || customName,
          phoneRaw: customPhone ? customPhone.replace(/\\D/g, '') : "020000000",
          phoneFormatted: customPhone || "02 000 0000",
          lineId: getParam("line") || "",
          zone: customZone ? (customZone.startsWith("📍") ? customZone : `📍 ${customZone}`) : "📍 สำนักงานใหญ่",
          clientTitle: customTitle || "Senior Property Consultant",
          goldBadge: "assets/badges/Golden__001_lion_web.png",
          avatar: getParam("avatar") || "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=300&auto=format&fit=crop&q=80"
        };
        const sel = document.getElementById("agentSelect");
        if (sel) {
          const opt = document.createElement("option");
          opt.value = customCode;
          opt.innerText = `${customCode}: ${customName}`;
          sel.prepend(opt);
        }
      }

      const code = customName ? customCode : (getParam("code") || "S98").toUpperCase();
      const mode = (getParam("mode") || "").toLowerCase();
      const metric = (getParam("metric") || "opt1").toLowerCase();'''

replacement_crlf = replacement.replace('\n', '\r\n')

if target_crlf in content:
    content = content.replace(target_crlf, replacement_crlf, 1)
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("[OK] Successfully patched agent_profile.html for dynamic URL parameters!")
elif target in content:
    content = content.replace(target, replacement, 1)
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write(content)
    print("[OK] Successfully patched agent_profile.html (LF mode)!")
else:
    print("[ERR] Target not found")
