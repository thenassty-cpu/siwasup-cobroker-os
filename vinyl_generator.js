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
// 🪄 UNIVERSAL 2-WAY SMART AUTO-FIT, STROKE THICKNESS & THAI TONE CLEARANCE ENGINE
// Automatically expands short text to fill target width, shrinks long text to stay
// within maxW, applies Faux-Bold Offset Stroke, and reserves top headroom for Thai
// upper vowels + tone marks (วรรณยุกต์ซ้อน เช่น บ้านเดี่ยว, ขายด่วน, ที่ดิน, ชั้น).
// ==============================================================================
function getThaiHeadroomProfile(str) {
  const s = String(str || '');
  // Double top stack: upper vowel (\u0E31, \u0E34-\u0E37, \u0E47, \u0E4D) + tone mark (\u0E48-\u0E4C) e.g. เดี่ยว, ที่, ชั้น, น้ำ
  const hasDoubleTop = /[\u0E31\u0E34-\u0E37\u0E47\u0E4D][\u0E48-\u0E4C]/.test(s);
  // Single top vowel or tone mark e.g. บ้าน, ด่วน, ให้
  const hasSingleTop = /[\u0E31\u0E34-\u0E37\u0E47-\u0E4E]/.test(s);
  return { hasDoubleTop, hasSingleTop };
}

function drawSmartText(ctx, text, x, y, opts) {
  if (!text) return 0;
  const str = String(text).trim();
  if (!str) return 0;

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
    maxStretchX = 1.12,   // Gentle horizontal expansion cap so letters stay well-proportioned
    protectThaiMarks = true
  } = opts;

  const cssWeight = weightMode === 'ultra' ? '900' : (weightMode === 'heavy' ? '800' : '700');
  const strokeFactor = weightMode === 'ultra' ? 0.034 : (weightMode === 'heavy' ? 0.016 : 0);

  // Reserve vertical headroom when text contains tall Thai upper vowels + tone marks (กันวรรณยุกต์เกยกรอบ)
  const thaiProfile = getThaiHeadroomProfile(str);
  let effectiveMaxSize = maxSize;
  if (protectThaiMarks) {
    if (thaiProfile.hasDoubleTop) {
      effectiveMaxSize = Math.max(minSize, Math.round(maxSize * 0.86));
    } else if (thaiProfile.hasSingleTop) {
      effectiveMaxSize = Math.max(minSize, Math.round(maxSize * 0.93));
    }
  }

  let size = Math.min(baseSize, effectiveMaxSize);
  ctx.font = `${cssWeight} ${size}px ${fontFamily}`;
  let w = ctx.measureText(str).width;

  // 1. Scale UP if autoExpand is active and text is narrower than targetW
  if (autoExpand && w < targetW && size < effectiveMaxSize) {
    while (w < targetW && size < effectiveMaxSize) {
      size += 2;
      ctx.font = `${cssWeight} ${size}px ${fontFamily}`;
      w = ctx.measureText(str).width;
    }
  }

  // 2. Scale DOWN if text exceeds maximum safe width (maxW)
  while (w > maxW && size > minSize) {
    size -= 2;
    ctx.font = `${cssWeight} ${size}px ${fontFamily}`;
    w = ctx.measureText(str).width;
  }

  // 3. Apply gentle horizontal stretch (or condense if still wider than maxW at minSize)
  let scaleX = 1.0;
  if (w > maxW) {
    scaleX = Math.max(0.72, maxW / w);
  } else if (autoExpand && w > 0 && w < targetW * 0.92 && maxStretchX > 1.0) {
    scaleX = Math.min(maxStretchX, (targetW * 0.92) / w);
  }

  // 4. Downward optical offset when tall Thai tone marks are present so they never clip top borders/bars
  let yOffset = 0;
  if (protectThaiMarks && baseline === 'middle') {
    if (thaiProfile.hasDoubleTop) {
      yOffset = Math.round(size * 0.08);
    } else if (thaiProfile.hasSingleTop) {
      yOffset = Math.round(size * 0.04);
    }
  }

  ctx.save();
  ctx.textAlign = align;
  ctx.textBaseline = baseline;
  ctx.fillStyle = fillStyle;
  ctx.font = `${cssWeight} ${size}px ${fontFamily}`;

  ctx.translate(x, y + yOffset);
  if (Math.abs(scaleX - 1.0) > 0.005) {
    ctx.scale(scaleX, 1);
  }
  if (strokeFactor > 0) {
    ctx.strokeStyle = fillStyle;
    ctx.lineWidth = Math.max(1.5, size * strokeFactor);
    ctx.lineJoin = 'round';
    ctx.miterLimit = 2;
    ctx.strokeText(str, 0, 0);
  }
  ctx.fillText(str, 0, 0);
  ctx.restore();
  return size;
}

