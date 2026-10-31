import os
import sys

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = r"C:\Users\ITss-Advice\Documents\GitHub\siwasup-cobroker-os"
MODALS_PATH = os.path.join(BASE_DIR, "modals.js")

with open(MODALS_PATH, "r", encoding="utf-8") as f:
    content = f.read().replace("\r\n", "\n")

# 1. Patch #npa-key-dispatch-modal in modals.js
old_req_block = """            <!-- วิธีรับกุญแจ (มติ 26 ต.ค. 69 ข้อ 2) -->
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
                <label class="block text-xs font-bold text-neutral-800 mb-1.5">เวลานัดหมายพาลูกค้าเข้าชมหน้างาน</label>
                <div class="grid grid-cols-2 gap-2">
                  <input type="date" id="npa-date" class="w-full px-3 py-2 rounded-xl border border-neutral-200 text-xs font-medium text-neutral-800 focus:outline-none focus:border-neutral-400" />
                  <input type="time" id="npa-time" value="14:00" class="w-full px-3 py-2 rounded-xl border border-neutral-200 text-xs font-medium text-neutral-800 focus:outline-none focus:border-neutral-400" />
                </div>
                <p class="text-[11px] text-emerald-700 font-medium mt-1.5 flex items-center gap-1">
                  <i data-lucide="check-circle-2" class="w-3.5 h-3.5"></i>
                  <span>แจ้งล่วงหน้า 24 ชม. (ผ่านเกณฑ์ Fast-Track เบิกกุญแจทันที)</span>
                </p>
              </div>

              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="block text-xs font-bold text-neutral-800 mb-1">ชื่อผู้จะซื้อ (ลูกค้า)</label>
                  <input type="text" id="npa-client-name" placeholder="คุณสมชาย ใจดี" class="w-full px-3 py-2 rounded-xl border border-neutral-200 text-xs focus:outline-none focus:border-neutral-400" />
                </div>
                <div>
                  <label class="block text-xs font-bold text-neutral-800 mb-1">เบอร์โทรลูกค้า</label>
                  <input type="tel" id="npa-client-phone" placeholder="08x-xxx-xxxx" class="w-full px-3 py-2 rounded-xl border border-neutral-200 text-xs focus:outline-none focus:border-neutral-400" />
                </div>
              </div>

              <!-- ตัวเลือกวิธีส่งคืนกุญแจหลังเปิดบ้าน (มติ 26 ต.ค. 69 ข้อ 2) -->
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
              </div>
            </div>"""

