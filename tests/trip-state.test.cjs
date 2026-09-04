const { test } = require('node:test');
const assert = require('node:assert/strict');
const { tripClock, dateKey, readChecks, saveChecks } = require('../assets/starter/trip-state.js');

test('countdown, D1, D2, final day and completion use calendar dates', () => {
  assert.deepEqual(tripClock('2030-01-02', '2030-01-05', '2030-01-01'), { phase: 'before', dayNumber: 1, label: '距出发还有 1 天' });
  for (const [today, day] of [['2030-01-02', 1], ['2030-01-03', 2], ['2030-01-05', 4]]) {
    assert.deepEqual(tripClock('2030-01-02', '2030-01-05', today), { phase: 'during', dayNumber: day, label: `旅程第 ${day} 天` });
  }
  assert.equal(tripClock('2030-01-02', '2030-01-05', '2030-01-06').dayNumber, null);
  assert.equal(tripClock('2030-12-31', '2031-01-02', '2031-01-01').dayNumber, 2);
});

test('device local date and DST transitions do not lose a day', () => {
  const oldTZ = process.env.TZ;
  try {
    process.env.TZ = 'America/New_York';
    assert.equal(dateKey(new Date('2030-03-10T04:30:00Z')), '2030-03-09');
    assert.equal(tripClock('2030-03-09', '2030-03-12', '2030-03-11').dayNumber, 3);
    process.env.TZ = 'Asia/Tokyo';
    assert.equal(dateKey(new Date('2030-03-10T04:30:00Z')), '2030-03-10');
  } finally { if (oldTZ === undefined) delete process.env.TZ; else process.env.TZ = oldTZ; }
});

test('bad dates fail explicitly rather than silently normalize', () => {
  assert.throws(() => tripClock('2030-02-30', '2030-03-03'));
  assert.throws(() => tripClock('2030-03-03', '2030-03-01'));
});

test('corrupt or disabled device storage never breaks the guide', () => {
  for (const raw of ['not json', 'null', '[]', '42']) assert.deepEqual(readChecks({ getItem: () => raw }, 'test'), {});
  assert.deepEqual(readChecks({ getItem() { throw Error('disabled'); } }, 'test'), {});
  assert.deepEqual(readChecks(null, 'test'), {});
  assert.deepEqual(readChecks({ getItem: () => '{"task":true,"untrusted":"text"}' }, 'test'), { task: true });
  const store = { setItem(key, value) { this[key] = value; }, getItem(key) { return this[key]; } };
  assert.equal(saveChecks(store, 'test', { task: true }), true);
  assert.deepEqual(readChecks(store, 'test'), { task: true });
  assert.equal(saveChecks(null, 'test', {}), false);
});
