# Interaction architecture for a growing guide

Use when Tools/My, editors, repeated navigation bugs or inconsistent spacing need repair. Preserve the existing product's design and scope. The examples below describe roles and contracts, not mandatory menu counts, routes, visual frameworks or a request to redesign the site.

## Give each action one home

| Concern | Suggested owner | Boundary |
| --- | --- | --- |
| Public field utilities | Tools hub | Independent tasks may open subpages; short related details may expand inside a task |
| Personal tickets and stays | Their own collection pages | Add/select/edit next to the records; avoid a second all-purpose profile editor |
| Generic equipment/checklists | Public utility reachable without login | Personal equipment and progress require the correct member scope |
| Account, synchronization and members | My/account area | Identity and connection status belong here, not repeated in the hero header |
| Offline/maps/updates and display/color | Discoverable settings entries | Same wording at entry and destination; avoid a redundant wrapper page |

Evaluate guest and signed-in paths separately. A guest must have a meaningful public destination from every generic packing entry. Do not show the owner's equipment while waiting for auth, after a fetch failure or through an export. Login may enrich a day with private records; it must not replace the whole day's public instructions with a sparse personal override.

## Collection actions and selection

Keep related Add and Select shared transport actions in a shared action row when they fit; allow accessible wrapping at larger text sizes. Select opens a bounded panel of ticket summaries and labeled checkboxes. Reuse the checklist row primitive when appropriate, but do not make a Details button part of the checkbox label. Scope generic input styles so text-field minimum heights do not inflate checkboxes.

Each saved item has one summary and an inline Details/Edit region. Add creates one draft; Cancel writes nothing; successful Save collapses only that item. Preserve the original row as a return anchor. After collapsing a long editor, retain the anchor when possible and allow natural scroll clamping when the page becomes short. Do not impose old pixel offsets that leave a blank screen or jump to the document top. Save only the edited collection/fields against the latest permitted state.

## Shared layout and navigation ownership

- Define page header variants, content widths, stack gaps, card padding, control heights, typography and safe-area ownership together. Full and compact headers must each reserve the status-bar inset; a return link should not create an accidental second hero header.
- Header height and hierarchy should be consistent for equivalent page levels regardless of login state. A compact detail return bar can remain sticky, but its controls must stay below the safe area, clear of content and keyboard focus.
- Use a shared stack or grid for sibling modules so newly inserted notices receive the same spacing. Long deadline text should wrap into a readable row/column; give flexible children min-width: 0 and test unknown-time labels as well as short clock times.
- Keep one scroll owner per transition: top-level navigation, sibling panel switch, previous/next day and return-to-item have distinct intents. A sibling switch should follow the chosen reading-position policy, without combining a global scroll reset with a second local adjustment.
- Bring an active day chip fully inside its horizontal rail, including direct links and previous/next navigation. Adjust that rail without scrolling the whole document. On short panels, use a deliberate minimum working area only when necessary to preserve the frame; do not add arbitrary screenfuls of blank padding.
- Fixed primary navigation should have a stable CSS viewport anchor and no document-scroll compensation. Test negative overscroll, browser chrome and keyboard separately. Inspect containing blocks before introducing visual-viewport offsets.

Disclosure triangles should rotate around a fixed center in a reserved icon box; switching Unicode glyphs with different metrics can shift the label. Use the separator contract below for card boundaries. Weather, account tiles, checkboxes and app pickers use the same semantic heading/content/action tokens across palettes and light/dark modes; adding a new module must not bypass the hierarchy.

## Content without duplication

Keep a single canonical Plan B slot. Merge public execution steps with personal records by section or stable IDs, not wholesale replacement. Compare all days before/after login: essential steps must remain, and identical fallback text must not appear twice.

Map city/date/route selectors should share an understandable hierarchy. When selecting a route means fitting its full extent, repeated selection can refit that route instead of adding an ambiguous global-route button. Use continuous displayed list indices for the current result set; keep stable point IDs and remove decorative numbering from place names.

An overview image should concentrate on date and actual route/activity. Align day, date and itinerary columns consistently; size the canvas to the content, wrap long routes deliberately, and avoid adding redundant intensity, recovery or transfer commentary. Follow the user's typography/palette choices. Public exports stay public-safe even when invoked by a signed-in member.

## Acceptance matrix

| Area | Cases | Observable result |
| --- | --- | --- |
| Header/nav | Every header variant; guest/member; narrow/wide; large text | Consistent hierarchy, visible return control, no overlap or overflow |
| Scroll | Top downward pull, normal long scroll, end bounce, keyboard, rotation | Primary navigation remains at its intended viewport anchor |
| Day/panel rail | First/middle/last day, direct URL, previous/next, long-to-short panel | Active chip fully visible; chosen top/restoration policy respected |
| Tickets/stays | Add, select, Details, Cancel, Save, long editor collapse | Separate selection/edit actions, one draft, stable return anchor |
| Public/private content | Every day and every packing entry before/after login | No private guest fallback, no lost essential public steps or duplicate Plan B |
| Tools/settings | Each hub tile, subpage return, accordion inside a task | Correct parent, matched labels, persistent state and consistent spacing |

Test observed outcomes rather than asserting that a compensating formula returns its own expected value. Responsive screenshots and synthetic viewport events cannot establish installed-iPhone bounce or safe-area behavior; report physical-device acceptance separately.

## Separator ownership

Use one shared rule for each header/content boundary. Fixed module headers and expanded disclosure summaries should use the same semantic divider color, thickness, content inset and following gap. In a disclosure, the summary owns this separator only when expanded; its body must not add a second border, background rule or pseudo-element at the same boundary. A local component must not add another line to compensate for spacing.

For an unboxed list directly below that boundary, row one has no leading divider; later siblings may have one inter-item divider. Keep independent card outlines, input borders and table grids: they express different boundaries and must not be removed by a blanket first-child reset. An action followed by an auxiliary disclosure normally needs shared spacing, not a separate rule above that disclosure. Keep these choices in reusable primitives or explicit layout roles, rather than accumulating page-name overrides.

Regression example: an expanded “Equipment” module contains folded “Day A / Day B” rows. Check one line below the module summary, no extra line above Day A, one between Day A and Day B, and one below an expanded day's summary. Also test a definition list and an image as disclosure bodies; neither should duplicate the summary line. Inspect computed borders, background images and pseudo-elements together, then inspect the rendered result.

## Navigation material and preview parity

If transparency is adjustable, derive actual top/bottom navigation and its preview from the same surface and blur tokens, child selected-state layers and component structure. Change the background tint, not whole-control opacity: text and icons retain contrast. An opaque selected tab can conceal the slider response even when the outer navigation backgrounds match. Preserve explicit accessibility overrides such as reduced transparency or increased contrast.

For a side-by-side comparison, use the same underlying image crop or neutral scene for both preview samples. Different scenery can look like different opacity. Preview overrides should only place controls in the sample; avoid importing live hide/show motion or introducing independent tint calculations. Verify intermediate values in both directions during actual input, comparing top, bottom and real navigation in the same frame. Include selected/unselected states and all offered palette/mode combinations. Stationary endpoint styles alone do not establish synchronized rendering; browser automation also does not establish an installed phone's compositor behavior.

## Settings descriptions

Match hub labels to destination titles. When users request a concise About section, retain one readable summary and put the detailed feature list behind a disclosure. Keep the update action ahead of secondary explanatory content when requested; do not turn one product's section names or ordering into a mandatory template. Bundle a public-safe changelog with offline content when offline access to it is promised, and keep it synchronized with the actual release.
