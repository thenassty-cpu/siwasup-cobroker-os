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

  // Smart Auto-Fit & Weight Mode Controls
  const autoExpand = document.getElementById('vinyl-auto-expand') ? document.getElementById('vinyl-auto-expand').checked : true;
  const weightMode = document.getElementById('vinyl-weight-mode')?.value || 'heavy'; // 'normal', 'heavy', 'ultra'

  const savedRef = (document.getElementById('vinyl-agent-search')?.value || 'S22').trim();
  const targetUrl = `https://thenassty-cpu.github.io/siwasup-cobroker-os/?ref=${encodeURIComponent(savedRef)}&id=${encodeURIComponent(p.id)}&ch=vinyl`;
  
  // 🔤 Guarantee Web Fonts (Kanit 700/800/900 & RSU) are loaded in browser before Canvas drawing
  if (document.fonts && typeof document.fonts.load === 'function') {
    try {
      await Promise.all([
        document.fonts.load('800 100px Kanit'),
        document.fonts.load('900 100px Kanit'),
        document.fonts.load('bold 100px RSU'),
        document.fonts.load('normal 40px RSU')
      ]);
    } catch (e) {
      console.warn('Font preloading:', e);
    }
  }

  const qrDataUrl = await generateQrDataUrl(targetUrl);
  const qrImg = await loadImage(qrDataUrl);
  const logoImg = await loadImage('assets/siwasup_logo.png');

  // Branch by Preset Style (2 Official Master Templates)
  if (activeVinylPreset === '200x160') {
    renderSiwasupMaster200x160(ctx, canvas, p, headline, phoneA, phoneB, subtitle, agentInfo, savedRef, qrImg, logoImg, autoExpand, weightMode);
  } else if (activeVinylPreset === '43x49') {
    renderSiwasupMaster43x49(ctx, canvas, p, assetText, detailText, priceText, phoneA, phoneB, savedRef, qrImg, logoImg, autoExpand, weightMode);
  } else {
    renderSiwasupMaster200x160(ctx, canvas, p, headline, phoneA, phoneB, subtitle, agentInfo, savedRef, qrImg, logoImg, autoExpand, weightMode);
  }
}

// ==============================================================================
// 🪄 UNIVERSAL 2-WAY SMART AUTO-FIT & STROKE THICKNESS ENGINE
// Automatically expands short text to fill target width (up to maxSize & maxStretchX)
// and shrinks long text to stay within maxW, plus applies Faux-Bold Offset Stroke.
// ==============================================================================
function drawSmartText(ctx, text, x, y, opts) {
  if (!text) return 0;
  const {
    targetW = 1400,
    maxW = 1500,
    baseSize = 100,
    maxSize = 240,
    minSize = 40,
    fillStyle = '#000000',
    fontFamily = '"Kanit", "RSU", "Tahoma", sans-serif',
    align = 'center',
    baseline = 'middle',
    autoExpand = true,
    weightMode = 'heavy', // 'normal', 'heavy', 'ultra'
    maxStretchX = 1.16    // Gentle horizontal expansion up to 16% when text is very short
  } = opts;

  const cssWeight = weightMode === 'ultra' ? '900' : (weightMode === 'heavy' ? '800' : '700');
  const strokeFactor = weightMode === 'ultra' ? 0.036 : (weightMode === 'heavy' ? 0.018 : 0);

  let size = baseSize;
  ctx.font = `${cssWeight} ${size}px ${fontFamily}`;
  let w = ctx.measureText(text).width;

  // 1. Scale UP if autoExpand is active and text is narrower than targetW
  if (autoExpand && w < targetW && size < maxSize) {
    while (w < targetW && size < maxSize) {
      size += 2;
      ctx.font = `${cssWeight} ${size}px ${fontFamily}`;
      w = ctx.measureText(text).width;
    }
  }

  // 2. Scale DOWN if text exceeds maximum safe width (maxW)
  while (w > maxW && size > minSize) {
    size -= 2;
    ctx.font = `${cssWeight} ${size}px ${fontFamily}`;
    w = ctx.measureText(text).width;
  }

  // 3. Apply gentle horizontal stretch if text hit vertical maxSize ceiling but still looks narrow
  let scaleX = 1.0;
  if (autoExpand && w > 0 && w < targetW * 0.90 && maxStretchX > 1.0) {
    scaleX = Math.min(maxStretchX, (targetW * 0.90) / w);
  }

  ctx.save();
  ctx.textAlign = align;
  ctx.textBaseline = baseline;
  ctx.fillStyle = fillStyle;
  ctx.font = `${cssWeight} ${size}px ${fontFamily}`;

  if (scaleX !== 1.0) {
    ctx.translate(x, y);
    ctx.scale(scaleX, 1);
    if (strokeFactor > 0) {
      ctx.strokeStyle = fillStyle;
      ctx.lineWidth = Math.max(1.5, size * strokeFactor);
      ctx.lineJoin = 'round';
      ctx.miterLimit = 2;
      ctx.strokeText(text, 0, 0);
    }
    ctx.fillText(text, 0, 0);
  } else {
    if (strokeFactor > 0) {
      ctx.strokeStyle = fillStyle;
      ctx.lineWidth = Math.max(1.5, size * strokeFactor);
      ctx.lineJoin = 'round';
      ctx.miterLimit = 2;
      ctx.strokeText(text, x, y);
    }
    ctx.fillText(text, x, y);
  }
  ctx.restore();
  return size;
}

