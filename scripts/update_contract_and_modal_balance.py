import os
import re

REPO_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
MODALS_PATH = os.path.join(REPO_DIR, "modals.js")
CATALOG_PATH = os.path.join(REPO_DIR, "catalog.html")
INDEX_PATH = os.path.join(REPO_DIR, "index.html")

# 1. Update modals.js Agent Action Row (Balanced Grid Layout)
with open(MODALS_PATH, "r", encoding="utf-8") as f:
    modals_code = f.read()

old_agent_row_pattern = re.compile(
    r'<!-- Agent Action Row \(สำหรับตัวแทนขาย\) -->\s*<div id="detail-agent-actions-row" class="space-y-1\.5">[\s\S]*?</div>\s*</div>\s*<!-- Admin Dedicated Operational Console',
    re.DOTALL
)

new_agent_row = """<!-- Agent Action Row (สำหรับตัวแทนขาย: Balanced 2-Column Grid) -->
            <div id="detail-agent-actions-row" class="space-y-2">
              <!-- Special Vinyl Sign Button (Visible ONLY for Exclusive/Consignment) -->
              <button id="detail-btn-vinyl" type="button" class="hidden w-full bg-[#FAF8F5] hover:bg-[#F2EDE4] text-[#8C6D23] font-bold py-2 rounded-xl border border-[#E8DFD1] text-xs shadow-2xs flex items-center justify-center gap-1.5 active:scale-95 transition-all cursor-pointer">
                <i data-lucide="printer" class="w-3.5 h-3.5 text-[#C2A460]"></i>
                <span>พิมพ์ป้ายไวนิล (เฉพาะทรัพย์ฝากขายศิวาทรัพย์)</span>
              </button>

              <!-- Balanced Primary Action Pair: Share + Key Request -->
              <div class="grid grid-cols-2 gap-2.5">
                <button id="detail-btn-share" type="button" class="w-full bg-neutral-900 hover:bg-neutral-800 text-white font-bold py-2.5 rounded-xl shadow-xs text-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all cursor-pointer">
                  <i data-lucide="share-2" class="w-3.5 h-3.5"></i>
                  <span>แชร์ล็อกสิทธิ์ (3-5%)</span>
                </button>
                <button id="detail-btn-npa-key" type="button" class="w-full bg-white hover:bg-neutral-50 text-neutral-800 font-bold py-2.5 rounded-xl border border-neutral-300 text-xs shadow-2xs flex items-center justify-center gap-1.5 active:scale-95 transition-all cursor-pointer">
                  <i data-lucide="key" class="w-3.5 h-3.5 text-neutral-600"></i>
                  <span>เบิกกุญแจ NPA (พี่ลิลลี่)</span>
                </button>
              </div>
            </div>

            <!-- Admin Dedicated Operational Console"""

modals_code = old_agent_row_pattern.sub(new_agent_row, modals_code)

with open(MODALS_PATH, "w", encoding="utf-8") as f:
    f.write(modals_code)
print("[OK] Updated modals.js balanced button layout!")

# 2. Update getCustomerContractUrl in catalog.html & index.html
def update_contract_url_generator(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    old_func_pattern = re.compile(
        r'function getCustomerContractUrl\(p\) \{[\s\S]*?\n    \}',
        re.DOTALL
    )

    new_func = """function getCustomerContractUrl(p) {
      if (!p) return 'assets/documents/siwasup_sales_contract.html';
      const cleanTitle = getDisplayTitle(p);
      const priceNum = parsePriceNumber(p.price);
      const depositNum = parsePriceNumber(calcDeposit(p.price));
      
      // Auto-resolve Agent Info from current session / profile
      let agentCode = (typeof getActiveAgentRef === 'function') ? getActiveAgentRef() : (localStorage.getItem('siwasup_agent_ref') || 'AG-09');
      let agentName = '';
      let agentPhone = '';
      if (window.SiwasupAgents && window.SiwasupAgents.find) {
        const ag = window.SiwasupAgents.find(agentCode) || window.SiwasupAgents.find('S90');
        if (ag) {
          agentName = ag.name || '';
          agentPhone = ag.phone || '';
        }
      }
      if (!agentName) {
        agentName = (agentCode === 'AG-09' || agentCode === 'S90') ? 'คุณณัฐ ระวังภัย' : `ตัวแทนรหัส ${agentCode}`;
        agentPhone = '092-456-7890';
      }

      // Auto-resolve Pinned Customer Info (if stickied)
      let buyerName = '';
      let buyerIdCard = '';
      let buyerPhone = '';
      try {
        const stick = JSON.parse(localStorage.getItem('siwasup_pinned_customer') || '{}');
        if (stick.name) buyerName = stick.name;
        if (stick.idCard) buyerIdCard = stick.idCard;
        if (stick.phone) buyerPhone = stick.phone;
      } catch(e) {}

      const witness1 = localStorage.getItem('siwasup_default_witness') || 'นางสาว บัว ศิวาทรัพย์';

      return `assets/documents/siwasup_sales_contract.html?code=${encodeURIComponent(p.id)}&title=${encodeURIComponent(cleanTitle)}&price=${priceNum}&deposit=${depositNum}&size=${encodeURIComponent(p.size || '-')}&loc=${encodeURIComponent(p.location || 'กรุงเทพฯ และปริมณฑล')}&agent=${encodeURIComponent(agentName)}&agent_code=${encodeURIComponent(agentCode)}&agent_phone=${encodeURIComponent(agentPhone)}&buyer=${encodeURIComponent(buyerName)}&idcard=${encodeURIComponent(buyerIdCard)}&phone=${encodeURIComponent(buyerPhone)}&witness1=${encodeURIComponent(witness1)}`;
    }"""

    content = old_func_pattern.sub(new_func, content)

    # Bump cache buster
    content = re.sub(r'v=20261106-\d+', 'v=20261106-0210', content)

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[OK] Updated getCustomerContractUrl in {file_path}")

update_contract_url_generator(CATALOG_PATH)
update_contract_url_generator(INDEX_PATH)

# Bump sw.js
SW_PATH = os.path.join(REPO_DIR, "sw.js")
with open(SW_PATH, "r", encoding="utf-8") as f:
    sw_c = f.read()
sw_c = re.sub(r"const CACHE_NAME = 'siwasup-os-v[^']+';", "const CACHE_NAME = 'siwasup-os-v20261106-0210';", sw_c)
with open(SW_PATH, "w", encoding="utf-8") as f:
    f.write(sw_c)
print("[OK] Bumped sw.js to v20261106-0210")
