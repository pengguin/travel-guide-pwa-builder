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
- If the project uses lazy CSS/JS chunks, verify offline requests hit precache even when responses carry `Vary: Origin`; test the actual preview server rather than assuming URL equality is sufficient.
- Confirm page title, manifest name, theme color, icons, and service-worker cache version match the current guide.
- For iOS/Add to Home Screen, check `apple-mobile-web-app-capable`, status-bar style, touch icon, safe-area viewport, `display: standalone`, `start_url`, `scope`, and standalone navigation behavior.

## Cold-start evidence

- Inspect the raw entry HTML: it must contain a meaningful local launch/App Shell, not only an empty framework root.
- Confirm core rendering does not await remote fonts, map tiles, weather, or API data.
- Record whether the test was a desktop/browser simulation, a deployed-domain test, or a physical iPhone test. Never describe a local preview or stopped-server test as a physical Add-to-Home-Screen result.
- A short local launch shell is acceptable; a long blank screen followed by content is not.

## Release archive

- Build output should contain the entry HTML, manifest, icons, service worker, and versioned assets.
- ZIP the contents of the deploy directory at archive root; do not wrap them in an extra project folder unless the host explicitly requires it.
- List the archive and perform an integrity test.
- Record the archive path, size, checksum, build command, and preview command.

## Evidence standard

A passing static build proves compilation only. Do not report browser, PWA, offline, or deployment behavior as verified unless each was tested. State untested areas plainly.
