# Architecture and maintenance discipline

Read this reference for broad UI repair, an existing guide with several accumulated patches, release/version problems, or updating this skill from a production project.

## Avoid the skill–project circularity trap

There is no circular dependency when the roles are explicit:

- the **project** is the source of truth for its own itinerary, data, routes, runtime, visual system, permissions and current release;
- the **skill** is a reusable planning method, architecture contract, source hierarchy and regression checklist;
- a **starter** is only a bootstrap artifact and never has authority to overwrite an evolved project;
- verified lessons move from a project back into the skill only as generalized invariants, neutral fixtures and tests.

Never repair a mature guide by regenerating it from the currently installed skill. Inspect the project first, identify the owning abstraction, and patch that abstraction. An older skill may be incomplete, but it must not force the live app backward. Conversely, do not copy a production app wholesale into the skill: that would carry destination-specific structure, dependencies and possibly private data into a reusable public package.

## Root-cause workflow

1. Reproduce the failure in the exact context that matters: route, orientation, installed PWA/browser, color mode, account state and offline state.
2. Trace the failure to the shared owner: application shell, safe-area token, layout primitive, route-state contract, print target, map instance, normalized record, service worker, or authorization boundary.
3. Define the invariant before editing. Examples: “map panes never exceed the map stacking context”, “a detail return restores the exact originating node”, or “a print action remains in the original user gesture”.
4. Fix the shared owner and remove local compensating margins, z-index inflation, duplicate route state or one-off color overrides that conflict with it.
5. Test the representative matrix, then search for other consumers of the same primitive.
6. Only after the project fix is validated, add the invariant and a neutral regression case to this skill.

## Application-shell invariants

- Apply each safe-area inset exactly once through the shell. Sticky sub-navigation uses the shell's computed top offset; fixed bottom or side navigation owns its corresponding inset.
- Give the bottom/side primary navigation an explicit layer. Content, map panes, legends, floating controls and back-to-top controls stay below it.
- Use semantic layout breakpoints. Portrait uses a fixed hand-friendly map height; landscape may use an equal-height map/list workspace and a vertical primary navigation.
- Reduce landscape header and page gutters. Use two columns for operational pairs such as map/list, summary/deadline, or form/navigation when it improves scan speed.
- Centralize header, card, button, selected, disabled, warning, print and dark-mode tokens. Do not repair contrast with isolated page selectors.
- Keep back-to-top controls visually subordinate: transparent or translucent, borderless, safe-area aware and clear of primary navigation.

## Route and return-state invariants

- Sticky tabs represent true panels. Changing a tab must update only the intended nested route or view state; it must not fall through to the application's default route.
- Carry a validated return contract: parent route, filter state, scroll item ID and optional schedule-node ID. Store stable IDs, not pixel offsets alone.
- A guide opened from an itinerary node returns to that node. A guide opened from a filtered list returns to that list item and keeps the filters.
- Deep links and browser Back must produce the same logical parent when possible. Reject external or malformed return targets.

## Map and orientation invariants

- Map markers, list entries, filters and route lines derive from the same normalized records.
- Do not rotate a live map with CSS transforms to simulate landscape. Visual coordinates and pointer coordinates diverge, producing drag and tap errors.
- Use automatic responsive layout by default. Add manual fullscreen/orientation controls only when requested and supported; explain any device limitation.
- After layout, fullscreen or orientation changes, wait for the new box size and call the map library's size invalidation method.
- Keep legend, orientation and locate controls in a single map-owned control row. Align height, typography, surface and focus states. For repeated point actions, a fixed grid may reserve an inert optional slot so the first three actions never shift between rows.
- A remote tile provider is an online enhancement, not the route database. Offer a second provider when useful, retain attribution, and preserve an offline point list. Do not promise uniform regional reachability or offline tiles unless tested and licensed.

## Print invariants

- `window.print()` must remain a direct consequence of the user's click. Do not open a helper page and then attempt an automatic print from an asynchronous event.
- Prefer a same-page print target: set a target attribute/class synchronously, call print, and clear the target on `afterprint`. Do not clear it with a short timer because iOS may render the print preview later.
- In `@media print`, explicitly set the page, body, target, cards, rows, headings, links, table cells and form text to white backgrounds and black text. Hide fixed navigation and floating controls. Elements hidden with visibility alone still occupy layout space; check page count and remove hidden ancestors from print layout so blank trailing pages do not remain.
- Test each print target separately in light and dark screen modes. A successful itinerary print does not prove the checklist or packing target.

## Collection-editing invariants

- Use one interaction grammar for editable tickets, stays and similar collections: compact saved summary, explicit Details, inline editor, Save/Cancel, then collapse after a successful save.
- An Add action creates one draft and scrolls only far enough to reveal that editor. Do not append a full empty form to every saved item.
- Keep selection and editing distinct. A Details action must not toggle its checkbox; constrain the selection hit area to the checkbox and its label text.
- Shared itinerary records may receive member-scoped field overrides, but must retain stable shared IDs and server-side field allowlists.

## Release identity and rollback

Maintain three separate identities:

1. a human-readable product version;
2. a unique machine release/build ID that changes for every deployable asset set;
3. a service-worker cache name derived from the machine release.

The update UI compares a machine-readable release manifest, not only the display version. A maintenance deployment may preserve the display version but must still receive a new build ID and cache key. Keep an immutable, tested baseline tag before broad changes, and record the exact hosted version/commit so rollback does not depend on reconstructing old source.

## Feeding improvements back into the skill

Before publishing a skill update:

- translate the fix into an implementation-neutral invariant;
- create synthetic tests or documentation examples;
- remove all real dates, bookings, names, equipment, access codes, provider credentials, local paths and deployment IDs;
- keep Chinese and English documentation structurally paired;
- render documentation screenshots as raster browser captures from neutral demo data;
- validate the skill and its starter independently of the production guide.
