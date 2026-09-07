---
name: travel-guide-pwa-builder
description: Build or update a mobile travel guide PWA or travel website, from a rough trip idea or an existing itinerary. Use for an explicitly requested website/PWA deliverable; not ordinary travel advice, PDF-only work, or a single-file HTML request.
metadata:
  version: "2.4.0"
---

# Travel Guide PWA Builder

Build a travel guide that remains useful on a phone during the trip. Preserve fixed facts, isolate dynamic claims and private records, keep the interface scannable, and distinguish tested behavior from implementation intent.

## Choose the request mode

1. **Planning mode:** for a rough idea such as “今年十一去某地自驾”. Read [planning-mode.md](references/planning-mode.md). Ask no more than five compact decision stages, perform a bounded feasibility check, normalize a draft itinerary, and deliver an initial guide. Do not wait for the user to write a detailed route.
2. **Execution mode:** for a substantially fixed itinerary or booked transport. Lock supplied facts and proceed directly; ask only if a missing choice would materially change the result.
3. **Update mode:** for an existing guide. Apply the newest explicit facts as a scoped delta, preserve immutable bookings and member edits, synchronize dependent views and rebuild the complete release. Read [itinerary-updates.md](references/itinerary-updates.md) for multi-day changes, day tours, recovery and base-hotel logistics. Retire obsolete active advice while preserving historical notes and real bookings until the user changes them.

A reference sample is optional in every mode. If optional answers are missing, use safe declared defaults and continue.

## Choose the implementation path

1. Inspect the workspace before editing.
2. Reuse the user's existing guide framework when one is named or clearly established. Preserve its information architecture and interaction patterns unless the user asks for a redesign.
3. For a hosted guide, a project containing `.openai/hosting.json`, or requested accounts/server synchronization, read [sites-workflow.md](references/sites-workflow.md). Use the currently installed official `sites-building` and `sites-hosting` skills, including their required references. Preserve existing project identity. Sites is the only built-in publishing workflow; do not add or fall back to EdgeOne or another provider.
4. For an explicitly local/portable guide without a server, read [standalone-mode.md](references/standalone-mode.md) and run `scripts/create_project.py`. This dependency-free starter has no authentication or cloud synchronization. A reference sample or finalized itinerary is never required; planning mode may populate the starter after route normalization. Do not turn its static files into a mock secure login.
5. For single-file HTML, handle the requested artifact directly with available tools; for print-first PDF, use the active official PDF skill. Do not require the removed travel-guidebook or travel-plan-viz skills.

For an existing guide, the live project's normalized records, routes, styles, tests and release contract are the ground truth for that instance. The reusable skill is a method and invariant checklist, not a generator that may overwrite a newer application architecture. Read [architecture-and-maintenance.md](references/architecture-and-maintenance.md) before broad refactors or before feeding lessons from a real project back into this skill.

## Read only the required modules

- Mobile layout, home state, forms, maps, navigation or tools: [mobile-experience.md](references/mobile-experience.md).
- Field execution, deadlines, daily-page deduplication, transfers and next-day preparation: [field-execution.md](references/field-execution.md).
- Accounts, access codes, ticket/booking uploads, personal editing or sync: [member-data.md](references/member-data.md), then the official Sites authentication and storage references.
- Offline or startup work: [pwa-offline.md](references/pwa-offline.md).
- New destination palette: [destination-theming.md](references/destination-theming.md).
- Reusable skill/GitHub handoff: [privacy-and-publishing.md](references/privacy-and-publishing.md).
- One-sentence idea, incomplete itinerary, or route planning: [planning-mode.md](references/planning-mode.md), then [research-and-risk.md](references/research-and-risk.md).
- Local runtime, network boundaries, Sites dependency or hosting portability questions: [environment-and-deployment.md](references/environment-and-deployment.md).
- Cross-page refactors, regression prevention, release identity, or updating the skill from a completed guide: [architecture-and-maintenance.md](references/architecture-and-maintenance.md).