new_req_block = """            <!-- วิธีรับกุญแจ (อัปเดตตามโมเดล 2 รอบเช้า-บ่าย + Smart Keybox Dual-Use) -->
            <div>
              <label class="block text-xs font-bold text-neutral-800 mb-1.5">วิธีรับมอบกุญแจ <span class="text-red-500">*</span></label>
              <div class="grid grid-cols-2 gap-2 text-xs">
                <label class="cursor-pointer">
                  <input type="radio" name="npa_receive_method" value="รับที่ออฟฟิศ / Smart Keybox" checked class="peer sr-only">
                  <div class="p-2.5 rounded-xl border border-neutral-200 bg-white peer-checked:border-[#C2A460] peer-checked:bg-[#FAF7F2] peer-checked:text-[#8C734B] text-center transition-all shadow-2xs">
                    <div class="font-bold">🏢 ออฟฟิศ (จ.-ส.) / 🔐 Keybox</div>
                    <div class="text-[10px] text-neutral-500 mt-0.5">ในเวลารับกับพี่ลิลลี่ • นอกเวลารหัส OTP</div>
                  </div>
                </label>
                <label class="cursor-pointer">
                  <input type="radio" name="npa_receive_method" value="แมสเซนเจอร์ส่งบ้านเอเจนท์/หน้างาน" class="peer sr-only">
                  <div class="p-2.5 rounded-xl border border-neutral-200 bg-white peer-checked:border-[#C2A460] peer-checked:bg-[#FAF7F2] peer-checked:text-[#8C734B] text-center transition-all shadow-2xs">
                    <div class="font-bold">🛵 แมสเซนเจอร์จัดส่ง</div>
                    <div class="text-[10px] text-neutral-500 mt-0.5">ส่งถึงบ้านเอเจนท์ หรือหน้าทรัพย์</div>
                  </div>
                </label>
              </div>
            </div>

            <div class="space-y-3">
              <div>
                <label class="block text-xs font-bold text-neutral-800 mb-1.5">เลือกรอบเปิดบ้าน (สูงสุดวันละ 2 รอบ • เผื่อเวลาชมบ้าน + ถ่ายคอนเทนต์)</label>
                <div class="grid grid-cols-2 gap-2">
                  <input type="date" id="npa-date" class="w-full px-3 py-2 rounded-xl border border-neutral-200 text-xs font-medium text-neutral-800 focus:outline-none focus:border-neutral-400" />
                  <select id="npa-time" class="w-full px-2.5 py-2 rounded-xl border border-neutral-200 text-xs font-bold text-neutral-800 focus:outline-none focus:border-neutral-400">
                    <option value="09:00">🌅 รอบเช้า (09:00 - 12:30 น.)</option>
                    <option value="13:30" selected>🌇 รอบบ่าย (13:30 - 17:00 น.)</option>
                  </select>
                </div>
                <p class="text-[11px] text-emerald-700 font-medium mt-1.5 flex items-center gap-1">
                  <i data-lucide="check-circle-2" class="w-3.5 h-3.5"></i>
                  <span>ให้เวลาเต็มอิ่มรอบละ 3.5 ชม. (พาลูกค้าชมบ้าน + ถ่ายคลิป TikTok/Reels ได้ไม่ต้องรีบ)</span>
                </p>
              </div>

              <div class="grid grid-cols-2 gap-2">
                <div>
                  <label class="block text-xs font-bold text-neutral-800 mb-1">ชื่อผู้จะซื้อ (ลูกค้า) <span class="text-red-500">*</span></label>
                  <input type="text" id="npa-client-name" placeholder="คุณสมชาย ใจดี (ต้องระบุเพื่อล็อกสิทธิ์)" class="w-full px-3 py-2 rounded-xl border border-neutral-200 text-xs focus:outline-none focus:border-neutral-400" />
                </div>
                <div>
                  <label class="block text-xs font-bold text-neutral-800 mb-1">เบอร์โทรลูกค้า <span class="text-red-500">*</span></label>
                  <input type="tel" id="npa-client-phone" placeholder="08x-xxx-xxxx" class="w-full px-3 py-2 rounded-xl border border-neutral-200 text-xs focus:outline-none focus:border-neutral-400" />
                </div>
              </div>

              <!-- ตัวเลือกวิธีส่งคืนกุญแจ / ส่งไม้ต่อเช้า-บ่าย -->
              <div>
                <label class="block text-xs font-bold text-neutral-800 mb-1.5">วิธีส่งคืนกุญแจ / ส่งไม้ต่อคิวบ่าย <span class="text-red-500">*</span></label>
                <div class="grid grid-cols-2 gap-2 text-xs">
                  <label class="cursor-pointer">
                    <input type="radio" name="npa_return_method" value="คล้องกล่อง Smart Keybox ส่งต่อคิวบ่าย" checked class="peer sr-only">
                    <div class="p-2 rounded-xl border border-neutral-200 bg-white peer-checked:border-[#C2A460] peer-checked:bg-[#FAF7F2] peer-checked:text-[#8C734B] text-center transition-all shadow-2xs">
                      <div class="font-bold text-[11px]">🔐 ส่งไม้ต่อคิวบ่าย (Relay)</div>
                      <div class="text-[9.5px] text-neutral-500 mt-0.5">เก็บใส่กล่องคล้องรั้ว + ถ่ายรูปส่งระบบ</div>
                    </div>
                  </label>
                  <label class="cursor-pointer">
                    <input type="radio" name="npa_return_method" value="คืนที่ออฟฟิศให้พี่ลิลลี่ / คืนแบงก์" class="peer sr-only">
                    <div class="p-2 rounded-xl border border-neutral-200 bg-white peer-checked:border-[#C2A460] peer-checked:bg-[#FAF7F2] peer-checked:text-[#8C734B] text-center transition-all shadow-2xs">
                      <div class="font-bold text-[11px]">🏢 คืนพี่ลิลลี่ (ท่าข้าม 12)</div>
                      <div class="text-[9.5px] text-neutral-500 mt-0.5">หิ้วพวงกุญแจ + กล่องรหัสกลับคืนออฟฟิศ</div>
                    </div>
                  </label>
                </div>
              </div>

              <div class="p-3.5 rounded-2xl bg-neutral-50 border border-neutral-200/70 text-[11px] text-neutral-600 space-y-1.5">
                <div class="font-bold text-neutral-800 flex items-center gap-1.5">
                  <i data-lucide="shield-check" class="w-3.5 h-3.5 text-neutral-700"></i>
                  <span>กฎเหล็กคิวเปิดบ้าน 2 รอบ & ป้องกันการกั๊กบ้าน (อัปเดต 31 ต.ค. 69)</span>
                </div>
                <ul class="list-disc pl-4 space-y-1 text-neutral-500 text-[10.5px]">
                  <li><strong>กรณีมีคิวเช้า-บ่ายต่อกัน:</strong> ภาคเช้าเก็บกุญแจใส่ Smart Keybox คล้องรั้วหน้าบ้านและถ่ายรูปส่งระบบ (พี่ลิลลี่คุมรหัส OTP ผ่านแอปคนเดียว 100% ภาคเช้าเปลี่ยนรหัสไม่ได้) แล้วภาคบ่ายเก็บทั้งกุญแจ+กล่องกลับคืนออฟฟิศ</li>
                  <li><strong>กฎคุ้มครองลีด:</strong> ต้องลงชื่อผู้ซื้อจริงจึงจะล็อกสิทธิ์คอมมิชชัน 60 วัน (หากอ้างว่าไปถ่ายคอนเทนต์อย่างเดียว จะไม่ล็อกสิทธิ์ผู้ซื้อ 0 วัน และต้องส่งลิงก์คลิปที่โพสต์จริงใน 48 ชม.)</li>
                </ul>
              </div>
            </div>"""

