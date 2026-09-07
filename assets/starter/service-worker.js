const CACHE_PREFIX = '__CACHE_PREFIX__';
const VERSION = '__CACHE_NAME__';
const PRECACHE = `${VERSION}-precache`;
const RUNTIME = `${VERSION}-runtime`;
const APP_SHELL = [
  './',
  './index.html',
  './styles.css',
  './app.js',
  './trip-state.js',
  './data/trip-data.js',
  './manifest.webmanifest',
  './icons/app-icon.svg',
];

self.addEventListener('install', (event) => {
  event.waitUntil((async () => {
    const cache = await caches.open(PRECACHE);
    try {
      await cache.addAll(APP_SHELL);
    } catch (error) {
      await caches.delete(PRECACHE);
      throw error;
    }
  })());
});
self.addEventListener('message', (event) => {
  if (event.data?.type === 'ACTIVATE_UPDATE') self.skipWaiting();
});
self.addEventListener('activate', (event) => {
  event.waitUntil((async () => {
    const windows = await self.clients.matchAll({ type: 'window', includeUncontrolled: true });
    const keys = windows.length ? [] : await caches.keys();
    await Promise.all(
      keys
        .filter((key) => key.startsWith(CACHE_PREFIX) && key !== PRECACHE && key !== RUNTIME)
        .map((key) => caches.delete(key)),
    );
    await self.clients.claim();
  })());
});

async function cachedAppShell() {
  const cache = await caches.open(PRECACHE);
  const cached = await cache.match('./index.html', { ignoreVary: true });
  return cached || new Response(
    '<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width"><h1>旅行路书</h1><p>离线安装尚未完成，请恢复网络并在线打开一次。</p>',
    { headers: { 'Content-Type': 'text/html; charset=utf-8' } },
  );
}

self.addEventListener('fetch', (event) => {
  const request = event.request;
  if (request.method !== 'GET') return;
  const url = new URL(request.url);
  const scope = new URL('./', self.location.href);
  // Explicit public allowlist: never cache API/auth/member responses.
  const publicPaths = new Set(APP_SHELL.map((path) => new URL(path, scope).pathname));
  if (url.origin !== scope.origin || !publicPaths.has(url.pathname)) return;

  if (request.mode === 'navigate') {
    event.respondWith(cachedAppShell());
    return;
  }

  if (url.origin !== self.location.origin) return;

  event.respondWith((async () => {
    // The current worker owns one whole release. A global caches.match can
    // silently serve an older file with the same unversioned starter name.
    const cache = await caches.open(PRECACHE);
    const cached = await cache.match(request, { ignoreVary: true });
    if (cached) return cached;
    // Do not mix a newly deployed unversioned file into an old cached shell.
    // Close old tabs and install a complete release; this starter has no
    // manifest-aware same-version repair UI.
    return new Response('Core offline asset missing. Reopen online after updating the complete guide.', {
      status: 503, statusText: 'Incomplete offline release',
    });
  })());
});
