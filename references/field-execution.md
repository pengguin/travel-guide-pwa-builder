# Field execution contract

Use this reference when the guide is meant to answer questions in roughly ten seconds during the trip.

## Home status area

Prefer one compact field-status area over several cards that repeat the same transfer. It should answer:

- current stage or city;
- next concrete action;
- next transport, when applicable;
- next hard deadline;
- time remaining only when the device clock and deadline timezone are explicit.

Before departure, show the countdown above the D1 preview. During travel, select the actual calendar day. After the trip, show completion. A preview selection must never pretend to change the current date.

## Hard deadlines

A hard deadline is a departure, recommended leave-by time, check-in cutoff, reservation, closure or other time-bound event whose loss has a real consequence. Store it as structured data: local date/time, timezone, action, related segment, target arrival, source/basis and safety margin. Do not put rest advice, sightseeing preferences or “do not add more activities” in this field.

Derive the displayed deadline from the same transport/schedule record used by the day page. Avoid duplicated hand-written strings. When a time is an editorial safety recommendation rather than an operator cutoff, label it as recommended and preserve the official departure separately.

## Daily page structure

Use this order unless the brief requires another:

1. date, location, one-sentence purpose, intensity and compact luggage mode;
2. hard deadline;
3. timeline as the execution spine;
4. Transport Box for each true A-to-B move;
5. expandable operational details and private overlays;
6. Plan B;
7. matching previous/next day controls.

Merge a “today focus” or private reminder into the relevant timeline node when it repeats the same instruction. Do not reduce operational detail merely to shorten the page; move secondary explanations behind disclosure controls.

## Transport Boxes

Prefer concrete local times over “morning”, “later” or “about three hours early”. Include From, To, recommended method, duration range, suggested departure, latest safe departure, target arrival, cost range and cautions. For a station-to-international-airport connection, include exit time, meal/buffer window, road-time allowance and tiered delay responses.

For complex transfer days, provide normal, moderate-delay and significant-delay branches. Never let a plan assume the first leg is punctual when missing the onward segment would be costly.

## Proactive preparation

Show next-day preparation on the prior evening when it materially changes packing, baggage allowance, wake-up time, documents or transport. Use a calm preparation color, not the danger treatment, unless immediate safety is involved. Keep generic packing in the packing page; show only the day-specific delta in the itinerary.

## Tickets and on-site actions

Ticket cards may offer copy actions for service number, terminal/station, destination and full segment. Only show “view original” when an authorized attachment exists. Public cards must not leak personal prices, references or screenshots. Offline private attachments require prior authorized download and member-scoped storage.

## Map and print behavior

Map overlays belong to the map's own isolated stacking context. Align legend/location controls inside the map boundary and keep the entire map below global fixed navigation. Date chips should pair day number with a readable date wherever the same filter concept appears.

Each printable view owns a single print target. Invoke printing directly from the user's click. In `@media print`, hide application chrome and explicitly force the target, descendants, table cells and page canvas to white backgrounds and black text. Do not rely on inherited theme variables or temporarily print the live dark-mode page.