# 2. Patch #admin-appointments-modal (the exact modal in P'Ton's screenshot!)
old_app_block = """          <!-- Key Location Live Status Box -->
          <div class="bg-gradient-to-r from-neutral-900 to-neutral-800 text-white p-3.5 rounded-2xl border border-neutral-700/60 space-y-2">
            <div class="flex items-center justify-between text-xs">
              <span class="text-neutral-400 flex items-center gap-1.5 font-semibold">
                <i data-lucide="key" class="w-3.5 h-3.5 text-[#C2A460]"></i>
                <span>สถานะกุญแจปัจจุบัน (Key Custody):</span>
              </span>
              <span id="admin-app-key-status-badge" class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-400/40">
                พร้อมส่งมอบ (In Vault)
              </span>
            </div>
            <div class="text-xs text-neutral-200 leading-relaxed" id="admin-app-key-desc">
              ตำแหน่ง: <strong>ตู้เซฟสำนักงานใหญ่ ชั้น 2 (กล่อง A-14)</strong> • ดอกจริง 2 ดอก + คีย์การ์ด 1 ใบ ครบ 100%
            </div>
          </div>

          <!-- Timeline Showing Queue -->
          <div class="space-y-2.5">
            <div class="flex items-center justify-between text-xs font-bold text-neutral-800">
              <span>รายการนัดหมายเข้าชมบ้านจริง (Showing Queue):</span>
              <span class="text-[11px] text-[#8B0000] font-semibold">2 นัดหมายรอเข้าชม</span>
            </div>

            <!-- Case Item 1 -->
            <div class="bg-white border border-neutral-200/90 rounded-2xl p-3.5 space-y-2 shadow-2xs hover:border-[#C2A460]/60 transition">
              <div class="flex items-center justify-between text-xs">
                <div class="flex items-center gap-2">
                  <span class="w-6 h-6 rounded-lg bg-neutral-900 text-[#E5C985] text-[10px] font-bold flex items-center justify-center">S22</span>
                  <div>
                    <div class="font-bold text-neutral-900">คุณสมชาย พาเจริญ (Falcon Hunter)</div>
                    <div class="text-[10px] text-neutral-400">โทร 086-333-2211</div>
                  </div>
                </div>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">
                  ยืนยันแล้ว
                </span>
              </div>
              <div class="text-xs text-neutral-700 pt-1.5 border-t border-neutral-100 flex items-center justify-between">
                <span>📅 <strong>วันนี้ 14:00 น.</strong> (นัดชมห้องจริง)</span>
                <span class="text-neutral-500">ผู้จะซื้อ: คุณวิชัย นพรัตน์</span>
              </div>
              <div class="text-[11px] text-neutral-500 bg-neutral-50 p-2 rounded-xl">
                💬 <strong>บันทึกลีด:</strong> ลูกค้าทำงาน SCB สำนักงานใหญ่ สนใจกู้ร่วม 2 คน เตรียมเอกสารยื่น Pre-Approve
              </div>
            </div>

            <!-- Case Item 2 -->
            <div class="bg-white border border-neutral-200/90 rounded-2xl p-3.5 space-y-2 shadow-2xs hover:border-[#C2A460]/60 transition">
              <div class="flex items-center justify-between text-xs">
                <div class="flex items-center gap-2">
                  <span class="w-6 h-6 rounded-lg bg-[#8B0000] text-[#E5C985] text-[10px] font-bold flex items-center justify-center">SW</span>
                  <div>
                    <div class="font-bold text-neutral-900">คุณอัครวินท์ (SW-001 Master Partner)</div>
                    <div class="text-[10px] text-neutral-400">โทร 092-555-8899</div>
                  </div>
                </div>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800">
                  รอยืนยันเวลา
                </span>
              </div>
              <div class="text-xs text-neutral-700 pt-1.5 border-t border-neutral-100 flex items-center justify-between">
                <span>📅 <strong>พรุ่งนี้ 10:30 น.</strong> (นัดชมห้องจริง)</span>
                <span class="text-neutral-500">ผู้จะซื้อ: คุณพัชราภา วงศ์สุวรรณ</span>
              </div>
              <div class="text-[11px] text-neutral-500 bg-neutral-50 p-2 rounded-xl">
                💬 <strong>บันทึกลีด:</strong> ผู้ซื้อเงินสด ซื้อลงทุนปล่อยเช่า พร้อมวางเงินทำสัญญาหากห้องสภาพตรงตามรูป
              </div>
            </div>

          </div>"""

