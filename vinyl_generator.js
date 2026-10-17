// ==============================================================================
// 🖨️ SIWASUP CO-BROKER OS - AUTO PDF VINYL SIGN GENERATOR
// Module: vinyl_generator.js
// Generates actual scale (1:1), print-ready vinyl banner PDFs & HD images
// with Dynamic QR tracking attribution, 60-30-10 CI brand styling, and agent credentials.
// Supports sizes: 200x160 cm, 43x49 cm (Siwasup Master), 120x80, 150x80, 60x90 cm
// ==============================================================================

let activeVinylProperty = null;
let activeVinylPreset = '200x160'; // '200x160', '43x49', '120x80', '150x80', '60x90'

// Open Vinyl Generator Modal
function openVinylModal(propertyId) {
  const list = (window.allProperties && window.allProperties.length > 0)
    ? window.allProperties
    : ((typeof allProperties !== 'undefined' && allProperties.length > 0)
      ? allProperties
      : (window.SIWASUP_PROPERTIES || []));
  const p = list.find(item => String(item.id) === String(propertyId));
  if (!p) {
    if (typeof showToast === 'function') showToast('ไม่พบข้อมูลทรัพย์ #' + propertyId);
    return;
  }
  activeVinylProperty = p;

  // Set default values from current agent or property
  const savedRef = localStorage.getItem('siwasup_my_agent_ref') || 'S22';
  const vinylSearchEl = document.getElementById('vinyl-agent-search');
  if (vinylSearchEl) vinylSearchEl.value = savedRef;

  const headlineEl = document.getElementById('vinyl-headline');
  const phoneEl = document.getElementById('vinyl-phone');
  const phoneBEl = document.getElementById('vinyl-phone-b');
  const subtitleEl = document.getElementById('vinyl-subtitle');
  const contactNameEl = document.getElementById('vinyl-contact-name');
  const hookEl = document.getElementById('vinyl-hook');

  const agent = (window.SiwasupAgents && typeof window.SiwasupAgents.find === 'function')
    ? window.SiwasupAgents.find(savedRef)
    : null;

  if (headlineEl) headlineEl.value = 'ขายด่วน';
  if (phoneEl) {
    phoneEl.value = (agent && agent.phone) ? agent.phone : '094-462-9796';
  }
  if (phoneBEl) {
    phoneBEl.value = '096-129-2459';
  }
  if (subtitleEl) {
    subtitleEl.value = 'เพจ: ซื้อ ขาย บ้าน ที่ดิน ทำการตลาดฟรี by Siwasup Asset';
  }
  if (contactNameEl) {
    if (agent) {
      const lineText = agent.lineId ? agent.lineId : '@siwasup';
      contactNameEl.value = `${agent.nickname || agent.name} (LINE: ${lineText})`;
    } else {
      contactNameEl.value = savedRef.replace('AG-', '') + ' (LINE: @siwasup)';
    }
  }
  if (hookEl) {
    hookEl.value = 'กู้ได้เต็ม 100% • ฟรีดาวน์ • ยื่นกู้ฟรี';
  }

  // Set default preset to Siwasup Master 200x160
  setVinylPreset('200x160');

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

  const btn200 = document.getElementById('btn-preset-200x160');
  const btn43 = document.getElementById('btn-preset-43x49');
  const btn120 = document.getElementById('btn-preset-120x80');
  const btn150 = document.getElementById('btn-preset-150x80');
  const btn60 = document.getElementById('btn-preset-60x90');

  // Reset classes
  [btn200, btn43, btn120, btn150, btn60].forEach(btn => {
    if (btn) {
      btn.className = 'py-1.5 px-2 rounded-lg border font-medium text-[11px] text-center transition-all bg-white text-gray-700 border-gray-200 hover:bg-gray-50';
    }
  });

  if (preset === '200x160') {
    if (btn200) btn200.className = 'py-1.5 px-2 rounded-lg border font-bold text-[11px] text-center transition-all bg-[#990000] text-white border-[#990000] shadow-xs';
    if (dimsLabel) dimsLabel.textContent = '200 x 160 ซม. (ขายด่วน 5:4 สไตล์บัว)';
  } else if (preset === '43x49') {
    if (btn43) btn43.className = 'py-1.5 px-2 rounded-lg border font-bold text-[11px] text-center transition-all bg-[#990000] text-white border-[#990000] shadow-xs';
    if (dimsLabel) dimsLabel.textContent = '43 x 49 ซม. (ไซส์ S ส่งร้าน/ติดเสา)';
  } else if (preset === '120x80') {
    if (btn120) btn120.className = 'py-1 px-1.5 rounded-lg border font-bold text-[11px] text-center transition-all bg-[#990000] text-white border-[#990000]';
    if (dimsLabel) dimsLabel.textContent = '120 x 80 ซม. (แนวนอน 3:2)';
  } else if (preset === '150x80') {
    if (btn150) btn150.className = 'py-1 px-1.5 rounded-lg border font-bold text-[11px] text-center transition-all bg-[#990000] text-white border-[#990000]';
    if (dimsLabel) dimsLabel.textContent = '150 x 80 ซม. (หน้ากว้างพิเศษ)';
  } else if (preset === '60x90') {
    if (btn60) btn60.className = 'py-1 px-1.5 rounded-lg border font-bold text-[11px] text-center transition-all bg-[#990000] text-white border-[#990000]';
    if (dimsLabel) dimsLabel.textContent = '60 x 90 ซม. (แนวตั้ง 2:3 ติดเสา)';
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
      console.warn('Local QR generation failed, using fallback', e);
    }
  }
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

