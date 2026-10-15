// ==============================================================================
// 🏢 SIWASUP CO-BROKER OS - MODAL & OVERLAY COMPONENTS
// Module: modals.js
// Extracted to optimize token usage and separate UI templates from business logic.
// All modals use .modal-backdrop, .modal-card, and .capsule-glass-20 global CSS utilities.
// ==============================================================================

(function() {
  const modalHTML = `
    <!-- Booking Modal -->
    <div id="booking-modal" class="hidden modal-backdrop">
      <div class="modal-card space-y-4">
        <div class="flex justify-between items-center border-b pb-2">
          <h3 class="font-bold text-base text-gray-800 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5"><i data-lucide="file-text" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>แจ้งหลักฐานการจอง (วางมัดจำ)</span>
          </h3>
          <button onclick="closeBookingModal()" class="text-gray-400 hover:text-gray-600 text-xl font-bold">&times;</button>
        </div>
        <div id="booking-property-info" class="bg-gray-50 p-2.5 rounded-lg text-xs space-y-1"></div>
        <form onsubmit="handleBookingSubmit(event)" class="space-y-3 text-xs">
          <div>
            <label class="block font-medium mb-1">ชื่อเอเจนต์ผู้พาจอง <span class="text-red-500">*</span></label>
            <input type="text" required placeholder="เช่น คุณกานต์ หรือ บัวไหล" class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-red-500 outline-none">
          </div>
          <div>
            <label class="block font-medium mb-1">เบอร์โทรเอเจนต์ <span class="text-red-500">*</span></label>
            <input type="tel" required placeholder="08x-xxx-xxxx" class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-red-500 outline-none">
          </div>
          <div>
            <label class="block font-medium mb-1">ชื่อลูกค้าผู้จอง <span class="text-red-500">*</span></label>
            <input type="text" required placeholder="เช่น คุณสมชาย (นัดทำสัญญา 15 ต.ค.)" class="w-full border rounded-lg p-2 focus:ring-2 focus:ring-red-500 outline-none">
          </div>
          <div>
            <label class="block font-medium mb-1">แนบสลิปเงินมัดจำ (เข้าบัญชีเจี๊ยบ) <span class="text-red-500">*</span></label>
            <input type="file" accept="image/*" class="w-full border rounded-lg p-2 bg-gray-50">
            <p class="text-[10px] text-gray-400 mt-0.5">ยอดมัดจำขั้นต่ำ 10,000 บาท</p>
          </div>
          <button type="submit" class="w-full bg-[#990000] hover:bg-red-800 text-white font-bold py-2.5 rounded-lg text-sm shadow-xs flex items-center justify-center gap-1.5">
            <span class="icon-circle w-4 h-4"><i data-lucide="check" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>ยืนยันส่งข้อมูลให้แอดมิน (เจี๊ยบ/บัว) ตรวจสอบ</span>
          </button>
        </form>
      </div>
    </div>

    <!-- Smart Share Center Modal (Omni-Channel Share) -->
    <div id="share-modal" class="hidden modal-backdrop !items-center !p-3 sm:!p-4 z-50" onclick="if(event.target === this) closeShareModal()">
      <div id="share-modal-card" class="modal-card no-scrollbar w-full max-w-md transition-all duration-300 p-4 sm:p-5 my-auto overflow-hidden">
        <div class="flex justify-between items-center border-b pb-2 mb-2.5">
          <h3 class="font-bold text-sm sm:text-base text-gray-800 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5 bg-amber-50 text-amber-700 border border-amber-200"><i data-lucide="share-2" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>Smart Share Center</span>
            <span class="text-[10px] text-amber-800 font-normal hidden sm:inline">(เลือกลิงก์โปรโมท)</span>
          </h3>
          <button onclick="closeShareModal()" class="text-gray-400 hover:text-gray-600 text-xl font-bold leading-none p-1">&times;</button>
        </div>
        
        <div id="share-prop-info" class="bg-amber-50/80 border border-amber-200/80 p-2 rounded-lg text-xs mb-2.5"></div>

        <div class="mb-2.5">
          <div class="flex justify-between items-center mb-1">
            <label class="font-medium text-[11px] text-gray-700 flex items-center gap-1.5">
              <span class="icon-circle w-3.5 h-3.5 bg-slate-100"><i data-lucide="user" class="w-2 h-2 stroke-[1.5]"></i></span>
              <span>รหัสเอเจนต์ของคุณ (ล็อกสิทธิ์ 5%):</span>
            </label>
            <span class="text-[9px] text-emerald-600 font-medium">จำค่าอัตโนมัติ 60 วัน</span>
          </div>
          <input type="text" id="agent-ref-input" value="AG-บัวรา" oninput="updateShareUrls()" 
                 class="w-full border rounded-lg py-1.5 px-2.5 text-xs font-semibold focus:ring-2 focus:ring-amber-500 outline-none bg-gray-50">
        </div>

        <!-- Adaptive Layout: Side-by-Side on Desktop/Tablet if QR open -->
        <div class="flex flex-col md:flex-row gap-3 items-stretch">
          <!-- Left Column: Channel Links -->
          <div class="flex-1 space-y-2 text-xs min-w-0">
            <div class="font-bold text-gray-700 text-[11px] flex justify-between items-center px-0.5">
              <span>กดคัดลอกลิงก์เฉพาะช่องทาง:</span>
              <span class="text-[9px] text-gray-400">เลือกลิงก์ที่ต้องการ</span>
            </div>

            <!-- Channel 1: Facebook -->
            <div class="flex items-center justify-between p-2 rounded-lg border border-blue-200 bg-blue-50/60 hover:bg-blue-50 transition-all">
              <div class="flex items-center gap-2 min-w-0">
                <span class="w-6 h-6 shrink-0 rounded-full bg-blue-600 text-white flex items-center justify-center font-bold text-xs shadow-2xs">f</span>
                <div class="truncate">
                  <div class="font-bold text-blue-950 text-xs">Facebook (Marketplace / โพสต์)</div>
                  <div class="text-[10px] text-blue-700 truncate">ดักจับ Lead จากโพสต์ & แคปชั่น FB</div>
                </div>
              </div>
              <button onclick="copyChannelLink('facebook')" class="shrink-0 ml-2 bg-blue-600 hover:bg-blue-700 text-white font-medium py-1 px-2.5 rounded text-[11px] shadow-xs active:scale-95 transition-all">
                คัดลอกลิงก์
              </button>
            </div>

            <!-- Channel 2: TikTok / Reels -->
            <div class="flex items-center justify-between p-2 rounded-lg border border-gray-300 bg-gray-50 hover:bg-gray-100/70 transition-all">
              <div class="flex items-center gap-2 min-w-0">
                <span class="w-6 h-6 shrink-0 rounded-full bg-gray-900 text-white flex items-center justify-center font-bold text-xs shadow-2xs">♪</span>
                <div class="truncate">
                  <div class="font-bold text-gray-950 text-xs">TikTok / Reels / Shorts</div>
                  <div class="text-[10px] text-gray-600 truncate">สำหรับแปะ Bio หรือใต้คอมเมนต์คลิป</div>
                </div>
              </div>
              <button onclick="copyChannelLink('tiktok')" class="shrink-0 ml-2 bg-gray-900 hover:bg-black text-white font-medium py-1 px-2.5 rounded text-[11px] shadow-xs active:scale-95 transition-all">
                คัดลอกลิงก์
              </button>
            </div>

            <!-- Channel 3: LINE -->
            <div class="flex items-center justify-between p-2 rounded-lg border border-emerald-200 bg-emerald-50/60 hover:bg-emerald-50 transition-all">
              <div class="flex items-center gap-2 min-w-0">
                <span class="w-6 h-6 shrink-0 rounded-full bg-emerald-500 text-white flex items-center justify-center font-bold text-xs shadow-2xs">L</span>
                <div class="truncate">
                  <div class="font-bold text-emerald-950 text-xs">LINE (แชตส่วนตัว / ส่งกลุ่ม)</div>
                  <div class="text-[10px] text-emerald-700 truncate">ส่งต่อให้คนรู้จัก หรือกลุ่มนักลงทุน</div>
                </div>
              </div>
              <button onclick="copyChannelLink('line')" class="shrink-0 ml-2 bg-emerald-600 hover:bg-emerald-700 text-white font-medium py-1 px-2.5 rounded text-[11px] shadow-xs active:scale-95 transition-all">
                คัดลอกลิงก์
              </button>
            </div>

            <!-- Channel 4: General Web / Forum -->
            <div class="flex items-center justify-between p-2 rounded-lg border border-gray-200 bg-gray-50/70 hover:bg-gray-100/70 transition-all">
              <div class="flex items-center gap-2 min-w-0">
                <span class="icon-circle w-6 h-6 shrink-0 bg-gray-800 text-white"><i data-lucide="globe" class="w-3.5 h-3.5 stroke-[1.5]"></i></span>
                <div class="truncate">
                  <div class="font-bold text-gray-900 text-xs">เว็บบอร์ด / LivingInsider / เว็บไซต์</div>
                  <div class="text-[10px] text-gray-500 truncate">ลิงก์กลางสำหรับโพสต์ลงเว็บไซต์ทั่วไป</div>
                </div>
              </div>
              <button onclick="copyChannelLink('web')" class="shrink-0 ml-2 bg-gray-800 hover:bg-gray-900 text-white font-medium py-1 px-2.5 rounded text-[11px] shadow-xs active:scale-95 transition-all">
                คัดลอกลิงก์
              </button>
            </div>

            <!-- Channel 5: QR Code Generator Action Row -->
            <div class="flex items-center justify-between p-2 rounded-lg border border-amber-200/90 bg-amber-50/50 hover:bg-amber-50 transition-all">
              <div class="flex items-center gap-2 min-w-0">
                <span class="icon-circle w-6 h-6 shrink-0 bg-amber-700 text-white"><i data-lucide="qr-code" class="w-3.5 h-3.5 stroke-[1.5]"></i></span>
                <div class="truncate">
                  <div class="font-bold text-amber-950 text-xs">QR Code ป้ายหน้าบ้าน / นามบัตร</div>
                  <div class="text-[10px] text-amber-700 truncate">สแกนป้ายแล้วล็อกค่าคอม 60 วัน</div>
                </div>
              </div>
              <button onclick="toggleQrView()" class="shrink-0 ml-2 bg-[#990000] hover:bg-red-800 text-white font-medium py-1 px-3 rounded text-[11px] shadow-xs flex items-center gap-1 active:scale-95 transition-all">
                <i data-lucide="scan-line" class="w-3 h-3"></i>
                <span id="qr-toggle-text">เปิดดู QR</span>
              </button>
            </div>
          </div>

          <!-- Right Column: Desktop/Tablet Side QR Panel -->
          <div id="desktop-qr-panel" style="display: none;" class="w-56 flex-col items-center justify-between p-3 bg-gradient-to-b from-amber-50/70 to-slate-50 border border-amber-200/80 rounded-xl text-center self-stretch animate-fadeIn">
            <div class="w-full">
              <div class="text-[11px] font-bold text-gray-800 mb-1.5 flex items-center justify-center gap-1">
                <i data-lucide="qr-code" class="w-3 h-3 text-amber-600"></i>
                <span>QR ป้ายหน้าบ้าน</span>
              </div>
              <div class="bg-white p-2 rounded-lg border border-gray-200 shadow-xs mb-1.5 inline-block">
                <img id="qr-image-desktop" src="" alt="QR Code" class="w-32 h-32 object-contain">
              </div>
              <div>
                <span class="inline-block text-[9px] bg-emerald-100 text-emerald-800 px-2 py-0.5 rounded-full font-medium border border-emerald-200">
                  ✓ ล็อกสิทธิ์ 60 วัน
                </span>
              </div>
            </div>
            <div class="w-full space-y-1.5 mt-2">
              <button onclick="downloadQrImage()" class="w-full bg-[#1E749C] hover:bg-[#185e7f] text-white font-medium py-1.5 px-2 rounded text-[10px] shadow-2xs flex items-center justify-center gap-1 transition-all active:scale-95">
                <i data-lucide="download" class="w-2.5 h-2.5"></i>
                <span>บันทึกรูป QR</span>
              </button>
              <button onclick="copyChannelLink('qr_sign')" class="w-full bg-white hover:bg-slate-100 text-gray-700 border border-gray-300 font-medium py-1.5 px-2 rounded text-[10px] shadow-2xs flex items-center justify-center gap-1 transition-all active:scale-95">
                <i data-lucide="copy" class="w-2.5 h-2.5"></i>
                <span>คัดลอกลิงก์ QR</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile Dedicated QR Code Sub-Modal (Popup ซ้อนขึ้นมาแบบคลีน ไม่มี Scrollbar) -->
    <div id="mobile-qr-modal" class="hidden modal-backdrop !items-center !p-4 z-[60]" onclick="if(event.target === this) closeMobileQrModal()">
      <div class="modal-card-sm no-scrollbar space-y-3 text-center bg-white border border-amber-200 shadow-2xl p-4 rounded-2xl max-w-[320px] mx-auto animate-fadeIn">
        <div class="flex justify-between items-center border-b pb-2">
          <div class="font-bold text-xs text-gray-800 flex items-center gap-1.5 text-left">
            <span class="icon-circle w-5 h-5 bg-amber-50 text-amber-700 border border-amber-200">
              <i data-lucide="qr-code" class="w-3 h-3 stroke-[1.5]"></i>
            </span>
            <span>QR Code สำหรับสแกน</span>
          </div>
          <button onclick="closeMobileQrModal()" class="text-gray-400 hover:text-gray-600 text-xl font-bold leading-none p-1">&times;</button>
        </div>

        <div id="mobile-qr-prop-info" class="text-left bg-slate-50 border border-slate-200 p-2 rounded-lg text-[11px] space-y-0.5"></div>

        <div class="bg-amber-50/60 p-3 rounded-xl border border-amber-200/70 inline-block shadow-inner my-1">
          <img id="qr-image-mobile" src="" alt="QR Code" class="w-44 h-44 object-contain bg-white p-2 rounded-lg border border-gray-200 shadow-sm mx-auto">
        </div>

        <div>
          <span class="inline-block text-[10px] bg-emerald-100 text-emerald-800 px-2.5 py-0.5 rounded-full font-medium border border-emerald-200">
            ✓ สแกนแล้วระบบล็อกสิทธิ์เอเจนต์ 60 วัน
          </span>
          <p class="text-[10px] text-gray-400 mt-1">แตะค้างที่รูปเพื่อบันทึก หรือกดปุ่มด้านล่าง</p>
        </div>

        <div class="grid grid-cols-2 gap-2 pt-1">
          <button onclick="downloadQrImage()" class="bg-[#1E749C] hover:bg-[#185e7f] text-white font-medium py-2 px-2 rounded-xl text-xs shadow-xs flex items-center justify-center gap-1 active:scale-95 transition-all">
            <i data-lucide="download" class="w-3.5 h-3.5"></i>
            <span>บันทึกรูป QR</span>
          </button>
          <button onclick="copyChannelLink('qr_sign')" class="bg-slate-100 hover:bg-slate-200 text-slate-700 font-medium py-2 px-2 rounded-xl text-xs border border-slate-200 shadow-xs flex items-center justify-center gap-1 active:scale-95 transition-all">
            <i data-lucide="copy" class="w-3.5 h-3.5"></i>
            <span>คัดลอกลิงก์</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Client Call Discount Modal (Click to Call) -->
    <div id="call-modal" class="hidden modal-backdrop !items-center !p-4">
      <div class="modal-card-sm space-y-3 text-center">
        <div class="icon-circle w-12 h-12 bg-amber-900/60 text-[#D4AF37] mx-auto">
          <i data-lucide="gift" class="w-6 h-6 stroke-[1.5]"></i>
        </div>
        <h3 class="font-bold text-base text-gray-900">รับสิทธิพิเศษสำหรับคุณ!</h3>
        <p class="text-xs text-gray-600">
          แจ้งรหัสอ้างอิงนี้กับเจ้าหน้าที่ฝ่ายขาย เพื่อรับ <strong class="text-[#990000]">สิทธิ์ฟรีค่าโอนกรรมสิทธิ์ / ส่วนลดพิเศษ</strong>
        </p>
        <div class="bg-amber-50 border-2 border-dashed border-amber-300 rounded-xl p-2.5 text-center">
          <span class="text-[11px] text-amber-800">รหัสส่วนลดของคุณ:</span>
          <div id="call-discount-code" class="text-xl font-extrabold text-amber-900 tracking-wider">SS-09</div>
        </div>
        <div class="pt-2 flex gap-2">
          <a id="btn-actual-call" href="tel:0944629796" onclick="logCallLead()" class="flex-1 bg-siwasup-gold hover:opacity-95 text-gray-950 font-bold py-2.5 rounded-xl text-xs shadow-xs text-center flex items-center justify-center gap-1.5">
            <span class="icon-circle w-4 h-4"><i data-lucide="phone" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>โทรติดต่อเจ้าหน้าที่ทันที</span>
          </a>
          <button onclick="closeCallModal()" class="px-3 bg-gray-100 hover:bg-gray-200 text-gray-700 font-medium rounded-xl text-xs border border-gray-200">
            ปิด
          </button>
        </div>
      </div>
    </div>

    <!-- Client Inquiry Modal (Appointment / Callback) -->
    <div id="inquiry-modal" class="hidden modal-backdrop !items-center !p-4">
      <div class="modal-card-sm space-y-3">
        <div class="flex justify-between items-center border-b pb-2">
          <h3 class="font-bold text-sm text-gray-900 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5"><i data-lucide="calendar" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>ขอนัดหมายเข้าชมห้องจริง / ปรึกษาสินเชื่อ</span>
          </h3>
          <button onclick="closeInquiryModal()" class="text-gray-400 hover:text-gray-600 text-xl font-bold">&times;</button>
        </div>
        <div id="inquiry-prop-info" class="bg-gray-50 p-2 rounded-lg text-xs font-medium text-gray-700"></div>
        <form onsubmit="handleInquirySubmit(event)" class="space-y-2.5 text-xs">
          <div>
            <label class="block font-medium mb-1">ชื่อของคุณ <span class="text-red-500">*</span></label>
            <input type="text" id="inquiry-name" required placeholder="เช่น คุณวิชัย" class="w-full border rounded-lg p-2 outline-none focus:ring-1 focus:ring-red-700 focus:border-red-700">
          </div>
          <div>
            <label class="block font-medium mb-1">เบอร์โทรศัพท์ติดต่อสะดวก <span class="text-red-500">*</span></label>
            <input type="tel" id="inquiry-phone" required placeholder="08x-xxx-xxxx" class="w-full border rounded-lg p-2 outline-none focus:ring-1 focus:ring-red-700 focus:border-red-700">
          </div>
          <div>
            <label class="block font-medium mb-1">วันที่สะดวกเข้าชม (โดยประมาณ)</label>
            <input type="text" id="inquiry-date" placeholder="เช่น เสาร์นี้ ช่วงบ่าย" class="w-full border rounded-lg p-2 outline-none focus:ring-1 focus:ring-red-700 focus:border-red-700">
          </div>
          <button type="submit" class="w-full bg-[#990000] hover:bg-red-800 text-white font-bold py-2.5 rounded-xl shadow-xs text-xs mt-2 flex items-center justify-center gap-1.5">
            <span class="icon-circle w-4 h-4"><i data-lucide="send" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>ยืนยันส่งข้อมูลนัดหมาย</span>
          </button>
        </form>
      </div>
    </div>

    <!-- Admin Notification Toast (Simulate 1-Click Approval) -->
    <div id="admin-toast" class="hidden fixed top-4 inset-x-4 max-w-sm mx-auto z-50 bg-gray-900 text-white p-3 rounded-xl shadow-2xl border border-gray-700 text-xs space-y-2 border-l-4 border-amber-400">
      <div class="flex items-center justify-between font-bold text-amber-300">
        <span class="flex items-center gap-1.5">
          <span class="icon-circle w-4 h-4"><i data-lucide="bell" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
          <span>แจ้งเตือนแอดมิน (เจี๊ยบ/บัว)</span>
        </span>
        <span class="text-[10px] text-gray-400">เมื่อสักครู่</span>
      </div>
      <p id="admin-toast-body" class="text-gray-200 text-[11px]"></p>
      <div class="flex gap-2 pt-1">
        <button onclick="adminApproveBooking()" class="flex-1 bg-[#D4AF37] hover:bg-[#c49f2b] text-gray-950 font-bold py-1.5 rounded text-center shadow-xs flex items-center justify-center gap-1.5">
          <span class="icon-circle w-4 h-4"><i data-lucide="check" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
          <span>กดอนุมัติการจอง (1-Click)</span>
        </button>
        <button onclick="document.getElementById('admin-toast').classList.add('hidden')" class="px-3 bg-gray-800 text-gray-300 rounded border border-gray-700">
          ปิด
        </button>
      </div>
    </div>

    <!-- 🏷️ Public Consignment / Trainee Challenge Modal (ฝากขายทรัพย์ฟรี) -->
    <div id="consign-modal" class="hidden modal-backdrop">
      <div class="modal-card space-y-3.5">
        <div class="flex justify-between items-center border-b pb-2">
          <div>
            <h3 class="font-bold text-sm text-gray-900 flex items-center gap-1.5" id="consign-modal-title">
              <span class="icon-circle w-5 h-5"><i data-lucide="building" class="w-3 h-3 stroke-[1.5]"></i></span>
              <span>ฝากขายบ้าน/คอนโด/ที่ดิน กับศิวาทรัพย์</span>
            </h3>
            <p class="text-[10px] text-emerald-600 font-semibold" id="consign-modal-sub">
              ฟรี! ไม่มีค่าแรกเข้า • เข้าถึงเครือข่ายเอเจนต์ทั่วประเทศ
            </p>
          </div>
          <button onclick="closeConsignModal()" class="text-gray-400 hover:text-gray-600 text-xl font-bold">&times;</button>
        </div>

        <div class="bg-amber-50 border border-amber-200 p-2.5 rounded-lg text-[11px] text-amber-900 leading-snug">
          <span class="icon-circle w-3.5 h-3.5 inline-flex mr-1 align-middle"><i data-lucide="sparkles" class="w-2 h-2 stroke-[1.5]"></i></span>
          <strong>สิทธิประโยชน์พิเศษ:</strong> หลังลงทะเบียน เจ้าหน้าที่จะติดต่อประเมินราคา และท่านสามารถเลือกรับสิทธิ์เป็น <strong>Free Agent</strong> เพื่อรับค่าคอมมิชชั่นของตัวเองเต็มๆ ได้ทันที!
        </div>

        <form onsubmit="handleConsignSubmit(event)" class="space-y-2.5 text-xs">
          <div>
            <label class="block font-medium mb-1">ประเภททรัพย์ <span class="text-red-500">*</span></label>
            <select id="consign-type" required class="w-full border rounded-lg p-2 bg-gray-50 outline-none focus:ring-1 focus:ring-red-700 focus:border-red-700">
              <option value="ทาวน์โฮม">ทาวน์โฮม / ทาวน์เฮ้าส์</option>
              <option value="บ้านเดี่ยว">บ้านเดี่ยว / บ้านแฝด</option>
              <option value="คอนโด">คอนโดมิเนียม</option>
              <option value="ที่ดิน">ที่ดินเปล่า</option>
              <option value="อาคารพาณิชย์">อาคารพาณิชย์ / ตึกแถว</option>
            </select>
          </div>

          <div>
            <label class="block font-medium mb-1">ชื่อโครงการ / ทำเล / ซอย / ถนน <span class="text-red-500">*</span></label>
            <input type="text" id="consign-title" required placeholder="เช่น ม.พฤกษา 12 คลองสาม ปทุมธานี" class="w-full border rounded-lg p-2 outline-none focus:ring-1 focus:ring-red-700 focus:border-red-700">
          </div>

          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block font-medium mb-1">ราคาที่ต้องการขาย (บาท) <span class="text-red-500">*</span></label>
              <input type="number" id="consign-price" required placeholder="เช่น 2500000" class="w-full border rounded-lg p-2 outline-none focus:ring-1 focus:ring-red-700 focus:border-red-700">
            </div>
            <div>
              <label class="block font-medium mb-1">ขนาดพื้นที่ (ตร.ว. / ตร.ม.)</label>
              <input type="text" id="consign-size" placeholder="เช่น 24 ตร.ว." class="w-full border rounded-lg p-2 outline-none focus:ring-1 focus:ring-red-700 focus:border-red-700">
            </div>
          </div>

          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block font-medium mb-1">ชื่อเจ้าของทรัพย์ / ผู้ส่ง <span class="text-red-500">*</span></label>
              <input type="text" id="consign-name" required placeholder="เช่น คุณสมบัติ" class="w-full border rounded-lg p-2 outline-none focus:ring-1 focus:ring-red-700 focus:border-red-700">
            </div>
            <div>
              <label class="block font-medium mb-1">เบอร์โทรศัพท์ <span class="text-red-500">*</span></label>
              <input type="tel" id="consign-phone" required placeholder="08x-xxx-xxxx" class="w-full border rounded-lg p-2 outline-none focus:ring-1 focus:ring-red-700 focus:border-red-700">
            </div>
          </div>

          <div>
            <label class="block font-medium mb-1">แนบรูปถ่ายทรัพย์ / โฉนด (ถ้ามี)</label>
            <input type="file" accept="image/*" class="w-full border rounded-lg p-1.5 bg-gray-50 text-[11px]">
            <p class="text-[10px] text-gray-400 mt-0.5">แนบรูปช่วยให้ประเมินราคาและปล่อยขายได้ไวยิ่งขึ้น</p>
          </div>

          <button type="submit" class="w-full bg-[#990000] hover:bg-red-800 text-white font-bold py-2.5 rounded-xl shadow-xs text-xs mt-2 flex items-center justify-center gap-1.5">
            <span class="icon-circle w-4 h-4"><i data-lucide="send" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>ยืนยันส่งข้อมูลฝากขาย (ฟรี)</span>
          </button>
        </form>
      </div>
    </div>

    <!-- 🤝 Member Get Member (MGM) Referral Modal -->
    <div id="mgm-modal" class="hidden modal-backdrop !items-center !p-4">
      <div class="modal-card-sm space-y-3.5">
        <div class="flex justify-between items-center border-b pb-2">
          <h3 class="font-bold text-sm text-gray-900 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5"><i data-lucide="users" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>ชวนเพื่อนมาเป็น Agent (MGM)</span>
          </h3>
          <button onclick="closeMgmModal()" class="text-gray-400 hover:text-gray-600 text-xl font-bold">&times;</button>
        </div>

        <div class="bg-gray-50 border border-gray-200 p-2.5 rounded-xl text-xs space-y-1 text-gray-800 border-l-4 border-[#D4AF37]">
          <div class="font-bold flex items-center gap-1.5 text-gray-900">
            <span class="icon-circle w-4 h-4"><i data-lucide="coins" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>สิทธิประโยชน์ผู้ชวน:</span>
          </div>
          <p class="text-[11px] leading-relaxed text-gray-600">
            1. รับ <strong class="text-[#990000]">100 แต้มสะสม</strong> เมื่อเพื่อนส่งทรัพย์ครบ 3 หลัง<br>
            2. รับ <strong class="text-[#990000]">ค่าบริหารทีม 0.5% (Overriding)</strong> จากยอดขายทุกดีลที่เพื่อนปิดได้ตลอดชีพ!
          </p>
        </div>

        <div class="space-y-1 text-xs">
          <label class="block font-medium text-gray-700">ลิงก์ชวนเพื่อนของคุณ (ฝังรหัสตัวแทน):</label>
          <div class="flex gap-1.5">
            <input type="text" id="mgm-link-input" readonly value="https://thenassty-cpu.github.io/siwasup-cobroker-os/?join_ref=AG-บัวรา" 
                   class="flex-1 bg-gray-100 border rounded-lg px-2.5 py-1.5 text-[11px] font-mono text-gray-700 outline-none">
            <button onclick="copyMgmLink()" class="bg-[#990000] hover:bg-red-800 text-white font-bold px-3 py-1.5 rounded-lg text-xs whitespace-nowrap shadow-xs flex items-center gap-1">
              <span class="icon-circle w-3.5 h-3.5"><i data-lucide="copy" class="w-2 h-2 stroke-[1.5]"></i></span>
              <span>คัดลอก</span>
            </button>
          </div>
        </div>

        <!-- MGM QR Code -->
        <div class="text-center p-2 bg-gray-50 rounded-xl border border-gray-200 space-y-1">
          <div class="text-[10px] text-gray-500 font-medium">ให้เพื่อนสแกน QR สมัครทันที</div>
          <img id="mgm-qr-img" src="https://api.qrserver.com/v1/create-qr-code/?size=140x140&data=https://thenassty-cpu.github.io/siwasup-cobroker-os/?join_ref=AG-%E0%B8%9A%E0%B8%B1%E0%B8%A7%E0%B8%A3%E0%B8%B2" 
               alt="MGM QR" class="w-32 h-32 mx-auto border p-1 bg-white rounded-lg shadow-xs">
        </div>
      </div>
    </div>

    <!-- 💬 Submit Offer / Negotiate Bank NPA Modal -->
    <div id="offer-modal" class="hidden modal-backdrop !items-center !p-4">
      <div class="modal-card-sm space-y-3">
        <div class="flex justify-between items-center border-b pb-2">
          <h3 class="font-bold text-sm text-gray-900 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5"><i data-lucide="handshake" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>ยื่นข้อเสนอซื้อ / ต่อรองราคาธนาคาร</span>
          </h3>
          <button onclick="closeOfferModal()" class="text-gray-400 hover:text-gray-600 text-xl font-bold">&times;</button>
        </div>

        <div id="offer-prop-info" class="bg-blue-50 border border-blue-200 p-2.5 rounded-xl text-xs space-y-0.5"></div>

        <form onsubmit="handleOfferSubmit(event)" class="space-y-2.5 text-xs">
          <div>
            <label class="block font-medium mb-1">ราคาที่ต้องการยื่นต่อรอง (บาท) <span class="text-red-500">*</span></label>
            <input type="number" id="offer-price" required placeholder="เช่น 2,200,000" class="w-full border rounded-lg p-2 outline-none focus:ring-2 focus:ring-blue-500 font-bold text-blue-900">
          </div>
          <div>
            <label class="block font-medium mb-1">ชื่อลูกค้าผู้เสนอซื้อ <span class="text-red-500">*</span></label>
            <input type="text" id="offer-name" required placeholder="เช่น คุณวิเชียร" class="w-full border rounded-lg p-2 outline-none focus:ring-2 focus:ring-blue-500">
          </div>
          <div>
            <label class="block font-medium mb-1">เบอร์โทรศัพท์ติดต่อ <span class="text-red-500">*</span></label>
            <input type="tel" id="offer-phone" required placeholder="08x-xxx-xxxx" class="w-full border rounded-lg p-2 outline-none focus:ring-2 focus:ring-blue-500">
          </div>
          <div>
            <label class="block font-medium mb-1">เงื่อนไขเพิ่มเติม (เช่น กู้ธนาคาร 100%, ซื้อสด)</label>
            <input type="text" id="offer-terms" placeholder="เช่น พร้อมทำสัญญาใน 7 วัน" class="w-full border rounded-lg p-2 outline-none focus:ring-2 focus:ring-blue-500">
          </div>
          <button type="submit" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2.5 rounded-xl shadow text-xs mt-2 flex items-center justify-center gap-1.5">
            <span class="icon-circle w-4 h-4"><i data-lucide="send" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>ส่งเรื่องให้แอดมิน (บัว) ดำเนินการต่อรองธนาคาร</span>
          </button>
        </form>
      </div>
    </div>

    <!-- 📥 Owner Leads Management Modal (สำหรับแอดมินบัว/เจี๊ยบ) -->
    <div id="owner-leads-modal" class="hidden modal-backdrop !items-center !p-4">
      <div class="modal-card space-y-3.5">
        <div class="flex justify-between items-center border-b pb-2">
          <h3 class="font-bold text-sm text-gray-900 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5"><i data-lucide="inbox" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>รายการทรัพย์ฝากขายใหม่ (Lead Magnet)</span>
          </h3>
          <button onclick="closeOwnerLeadsModal()" class="text-gray-400 hover:text-gray-600 text-xl font-bold">&times;</button>
        </div>

        <div id="owner-leads-container" class="space-y-2 text-xs">
          <!-- Dynamically populated -->
        </div>
      </div>
    </div>

    <!-- 💰 Edit Price Modal (สำหรับเจ้าของ/แอดมิน บัว & กูล) -->
    <div id="edit-price-modal" class="hidden modal-backdrop !items-center !p-4">
      <div class="modal-card-sm space-y-3.5">
        <div class="flex justify-between items-center border-b pb-2">
          <h3 class="font-bold text-sm text-gray-900 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5"><i data-lucide="edit-3" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>แก้ไขราคาขาย (แอดมิน บัว & กูล)</span>
          </h3>
          <button onclick="closeEditPriceModal()" class="text-gray-400 hover:text-gray-600 text-xl font-bold">&times;</button>
        </div>

        <div id="edit-price-prop-info" class="bg-gray-50 border border-gray-200 p-2.5 rounded-xl text-xs space-y-0.5"></div>

        <form onsubmit="handleEditPriceSubmit(event)" class="space-y-3 text-xs">
          <div>
            <label class="block font-medium mb-1 text-gray-700">ราคาขายใหม่ (บาท) <span class="text-red-500">*</span></label>
            <input type="number" id="new-price-input" required placeholder="เช่น 3390000" 
                   class="w-full border-2 border-gray-300 rounded-lg p-2.5 outline-none focus:border-[#990000] focus:ring-1 focus:ring-[#990000] font-extrabold text-base text-gray-900 bg-white">
            <p class="text-[10px] text-gray-400 mt-1">ระบบจะคำนวณยอดเงินค่าคอมมิชชั่นของเอเจนต์ใหม่ให้อัตโนมัติ</p>
          </div>

          <div class="flex items-center gap-2 p-2 bg-amber-50 rounded-lg border border-amber-200">
            <input type="checkbox" id="mark-hot-deal" class="rounded text-amber-600 focus:ring-amber-500">
            <label for="mark-hot-deal" class="text-[11px] font-bold text-amber-900 cursor-pointer flex items-center gap-1.5">
              <span class="icon-circle w-3.5 h-3.5"><i data-lucide="flame" class="w-2 h-2 stroke-[1.5]"></i></span>
              <span>แปะป้าย "ลดราคาพิเศษ (Hot Deal)"</span>
            </label>
          </div>

          <button type="submit" class="w-full bg-[#990000] hover:bg-red-800 text-white font-bold py-2.5 rounded-xl shadow-xs text-xs flex items-center justify-center gap-1.5">
            <span class="icon-circle w-4 h-4"><i data-lucide="save" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>บันทึกราคาใหม่ทันที</span>
          </button>
        </form>
      </div>
    </div>

    <!-- Instant Bundle Floating Action Bar (White 60% Glassmorphism + Satin Gold 10%) -->
    <div id="bundle-bar" class="hidden fixed bottom-0 inset-x-0 max-w-md mx-auto bg-white/95 backdrop-blur-md text-gray-900 p-3 z-40 shadow-xl flex items-center justify-between border-t-2 border-[#C2A460] border-x border-b border-gray-200 rounded-t-xl">
      <div>
        <div class="font-extrabold text-xs text-gray-900 flex items-center gap-1.5">
          <span class="icon-circle w-5 h-5"><i data-lucide="package" class="w-3 h-3 stroke-[1.5]"></i></span>
          <span>มัดรวมส่งลูกค้า (<span id="bundle-count" class="text-[#990000]">0</span> หลัง)</span>
        </div>
        <div class="text-[10px] text-gray-500">สร้างหน้าเว็บ VIP + แคปชั่นส่งในไลน์</div>
      </div>
      <div class="flex items-center gap-1.5">
        <button onclick="clearBundleSelection()" class="text-[11px] text-gray-400 hover:text-gray-700 px-2 py-1">
          ล้าง
        </button>
        <button onclick="openBundleModal()" class="bg-siwasup-gold hover:opacity-95 text-gray-950 font-bold py-1.5 px-3 rounded-lg text-xs shadow-xs flex items-center gap-1.5">
          <span class="icon-circle w-4 h-4"><i data-lucide="send" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
          <span>ส่งลูกค้าทันที</span>
        </button>
      </div>
    </div>

    <!-- 📦 Instant Bundle Modal (มัดรวมส่งลูกค้า) -->
    <div id="bundle-modal" class="hidden modal-backdrop">
      <div class="modal-card space-y-4">
        <div class="flex justify-between items-center border-b pb-2">
          <h3 class="font-bold text-base text-gray-800 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5"><i data-lucide="package" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>มัดรวมส่งลูกค้า (VIP Micro-Catalog)</span>
          </h3>
          <button onclick="closeBundleModal()" class="text-gray-400 hover:text-gray-600 text-xl font-bold">&times;</button>
        </div>

        <div>
          <label class="block font-medium text-xs mb-1 text-gray-700 flex items-center gap-1.5">
            <span class="icon-circle w-4 h-4"><i data-lucide="user" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>ชื่อลูกค้าผู้รับ (ใส่เพื่อเพิ่มความประทับใจ VIP):</span>
          </label>
          <input type="text" id="bundle-client-name" value="คุณวิชัย" oninput="updateBundlePreview()"
                 placeholder="เช่น คุณวิชัย, คุณสมชาย" 
                 class="w-full border rounded-lg p-2 text-xs font-semibold focus:ring-1 focus:ring-red-700 focus:border-red-700 outline-none bg-gray-50">
        </div>

        <!-- Selected Properties List Preview -->
        <div class="space-y-1.5">
          <div class="text-xs font-bold text-gray-800 flex items-center gap-1.5">
            <span class="icon-circle w-4 h-4"><i data-lucide="home" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>รายการทรัพย์ที่คัดสรร (<span id="bundle-modal-count">0</span> หลัง):</span>
          </div>
          <div id="bundle-selected-list" class="max-h-40 overflow-y-auto space-y-1.5 pr-1"></div>
        </div>

        <!-- Generated Text Preview for LINE -->
        <div class="space-y-1.5">
          <div class="text-xs font-bold text-gray-800 flex justify-between items-center">
            <span class="flex items-center gap-1.5">
              <span class="icon-circle w-4 h-4"><i data-lucide="message-square" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
              <span>ข้อความแคปชั่นพร้อมส่งใน LINE:</span>
            </span>
            <span class="text-[10px] text-gray-500 font-normal">จัดหน้าสวยงามพร้อมลิงก์</span>
          </div>
          <div class="bg-gray-100 border border-gray-300 rounded-lg p-2.5 text-[11px] text-gray-700 whitespace-pre-wrap font-sans leading-relaxed select-all" id="bundle-text-preview"></div>
        </div>

        <div class="grid grid-cols-2 gap-2 pt-1">
          <button onclick="copyBundleMessage()" class="bg-[#990000] hover:bg-red-800 text-white font-bold py-2.5 px-2 rounded-xl text-xs shadow-xs flex items-center justify-center gap-1.5">
            <span class="icon-circle w-4 h-4"><i data-lucide="copy" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>คัดลอกข้อความ</span>
          </button>
          <button onclick="sendBundleToLine()" class="bg-[#06C755] hover:bg-[#05b34c] text-white font-bold py-2.5 px-2 rounded-xl text-xs shadow-xs flex items-center justify-center gap-1.5">
            <span class="icon-circle w-4 h-4"><i data-lucide="send" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
            <span>ส่งเข้าแอป LINE</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 🖨️ Auto PDF Vinyl Sign Generator Modal -->
    <div id="vinyl-modal" class="hidden modal-backdrop">
      <div class="modal-card space-y-4 max-w-lg">
        <div class="flex justify-between items-center border-b pb-2">
          <h3 class="font-bold text-sm sm:text-base text-gray-800 flex items-center gap-1.5">
            <span class="icon-circle w-5 h-5 bg-amber-600"><i data-lucide="printer" class="w-3 h-3 stroke-[1.5]"></i></span>
            <span>Auto PDF Vinyl Sign Generator (ป้ายไวนิลหน้าบ้าน)</span>
          </h3>
          <button onclick="closeVinylModal()" class="text-gray-400 hover:text-gray-600 text-xl font-bold">&times;</button>
        </div>

        <!-- Live Vinyl Sign Preview Container -->
        <div class="space-y-1">
          <div class="flex justify-between items-center text-xs text-gray-500">
            <span class="font-medium">ตัวอย่างป้ายไวนิลจริง (Live Preview):</span>
            <span id="vinyl-preview-dims" class="text-[10px] bg-gray-100 text-gray-700 font-mono px-2 py-0.5 rounded">120 x 80 ซม. (3:2)</span>
          </div>
          <div class="bg-gray-900/5 p-2 rounded-xl border border-gray-200 flex items-center justify-center overflow-hidden">
            <canvas id="vinyl-canvas" class="w-full max-h-60 rounded shadow-sm object-contain bg-white"></canvas>
          </div>
        </div>

        <!-- Customization Controls -->
        <div class="space-y-2.5 text-xs">
          <!-- Preset Size Selection -->
          <div>
            <label class="block font-medium mb-1 text-gray-700">สัดส่วนขนาดป้าย:</label>
            <div class="grid grid-cols-3 gap-1.5">
              <button type="button" onclick="setVinylPreset('120x80')" id="btn-preset-120x80" class="py-1 px-1.5 rounded-lg border font-bold text-[11px] text-center transition-all bg-[#990000] text-white border-[#990000]">
                120 x 80 ซม.<br><span class="text-[9px] font-normal opacity-90">มาตรฐาน (3:2)</span>
              </button>
              <button type="button" onclick="setVinylPreset('150x80')" id="btn-preset-150x80" class="py-1 px-1.5 rounded-lg border font-medium text-[11px] text-center transition-all bg-white text-gray-700 border-gray-200 hover:bg-gray-50">
                150 x 80 ซม.<br><span class="text-[9px] font-normal text-gray-400">หน้ากว้าง</span>
              </button>
              <button type="button" onclick="setVinylPreset('60x90')" id="btn-preset-60x90" class="py-1 px-1.5 rounded-lg border font-medium text-[11px] text-center transition-all bg-white text-gray-700 border-gray-200 hover:bg-gray-50">
                60 x 90 ซม.<br><span class="text-[9px] font-normal text-gray-400">แนวตั้ง (2:3)</span>
              </button>
            </div>
          </div>

          <!-- Headline Banner & Selling Hook -->
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block font-medium mb-1 text-gray-700">ข้อความพาดหัว:</label>
              <select id="vinyl-headline" onchange="renderVinylCanvas()" class="w-full border rounded-lg p-1.5 text-xs bg-gray-50 font-bold text-[#990000]">
                <option value="ขายด่วน!">ขายด่วน!</option>
                <option value="ขายบ้านรีโนเวท">ขายบ้านรีโนเวท</option>
                <option value="บ้านหลุดจำนอง / NPA">บ้านหลุดจำนอง / NPA</option>
                <option value="ขาย / ให้เช่า">ขาย / ให้เช่า</option>
              </select>
            </div>
            <div>
              <label class="block font-medium mb-1 text-gray-700">ป้ายจุดเด่นการกู้:</label>
              <input type="text" id="vinyl-hook" value="กู้ได้เต็ม 100% • ฟรีดาวน์" oninput="renderVinylCanvas()" 
                     class="w-full border rounded-lg p-1.5 text-xs outline-none focus:ring-1 focus:ring-red-700">
            </div>
          </div>

          <!-- Contact Info -->
          <div class="grid grid-cols-2 gap-2">
            <div>
              <label class="block font-medium mb-1 text-gray-700">เบอร์โทรติดต่อหน้าป้าย: <span class="text-red-500">*</span></label>
              <input type="tel" id="vinyl-phone" value="06-2396-5161" oninput="renderVinylCanvas()" 
                     class="w-full border rounded-lg p-1.5 text-xs font-bold text-gray-900 outline-none focus:ring-1 focus:ring-red-700">
            </div>
            <div>
              <label class="block font-medium mb-1 text-gray-700">ชื่อตัวแทน / LINE ID:</label>
              <input type="text" id="vinyl-contact-name" value="บัวรา (Siwasup)" oninput="renderVinylCanvas()" 
                     class="w-full border rounded-lg p-1.5 text-xs outline-none focus:ring-1 focus:ring-red-700">
            </div>
          </div>

          <!-- Toggle Price and Installment -->
          <div class="flex items-center justify-between p-2 bg-gray-50 rounded-lg border border-gray-200">
            <label class="flex items-center gap-1.5 cursor-pointer text-gray-800 font-medium">
              <input type="checkbox" id="vinyl-show-price" checked onchange="renderVinylCanvas()" class="rounded text-[#990000] focus:ring-red-600">
              <span>แสดงตัวเลขราคาขายตัวใหญ่</span>
            </label>
            <span class="text-[10px] text-emerald-600 font-semibold flex items-center gap-1">
              <i data-lucide="qr-code" class="w-3 h-3 stroke-[1.5]"></i>
              ฝัง QR ล็อกสิทธิ์อัตโนมัติ
            </span>
          </div>

          <!-- Download Action Buttons -->
          <div class="grid grid-cols-2 gap-2 pt-1">
            <button type="button" onclick="downloadVinylPDF()" class="bg-[#990000] hover:bg-red-800 text-white font-bold py-2.5 px-2 rounded-xl text-xs shadow-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all">
              <span class="icon-circle w-4 h-4"><i data-lucide="download" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
              <span>โหลด PDF ส่งโรงพิมพ์</span>
            </button>
            <button type="button" onclick="downloadVinylJPG()" class="bg-gray-900 hover:bg-black text-white font-bold py-2.5 px-2 rounded-xl text-xs shadow-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all">
              <span class="icon-circle w-4 h-4"><i data-lucide="image" class="w-2.5 h-2.5 stroke-[1.5]"></i></span>
              <span>โหลดรูป HD ส่ง LINE</span>
            </button>
          </div>
          <p class="text-[10px] text-center text-gray-400">PDF ถูกตั้งค่าขนาดและสเกลจริง (1:1) สำหรับเครื่องพิมพ์อิงค์เจ็ทไวนิล</p>
        </div>
      </div>
    </div>

    <!-- Homerun-Style Clean Property Detail Modal -->
    <div id="property-detail-modal" class="hidden modal-backdrop !items-center !p-4">
      <div class="modal-card max-w-lg space-y-4 max-h-[92vh] overflow-y-auto">
        <div class="flex justify-between items-center pb-2 border-b border-slate-100">
          <div class="flex items-center gap-2">
            <span id="detail-category-badge" class="capsule-bokeh text-[11px] font-medium px-3 py-0.5">ทาวน์โฮม</span>
            <span id="detail-bank-badge"></span>
            <span id="detail-code" class="text-xs text-slate-400 font-mono">รหัส: -</span>
          </div>
          <button onclick="closePropertyDetailModal()" class="w-7 h-7 rounded-full bg-slate-100 hover:bg-slate-200 text-slate-600 flex items-center justify-center text-lg font-bold">&times;</button>
        </div>

        <!-- Detail Image Carousel / Hero -->
        <div class="relative aspect-[16/10] bg-slate-100 rounded-2xl overflow-hidden shadow-inner">
          <img id="detail-main-img" src="" alt="" class="w-full h-full object-cover">
          <div class="absolute bottom-2.5 left-2.5">
            <span id="detail-status-pill" class="bg-[#FF3838] text-white text-[11px] font-bold px-2.5 py-0.5 rounded-full shadow-sm">New</span>
          </div>
          <a id="detail-external-link" href="#" target="_blank" class="absolute bottom-2.5 right-2.5 capsule-bokeh hover:bg-slate-900/70 text-white text-[11px] font-medium px-3 py-1 flex items-center gap-1 shadow-sm">
            <i data-lucide="external-link" class="w-3 h-3"></i>
            <span>ดูหน้าเว็บเดิม</span>
          </a>
        </div>

        <!-- Title & Location -->
        <div class="space-y-1">
          <h2 id="detail-title" class="font-bold text-slate-900 text-base md:text-lg leading-snug"></h2>
          <div class="flex items-center gap-1.5 text-xs text-slate-500">
            <i data-lucide="map-pin" class="w-3.5 h-3.5 text-slate-400 shrink-0"></i>
            <span id="detail-location">กรุงเทพฯ และปริมณฑล</span>
          </div>
        </div>

        <!-- Homerun Specs Grid -->
        <div class="grid grid-cols-2 gap-2 bg-slate-50/80 p-3 rounded-2xl border border-slate-100 text-xs">
          <div class="flex items-center gap-2">
            <div class="w-7 h-7 rounded-full bg-white shadow-xs flex items-center justify-center text-slate-500">
              <i data-lucide="grid" class="w-3.5 h-3.5"></i>
            </div>
            <div>
              <div class="text-[10px] text-slate-400">เนื้อที่</div>
              <div id="detail-size" class="font-bold text-slate-800">43.9 ตร.ว.</div>
            </div>
          </div>
          <div class="flex items-center gap-2">
            <div class="w-7 h-7 rounded-full bg-white shadow-xs flex items-center justify-center text-slate-500">
              <i data-lucide="home" class="w-3.5 h-3.5"></i>
            </div>
            <div>
              <div class="text-[10px] text-slate-400">พื้นที่ใช้สอย</div>
              <div id="detail-usable" class="font-bold text-slate-800">110 ตร.ม.</div>
            </div>
          </div>
        </div>

        <!-- Description -->
        <p id="detail-desc" class="text-xs text-slate-600 leading-relaxed bg-white border border-slate-100 p-3 rounded-2xl"></p>

        <!-- Financial Breakdown (Homerun Style) -->
        <div class="bg-gradient-to-br from-slate-50 to-blue-50/30 p-3.5 rounded-2xl border border-blue-100/60 space-y-2">
          <div class="flex items-center justify-between">
            <span class="text-xs text-slate-600 flex items-center gap-1.5">
              <span class="w-4 h-4 rounded-full border border-blue-400 text-blue-600 font-bold text-[11px] inline-flex items-center justify-center leading-none select-none">฿</span>
              <span>ราคาก่อนต่อรอง</span>
            </span>
            <span id="detail-price" class="text-lg font-black text-[#1E749C] tracking-tight">฿3,410,000</span>
          </div>
          <div class="flex items-center justify-between text-xs pt-1 border-t border-slate-200/60">
            <span class="text-slate-500 flex items-center gap-1.5">
              <span class="w-4 h-4 rounded-full border border-slate-400 text-slate-600 font-bold text-[11px] inline-flex items-center justify-center leading-none select-none">฿</span>
              <span>หลักประกันเพื่อต่อรองราคา</span>
            </span>
            <span id="detail-deposit" class="font-bold text-slate-800">฿50,000</span>
          </div>
          <div class="flex items-center justify-between text-xs pt-1 border-t border-slate-200/60">
            <span class="text-slate-500 flex items-center gap-1.5">
              <i data-lucide="calculator" class="w-3.5 h-3.5 text-emerald-600"></i>
              <span>ประมาณการผ่อนต่อเดือน</span>
            </span>
            <span id="detail-installment" class="font-bold text-emerald-700">~ 12,000 บ./เดือน</span>
          </div>
        </div>

        <!-- Primary Homerun-Style Action Bar -->
        <div class="space-y-2 pt-1">
          <div class="grid grid-cols-2 gap-2">
            <button id="detail-btn-vinyl" onclick="" class="w-full bg-amber-50 hover:bg-amber-100 text-[#8C6D23] font-bold py-2.5 rounded-full border border-amber-300 text-xs shadow-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all">
              <i data-lucide="printer" class="w-4 h-4 text-amber-600"></i>
              <span>พิมพ์ป้ายไวนิล (Auto PDF)</span>
            </button>
            <button id="detail-btn-share" onclick="" class="w-full bg-[#990000] hover:bg-red-800 text-white font-bold py-2.5 rounded-full shadow-xs text-xs flex items-center justify-center gap-1.5 active:scale-95 transition-all">
              <i data-lucide="share-2" class="w-4 h-4"></i>
              <span>แชร์ล็อกสิทธิ์ (3-5%)</span>
            </button>
          </div>
          <button id="detail-btn-offer" onclick="" class="w-full bg-[#BFA267] hover:bg-[#b09257] text-white font-bold py-3 rounded-full shadow-xs flex items-center justify-center gap-2 text-sm active:scale-95 transition-all">
            <i data-lucide="handshake" class="w-4 h-4"></i>
            <span>ยื่นข้อเสนอต่อรองราคา NPA</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Copy Share Toast -->
    <div id="toast" class="fixed bottom-6 left-1/2 -translate-x-1/2 bg-gray-900 text-white text-xs px-4 py-2 rounded-full shadow-lg opacity-0 transition-opacity pointer-events-none z-50">
      ก๊อปปี้เรียบร้อย!
    </div>
  `;

  function mountModals() {
    const root = document.getElementById('modals-root');
    if (root && !root.dataset.mounted) {
      root.innerHTML = modalHTML;
      root.dataset.mounted = 'true';
      if (window.lucide) {
        lucide.createIcons();
      }
    }
  }

  // Execute immediately if root element already exists in DOM, else await DOMContentLoaded
  if (document.getElementById('modals-root')) {
    mountModals();
  } else if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mountModals);
  } else {
    mountModals();
  }
})();
