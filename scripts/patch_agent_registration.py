import sys

file_path = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\agent_registration.html"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# 1. Update preset buttons
old_buttons = '''        <div class="grid grid-cols-3 gap-1.5 text-[11px]">
          <button type="button" onclick="applyPreset('gool')" class="p-1.5 rounded-xl bg-slate-800 hover:bg-amber-500/20 hover:border-amber-500/50 border border-slate-700 text-left transition">
            <div class="font-bold text-white truncate">👑 คุณกูล</div>
            <div class="text-[9px] text-slate-400 truncate">บอสใหญ่ / CEO</div>
          </button>
          <button type="button" onclick="applyPreset('bua')" class="p-1.5 rounded-xl bg-slate-800 hover:bg-amber-500/20 hover:border-amber-500/50 border border-slate-700 text-left transition">
            <div class="font-bold text-white truncate">👑 คุณบัว</div>
            <div class="text-[9px] text-slate-400 truncate">เทียบเท่ากูล / บริหาร</div>
          </button>
          <button type="button" onclick="applyPreset('jeab')" class="p-1.5 rounded-xl bg-slate-800 hover:bg-amber-500/20 hover:border-amber-500/50 border border-slate-700 text-left transition">
            <div class="font-bold text-white truncate">📋 คุณเจี๊ยบ</div>
            <div class="text-[9px] text-slate-400 truncate">Co-Broker Lead</div>
          </button>
          <button type="button" onclick="applyPreset('lily')" class="p-1.5 rounded-xl bg-slate-800 hover:bg-amber-500/20 hover:border-amber-500/50 border border-slate-700 text-left transition">
            <div class="font-bold text-white truncate">🔑 พี่ลิลลี่</div>
            <div class="text-[9px] text-slate-400 truncate">Head of Viewing</div>
          </button>
          <button type="button" onclick="applyPreset('ton')" class="p-1.5 rounded-xl bg-slate-800 hover:bg-amber-500/20 hover:border-amber-500/50 border border-slate-700 text-left transition">
            <div class="font-bold text-white truncate">💻 คุณต้น</div>
            <div class="text-[9px] text-slate-400 truncate">Tech Architect</div>
          </button>
          <button type="button" onclick="applyPreset('custom')" class="p-1.5 rounded-xl bg-slate-800 hover:bg-amber-500/20 hover:border-amber-500/50 border border-slate-700 text-left transition">
            <div class="font-bold text-white truncate">🏢 ทีมงานอื่น</div>
            <div class="text-[9px] text-slate-400 truncate">กรอกเองอิสระ</div>
          </button>
        </div>'''

new_buttons = '''        <div class="grid grid-cols-2 sm:grid-cols-5 gap-1.5 text-[11px]">
          <button type="button" onclick="applyPreset('jeab_gool')" class="p-2 rounded-xl bg-slate-800 hover:bg-amber-500/20 hover:border-amber-500/50 border border-slate-700 text-left transition">
            <div class="font-bold text-white truncate">👑 คุณเจี๊ยบ (กูล)</div>
            <div class="text-[9px] text-amber-400 truncate">CEO & Co-Broker Lead</div>
          </button>
          <button type="button" onclick="applyPreset('bua')" class="p-2 rounded-xl bg-slate-800 hover:bg-amber-500/20 hover:border-amber-500/50 border border-slate-700 text-left transition">
            <div class="font-bold text-white truncate">👑 คุณบัว</div>
            <div class="text-[9px] text-amber-400 truncate">เทียบเท่าเจี๊ยบ / บริหาร</div>
          </button>
          <button type="button" onclick="applyPreset('lily')" class="p-2 rounded-xl bg-slate-800 hover:bg-amber-500/20 hover:border-amber-500/50 border border-slate-700 text-left transition">
            <div class="font-bold text-white truncate">🔑 พี่ลิลลี่</div>
            <div class="text-[9px] text-emerald-400 truncate">Head of Viewing ท่าข้าม</div>
          </button>
          <button type="button" onclick="applyPreset('ton')" class="p-2 rounded-xl bg-slate-800 hover:bg-amber-500/20 hover:border-amber-500/50 border border-slate-700 text-left transition">
            <div class="font-bold text-white truncate">💻 คุณต้น</div>
            <div class="text-[9px] text-rose-400 truncate">Tech Architect</div>
          </button>
          <button type="button" onclick="applyPreset('support')" class="p-2 rounded-xl bg-slate-800 hover:bg-amber-500/20 hover:border-amber-500/50 border border-slate-700 text-left transition">
            <div class="font-bold text-white truncate">🏢 ซัพพอร์ต/ธุรการ</div>
            <div class="text-[9px] text-slate-400 truncate">เจ้าหน้าที่ออฟฟิศ</div>
          </button>
        </div>'''

# Normalize newlines for robust matching
content_norm = content.replace("\r\n", "\n")
old_buttons_norm = old_buttons.replace("\r\n", "\n")
new_buttons_norm = new_buttons.replace("\r\n", "\n")

if old_buttons_norm in content_norm:
    content_norm = content_norm.replace(old_buttons_norm, new_buttons_norm)
    print("Buttons replaced successfully")
else:
    print("Warning: old_buttons not found")