// Render Vinyl Sign Canvas in High-Res
async function renderVinylCanvas() {
  const canvas = document.getElementById('vinyl-canvas');
  if (!canvas || !activeVinylProperty) return;

  const ctx = canvas.getContext('2d');
  const p = activeVinylProperty;

  // Form values
  const headline = (document.getElementById('vinyl-headline')?.value || 'ขายด่วน').trim();
  const hook = (document.getElementById('vinyl-hook')?.value || 'กู้ได้เต็ม 100% • ฟรีดาวน์').trim();
  const phoneA = (document.getElementById('vinyl-phone')?.value || '094-462-9796').trim();
  const phoneB = (document.getElementById('vinyl-phone-b')?.value || '096-129-2459').trim();
  const subtitle = (document.getElementById('vinyl-subtitle')?.value || 'www.siwasup.com ซื้อ ขาย บ้าน ที่ดิน ทำการตลาดฟรี  @siwasup').trim();
  const agentInfo = (document.getElementById('vinyl-agent-info')?.value || 'ติดต่อ: คุณเอ (ตัวแทนพื้นที่โซนบางนา) LINE ID: ของตัวแทน').trim();
  const contactName = (document.getElementById('vinyl-contact-name')?.value || 'บัวรา (Siwasup)').trim();
  const showPrice = document.getElementById('vinyl-show-price')?.checked ?? true;

  const savedRef = (document.getElementById('vinyl-agent-search')?.value || 'S22').trim();
  const targetUrl = `https://thenassty-cpu.github.io/siwasup-cobroker-os/?ref=${encodeURIComponent(savedRef)}&id=${encodeURIComponent(p.id)}&ch=vinyl`;
  
  // 🔤 Guarantee RSU Web Font is loaded in browser before Canvas drawing
  if (document.fonts && typeof document.fonts.load === 'function') {
    try {
      await Promise.all([
        document.fonts.load('bold 100px RSU'),
        document.fonts.load('normal 40px RSU')
      ]);
    } catch (e) {
      console.warn('RSU font preloading:', e);
    }
  }

  const qrDataUrl = await generateQrDataUrl(targetUrl);
  const qrImg = await loadImage(qrDataUrl);
  const logoImg = await loadImage('assets/siwasup_logo.png');

  // Branch by Preset Style
  if (activeVinylPreset === '200x160') {
    renderSiwasupMaster200x160(ctx, canvas, p, headline, phoneA, phoneB, subtitle, agentInfo, savedRef, qrImg, logoImg);
  } else if (activeVinylPreset === '43x49') {
    renderSiwasupMaster43x49(ctx, canvas, p, headline, phoneA, phoneB, subtitle, savedRef, qrImg, logoImg);
  } else {
    renderClassicPropertyVinyl(ctx, canvas, p, headline, hook, phoneA, contactName, showPrice, savedRef, qrImg);
  }
}

