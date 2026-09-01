const CACHE_PREFIX = '__CACHE_PREFIX__';
const VERSION = '__CACHE_NAME__';
const PRECACHE = `${VERSION}-precache`;
const RUNTIME = `${VERSION}-runtime`;
const APP_SHELL = [
  './',
  './index.html',
  './styles.css',
  './app.js',
  './data/trip-data.js',
  './manifest.webmanifest',
  './icons/app-icon.svg',
];

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(PRECACHE);
    await cache.addAll(APP_SHELL);
    await self.skipWaiting();
  })());
});
self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(
      keys
        .filter((key) => key.startsWith(CACHE_PREFIX) && key !== PRECACHE && key !== RUNTIME)
        .map((key) => caches.delete(key)),
    );
    await self.clients.claim();
  })());
});

async function cachedAppShell(event) {
  const cache = await caches.open(PRECACHE);
  const cached = await cache.match('./index.html', { ignoreVary: true });
  event.waitUntil(
    fetch(event.request)
      .then((response) => response.ok && cache.put('./index.html', response.clone()))
      .catch(() => {}),
  );
  return cached || new Response(
    '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><h1>旅行路书</h1><p>离线安装尚未完成，请恢复网络并在线打开一次。</p>',
    { headers: { 'Content-Type': 'text/html; charset=utf-8' } },
  );
}

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);

  if (request.mode === 'navigate') {
    event.respondWith(cachedAppShell(event));
    return;
  }

  if (url.origin !== self.location.origin) return;

  event.respondWith((async () => {
    const cached = await caches.match(request, { ignoreVary: true });
    if (cached) return cached;
    try {
      const response = await fetch(request);
      if (response.ok) {
        const cache = await caches.open(RUNTIME);
        await cache.put(request, response.clone());
      }
      return response;
    } catch {
      return new Response('', { status: 503, statusText: 'Offline' });
    }
  })());
});
