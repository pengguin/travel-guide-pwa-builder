(() => {
  'use strict';

  const trip = window.TRIP_DATA;
  const app = document.querySelector('#app');
  const routes = new Set(['overview', 'itinerary', 'map', 'guides', 'tools']);
  let dayFilter = 'all';
  const state = window.TripState;
  let lastDate = state.dateKey();
  let localStore;
  try { localStore = window.localStorage; } catch { localStore = null; }

  const escapeHtml = (value = '') => String(value).replace(/[&<>'"]/g, (character) => ({
    '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;',
  })[character]);
  const money = (value) => new Intl.NumberFormat('zh-CN', {
    style: 'currency', currency: trip.currency || 'CNY', maximumFractionDigits: 0,
  }).format(value || 0);
  const badge = (text, kind = '') => `<span class="badge ${kind}">${escapeHtml(text)}</span>`;
  const recheck = (value) => value ? badge('需临出发前再次确认', 'warn') : '';
  const phaseById = (id) => trip.phases.find((phase) => phase.id === id);

  document.querySelector('#brand-title').textContent = trip.shortTitle || trip.title;
  document.querySelector('#header-dates').textContent = trip.dateLabel;
  document.title = trip.title;

  function pageHead(eyebrow, title, lede) {
    return `<header class="page-head"><p class="eyebrow">${escapeHtml(eyebrow)}</p><h1>${escapeHtml(title)}</h1><p class="lede">${escapeHtml(lede)}</p></header>`;
  }

  function renderOverview() {
    const clock = state.tripClock(trip.startDate, trip.endDate);
    const today = trip.days.find((day) => day.date === state.dateKey());
    const selected = clock.phase === 'before' ? trip.days[0] : today;
    const currentCard = selected ? `<section class="card section"><p class="eyebrow">${clock.phase === 'before' ? '出发日预览' : '今日安排'} · D${selected.dayNumber}</p><h2>${escapeHtml(selected.location)}</h2><p>${escapeHtml(selected.summary)}</p><a class="button" href="#itinerary?day=${encodeURIComponent(selected.id)}">打开当天</a></section>` : '';
    const phaseCards = trip.phases.map((phase) => `
      <article class="card phase-card" style="--phase:${escapeHtml(phase.accent || '#d66b48')}">
        <p class="eyebrow">${escapeHtml(phase.dateRange)}</p>
        <h3>${escapeHtml(phase.name)}</h3>
        <p class="muted">${escapeHtml(phase.summary)}</p>
      </article>`).join('');
    const riskCards = trip.risks.map((risk) => `
      <article class="card risk-card ${risk.level === 'high' ? 'high' : ''}">
        <h3>${escapeHtml(risk.title)}</h3>
        <p>${escapeHtml(risk.detail)}</p>
        ${recheck(risk.needsRecheck)}
      </article>`).join('');
    const highlights = trip.highlights.map((item) => badge(item.label, item.status === 'core' ? 'core' : '')).join('');
    const perPerson = trip.budget.perPersonLow || trip.budget.perPersonHigh
      ? `${money(trip.budget.perPersonLow)}–${money(trip.budget.perPersonHigh)}` : '待核算';
    app.innerHTML = `
      <p class="trip-status" role="status">${escapeHtml(clock.label)}</p>
      <section class="hero">
        <div>
          <p class="eyebrow">完整旅行路书</p>
          <h1>${escapeHtml(trip.title)}</h1>
          <p class="lede">${escapeHtml(trip.summary)}</p>
          <p class="route-line">${escapeHtml(trip.routeText)}</p>
        </div>
        <div class="hero-meta">
          <div class="metric"><strong>${escapeHtml(trip.dateLabel)}</strong><span>旅行日期</span></div>
          <div class="metric"><strong>${trip.days.length} 天</strong><span>${trip.partySize || 1} 人 · ${escapeHtml(trip.currency)}</span></div>
          <div class="metric"><strong>${perPerson}</strong><span>人均预算区间</span></div>
        </div>
      </section>
      ${currentCard}
      <section class="section"><p class="eyebrow">Trip structure</p><h2>行程阶段</h2><div class="grid">${phaseCards}</div></section>
      <section class="section"><h2>行程一览</h2><ol class="overview-days">${trip.days.map((day) => `<li><a href="#itinerary?day=${encodeURIComponent(day.id)}"><strong>${escapeHtml(day.date)} · D${day.dayNumber} · ${escapeHtml(day.location)}</strong><span>${escapeHtml(day.title)}</span></a></li>`).join('')}</ol></section>
      <section class="section grid two">
        <div class="card"><p class="eyebrow">Must keep</p><h2>不可砍核心</h2><div>${highlights}</div></div>
        <div class="card"><p class="eyebrow">Rhythm</p><h2>节奏总览</h2><div class="rhythm">
          <span>移动日：${escapeHtml(trip.rhythm.transferDays.join('、') || '无')}</span>
          <span>高强度：${escapeHtml(trip.rhythm.highDays.join('、') || '无')}</span>
          <span>缓冲日：${escapeHtml(trip.rhythm.bufferDays.join('、') || '无')}</span>
        </div></div>
      </section>
      <section class="section"><p class="eyebrow">Critical items</p><h2>最重要的风险与下单事项</h2><div class="grid two">${riskCards}</div></section>
      <p class="muted section">内容最近核验：${escapeHtml(trip.lastVerified)}。动态信息仍须以临出发前的官方信息为准。</p>`;
  }

  function renderItinerary() {
    const selectedId = new URLSearchParams(location.hash.split('?')[1] || '').get('day');
    const filters = [{ id: 'all', name: '全部' }, ...trip.phases].map((phase) => `
      <button class="filter-button ${dayFilter === phase.id ? 'active' : ''}" data-filter="${escapeHtml(phase.id)}">${escapeHtml(phase.name)}</button>`).join('');
    const days = trip.days.filter((day) => dayFilter === 'all' || day.phaseId === dayFilter).map((day) => {
      const phase = phaseById(day.phaseId);
      const image = day.heroImage ? `<img class="day-image" src="${escapeHtml(day.heroImage)}" alt="${escapeHtml(day.imageAlt || day.title)}">` : '';
      const schedule = day.schedule.map((node) => `
        <li><span class="time">${escapeHtml(node.time)}</span><h3>${escapeHtml(node.title)}</h3>
          <p>${escapeHtml(node.detail)}</p>${node.transport ? badge(node.transport) : ''}</li>`).join('');
      const index = trip.days.indexOf(day);
      const dayLink = (target, label) => target ? `<a class="button secondary" href="#itinerary?day=${encodeURIComponent(target.id)}">${label}</a>` : `<button class="button secondary" disabled>${label}</button>`;
      return `<details class="card day-card" id="${escapeHtml(day.id)}" ${(selectedId ? day.id === selectedId : day.dayNumber === 1) ? 'open' : ''}>
        <summary>
          <span class="day-number">D${day.dayNumber}</span>
          <span class="day-title"><strong>${escapeHtml(day.date)} · ${escapeHtml(day.location)}</strong><p>${escapeHtml(day.title)}</p></span>
          ${badge(day.intensity === 'transfer' ? '移动日' : day.intensity)}
        </summary>
        <div class="day-body">
          ${image}
          <p>${escapeHtml(day.summary)}</p>
          <p>${phase ? badge(phase.name) : ''}${day.hotelChange ? badge('换酒店', 'warn') : badge('不换酒店')} ${recheck(day.needsRecheck)}</p>
          <ol class="timeline">${schedule}</ol>
          <div class="card"><strong>住宿</strong><p>${escapeHtml(day.stay || day.overnightLocation || '待确认')}</p></div>
          ${day.food?.length ? `<p><strong>餐饮：</strong>${escapeHtml(day.food.join('；'))}</p>` : ''}
          ${day.notes?.length ? `<p class="muted">${escapeHtml(day.notes.join('；'))}</p>` : ''}
          <nav class="day-navigation" aria-label="逐日跳转">${dayLink(trip.days[index - 1], '← 前一天')}${dayLink(trip.days[index + 1], '下一天 →')}</nav>
        </div>
      </details>`;
    }).join('');
    app.innerHTML = `${pageHead('Daily plan', '逐日行程', '主卡片先显示当天主线、移动强度与住宿变化，细节展开后查看。')}
      <div class="filters" aria-label="按阶段筛选">${filters}</div>${days || '<p>当前筛选下没有日程。</p>'}`;
    app.querySelectorAll('[data-filter]').forEach((button) => button.addEventListener('click', () => {
      dayFilter = button.dataset.filter;
      renderItinerary();
    }));
  }

  function mapSvg(points) {
    if (!points.length) return '<p>尚未添加路线坐标。</p>';
    const width = 800, height = 500, padding = 58;
    const lats = points.map((point) => point.lat), lngs = points.map((point) => point.lng);
    const latSpan = Math.max(...lats) - Math.min(...lats) || 1;
    const lngSpan = Math.max(...lngs) - Math.min(...lngs) || 1;
    const xy = points.map((point) => ({
      ...point,
      x: padding + ((point.lng - Math.min(...lngs)) / lngSpan) * (width - padding * 2),
      y: height - padding - ((point.lat - Math.min(...lats)) / latSpan) * (height - padding * 2),
    }));
    const line = xy.map((point) => `${point.x},${point.y}`).join(' ');
    const nodes = xy.map((point, index) => `
      <g><circle cx="${point.x}" cy="${point.y}" r="17" fill="#d66b48" stroke="#fff" stroke-width="5"/>
      <text x="${point.x}" y="${point.y + 5}" text-anchor="middle" fill="#fff" font-size="13" font-weight="800">${index + 1}</text>
      <text x="${point.x}" y="${point.y - 28}" text-anchor="middle" fill="#173f3b" font-size="16" font-weight="750">${escapeHtml(point.label)}</text></g>`).join('');
    return `<svg viewBox="0 0 ${width} ${height}" role="img" aria-label="${escapeHtml(trip.routeText)}">
      <path d="M32 90 C160 30 260 120 380 68 S620 10 770 88" fill="none" stroke="#c5d8cf" stroke-width="34" opacity=".65"/>
      <polyline points="${line}" fill="none" stroke="#173f3b" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="14 12"/>
      ${nodes}</svg>`;
  }

  function renderMap() {
    const list = trip.route.map((point, index) => `<li><span class="route-index">${index + 1}</span><span><strong>${escapeHtml(point.label)}</strong><br><small class="muted">${escapeHtml(point.region)}</small></span></li>`).join('');
    app.innerHTML = `${pageHead('Route map', '路线总览', '路线图用于理解转场顺序；精确导航仍应使用离线地图或当地地图服务。')}
      <div class="map-shell"><div id="route-map">${mapSvg(trip.route)}</div><aside class="card"><h2>经过地点</h2><ol class="route-list">${list}</ol></aside></div>`;
  }

  function renderGuides() {
    const guides = trip.guides.map((guide) => `
      <section class="guide-block section"><p class="eyebrow">Practical guide</p><h2>${escapeHtml(guide.title)}</h2><p class="lede">${escapeHtml(guide.summary)}</p>
        ${guide.items.map((item) => `<details><summary>${escapeHtml(item.title)} ${item.needsRecheck ? '· 需复核' : ''}</summary><div>${escapeHtml(item.body)} ${recheck(item.needsRecheck)}</div></details>`).join('')}
      </section>`).join('');
    const sources = trip.sources.length ? `<section class="section"><h2>来源与核验</h2><div class="card">${trip.sources.map((source) => `<p><a href="${escapeHtml(source.url)}" target="_blank" rel="noreferrer">${escapeHtml(source.title)}</a><br><small>${escapeHtml(source.publisher)} · ${escapeHtml(source.checkedAt)}</small></p>`).join('')}</div></section>` : '';
    app.innerHTML = `${pageHead('Travel notes', '实用指南', '把法规、交通备选、住宿、餐饮、装备和支付等细节集中在这里，不干扰每日主线。')}${guides}${sources}`;
  }

  function budgetTotals() {
    return trip.budgetItems.reduce((totals, item) => ({ low: totals.low + Number(item.low || 0), high: totals.high + Number(item.high || 0) }), { low: 0, high: 0 });
  }

  function downloadCalendar() {
    const stamp = new Date().toISOString().replace(/[-:]/g, '').replace(/\.\d{3}/, '');
    const events = trip.days.map((day) => {
      const date = day.date.replaceAll('-', '');
      const next = new Date(`${day.date}T00:00:00`); next.setDate(next.getDate() + 1);
      const end = `${next.getFullYear()}${String(next.getMonth() + 1).padStart(2, '0')}${String(next.getDate()).padStart(2, '0')}`;
      return ['BEGIN:VEVENT', `UID:${trip.id}-${day.id}@travel-guide`, `DTSTAMP:${stamp}`, `DTSTART;VALUE=DATE:${date}`, `DTEND;VALUE=DATE:${end}`, `SUMMARY:${day.location}｜${day.title}`, `DESCRIPTION:${day.summary}`, 'END:VEVENT'].join('\r\n');
    }).join('\r\n');
    const content = `BEGIN:VCALENDAR\r\nVERSION:2.0\r\nPRODID:-//Travel Guide PWA//CN\r\n${events}\r\nEND:VCALENDAR`;
    const url = URL.createObjectURL(new Blob([content], { type: 'text/calendar;charset=utf-8' }));
    const link = document.createElement('a'); link.href = url; link.download = `${trip.id}.ics`; link.click(); URL.revokeObjectURL(url);
  }

  function renderTools() {
    const totals = budgetTotals();
    const storageKey = `${trip.id}-checklist`;
    const checked = state.readChecks(localStore, storageKey);
    const budgetRows = trip.budgetItems.map((item) => `<div class="budget-row"><span>${escapeHtml(item.label)}<br><small class="muted">${escapeHtml(item.basis)}</small></span><strong>${money(item.low)}–${money(item.high)}</strong></div>`).join('');
    const checks = trip.checklist.map((item) => `<li><label><input type="checkbox" data-check="${escapeHtml(item.id)}" ${checked[item.id] ? 'checked' : ''}><span>${escapeHtml(item.label)}</span></label></li>`).join('');
    app.innerHTML = `${pageHead('Trip tools', '预算与下单清单', '预算区分估算与已确认成本；清单状态只保存在当前设备。')}
      <details class="card tool-module"><summary>预算估算 <span class="muted">${money(totals.low)}–${money(totals.high)} / 人</span></summary><div class="budget-total"><span>当前人均估算</span><strong>${money(totals.low)}–${money(totals.high)}</strong><small>另建议预留 ${Math.round((trip.budget.contingencyRate || 0) * 100)}% 机动金</small></div>${budgetRows}</details>
      <details class="card tool-module"><summary>最终下单前检查 <span id="check-progress" class="muted"></span></summary><ul class="checklist">${checks}</ul><p id="storage-status" role="status" class="muted"></p></details>
      <details class="card tool-module"><summary>日历与打印 <span class="muted">导出日程、打印当前页面</span></summary><div class="action-row"><button class="button" id="calendar-button">导出日历</button><button class="button secondary" onclick="window.print()">打印 / PDF</button></div></details>`;
    const progress = () => { document.querySelector('#check-progress').textContent = `${trip.checklist.filter((item) => checked[item.id]).length} / ${trip.checklist.length} 已完成`; };
    progress();
    app.querySelectorAll('[data-check]').forEach((input) => input.addEventListener('change', () => {
      checked[input.dataset.check] = input.checked;
      document.querySelector('#storage-status').textContent = state.saveChecks(localStore, storageKey, checked) ? '' : '设备存储不可用，本次勾选仅在当前页面保留。';
      progress();
    }));
    document.querySelector('#calendar-button').addEventListener('click', downloadCalendar);
  }

  const renderers = { overview: renderOverview, itinerary: renderItinerary, map: renderMap, guides: renderGuides, tools: renderTools };
  function renderRoute() {
    const route = location.hash.slice(1).split('?')[0] || 'overview';
    const safeRoute = routes.has(route) ? route : 'overview';
    if (safeRoute === 'itinerary' && location.hash.includes('?day=')) dayFilter = 'all';
    renderers[safeRoute]();
    document.querySelectorAll('[data-route]').forEach((link) => link.classList.toggle('active', link.dataset.route === safeRoute));
    window.scrollTo({ top: 0, behavior: 'instant' });
    if (safeRoute === 'itinerary') {
      const id = new URLSearchParams(location.hash.split('?')[1] || '').get('day');
      if (id) document.getElementById(id)?.scrollIntoView({ block: 'start' });
    }
  }

  function refreshDate() {
    const nextDate = state.dateKey();
    if (nextDate === lastDate) return;
    lastDate = nextDate;
    if (!location.hash || location.hash === '#overview') renderOverview();
  }
  ['focus', 'pageshow'].forEach((event) => window.addEventListener(event, refreshDate));
  document.addEventListener('visibilitychange', () => { if (!document.hidden) refreshDate(); });
  window.setInterval(refreshDate, 30000);
  const topButton = document.querySelector('#back-top');
  const updateTop = () => { topButton.hidden = window.scrollY < 500 || /^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement?.tagName || ''); };
  window.addEventListener('scroll', updateTop, { passive: true });
  document.addEventListener('focusin', updateTop);
  document.addEventListener('focusout', () => window.setTimeout(updateTop, 0));
  topButton.addEventListener('click', () => window.scrollTo({ top: 0, behavior: window.matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' }));
  let printDetails = [];
  window.addEventListener('beforeprint', () => {
    printDetails = Array.from(app.querySelectorAll('details:not([open])'));
    printDetails.forEach((details) => { details.open = true; });
  });
  window.addEventListener('afterprint', () => { printDetails.forEach((details) => { details.open = false; }); printDetails = []; });

  window.addEventListener('hashchange', renderRoute);
  renderRoute();
  if ('serviceWorker' in navigator && location.protocol.startsWith('http')) {
    const register = () => navigator.serviceWorker.register('./service-worker.js').catch(() => {});
    if ('requestIdleCallback' in window) window.requestIdleCallback(register, { timeout: 1800 });
    else window.setTimeout(register, 250);
  }
})();
