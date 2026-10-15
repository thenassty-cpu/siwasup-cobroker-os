// ==============================================================================
// 🖨️ SIWASUP CO-BROKER OS - AUTO PDF VINYL SIGN GENERATOR
// Module: vinyl_generator.js
// Generates actual scale (1:1), print-ready vinyl banner PDFs & HD images
// with Dynamic QR tracking attribution, 60-30-10 CI brand styling, and agent credentials.
// ==============================================================================

let activeVinylProperty = null;
let activeVinylPreset = '120x80'; // '120x80', '150x80', '60x90'

// Open Vinyl Generator Modal
function openVinylModal(propertyId) {
  const p = (window.allProperties || []).find(item => item.id === propertyId);
  if (!p) {
    if (typeof showToast === 'function') showToast("ไม่พบข้อมูลทรัพย์");
    return;
  }
  activeVinylProperty = p;

  // Set default values from current agent or property
  const savedRef = localStorage.getItem('siwasup_my_agent_ref') || 'AG-บัวรา';
  const headlineEl = document.getElementById('vinyl-headline');
  const phoneEl = document.getElementById('vinyl-phone');
  const contactNameEl = document.getElementById('vinyl-contact-name');
  const hookEl = document.getElementById('vinyl-hook');

  if (phoneEl) {
    phoneEl.value = (savedRef.includes('บัว') || currentMode === 'owner') ? '06-2396-5161' : '089-178-xxxx';
  }
  if (contactNameEl) {
    contactNameEl.value = savedRef.replace('AG-', '') + ' (LINE: @siwasup)';
  }
  if (hookEl) {
    hookEl.value = 'กู้ได้เต็ม 100% • ฟรีดาวน์ • ยื่นกู้ฟรี';
  }

  // Set default preset
  setVinylPreset('120x80');

  // Open modal
  const modal = document.getElementById('vinyl-modal');
  if (modal) {
    modal.classList.remove('hidden');
    if (window.lucide) { lucide.createIcons(); }
  }

  // Render canvas
  setTimeout(renderVinylCanvas, 50);
}

// Close Vinyl Generator Modal
function closeVinylModal() {
  const modal = document.getElementById('vinyl-modal');
  if (modal) {
    modal.classList.add('hidden');
  }
}

// Set Preset Dimensions
function setVinylPreset(preset) {
  activeVinylPreset = preset;
  const dimsLabel = document.getElementById('vinyl-preview-dims');

  const btn120 = document.getElementById('btn-preset-120x80');
  const btn150 = document.getElementById('btn-preset-150x80');
  const btn60 = document.getElementById('btn-preset-60x90');

  // Reset classes
  [btn120, btn150, btn60].forEach(btn => {
    if (btn) {
      btn.className = "py-1 px-1.5 rounded-lg border font-medium text-[11px] text-center transition-all bg-white text-gray-700 border-gray-200 hover:bg-gray-50";
    }
  });

  if (preset === '120x80') {
    if (btn120) btn120.className = "py-1 px-1.5 rounded-lg border font-bold text-[11px] text-center transition-all bg-[#990000] text-white border-[#990000]";
    if (dimsLabel) dimsLabel.textContent = "120 x 80 ซม. (แนวนอน 3:2)";
  } else if (preset === '150x80') {
    if (btn150) btn150.className = "py-1 px-1.5 rounded-lg border font-bold text-[11px] text-center transition-all bg-[#990000] text-white border-[#990000]";
    if (dimsLabel) dimsLabel.textContent = "150 x 80 ซม. (หน้ากว้างพิเศษ)";
  } else if (preset === '60x90') {
    if (btn60) btn60.className = "py-1 px-1.5 rounded-lg border font-bold text-[11px] text-center transition-all bg-[#990000] text-white border-[#990000]";
    if (dimsLabel) dimsLabel.textContent = "60 x 90 ซม. (แนวตั้ง 2:3 ติดเสา)";
  }

  renderVinylCanvas();
}

// Helper: Generate QR Code Image URL (Offline or Online fallback)
async function generateQrDataUrl(text) {
  if (window.QRCode && typeof window.QRCode.toDataURL === 'function') {
    try {
      return await window.QRCode.toDataURL(text, {
        width: 450,
        margin: 1,
        color: { dark: '#000000', light: '#ffffff' }
      });
    } catch (e) {
      console.warn("Local QR generation failed, using fallback", e);
    }
  }
  // Fallback to QR server
  return `https://api.qrserver.com/v1/create-qr-code/?size=450x450&margin=10&data=${encodeURIComponent(text)}`;
}

