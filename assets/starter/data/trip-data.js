window.TRIP_DATA = {
  scaffoldStatus: '__REPLACE_WITH_FINAL_ITINERARY__',
  id: '__TRIP_ID__',
  title: '__TITLE__',
  shortTitle: '__SHORT_TITLE__',
  subtitle: '__ORIGIN__ 出发 · 手机优先 · 离线可读',
  dateLabel: '__START_DATE__—__END_DATE__',
  startDate: '__START_DATE__',
  endDate: '__END_DATE__',
  partySize: 2,
  currency: 'CNY',
  lastVerified: '尚未核验',
  routeText: '__ORIGIN__ → __DESTINATIONS__ → __ORIGIN__',
  summary: '请根据用户确认的行程，改写为一句能概括旅行主线和取舍逻辑的摘要。',
  budget: { perPersonLow: 0, perPersonHigh: 0, contingencyRate: 0.1 },
  phases: [
    {
      id: 'phase-1',
      name: '阶段一',
      dateRange: '__START_DATE__',
      summary: '替换为这一阶段的主线与节奏。',
      accent: '#d66b48',
    },
  ],
  rhythm: {
    transferDays: ['D1'],
    highDays: [],
    bufferDays: [],
  },
  highlights: [
    { label: '替换为不可砍的核心体验', status: 'core' },
  ],
  risks: [
    {
      title: '替换为最脆弱的交通或预订衔接',
      detail: '说明失败影响、备选方案和最晚确认时间。',
      level: 'high',
      needsRecheck: true,
    },
  ],
  route: [
    { id: 'origin', label: '__ORIGIN__', region: '出发地', lat: 31.23, lng: 121.47 },
    { id: 'destination', label: '__DESTINATIONS__', region: '目的地', lat: 35.0, lng: 100.0 },
  ],
  days: [
    {
      id: 'day-1',
      dayNumber: 1,
      date: '__START_DATE__',
      phaseId: 'phase-1',
      location: '__ORIGIN__',
      title: '替换为当天核心安排',
      summary: '只保留当天最重要的行动和目的。',
      intensity: 'transfer',
      hotelChange: true,
      overnightLocation: '待确认',
      needsRecheck: true,
      heroImage: '',
      imageAlt: '',
      schedule: [
        {
          time: '待确认',
          title: '替换为已确认交通或活动',
          detail: '补充到达方式、时长、预约状态与备选。',
          transport: '待确认',
        },
      ],
      stay: '待确认',
      food: [],
      notes: [],
    },
  ],
  guides: [
    {
      id: 'entry',
      title: '入境与证件',
      summary: '根据国籍、国家和出入境次数核验。',
      items: [
        { title: '待核验事项', body: '使用官方来源核验，并记录核验日期。', needsRecheck: true },
      ],
    },
    {
      id: 'equipment',
      title: '天气与装备',
      summary: '按海拔、温差、徒步与住宿条件组织。',
      items: [
        { title: '分层穿着', body: '在最终路书中替换为目的地和季节对应的装备建议。', needsRecheck: false },
      ],
    },
  ],
  budgetItems: [
    { id: 'transport', label: '大交通', low: 0, high: 0, scope: 'per_person', basis: '待核验' },
    { id: 'stay', label: '住宿', low: 0, high: 0, scope: 'per_person', basis: '待核验' },
  ],
  checklist: [
    { id: 'fixed-tickets', label: '核对所有已出票交通的日期、机场、航站楼和行李规则' },
    { id: 'dynamic-check', label: '临出发前再次确认动态班次、票价、入境和天气信息' },
  ],
  sources: [],
};
