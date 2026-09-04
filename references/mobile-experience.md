# Mobile interaction contract

Apply relevant features to the requested guide, not a fixed copy of another trip. The standalone starter includes a subset; implement Sites account features only when requested.

## Home and calendar state

Put countdown/status above the daily card. Before departure show '距出发还有 N 天' and label D1 as a departure-day preview. During travel show '旅程第 N 天' with the matching date's record; after return show completion, not D1. A manual day preview must not pretend to change today's date.

Use explicit calendar-date arithmetic, not elapsed milliseconds divided by 24 hours across DST. Default to device-local date unless the user requests a fixed trip timezone; document that choice. Refresh after local midnight, resume/focus and visibility changes without losing form edits or scroll. Test before/start/middle/end/after, month/year boundaries and DST. Flight times remain airport-local and separate from the home date policy.

Keep the field-use home to today's city, three actions, next transfer and next hard deadline. Lower down add a compact phase-grouped overview with dates, cities, main activity and overnight/transfer markers. Shareable screenshots/export must omit private tickets, prices, names and booking references even for signed-in users.

## Navigation and density

- Use recognizable consistent icons with labels: home, calendar, map pin, guidebook, tools, person. Do not use arbitrary text glyphs as icons.
- A reasonable primary navigation is Home / Itinerary / Map / Guides / Tools / My. Adapt to scope. Public guide content remains available without login; My owns login and private ticket/packing/stay/member functions when enabled.
- Every day detail ends with matching Previous/Next buttons; endpoints are visibly disabled. Put shared button styles in global CSS, not a lazily loaded page stylesheet.
- Editor back links go to the actual parent route with validated same-origin return targets. Preserve filters/scroll or the selected member. Avoid a universal 'Back to Tools' on every depth.
- Provide a labeled back-to-top control on long pages, clear of the bottom bar and safe area; hide during text entry and near the top. Respect reduced motion.
- Tools uses a small set of collapsed native details or accessible accordions. Summaries show title, one-line purpose and current progress; details preserve state. Printing must include intended collapsed content without printing duplicate hidden copies.

## Consistent typography and safe areas

Use one shared opaque header/safe-area background token on all routes, no mismatched gradient at the status bar. Apply top inset once; check that standalone padding is not doubled by body, header and page. Account for bottom inset and keep keyboard focus visible.

Use system fonts. Font preferences small/medium/large apply through global tokens to cards, controls, summaries, map-app picker and nav, not only paragraphs. Form inputs/selects/textareas must compute to at least 16 CSS px on iOS, including the small setting, to avoid focus zoom. Do not disable user pinch zoom. Set box-sizing, width/max-width, min-width:0 and grid minmax(0,1fr) so date controls and long labels do not overflow. Date inputs need the same padding/height as other fields, checked on WebKit rather than assumed from desktop Chrome.

## Maps and guide filters

Derive city, date and type filters from actual records; omit categories with no content. For conflicting combined filters, show a useful empty state and clear action. City and date can occupy two compact horizontal rows.

After filtering, update both features and viewport: multiple points fitBounds with padding; one point gets a bounded zoom; zero points does not fit invalid bounds. Preserve a usable offline list. Route lines indicate order only unless a real routing service supplied road geometry.

Use one map-link resolver for all 'view on map' links, including deep guides and booked stays. Apply the user's chosen provider and validated latitude/longitude order. Consult current official provider link documentation and test a real destination. Opening 2GIS or another app alone does not prove that a pin/navigation target was passed. Prefer documented web/universal links with fallback; expose copy address/coordinates when app links or regional coverage fail. Do not claim offline turn-by-turn navigation from cached website content.

## Checklists and planning deadlines

Separate packing and preparation, each with categories, editable custom items and its own clean print view. Use stable item IDs, local persistence for guests and member-scoped sync only when authorized. Keep named personal gear out of generic defaults.

When requested, model reverse-planning tasks with a due date or offset from departure, editable deadlines, completion and reminder offset. Calendar export uses stable UIDs, proper escaping/folding, timezone-aware timed events or correct all-day dates, and explicit alarms if requested. Test import/update in the target calendar; exporting an ICS does not guarantee notifications or automatic subscription updates. Keep private calendar exports opt-in and out of public bundles.

## Test boundaries

Use unit tests for date/state/filter logic and permission tests for private data. Follow official Sites restrictions on browser QA and obtain missing user authorization if needed. Responsive emulation cannot prove physical iPhone keyboard zoom, standalone cold-start, safe-area, cache retention or installed map-app links. State untested device behavior clearly.
