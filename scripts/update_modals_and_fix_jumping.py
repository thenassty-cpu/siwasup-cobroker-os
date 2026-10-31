import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from overnight_r2_crawler import put_object_r2

BASE_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
INDEX_PATH = os.path.join(BASE_DIR, "index.html")
CATALOG_PATH = os.path.join(BASE_DIR, "catalog.html")
MODALS_PATH = os.path.join(BASE_DIR, "modals.js")

# ==============================================================================
# 1. FIX CSS IN index.html & catalog.html TO STOP BUTTONS FROM JUMPING / EXPANDING
# ==============================================================================
buggy_css = "html, body, button, input, select, textarea { overflow-x: hidden; max-width: 100%; width: 100%; font-family: 'Prompt', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important; -webkit-tap-highlight-color: transparent; }"
fixed_css = "html, body { overflow-x: hidden; max-width: 100%; width: 100%; font-family: 'Prompt', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; -webkit-tap-highlight-color: transparent; }\n    button, input, select, textarea { font-family: 'Prompt', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }"

for fname in ["index.html", "catalog.html"]:
    fpath = os.path.join(BASE_DIR, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        html = f.read().replace("\r\n", "\n")

    if buggy_css in html:
        html = html.replace(buggy_css, fixed_css)
        print(f"Fixed button width bug in {fname}")

    # Ensure desktop consign button has w-auto and shrink-0
    old_btn = 'class="hidden lg:flex px-4 py-2 rounded-full bg-[#C0A366] hover:bg-[#B09255] text-white text-xs font-bold items-center gap-1.5 shadow-sm transition shrink-0 cursor-pointer active:scale-95"'
    new_btn = 'class="hidden lg:flex px-4 py-2 rounded-full bg-[#C0A366] hover:bg-[#B09255] text-white text-xs font-bold items-center gap-1.5 shadow-sm transition shrink-0 cursor-pointer active:scale-95 w-auto whitespace-nowrap"'
    if old_btn in html:
        html = html.replace(old_btn, new_btn)

    with open(fpath, "w", encoding="utf-8") as f:
        f.write(html)

# ==============================================================================
# 2. UPDATE modals.js WITH OCTOBER 26 RESOLUTIONS
# ==============================================================================
with open(MODALS_PATH, "r", encoding="utf-8") as f:
    modals = f.read().replace("\r\n", "\n")

# --- 2.1 Modal เสนอราคา (ข้อ 20): เพิ่มตัวเลือก/ช่องระบุส่วนลดต่อรองได้สูงสุดถึง -50% ---
old_offer_price_block = """            <!-- ราคาที่ต้องการเสนอ (ให้ใส่ราคาอย่างอิสระ ไม่แสดงตัวเลขเพดาน 50% ให้ติดตา) -->
            <div>
              <div class="flex justify-between items-baseline mb-1">
                <label class="font-bold text-neutral-700">ราคาที่ต้องการเสนอซื้อ (บาท) <span class="text-red-500">*</span></label>
                <span id="offer-discount-percent" class="text-[11px] font-semibold text-emerald-700"></span>
              </div>
              <div class="relative">
                <input type="text" id="offer-amount-input" required placeholder="เช่น 2,850,000" 
                       class="w-full border border-neutral-200 rounded-xl p-2.5 pl-8 text-base font-extrabold text-[#8B0000] outline-none focus:ring-1 focus:ring-[#C2A460] focus:border-[#C2A460] transition font-mono bg-white"
                       oninput="formatCurrencyInput(this); updateOfferSummaryBox();">
                <span class="absolute left-3 top-3 text-neutral-400 font-bold">฿</span>
              </div>"""

new_offer_price_block = """            <!-- ราคาที่ต้องการเสนอ (พร้อมปุ่มลัดส่วนลดต่อรองได้สูงสุดถึง -50% ตามมติ 26 ต.ค. 69 ข้อ 20) -->
            <div>
              <div class="flex justify-between items-baseline mb-1">
                <label class="font-bold text-neutral-700 flex items-center gap-1.5">
                  <span>ราคาที่ต้องการเสนอซื้อ (บาท)</span>
                  <span class="text-[10px] font-semibold px-2 py-0.2 rounded-full bg-amber-50 text-amber-800 border border-amber-200">ต่อรองได้สูงสุด -50%</span>
                </label>
                <span id="offer-discount-percent" class="text-[11px] font-bold text-emerald-700"></span>
              </div>
              <div class="relative">
                <input type="text" id="offer-amount-input" required placeholder="เช่น 2,850,000" 
                       class="w-full border border-neutral-200 rounded-xl p-2.5 pl-8 text-base font-extrabold text-[#8B0000] outline-none focus:ring-1 focus:ring-[#C2A460] focus:border-[#C2A460] transition font-mono bg-white"
                       oninput="formatCurrencyInput(this); updateOfferSummaryBox();">
                <span class="absolute left-3 top-3 text-neutral-400 font-bold">฿</span>
              </div>

              <!-- ปุ่มลัดคำนวณส่วนลด 1-Click (ข้อ 20: ต่อรองสูงสุด -50%) -->
              <div class="mt-2 flex items-center gap-1.5 overflow-x-auto no-scrollbar py-0.5">
                <span class="text-[10px] font-semibold text-neutral-400 shrink-0">ปุ่มลัดส่วนลด:</span>
                <button type="button" onclick="applyQuickOfferDiscount(5)" class="px-2 py-0.5 rounded-lg border border-neutral-200 hover:border-neutral-800 bg-white text-neutral-700 text-[10.5px] font-bold transition active:scale-95 shrink-0">-5%</button>
                <button type="button" onclick="applyQuickOfferDiscount(10)" class="px-2 py-0.5 rounded-lg border border-neutral-200 hover:border-neutral-800 bg-white text-neutral-700 text-[10.5px] font-bold transition active:scale-95 shrink-0">-10%</button>
                <button type="button" onclick="applyQuickOfferDiscount(15)" class="px-2 py-0.5 rounded-lg border border-neutral-200 hover:border-neutral-800 bg-white text-neutral-700 text-[10.5px] font-bold transition active:scale-95 shrink-0">-15%</button>
                <button type="button" onclick="applyQuickOfferDiscount(20)" class="px-2 py-0.5 rounded-lg border border-neutral-200 hover:border-neutral-800 bg-white text-neutral-700 text-[10.5px] font-bold transition active:scale-95 shrink-0">-20%</button>
                <button type="button" onclick="applyQuickOfferDiscount(30)" class="px-2 py-0.5 rounded-lg border border-neutral-200 hover:border-neutral-800 bg-white text-neutral-700 text-[10.5px] font-bold transition active:scale-95 shrink-0">-30%</button>
                <button type="button" onclick="applyQuickOfferDiscount(50)" class="px-2.5 py-0.5 rounded-lg border border-rose-300 bg-rose-50 hover:bg-rose-100 text-rose-700 text-[10.5px] font-extrabold transition active:scale-95 shrink-0">-50% (เพดานสูงสุด)</button>
              </div>"""

if old_offer_price_block in modals:
    modals = modals.replace(old_offer_price_block, new_offer_price_block)
    print("Updated Offer Modal with -50% quick buttons (Meeting Point 20)")

# Add applyQuickOfferDiscount JS function if not present
if "function applyQuickOfferDiscount" not in modals:
    helper_fn = """
    function applyQuickOfferDiscount(pct) {
      if (!currentOfferProp || !currentOfferProp.price) return;
      const baseNum = parsePriceNumber(currentOfferProp.price);
      if (baseNum <= 0) return;
      const discounted = Math.round(baseNum * (1 - pct / 100));
      const inputEl = document.getElementById('offer-amount-input');
      if (inputEl) {
        inputEl.value = discounted.toLocaleString();
        formatCurrencyInput(inputEl);
        updateOfferSummaryBox();
      }
    }
"""
    modals += helper_fn
    print("Added applyQuickOfferDiscount helper function")

# --- 2.2 Modal เบิกกุญแจ (ข้อ 2): เงื่อนไขแบงก์ + ตัวเลือกขาคืน ---
old_key_sla_block = """            <div class="space-y-3">
              <div>
                <label class="block text-xs font-bold text-neutral-800 mb-1.5">เวลานัดหมายพาลูกค้าเข้าชมหน้างาน</label>"""

new_key_sla_block = """            <!-- ป้ายเงื่อนไขระยะเวลายืมกุญแจแยกตามแบงก์ (มติ 26 ต.ค. 69 ข้อ 2) -->
            <div id="npa-bank-sla-banner" class="p-2.5 rounded-xl bg-amber-50/80 border border-amber-200/90 text-amber-900 text-[11px] space-y-1">
              <div class="font-bold flex items-center gap-1.5">
                <i data-lucide="clock" class="w-3.5 h-3.5 text-amber-700 shrink-0"></i>
                <span id="npa-sla-headline">เงื่อนไขเวลายืมกุญแจตามนโยบายธนาคาร</span>
              </div>
              <ul class="text-[10.5px] space-y-0.5 text-amber-800 list-disc pl-4">
                <li><strong class="text-neutral-900">SCB:</strong> ยืมได้สูงสุด <strong>3 วันทำการ</strong> (+ มีค่ามัดจำคีย์ธนาคาร)</li>
                <li><strong class="text-neutral-900">KBANK / KTB / TTB:</strong> ยืมได้สูงสุด <strong>7 วันทำการ</strong></li>
                <li><strong class="text-neutral-900">SAM / ทรัพย์ทั่วไป:</strong> ยืมได้ตามรอบพาลูกค้าเข้าชม 3-7 วัน</li>
              </ul>
            </div>

            <!-- วิธีรับกุญแจ (มติ 26 ต.ค. 69 ข้อ 2) -->
            <div>
              <label class="block text-xs font-bold text-neutral-800 mb-1.5">วิธีรับมอบกุญแจ <span class="text-red-500">*</span></label>
              <div class="grid grid-cols-2 gap-2 text-xs">
                <label class="cursor-pointer">
                  <input type="radio" name="npa_receive_method" value="รับที่ออฟฟิศ" checked class="peer sr-only">
                  <div class="p-2.5 rounded-xl border border-neutral-200 bg-white peer-checked:border-[#C2A460] peer-checked:bg-[#FAF7F2] peer-checked:text-[#8C734B] text-center transition-all shadow-2xs">
                    <div class="font-bold">📦 มารับที่จุดดรอป</div>
                    <div class="text-[10px] text-neutral-500 mt-0.5">Drop-box ออฟฟิศท่าข้าม 12</div>
                  </div>
                </label>
                <label class="cursor-pointer">
                  <input type="radio" name="npa_receive_method" value="แมสเซนเจอร์ส่งหน้างาน" class="peer sr-only">
                  <div class="p-2.5 rounded-xl border border-neutral-200 bg-white peer-checked:border-[#C2A460] peer-checked:bg-[#FAF7F2] peer-checked:text-[#8C734B] text-center transition-all shadow-2xs">
                    <div class="font-bold">🛵 แมสเซนเจอร์</div>
                    <div class="text-[10px] text-neutral-500 mt-0.5">วิ่งส่งมอบ ณ หน้าทรัพย์</div>
                  </div>
                </label>
              </div>
            </div>

            <div class="space-y-3">
              <div>
                <label class="block text-xs font-bold text-neutral-800 mb-1.5">เวลานัดหมายพาลูกค้าเข้าชมหน้างาน</label>"""

if old_key_sla_block in modals:
    modals = modals.replace(old_key_sla_block, new_key_sla_block)
    print("Updated Key Modal with Bank Lending SLA & Receive Methods (Meeting Point 2)")

# Add Return Method options in Key Modal
old_key_policy_block = """              <div class="p-3.5 rounded-2xl bg-neutral-50 border border-neutral-200/70 text-[11px] text-neutral-600 space-y-1.5">
                <div class="font-bold text-neutral-800 flex items-center gap-1.5">
                  <i data-lucide="shield-check" class="w-3.5 h-3.5 text-neutral-700"></i>
                  <span>ข้อตกลงและนโยบายการเบิกกุญแจธนาคาร</span>
                </div>
                <ul class="list-disc pl-4 space-y-1 text-neutral-500">
                  <li>Messenger จะนำกุญแจไปส่งมอบให้ Agent ณ จุดนัดพบหน้าทรัพย์</li>
                  <li>Agent ต้องตรวจนับดอกกุญแจและเซ็นรับมอบต่อหน้า Messenger</li>
                  <li>เมื่อชมเสร็จ ต้องล็อกบ้านเรียบร้อยและส่งมอบกุญแจคืนทันที (ไม่เกิน 24 ชม.)</li>
                </ul>
              </div>"""

new_key_policy_block = """              <!-- ตัวเลือกวิธีส่งคืนกุญแจหลังเปิดบ้าน (มติ 26 ต.ค. 69 ข้อ 2) -->
              <div>
                <label class="block text-xs font-bold text-neutral-800 mb-1.5">วิธีส่งคืนกุญแจหลังเปิดบ้าน 1-2 วัน <span class="text-red-500">*</span></label>
                <div class="grid grid-cols-2 gap-2 text-xs">
                  <label class="cursor-pointer">
                    <input type="radio" name="npa_return_method" value="คืนสาขาแบงก์เอง" checked class="peer sr-only">
                    <div class="p-2 rounded-xl border border-neutral-200 bg-white peer-checked:border-[#C2A460] peer-checked:bg-[#FAF7F2] peer-checked:text-[#8C734B] text-center transition-all shadow-2xs">
                      <div class="font-bold text-[11px]">🏦 คืนสาขาแบงก์เอง</div>
                      <div class="text-[9.5px] text-neutral-500 mt-0.5">Agent เอาไปคืนสาขาเจ้าของทรัพย์</div>
                    </div>
                  </label>
                  <label class="cursor-pointer">
                    <input type="radio" name="npa_return_method" value="คืนที่ออฟฟิศให้พี่ลิลลี่" class="peer sr-only">
                    <div class="p-2 rounded-xl border border-neutral-200 bg-white peer-checked:border-[#C2A460] peer-checked:bg-[#FAF7F2] peer-checked:text-[#8C734B] text-center transition-all shadow-2xs">
                      <div class="font-bold text-[11px]">🏢 ส่งคืนออฟฟิศ</div>
                      <div class="text-[9.5px] text-neutral-500 mt-0.5">พี่ลิลลี่ดำเนินการส่งคืนแบงก์ต่อ</div>
                    </div>
                  </label>
                </div>
              </div>

              <div class="p-3.5 rounded-2xl bg-neutral-50 border border-neutral-200/70 text-[11px] text-neutral-600 space-y-1.5">
                <div class="font-bold text-neutral-800 flex items-center gap-1.5">
                  <i data-lucide="shield-check" class="w-3.5 h-3.5 text-neutral-700"></i>
                  <span>ข้อตกลงและนโยบายการเบิกกุญแจธนาคาร (มติ 26 ต.ค. 69)</span>
                </div>
                <ul class="list-disc pl-4 space-y-1 text-neutral-500 text-[10.5px]">
                  <li>Agent ยื่นขอ -> พี่ลิลลี่เช็คแบงก์และกดยืนยัน -> Agent นัดวันลูกค้า</li>
                  <li>เมื่อเปิดบ้านเสร็จ ให้แจ้งคืนกุญแจในระบบและส่งมอบคืนตามวิธีที่เลือกภายใน SLA ที่กำหนด</li>
                  <li>รักษาความสะอาดและล็อกประตูหน้าต่าง ปิดน้ำไฟทุกจุดให้เรียบร้อย 100%</li>
                </ul>
              </div>"""

if old_key_policy_block in modals:
    modals = modals.replace(old_key_policy_block, new_key_policy_block)
    print("Updated Key Modal with Return Method Options (Meeting Point 2)")

# --- 2.3 Modal ฝากขาย (ข้อ 9): อัปเดตตัวเลขส่วนแบ่ง สัญญาปิด 60% / เปิด 50% ---
old_consign_info = """        <div class="bg-amber-50 border border-amber-200 p-2.5 rounded-lg text-[11px] text-amber-900 leading-snug">
          <span class="icon-circle w-3.5 h-3.5 inline-flex mr-1 align-middle"><i data-lucide="sparkles" class="w-2 h-2 stroke-[1.5]"></i></span>
          <strong>สิทธิประโยชน์พิเศษ:</strong> หลังลงทะเบียน เจ้าหน้าที่จะติดต่อประเมินราคา และท่านสามารถเลือกรับสิทธิ์เป็น <strong>Free Agent</strong> เพื่อรับค่าคอมมิชชั่นของตัวเองเต็มๆ ได้ทันที!
        </div>"""

new_consign_info = """        <div class="bg-amber-50 border border-amber-200 p-2.5 rounded-lg text-[11px] text-amber-900 leading-snug space-y-1">
          <div class="font-bold flex items-center gap-1.5 text-amber-950">
            <span class="icon-circle w-3.5 h-3.5 inline-flex align-middle"><i data-lucide="sparkles" class="w-2 h-2 stroke-[1.5]"></i></span>
            <span>เกณฑ์การแบ่งคอมมิชชั่นตามมติ 26 ต.ค. 69 (ข้อ 9):</span>
          </div>
          <div class="grid grid-cols-2 gap-2 pt-1 text-[10.5px]">
            <div class="p-1.5 rounded-md bg-white/80 border border-amber-200">
              <strong class="text-neutral-900 block">🔒 สัญญาปิด (Exclusive)</strong>
              <span class="text-emerald-700 font-extrabold">รับคอมมิชชั่น 60%</span>
              <span class="text-neutral-500 block text-[9.5px]">การันตียอดขาย คุ้มครอง 6-12 ด.</span>
            </div>
            <div class="p-1.5 rounded-md bg-white/80 border border-amber-200">
              <strong class="text-neutral-900 block">🔓 สัญญาเปิด (Open)</strong>
              <span class="text-neutral-800 font-extrabold">รับคอมมิชชั่น 50%</span>
              <span class="text-neutral-500 block text-[9.5px]">เจ้าของร่วมขายอิสระ</span>
            </div>
          </div>
          <p class="text-[9.5px] text-neutral-500 pt-0.5 leading-tight">
            * แบ่งค่าคอมมิชชั่น 3 ฝ่ายชัดเจน: 1. Sales เจ้าของ Listing • 2. Sales ผู้แชร์/ส่งต่อลูกค้า • 3. บริษัท
          </p>
        </div>"""

if old_consign_info in modals:
    modals = modals.replace(old_consign_info, new_consign_info)
    print("Updated Consign Modal with 60%/50% Commission Rules (Meeting Point 9)")

# --- 2.4 MGM เชิญเพื่อน (ข้อ 3): อัปเดตส่วนแบ่ง 3% นาน 6 เดือน ขั้นต่ำ 500 บ. ---
old_mgm_text = """        <div class="bg-gray-50 border border-gray-200 p-2.5 rounded-xl text-xs space-y-1 text-gray-800 border-l-4 border-[#C2A460]">
          <div class="font-bold flex items-center gap-1.5 text-gray-900">
            <span class="icon-circle w-4 h-4"><i data-lucide="coins" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>สิทธิประโยชน์ผู้ชวน:</span>
          </div>
          <p class="text-[11px] leading-relaxed text-gray-600">
            1. รับ <strong class="text-[#990000]">100 แต้มสะสม</strong> เมื่อเพื่อนส่งทรัพย์ครบ 3 หลัง<br>
            2. รับ <strong class="text-[#990000]">ค่าบริหารทีม 0.5% (Overriding)</strong> จากยอดขายทุกดีลที่เพื่อนปิดได้ตลอดชีพ!
          </p>
        </div>"""

new_mgm_text = """        <div class="bg-gray-50 border border-gray-200 p-3 rounded-2xl text-xs space-y-1.5 text-gray-800 border-l-4 border-[#C2A460]">
          <div class="font-bold flex items-center gap-1.5 text-gray-900 text-[13px]">
            <span class="icon-circle w-4 h-4"><i data-lucide="coins" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>สิทธิประโยชน์ผู้แนะนำตัวแทน (มติ 26 ต.ค. 69 ข้อ 3):</span>
          </div>
          <ul class="text-[11px] leading-relaxed text-gray-700 space-y-1 pl-1">
            <li class="flex items-start gap-1.5">
              <span class="w-1.5 h-1.5 rounded-full bg-[#8B0000] shrink-0 mt-1.5"></span>
              <span>รับ <strong class="text-[#8B0000]">ส่วนแบ่ง 3% จากยอดขาย</strong> ของตัวแทนที่ตนเชิญเข้ามา (ช่วง 6 เดือนแรก / <strong>ขั้นต่ำ 500 บาท</strong> สำหรับคนเชิญทุกดีล)</span>
            </li>
            <li class="flex items-start gap-1.5">
              <span class="w-1.5 h-1.5 rounded-full bg-emerald-600 shrink-0 mt-1.5"></span>
              <span>รับ <strong class="text-emerald-700">100 แต้มสะสม</strong> ทันทีเมื่อเพื่อนเริ่มพาลูกค้าชมบ้านหรือส่งทรัพย์เข้าคลัง</span>
            </li>
            <li class="flex items-start gap-1.5">
              <span class="w-1.5 h-1.5 rounded-full bg-neutral-400 shrink-0 mt-1.5"></span>
              <span class="text-[10px] text-neutral-500">🛡️ กฎป้องกัน Tricky: มีระบบคัดกรอง ป้องกันการเชิญคนมาดองในระบบ (ตัวแทนต้อง Active พาลูกค้าชมจริง)</span>
            </li>
          </ul>
        </div>"""

if old_mgm_text in modals:
    modals = modals.replace(old_mgm_text, new_mgm_text)
    print("Updated MGM Modal with 3% 6-month & Anti-Tricky Rule (Meeting Point 3)")

with open(MODALS_PATH, "w", encoding="utf-8") as f:
    f.write(modals)

# ==============================================================================
# 3. UPLOAD ALL 3 FILES TO CLOUDFLARE R2
# ==============================================================================
for fname in ["index.html", "catalog.html", "modals.js"]:
    fpath = os.path.join(BASE_DIR, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        content = f.read()
    ctype = "application/javascript; charset=utf-8" if fname.endswith(".js") else "text/html; charset=utf-8"
    res = put_object_r2(fname, content.encode("utf-8"), ctype)
    print(f"Uploaded {fname} to Cloudflare R2 (status={res})")
