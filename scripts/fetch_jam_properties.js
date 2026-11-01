const https = require('https');
const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

const KEY = Buffer.from('QWT9g38M6fwBzJcbCjRjIBqn97UBm1Cf', 'utf8');
const OUTPUT_FILE = path.join(__dirname, '..', 'data', 'jam_properties_golden_zone.json');

function fetchAndDecrypt(urlPath) {
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'www.jjpropertythai.com',
      path: urlPath,
      method: 'GET',
      headers: {
        'User-Agent': 'Mozilla/5.0',
        'Accept': 'application/json',
        'Origin': 'https://www.jjpropertythai.com',
        'Referer': 'https://www.jjpropertythai.com/'
      }
    };

    const req = https.request(options, (res) => {
      let body = '';
      res.on('data', chunk => body += chunk);
      res.on('end', () => {
        try {
          const json = JSON.parse(body);
          if (!json._encrypted) {
            return resolve(json);
          }
          const parts = json._encrypted.split(':');
          const iv = Buffer.from(parts[0], 'hex');
          const tag = Buffer.from(parts[1], 'hex');
          const ciphertext = Buffer.from(parts[2], 'hex');

          const decipher = crypto.createDecipheriv('aes-256-gcm', KEY, iv);
          decipher.setAuthTag(tag);
          let decrypted = decipher.update(ciphertext, null, 'utf8');
          decrypted += decipher.final('utf8');

          resolve(JSON.parse(decrypted));
        } catch (err) {
          reject(err);
        }
      });
    });

    req.on('error', reject);
    req.end();
  });
}

async function run() {
  console.log('=== STARTING JAM (JMT/BAANBAAN) CRAWLER ===');
  try {
    // Test pagination and batch fetch
    const res = await fetchAndDecrypt('/api/proxy/v1/assets?page=1&limit=50');
    console.log(`[STATUS] Total JAM Assets: ${res.count}`);
    const items = res.data || [];
    console.log(`Fetched initial batch: ${items.length} items`);

    const normalizedMap = {};
    for (const p of items) {
      const pid = p.Asset_ID || p.Asset_No;
      if (!pid) continue;

      const images = [];
      if (p.Images_Main_Web) images.push(p.Images_Main_Web);
      if (Array.isArray(p.images)) {
        for (const img of p.images) {
          if (img.Part_File && !images.includes(img.Part_File)) {
            images.push(img.Part_File);
          }
        }
      }

      const normalized = {
        id: `JAM-${pid}`,
        source: 'JAM',
        source_code: p.Borr_Code || p.Asset_No,
        title: p.Project_TH || p.TitleAds_TH || `ทรัพย์ JAM ${p.PROVINCE_NAME || ''}`,
        property_type: p.Type_Asset_TH || 'บ้าน',
        price: parseFloat(p.Selling) || 0,
        discount_price: parseFloat(p.Discount) || 0,
        province: p.PROVINCE_NAME,
        district: p.AMPHUR_NAME,
        subdistrict: p.DISTRICT_NAME,
        address: p.aAddress,
        latitude: p.Lat ? parseFloat(p.Lat) : null,
        longitude: p.Lon ? parseFloat(p.Lon) : null,
        bedrooms: p.Bedroom || null,
        bathrooms: p.Bathroom || null,
        livingrooms: p.Livingroom || null,
        area_sqw: p.Wah || null,
        area_sqm: p.Meter || null,
        images: images,
        commission_rate: '3.0%',
        url: `https://www.jjpropertythai.com/Detailasset?id=${pid}`
      };

      normalizedMap[normalized.id] = normalized;
    }

    fs.writeFileSync(OUTPUT_FILE, JSON.stringify(normalizedMap, null, 2), 'utf8');
    console.log(`[OK] Saved ${Object.keys(normalizedMap).length} normalized JAM properties to ${OUTPUT_FILE}`);
  } catch (err) {
    console.error('[ERR]', err);
  }
}

run();