// ------------------------------------------------------------------------------
// STYLE 1: SIWASUP MASTER 200x160 CM (ขายด่วน สไตล์ Ads200x160.ait พร้อม Bar สีทอง)
// ------------------------------------------------------------------------------
function renderSiwasupMaster200x160(ctx, canvas, p, headline, phoneA, phoneB, subtitle, agentInfo, savedRef, qrImg, logoImg) {
  const W = 2000;
  const H = 1600;
  canvas.width = W;
  canvas.height = H;

  // Background Canvas
  ctx.fillStyle = '#FFFFFF';
  ctx.fillRect(0, 0, W, H);

  // Outer safety guide
  ctx.lineWidth = 4;
  ctx.strokeStyle = '#F3F4F6';
  ctx.strokeRect(20, 20, W - 40, H - 40);

  // 1. Red Header Block 'Horsale' (Height = 580px)
  const headerHeight = 580;
  ctx.fillStyle = '#C8102E';
  ctx.fillRect(30, 30, W - 60, headerHeight);

  // Big Bold White Headline 'ขายด่วน' (RSU Bold style)
  ctx.fillStyle = '#FFFFFF';
  ctx.font = 'bold 280px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(headline, W / 2, 30 + headerHeight / 2);

  // ⭐ 1.1 Signature Satin Gold Accent Bar (แถบสีทองคั่นใต้บล็อกแดงตาม Ads200x160.ait)
  const goldBarH = 26;
  const goldBarY = 30 + headerHeight;
  ctx.fillStyle = '#C2A460'; // Satin Gold CI
  ctx.fillRect(30, goldBarY, W - 60, goldBarH);

  // 2. Middle Body: Job_Discription + Huge Phone Numbers + Ticker_AgentInfo
  const bodyTop = goldBarY + goldBarH;

  // Job_Discription: Red Web & LINE text
  ctx.fillStyle = '#C8102E';
  ctx.font = 'bold 40px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'top';
  ctx.fillText(subtitle, W / 2, bodyTop + 24);

  // Phone Number A (Ticker_NumberA)
  ctx.fillStyle = '#111827';
  ctx.font = 'bold 190px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(phoneA, W / 2, bodyTop + 185);

  // Phone Number B (Ticker_NumberB)
  ctx.fillText(phoneB, W / 2, bodyTop + 365);

  // Ticker_AgentInfo: Red text line below phone numbers
  ctx.fillStyle = '#C8102E';
  ctx.font = 'bold 44px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(agentInfo, W / 2, bodyTop + 490);

  // 3. Bottom Footer Bar: Siwasup Logo + Services + QR Code
  const footerTop = 1270;

  // Siwasup Logo on the left
  if (logoImg) {
    ctx.drawImage(logoImg, 90, footerTop + 10, 230, 185);
  } else {
    // Canvas Fallback Logo
    ctx.fillStyle = '#C8102E';
    ctx.beginPath();
    ctx.arc(170, footerTop + 90, 60, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#FFFFFF';
    ctx.font = 'bold 70px "Kanit", sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('S', 170, footerTop + 90);
  }

  // Footer Center: Services & Catchphrase
  ctx.textAlign = 'left';
  ctx.textBaseline = 'top';
  ctx.fillStyle = '#C8102E';
  ctx.font = 'bold 64px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif';
  ctx.fillText('รับฝากขายบ้าน-ที่ดิน', 350, footerTop + 20);

  ctx.fillStyle = '#374151';
  ctx.font = 'bold 36px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif';
  ctx.fillText('ให้เราช่วยขาย ง่ายกว่า โฆษณาฟรี มีบริการจัดสินเชื่อ', 350, footerTop + 95);

  ctx.fillStyle = '#9CA3AF';
  ctx.font = '500 24px "Kanit", "Tahoma", sans-serif';
  ctx.fillText(`รหัสตัวแทน: ${savedRef} • บริษัท ศิวาทรัพย์ แอสเซท จำกัด`, 350, footerTop + 148);

  // Footer Right: Dynamic QR Code
  if (qrImg) {
    const qrSize = 220;
    const qrX = W - qrSize - 90;
    const qrY = footerTop;

    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(qrX - 6, qrY - 6, qrSize + 12, qrSize + 12);
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#E5E7EB';
    ctx.strokeRect(qrX - 6, qrY - 6, qrSize + 12, qrSize + 12);
    ctx.drawImage(qrImg, qrX, qrY, qrSize, qrSize);
  }

  // 4 Corner Eyelet Markers
  drawEyelets(ctx, W, H, 55, 14);
}

// ------------------------------------------------------------------------------
// STYLE 2: SIWASUP MASTER 43x49 CM (ป้ายไซส์ S ส่งร้าน/ติดเสาไฟฟ้า)
// ------------------------------------------------------------------------------
function renderSiwasupMaster43x49(ctx, canvas, p, headline, phoneA, phoneB, subtitle, savedRef, qrImg, logoImg) {
  const W = 1720;
  const H = 1960;
  canvas.width = W;
  canvas.height = H;

  // Canvas Background
  ctx.fillStyle = '#FFFFFF';
  ctx.fillRect(0, 0, W, H);

  // Top-Left: Siwasup Logo
  if (logoImg) {
    ctx.drawImage(logoImg, 70, 70, 380, 305);
  }

  // Top-Right: Solid Red Header Block 'ขาย'
  const redBoxX = 540;
  const redBoxW = W - redBoxX;
  const redBoxH = 460;
  ctx.fillStyle = '#C8102E';
  ctx.fillRect(redBoxX, 0, redBoxW, redBoxH);

  // White text 'ขาย'
  ctx.fillStyle = '#FFFFFF';
  ctx.font = 'bold 310px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('ขาย', redBoxX + redBoxW / 2, redBoxH / 2 - 25);

  // Subtitle 'Siwasup Asset' (Replaces All About Assets)
  ctx.font = 'bold 50px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif';
  ctx.fillText('Siwasup Asset', redBoxX + redBoxW / 2, redBoxH - 55);

  // Middle Area: Property Note / Space
  const midY = 560;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'top';

  if (p && p.title) {
    ctx.fillStyle = '#8C6D23';
    ctx.font = 'bold 44px "Kanit", "Tahoma", sans-serif';
    ctx.fillText((p.category || 'บ้านพร้อมอยู่') + ' • ' + (p.bank_source ? `ทรัพย์ ${p.bank_source}` : 'ศิวาทรัพย์'), W / 2, midY + 40);

    ctx.fillStyle = '#111827';
    ctx.font = 'bold 64px "Kanit", "Tahoma", sans-serif';
    let shortTitle = p.title;
    if (shortTitle.length > 28) shortTitle = shortTitle.substring(0, 26) + '...';
    ctx.fillText(shortTitle, W / 2, midY + 115);

    if (p.price_negotiate || p.price_sell) {
      ctx.fillStyle = '#C8102E';
      ctx.font = '900 84px "Kanit", "Tahoma", sans-serif';
      const pr = p.price_negotiate || p.price_sell;
      ctx.fillText(`฿${Number(pr).toLocaleString()}`, W / 2, midY + 205);
    }
  }

  // Bottom Red Ribbon for Phone Numbers
  const ribbonY = 1380;
  const ribbonH = 220;
  ctx.fillStyle = '#C8102E';
  ctx.fillRect(0, ribbonY, W, ribbonH);

  // Phone Numbers
  ctx.fillStyle = '#FFFFFF';
  ctx.font = 'bold 74px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif';
  ctx.textAlign = 'left';
  ctx.textBaseline = 'middle';
  ctx.fillText(`📞 ${phoneA}   ${phoneB}`, 70, ribbonY + ribbonH / 2);

  // Dynamic QR Code inside ribbon
  if (qrImg) {
    const qrSize = 250;
    const qrX = W - qrSize - 40;
    const qrY = ribbonY - 20;

    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(qrX - 6, qrY - 6, qrSize + 12, qrSize + 12);
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#D1D5DB';
    ctx.strokeRect(qrX - 6, qrY - 6, qrSize + 12, qrSize + 12);
    ctx.drawImage(qrImg, qrX, qrY, qrSize, qrSize);
  }

  // Slogan below ribbon
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillStyle = '#C8102E';
  ctx.font = 'bold 84px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif';
  ctx.fillText('รับฝากขาย รีโนเวท โฆษณาฟรี!', W / 2, 1750);

  // 4 Corner Eyelet Markers
  drawEyelets(ctx, W, H, 50, 12);
}

// ------------------------------------------------------------------------------
// STYLE 3: HOMERUN MODERN VINYL (120x80, 150x80, 60x90)
// ------------------------------------------------------------------------------
function renderClassicPropertyVinyl(ctx, canvas, p, headline, hook, phone, contactName, showPrice, savedRef, qrImg) {
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

  // Background
  ctx.fillStyle = '#FFFFFF';
  ctx.fillRect(0, 0, W, H);

  // Double border
  ctx.lineWidth = 14;
  ctx.strokeStyle = '#C2A460';
  ctx.strokeRect(16, 16, W - 32, H - 32);

  ctx.lineWidth = 8;
  ctx.strokeStyle = '#990000';
  ctx.strokeRect(34, 34, W - 68, H - 68);

  // Header Banner
  const headerHeight = isVertical ? 380 : 320;
  ctx.fillStyle = '#990000';
  ctx.fillRect(42, 42, W - 84, headerHeight);

  // S Badge
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

  // Headline
  ctx.textAlign = 'right';
  ctx.fillStyle = '#FFFFFF';
  ctx.font = 'bold 88px "Kanit", "Tahoma", sans-serif';
  ctx.fillText(headline, W - 90, 42 + (headerHeight / 2) + 5);

  // Property Details
  const bodyTop = 42 + headerHeight + 60;
  ctx.textAlign = 'left';

  // Category Tag
  const categoryText = (p.category || 'บ้านพร้อมอยู่') + (p.bank_source ? ` • ทรัพย์ ${p.bank_source}` : '');
  ctx.fillStyle = '#8C6D23';
  ctx.font = 'bold 44px "Kanit", "Tahoma", sans-serif';
  ctx.fillText(categoryText, 90, bodyTop);

  // Title
  ctx.fillStyle = '#111827';
  ctx.font = 'bold 74px "Kanit", "Tahoma", sans-serif';
  let titleStr = p.title || 'บ้านสวยทำเลทอง พร้อมอยู่';
  if (titleStr.length > 38 && !isVertical) {
    titleStr = titleStr.substring(0, 36) + '...';
  }
  ctx.fillText(titleStr, 90, bodyTop + 90);

  // Specs
  const specY = bodyTop + 175;
  const specText = (p.specs || 'สเปก 3 ห้องนอน • 2 ห้องน้ำ • ที่จอดรถ') + (p.location ? ` | ทำเล: ${p.location}` : '');
  ctx.fillStyle = '#4B5563';
  ctx.font = '500 46px "Kanit", "Tahoma", sans-serif';
  ctx.fillText(specText, 90, specY);

  // Selling Hook Pill
  const hookY = specY + 60;
  const hookWidth = isVertical ? W - 180 : (W * 0.58);
  ctx.fillStyle = '#FEF3C7';
  ctx.strokeStyle = '#F59E0B';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.roundRect(90, hookY, hookWidth, 80, 20);
  ctx.fill();
  ctx.stroke();

  ctx.fillStyle = '#92400E';
  ctx.font = 'bold 40px "Kanit", "Tahoma", sans-serif';
  ctx.fillText(`⭐ ${hook}`, 120, hookY + 54);

  // Big Price Section
  if (showPrice) {
    const priceY = hookY + 180;
    ctx.fillStyle = '#6B7280';
    ctx.font = 'bold 36px "Kanit", "Tahoma", sans-serif';
    ctx.fillText('ราคาพิเศษเปิดจองเพียง', 90, priceY);

    const priceNum = p.price_sell || p.price_negotiate || 2590000;
    ctx.fillStyle = '#990000';
    ctx.font = '900 115px "Kanit", "Tahoma", sans-serif';
    ctx.fillText(`฿${Number(priceNum).toLocaleString()}`, 90, priceY + 115);

    const monthlyEst = Math.round((priceNum / 1000000) * 3500);
    ctx.fillStyle = '#059669';
    ctx.font = 'bold 44px "Kanit", "Tahoma", sans-serif';
    ctx.fillText(`ผ่อนเริ่มต้นเพียง ~${monthlyEst.toLocaleString()} บ./ด.* (ล้านละ 3,500 บ.)`, 90, priceY + 185);
  }

  // QR Code on right side
  if (qrImg) {
    const qrSize = isVertical ? 380 : 360;
    const qrX = W - qrSize - 120;
    const qrY = isVertical ? H - 760 : bodyTop + 60;

    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(qrX - 10, qrY - 10, qrSize + 20, qrSize + 20);
    ctx.lineWidth = 4;
    ctx.strokeStyle = '#C2A460';
    ctx.strokeRect(qrX - 10, qrY - 10, qrSize + 20, qrSize + 20);
    ctx.drawImage(qrImg, qrX, qrY, qrSize, qrSize);

    ctx.textAlign = 'center';
    ctx.fillStyle = '#1F2937';
    ctx.font = 'bold 30px "Kanit", sans-serif';
    ctx.fillText('สแกนดูรูป & แปลนห้อง', qrX + qrSize / 2, qrY + qrSize + 40);
  }

  // Bottom Footer Bar
  const footerHeight = isVertical ? 280 : 250;
  const footerY = H - footerHeight - 42;

  ctx.fillStyle = '#990000';
  ctx.fillRect(42, footerY, W - 84, footerHeight);

  ctx.textAlign = 'left';
  ctx.fillStyle = '#FDE68A';
  ctx.font = 'bold 36px "Kanit", sans-serif';
  ctx.fillText('📞 สนใจนัดชมบ้านจริง / ปรึกษาสินเชื่อฟรีทุกธนาคาร:', 90, footerY + 65);

  ctx.fillStyle = '#FFFFFF';
  ctx.font = '900 88px "Kanit", sans-serif';
  ctx.fillText(phone, 90, footerY + 160);

  ctx.fillStyle = '#FDE68A';
  ctx.font = 'bold 42px "Kanit", sans-serif';
  ctx.fillText(`ผู้ดูแล: ${contactName}`, 90, footerY + 215);

  drawEyelets(ctx, W, H, 65, 14);
}

// Helper: Draw Eyelet markers
function drawEyelets(ctx, W, H, offset, radius) {
  const eyelets = [
    [offset, offset],
    [W - offset, offset],
    [offset, H - offset],
    [W - offset, H - offset]
  ];
  ctx.fillStyle = '#FFFFFF';
  ctx.strokeStyle = '#374151';
  ctx.lineWidth = 3;
  eyelets.forEach(([ex, ey]) => {
    ctx.beginPath();
    ctx.arc(ex, ey, radius, 0, Math.PI * 2);
    ctx.fill();
    ctx.stroke();
  });
}

// Download Print-Ready PDF at Actual 1:1 Scale (pdf-lib)
async function downloadVinylPDF() {
  const canvas = document.getElementById('vinyl-canvas');
  if (!canvas || !activeVinylProperty || !window.PDFLib) {
    if (typeof showToast === 'function') showToast('กำลังเตรียมระบบ กรุณาลองใหม่อีกครั้ง');
    return;
  }

  try {
    if (typeof showToast === 'function') showToast('⏳ กำลังสร้างไฟล์ PDF ป้ายไวนิลขนาดจริง...');

    const { PDFDocument } = window.PDFLib;
    const pdfDoc = await PDFDocument.create();

    // 1 cm = 72 / 2.54 = 28.3464567 PDF Points
    const ptPerCm = 28.3464567;
    let widthCm = 200;
    let heightCm = 160;

    if (activeVinylPreset === '200x160') {
      widthCm = 200;
      heightCm = 160;
    } else if (activeVinylPreset === '43x49') {
      widthCm = 43;
      heightCm = 49;
    } else if (activeVinylPreset === '120x80') {
      widthCm = 120;
      heightCm = 80;
    } else if (activeVinylPreset === '150x80') {
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
    link.download = `Vinyl_Sign_${activeVinylProperty.id || 'Siwasup'}_${widthCm}x${heightCm}cm.pdf`;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // Automated Point Trigger: Intent to Work (+5 points)
    const agentSearchEl = document.getElementById('vinyl-agent-search');
    const agentCode = (agentSearchEl ? agentSearchEl.value.trim() : '') || localStorage.getItem('siwasup_my_agent_ref') || 'S22';
    if (window.SiwasupAgents && typeof window.SiwasupAgents.award === 'function' && agentCode) {
      window.SiwasupAgents.award(agentCode, 'vinyl_download', { propertyId: activeVinylProperty.id });
    }

    if (typeof showToast === 'function') {
      showToast(`✅ ดาวน์โหลด PDF [${widthCm}x${heightCm} ซม.] สำเร็จ! บันทึกแต้มกิจกรรม +5 แต้ม ให้ [${agentCode}] อัตโนมัติ!`);
    }
  } catch (err) {
    console.error('PDF generation error:', err);
    if (typeof showToast === 'function') showToast('เกิดข้อผิดพลาดในการสร้าง PDF');
  }
}

// Download High-Resolution JPG (Direct LINE sharing to print shops or Save to Camera Roll)
async function downloadVinylJPG() {
  const canvas = document.getElementById('vinyl-canvas');
  if (!canvas || !activeVinylProperty) return;

  let widthCm = 200;
  let heightCm = 160;
  if (activeVinylPreset === '200x160') { widthCm = 200; heightCm = 160; }
  else if (activeVinylPreset === '43x49') { widthCm = 43; heightCm = 49; }
  else if (activeVinylPreset === '120x80') { widthCm = 120; heightCm = 80; }
  else if (activeVinylPreset === '150x80') { widthCm = 150; heightCm = 80; }
  else if (activeVinylPreset === '60x90') { widthCm = 60; heightCm = 90; }

  const fileName = `Vinyl_Sign_${activeVinylProperty.id || 'Siwasup'}_${widthCm}x${heightCm}cm.jpg`;
  const agentSearchEl = document.getElementById('vinyl-agent-search');
  const agentCode = (agentSearchEl ? agentSearchEl.value.trim() : '') || localStorage.getItem('siwasup_my_agent_ref') || 'S22';

  // Check if Mobile Web Share API with File support is available (LINE, iOS Photos, Android)
  if (navigator.share && navigator.canShare && canvas.toBlob) {
    try {
      const blob = await new Promise(resolve => canvas.toBlob(resolve, 'image/jpeg', 0.95));
      const file = new File([blob], fileName, { type: 'image/jpeg' });
      if (navigator.canShare({ files: [file] })) {
        await navigator.share({
          files: [file],
          title: `ป้ายขายด่วน ${widthCm}x${heightCm} ซม.`,
          text: `ป้ายไวนิลศิวาทรัพย์ รหัสทรัพย์ #${activeVinylProperty.id} (ตัวแทน: ${agentCode})`
        });
        if (window.SiwasupAgents && typeof window.SiwasupAgents.award === 'function' && agentCode) {
          window.SiwasupAgents.award(agentCode, 'vinyl_download', { propertyId: activeVinylProperty.id });
        }
        if (typeof showToast === 'function') {
          showToast(`✅ แชร์รูปภาพสำเร็จ! บันทึกแต้มกิจกรรม +5 แต้ม ให้ [${agentCode}] อัตโนมัติ!`);
        }
        return;
      }
    } catch (shareErr) {
      if (shareErr.name !== 'AbortError') {
        console.warn('Web Share failed, fallback to download:', shareErr);
      } else {
        return; // User canceled share
      }
    }
  }

  // Standard File Download fallback (PC / Mac)
  const link = document.createElement('a');
  link.href = canvas.toDataURL('image/jpeg', 0.95);
  link.download = fileName;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);

  // Automated Point Trigger: Intent to Work (+5 points)
  if (window.SiwasupAgents && typeof window.SiwasupAgents.award === 'function' && agentCode) {
    window.SiwasupAgents.award(agentCode, 'vinyl_download', { propertyId: activeVinylProperty.id });
  }

  if (typeof showToast === 'function') {
    showToast(`✅ บันทึกรูปภาพ HD [${widthCm}x${heightCm} ซม.] สำเร็จ! บันทึกแต้มกิจกรรม +5 แต้ม ให้ [${agentCode}] อัตโนมัติ!`);
  }
}

// Global window bindings
window.openVinylModal = openVinylModal;
window.closeVinylModal = closeVinylModal;
window.setVinylPreset = setVinylPreset;
window.renderVinylCanvas = renderVinylCanvas;
window.downloadVinylPDF = downloadVinylPDF;
window.downloadVinylJPG = downloadVinylJPG;