When updating this skill from a real guide, extract behavior and data contracts, not the guide's source tree, database, assets, account settings, or deployment manifest.

## Lock the brief before research

Convert the request into three lists:

- **Immutable facts:** dates, booked flights, arrival airports, companions, non-negotiable destinations, fixed activities, stated budget target.
- **Dynamic facts:** flight schedules not yet booked, train timetables, visa and registration rules, ticket-release windows, prices, opening hours, weather, transit benefits.
- **Editorial choices:** optional sights, daily ordering, restaurant and hotel recommendations, visual theme, depth of appendix material.

Never silently change an immutable fact. If supplied details conflict, call out the conflict and use the newest explicit instruction. Read [research-and-risk.md](references/research-and-risk.md) before verifying transport, entry, registration, or other time-sensitive claims.

In planning mode, collect the minimum branch decisions first, then promote accepted assumptions into the same three lists. Keep the first research pass to the plan-invalidating facts defined in `planning-mode.md`; depth can grow after the user reviews the initial route.

## Build a normalized content model

Keep content in data modules or JSON-like records rather than embedding itinerary facts throughout components. At minimum model:

- trip identity and date range;
- phases and route summary;
- days and daily schedule nodes;
- places and map coordinates;
- transport segments and booking status;
- accommodation and food recommendations;
- budget scenarios and assumptions;
- practical guides, sources, verification dates, and recheck flags;
- image metadata and credits.

Use stable IDs and derive repeated labels, counts, route filters, and totals from the same records. Read [content-model.md](references/content-model.md) for the required fields and invariants.

## Research and evidence rules

1. Search current primary sources for dynamic or high-risk facts. Prefer immigration authorities, transport operators, airport and airline pages, railway operators, official attraction sites, and accommodation properties.
2. Treat a ticket screenshot or user-supplied booking confirmation as authoritative only for that booked segment. Do not extrapolate a current schedule from an old screenshot.
3. Record `sourceUrl`, `verifiedAt`, and a concise `uncertaintyNote` where relevant.
4. Mark schedules, prices, visa rules, ticket windows, and weather-sensitive operations as “需临出发前再次确认” in the UI.
5. Distinguish confirmed facts, planning assumptions, and recommendations visually and in the data.
6. Never invent a flight, train, hotel benefit, visa exemption, border rule, rating, opening hour, or price.

## Design the information architecture

Make the first screen useful within about ten seconds. For a field-use guide, combine current stage, next action, next transport and next hard deadline into one compact status area; keep the three most important actions nearby without restating the same transfer in several cards. A hard deadline is a real time-bound departure, check-in, reservation or closure—not advice such as “rest early”. Keep the full route, budget and research detail on dedicated pages. For a planning-first guide, an overview may lead instead. Follow the user's stated hierarchy rather than forcing both modes onto one crowded home screen. Read [field-execution.md](references/field-execution.md).

Recommended sections:

1. Home: top-level countdown before departure, actual current day during travel, completion state afterward. Never label the departure-day preview as today. Include a compact, public-safe whole-trip summary suitable for sharing.
2. Itinerary: one expandable card per day with date, place, core plan, transport, hotel change, and intensity visible before expansion.
3. Map: route and place layers with usable mobile controls and a non-map fallback list.
4. Transport: fixed tickets, unbooked segments, transfer logic, booking deadlines, alternatives.
5. Stay and food: shortlists tied to neighborhood and day, not generic city dumps.
6. Guides: entry, registration, money, communications, equipment, health and safety.
7. Tools: collapsed, labeled modules for checklists, budget, emergency details, preferences and calendar; show useful progress in summaries rather than a long expanded page.
8. My (when accounts are requested): sign-in, personal tickets, packing, stays, sync and role-appropriate member management. Keep public reading available when the user requests a public guide.