new_app_block = """          <!-- Key Location Live Status Box (อัปเดตโลจิกจริง: ออฟฟิศ จ.-ส. + Smart Keybox Dual-Use) -->
          <div class="bg-gradient-to-r from-neutral-900 to-neutral-800 text-white p-3.5 rounded-2xl border border-neutral-700/60 space-y-2">
            <div class="flex items-center justify-between text-xs">
              <span class="text-neutral-400 flex items-center gap-1.5 font-semibold">
                <i data-lucide="key" class="w-3.5 h-3.5 text-[#C2A460]"></i>
                <span>สถานะกุญแจ & โหมดส่งมอบ (Key Custody):</span>
              </span>
              <span id="admin-app-key-status-badge" class="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/20 text-emerald-300 border border-emerald-400/40">
                โหมดส่งไม้ต่อ เช้า➔บ่าย (Relay Active)
              </span>
            </div>
            <div class="text-xs text-neutral-200 leading-relaxed" id="admin-app-key-desc">
              • <strong>จ.–ส. (เวลาทำการ):</strong> รับกับพี่ลิลลี่ ณ ออฟฟิศท่าข้าม 12 หรือเรียก Messenger ส่งบ้านเอเจนท์<br>
              • <strong>นอกเวลา / ส่งไม้ต่อเช้า-บ่าย:</strong> ใช้ <strong>Smart Keybox รุ่นห่วงคล้องพกพา (TTLock OTP)</strong> พี่ลิลลี่คุมรหัสจากออฟฟิศคนเดียว 100% (ภาคเช้าเปลี่ยนรหัสหนีไม่ได้)
            </div>
          </div>

          <!-- Timeline Showing Queue (กฎเหล็ก: 1 บ้าน รับสูงสุดวันละ 2 รอบ เผื่อเวลาทำคอนเทนต์) -->
          <div class="space-y-2.5">
            <div class="flex items-center justify-between text-xs font-bold text-neutral-800">
              <span>ตารางคิวเปิดบ้าน (สูงสุด 2 รอบ/วัน • เผื่อเวลาชมบ้าน + ถ่ายคอนเทนต์):</span>
              <span class="text-[11px] text-[#8B0000] font-semibold">เต็มโควตา 2/2 รอบวันนี้</span>
            </div>

            <!-- Slot 1: Morning Slot (09:00 - 12:30) -->
            <div class="bg-white border border-neutral-200/90 rounded-2xl p-3.5 space-y-2 shadow-2xs hover:border-[#C2A460]/60 transition">
              <div class="flex items-center justify-between text-xs">
                <div class="flex items-center gap-2">
                  <span class="w-7 h-7 rounded-lg bg-neutral-900 text-[#E5C985] text-[10px] font-bold flex items-center justify-center">S90</span>
                  <div>
                    <div class="font-bold text-neutral-900 flex items-center gap-1.5">
                      <span>คุณนัญ — อนัญญา</span>
                      <span class="px-1.5 py-0.2 rounded bg-amber-100 text-amber-900 text-[9px] font-bold">⭐ Alpha Agent</span>
                    </div>
                    <div class="text-[10px] text-neutral-400">รับกุญแจหลัก + Smart Keybox พกพาจากพี่ลิลลี่</div>
                  </div>
                </div>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-100 text-emerald-800">
                  🌅 รอบเช้า (3.5 ชม.)
                </span>
              </div>
              <div class="text-xs text-neutral-700 pt-1.5 border-t border-neutral-100 flex items-center justify-between">
                <span>🕘 <strong>09:00 – 12:30 น.</strong> (ชมบ้าน + ถ่ายคลิป Reels)</span>
                <span class="text-neutral-600 font-semibold">ผู้ซื้อ: คุณวิชัย นพรัตน์ (ล็อกลีด 60 วัน)</span>
              </div>
              <div class="text-[11px] text-emerald-900 bg-emerald-50/80 border border-emerald-200/70 p-2 rounded-xl">
                🔐 <strong>การส่งไม้ต่อ (12:00 น.):</strong> ล็อกบ้าน ➔ เก็บกุญแจหลักใส่ Smart Keybox คล้องรั้วหน้าบ้าน ➔ ถ่ายรูปส่งระบบครบ ➔ <strong>Auto-Pass</strong> ส่งรหัส OTP ชุดบ่ายให้คิวที่ 2 อัตโนมัติ (พี่ลิลลี่ไม่ต้องโอเวอร์โหลดตอนพักเที่ยง)
              </div>
            </div>

            <!-- Slot 2: Afternoon Slot (13:30 - 17:00) -->
            <div class="bg-white border border-neutral-200/90 rounded-2xl p-3.5 space-y-2 shadow-2xs hover:border-[#C2A460]/60 transition">
              <div class="flex items-center justify-between text-xs">
                <div class="flex items-center gap-2">
                  <span class="w-7 h-7 rounded-lg bg-[#8B0000] text-[#E5C985] text-[10px] font-bold flex items-center justify-center">S94</span>
                  <div>
                    <div class="font-bold text-neutral-900 flex items-center gap-1.5">
                      <span>คุณหลิว — พัณณ์นิกา</span>
                      <span class="px-1.5 py-0.2 rounded bg-amber-100 text-amber-900 text-[9px] font-bold">⭐ Alpha Agent</span>
                    </div>
                    <div class="text-[10px] text-neutral-400">รับรหัส OTP ชุดบ่ายจากระบบเมื่อ S90 ส่งรูปคืนกุญแจครบ</div>
                  </div>
                </div>
                <span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-amber-100 text-amber-800">
                  🌇 รอบบ่าย (3.5 ชม.)
                </span>
              </div>
              <div class="text-xs text-neutral-700 pt-1.5 border-t border-neutral-100 flex items-center justify-between">
                <span>🕜 <strong>13:30 – 17:00 น.</strong> (ชมบ้าน + ถ่ายคอนเทนต์)</span>
                <span class="text-neutral-600 font-semibold">ผู้ซื้อ: คุณพัชราภา วงศ์สุวรรณ (ล็อกลีด 60 วัน)</span>
              </div>
              <div class="text-[11px] text-neutral-600 bg-neutral-50 border border-neutral-200/80 p-2 rounded-xl">
                🏢 <strong>จบภารกิจรอบบ่าย (17:00 น.):</strong> ล็อกบ้าน ➔ <strong>หิ้วทั้งพวงกุญแจหลัก + กล่อง Smart Keybox กลับคืนพี่ลิลลี่ที่ออฟฟิศ</strong> (ไม่ทิ้งกล่องค้างคืนหน้าบ้าน NPA ป้องกันโจร 100%)
              </div>
            </div>

            <!-- Anti-Hoarding Notice -->
            <div class="p-2.5 rounded-xl bg-rose-50/70 border border-rose-200/80 text-[10.5px] text-rose-900 leading-relaxed">
              🛡️ <strong>กฎป้องกันการกั๊กบ้าน & แอบดีล:</strong> บ้าน 1 หลังรับสูงสุด 2 รอบ/วัน (คิวที่ 3 ปัดไปวันถัดไปอัตโนมัติ) • ไม่ลงชื่อลูกค้าผู้ซื้อจริง = ไม่คุ้มครองสิทธิ์คอมมิชชัน (0 วัน) • คิวที่มีลูกค้าผู้ซื้อจริงได้สิทธิ์ชนะคิวถ่ายคอนเทนต์เสมอ
            </div>

          </div>"""

assert old_req_block in content, "old_req_block not found!"
assert old_app_block in content, "old_app_block not found!"

content = content.replace(old_req_block, new_req_block)
content = content.replace(old_app_block, new_app_block)

with open(MODALS_PATH, "w", encoding="utf-8", newline="\r\n") as f:
    f.write(content)

print("[OK] Successfully patched modals.js with 2-Slot Relay Keybox & Content-Friendly Viewing Logic!")