// Helper: Load Image safely into Image element
function loadImage(src) {
  return new Promise((resolve) => {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => resolve(img);
    img.onerror = () => resolve(null);
    img.src = src;
  });
}

// Render Vinyl Sign Canvas in High-Res (2400x1600 or scaled)
async function renderVinylCanvas() {
  const canvas = document.getElementById('vinyl-canvas');
  if (!canvas || !activeVinylProperty) return;

  const ctx = canvas.getContext('2d');
  const p = activeVinylProperty;

  // Form values
  const headline = (document.getElementById('vinyl-headline')?.value || 'ขายด่วน!').trim();
  const hook = (document.getElementById('vinyl-hook')?.value || 'กู้ได้เต็ม 100% • ฟรีดาวน์').trim();
  const phone = (document.getElementById('vinyl-phone')?.value || '06-2396-5161').trim();
  const contactName = (document.getElementById('vinyl-contact-name')?.value || 'บัวรา (Siwasup)').trim();
  const showPrice = document.getElementById('vinyl-show-price')?.checked ?? true;

  // Dimensions based on preset
  let W = 2400;
  let H = 1600;
  const isVertical = (activeVinylPreset === '60x90');

  if (activeVinylPreset === '150x80') {
    W = 3000;
    H = 1600;
  } else if (activeVinylPreset === '60x90') {
    W = 1600;
    H = 2400;
  }

  canvas.width = W;
  canvas.height = H;

  // 1. Background (White 60% Canvas with Heavy Architectural Frame)
  ctx.fillStyle = '#FFFFFF';
  ctx.fillRect(0, 0, W, H);

  // Outer Decorative Border (Satin Gold & Crimson Double Trim)
  ctx.lineWidth = 14;
  ctx.strokeStyle = '#C2A460'; // Satin Gold
  ctx.strokeRect(16, 16, W - 32, H - 32);

  ctx.lineWidth = 8;
  ctx.strokeStyle = '#990000'; // Brand Crimson Red
  ctx.strokeRect(34, 34, W - 68, H - 68);

  // 2. Header Banner (Red 30% Dominant Brand Identity)
  const headerHeight = isVertical ? 380 : 320;
  const headerGrad = ctx.createLinearGradient(0, 42, W, headerHeight);
  headerGrad.addColorStop(0, '#730000');
  headerGrad.addColorStop(0.5, '#990000');
  headerGrad.addColorStop(1, '#800000');

  ctx.fillStyle = headerGrad;
  ctx.fillRect(42, 42, W - 84, headerHeight);

  // Brand Crest / S Badge (Satin Gold 10%)
  ctx.fillStyle = '#C2A460';
  ctx.beginPath();
  ctx.arc(130, 42 + headerHeight / 2, 55, 0, Math.PI * 2);
  ctx.fill();

  ctx.fillStyle = '#FFFFFF';
  ctx.font = 'bold 65px "Kanit", "Tahoma", sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('S', 130, 42 + headerHeight / 2);

  // Brand Name
  ctx.textAlign = 'left';
  ctx.fillStyle = '#D4BA7A';
  ctx.font = 'bold 36px "Kanit", "Tahoma", sans-serif';
  ctx.fillText('บริษัท ศิวาทรัพย์ แอสเซท จำกัด', 210, 42 + (headerHeight / 2) - 28);

  ctx.fillStyle = '#FFFFFF';
  ctx.font = '500 24px "Kanit", "Tahoma", sans-serif';
  ctx.fillText('SIWASUP ASSET • CO-BROKER & RENOVATION NETWORK', 210, 42 + (headerHeight / 2) + 12);

  // Main Banner Headline (Huge White Text)
  ctx.textAlign = 'right';
  ctx.fillStyle = '#FFFFFF';
  ctx.font = 'bold 88px "Kanit", "Tahoma", sans-serif';
  ctx.fillText(headline, W - 90, 42 + (headerHeight / 2) + 5);

  // 3. Middle Body - Property Information
  const bodyTop = 42 + headerHeight + 60;
  ctx.textAlign = 'left';

  // Category Tag
  const categoryText = (p.category || 'บ้านพร้อมอยู่') + (p.bank_source ? ` • ทรัพย์ ${p.bank_source}` : '');
  ctx.fillStyle = '#8C6D23';
  ctx.font = 'bold 44px "Kanit", "Tahoma", sans-serif';
  ctx.fillText(categoryText, 90, bodyTop);

  // Property Title (Truncated if too long)
  ctx.fillStyle = '#111827';
  ctx.font = 'bold 74px "Kanit", "Tahoma", sans-serif';
  let titleStr = p.title || 'บ้านสวยทำเลทอง พร้อมอยู่';
  if (titleStr.length > 38 && !isVertical) {
    titleStr = titleStr.substring(0, 36) + '...';
  }
  ctx.fillText(titleStr, 90, bodyTop + 90);

  // Specs Pills (Bedrooms, Bathrooms, Area)
  const specY = bodyTop + 175;
  const specText = (p.specs || 'สเปก 3 ห้องนอน • 2 ห้องน้ำ • ที่จอดรถ') + (p.location ? ` | ทำเล: ${p.location}` : '');
  ctx.fillStyle = '#4B5563';
  ctx.font = '500 46px "Kanit", "Tahoma", sans-serif';
  ctx.fillText(specText, 90, specY);

  // Callout Box: Selling Hook (Satin Gold Pill)
  const hookY = specY + 60;
  const hookWidth = isVertical ? W - 180 : (W * 0.58);
  ctx.fillStyle = '#FEF3C7'; // Light amber
  ctx.strokeStyle = '#F59E0B';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.roundRect(90, hookY, hookWidth, 80, 20);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = '#92400E';
  ctx.font = 'bold 40px "Kanit", "Tahoma", sans-serif';
  ctx.fillText(`⭐ ${hook}`, 120, hookY + 54);

  // 4. Big Price Section
  if (showPrice) {
    const priceY = hookY + 180;
    ctx.fillStyle = '#6B7280';
    ctx.font = '500 40px "Kanit", "Tahoma", sans-serif';
    ctx.fillText('ราคาพิเศษเพียง:', 90, priceY);

    ctx.fillStyle = '#990000';
    ctx.font = '900 125px "Kanit", "Tahoma", sans-serif';
    ctx.fillText(`${p.price}`, 90, priceY + 120);

    ctx.fillStyle = '#4B5563';
    ctx.font = 'bold 42px "Kanit", "Tahoma", sans-serif';
    ctx.fillText('ผ่อนเริ่มต้นเพียงล้านละ ~3,xxx บาท/เดือน (กู้ไม่ผ่านยินดีคืนเงินมัดจำ)', 90, priceY + 180);
  }

  // 5. Dynamic QR Code Box (Right Side in Landscape / Middle in Vertical)
  const savedRef = localStorage.getItem('siwasup_my_agent_ref') || 'AG-บัวรา';
  const trackingUrl = `${window.location.origin}${window.location.pathname}?id=${encodeURIComponent(p.id)}&ref=${encodeURIComponent(savedRef)}&src=qr_sign`;

  const qrDataUrl = await generateQrDataUrl(trackingUrl);
  const qrImg = await loadImage(qrDataUrl);

  const qrSize = isVertical ? 380 : 440;
  const qrX = isVertical ? (W - qrSize) / 2 : W - qrSize - 90;
  const qrY = isVertical ? H - 760 : bodyTop + 40;

  // QR Container Card
  ctx.fillStyle = '#F9FAFB';
  ctx.strokeStyle = '#E5E7EB';
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.roundRect(qrX - 25, qrY - 25, qrSize + 50, qrSize + 130, 24);
  ctx.fill();
  ctx.stroke();

  // Draw QR Image
  if (qrImg) {
    ctx.drawImage(qrImg, qrX, qrY, qrSize, qrSize);
  }

  // QR Instruction Text
  ctx.textAlign = 'center';
  ctx.fillStyle = '#1F2937';
  ctx.font = 'bold 32px "Kanit", "Tahoma", sans-serif';
  ctx.fillText('📲 สแกนดูรูปทุกมุม & แปลนห้อง', qrX + (qrSize / 2), qrY + qrSize + 45);

  ctx.fillStyle = '#8C6D23';
  ctx.font = '500 24px "Kanit", "Tahoma", sans-serif';
  ctx.fillText(`รหัสทรัพย์: ${p.id} • ตัวแทน: ${savedRef}`, qrX + (qrSize / 2), qrY + qrSize + 82);

  // 6. Bottom Contact Footer Bar (Crimson Red / Solid Gold High Contrast)
  const footerHeight = isVertical ? 280 : 250;
  const footerY = H - footerHeight - 42;

  ctx.fillStyle = '#990000';
  ctx.fillRect(42, footerY, W - 84, footerHeight);

  // Top border line of footer
  ctx.fillStyle = '#C2A460';
  ctx.fillRect(42, footerY, W - 84, 10);

  // Contact Info Texts
  ctx.textAlign = 'left';
  ctx.fillStyle = '#FDE68A'; // Satin Light Gold
  ctx.font = 'bold 36px "Kanit", "Tahoma", sans-serif';
  ctx.fillText('📞 สนใจนัดชมบ้านจริง / ปรึกษาสินเชื่อฟรีทุกธนาคาร:', 90, footerY + 65);

  // Giant Phone Number
  ctx.fillStyle = '#FFFFFF';
  ctx.font = '900 88px "Kanit", "Tahoma", sans-serif';
  ctx.fillText(phone, 90, footerY + 160);

  // Agent Name & LINE
  ctx.fillStyle = '#FDE68A';
  ctx.font = 'bold 42px "Kanit", "Tahoma", sans-serif';
  ctx.fillText(`ผู้ดูแล: ${contactName}`, 90, footerY + 215);

  // Corner Eyelet Guide Markers (จุดเจาะตาไก่ 4 มุมสำหรับโรงพิมพ์)
  const eyeletRadius = 14;
  const eyeletOffset = 65;
  const eyelets = [
    [eyeletOffset, eyeletOffset],
    [W - eyeletOffset, eyeletOffset],
    [eyeletOffset, H - eyeletOffset],
    [W - eyeletOffset, H - eyeletOffset]
  ];
  ctx.fillStyle = '#FFFFFF';
  ctx.strokeStyle = '#374151';
  ctx.lineWidth = 3;
  eyelets.forEach(([ex, ey]) => {
    ctx.beginPath();
    ctx.arc(ex, ey, eyeletRadius, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  });
}

// Download Print-Ready PDF at Actual 1:1 Scale (pdf-lib)
async function downloadVinylPDF() {
  const canvas = document.getElementById('vinyl-canvas');
  if (!canvas || !activeVinylProperty || !window.PDFLib) {
    if (typeof showToast === 'function') showToast("กำลังเตรียมระบบ กรุณาลองใหม่อีกครั้ง");
    return;
  }

  try {
    if (typeof showToast === 'function') showToast("⏳ กำลังสร้างไฟล์ PDF ป้ายไวนิลขนาดจริง...");

    const { PDFDocument } = window.PDFLib;
    const pdfDoc = await PDFDocument.create();

    // 1 cm = 72 / 2.54 = 28.3464567 PDF Points
    const ptPerCm = 28.3464567;
    let widthCm = 120;
    let heightCm = 80;

    if (activeVinylPreset === '150x80') {
      widthCm = 150;
      heightCm = 80;
    } else if (activeVinylPreset === '60x90') {
      widthCm = 60;
      heightCm = 90;
    }

    const pageW = widthCm * ptPerCm;
    const pageH = heightCm * ptPerCm;

    const page = pdfDoc.addPage([pageW, pageH]);

    // High quality JPEG from canvas
    const imgDataUrl = canvas.toDataURL('image/jpeg', 0.95);
    const imgBytes = await fetch(imgDataUrl).then(res => res.arrayBuffer());
    const embeddedImg = await pdfDoc.embedJpg(imgBytes);

    page.drawImage(embeddedImg, {
      x: 0,
      y: 0,
      width: pageW,
      height: pageH,
    });

    const pdfBytes = await pdfDoc.save();
    const blob = new Blob([pdfBytes], { type: 'application/pdf' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `Vinyl_Sign_${activeVinylProperty.id || 'NPA'}_${widthCm}x${heightCm}cm.pdf`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    if (typeof showToast === 'function') {
      showToast(`✅ ดาวน์โหลด PDF ป้ายไวนิลขนาดจริง (${widthCm}x${heightCm} ซม.) สำเร็จ!`);
    }
  } catch (err) {
    console.error("PDF generation error:", err);
    if (typeof showToast === 'function') showToast("เกิดข้อผิดพลาดในการสร้าง PDF");
  }
}

// Download High-Resolution JPG (Direct LINE sharing to print shops)
function downloadVinylJPG() {
  const canvas = document.getElementById('vinyl-canvas');
  if (!canvas || !activeVinylProperty) return;

  let widthCm = 120;
  let heightCm = 80;
  if (activeVinylPreset === '150x80') { widthCm = 150; heightCm = 80; }
  else if (activeVinylPreset === '60x90') { widthCm = 60; heightCm = 90; }

  const link = document.createElement('a');
  link.href = canvas.toDataURL('image/jpeg', 0.95);
  link.download = `Vinyl_Sign_${activeVinylProperty.id || 'NPA'}_${widthCm}x${heightCm}cm.jpg`;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  if (typeof showToast === 'function') {
    showToast(`✅ บันทึกรูปภาพ HD ป้ายไวนิล (${widthCm}x${heightCm} ซม.) เรียบร้อย!`);
  }
}
