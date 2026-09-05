# Planning mode

Use planning mode when the user supplies a destination idea, season, duration, or rough route rather than a locked day-by-day itinerary. The goal is a useful first guide with minimal interaction, not an exhaustive consultancy intake.

## Entry modes

- **Planning mode:** the itinerary is incomplete, ambiguous, or only a one-sentence idea. Normalize the request, ask only branch-changing questions, perform one bounded research pass, propose a route, and build the first guide.
- **Execution mode:** dates, route, or bookings are already substantially fixed. Treat the latest supplied facts as authoritative and proceed directly to implementation, asking only about a genuine blocker.
- **Update mode:** an existing guide is named. Preserve project identity and unchanged content; reconcile the requested delta against the canonical data model, then rebuild and release the whole deployable artifact.

Do not require a reference guide or a fully specified itinerary in any mode.

## Five-stage intake ceiling

Ask at most five decision stages before producing the initial plan. Combine related questions in one compact prompt. Skip any stage already answered, infer safe defaults when the answer will not materially change the trip, and never repeat a question.

1. **Trip frame:** departure region, date or date window, duration, party size, and fixed transport/self-drive constraints.
2. **Route priorities:** must-see places or experiences, exclusions, and pace preference.
3. **Cost and comfort:** approximate per-person or group budget, room standard, and tolerance for long transfers/early starts.
4. **Operational needs:** mobility, children/older travelers, weather tolerance, visa/passport constraints, dietary or health needs that affect the route.
5. **Delivery and privacy:** local-only or ChatGPT Sites; public-only or optional personalized mode. Explain briefly that personalized mode requires authenticated/server-authorized storage and extra setup.

If the user does not answer optional questions, use declared defaults and list them visibly in the draft. A good default is a balanced pace, mid-range stays, public-only guide, and dynamic facts marked for recheck. Do not block a first draft for restaurant taste, exact hotel, styling preference, or other choices that can be edited later.

## Lightweight research pass

Before laying out the route, verify only facts capable of invalidating the plan:

- entry or self-drive constraints;
- operating-day or seasonal-closure risk for the anchor experience;
- feasibility of the longest or most fragile transport legs;
- realistic travel time between overnight bases;
- one or two price anchors needed to test the budget.

Prefer three to five targeted primary-source queries or page checks in one pass. Reuse supplied confirmed bookings. Do not research a complete catalog of hotels, restaurants, ticket prices, and attractions before the first guide exists. Mark unresolved or future-dated facts as `需临出发前再次确认` and attach a check deadline.

Use a second research pass only if the first pass exposes a material conflict such as a closed road, impossible connection, border limitation, or budget failure.

## Normalize and produce

Create a draft trip model before UI work:

1. identify immutable facts, dynamic facts, editorial choices, and assumptions;
2. group the trip into three to five phases;
3. select overnight bases and minimize backtracking;
4. assign one primary purpose to each day plus buffers around fragile legs;
5. expose the three largest risks and a Plan B for each;
6. estimate a range with explicit party-size and paid/unbooked assumptions;
7. generate the guide using the same production content model and QA gates as execution mode.

The first delivery should already be usable: route overview, daily plan, transfers, map/list, stay-area guidance, packing/risk notes, budget range, recheck items, and the chosen publication/privacy boundary. Label it as a planning draft until fixed tickets and accommodations are reconciled.

## Personalization decision

`Public-only` is the default for fast planning. It contains shareable itinerary and practical information with local guest preferences/checklists only.

Enable `personalized mode` only when requested. Keep its data contract generic and server-authorized: member identity, personal tickets/stays/packing, access-code membership, expiry/renewal, sync, and member-specific offline storage. Do not seed a generated guide or reusable repository with a real traveler, access code, booking, or private attachment.

## Efficiency rules

- Prefer one structured question containing 2–4 short fields over serial micro-questions.
- Give a recommended answer or safe default where useful.
- Do not ask about decisions the route can defer.
- Do not search broadly for inspiration after the route is already feasible.
- Build from normalized records; do not spend tokens composing long travel essays.
- State assumptions and recheck items rather than pretending future schedules are confirmed.
