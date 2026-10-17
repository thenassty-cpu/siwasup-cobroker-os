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
    subtitleEl.value = 'www.siwasup.com ซื้อ ขาย บ้าน ที่ดิน ทำการตลาดฟรี  @siwasup';
  }
  if (contactNameEl) {
    if (agent) {
      const lineText = agent.lineId ? agent.lineId : '@siwasup';
      contactNameEl.value = `${agent.nickname || agent.name} (LINE: ${lineText})`;
    } else {
      contactNameEl.value = savedRef.replace('AG-', '') + ' (LINE: @siwasup)';
    }
  }

  // Pre-fill inputs for 43x49 cm
  const assetEl = document.getElementById('vinyl-asset');
  const detailEl = document.getElementById('vinyl-detail');
  const priceEl = document.getElementById('vinyl-price');
  if (assetEl) assetEl.value = p.category ? `${p.category}พร้อมอยู่` : 'บ้านเดี่ยวพร้อมอยู่';
  if (detailEl) detailEl.value = (p.specs || '2 ห้องนอน 2 ห้องน้ำ') + (p.location ? ` ทำเล${p.location}` : ' ทำเลรามคำแหง');
  if (priceEl) priceEl.value = `฿ ${Number(p.price_sell || p.price_negotiate || 2500000).toLocaleString()}`;

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