Place settings under My even for guests. Separate them into compact **Function settings** (updates, offline state, map provider, exports) and **Appearance settings** (font size, color mode, destination palette, visual style). Do not advertise unimplemented visual systems as selectable features.

On long mobile sections, use a compact sticky sub-navigation for the current day or module. It must remain below the shared safe-area inset and must switch real in-page panels without accidentally navigating to Home. In landscape, reduce decorative header depth and reorganize operational content into columns; do not merely stretch portrait cards across the viewport. A right-side primary navigation is appropriate when it materially increases vertical working space.

For sibling day/module switches, preserve the current reading frame; bottom previous/next may return to the sticky frame anchor but not the document top. Keep one scroll owner per transition. For editable ticket/stay collections, use compact saved summaries with an explicit Details → inline edit → Save/Cancel flow, and keep selection hit areas separate from editing actions.

Use large type, strong hierarchy, generous spacing, restrained colors, and complete images. Put secondary detail behind expandable sections. Do not turn the main view into a dense article or thin-line table.

## Adapt the visual theme to the destination

Derive the palette from the destination's landscape, built environment, materials, climate, and travel mood rather than reusing one house palette or copying flag colors. Keep semantic roles stable (`paper`, `surface`, `ink`, `primary`, `secondary`, `highlight`, `soft`, `danger`) so components and contrast behavior remain reusable. Use one dominant dark color, one restrained accent, and neutral surfaces; destination character should come from color, imagery, and small material cues, not decorative clutter.

When using the standalone starter, pass `--theme auto` or choose a named family with `--theme heritage|desert|mountain|coast|forest|tropical|polar|urban`. Auto selection is a starting point, not evidence about a place. Review the chosen palette against the actual itinerary and override the family when the destination's visual identity differs from the name heuristic. Read [destination-theming.md](references/destination-theming.md) before creating a new destination theme or substantially recoloring an existing guide.

## Media rules

- Prefer local, optimized assets in the release bundle so the guide works offline.
- Use one relevant image per card or place. Never reuse one scenic photo to represent different locations.
- Check binary hashes for duplicates before release.
- Store source, creator/license status, and alt text for every externally sourced image.
- Do not commit user screenshots, boarding passes, faces, booking references, personal cloud paths, or private images unless the user explicitly asks and understands the publication scope.
- Use generated or license-compatible neutral artwork for app icons. Verify maskable icons at common mobile crops.
- Documentation screenshots must show the real interaction model. The first planning screenshot begins in the Codex conversation that invokes the skill, not inside a PWA that does not exist yet. When documentation is bilingual, capture strict Chinese/English counterparts with the same layout and synthetic content.

## Budget model

Show both per-person and group totals when party size matters. Separate fixed paid costs, quoted or observed costs, estimated ranges, contingency, and exchange-rate assumptions. Derive totals in code and expose the few cost levers that materially change the result. Do not present a target budget as a verified total.

## Implement and verify

Keep presentation components generic and itinerary content in data. Update coupled elements together: navigation, phases, dates, map filters, calendar export, manifest, service-worker cache name, icons, page title, budget totals, and source list.

### Cold start and offline invariants