// ------------------------------------------------------------------------------
// STYLE 1: SIWASUP MASTER 200x160 CM (ขายด่วน สไตล์ Ads200x160.ait พร้อม Bar สีทอง)
// ------------------------------------------------------------------------------
function renderSiwasupMaster200x160(ctx, canvas, p, headline, phoneA, phoneB, subtitle, agentInfo, savedRef, qrImg, logoImg, autoExpand = true, weightMode = 'heavy') {
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

  // ⭐ Headline Text: Break into 2 lines ONLY when text is long (> 14 chars like 'บ้านหลุดจำนอง / NPA')
  // Short phrases like 'ขายด่วน', 'ขาย / ให้เช่า', 'ขายบ้านรีโนเวท' stay on 1 huge full-bleed line!
  const maxHeadW = W - 130;    // 1870px hard limit
  const targetHeadW = W - 220; // 1780px target fill width

  let headLines = [];
  if (headline.includes('\n')) {
    headLines = headline.split('\n').map(s => s.trim()).filter(Boolean);
  } else if (headline.length > 14 && headline.includes('/')) {
    const parts = headline.split('/');
    headLines.push(parts[0].trim());
    headLines.push(parts[1].trim());
  } else if (headline.length > 16) {
    const spaceIdx = headline.lastIndexOf(' ', 12);
    if (spaceIdx !== -1) {
      headLines.push(headline.substring(0, spaceIdx).trim());
      headLines.push(headline.substring(spaceIdx + 1).trim());
    } else {
      headLines = [headline];
    }
  } else {
    headLines = [headline];
  }

  if (headLines.length > 1) {
    // 2-line layout inside 580px red box (Each line up to 250px tall)
    const midY = 30 + headerHeight / 2;
    const lineGap = 240;
    drawSmartText(ctx, headLines[0], W / 2, midY - lineGap / 2 - 5, {
      targetW: targetHeadW,
      maxW: maxHeadW,
      baseSize: 215,
      maxSize: 255,
      minSize: 90,
      fillStyle: '#FFFFFF',
      autoExpand,
      weightMode,
      maxStretchX: 1.20
    });
    drawSmartText(ctx, headLines[1], W / 2, midY + lineGap / 2 + 5, {
      targetW: targetHeadW * 0.75,
      maxW: maxHeadW,
      baseSize: 215,
      maxSize: 255,
      minSize: 90,
      fillStyle: '#FFFFFF',
      autoExpand,
      weightMode,
      maxStretchX: 1.25
    });
  } else {
    // 1-line layout: Expands up to 410px tall to fill the 580px red box like Ads200x160.ait!
    drawSmartText(ctx, headLines[0], W / 2, 30 + headerHeight / 2 + 8, {
      targetW: targetHeadW,
      maxW: maxHeadW,
      baseSize: 310,
      maxSize: 410,
      minSize: 120,
      fillStyle: '#FFFFFF',
      autoExpand,
      weightMode,
      maxStretchX: 1.22
    });
  }

  // ⭐ 1.1 Signature Satin Gold Accent Bar (แถบสีทองคั่นใต้บล็อกแดงตาม Ads200x160.ait)
  const goldBarH = 26;
  const goldBarY = 30 + headerHeight;
  ctx.fillStyle = '#C2A460'; // Satin Gold CI
  ctx.fillRect(30, goldBarY, W - 60, goldBarH);

  // 2. Middle Body: Job_Discription + Huge Phone Numbers + Ticker_AgentInfo
  const bodyTop = goldBarY + goldBarH;

  // Job_Discription: Red Web & LINE text (Fills width nicely above phones)
  drawSmartText(ctx, subtitle, W / 2, bodyTop + 42, {
    targetW: 1680,
    maxW: 1840,
    baseSize: 48,
    maxSize: 64,
    minSize: 28,
    fillStyle: '#C8102E',
    autoExpand,
    weightMode: weightMode === 'ultra' ? 'heavy' : 'normal',
    maxStretchX: 1.08
  });

  // Phone Numbers - Auto-Fit to span 1760px width across the 2000px banner!
  if (phoneB && phoneB.trim() !== '') {
    drawSmartText(ctx, phoneA, W / 2, bodyTop + 190, {
      targetW: 1760,
      maxW: 1850,
      baseSize: 235,
      maxSize: 285,
      minSize: 140,
      fillStyle: '#1F2937',
      autoExpand,
      weightMode,
      maxStretchX: 1.18
    });
    drawSmartText(ctx, phoneB, W / 2, bodyTop + 405, {
      targetW: 1760,
      maxW: 1850,
      baseSize: 235,
      maxSize: 285,
      minSize: 140,
      fillStyle: '#1F2937',
      autoExpand,
      weightMode,
      maxStretchX: 1.18
    });
  } else {
    // Single phone number: Massive centered hero number
    drawSmartText(ctx, phoneA, W / 2, bodyTop + 295, {
      targetW: 1800,
      maxW: 1860,
      baseSize: 270,
      maxSize: 330,
      minSize: 150,
      fillStyle: '#1F2937',
      autoExpand,
      weightMode,
      maxStretchX: 1.22
    });
  }

  // Ticker_AgentInfo: Red text line below phone numbers
  drawSmartText(ctx, agentInfo, W / 2, bodyTop + 545, {
    targetW: 1560,
    maxW: 1840,
    baseSize: 52,
    maxSize: 68,
    minSize: 28,
    fillStyle: '#C8102E',
    autoExpand,
    weightMode: weightMode === 'ultra' ? 'heavy' : 'normal',
    maxStretchX: 1.08
  });

  // 3. Bottom Footer Bar: Siwasup Logo + Services + QR Code (Larger & Perfectly Centered Group)
  const footerTop = 1255;
  const logoW = 225;
  const logoH = 180;
  const qrSize = 185;
  const textW = 860;
  const gap = 38;
  const totalGroupW = logoW + gap + textW + gap + qrSize; // 1346px
  const startX = Math.round((W - totalGroupW) / 2); // Centered at ~327px

  // Siwasup Logo on the left of group
  if (logoImg) {
    ctx.drawImage(logoImg, startX, footerTop + 5, logoW, logoH);
  } else {
    ctx.fillStyle = '#C8102E';
    ctx.beginPath();
    ctx.arc(startX + logoW / 2, footerTop + logoH / 2, 60, 0, Math.PI * 2);
    ctx.fill();
    ctx.fillStyle = '#FFFFFF';
    ctx.font = 'bold 60px "Kanit", sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('S', startX + logoW / 2, footerTop + logoH / 2);
  }

  // Footer Center Text: Services & Catchphrase (Auto-fit to textW = 860px)
  const textCenterX = startX + logoW + gap + textW / 2;
  drawSmartText(ctx, 'รับฝากขายบ้าน-ที่ดิน', textCenterX, footerTop + 48, {
    targetW: textW * 0.96,
    maxW: textW,
    baseSize: 78,
    maxSize: 98,
    minSize: 48,
    fillStyle: '#C8102E',
    autoExpand,
    weightMode,
    maxStretchX: 1.15
  });

  drawSmartText(ctx, 'ให้เราช่วยขาย ง่ายกว่า โฆษณาฟรี มีบริการจัดสินเชื่อ', textCenterX, footerTop + 118, {
    targetW: textW * 0.96,
    maxW: textW,
    baseSize: 40,
    maxSize: 48,
    minSize: 28,
    fillStyle: '#1F2937',
    autoExpand,
    weightMode: 'normal',
    maxStretchX: 1.08
  });

  ctx.fillStyle = '#6B7280';
  ctx.font = '600 26px "Kanit", "Tahoma", sans-serif';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(`รหัสตัวแทน: ${savedRef} • บริษัท ศิวาทรัพย์ แอสเซท จำกัด`, textCenterX, footerTop + 165);

  // Footer Right: Dynamic QR Code
  const qrX = startX + logoW + gap + textW + gap;
  if (qrImg) {
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(qrX - 5, footerTop - 2, qrSize + 10, qrSize + 10);
    ctx.lineWidth = 2;
    ctx.strokeStyle = '#E5E7EB';
    ctx.strokeRect(qrX - 5, footerTop - 2, qrSize + 10, qrSize + 10);
    ctx.drawImage(qrImg, qrX, footerTop + 3, qrSize, qrSize);
  }

  // 4 Corner Eyelet Markers
  drawEyelets(ctx, W, H, 55, 14);
}

