import os

files = [
    r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\catalog.html",
    r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os\index.html"
]

old_select = """<option value="all">ทุกธนาคาร</option>
                      <option value="Siwasup">ศิวาทรัพย์ รีโนเวท</option>
                      <option value="SAM">SAM</option>
                      <option value="SCB">SCB</option>
                      <option value="KBANK">KBank</option>
                      <option value="TTB">TTB</option>
                      <option value="KTB">KTB</option>
                      <option value="GSB">GSB</option>
                      <option value="PAMCO">PAMCO</option>"""

new_select = """<option value="all">ทุกสถาบัน / เจ้าของ</option>
                      <option value="Siwasup">ศิวาทรัพย์ รีโนเวท</option>
                      <option value="SAM">SAM</option>
                      <option value="SCB">SCB</option>
                      <option value="BAM">BAM</option>
                      <option value="GSB">GSB</option>"""

old_chips = """<button type="button" onclick="selectBankChip('all', this)" class="bank-chip active h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-[#1D1D1D] text-white shadow-sm shrink-0 inline-flex items-center">ทั้งหมด</button>
              <button type="button" onclick="selectBankChip('Siwasup', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-[#8C734B] hover:bg-[#FAF7F2] shadow-xs flex items-center gap-1 shrink-0 inline-flex items-center">
                <span>✦</span>
                <span>ศิวาทรัพย์ รีโนเวท</span>
              </button>
              <button type="button" onclick="selectBankChip('SAM', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-neutral-800 hover:bg-neutral-100 shadow-xs shrink-0 inline-flex items-center">SAM</button>
              <button type="button" onclick="selectBankChip('SCB', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-neutral-800 hover:bg-neutral-100 shadow-xs shrink-0 inline-flex items-center">SCB</button>
              <button type="button" onclick="selectBankChip('KBANK', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-neutral-800 hover:bg-neutral-100 shadow-xs shrink-0 inline-flex items-center">KBank</button>
              <button type="button" onclick="selectBankChip('TTB', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-neutral-800 hover:bg-neutral-100 shadow-xs shrink-0 inline-flex items-center">TTB</button>
              <button type="button" onclick="selectBankChip('KTB', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-neutral-800 hover:bg-neutral-100 shadow-xs shrink-0 inline-flex items-center">KTB</button>
              <button type="button" onclick="selectBankChip('GSB', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-neutral-800 hover:bg-neutral-100 shadow-xs shrink-0 inline-flex items-center">GSB</button>
              <button type="button" onclick="selectBankChip('PAMCO', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-neutral-800 hover:bg-neutral-100 shadow-xs shrink-0 inline-flex items-center">PAMCO</button>"""

new_chips = """<button type="button" onclick="selectBankChip('all', this)" class="bank-chip active h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-[#1D1D1D] text-white shadow-sm shrink-0 inline-flex items-center">ทั้งหมด</button>
              <button type="button" onclick="selectBankChip('Siwasup', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-[#8C734B] hover:bg-[#FAF7F2] shadow-xs flex items-center gap-1 shrink-0 inline-flex items-center">
                <span>✦</span>
                <span>ศิวาทรัพย์ รีโนเวท</span>
              </button>
              <button type="button" onclick="selectBankChip('SAM', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-neutral-800 hover:bg-neutral-100 shadow-xs shrink-0 inline-flex items-center">SAM</button>
              <button type="button" onclick="selectBankChip('SCB', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-neutral-800 hover:bg-neutral-100 shadow-xs shrink-0 inline-flex items-center">SCB</button>
              <button type="button" onclick="selectBankChip('BAM', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-neutral-800 hover:bg-neutral-100 shadow-xs shrink-0 inline-flex items-center">BAM</button>
              <button type="button" onclick="selectBankChip('GSB', this)" class="bank-chip h-6 sm:h-7 px-3 sm:px-3.5 rounded-full text-[11px] font-bold bg-white text-neutral-800 hover:bg-neutral-100 shadow-xs shrink-0 inline-flex items-center">GSB</button>"""

old_badges = """      if (b === 'SAM') { dotColor = "bg-indigo-400"; bankLabel = "SAM"; }
      else if (b === 'SCB') { dotColor = "bg-purple-400"; bankLabel = "SCB"; }
      else if (b === 'KBANK') { dotColor = "bg-emerald-400"; bankLabel = "KBank"; }
      else if (b === 'TTB') { dotColor = "bg-blue-400"; bankLabel = "TTB"; }
      else if (b === 'KTB') { dotColor = "bg-cyan-400"; bankLabel = "KTB"; }
      else if (b === 'GSB') { dotColor = "bg-pink-400"; bankLabel = "GSB"; }
      else if (b === 'GHB') { dotColor = "bg-amber-400"; bankLabel = "ธอส."; }
      else if (b === 'BBL') { dotColor = "bg-slate-400"; bankLabel = "กรุงเทพ"; }
      else if (b === 'PAMCO') { dotColor = "bg-teal-400"; bankLabel = "PAMCO"; }"""

new_badges = """      if (b === 'SAM') { dotColor = "bg-indigo-400"; bankLabel = "SAM"; }
      else if (b === 'SCB') { dotColor = "bg-purple-400"; bankLabel = "SCB"; }
      else if (b === 'BAM') { dotColor = "bg-amber-400"; bankLabel = "BAM"; }
      else if (b === 'GSB') { dotColor = "bg-pink-400"; bankLabel = "GSB"; }
      else if (b === 'TTB') { dotColor = "bg-blue-400"; bankLabel = "TTB"; }"""

for path in files:
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    c_norm = content.replace('\r\n', '\n')
    changed = False
    if old_select in c_norm:
        c_norm = c_norm.replace(old_select, new_select)
        changed = True
    else:
        print(f"[-] old_select not found in {os.path.basename(path)}")

    if old_chips in c_norm:
        c_norm = c_norm.replace(old_chips, new_chips)
        changed = True
    else:
        print(f"[-] old_chips not found in {os.path.basename(path)}")

    if old_badges in c_norm:
        c_norm = c_norm.replace(old_badges, new_badges)
        changed = True
    else:
        print(f"[-] old_badges not found in {os.path.basename(path)}")

    if changed:
        with open(path, 'w', encoding='utf-8', newline='\r\n') as f:
            f.write(c_norm)
        print(f"[OK] Successfully patched {os.path.basename(path)}")
