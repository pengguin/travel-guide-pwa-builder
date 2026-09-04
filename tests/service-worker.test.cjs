const { test } = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../assets/starter/service-worker.js'), 'utf8');

function fixture() {
  const listeners = {}, added = [], puts = [];
  const cache = { addAll: async (items) => added.push(...items), match: async () => new Response('cached shell'), put: async (...args) => puts.push(args) };
  vm.runInNewContext(source, {
    URL, Response, Set,
    self: { location: { href: 'https://example.com/guide/service-worker.js', origin: 'https://example.com' }, addEventListener: (name, cb) => { listeners[name] = cb; }, skipWaiting: async () => {}, clients: { claim: async () => {} } },
    caches: { open: async () => cache, match: async () => new Response('cached asset') },
    fetch: async () => { throw Error('network offline'); },
  });
  return { listeners, added, puts };
}

test('install includes all neutral starter shell dependencies', async () => {
  const { listeners, added } = fixture();
  let installing;
  listeners.install({ waitUntil: (promise) => { installing = promise; } });
  await installing;
  for (const file of ['index.html', 'styles.css', 'app.js', 'trip-state.js', 'data/trip-data.js']) assert.ok(added.includes(`./${file}`));
});

test('private APIs, auth, non-GET and other origins are not intercepted', () => {
  const { listeners } = fixture();
  for (const url of ['https://example.com/guide/api/profile', 'https://example.com/guide/members', 'https://example.com/signin-with-chatgpt', 'https://other.example/guide/index.html']) {
    listeners.fetch({ request: { method: 'GET', mode: 'navigate', url }, respondWith() { assert.fail(`Intercepted ${url}`); } });
  }
  listeners.fetch({ request: { method: 'POST', url: 'https://example.com/guide/' }, respondWith() { assert.fail('Intercepted POST'); } });
});

test('public shell opens offline without waiting for remote fetch or mixing HTML versions', async () => {
  const { listeners, puts } = fixture();
  let response;
  listeners.fetch({ request: { method: 'GET', mode: 'navigate', url: 'https://example.com/guide/?release=2' }, respondWith(promise) { response = promise; } });
  assert.equal(await (await response).text(), 'cached shell');
  assert.equal(puts.length, 0);
});
