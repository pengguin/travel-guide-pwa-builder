# QA and release gate

Use this checklist for every deployable handoff.

## Content reconciliation

- Compare the rendered day count, dates, route order, hotel nights, and fixed tickets with the final user brief.
- Search the complete source tree for retired dates, destinations, flight numbers, budgets, names, and headings.
- Confirm optional items, assumptions, and dynamic facts carry the correct labels.
- Confirm sources directly support the claims attached to them.

## Asset checks

- Resolve every local image, icon, manifest icon, and social preview asset.
- Hash raster assets and inspect duplicates. Repetition is acceptable only for intentional brand assets.
- Check image subject, crop, alt text, dimensions, compression, and credit record.
- Test maskable icons at square, circular, and rounded-square crops.

## Build and browser checks

Always run applicable automated checks. For Sites, perform browser UI QA only when explicitly requested, following the official Sites skill; otherwise include the items below as an untested checklist, not claimed results.

- Run the production build with a clean exit.
- Serve the production output locally.
- Test at least one narrow phone viewport and one desktop viewport.
- Open every primary route and representative detail page.
- Reload nested routes; verify routing survives static hosting.
- Exercise expandable cards, filters, map layers, navigation, calculators, and calendar export.
- Inspect console errors, failed requests, broken images, and horizontal overflow.
- On a fresh origin, visit only the home route, wait for service-worker installation, then stop the local server or enable browser offline mode. Reload and open several previously unvisited lazy routes. This distinguishes true precache from runtime caching of pages already visited online.
- Include at least itinerary, tickets/transport, packing or tools, hotel/food, emergency information, and the map fallback in the offline route sample.
- Restore the server/network, reload, and confirm the current release replaces stale entry HTML and chunks without console errors.
- With an old release page still open on a lazy route, install a new release and navigate again before activating it. Confirm the old page does not show a missing CSS/JS chunk error. Then use the explicit version-update action or close all old clients and confirm the new worker activates cleanly.
- If the project uses lazy CSS/JS chunks, verify offline requests hit precache even when responses carry `Vary: Origin`; test the actual preview server rather than assuming URL equality is sufficient.
- Confirm page title, manifest name, theme color, icons, and service-worker cache version match the current guide.
- For iOS/Add to Home Screen, check `apple-mobile-web-app-capable`, status-bar style, touch icon, safe-area viewport, `display: standalone`, `start_url`, `scope`, and standalone navigation behavior.

## Cold-start evidence

- Inspect the raw entry HTML: it must contain a meaningful local launch/App Shell, not only an empty framework root.
- Confirm core rendering does not await remote fonts, map tiles, weather, or API data.
- Record whether the test was a desktop/browser simulation, a deployed-domain test, or a physical iPhone test. Never describe a local preview or stopped-server test as a physical Add-to-Home-Screen result.
- A short local launch shell is acceptable; a long blank screen followed by content is not.

## Release archive

The following flat ZIP rules apply to portable static output. Sites publication must instead use the official packaging helper with its current Worker/static contract, metadata and migrations. The included static audit is not a Worker runtime or authorization audit.

- Build output should contain the entry HTML, manifest, icons, service worker, and versioned assets.
- ZIP the contents of the deploy directory at archive root; do not wrap them in an extra project folder unless the host explicitly requires it.
- List the archive and perform an integrity test.
- Record the archive path, size, checksum, build command, and preview command.

## Mobile and member regression matrix

- Clock: before departure, D1, D2, final day, completed trip, local midnight/resume, timezone and DST; preview is not presented as today.
- Navigation: every day has matching previous/next buttons, endpoints disabled; editor returns one level; My routes gate private information only; back-to-top does not obscure inputs; guide details restore the originating list item and expose the next guide.
- Tools: summaries show live progress, all modules expand/collapse by keyboard/touch, data persists, print includes intended collapsed content, each relevant checklist has its own printable scope.
- Form settings: all font sizes affect selectors and controls; computed input text remains at least 16px; date controls fit phone width; safe-area color/inset is consistent on every route; function and appearance settings are compact, correctly labeled, and persist without login.
- Theme matrix: light and dark modes across every primary route; selected/unselected/disabled/focus states; map legend/locate controls; floating back-to-top; danger/warning badges; inputs; bottom navigation; destination palettes. Text, icons and essential control boundaries meet the intended contrast targets.
- Maps/guides: filters derive from real records; city/date combination updates bounds and list; zero/one-point cases work; all navigation links respect selected provider and open the actual target where supported.
- Deep-guide order: earliest itinerary day first, explicit within-day sequence second; no guide disappears unless an actual filter excludes it.
- Accounts: guest, owner, unrelated ChatGPT user, member A and member B; server rejects cross-user reads/writes and role changes; same-name users do not share records.
- Repeat login, renewal, rotation, expired/revoked code, dismissible expiry reminder and login-return immediate profile update; private cache/attachments never cross sessions.
- Member edit conflict and sync failure; ticket/stay provenance accurately distinguishes available structured data from absent attachments.
- Verify public source/build/GitHub payload contains no private records, seed data, screenshots, codes or account/deployment credentials. See `privacy-and-publishing.md`.

## Evidence standard

A passing static build proves compilation only. Do not report browser, PWA, offline, or deployment behavior as verified unless each was tested. State untested areas plainly.
