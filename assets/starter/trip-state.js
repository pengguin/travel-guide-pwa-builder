(function (root) {
  'use strict';
  const dateKey = (now = new Date()) => [now.getFullYear(), String(now.getMonth() + 1).padStart(2, '0'), String(now.getDate()).padStart(2, '0')].join('-');
  function calendarDay(value) {
    if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) throw new Error('Invalid calendar date');
    const date = new Date(`${value}T00:00:00Z`);
    if (!Number.isFinite(date.getTime()) || date.toISOString().slice(0, 10) !== value) throw new Error('Invalid calendar date');
    return date.getTime() / 86400000;
  }
  function tripClock(start, end, today = dateKey()) {
    const first = calendarDay(start), last = calendarDay(end), current = calendarDay(today);
    if (first > last) throw new Error('Reversed trip dates');
    if (current < first) return { phase: 'before', dayNumber: 1, label: `距出发还有 ${first - current} 天` };
    if (current > last) return { phase: 'after', dayNumber: null, label: '行程已结束' };
    return { phase: 'during', dayNumber: current - first + 1, label: `旅程第 ${current - first + 1} 天` };
  }
  function readChecks(storage, key) {
    try {
      const data = JSON.parse(storage.getItem(key) || '{}');
      return data && typeof data === 'object' && !Array.isArray(data)
        ? Object.fromEntries(Object.entries(data).filter(([, value]) => typeof value === 'boolean')) : {};
    } catch { return {}; }
  }
  function saveChecks(storage, key, value) {
    try { storage.setItem(key, JSON.stringify(value)); return true; } catch { return false; }
  }
  const api = { dateKey, calendarDay, tripClock, readChecks, saveChecks };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  else root.TripState = api;
})(globalThis);
