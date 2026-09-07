# Updating an existing trip without redesigning the guide

Use this workflow for multi-day route changes, fixed tickets, day tours and base-hotel logistics. Preserve the existing project architecture and the user's chosen scope.

## Establish the delta and authority

Separate three kinds of information before editing:

- Immutable booked segments: supplied service/date/local time/terminal/station and private booking records. Public timetable searches do not override the user's purchased tickets. Flag contradictions instead of silently fixing a booked time.
- High-priority experiences: a named operator product, personalized city theme, or required activity. A similarly named standard tour is not an equivalent substitute.
- Flexible support: meal choice, hotel candidate, sightseeing order and optional stops. Optimize these around departures, luggage, sleep and recovery.

Keep booked records separate from public recommendations. The user may explicitly authorize public operating times or equipment categories without authorizing prices, references, attachments or identity. Apply field-level disclosure to the Site; use wholly synthetic examples in the public skill.

Historical development notes and immutable booking records are not retired advice. Remove obsolete content from active views and indexes; retain history and do not cancel an actual reservation without authorization.

## Synchronize the whole itinerary

Inventory every consumer of the date/route before editing: trip summary, phase labels, daily nodes, deadline cards, transport, restaurants, hotels, map points/lines, sight-guide dates, packing and prior-evening reminders, budget, checklists, calendar export, offline manifest and changelog. Preserve the route's dates and total day count unless the user changed them.

Use existing stable record IDs where the meaning remains the same. Give a replaced task a new ID, or use content/revision-aware identity, so an old completed checkbox does not silently mark a new obligation complete. Keep user-added items, edited due dates and member state distinct from generated recommendations.

Validate coupled facts programmatically where practical: one daily record per calendar date, intended overnight counts, fixed transport times, valid node IDs and order, meal/stay coverage, active guide dates and calendar events. Snapshot only immutable fields; do not put real private records into test logs or public fixtures.

## Fit food and hotels to the route

For an operational guide, group food by day and meal rather than a long city ranking. A useful default is one primary and one backup per meal. Explain location/transfer fit, planned arrival, meal duration, rough local-currency budget, hours, wait/booking decision and dishes. Clearly distinguish estimated budget from a quoted menu. Review recency and sample size matter; do not advertise a stable rating from a few old reviews.

A hotel candidate is not a confirmed booking. Select around the next departure: a very early pickup may outweigh a sea view or central tourist district. State the actual pickup address and whether walking, a taxi or a booked transfer is required.

For a repeated base hotel, distinguish:

- a day tour while the room remains booked (luggage stays in the room);
- storage after checkout across two separate reservations;
- exact drop-off/pickup dates, fee, receipt, responsibility and collection hours;
- early arrival, late arrival, breakfast box and early checkout requirements.

A property advertising luggage storage does not prove it will store bags free during a multi-day absence. Make that condition a booking prerequisite when the route depends on it. Preserve existing insurance/backup hotel reservations as private records until the traveler chooses to change them.

## Recovery and the prior evening

After a long overnight arrival or very early day tour, leave genuine slack rather than relabeling a full day as recovery. Mark optional activities as removable. A late-return tour followed by a booked early flight can still leave inadequate sleep even after optimization; expose the remaining constraint and operator confirmation needed.

Move unavoidable preparation before the long tour: packing/weighing, clothing, settlement, airport car, breakfast and alarms. Avoid a plan that relies on midnight shopping or a full repack after a fourteen-hour day. Do not move booked transport to create artificial slack.

## Map fidelity

Use actual map tiles and verified coordinates. Link city-route presets to the existing node IDs; include dinner, luggage retrieval and the departure station when they are part of the execution route. Lists, markers, popup time/action and route lines must share the same records.

Straight lines and directional arrows show sequence, not roads; label that explicitly. Distinguish walking, car and actual rail/metro segments. Visiting a metro station and leaving by the same entrance does not justify drawing a train ride. Unknown points break a line and remain in the text list; do not infer a precise parking point from a building or regional coordinate.

Do not extend this workflow into new encyclopedic guides, new reservations, a visual redesign or a template rewrite unless requested. Finish with the changed dates, removed active advice, new recovery days, meal/hotel/storage logic, verified operator information and unresolved order-specific questions.