- Render a local App Shell or meaningful launch shell before framework hydration or route chunks finish. Do not use a loading animation to hide an empty root.
- Bundle only public itinerary, generic transport/stay/packing notes, emergency information and public media. Core public reading must not wait for an API, remote font, map tile, or weather request. Private tickets, booked hotels and attachments must be fetched after server authorization, then optionally stored in an isolated per-member offline store; never put them in public assets or a shared precache.
- Register the service worker after the first render; registration and activation must not block the App Shell.
- Precache every core HTML/CSS/JS chunk, local image, icon, manifest, and offline fallback. If chunks are discovered only after build, generate the precache list from the final build output.
- Account for `Vary` on verified public static assets only. Never ignore identity/cookie variation on private responses or cache authentication endpoints.
- Version caches per release, remove only caches owned by the guide, and prove that a new release replaces stale entry HTML and chunks.
- Make the visible offline recheck self-healing while online: refresh the current precache through the controlling worker, then verify the exact current-release cache and update the check timestamp. A matching release ID does not prove the cache is complete.
- Do not automatically call `skipWaiting()` from `install` for a hashed, code-split app. An old open page may still request old lazy CSS/JS after the new worker deletes its cache. Let the installed worker wait until old clients close, or activate it only after an explicit version-update action; preserve the old release caches until activation is safe.
- Hash routing or a host rewrite must support standalone `start_url`, nested-route reloads, and subpath deployments. A relative `base`, `scope`, and `start_url` must agree.
- Online-only features such as map tiles and real-time weather must fail locally and visibly without crashing the guide.

Read [pwa-offline.md](references/pwa-offline.md) whenever the request includes offline use, iPhone Add to Home Screen, a white startup screen, service-worker changes, or a deployable PWA release.

Before delivery:

1. Run the project's production build.
2. Run `python3 scripts/audit_travel_guide.py <project-path> --release` from this skill directory. The auditor recognizes static and Sites/Vinext public output; use `--public-dir` for another layout and `--source` for a separate source-tree scan. It does not test authorization or browser behavior. The standalone starter intentionally fails until its final-itinerary marker is removed.
3. Search globally for retired destination names, dates, stale route labels, placeholder text, private paths, and old cache keys.
4. Preview the production build, not only the development server.
5. Run automated content, date, permissions and release checks. When browser QA is requested/authorized, test desktop/mobile routes, expandable content, maps, navigation, reload, offline cold start and overflow. Follow official Sites browser-testing rules; otherwise report browser and physical-device checks as untested.
6. When browser QA is authorized, exercise every selected/unselected/disabled/focus state in both light and dark modes. Check controls over map tiles, floating controls, warnings, active filters, inputs, and navigation against semantic theme tokens rather than one-off colors.
7. When browser/system QA is authorized, print each supported itinerary/checklist view from its explicit user action. Printed pages must force white surfaces and black text independent of the selected screen theme; a mobile print action must not be invoked again by timers or lifecycle effects.
8. When browser QA is authorized, verify the install icon and PWA manifest on a mobile-sized viewport. For a physical iPhone requirement, repeat on the deployed HTTPS URL and state explicitly if that step remains untested.
9. For a requested portable ZIP, package public static deploy contents at archive root. For Sites, use its current official packaging helper and contract; a server-backed Sites archive is not interchangeable with a static ZIP.

Read [qa-and-release.md](references/qa-and-release.md) for the complete release gate.

## Privacy-safe handoff and publishing

Read [privacy-and-publishing.md](references/privacy-and-publishing.md) before creating a reusable template or pushing to GitHub.

- A request to update this skill or push its GitHub repository does not authorize changing or publishing the personal Site used as reference.
- Follow the official Sites publication and access-approval gates for website builds; honor local-only requests. Reuse the named Site, and never silently change its access policy.
- Default to the narrowest safe scope and preserve existing repository visibility.
- For a new repository with unspecified visibility, pause for a choice unless a private default has already been agreed.
- Before pushing, inspect the staged diff and run the privacy audit. Exclude `.env`, credentials, local absolute paths, user names, account identifiers, booking codes, ticket images, build caches, and `node_modules`.
- Report the repository URL, commit, visibility, validation results, and any dynamic facts still requiring recheck.

## Delivery contract

For hosted work, return the verified Sites URL using the official handoff. For local-only work, return the runnable project/preview and portable ZIP when requested. Summarize changes, offline coverage, online-only functions, untested areas and remaining user confirmations. Include a plain-language travel-information disclaimer in the guide or handoff where appropriate. Push GitHub only when authorized. Do not claim end-to-end completion from a successful build alone.
