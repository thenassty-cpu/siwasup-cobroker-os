// Siwasup Co-Broker OS - Lightweight PWA Service Worker
// Version: 2.0.0 (Cache Bust: v2 - Full 75-15-5-5 Theme, Falcon & Gryphon Characters & Vector Emblems)
// Strategy: Network-First (เพื่อให้อัปเดตโค้ดบน GitHub Pages/Web แล้วผู้ใช้ได้เวอร์ชันใหม่ทันที ไม่ติดแคชเก่า)

const CACHE_NAME = 'siwasup-cache-v2.1';

const ASSETS_TO_CACHE = [
  './',
  './index.html',
  './modals.js',
  './siwasup_agents.js',
  './manifest.json',
  './Siwasup_Brand_Color_System_Dashboard.html',
  './Siwasup_Emblem_Showcase.html',
  './assets/icons/icon-192.png',
  './assets/icons/icon-512.png',
  './assets/icons/apple-touch-icon.png',
  // Fonts
  './assets/fonts/RSU_BOLD.ttf',
  './assets/fonts/RSU_Regular.ttf',
  // 6 3D Mascot Character Badges
  './assets/characters/badge_bear.png',
  './assets/characters/badge_wolf.png',
  './assets/characters/badge_lion.png',
  './assets/characters/badge_falcon.png',
  './assets/characters/badge_eagle.png',
  './assets/characters/badge_gryphon.png',
  // 6 3D Turnaround Sheets
  './assets/characters/turnaround_bear.png',
  './assets/characters/turnaround_wolf.png',
  './assets/characters/turnaround_lion.png',
  './assets/characters/turnaround_falcon.png',
  './assets/characters/turnaround_eagle.png',
  './assets/characters/turnaround_gryphon.png',
  // 6 Micro-Emblem Scalable SVGs
  './assets/badges/bear_emblem_micro.svg',
  './assets/badges/wolf_emblem_micro.svg',
  './assets/badges/lion_emblem_micro.svg',
  './assets/badges/falcon_emblem_micro.svg',
  './assets/badges/eagle_emblem_micro.svg',
  './assets/badges/gryphon_emblem_micro.svg',
  // 6 Master Medallion 3D Seals
  './assets/badges/bear_crest.jpg',
  './assets/badges/wolf_crest.jpg',
  './assets/badges/lion_crest.jpg',
  './assets/badges/falcon_crest.jpg',
  './assets/badges/eagle_crest.jpg',
  './assets/badges/gryphon_crest.jpg'
];

// Install: Pre-cache essential shell assets & skip waiting immediately
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      // Use catch on each to avoid complete failure if single asset missing
      return Promise.allSettled(
        ASSETS_TO_CACHE.map((url) =>
          cache.add(url).catch((err) => {
            console.warn('[PWA SW] Pre-cache skip for:', url, err);
          })
        )
      );
    }).then(() => self.skipWaiting())
  );
});

// Activate: Clean up old caches immediately and claim clients
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[PWA SW] Deleting obsolete cache:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch: Network-First with Cache Fallback
self.addEventListener('fetch', (event) => {
  // Only handle GET requests
  if (event.request.method !== 'GET') return;

  const url = new URL(event.request.url);

  // Skip chrome-extension, Google Sheet live dynamic CSV or non-http
  if (!url.protocol.startsWith('http')) return;
  if (url.hostname.includes('docs.google.com')) {
    // Dynamic Google Sheet data - always fetch live
    return;
  }

  event.respondWith(
    fetch(event.request)
      .then((networkResponse) => {
        // If response is valid, update the cache in background
        if (networkResponse && networkResponse.status === 200 && networkResponse.type === 'basic') {
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(event.request, responseToCache);
          });
        }
        return networkResponse;
      })
      .catch(() => {
        // If network fails (offline), fall back to cached copy
        return caches.match(event.request).then((cachedResponse) => {
          if (cachedResponse) return cachedResponse;
          // Fallback to offline index shell if page navigation
          if (event.request.mode === 'navigate') {
            return caches.match('./index.html');
          }
        });
      })
  );
});