// ==============================================================================
// 📞 PAIRED DUAL PHONE RENDERER (Equal Weight + Dynamic Tracking for Narrow Digits like '1')
// Ensures both phone lines use the EXACT SAME font size & stroke weight while
// aligning to the exact same total width via inter-character letter-spacing.
// ==============================================================================
function drawPairedPhones(ctx, phoneA, phoneB, centerX, yA, yB, opts = {}) {
  const {
    targetW = 1720,
    maxW = 1820,
    baseSize = 220,
    maxSize = 255,
    minSize = 130,
    fillStyle = '#1F2937',
    fontFamily = '"Kanit", "RSU", "Tahoma", sans-serif',
    autoExpand = true,
    weightMode = 'heavy'
  } = opts;

  const cssWeight = weightMode === 'ultra' ? '900' : (weightMode === 'heavy' ? '800' : '700');
  const strokeFactor = weightMode === 'ultra' ? 0.034 : (weightMode === 'heavy' ? 0.016 : 0);

  const strA = String(phoneA || '').trim();
  const strB = String(phoneB || '').trim();

  // Measure both phones at the same fontSize so stroke thickness & height are 100% identical
  let size = baseSize;
  ctx.font = `${cssWeight} ${size}px ${fontFamily}`;
  let wA = ctx.measureText(strA).width;
  let wB = ctx.measureText(strB).width;
  let maxNaturalW = Math.max(wA, wB);

  // 1. Scale UP shared fontSize based on the wider phone number
  if (autoExpand && maxNaturalW > 0 && maxNaturalW < targetW && size < maxSize) {
    while (maxNaturalW < targetW && size < maxSize) {
      size += 2;
      ctx.font = `${cssWeight} ${size}px ${fontFamily}`;
      wA = ctx.measureText(strA).width;
      wB = ctx.measureText(strB).width;
      maxNaturalW = Math.max(wA, wB);
    }
  }

  // 2. Scale DOWN shared fontSize if the wider phone exceeds maxW
  while (maxNaturalW > maxW && size > minSize) {
    size -= 2;
    ctx.font = `${cssWeight} ${size}px ${fontFamily}`;
    wA = ctx.measureText(strA).width;
    wB = ctx.measureText(strB).width;
    maxNaturalW = Math.max(wA, wB);
  }

  // 3. Determine unified target span width (so narrow digits like '1' expand via tracking, not distortion)
  const unifiedSpanW = autoExpand
    ? Math.min(maxW, Math.max(maxNaturalW, Math.min(targetW, maxNaturalW * 1.10)))
    : Math.min(maxW, maxNaturalW);

  const renderTrackedPhone = (str, yPos, naturalW) => {
    if (!str) return;
    const chars = Array.from(str);
    const gaps = Math.max(1, chars.length - 1);
    const extraW = Math.max(0, unifiedSpanW - naturalW);
    const maxTrackPerGap = size * 0.15; // Cap tracking so digits remain cohesive
    const tracking = Math.min(maxTrackPerGap, extraW / gaps);
    const totalLineW = naturalW + tracking * gaps;

    // Gentle shared horizontal scale only if unifiedSpanW still needs a tiny nudge
    const scaleX = totalLineW > maxW ? (maxW / totalLineW) : 1.0;

    ctx.save();
    ctx.translate(centerX, yPos);
    if (Math.abs(scaleX - 1.0) > 0.005) {
      ctx.scale(scaleX, 1);
    }
    ctx.font = `${cssWeight} ${size}px ${fontFamily}`;
    ctx.fillStyle = fillStyle;
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';

    if (strokeFactor > 0) {
      ctx.strokeStyle = fillStyle;
      ctx.lineWidth = Math.max(1.5, size * strokeFactor);
      ctx.lineJoin = 'round';
      ctx.miterLimit = 2;
    }

    let cursorX = -totalLineW / 2;
    for (let i = 0; i < chars.length; i++) {
      const ch = chars[i];
      if (strokeFactor > 0) {
        ctx.strokeText(ch, cursorX, 0);
      }
      ctx.fillText(ch, cursorX, 0);
      cursorX += ctx.measureText(ch).width + tracking;
    }
    ctx.restore();
  };

  renderTrackedPhone(strA, yA, wA);
  renderTrackedPhone(strB, yB, wB);
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

  // 1. Red Header Block 'Horsale' (Height = 580px: Y=30..610)
  const headerHeight = 580;
  ctx.fillStyle = '#C8102E';
  ctx.fillRect(30, 30, W - 60, headerHeight);

  // ⭐ 1.1 Job_Discription (www.siwasup.com ซื้อ ขาย บ้าน ที่ดิน ทำการตลาดฟรี @siwasup)
  // Moved inside the bottom of the Red Header Box in crisp White (#FFFFFF)
  const hasSubtitle = subtitle && String(subtitle).trim() !== '';
  if (hasSubtitle) {
    drawSmartText(ctx, subtitle, W / 2, 30 + headerHeight - 55, {
      targetW: 1680,
      maxW: 1820,
      baseSize: 46,
      maxSize: 54,
      minSize: 28,
      fillStyle: '#FFFFFF',
      autoExpand,
      weightMode: weightMode === 'ultra' ? 'heavy' : 'normal',
      maxStretchX: 1.06
    });
  }

  // ⭐ 1.2 Headline Text inside upper portion of Red Header Box (Y=30..500)
  // Works seamlessly whether the user selects a 1-line or 2-line headline!
  const maxHeadW = W - 150;    // 1850px hard limit
  const targetHeadW = W - 240; // 1760px target fill width
  const headZoneBottom = hasSubtitle ? (30 + headerHeight - 110) : (30 + headerHeight - 20);
  const headZoneMidY = Math.round((30 + headZoneBottom) / 2);

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
    // 2-line layout (e.g. 'บ้านหลุดจำนอง / NPA') positioned cleanly above the white www.siwasup.com line
    const lineGap = 195;
    drawSmartText(ctx, headLines[0], W / 2, headZoneMidY - lineGap / 2, {
      targetW: targetHeadW * 0.94,
      maxW: maxHeadW,
      baseSize: 180,
      maxSize: 205,
      minSize: 90,
      fillStyle: '#FFFFFF',
      autoExpand,
      weightMode,
      maxStretchX: 1.12
    });
    drawSmartText(ctx, headLines[1], W / 2, headZoneMidY + lineGap / 2, {
      targetW: targetHeadW * 0.72,
      maxW: maxHeadW,
      baseSize: 175,
      maxSize: 200,
      minSize: 90,
      fillStyle: '#FFFFFF',
      autoExpand,
      weightMode,
      maxStretchX: 1.14
    });
  } else {
    // 1-line layout (e.g. 'ขายด่วน', 'ขาย / ให้เช่า', 'ขายบ้านรีโนเวท') with Thai tone-mark headroom protection
    drawSmartText(ctx, headLines[0], W / 2, headZoneMidY, {
      targetW: targetHeadW,
      maxW: maxHeadW,
      baseSize: 280,
      maxSize: 345,
      minSize: 120,
      fillStyle: '#FFFFFF',
      autoExpand,
      weightMode,
      maxStretchX: 1.14
    });
  }

  // ⭐ 1.3 Signature Satin Gold Accent Bar (แถบสีทองคั่นใต้บล็อกแดงตาม Ads200x160.ait)
  const goldBarH = 26;
  const goldBarY = 30 + headerHeight; // 610
  ctx.fillStyle = '#C2A460'; // Satin Gold CI
  ctx.fillRect(30, goldBarY, W - 60, goldBarH);

  // 2. Middle White Body (Y=636..1265 -> Generous vertical breathing room!)
  const bodyTop = goldBarY + goldBarH; // 636

  // Phone Numbers - Equal font weight & dynamic tracking for narrow '1' digits
  if (phoneB && phoneB.trim() !== '') {
    drawPairedPhones(ctx, phoneA, phoneB, W / 2, bodyTop + 145, bodyTop + 370, {
      targetW: 1740,
      maxW: 1840,
      baseSize: 220,
      maxSize: 255,
      minSize: 135,
      fillStyle: '#1F2937',
      autoExpand,
      weightMode
    });
  } else {
    // Single phone number: Massive centered hero number
    drawSmartText(ctx, phoneA, W / 2, bodyTop + 255, {
      targetW: 1760,
      maxW: 1850,
      baseSize: 255,
      maxSize: 300,
      minSize: 150,
      fillStyle: '#1F2937',
      autoExpand,
      weightMode,
      maxStretchX: 1.14
    });
  }

  // Ticker_AgentInfo: Red text line below phone numbers with airy gap above & below
  drawSmartText(ctx, agentInfo, W / 2, bodyTop + 535, {
    targetW: 1540,
    maxW: 1820,
    baseSize: 50,
    maxSize: 62,
    minSize: 28,
    fillStyle: '#C8102E',
    autoExpand,
    weightMode: weightMode === 'ultra' ? 'heavy' : 'normal',
    maxStretchX: 1.06
  });

  // 3. Bottom Footer Bar: Siwasup Logo + Services + QR Code (Larger & Perfectly Centered Group)
  const footerTop = 1265;
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
    targetW: textW * 0.94,
    maxW: textW,
    baseSize: 74,
    maxSize: 90,
    minSize: 48,
    fillStyle: '#C8102E',
    autoExpand,
    weightMode,
    maxStretchX: 1.10
  });

  drawSmartText(ctx, 'ให้เราช่วยขาย ง่ายกว่า โฆษณาฟรี มีบริการจัดสินเชื่อ', textCenterX, footerTop + 118, {
    targetW: textW * 0.95,
    maxW: textW,
    baseSize: 38,
    maxSize: 46,
    minSize: 28,
    fillStyle: '#1F2937',
    autoExpand,
    weightMode: 'normal',
    maxStretchX: 1.06
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

  // White text 'ขาย' (Balanced with generous red padding above 'Siwasup Assets')
  drawSmartText(ctx, 'ขาย', redBoxX + redBoxW / 2, 50 + redBoxH / 2 - 34, {
    targetW: redBoxW * 0.78,
    maxW: redBoxW - 90,
    baseSize: 285,
    maxSize: 330,
    minSize: 180,
    fillStyle: '#FFFFFF',
    autoExpand: true,
    weightMode,
    maxStretchX: 1.12
  });

  // Subtitle 'Siwasup Assets' (Right-aligned under 'ขาย' matching Ads43x49.ai)
  ctx.fillStyle = '#FFFFFF';
  ctx.font = '700 46px "Kanit", "RSU", "Tahoma", sans-serif';
  ctx.textAlign = 'right';
  ctx.textBaseline = 'middle';
  ctx.fillText('Siwasup Assets', redBoxX + redBoxW - 65, 50 + redBoxH - 42);

  // ⭐ Signature Satin Gold Accent Bar (แถบสีทองคั่นใต้ส่วนหัวตาม Ads43x49.ai)
  const goldBarY = 50 + redBoxH + 16; // 526
  const goldBarH = 26;                // Bottom of Gold Bar = 552
  ctx.fillStyle = '#C2A460'; // Satin Gold CI
  ctx.fillRect(50, goldBarY, W - 100, goldBarH);

  // Middle Area: Ticker_Asset + Ticker_Detail + Ticker_Price (2-Way Smart Auto-Fit + Airy Line Spacing)
  // Hard safety limit: 37 cm = 1480px on this 1720px canvas
  const maxContentW = Math.round(W * (37 / 43)); // 1480px

  // 1. Ticker_Asset (Gold font: บ้านเดี่ยว / คอนโด UBIO ริมถนน)
  // Positioned at Y=735 with Thai tone-mark clearance so ไม้เอก/สระอี never touches the Gold Bar (Y=552)
  drawSmartText(ctx, assetText, W / 2, 735, {
    targetW: 1260,
    maxW: maxContentW,
    baseSize: 148,
    maxSize: 180,
    minSize: 65,
    fillStyle: '#967C3E',
    autoExpand,
    weightMode,
    maxStretchX: 1.08
  });

  // 2. Ticker_Detail (Dark font: 2ทำเลทอง / 3 ห้องนอน ทำเลพุทธมณฑลสาย 2)
  // Positioned at Y=975 (240px gap below Asset)
  drawSmartText(ctx, detailText, W / 2, 975, {
    targetW: 1200,
    maxW: maxContentW,
    baseSize: 108,
    maxSize: 135,
    minSize: 48,
    fillStyle: '#1F2937',
    autoExpand,
    weightMode,
    maxStretchX: 1.06
  });

  // 3. Ticker_Price (Big Red font: ฿ 5,500,000)
  // Positioned at Y=1245 (270px gap below Detail, 235px gap above Red Ribbon at Y=1480)
  drawSmartText(ctx, priceText, W / 2, 1245, {
    targetW: 1340,
    maxW: maxContentW,
    baseSize: 215,
    maxSize: 255,
    minSize: 95,
    fillStyle: '#C8102E',
    autoExpand,
    weightMode,
    maxStretchX: 1.10
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

  // Phone Numbers on left of ribbon - Balanced padding inside the red ribbon
  const phoneText = phoneB && phoneB.trim() !== '' ? `📞 ${phoneA}   ${phoneB}` : `📞 ${phoneA}`;
  const availRibbonW = qrX - 115; // ~1265px available width
  drawSmartText(ctx, phoneText, 75 + availRibbonW / 2, ribbonY + ribbonH / 2, {
    targetW: availRibbonW * 0.90,
    maxW: availRibbonW - 20,
    baseSize: 64,
    maxSize: 80,
    minSize: 42,
    fillStyle: '#FFFFFF',
    autoExpand,
    weightMode,
    maxStretchX: 1.06
  });

  if (qrImg) {
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(qrX - 8, qrY - 8, qrSize + 16, qrSize + 16);
    ctx.lineWidth = 2.5;
    ctx.strokeStyle = '#D1D5DB';
    ctx.strokeRect(qrX - 8, qrY - 8, qrSize + 16, qrSize + 16);
    ctx.drawImage(qrImg, qrX, qrY, qrSize, qrSize);
  }

  // Slogan below ribbon - Clean breathing room below ribbon and above bottom border
  drawSmartText(ctx, 'รับฝากขาย รีโนเวท โฆษณาฟรี!', (50 + qrX) / 2 + 40, ribbonY + ribbonH + 125, {
    targetW: 1200,
    maxW: 1340,
    baseSize: 80,
    maxSize: 95,
    minSize: 54,
    fillStyle: '#C8102E',
    autoExpand,
    weightMode,
    maxStretchX: 1.08
  });

  // 4 Corner Eyelet Markers
  drawEyelets(ctx, W, H, 50, 12);
}

// ------------------------------------------------------------------------------
// [ARCHIVED] STYLE 3: HOMERUN MODERN VINYL (120x80, 150x80, 60x90)
// โค้ดแม่แบบป้ายสไตล์เดิม (Classic Homerun Vinyl) ถูกแยกสำรองไปเก็บไว้ที่:
// 📂 archive/legacy_vinyl_style3.js ตามนโยบาย Modular Architecture & Code Hygiene
// หากต้องการนำกลับมาใช้ ให้ดึงจากไฟล์ archive ดังกล่าว
// ------------------------------------------------------------------------------

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
