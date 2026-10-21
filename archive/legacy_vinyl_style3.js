/**
 * ==============================================================================
 * ARCHIVE / LEGACY BACKUP: STYLE 3 - HOMERUN MODERN VINYL
 * ==============================================================================
 * Project: Siwasup Co-Broker OS (siwasup-cobroker-os)
 * Original File: vinyl_generator.js (Lines 792 - 956)
 * Archived Date: 17 ตุลาคม 2569
 * Purpose: แยกสำรองโค้ดแม่แบบป้ายสไตล์เดิม (Classic Homerun Vinyl 120x80, 150x80, 60x90)
 *          ออกจาก vinyl_generator.js ตามนโยบาย Modular Architecture & Code Hygiene
 *          เพื่อลดขนาดไฟล์หลักให้เบาลงและประหยัด Token ในการแก้ไข
 *
 * Usage/Restore: หากต้องการนำกลับมาใช้งาน ให้ import หรือ copy ฟังก์ชันนี้กลับไปที่
 *                vinyl_generator.js และผูกเข้ากับ renderVinylCanvas() ใน activeVinylPreset
 * ==============================================================================
 */

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
