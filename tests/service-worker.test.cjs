const { test } = require('node:test');
const assert = require('node:assert/strict');
const vm = require('node:vm');
const fs = require('node:fs');
const path = require('node:path');
const source = fs.readFileSync(path.join(__dirname, '../assets/starter/service-worker.js'), 'utf8');

function fixture() {
  const listeners = {}, added = [], puts = [];
  let skipWaitingCalls = 0;
  const cache = { addAll: async (items) => added.push(...items), match: async () => new Response('cached shell'), put: async (...args) => puts.push(args) };
  vm.runInNewContext(source, {
    URL, Response, Set,
    self: { location: { href: 'https://example.com/guide/service-worker.js', origin: 'https://example.com' }, addEventListener: (name, cb) => { listeners[name] = cb; }, skipWaiting: async () => { skipWaitingCalls += 1; }, clients: { claim: async () => {} } },
    caches: { open: async () => cache, match: async () => new Response('cached asset') },
    fetch: async () => { throw Error('network offline'); },
  });
  return { listeners, added, puts, getSkipWaitingCalls: () => skipWaitingCalls };
}

test('install includes all neutral starter shell dependencies', async () => {
  const { listeners, added } = fixture();
  let installing;
  listeners.install({ waitUntil: (promise) => { installing = promise; } });
  await installing;
  for (const file of ['index.html', 'styles.css', 'app.js', 'trip-state.js', 'data/trip-data.js']) assert.ok(added.includes(`./${file}`));
});

test('a new worker waits until the app explicitly activates the update', async () => {
  const { listeners, getSkipWaitingCalls } = fixture();
  let installing;
  listeners.install({ waitUntil: (promise) => { installing = promise; } });
  await installing;
  assert.equal(getSkipWaitingCalls(), 0);
  listeners.message({ data: { type: 'ACTIVATE_UPDATE' } });
  assert.equal(getSkipWaitingCalls(), 1);
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

function releaseFixture({present=true,installFails=false,clients=[],keys=[]}={}) {
  const listeners={},deleted=[];let claimed=0,fetches=0,globalMatches=0;
  const cache={addAll:async()=>{if(installFails)throw Error('missing core file')},match:async()=>present?new Response('current release'):undefined};
  vm.runInNewContext(source,{
    URL,Response,Set,
    self:{location:{href:'https://example.com/guide/service-worker.js',origin:'https://example.com'},addEventListener:(n,cb)=>listeners[n]=cb,skipWaiting:async()=>{},clients:{matchAll:async()=>clients,claim:async()=>{claimed++}}},
    caches:{open:async()=>cache,keys:async()=>keys,delete:async k=>deleted.push(k),match:async()=>{globalMatches++;return new Response('old release')}},
    fetch:async()=>{fetches++;return new Response('newer server file')},
  });
  return {listeners,deleted,stats:()=>({claimed,fetches,globalMatches})};
}
const lifecycle=async(f,name)=>{let task;f.listeners[name]({waitUntil:p=>task=p});await task};
test('failed install rejects and removes incomplete current cache',async()=>{
 const f=releaseFixture({installFails:true});await assert.rejects(lifecycle(f,'install'),/missing core/);assert.deepEqual(f.deleted,['__CACHE_NAME__-precache']);
});
test('activation retains prior releases while any windows remain',async()=>{
 const f=releaseFixture({clients:[{id:'synthetic-old-client'}],keys:['__CACHE_PREFIX__old-precache']});await lifecycle(f,'activate');assert.deepEqual(f.deleted,[]);
});
test('activation with no windows deletes only this guides older caches',async()=>{
 const f=releaseFixture({keys:['__CACHE_PREFIX__old-precache','__CACHE_NAME__-precache','unrelated']});await lifecycle(f,'activate');assert.deepEqual(f.deleted,['__CACHE_PREFIX__old-precache']);
});
test('a cached file uses the current release instead of a global older match',async()=>{
 const f=releaseFixture();let response;f.listeners.fetch({request:{method:'GET',mode:'cors',url:'https://example.com/guide/app.js'},respondWith:p=>response=p});assert.equal(await (await response).text(),'current release');assert.equal(f.stats().globalMatches,0);
});
test('a missing core asset cannot fall through to a newer unversioned network file',async()=>{
 const f=releaseFixture({present:false});let response;f.listeners.fetch({request:{method:'GET',mode:'cors',url:'https://example.com/guide/app.js'},respondWith:p=>response=p});assert.equal((await response).status,503);assert.equal(f.stats().fetches,0);assert.equal(f.stats().globalMatches,0);
});