# 2. Update applyPreset function
old_fn = '''    function applyPreset(who) {
      if (who === 'gool') {
        document.getElementById('inputName').value = "คุณกูล";
        document.getElementById('inputNickname').value = "กูล";
        document.getElementById('inputPhone').value = "0819999999";
        document.getElementById('selectZone').value = "สำนักงานใหญ่";
        document.getElementById('permPrice').checked = true;
        document.getElementById('permExecutive').checked = true;
        document.getElementById('permLead').checked = true;
        document.getElementById('permCatalog').checked = true;
        document.getElementById('permKeybox').checked = true;
        document.getElementById('permTech').checked = false;
      } else if (who === 'bua') {
        document.getElementById('inputName').value = "คุณบัว";
        document.getElementById('inputNickname').value = "บัว";
        document.getElementById('inputPhone').value = "0818888888";
        document.getElementById('selectZone').value = "สำนักงานใหญ่";
        document.getElementById('permPrice').checked = true;
        document.getElementById('permExecutive').checked = true;
        document.getElementById('permLead').checked = true;
        document.getElementById('permCatalog').checked = true;
        document.getElementById('permKeybox').checked = true;
        document.getElementById('permTech').checked = false;
      } else if (who === 'jeab') {
        document.getElementById('inputName').value = "คุณวารินทร์ (คุณเจี๊ยบ)";
        document.getElementById('inputNickname').value = "เจี๊ยบ";
        document.getElementById('inputPhone').value = "0817777777";
        document.getElementById('selectZone').value = "สำนักงานใหญ่";
        document.getElementById('permPrice').checked = false;
        document.getElementById('permExecutive').checked = false;
        document.getElementById('permLead').checked = true;
        document.getElementById('permCatalog').checked = true;
        document.getElementById('permKeybox').checked = true; // สำรองกุญแจ
        document.getElementById('permTech').checked = false;'''

new_fn = '''    function applyPreset(who) {
      if (who === 'jeab_gool') {
        document.getElementById('inputName').value = "คุณวารินทร์ กูลจีรัง (เจี๊ยบ)";
        document.getElementById('inputNickname').value = "เจี๊ยบ (กูล)";
        document.getElementById('inputPhone').value = "0819999999";
        document.getElementById('selectZone').value = "สำนักงานใหญ่";
        document.getElementById('permPrice').checked = true;
        document.getElementById('permExecutive').checked = true;
        document.getElementById('permLead').checked = true;
        document.getElementById('permCatalog').checked = true;
        document.getElementById('permKeybox').checked = true;
        document.getElementById('permTech').checked = false;
      } else if (who === 'bua') {
        document.getElementById('inputName').value = "คุณบัว";
        document.getElementById('inputNickname').value = "บัว";
        document.getElementById('inputPhone').value = "0818888888";
        document.getElementById('selectZone').value = "สำนักงานใหญ่";
        document.getElementById('permPrice').checked = true;
        document.getElementById('permExecutive').checked = true;
        document.getElementById('permLead').checked = true;
        document.getElementById('permCatalog').checked = true;
        document.getElementById('permKeybox').checked = true;
        document.getElementById('permTech').checked = false;'''

old_fn_norm = old_fn.replace("\r\n", "\n")
new_fn_norm = new_fn.replace("\r\n", "\n")

if old_fn_norm in content_norm:
    content_norm = content_norm.replace(old_fn_norm, new_fn_norm)
    print("Function head replaced successfully")
else:
    print("Warning: old_fn not found")

# 3. Update else / custom to support
old_support = '''      } else {
        document.getElementById('inputName').value = "";
        document.getElementById('inputNickname').value = "";
        document.getElementById('inputPhone').value = "";
        document.getElementById('permPrice').checked = false;
        document.getElementById('permExecutive').checked = false;
        document.getElementById('permLead').checked = false;
        document.getElementById('permCatalog').checked = false;
        document.getElementById('permKeybox').checked = false;
        document.getElementById('permTech').checked = false;
      }'''

new_support = '''      } else if (who === 'support') {
        document.getElementById('inputName').value = "เจ้าหน้าที่ธุรการ/ซัพพอร์ต";
        document.getElementById('inputNickname').value = "ซัพพอร์ต";
        document.getElementById('inputPhone').value = "0814444444";
        document.getElementById('selectZone').value = "สำนักงานใหญ่";
        document.getElementById('permPrice').checked = false;
        document.getElementById('permExecutive').checked = false;
        document.getElementById('permLead').checked = false;
        document.getElementById('permCatalog').checked = false;
        document.getElementById('permKeybox').checked = false;
        document.getElementById('permTech').checked = false;
      } else {
        document.getElementById('inputName').value = "";
        document.getElementById('inputNickname').value = "";
        document.getElementById('inputPhone').value = "";
        document.getElementById('permPrice').checked = false;
        document.getElementById('permExecutive').checked = false;
        document.getElementById('permLead').checked = false;
        document.getElementById('permCatalog').checked = false;
        document.getElementById('permKeybox').checked = false;
        document.getElementById('permTech').checked = false;
      }'''

old_support_norm = old_support.replace("\r\n", "\n")
new_support_norm = new_support.replace("\r\n", "\n")

if old_support_norm in content_norm:
    content_norm = content_norm.replace(old_support_norm, new_support_norm)
    print("Support branch replaced successfully")
else:
    print("Warning: old_support not found")

with open(file_path, "w", encoding="utf-8") as f:
    f.write(content_norm)

print("Finished updating agent_registration.html")
