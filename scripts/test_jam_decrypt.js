const https = require('https');
const crypto = require('crypto');

const KEY = Buffer.from('QWT9g38M6fwBzJcbCjRjIBqn97UBm1Cf', 'utf8');

const options = {
  hostname: 'www.jjpropertythai.com',
  path: '/api/proxy/v1/assets',
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
    const json = JSON.parse(body);
    const parts = json._encrypted.split(':');
    const iv = Buffer.from(parts[0], 'hex');
    const tag = Buffer.from(parts[1], 'hex');
    const ciphertext = Buffer.from(parts[2], 'hex');

    const decipher = crypto.createDecipheriv('aes-256-gcm', KEY, iv);
    decipher.setAuthTag(tag);
    let decrypted = decipher.update(ciphertext, null, 'utf8');
    decrypted += decipher.final('utf8');

    const data = JSON.parse(decrypted);
    console.log('JAM Total Count in system:', data.count);
    console.log('Keys of asset object:', Object.keys(data.data[0]));
    console.log('Sample Asset Full Details:');
    console.log(JSON.stringify(data.data[0], null, 2));
  });
});
req.end();
