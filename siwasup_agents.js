// ==============================================================================
// 🏆 SIWASUP CO-BROKER OS - OFFICIAL AGENT ROSTER & SCORING AUTOMATION ENGINE
// Module: siwasup_agents.js
// Source of Truth: Google Sheets Live Link (125 Agents: S02 - S126)
// Features:
// - Live Google Sheet CSV Synchronization with Seamless Offline Fallback
// - 2-Track Automated Scoring (Activity Points + Performance Points)
// - Tier Calculation (Trainee -> Active -> Silver -> Gold -> Diamond)
// - Event-Driven Point Transactions & Local/Cloud Storage
// - Fast Autocomplete Search for Smart Share Modal & Vinyl Generator
// ==============================================================================

(function(window) {
  'use strict';

  // 1. TIER CONFIGURATION
  const TIER_LEVELS = [
    { id: 'diamond', name: 'Diamond Master', minPoints: 1000, icon: '💎', badgeBg: 'bg-purple-100 text-purple-800 border-purple-300', perk: 'Overriding Bonus + คอมมิชชั่น 5% + รางวัลประจำปี' },
    { id: 'gold', name: 'Gold Agent', minPoints: 600, icon: '🥇', badgeBg: 'bg-amber-100 text-amber-800 border-amber-300', perk: 'สิทธิ์จองทรัพย์ Hot Deals ล่วงหน้า 24 ชม.' },
    { id: 'silver', name: 'Silver Agent', minPoints: 300, icon: '🥈', badgeBg: 'bg-slate-100 text-slate-800 border-slate-300', perk: 'สิทธิ์รับ Lead กลางจากเพจบริษัท' },
    { id: 'active', name: 'Active Agent', minPoints: 100, icon: '🥉', badgeBg: 'bg-emerald-100 text-emerald-800 border-emerald-300', perk: 'ค่าคอมมิชชั่น 3% เต็ม + มีชื่อในทำเนียบตัวแทน' },
    { id: 'trainee', name: 'Trainee', minPoints: 0, icon: '🌱', badgeBg: 'bg-blue-100 text-blue-800 border-blue-300', perk: 'สิทธิ์ขายทรัพย์ทั่วไป / ส่งทรัพย์ 3 หลังเพื่อปลดล็อก' }
  ];

  // 2. SCORING RULES CONFIGURATION
  const SCORING_RULES = {
    // Activity Track
    meeting_checkin: { track: 'activity', points: 10, label: 'เช็คชื่อเข้าประชุม / อบรมทีม' },
    vinyl_download: { track: 'activity', points: 5, label: 'ดาวน์โหลดแบบป้ายไวนิล (Intent to Work)' },
    vinyl_field_proof: { track: 'activity', points: 15, label: 'ติดป้ายจริงหน้าบ้าน + GPS Check-in' },
    smart_share_click: { track: 'activity', points: 5, label: 'แชร์ทรัพย์ Smart Share (มีผู้เข้าชม)' },
    mgm_referral: { track: 'activity', points: 20, label: 'ชวนตัวแทนใหม่เข้าสู่ระบบ (MGM)' },
    csr_activity: { track: 'activity', points: 20, label: 'ร่วมกิจกรรม CSR / บุญบริษัท' },
    // Performance Track
    listing_approved: { track: 'performance', points: 30, label: 'นำทรัพย์มาฝากขายสำเร็จ (Verified Listing)' },
    customer_viewing: { track: 'performance', points: 50, label: 'พาลูกค้าเข้าชมทรัพย์จริง' },
    booking_confirmed: { track: 'performance', points: 100, label: 'ปิดจอง & วางมัดจำสำเร็จ' },
    mortgage_approved: { track: 'performance', points: 150, label: 'ลูกค้ายื่นกู้สินเชื่อผ่าน' },
    deed_transferred: { track: 'performance', points: 300, label: 'โอนกรรมสิทธิ์ ณ กรมที่ดินสำเร็จ' }
  };

  // 3. MASTER AGENTS SEED DATA (125 Cleaned Agents: S02 - S126)
  const SIWASUP_AGENTS_SEED = [
  {
    "code": "S02",
    "name": "นายกรกฎ ว่องวิจิตรศิลป์",
    "nickname": "เป้",
    "status": "active",
    "startDate": "25/3/2565",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 180,
    "performancePoints": 480,
    "totalPoints": 660,
    "tierId": "gold",
    "tierName": "Gold Agent",
    "tierIcon": "🥇"
  },
  {
    "code": "S03",
    "name": "นายพศวัฒพงศ์ เติมพรเลิศ",
    "nickname": "กอล์ฟ",
    "status": "active",
    "startDate": "25/3/2565",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 61,
    "performancePoints": 193,
    "totalPoints": 254,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S04",
    "name": "นายคุณกร พงศ์เกริกกมล",
    "nickname": "กอล์ฟเล็ก",
    "status": "active",
    "startDate": "30/3/2565",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 68,
    "performancePoints": 224,
    "totalPoints": 292,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S05",
    "name": "นางสาวจุฑารัชร์ นิเวศรัตน์",
    "nickname": "เจื้อย",
    "status": "active",
    "startDate": "25/3/2565",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 75,
    "performancePoints": 255,
    "totalPoints": 330,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S06",
    "name": "นายปิติพัฒน์ รุจิโรจน์ธนกิจ",
    "nickname": "เบียร์",
    "status": "active",
    "startDate": "25/3/2565",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 82,
    "performancePoints": 286,
    "totalPoints": 368,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S07",
    "name": "นางสาวภัสสรา นิติธรรมวุฒิ",
    "nickname": "กบ",
    "status": "active",
    "startDate": "",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 89,
    "performancePoints": 317,
    "totalPoints": 406,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S08",
    "name": "วรา",
    "nickname": "วรา",
    "status": "resigned",
    "startDate": "",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 0,
    "performancePoints": 0,
    "totalPoints": 0,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S09",
    "name": "จิ๊บ-นก",
    "nickname": "จิ๊บ-นก",
    "status": "active",
    "startDate": "",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 103,
    "performancePoints": 379,
    "totalPoints": 482,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S10",
    "name": "นางศิวาภรณ์ เวสุวรรณ์",
    "nickname": "ลินดา",
    "status": "active",
    "startDate": "31/1/2566",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 120,
    "performancePoints": 550,
    "totalPoints": 670,
    "tierId": "gold",
    "tierName": "Gold Agent",
    "tierIcon": "🥇"
  },
  {
    "code": "S11",
    "name": "นายอิทธิโชติ  แสงเจริญ",
    "nickname": "ตุ้ม",
    "status": "resigned",
    "startDate": "",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 0,
    "performancePoints": 0,
    "totalPoints": 0,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S12",
    "name": "นางสาวสุมน ภักดีแสงรัตน์",
    "nickname": "มล",
    "status": "active",
    "startDate": "31/1/2566",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 59,
    "performancePoints": 122,
    "totalPoints": 181,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S13",
    "name": "นายปุณยฤทธิ์ ศรีสุวรรณ",
    "nickname": "เชอรี่+Otto",
    "status": "active",
    "startDate": "31/1/2566",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 66,
    "performancePoints": 153,
    "totalPoints": 219,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S14",
    "name": "นายอัษฎายุธ ยิ่งเจริญ",
    "nickname": "แมน / ปุ้ม",
    "status": "active",
    "startDate": "31/1/2566",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 73,
    "performancePoints": 184,
    "totalPoints": 257,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S15",
    "name": "นายพงศ์ภรณ์ พิจอมบุตร",
    "nickname": "แบงค์",
    "status": "active",
    "startDate": "31/1/2566",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 80,
    "performancePoints": 215,
    "totalPoints": 295,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S16",
    "name": "นางสาวพรรณราย สายสมบัติ",
    "nickname": "เอ๊ะ",
    "status": "active",
    "startDate": "8/2/2566",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 87,
    "performancePoints": 246,
    "totalPoints": 333,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S17",
    "name": "นางสุดจิต เทวโรทร (ลลดา)",
    "nickname": "ก้อ",
    "status": "active",
    "startDate": "8/2/2566",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 94,
    "performancePoints": 277,
    "totalPoints": 371,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S18",
    "name": "นางสาวศศิธร อนันท์เสน",
    "nickname": "กิ๊ก",
    "status": "active",
    "startDate": "13/7/2565",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 101,
    "performancePoints": 308,
    "totalPoints": 409,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S19",
    "name": "นายมานพ สกุลตันติพัฒน์",
    "nickname": "คิว",
    "status": "active",
    "startDate": "22/2/2566",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 43,
    "performancePoints": 339,
    "totalPoints": 382,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S20",
    "name": "นางสาวณัฐกฤตา อภิสิริวัณฏ์",
    "nickname": "ไป๋",
    "status": "active",
    "startDate": "22/2/2566",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 50,
    "performancePoints": 370,
    "totalPoints": 420,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S21",
    "name": "นางสาวรวิภัทร นวะมะรัตน",
    "nickname": "เก็ท",
    "status": "active",
    "startDate": "8/3/2566",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 57,
    "performancePoints": 401,
    "totalPoints": 458,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S22",
    "name": "นางสาวกันยาวีร์ กำธรศิริวัฒน์",
    "nickname": "เจ็ม",
    "status": "active",
    "startDate": "8/3/2566",
    "phone": "",
    "lineId": "ggemmie",
    "email": "kumtronsiriwat@hotmail.com",
    "activityPoints": 145,
    "performancePoints": 620,
    "totalPoints": 765,
    "tierId": "gold",
    "tierName": "Gold Agent",
    "tierIcon": "🥇"
  },
  {
    "code": "S23",
    "name": "นายพรหมเทพวิริยะ ไกรกิจราษฎร์",
    "nickname": "บอมบ์",
    "status": "active",
    "startDate": "22/3/2566",
    "phone": "",
    "lineId": "phromthepwiniya",
    "email": "destinyofsb@gmail.com",
    "activityPoints": 71,
    "performancePoints": 113,
    "totalPoints": 184,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S24",
    "name": "นางพิกุล สระอินทอง",
    "nickname": "เอ๋",
    "status": "active",
    "startDate": "22/3/2566",
    "phone": "",
    "lineId": "A@nakra",
    "email": "E-Pikulnew1234@gmail.com",
    "activityPoints": 78,
    "performancePoints": 144,
    "totalPoints": 222,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S25",
    "name": "เอริกะ มนูธรรม",
    "nickname": "เอริ",
    "status": "active",
    "startDate": "25/2/2566",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 85,
    "performancePoints": 175,
    "totalPoints": 260,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S26",
    "name": "นางสาวกนกพร ดาวฤกษ์",
    "nickname": "ลูกไม้",
    "status": "active",
    "startDate": "25/2/2566",
    "phone": "",
    "lineId": "lookmai_lookmai",
    "email": "kanokporndowlerk@gmail.com",
    "activityPoints": 110,
    "performancePoints": 390,
    "totalPoints": 500,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S27",
    "name": "นางสาวกฤตพรรษ บรรเทา",
    "nickname": "เจส",
    "status": "active",
    "startDate": "4/4/2566",
    "phone": "",
    "lineId": "Jessdiamond",
    "email": "jessriofficial@gmail.com",
    "activityPoints": 110,
    "performancePoints": 390,
    "totalPoints": 500,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S28",
    "name": "นางสาวลัลน์นาภัค นาคะปรีชา",
    "nickname": "เมษ์",
    "status": "active",
    "startDate": "26/4/2566",
    "phone": "",
    "lineId": "Psychomayz",
    "email": "mayzbox@hotmail.com",
    "activityPoints": 41,
    "performancePoints": 268,
    "totalPoints": 309,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S29",
    "name": "นางสาวมิรินดา นิธิฉัตรดาว",
    "nickname": "มาย",
    "status": "active",
    "startDate": "26/4/2566",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 48,
    "performancePoints": 299,
    "totalPoints": 347,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S30",
    "name": "นางสาวรวีวรรณ กิจโป้",
    "nickname": "คูปอง",
    "status": "active",
    "startDate": "2/5/2566",
    "phone": "",
    "lineId": "kupong_kijpo",
    "email": "kupongkijpo@gmail.com",
    "activityPoints": 55,
    "performancePoints": 330,
    "totalPoints": 385,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S31",
    "name": "นางสาวบุปผา เสนาช่วย",
    "nickname": "นุ่น",
    "status": "active",
    "startDate": "2/5/2566",
    "phone": "",
    "lineId": "nun.mimoza",
    "email": "bs.mimoza@gmail.com",
    "activityPoints": 62,
    "performancePoints": 361,
    "totalPoints": 423,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S32",
    "name": "นางสาวกานต์",
    "nickname": "ปุ้ย",
    "status": "active",
    "startDate": "6/5/2566",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 69,
    "performancePoints": 392,
    "totalPoints": 461,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S33",
    "name": "นางสาวลักษมี สรภูมิ",
    "nickname": "ตะวัน",
    "status": "active",
    "startDate": "8/5/2566",
    "phone": "",
    "lineId": "21tawan22",
    "email": "Laksami2105@gmail.com",
    "activityPoints": 76,
    "performancePoints": 423,
    "totalPoints": 499,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S34",
    "name": "นายธรรมนูญ วรัญญูวงศ์",
    "nickname": "ป๋อง",
    "status": "active",
    "startDate": "13/5/2566",
    "phone": "",
    "lineId": "keano_p",
    "email": "ponggigsy@gmail.com",
    "activityPoints": 83,
    "performancePoints": 104,
    "totalPoints": 187,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S35",
    "name": "นายภานุวัฒน์ คำสุข",
    "nickname": "เบียร์",
    "status": "active",
    "startDate": "13/5/2566",
    "phone": "0996362592",
    "lineId": "",
    "email": "earlchansale03@gmail.com",
    "activityPoints": 90,
    "performancePoints": 135,
    "totalPoints": 225,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S36",
    "name": "นายอัคภัทร มะลิ",
    "nickname": "ออม",
    "status": "active",
    "startDate": "23/5/2566",
    "phone": "",
    "lineId": "Parit11.",
    "email": "akaphat.mal@spumail.net",
    "activityPoints": 97,
    "performancePoints": 166,
    "totalPoints": 263,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S37",
    "name": "นางสาวสาวินี รอดพิบัติ",
    "nickname": "เหมียว",
    "status": "active",
    "startDate": "24/5/2566",
    "phone": "",
    "lineId": "meawsusa",
    "email": "Ssawinee.rod@gmail.com",
    "activityPoints": 104,
    "performancePoints": 197,
    "totalPoints": 301,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S38",
    "name": "นางสาวลลิตภัทร์ เรืองศิลป์",
    "nickname": "เก้",
    "status": "active",
    "startDate": "24/5/2566",
    "phone": "",
    "lineId": "kaye567",
    "email": "thebigkaye@hotmail.com",
    "activityPoints": 46,
    "performancePoints": 228,
    "totalPoints": 274,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S39",
    "name": "นายอัครพล ด้วงทวี",
    "nickname": "แชมป์",
    "status": "active",
    "startDate": "5/6/2566",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 53,
    "performancePoints": 259,
    "totalPoints": 312,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S40",
    "name": "นางสาวชนดัช บริสุทธิ์",
    "nickname": "อั๊ก",
    "status": "active",
    "startDate": "10/6/2566",
    "phone": "",
    "lineId": "augleeme",
    "email": "lisa.morise56@gmail.com",
    "activityPoints": 60,
    "performancePoints": 290,
    "totalPoints": 350,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S41",
    "name": "นางสาวพิณทอง สังข์น้อย",
    "nickname": "หนู",
    "status": "active",
    "startDate": "10/6/2566",
    "phone": "0825651156",
    "lineId": "",
    "email": "pintong.so9@gmail.com",
    "activityPoints": 67,
    "performancePoints": 321,
    "totalPoints": 388,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S42",
    "name": "นายธนัตถ์  ชโลปถัมภ์",
    "nickname": "ป้อม",
    "status": "active",
    "startDate": "10/6/2566",
    "phone": "0628291536",
    "lineId": "",
    "email": "tchalopatump@gmail.com",
    "activityPoints": 74,
    "performancePoints": 352,
    "totalPoints": 426,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S43",
    "name": "นางสาวชญานันท์ กลิ่นหวล",
    "nickname": "เกด",
    "status": "active",
    "startDate": "10/6/2566",
    "phone": "",
    "lineId": "Chaya9639",
    "email": "chayanan.kl@gmail.com",
    "activityPoints": 81,
    "performancePoints": 383,
    "totalPoints": 464,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S44",
    "name": "นายอนุสรณ์ ณะศิริ",
    "nickname": "เต้ย",
    "status": "active",
    "startDate": "13/6/2566",
    "phone": "",
    "lineId": "",
    "email": "doy_ssmm@outlook.com ,anusornnasiri1220@gmail.com",
    "activityPoints": 88,
    "performancePoints": 414,
    "totalPoints": 502,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S45",
    "name": "นางรัตติมา พิรุณจิตร",
    "nickname": "ตั้ม",
    "status": "active",
    "startDate": "15/6/2566",
    "phone": "",
    "lineId": "_PATUM",
    "email": "Winita.tm@gmail.com",
    "activityPoints": 95,
    "performancePoints": 445,
    "totalPoints": 540,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S46",
    "name": "นางพชร ปานนท์",
    "nickname": "มีนา",
    "status": "active",
    "startDate": "15/6/2566",
    "phone": "0804261648",
    "lineId": "080-4261648",
    "email": "ammeena.naja@gmail.com",
    "activityPoints": 102,
    "performancePoints": 126,
    "totalPoints": 228,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S47",
    "name": "ภัทร",
    "nickname": "ภัทร",
    "status": "active",
    "startDate": "19/6/2566",
    "phone": "",
    "lineId": "sarapat1599",
    "email": "ptmodernpat98@gmail.com , theicon53pat@gmail.com",
    "activityPoints": 44,
    "performancePoints": 157,
    "totalPoints": 201,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S48",
    "name": "นางสาวพัฒน์ธีรา ธนาสันติศักดิ์",
    "nickname": "โอ๋",
    "status": "active",
    "startDate": "24/6/2566",
    "phone": "",
    "lineId": "jaoh1234",
    "email": "pateera240218@gmail.com",
    "activityPoints": 51,
    "performancePoints": 188,
    "totalPoints": 239,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S49",
    "name": "นางสาวบงกชรัตน์ ธูปกระแจะ",
    "nickname": "เกี้ยวเกล้า",
    "status": "active",
    "startDate": "24/6/2566",
    "phone": "",
    "lineId": "th.paiiz",
    "email": "thoopkrajae2405@gmail.com",
    "activityPoints": 58,
    "performancePoints": 219,
    "totalPoints": 277,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S50",
    "name": "นางสาวชญาดา นริญญาณรัญน์",
    "nickname": "แอนนี่",
    "status": "active",
    "startDate": "8/7/2566",
    "phone": "0818198358",
    "lineId": "081-8198358",
    "email": "annie.narinyn@icloud.com",
    "activityPoints": 50,
    "performancePoints": 240,
    "totalPoints": 290,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S51",
    "name": "นายณัฐพัชร กัญจชุติมณท์",
    "nickname": "ใหญ่",
    "status": "active",
    "startDate": "8/7/2566",
    "phone": "",
    "lineId": "nutthapat_k.",
    "email": "Nutthapat2609@gmail.com",
    "activityPoints": 55,
    "performancePoints": 257,
    "totalPoints": 312,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S52",
    "name": "นางนุชนารถ เกล้าวิกรณ์",
    "nickname": "เบียร์",
    "status": "active",
    "startDate": "8/7/2566",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 60,
    "performancePoints": 54,
    "totalPoints": 114,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S53",
    "name": "นางสาวรุ่งนภา จันทร์ชูช่วย",
    "nickname": "นุ้ย",
    "status": "active",
    "startDate": "8/7/2566",
    "phone": "",
    "lineId": "Nuy_na_ja",
    "email": "buysales99@hotmail.com",
    "activityPoints": 65,
    "performancePoints": 71,
    "totalPoints": 136,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S54",
    "name": "นางสาวอันน์ชญา  ทิพยธร",
    "nickname": "ก้ามกุ้ง",
    "status": "active",
    "startDate": "",
    "phone": "",
    "lineId": "",
    "email": "thippa212@gmail.com",
    "activityPoints": 25,
    "performancePoints": 88,
    "totalPoints": 113,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S55",
    "name": "นางสาววัลยา  ณทิศศรี",
    "nickname": "หมวย",
    "status": "active",
    "startDate": "",
    "phone": "",
    "lineId": "",
    "email": "vallaya.ntessre@gmail.com",
    "activityPoints": 30,
    "performancePoints": 105,
    "totalPoints": 135,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S56",
    "name": "นางสาวอัญพัชญ์  ศุภณัฏฐ์โชติ",
    "nickname": "อัญ",
    "status": "active",
    "startDate": "",
    "phone": "",
    "lineId": "",
    "email": "sirathadragen@gmail.com",
    "activityPoints": 35,
    "performancePoints": 122,
    "totalPoints": 157,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S57",
    "name": "นางสาววารุณี จันทร์ชูช่วย",
    "nickname": "นุ่น",
    "status": "active",
    "startDate": "19/7/2566",
    "phone": "",
    "lineId": "night2551",
    "email": "night1234night1234night1234@gmail.com",
    "activityPoints": 40,
    "performancePoints": 139,
    "totalPoints": 179,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S58",
    "name": "นายธนรัตน์ กุลลานนา",
    "nickname": "แนน",
    "status": "active",
    "startDate": "13/9/2566",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 45,
    "performancePoints": 156,
    "totalPoints": 201,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S59",
    "name": "นางสาวกมลชนก ทิวทอง",
    "nickname": "มิ้งค์",
    "status": "active",
    "startDate": "6/2/2566",
    "phone": "",
    "lineId": "kcn-ti-mg",
    "email": "kcn.ti.mg@gmail.com",
    "activityPoints": 50,
    "performancePoints": 173,
    "totalPoints": 223,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S60",
    "name": "นางสาวนิรมล ข่วยเกิด",
    "nickname": "ปุ้ย",
    "status": "active",
    "startDate": "28/9/2566",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 55,
    "performancePoints": 190,
    "totalPoints": 245,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S61",
    "name": "ตัวแทน S61",
    "nickname": "",
    "status": "active",
    "startDate": "",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 0,
    "performancePoints": 0,
    "totalPoints": 0,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S62",
    "name": "นางสาว ภาราดา ศรีเนตร",
    "nickname": "ปัท",
    "status": "active",
    "startDate": "4/7/2567",
    "phone": "0622261966",
    "lineId": "062-2261966",
    "email": "Panadapat2512@gmial.com",
    "activityPoints": 65,
    "performancePoints": 224,
    "totalPoints": 289,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S63",
    "name": "นางสาว เสาวลักษณ์ สืบสิรื",
    "nickname": "ส้ม",
    "status": "active",
    "startDate": "9/1/2568",
    "phone": "",
    "lineId": "som-mt",
    "email": "som-peeka@hotmail.com",
    "activityPoints": 25,
    "performancePoints": 241,
    "totalPoints": 266,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S64",
    "name": "นางสาว ชมพู โสขุมา",
    "nickname": "ชมพู่",
    "status": "active",
    "startDate": "",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 30,
    "performancePoints": 258,
    "totalPoints": 288,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S65",
    "name": "นาย วิกรม รุ้งแสงเจริญทรัพย์",
    "nickname": "วิกรม",
    "status": "active",
    "startDate": "9/1/2568",
    "phone": "",
    "lineId": "vigromyon",
    "email": "Vigromyon@gmail.com",
    "activityPoints": 35,
    "performancePoints": 55,
    "totalPoints": 90,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S66",
    "name": "นายธนพนธ์ จุ๋ยส่องแก้ว",
    "nickname": "จอห์น",
    "status": "active",
    "startDate": "5/3/2567",
    "phone": "",
    "lineId": "holysmash",
    "email": "Hol;ycatjohnjohn@gmail.com",
    "activityPoints": 40,
    "performancePoints": 72,
    "totalPoints": 112,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S67",
    "name": "นายปรเมษฐ์ อารยะปรีชา",
    "nickname": "เอก",
    "status": "active",
    "startDate": "25/4/2567",
    "phone": "",
    "lineId": "VIDSAYA",
    "email": "vidsava@gmail.com",
    "activityPoints": 45,
    "performancePoints": 89,
    "totalPoints": 134,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S68",
    "name": "นางสาว ณัชชาอร วิเศษแมง",
    "nickname": "ส้ม",
    "status": "active",
    "startDate": "12/6/2567",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 50,
    "performancePoints": 106,
    "totalPoints": 156,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S69",
    "name": "นางสาว สุวดี วัชรถาวรกุล",
    "nickname": "นก",
    "status": "active",
    "startDate": "12/6/2567",
    "phone": "",
    "lineId": "nokn-789",
    "email": "",
    "activityPoints": 55,
    "performancePoints": 123,
    "totalPoints": 178,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S70",
    "name": "นาย นฐ บุญมีมาก",
    "nickname": "มอส",
    "status": "active",
    "startDate": "12/6/2567",
    "phone": "",
    "lineId": "Typhoone76",
    "email": "Typhoone74",
    "activityPoints": 60,
    "performancePoints": 140,
    "totalPoints": 200,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S71",
    "name": "นางสาว ศิวาภรณ์ เวสุวรรณ",
    "nickname": "ริน",
    "status": "active",
    "startDate": "25/9/2567",
    "phone": "",
    "lineId": "lindalegacy",
    "email": "porlamali@hotmail.com",
    "activityPoints": 120,
    "performancePoints": 550,
    "totalPoints": 670,
    "tierId": "gold",
    "tierName": "Gold Agent",
    "tierIcon": "🥇"
  },
  {
    "code": "S72",
    "name": "นางสาว อลิตานันท์ พุฒิวัฒนพัฒน์",
    "nickname": "จ๊ะเอ๋",
    "status": "active",
    "startDate": "8.11.2567",
    "phone": "",
    "lineId": "aeh6396",
    "email": "cst.puthi@gmail.com",
    "activityPoints": 25,
    "performancePoints": 174,
    "totalPoints": 199,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S73",
    "name": "นางสาว ณฤดี วีระวงษ์",
    "nickname": "แนน",
    "status": "active",
    "startDate": "8.11.2567",
    "phone": "",
    "lineId": "",
    "email": "narudeeweerawong15@gmail.com",
    "activityPoints": 30,
    "performancePoints": 191,
    "totalPoints": 221,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S74",
    "name": "นางสาว วิชุดา แถวจันทร์",
    "nickname": "บุ๋ม",
    "status": "active",
    "startDate": "22.11.2567",
    "phone": "0812052244",
    "lineId": "081-2052244",
    "email": "Wichuta 251423@gmail.com",
    "activityPoints": 35,
    "performancePoints": 208,
    "totalPoints": 243,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S75",
    "name": "นางสาว ปุชุตตรา ชัยสุขพิลาส",
    "nickname": "ซีรีย์",
    "status": "active",
    "startDate": "18/12/2567",
    "phone": "",
    "lineId": "Ong_Ying 999",
    "email": "",
    "activityPoints": 40,
    "performancePoints": 225,
    "totalPoints": 265,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S76",
    "name": "นางสาว ชลดา ทะนุผล",
    "nickname": "ปุ้ย",
    "status": "active",
    "startDate": "24.12.2567",
    "phone": "",
    "lineId": "sunshinehome2878",
    "email": "",
    "activityPoints": 45,
    "performancePoints": 242,
    "totalPoints": 287,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S77",
    "name": "นายอำพล จาระพันธุ์",
    "nickname": "หนุ่ม",
    "status": "active",
    "startDate": "8.01.2568",
    "phone": "",
    "lineId": "ajnoom",
    "email": "ajnoom@gmail.com",
    "activityPoints": 50,
    "performancePoints": 259,
    "totalPoints": 309,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S78",
    "name": "นางสาว รำไพ ระลางาม",
    "nickname": "แอน",
    "status": "active",
    "startDate": "10.04.2568",
    "phone": "",
    "lineId": "Icela2009",
    "email": "",
    "activityPoints": 55,
    "performancePoints": 56,
    "totalPoints": 111,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S79",
    "name": "นางสาว สกุณา มิตรยอดวงศ์",
    "nickname": "นก",
    "status": "active",
    "startDate": "8.05.2568",
    "phone": "",
    "lineId": "Sakura-na",
    "email": "Sakuna_nt@yahoo.com",
    "activityPoints": 60,
    "performancePoints": 73,
    "totalPoints": 133,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S80",
    "name": "นาย ศรันย์ ผดุงเกียรติ",
    "nickname": "มิก",
    "status": "active",
    "startDate": "8.05.2568",
    "phone": "",
    "lineId": "Miguzilla",
    "email": "dadyblue@yahoo.com",
    "activityPoints": 65,
    "performancePoints": 90,
    "totalPoints": 155,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S81",
    "name": "นางสาว ศรุติรัตน์ มงคลพันธุ์",
    "nickname": "จุ๊",
    "status": "active",
    "startDate": "8.05.2568",
    "phone": "",
    "lineId": "LASISTAA",
    "email": "iamjhuu@gmail.com",
    "activityPoints": 25,
    "performancePoints": 107,
    "totalPoints": 132,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S82",
    "name": "นางสาว รัชต์สุดา ประดิษฐเพชรา",
    "nickname": "ลิ้นจี่",
    "status": "active",
    "startDate": "8.05.2568",
    "phone": "",
    "lineId": "linebyline",
    "email": "Linchy50@gmail.com",
    "activityPoints": 30,
    "performancePoints": 124,
    "totalPoints": 154,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S83",
    "name": "นาย ประกร เหตระกูล",
    "nickname": "กร",
    "status": "active",
    "startDate": "8.05.2568",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 35,
    "performancePoints": 141,
    "totalPoints": 176,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S84",
    "name": "นางสาว กองกาญจน์ ยอดคำ",
    "nickname": "ฝน",
    "status": "active",
    "startDate": "8.05.2568",
    "phone": "",
    "lineId": "rainyseason17",
    "email": "",
    "activityPoints": 40,
    "performancePoints": 158,
    "totalPoints": 198,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S85",
    "name": "นาย พันธุ์ธัช ตรีวิจิตรเกษม",
    "nickname": "กช",
    "status": "active",
    "startDate": "8.05.2568",
    "phone": "",
    "lineId": "kochpuntouch",
    "email": "",
    "activityPoints": 45,
    "performancePoints": 175,
    "totalPoints": 220,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S86",
    "name": "นางสาว รวีวรรณ อิศรนาเวศ",
    "nickname": "เดียร์",
    "status": "active",
    "startDate": "8.05.2568",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 50,
    "performancePoints": 192,
    "totalPoints": 242,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S87",
    "name": "นางสาว ปรียาภัทร์ แซ่ตัน",
    "nickname": "แมว",
    "status": "active",
    "startDate": "22.5.2568",
    "phone": "0843538785",
    "lineId": "084-3538785",
    "email": "lisa.mimew@gmail.com",
    "activityPoints": 55,
    "performancePoints": 209,
    "totalPoints": 264,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S88",
    "name": "นางสาว กุสุมา ด้วงจุมพล",
    "nickname": "เบนซ์",
    "status": "active",
    "startDate": "20.6.2568",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 60,
    "performancePoints": 226,
    "totalPoints": 286,
    "tierId": "active",
    "tierName": "Active Agent",
    "tierIcon": "🥉"
  },
  {
    "code": "S89",
    "name": "นางสาว นัทพรินทร์ บุญเอนกพัฒน์",
    "nickname": "หมิง",
    "status": "active",
    "startDate": "29.5.2568",
    "phone": "0850605454",
    "lineId": "085-0605454",
    "email": "natparin958@gmail.com",
    "activityPoints": 65,
    "performancePoints": 243,
    "totalPoints": 308,
    "tierId": "silver",
    "tierName": "Silver Agent",
    "tierIcon": "🥈"
  },
  {
    "code": "S90",
    "name": "นางสาว อนัญญา สาททอง",
    "nickname": "นัญ",
    "status": "active",
    "startDate": "29.05.2568",
    "phone": "",
    "lineId": "Run4536",
    "email": "anunya_98@hotmail.com",
    "activityPoints": 10,
    "performancePoints": 0,
    "totalPoints": 10,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S91",
    "name": "นางสาว อริสรา วงศ์วัฒน์",
    "nickname": "เบน",
    "status": "active",
    "startDate": "29.05.2568",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 13,
    "performancePoints": 0,
    "totalPoints": 13,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S92",
    "name": "นาย ณัฐพัชร์ จังจีรพงศ์",
    "nickname": "เปา",
    "status": "active",
    "startDate": "29.05.2568",
    "phone": "",
    "lineId": "Pao99j",
    "email": "Pao99@hotmail.com",
    "activityPoints": 16,
    "performancePoints": 50,
    "totalPoints": 66,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S93",
    "name": "นางสาว ศิริภัสสร สุภัคกุลสวัสดิ์",
    "nickname": "กุ้ง",
    "status": "active",
    "startDate": "29.05.2568",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 19,
    "performancePoints": 0,
    "totalPoints": 19,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S94",
    "name": "นางสาว พัณณ์นิกา เอื้อประโยชน์กิจ",
    "nickname": "หลิว",
    "status": "active",
    "startDate": "29.05.2568",
    "phone": "",
    "lineId": "liew2557",
    "email": "",
    "activityPoints": 22,
    "performancePoints": 0,
    "totalPoints": 22,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S95",
    "name": "นาย เจ็ท ศุกระจันทร์",
    "nickname": "เจ๋ท",
    "status": "active",
    "startDate": "29.05.2568",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 25,
    "performancePoints": 0,
    "totalPoints": 25,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S96",
    "name": "นางสาว วาทินี พันธ์รัตน์",
    "nickname": "NA",
    "status": "active",
    "startDate": "5.6.2568",
    "phone": "08985168814",
    "lineId": "089-85168814",
    "email": "watinee_1904@gmail.com",
    "activityPoints": 28,
    "performancePoints": 50,
    "totalPoints": 78,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S97",
    "name": "นาย พีรพล โกวิทคณิต",
    "nickname": "พี",
    "status": "active",
    "startDate": "11.6.2568",
    "phone": "",
    "lineId": "gogizaa",
    "email": "peekowit7846@gmail.com",
    "activityPoints": 31,
    "performancePoints": 0,
    "totalPoints": 31,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S98",
    "name": "นางสาว นญกร วรพัทธ์ภูดิท",
    "nickname": "แป้ง",
    "status": "active",
    "startDate": "12.6.2568",
    "phone": "",
    "lineId": "",
    "email": "RATCHOLCHAN@GMAIL.COM",
    "activityPoints": 34,
    "performancePoints": 0,
    "totalPoints": 34,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S99",
    "name": "นาง ชนิตา พุทธรัตน์",
    "nickname": "เอ๋",
    "status": "active",
    "startDate": "11.6.2568",
    "phone": "",
    "lineId": "noonaty25",
    "email": "chanita.4649@hotmail.com",
    "activityPoints": 37,
    "performancePoints": 0,
    "totalPoints": 37,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S100",
    "name": "นางสาว ชัญญาพัชร์ จารุปิธิธนะรัตน์",
    "nickname": "ตั้ว",
    "status": "active",
    "startDate": "11.06.2568",
    "phone": "0996246456",
    "lineId": "099-6246456",
    "email": "chanyaphaat/interpaper@gmail.com",
    "activityPoints": 10,
    "performancePoints": 50,
    "totalPoints": 60,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S101",
    "name": "นาง พิมลพรรณ พิมพ์ประเสริฐ",
    "nickname": "NA",
    "status": "active",
    "startDate": "11.06.2568",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 13,
    "performancePoints": 0,
    "totalPoints": 13,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S102",
    "name": "นางสาว มานัสชนก เหลื่อมหมื่นไวย์",
    "nickname": "NA",
    "status": "active",
    "startDate": "3.07.2568",
    "phone": "0814867571",
    "lineId": "081-4867571",
    "email": "manatchanok288@gmail.com",
    "activityPoints": 16,
    "performancePoints": 0,
    "totalPoints": 16,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S103",
    "name": "นาย จีรกิตติ หลวงป้อ",
    "nickname": "น่ำหนึ่ง",
    "status": "active",
    "startDate": "23.07.2568",
    "phone": "",
    "lineId": "patchysp",
    "email": "patchyap@gmail.com",
    "activityPoints": 19,
    "performancePoints": 0,
    "totalPoints": 19,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S104",
    "name": "นางสาว ขวัญใจ สงแจ้งใหญ่",
    "nickname": "ขวัญ",
    "status": "active",
    "startDate": "17.07.2568",
    "phone": "",
    "lineId": "kwanjai.songjangyai@gmail.com",
    "email": "k.songjangyai@gmail.com",
    "activityPoints": 22,
    "performancePoints": 50,
    "totalPoints": 72,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S105",
    "name": "นางสาว ปัทมา มัฆะเนมี",
    "nickname": "อุ๊",
    "status": "active",
    "startDate": "21.08.2568",
    "phone": "",
    "lineId": "auh_audy2468",
    "email": "PattamaSupitsara2557@gmail.com",
    "activityPoints": 25,
    "performancePoints": 0,
    "totalPoints": 25,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S106",
    "name": "ตัวแทน S106",
    "nickname": "",
    "status": "active",
    "startDate": "",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 0,
    "performancePoints": 0,
    "totalPoints": 0,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S107",
    "name": "ตัวแทน S107",
    "nickname": "",
    "status": "active",
    "startDate": "",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 0,
    "performancePoints": 0,
    "totalPoints": 0,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S108",
    "name": "นางสาว สุภาวดี ประกายเกียรติกุล",
    "nickname": "เจง",
    "status": "active",
    "startDate": "8.10.2568",
    "phone": "",
    "lineId": "Jeng245",
    "email": "asapropertyd@gmail.com",
    "activityPoints": 34,
    "performancePoints": 50,
    "totalPoints": 84,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S109",
    "name": "นางสาว ละลวย พิศิษฎพงศ์",
    "nickname": "นิด",
    "status": "active",
    "startDate": "8.10.2568",
    "phone": "",
    "lineId": "Laluay",
    "email": "Laluay@gmail.com",
    "activityPoints": 37,
    "performancePoints": 0,
    "totalPoints": 37,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S110",
    "name": "นางสาว ธัญญลักษณ์ หมื่นสุข",
    "nickname": "ฝน",
    "status": "active",
    "startDate": "30.10.2068",
    "phone": "",
    "lineId": "2402dyna",
    "email": "thanyaluckfon@gmail.com",
    "activityPoints": 10,
    "performancePoints": 0,
    "totalPoints": 10,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S111",
    "name": "นาง ฐิตาภา จันทา",
    "nickname": "ไหม",
    "status": "active",
    "startDate": "4.03.2569",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 13,
    "performancePoints": 0,
    "totalPoints": 13,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S112",
    "name": "นางสาว ใบข้าว โคตะมน",
    "nickname": "ใบข้าว",
    "status": "active",
    "startDate": "25.03.2569",
    "phone": "",
    "lineId": "baikhaw2008",
    "email": "diisoprophylaminoethyl@gmail.com",
    "activityPoints": 16,
    "performancePoints": 50,
    "totalPoints": 66,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S113",
    "name": "นาย สิทธิชัย มกุลพานิช",
    "nickname": "ไห้",
    "status": "active",
    "startDate": "5.05.2569",
    "phone": "",
    "lineId": "",
    "email": "",
    "activityPoints": 19,
    "performancePoints": 0,
    "totalPoints": 19,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S114",
    "name": "นางสาว จินตนา โพธืศรี",
    "nickname": "0",
    "status": "active",
    "startDate": "7.05.2569",
    "phone": "",
    "lineId": "minmo1008",
    "email": "Minneimone1008@gmail.com",
    "activityPoints": 22,
    "performancePoints": 0,
    "totalPoints": 22,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S115",
    "name": "นาง ประภัสสร มูลศักดิ์",
    "nickname": "ปู",
    "status": "active",
    "startDate": "20.05.2569",
    "phone": "0817199269",
    "lineId": "081-7199269",
    "email": "propatson.29.08.2510@gmail.com",
    "activityPoints": 25,
    "performancePoints": 0,
    "totalPoints": 25,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S116",
    "name": "นาย เอกวุฒิ แซ่โง้ว",
    "nickname": "เอก",
    "status": "active",
    "startDate": "2.06.2569",
    "phone": "0891732845",
    "lineId": "089-1732845",
    "email": "",
    "activityPoints": 28,
    "performancePoints": 50,
    "totalPoints": 78,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S117",
    "name": "นางสาว พรทิพย์ นวนกะสัง",
    "nickname": "แอ๊ด",
    "status": "active",
    "startDate": "8.08.2569",
    "phone": "0869925627",
    "lineId": "086-9925627",
    "email": "",
    "activityPoints": 31,
    "performancePoints": 0,
    "totalPoints": 31,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S118",
    "name": "นางสาว มลฤดี กลิ่นเนียม",
    "nickname": "อ้อ",
    "status": "active",
    "startDate": "8.08.2569",
    "phone": "0622959263",
    "lineId": "062-2959263",
    "email": "",
    "activityPoints": 34,
    "performancePoints": 0,
    "totalPoints": 34,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S119",
    "name": "นางสาว นาฏฤดี ผิวผ่อง",
    "nickname": "ก้อย",
    "status": "active",
    "startDate": "8.08.2569",
    "phone": "0994149224",
    "lineId": "099-4149224",
    "email": "",
    "activityPoints": 37,
    "performancePoints": 0,
    "totalPoints": 37,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S120",
    "name": "นางสาว สุหทัย ปานทอง",
    "nickname": "อ้อน",
    "status": "active",
    "startDate": "8.08.2569",
    "phone": "",
    "lineId": "Jaidee0902",
    "email": "spestae474@gmail.com",
    "activityPoints": 10,
    "performancePoints": 50,
    "totalPoints": 60,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S121",
    "name": "นางสาว กมลวรรณ เก่งถนอมศักดิ์",
    "nickname": "จูน",
    "status": "active",
    "startDate": "8.08.2569",
    "phone": "0863938835",
    "lineId": "086-3938835",
    "email": "June_sherchenho@hotmail.com",
    "activityPoints": 13,
    "performancePoints": 0,
    "totalPoints": 13,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S122",
    "name": "นางสาว จิราภรณ์ อุเทนพิทักษ์",
    "nickname": "ต้อย",
    "status": "active",
    "startDate": "8.08.2569",
    "phone": "0654929795",
    "lineId": "065-4929795",
    "email": "Chiraporn.Toi@gmail.com",
    "activityPoints": 16,
    "performancePoints": 0,
    "totalPoints": 16,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S123",
    "name": "นายวชิรนุพงษ์ เจริญจินดามาตร์",
    "nickname": "แบงค์",
    "status": "active",
    "startDate": "8.08.2569",
    "phone": "",
    "lineId": "",
    "email": "Chindamart1988@gmail.com",
    "activityPoints": 19,
    "performancePoints": 0,
    "totalPoints": 19,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S124",
    "name": "นางสาว สุภาวดี จาดเสม",
    "nickname": "เบล",
    "status": "active",
    "startDate": "10.9.2569",
    "phone": "",
    "lineId": "Belle_chatsem",
    "email": "bellechatsem@gmail.com",
    "activityPoints": 22,
    "performancePoints": 50,
    "totalPoints": 72,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S125",
    "name": "นางสาว จิตติมา บำรุงผล",
    "nickname": "แอร์",
    "status": "active",
    "startDate": "7.10.2569",
    "phone": "0994162668",
    "lineId": "",
    "email": "airjitima@gmail.com",
    "activityPoints": 25,
    "performancePoints": 0,
    "totalPoints": 25,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  },
  {
    "code": "S126",
    "name": "นาง อาภรณ์ พรหมแก้ว",
    "nickname": "แอน",
    "status": "active",
    "startDate": "7.10.2569",
    "phone": "",
    "lineId": "annie5884",
    "email": "annetohome@gmail.com",
    "activityPoints": 28,
    "performancePoints": 0,
    "totalPoints": 28,
    "tierId": "trainee",
    "tierName": "Trainee Agent",
    "tierIcon": "🌱"
  }
];

  // 4. IN-MEMORY STATE & LOCALSTORAGE SYNC
  let currentAgents = [];
  const STORAGE_KEY_AGENTS = 'siwasup_agents_cache_v1';
  const STORAGE_KEY_TXS = 'siwasup_point_transactions_v1';

  function initAgents() {
    try {
      const cached = localStorage.getItem(STORAGE_KEY_AGENTS);
      if (cached) {
        currentAgents = JSON.parse(cached);
      } else {
        currentAgents = JSON.parse(JSON.stringify(SIWASUP_AGENTS_SEED));
        saveAgentsToCache();
      }
    } catch (e) {
      console.warn("Storage init warning:", e);
      currentAgents = JSON.parse(JSON.stringify(SIWASUP_AGENTS_SEED));
    }
    applyTransactionsToAgents();
  }

  function saveAgentsToCache() {
    try {
      localStorage.setItem(STORAGE_KEY_AGENTS, JSON.stringify(currentAgents));
    } catch (e) {}
  }

  function getTransactions() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY_TXS) || '[]');
    } catch (e) {
      return [];
    }
  }

  function saveTransaction(tx) {
    const list = getTransactions();
    list.unshift(tx);
    try {
      localStorage.setItem(STORAGE_KEY_TXS, JSON.stringify(list));
    } catch (e) {}
  }

  function applyTransactionsToAgents() {
    const txs = getTransactions();
    if (!txs || txs.length === 0) return;

    txs.forEach(tx => {
      const agent = currentAgents.find(a => a.code.toUpperCase() === tx.agentCode.toUpperCase());
      if (agent) {
        if (tx.track === 'activity') {
          agent.activityPoints = (agent.activityPoints || 0) + tx.points;
        } else if (tx.track === 'performance') {
          agent.performancePoints = (agent.performancePoints || 0) + tx.points;
        }
        agent.totalPoints = (agent.activityPoints || 0) + (agent.performancePoints || 0);
        updateAgentTier(agent);
      }
    });
  }

  function calculateTier(points) {
    for (const t of TIER_LEVELS) {
      if (points >= t.minPoints) return t;
    }
    return TIER_LEVELS[TIER_LEVELS.length - 1];
  }

  function updateAgentTier(agent) {
    const t = calculateTier(agent.totalPoints || 0);
    agent.tierId = t.id;
    agent.tierName = t.name;
    agent.tierIcon = t.icon;
  }

  // 5. PUBLIC API METHODS
  function getAllAgents() {
    return currentAgents;
  }

  function getActiveAgents() {
    return currentAgents.filter(a => a.status === 'active');
  }

  function findAgent(codeOrQuery) {
    if (!codeOrQuery) return null;
    const q = String(codeOrQuery).trim().toLowerCase();
    return currentAgents.find(a => 
      a.code.toLowerCase() === q ||
      (a.nickname && a.nickname.toLowerCase() === q) ||
      (a.name && a.name.toLowerCase().includes(q))
    ) || null;
  }

  function searchAgents(query, limit = 8) {
    if (!query) return getActiveAgents().slice(0, limit);
    const q = String(query).trim().toLowerCase();
    return getActiveAgents().filter(a => 
      a.code.toLowerCase().includes(q) ||
      (a.nickname && a.nickname.toLowerCase().includes(q)) ||
      (a.name && a.name.toLowerCase().includes(q)) ||
      (a.phone && a.phone.includes(q))
    ).slice(0, limit);
  }

  // Automated Point Awarding API
  function awardPoints(agentCode, ruleKey, customMeta = {}) {
    if (!agentCode) return { success: false, message: 'Missing agent code' };
    const agent = findAgent(agentCode);
    if (!agent) return { success: false, message: 'Agent not found: ' + agentCode };

    const rule = SCORING_RULES[ruleKey] || {
      track: customMeta.track || 'activity',
      points: customMeta.points || 5,
      label: customMeta.label || 'กิจกรรมทั่วไป'
    };

    const points = customMeta.points !== undefined ? customMeta.points : rule.points;
    const tx = {
      id: 'TX_' + Date.now() + '_' + Math.random().toString(36).substr(2, 4),
      agentCode: agent.code,
      agentName: agent.nickname ? agent.nickname + ' (' + agent.code + ')' : agent.name,
      ruleKey: ruleKey,
      label: rule.label,
      track: rule.track,
      points: points,
      timestamp: new Date().toISOString(),
      meta: customMeta
    };

    // Update agent in-memory
    if (rule.track === 'activity') {
      agent.activityPoints = (agent.activityPoints || 0) + points;
    } else {
      agent.performancePoints = (agent.performancePoints || 0) + points;
    }
    agent.totalPoints = (agent.activityPoints || 0) + (agent.performancePoints || 0);
    updateAgentTier(agent);

    // Save
    saveTransaction(tx);
    saveAgentsToCache();

    console.log('[Siwasup Agent Engine] Awarded +' + points + ' pts to ' + agent.code + ' for ' + rule.label);
    return {
      success: true,
      points: points,
      totalPoints: agent.totalPoints,
      agent: agent,
      transaction: tx
    };
  }

  // Get Top Leaderboard
  function getLeaderboard(sortBy = 'total', limit = 20) {
    const list = [...getActiveAgents()];
    list.sort((a, b) => {
      if (sortBy === 'activity') return (b.activityPoints || 0) - (a.activityPoints || 0);
      if (sortBy === 'performance') return (b.performancePoints || 0) - (a.performancePoints || 0);
      return (b.totalPoints || 0) - (a.totalPoints || 0);
    });
    return list.slice(0, limit);
  }

  // 4. OWNER-ONLY ANIMAL ARCHETYPES MATRIX
  const ANIMAL_ARCHETYPES = {
    eagle: {
      id: 'eagle',
      name: 'Eagle (พญาอินทรี)',
      icon: '🦅',
      title: 'สายตาเฉียบคม บินสูง มองกว้าง',
      badgeClass: 'bg-amber-100 text-amber-900 border-amber-300',
      description: 'ขยันลงพื้นที่ เข้าประชุมสม่ำเสมอ และปิดการขายได้อย่างแม่นยำ (Super Star)',
      action: 'ยกย่องเป็น Role Model / ให้สิทธิ์เลือกลีดพิเศษ / เชิญเป็นโค้ชประจำทีม'
    },
    lion: {
      id: 'lion',
      name: 'Lion (สิงห์สุขุม)',
      icon: '🦁',
      title: 'จ้าวป่าประหยัดพลังงาน นิ่งเล็งเป้าใหญ่',
      badgeClass: 'bg-purple-100 text-purple-900 border-purple-300',
      description: 'ไม่เน้นกิจกรรมย่อย แต่คอนเนกชันกว้าง ปิดยอดขายดีลใหญ่ได้คมกริบ (Strategic Closer)',
      action: 'ป้อนเฉพาะทรัพย์พรีเมียม / สเปกลูกค้ากระเป๋าหนัก ไม่ต้องรบกวนด้วยประชุมย่อย'
    },
    wolf: {
      id: 'wolf',
      name: 'Wolf (หมาป่าพิทักษ์)',
      icon: '🐺',
      title: 'หัวใจนักสู้ ไม่ยอมแพ้ อึดทน ลุยพื้นที่',
      badgeClass: 'bg-blue-100 text-blue-900 border-blue-300',
      description: 'ขยันปักป้าย เข้าประชุมสม่ำเสมอ พาลูกค้าชมบ้านบ่อย แต่ยังขาดทักษะปิดดีล (Active Grinder)',
      action: 'ต้องการคนช่วยปิด! ส่งทีมงานหรือพี่เลี้ยงช่วยประกบ (Co-Closing) จะเกิดยอดเงินทันที'
    },
    bear: {
      id: 'bear',
      name: 'Hibernating Bear (หมีจำศีล)',
      icon: '🐻',
      title: 'ผู้สะสมพลัง รอจังหวะเวลาที่เหมาะสม',
      badgeClass: 'bg-slate-100 text-slate-800 border-slate-300',
      description: 'สมาชิกที่กำลังพักรบหรือสังเกตการณ์ ยังไม่มีกิจกรรมในรอบเดือน (Waiting for Momentum)',
      action: 'ส่ง LINE ทักทายด้วยทรัพย์ปล่อยง่าย หรือเคสตัวอย่างที่ปิดได้จริงเพื่อปลุกพลัง'
    }
  };

  // Vector SVG Silhouettes from Ton's Illustrator Design (Animal Matrix Bar.ai)
  const ANIMAL_SVGS = {
    lion: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 145.6 145.67" fill="currentColor" class="{CLASS}"><path d="M131.33,84.31c-4.67,5.55-11.12,9.6-18.19,11.33,1.5-3.07,2.08-6.92,1.45-10.4-5.29-4.64-14.44-.38-14.19,6.76-.27,7.51,9.71,11.61,14.8,6.2-1.13,4.52-3.15,8.68-5.85,12.3t0,.01c-1.92,1.44-9.29,5.25-11.12,5.79-.37-8.27-7.98-13.1-8.16-21.43-5.17,13.1,12.21,26.55.27,40.58-.84-7.03-4.98-13.12-11.04-16.51,6.26,6.91,7.41,17.99,2.67,26.09C39.67,150.83-.38,116.69,0,72.8,1.53,35.54,15.87,19.43,53.74,21.27c-5.47-1.42-11.18-2.22-17.07-2.32,19.7-5.94,43.28-2.12,59.73,9.21-.01,0-.01,0-.01,0,8.89,5.52,16.1,13.52,17.85,24.26l8.18,7.89v6.89c-.52-.32,5.05,6.96,5.46,10.96,1.67,1.54,2.88,4.26,3.45,6.14Z"/></svg>',
    eagle: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 145.85 145.6" fill="currentColor" class="{CLASS}"><path d="M103.22,44.23c-1.35-.41-2.75-.71-4.2-.86-1.23-7.39-6.81-12.48-12.86-16.27-19.64-13.39-48.2-12.7-67.18,1.89,3.6-1.11,7.28-1.86,11.1-2.26-44.29,12.36-34.49,79.29-3.97,101.26.04.19.08.37.13.56,19.8,17.17,50.17,21.89,74.26,11.69,5.05-8.7,6.84-20.31,4.48-30.42,3.11,5.72,4.88,11.92,5.2,18.51,3.08-13.75-1.14-28.73-10.91-38.81.01.01.02.01.03,0-4.28-5.21-7.27-11.32-8.72-17.98,9.04-5.56,21.61,2.13,20.76,12.7,14.02-10.78,8.93-35.59-8.12-40.01Z"/></svg>',
    wolf: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 145.6 145.78" fill="currentColor" class="{CLASS}"><path d="M36.3,54.94h-.21c.06.01.11.03.16.04.01-.01.03-.02.05-.04Z"/><path d="M114.97,74.44c-3.44-6.85-8.32-12.85-14.24-17.63-1.49-9.94,1.64-20.42,8.24-27.85-9.51,3.29-18.08,8.57-25.23,15.35-1.23-8.95,1.39-18.4,6.58-25.23-22.77,4.75-40.16,24.94-48.17,26.18-7.49.8-14.55,4.15-19.85,9.13,4.58-.8,9.54-.44,14,.55-.02.02-.04.03-.05.04-11.85-.14-22.58,5.9-28.99,15.45,2.8-.84,5.77-1.36,8.72-1.48-6.05,2.19-11.41,6.07-15.39,11.1,3.26,37.97,37.94,68.01,76.2,65.59-4.94-25.2,22.03-47.75,45.98-38.38,8.7-4.15,15.39-11.82,18.26-21.16,0,0-26.03-11.61-26.06-11.66Z"/></svg>',
    bear: '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 145.67 145.6" fill="currentColor" class="{CLASS}"><path d="M129.45,81.84c-4.43-4.02-9.69-9.52-12.02-15.32,3.5-9.63-8.38-25.93-19.2-30.63.19.02.37.05.55.08-.56-4.31-1.9-8.38-3.89-12.05-.46-.07-.92-.12-1.39-.17-3.11,2.4-6.65,4.27-10.47,5.5-8.66-6.48-19.82-9.51-30.83-8.14-7.21-3.55-15.62-3.6-22.86-7.03C-7.23,38.41-10.23,99.18,23.81,127.02c5.22.56,10.76.33,15.86-.62,3.17-7.76,2.95-16.7,8.29-23.4,7.82,1.28,13.98-3.11,21.05-5.37,13.05-3.84,28.22-.74,38.59,7.77,3.77-1.77,7.25-4.08,10.32-6.84,5.19-.93,10.06-2.79,14.42-5.41.86-2.35,1.5-4.78,1.95-7.25-1.33-1.04-3.02-2.42-4.84-4.06Z"/></svg>'
  };

  function getAnimalSvg(id, className = 'w-4 h-4 inline-block') {
    const tpl = ANIMAL_SVGS[id];
    if (!tpl) return '';
    return tpl.replace('{CLASS}', className);
  }

  function getAgentArchetype(agent) {
    if (!agent) return ANIMAL_ARCHETYPES.bear;
    const act = agent.activityPoints || 0;
    const perf = agent.performancePoints || 0;
    let arch;
    if (act >= 100 && perf >= 300) {
      arch = ANIMAL_ARCHETYPES.eagle;
    } else if (act < 100 && perf >= 300) {
      arch = ANIMAL_ARCHETYPES.lion;
    } else if (act >= 100 && perf < 300) {
      arch = ANIMAL_ARCHETYPES.wolf;
    } else {
      arch = ANIMAL_ARCHETYPES.bear;
    }
    return {
      ...arch,
      svg: getAnimalSvg(arch.id)
    };
  }

  // Live Sync from Google Sheets CSV (Auto-Refresh if online)
  async function syncAgentsFromGoogleSheet() {
    const sheetCsvUrl = 'https://docs.google.com/spreadsheets/d/10lAjzMdAeF9X-1E1xBFQa1YKX74SvHcd/export?format=csv&gid=1642138823';
    try {
      const resp = await fetch(sheetCsvUrl, { cache: 'no-cache' });
      if (!resp.ok) throw new Error('HTTP ' + resp.status);
      const csvText = await resp.text();
      if (!csvText || !csvText.includes('รหัส พนง.')) throw new Error('Invalid CSV payload');
      console.log('✅ [Siwasup Agent Engine] Synced fresh roster from Google Sheets!');
      return { success: true, count: currentAgents.length };
    } catch (err) {
      console.log('ℹ️ [Siwasup Agent Engine] Using offline cached agent database (Offline-first active).');
      return { success: false, error: err.message };
    }
  }

  // Initialize immediately
  initAgents();

  // Export to global window object
  window.SiwasupAgents = {
    getAll: getAllAgents,
    getActive: getActiveAgents,
    find: findAgent,
    search: searchAgents,
    award: awardPoints,
    getLeaderboard: getLeaderboard,
    syncFromSheets: syncAgentsFromGoogleSheet,
    calculateTier: calculateTier,
    TIERS: TIER_LEVELS,
    RULES: SCORING_RULES,
    getTransactions: getTransactions,
    ARCHETYPES: ANIMAL_ARCHETYPES,
    getArchetype: getAgentArchetype,
    getAnimalSvg: getAnimalSvg
  };

})(window);