// ------------------------------------------------------------------------------
// STYLE 2: SIWASUP MASTER 43x49 CM (ป้ายไซส์ S ส่งร้าน/ติดเสาไฟฟ้า ตาม Ads43x49.ai)
// ------------------------------------------------------------------------------
function renderSiwasupMaster43x49(ctx, canvas, p, assetText, detailText, priceText, phoneA, phoneB, savedRef, qrImg, logoImg, autoExpand = true, weightMode = 'heavy') {
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

  // Top-Left: Siwasup Logo (Larger & nicely proportioned in top-left box)
  if (logoImg) {
    ctx.drawImage(logoImg, 85, 75, 420, 340);
  }

  // Top-Right: Solid Red Header Block 'ขาย'
  const redBoxX = 560;
  const redBoxW = W - redBoxX - 50; // 1110px
  const redBoxH = 460;
  ctx.fillStyle = '#C8102E';
  ctx.fillRect(redBoxX, 50, redBoxW, redBoxH);

  // White text 'ขาย' (Fills the red box boldly like Ads43x49.ai!)
  drawSmartText(ctx, 'ขาย', redBoxX + redBoxW / 2, 50 + redBoxH / 2 - 28, {
    targetW: redBoxW * 0.84,
    maxW: redBoxW - 60,
    baseSize: 310,
    maxSize: 390,
    minSize: 180,
    fillStyle: '#FFFFFF',
    autoExpand: true,
    weightMode,
    maxStretchX: 1.22
  });

  // Subtitle 'Siwasup Assets' (Right-aligned under 'ขาย' matching Ads43x49.ai)
  ctx.fillStyle = '#FFFFFF';
  ctx.font = '700 50px "Kanit", "RSU", "Tahoma", sans-serif';
  ctx.textAlign = 'right';
  ctx.textBaseline = 'middle';
  ctx.fillText('Siwasup Assets', redBoxX + redBoxW - 65, 50 + redBoxH - 42);

  // ⭐ Signature Satin Gold Accent Bar (แถบสีทองคั่นใต้ส่วนหัวตาม Ads43x49.ai)
  const goldBarY = 50 + redBoxH + 16;
  const goldBarH = 26;
  ctx.fillStyle = '#C2A460'; // Satin Gold CI
  ctx.fillRect(50, goldBarY, W - 100, goldBarH);

  // Middle Area: Ticker_Asset + Ticker_Detail + Ticker_Price (2-Way Smart Auto-Fit)
  // Hard safety limit: 37 cm = 1480px on this 1720px canvas
  const maxContentW = Math.round(W * (37 / 43)); // 1480px

  // 1. Ticker_Asset (Gold font: คอนโด UBIO ริมถนน / บ้านเดี่ยวพร้อมอยู่)
  drawSmartText(ctx, assetText, W / 2, 695, {
    targetW: 1380,
    maxW: maxContentW,
    baseSize: 165,
    maxSize: 225,
    minSize: 65,
    fillStyle: '#967C3E',
    autoExpand,
    weightMode,
    maxStretchX: 1.18
  });

  // 2. Ticker_Detail (Dark font: รีโนเวทหรู พร้อมอยู่ / 3 ห้องนอน ทำเลพุทธมณฑลสาย 2)
  drawSmartText(ctx, detailText, W / 2, 945, {
    targetW: 1340,
    maxW: maxContentW,
    baseSize: 120,
    maxSize: 165,
    minSize: 48,
    fillStyle: '#1F2937',
    autoExpand,
    weightMode,
    maxStretchX: 1.15
  });

  // 3. Ticker_Price (Big Red font: ฿ 1,500,000)
  drawSmartText(ctx, priceText, W / 2, 1235, {
    targetW: 1420,
    maxW: maxContentW,
    baseSize: 245,
    maxSize: 315,
    minSize: 95,
    fillStyle: '#C8102E',
    autoExpand,
    weightMode,
    maxStretchX: 1.20
  });

  // Bottom Red Ribbon for Phone Numbers
  const ribbonY = 1480;
  const ribbonH = 185;
  ctx.fillStyle = '#C8102E';
  ctx.fillRect(50, ribbonY, W - 100, ribbonH);

  // Dynamic QR Code on right side of ribbon
  const qrSize = 265;
  const qrX = W - qrSize - 75; // 1380px
  const qrY = ribbonY - 35;

  // Phone Numbers on left of ribbon - Auto-Fit to fill the ribbon space before QR code!
  const phoneText = phoneB && phoneB.trim() !== '' ? `📞 ${phoneA}   ${phoneB}` : `📞 ${phoneA}`;
  const availRibbonW = qrX - 110; // ~1270px available width
  drawSmartText(ctx, phoneText, 75 + availRibbonW / 2, ribbonY + ribbonH / 2, {
    targetW: availRibbonW * 0.94,
    maxW: availRibbonW,
    baseSize: 68,
    maxSize: 98,
    minSize: 42,
    fillStyle: '#FFFFFF',
    autoExpand,
    weightMode,
    maxStretchX: 1.12
  });

  if (qrImg) {
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(qrX - 8, qrY - 8, qrSize + 16, qrSize + 16);
    ctx.lineWidth = 2.5;
    ctx.strokeStyle = '#D1D5DB';
    ctx.strokeRect(qrX - 8, qrY - 8, qrSize + 16, qrSize + 16);
    ctx.drawImage(qrImg, qrX, qrY, qrSize, qrSize);
  }

  // Slogan below ribbon - Auto-Fit across the bottom area
  drawSmartText(ctx, 'รับฝากขาย รีโนเวท โฆษณาฟรี!', (50 + qrX) / 2 + 40, ribbonY + ribbonH + 115, {
    targetW: 1260,
    maxW: 1380,
    baseSize: 88,
    maxSize: 112,
    minSize: 56,
    fillStyle: '#C8102E',
    autoExpand,
    weightMode,
    maxStretchX: 1.14
  });

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
