# PWA cold-start and offline implementation

Read this reference for white startup screens, iPhone standalone mode, offline requirements, service-worker changes, or release QA.

## Diagnose before decorating

Do not add a spinner before identifying the blank-screen dependency chain. Inspect:

- whether the entry HTML contains visible local markup before JavaScript runs;
- whether initial render awaits an API, remote font, map library, or large image;
- initial JavaScript and CSS size, eager imports, and route chunking;
- service-worker install/activate timing and whether registration blocks render;
- manifest `start_url`, `scope`, bundler `base`, router mode, and deployment subpath;
- console errors, failed chunks, stale cached entry HTML, and mismatched hashed assets.

The preferred result is: local launch shell immediately, home data from the bundle, then non-critical enhancement.

## Core offline boundary

Precache everything needed to read the guide:

- entry HTML and offline fallback;
- shared CSS/JS plus every lazy route chunk and extracted route CSS;
- manifest, icons, touch icon, and local core images;
- itinerary, booked tickets, hotels, transfers, packing, emergency information, and source notes.

Runtime-cache optional same-origin content and bounded map tiles where appropriate. Do not make remote tiles, real-time weather, external navigation, or live prices part of the core startup contract. Show an explicit offline state inside those modules.

## Bundled-app pattern

For Vite, Rollup, or another hashed build, generate the service-worker precache list from the completed deploy directory. A hand-maintained list will eventually omit lazy JavaScript or extracted CSS.

Use cache keys owned by the guide, for example `<guide>-<release>-precache` and `<guide>-<release>-runtime`. During activation, delete only older caches with the same guide prefix.

Cache matching must account for preview/CDN response variation. When using the Cache API directly, `caches.match(request, { ignoreVary: true })` is often necessary for static CSS/JS whose response includes `Vary: Origin`. Workbox or another library is acceptable when its behavior is verified.

Navigation should return the cached App Shell immediately and refresh it in the background. Install must finish caching all core resources before `skipWaiting`; activation can claim clients only after the new core cache is complete.

## Dependency-free starter pattern

The bundled starter precaches all static files because it has no generated chunks. Keep the launch content in `index.html`, replace it synchronously from local `trip-data.js`, and register the worker after initial render during idle time.

If the starter gains code splitting or generated assets, replace the static list with a build-generated list before release.

## iOS standalone checks

Use relative and mutually consistent values for subpath deployment:

- bundler base such as `./`;
- manifest `start_url` such as `./#/` or the guide's actual hash route;
- manifest `scope: "./"`;
- hash routing unless the host has a verified SPA rewrite.

Include Apple mobile-web-app metadata, a PNG touch icon, `viewport-fit=cover`, safe-area padding, theme/background colors, and standalone-safe navigation. Test the deployed HTTPS URL on a physical iPhone because desktop responsive mode cannot prove Add to Home Screen, standalone launch, iOS cache persistence, or system flight-mode behavior.

## Offline acceptance test

1. Use a fresh local origin or clear only the test origin before starting.
2. Load the production home page once; do not visit the other routes.
3. Wait for service-worker readiness and a controlled reload.
4. Stop the local server or enable browser offline mode.
5. Cold-reload the app, then open itinerary, tickets, packing/tools, stay/food, emergency, and map fallback routes that were not visited online.
6. Inspect failed requests and console errors.
7. Restore the network/server and verify the current cache version activates without serving stale HTML or missing chunks.
8. Separately repeat on the deployed HTTPS domain and physical iPhone when the user requires genuine iOS acceptance.