// Set Preset Dimensions (Focus on 2 Official Master Templates)
function setVinylPreset(preset) {
  activeVinylPreset = preset;
  const dimsLabel = document.getElementById('vinyl-preview-dims');

  const btn200 = document.getElementById('btn-preset-200x160');
  const btn43 = document.getElementById('btn-preset-43x49');
  const sec200 = document.getElementById('vinyl-section-200x160');
  const sec43 = document.getElementById('vinyl-section-43x49');

  if (preset === '200x160') {
    if (btn200) btn200.className = 'py-2 px-2.5 rounded-xl border font-bold text-xs text-center transition-all bg-[#990000] text-white border-[#990000] shadow-xs active:scale-95';
    if (btn43) btn43.className = 'py-2 px-2.5 rounded-xl border font-medium text-xs text-center transition-all bg-white text-gray-700 border-gray-200 hover:bg-gray-50 active:scale-95';
    if (dimsLabel) dimsLabel.textContent = '200 x 160 ซม. (ขายด่วน 5:4 สไตล์บัว)';
    if (sec200) sec200.classList.remove('hidden');
    if (sec43) sec43.classList.add('hidden');
  } else if (preset === '43x49') {
    if (btn200) btn200.className = 'py-2 px-2.5 rounded-xl border font-medium text-xs text-center transition-all bg-white text-gray-700 border-gray-200 hover:bg-gray-50 active:scale-95';
    if (btn43) btn43.className = 'py-2 px-2.5 rounded-xl border font-bold text-xs text-center transition-all bg-[#990000] text-white border-[#990000] shadow-xs active:scale-95';
    if (dimsLabel) dimsLabel.textContent = '43 x 49 ซม. (ไซส์ S ส่งร้าน/ติดเสา)';
    if (sec200) sec200.classList.add('hidden');
    if (sec43) sec43.classList.remove('hidden');
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
  const phoneA = (document.getElementById('vinyl-phone')?.value || '094-462-9796').trim();
  const phoneB = (document.getElementById('vinyl-phone-b')?.value || '096-129-2459').trim();
  const subtitle = (document.getElementById('vinyl-subtitle')?.value || 'www.siwasup.com ซื้อ ขาย บ้าน ที่ดิน ทำการตลาดฟรี  @siwasup').trim();
  const agentInfo = (document.getElementById('vinyl-agent-info')?.value || 'ติดต่อ: คุณเอ (ตัวแทนพื้นที่โซนบางนา) LINE ID: ของตัวแทน').trim();
  
  // Specific values for 43x49 cm
  const assetText = (document.getElementById('vinyl-asset')?.value || '').trim() || (p.category ? `${p.category}พร้อมอยู่` : 'บ้านเดี่ยวพร้อมอยู่');
  const detailText = (document.getElementById('vinyl-detail')?.value || '').trim() || ((p.specs || '2 ห้องนอน 2 ห้องน้ำ') + (p.location ? ` ทำเล${p.location}` : ' ทำเลรามคำแหง'));
  const priceText = (document.getElementById('vinyl-price')?.value || '').trim() || (`฿ ${Number(p.price_sell || p.price_negotiate || 2500000).toLocaleString()}`);

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

  // Branch by Preset Style (2 Official Master Templates)
  if (activeVinylPreset === '200x160') {
    renderSiwasupMaster200x160(ctx, canvas, p, headline, phoneA, phoneB, subtitle, agentInfo, savedRef, qrImg, logoImg);
  } else if (activeVinylPreset === '43x49') {
    renderSiwasupMaster43x49(ctx, canvas, p, assetText, detailText, priceText, phoneA, phoneB, savedRef, qrImg, logoImg);
  } else {
    renderSiwasupMaster200x160(ctx, canvas, p, headline, phoneA, phoneB, subtitle, agentInfo, savedRef, qrImg, logoImg);
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

  // ⭐ Headline Text (Supports auto 2-line break & auto-shrink to NEVER overflow red box)
  ctx.fillStyle = '#FFFFFF';
  const maxHeadW = W - 140; // 1860px max width inside red box
  
  let headLines = [];
  if (headline.includes('/')) {
    const parts = headline.split('/');
    headLines.push(parts[0].trim());
    headLines.push(parts[1].trim());
  } else if (headline.includes('\n')) {
    headLines = headline.split('\n').map(s => s.trim()).filter(Boolean);
  } else if (headline.length > 9) {
    const spaceIdx = headline.lastIndexOf(' ', 9);
    if (spaceIdx !== -1) {
      headLines.push(headline.substring(0, spaceIdx).trim());
      headLines.push(headline.substring(spaceIdx + 1).trim());
    } else {
      headLines = [headline];
    }
  } else {
    headLines = [headline];
  }

  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';

  if (headLines.length > 1) {
    // 2-line layout
    let fontSize = 210;
    ctx.font = `bold ${fontSize}px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif`;
    while ((ctx.measureText(headLines[0]).width > maxHeadW || ctx.measureText(headLines[1]).width > maxHeadW) && fontSize > 80) {
      fontSize -= 4;
      ctx.font = `bold ${fontSize}px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif`;
    }
    const lineGap = fontSize * 1.08;
    const midY = 30 + headerHeight / 2;
    ctx.fillText(headLines[0], W / 2, midY - lineGap / 2);
    ctx.fillText(headLines[1], W / 2, midY + lineGap / 2);
  } else {
    // 1-line layout
    let fontSize = 300;
    ctx.font = `bold ${fontSize}px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif`;
    while (ctx.measureText(headLines[0]).width > maxHeadW && fontSize > 110) {
      fontSize -= 6;
      ctx.font = `bold ${fontSize}px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif`;
    }
    ctx.fillText(headLines[0], W / 2, 30 + headerHeight / 2);
  }

  // ⭐ 1.1 Signature Satin Gold Accent Bar (แถบสีทองคั่นใต้บล็อกแดงตาม Ads200x160.ait)
  const goldBarH = 26;
  const goldBarY = 30 + headerHeight;
  ctx.fillStyle = '#C2A460'; // Satin Gold CI
  ctx.fillRect(30, goldBarY, W - 60, goldBarH);

  // 2. Middle Body: Job_Discription + Huge Phone Numbers + Ticker_AgentInfo
  const bodyTop = goldBarY + goldBarH;

  // Job_Discription: Red Web & LINE text
  ctx.fillStyle = '#C8102E';
  ctx.font = 'bold 46px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'top';
  ctx.fillText(subtitle, W / 2, bodyTop + 24);

  // Phone Numbers - Enlarge to 235px (crisp, prominent from 50m distance)
  const maxPhoneW = W - 160; // 1840px
  let phoneFontSize = 235;
  ctx.font = `bold ${phoneFontSize}px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif`;
  while ((ctx.measureText(phoneA).width > maxPhoneW || (phoneB && ctx.measureText(phoneB).width > maxPhoneW)) && phoneFontSize > 150) {
    phoneFontSize -= 5;
    ctx.font = `bold ${phoneFontSize}px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif`;
  }

  ctx.fillStyle = '#111827';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';

  if (phoneB && phoneB.trim() !== '') {
    ctx.fillText(phoneA, W / 2, bodyTop + 175);
    ctx.fillText(phoneB, W / 2, bodyTop + 395);
  } else {
    // Single phone number: center it prominently
    ctx.fillText(phoneA, W / 2, bodyTop + 280);
  }

  // Ticker_AgentInfo: Red text line below phone numbers - Enlarge to 52px
  ctx.fillStyle = '#C8102E';
  let agentFontSize = 52;
  ctx.font = `bold ${agentFontSize}px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif`;
  while (ctx.measureText(agentInfo).width > maxPhoneW && agentFontSize > 28) {
    agentFontSize -= 2;
    ctx.font = `bold ${agentFontSize}px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif`;
  }
  ctx.fillText(agentInfo, W / 2, bodyTop + 525);

  // 3. Bottom Footer Bar: Siwasup Logo + Services + QR Code (Centered Harmonious Group)
  const footerTop = 1260;
  const logoW = 190;
  const logoH = 152;
  const qrSize = 155;
  const textW = 760;
  const gap = 35;
  const totalGroupW = logoW + gap + textW + gap + qrSize; // ~1175px
  const startX = Math.round((W - totalGroupW) / 2); // Center of whole artboard (~412px)

  // Siwasup Logo on the left of group
  if (logoImg) {
    ctx.drawImage(logoImg, startX, footerTop + 6, logoW, logoH);
  } else {
    ctx.fillStyle = '#C8102E';
    ctx.beginPath();
    ctx.arc(startX + logoW / 2, footerTop + logoH / 2, 50, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#FFFFFF';
    ctx.font = 'bold 50px "Kanit", sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('S', startX + logoW / 2, footerTop + logoH / 2);
  }

  // Footer Center Text: Services & Catchphrase
  const textX = startX + logoW + gap;
  ctx.textAlign = 'left';
  ctx.textBaseline = 'top';

  ctx.fillStyle = '#C8102E';
  ctx.font = 'bold 64px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif';
  ctx.fillText('รับฝากขายบ้าน-ที่ดิน', textX, footerTop + 12);

  ctx.fillStyle = '#1F2937';
  ctx.font = 'bold 36px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif';
  ctx.fillText('ให้เราช่วยขาย ง่ายกว่า โฆษณาฟรี มีบริการจัดสินเชื่อ', textX, footerTop + 85);

  ctx.fillStyle = '#9CA3AF';
  ctx.font = '500 24px "Kanit", "Tahoma", sans-serif';
  ctx.fillText(`รหัสตัวแทน: ${savedRef} • บริษัท ศิวาทรัพย์ แอสเซท จำกัด`, textX, footerTop + 138);

  // Footer Right: Dynamic QR Code
  const qrX = textX + textW + gap;
  if (qrImg) {
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(qrX - 4, footerTop - 4, qrSize + 8, qrSize + 8);
    ctx.lineWidth = 1.5;
    ctx.strokeStyle = '#E5E7EB';
    ctx.strokeRect(qrX - 4, footerTop - 4, qrSize + 8, qrSize + 8);
    ctx.drawImage(qrImg, qrX, footerTop, qrSize, qrSize);
  }

  // 4 Corner Eyelet Markers
  drawEyelets(ctx, W, H, 55, 14);
}

// ------------------------------------------------------------------------------
// STYLE 2: SIWASUP MASTER 43x49 CM (ป้ายไซส์ S ส่งร้าน/ติดเสาไฟฟ้า ตาม Ads43x49.ai)
// ------------------------------------------------------------------------------
function renderSiwasupMaster43x49(ctx, canvas, p, assetText, detailText, priceText, phoneA, phoneB, savedRef, qrImg, logoImg) {
  const W = 1720;
  const H = 1960;
  canvas.width = W;
  canvas.height = H;

  // Canvas Background
  ctx.fillStyle = '#FFFFFF';
  ctx.fillRect(0, 0, W, H);

  // Outer safety guide
  ctx.lineWidth = 4;
  ctx.strokeStyle = '#E5E7EB';
  ctx.strokeRect(30, 30, W - 60, H - 60);

  // Top-Left: Siwasup Logo
  if (logoImg) {
    ctx.drawImage(logoImg, 100, 80, 380, 305);
  }

  // Top-Right: Solid Red Header Block 'ขาย'
  const redBoxX = 600;
  const redBoxW = W - redBoxX - 50;
  const redBoxH = 460;
  ctx.fillStyle = '#C8102E';
  ctx.fillRect(redBoxX, 50, redBoxW, redBoxH);

  // White text 'ขาย'
  ctx.fillStyle = '#FFFFFF';
  ctx.font = 'bold 260px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText('ขาย', redBoxX + redBoxW / 2, 50 + redBoxH / 2 - 30);

  // Subtitle 'Siwasup Assets' (ตรงตามไฟล์ Ads43x49.ai)
  ctx.font = 'bold 48px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif';
  ctx.fillText('Siwasup Assets', redBoxX + redBoxW / 2, 50 + redBoxH - 50);

  // ⭐ Signature Satin Gold Accent Bar (แถบสีทองคั่นใต้ส่วนหัวตาม Ads43x49.ai)
  const goldBarY = 50 + redBoxH + 20;
  const goldBarH = 24;
  ctx.fillStyle = '#C2A460'; // Satin Gold CI
  ctx.fillRect(50, goldBarY, W - 100, goldBarH);

  // Middle Area: Ticker_Asset + Ticker_Detail + Ticker_Price
  const midY = goldBarY + goldBarH + 60;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'top';

  // Helper for auto-shrinking text to fit max width (37 cm = 1480px on this 1720 canvas)
  const maxContentW = Math.round(W * (37 / 43)); // 1480px
  function fillAutoFitText(text, x, y, initialSize, minSize, fontFace, fillStyle) {
    let size = initialSize;
    ctx.fillStyle = fillStyle;
    ctx.font = `bold ${size}px ${fontFace}`;
    while (ctx.measureText(text).width > maxContentW && size > minSize) {
      size -= 2;
      ctx.font = `bold ${size}px ${fontFace}`;
    }
    ctx.fillText(text, x, y);
  }

  // 1. Ticker_Asset (Gold font: บ้านเดี่ยวพร้อมอยู่)
  fillAutoFitText(assetText, W / 2, midY + 50, 96, 48, '"RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif', '#967C3E');

  // 2. Ticker_Detail (Dark font: 2 ห้องนอน 2 ห้องน้ำ ทำเลรามคำแหง)
  fillAutoFitText(detailText, W / 2, midY + 190, 68, 36, '"RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif', '#1F2937');

  // 3. Ticker_Price (Big Red font: ฿ 2,500,000)
  fillAutoFitText(priceText, W / 2, midY + 310, 144, 72, '"RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif', '#C8102E');

  // Bottom Red Ribbon for Phone Numbers
  const ribbonY = 1480;
  const ribbonH = 190;
  ctx.fillStyle = '#C8102E';
  ctx.fillRect(50, ribbonY, W - 100, ribbonH);

  // Phone Numbers
  ctx.fillStyle = '#FFFFFF';
  ctx.font = 'bold 50px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif';
  ctx.textAlign = 'left';
  ctx.textBaseline = 'middle';
  ctx.fillText(`📞 ${phoneA}   ${phoneB}`, 90, ribbonY + ribbonH / 2);

  // Dynamic QR Code on right side of ribbon
  if (qrImg) {
    const qrSize = 220;
    const qrX = W - qrSize - 80;
    const qrY = ribbonY - 15;

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
  ctx.font = 'bold 78px "RSU", "RSU Bold", "Kanit", "Tahoma", sans-serif';
  ctx.fillText('รับฝากขาย รีโนเวท โฆษณาฟรี!', W / 2, ribbonY + ribbonH + 110);

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
