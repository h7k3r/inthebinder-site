/**
 * sw.js - lets inthebinder.com/app open with no signal once it has been
 * opened once (and so work as a home-screen app on iPhone).
 *
 * - The page itself: network first, the saved copy when offline.
 * - Everything else on inthebinder.com (app.js, styles, card data,
 *   translations, icons): the saved copy at once, refreshed in the
 *   background for next time.
 * - Other sites (card pictures, prices, other games' catalogues) are left
 *   alone: the browser's own cache handles them.
 * Each build has its own cache (mv7hfsyi); older ones are deleted.
 */
const CACHE = 'itb-app-mv7hfsyi';
const SCANNER = 'itb-scanner';
const CORE = [
  './',
  './app.js?v=mv7hfsyi',
  './styles.css?v=mv7hfsyi',
  './manifest.webmanifest',
  './data/en.json',
  './data/meta.json',
  '/icon.png',
  '/apple-touch-icon.png',
];

self.addEventListener('install', (e) => {
  // One file failing (an icon moved, a slow connection) must not stop the rest being saved.
  e.waitUntil((async () => {
    const c = await caches.open(CACHE);
    await Promise.all(CORE.map((u) => c.add(u).catch(() => {})));
    await self.skipWaiting();
  })());
});

self.addEventListener('activate', (e) => {
  e.waitUntil((async () => {
    for (const k of await caches.keys()) if (k.startsWith('itb-app-') && k !== CACHE) await caches.delete(k);
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return;

  // The picture scanner (~55 MB): kept in its own cache that app updates do
  // not clear, served from there without asking the network again. Its
  // addresses change when it changes (models/*?v=, ort-<version>/); an older
  // copy of the same file is dropped when the new one is saved.
  // models/manifest.json says which version is current: network first.
  if (url.pathname.endsWith('/models/manifest.json')) {
    e.respondWith(fetch(req).catch(async () => (await caches.match(req, { ignoreSearch: true })) || Response.error()));
    return;
  }
  if (url.pathname.includes('/models/') || /\/ort-[^/]+\//.test(url.pathname)) {
    e.respondWith((async () => {
      const cache = await caches.open(SCANNER);
      const hit = await cache.match(req);
      if (hit) return hit;
      const r = await fetch(req);
      if (r.ok) {
        for (const old of await cache.keys()) {
          const o = new URL(old.url);
          if (o.pathname === url.pathname && o.search !== url.search) await cache.delete(old);
        }
        e.waitUntil(cache.put(req, r.clone()));
      }
      return r;
    })());
    return;
  }

  if (req.mode === 'navigate') {
    e.respondWith((async () => {
      try {
        const fresh = await fetch(req);
        if (fresh.ok) (await caches.open(CACHE)).put('./', fresh.clone());
        return fresh;
      } catch (err) {
        return (await caches.match('./', { cacheName: CACHE })) || Response.error();
      }
    })());
    return;
  }

  e.respondWith((async () => {
    const cache = await caches.open(CACHE);
    const hit = await cache.match(req);
    const refresh = fetch(req).then((r) => {
      if (r.ok) cache.put(req, r.clone());
      return r;
    }).catch(() => null);
    if (hit) { e.waitUntil(refresh); return hit; }
    return (await refresh) || Response.error();
  })());
});
