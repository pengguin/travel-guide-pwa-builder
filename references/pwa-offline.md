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
- public itinerary, generic transfers/stay/packing notes, emergency information and public sources.

Private booked tickets, hotel confirmations, attachments and personal equipment must not be in the public bundle, HTML, service-worker precache or shared runtime cache. Fetch them only after server authorization, optionally store them in a separate member-scoped offline store, and implement logout, expiry and account-switch handling as specified in `member-data.md`. First authentication/private download requires a network connection. Later offline reading with a valid prior grant must not wait for a network check; see [offline-identity.md](offline-identity.md). Do not claim instantaneous remote revocation of an already disconnected device.

Runtime-cache explicitly allowlisted public assets only. Same-origin does not mean public: never blanket-cache API, auth, member or attachment routes. Optional map tiles require provider permission and bounded storage. Remote tiles, weather, external navigation and live prices are not part of core startup; show an explicit offline state inside those modules.

## Bundled-app pattern

For Vite, Rollup, or another hashed build, generate the service-worker precache list from the completed deploy directory. A hand-maintained list will eventually omit lazy JavaScript or extracted CSS.

Use cache keys owned by the guide, for example `<guide>-<release>-precache` and `<guide>-<release>-runtime`. During activation, delete only older caches with the same guide prefix.

Cache matching must account for preview/CDN response variation. Restrict `ignoreVary: true` to verified public static resources (for example CSS varying only by Origin). Never ignore user/session variation on personal responses. Workbox or another library is acceptable when verified.

Public navigation should return a cached App Shell immediately. Update HTML and its referenced assets as one complete release; do not replace cached HTML alone while retaining incompatible JS/CSS. Keep old hashed assets while old clients need them, or prompt a controlled reload. Install must finish caching all core resources before activation. A real server/auth endpoint must not fall back to a successful HTML shell.

For a code-split app, do not automatically call `skipWaiting()` in the install handler. If a newly installed worker activates while an old page is open, activation cleanup can delete the old hashed CSS/JS and produce a transient route-load failure. Use this lifecycle instead:

1. fully cache the new release during install;
2. leave it waiting while old clients remain;
3. expose a **Check/update app version** action that detects a waiting worker and explicitly messages it to activate;
4. reload once after `controllerchange`;
5. keep old guide-owned caches while any old clients can request their assets; only clean them when no such clients remain;
6. otherwise allow normal activation after every old tab/client closes.

Keep **app version update** separate from **personal data sync**. The former installs a new code/content release and reloads the app; the latter uploads/downloads authorized member records. Label both status and last-check time clearly.

The settings UI should distinguish the stable display release from a unique internal build/release ID and a service-worker cache name. Every deployable asset set receives a new build ID even when a maintenance patch intentionally keeps the public version label. Never report an installed client as current merely because the visible label matches; compare a machine-readable release manifest and verify the complete public precache before reporting readiness.

For apps with a release manifest and verified repair implementation, treat offline verification as an active repair operation when online, not only a cache inventory. A user-triggered recheck should ask the controlling service worker to refetch the current precache through a `MessageChannel`, then verify every manifest entry inside the exact current-release static cache. Fetch the manifest with a cache-busting query that the service worker sends network-only. Update the visible verification time after every completed attempt, including incomplete results.

When the server release ID equals the client release ID, still run service-worker update/activation and precache repair. “No newer release” does not prove that the current cache is complete. If a waiting worker exists, activate it under the product's explicit update policy before messaging the new controller. Report missing counts and recovery instructions rather than a false ready state.

## Dependency-free starter pattern

The bundled starter precaches its explicit public file list, including `trip-state.js`, because it has no generated chunks. Keep launch content in `index.html`, replace it synchronously from local `trip-data.js`, and register the worker after initial render during idle time. Add every new core public image/file to that list and bump the worker release name. It deliberately does not intercept arbitrary same-origin URLs. Do not reuse this static worker unchanged for a server-backed Sites project.

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
3. Wait for service-worker readiness. If the app exposes an update action, test the waiting-worker prompt and exactly one controlled reload.
4. Stop the local server or enable browser offline mode.
5. Cold-reload the app, then open itinerary, tickets, packing/tools, stay/food, emergency, and map fallback routes that were not visited online.
6. Inspect failed requests and console errors.
7. Restore the network/server and verify the current cache version activates without serving stale HTML or missing chunks. Keep an old lazy route open during an update and prove it does not lose its old CSS/JS before the controlled activation.
8. Separately repeat on the deployed HTTPS domain and physical iPhone when the user requires genuine iOS acceptance.
9. For private mode, download authorized synthetic test data online, then verify offline reading and expiry behavior. Switch users/logout and prove private records cannot reappear through a shared cache or stale request. Never copy production records into test fixtures.

## Integrity and failure outcomes

For a manifest-driven app, record per-file SHA-256 digests, fetch into a staging cache, verify response status/bytes and commit readiness only after every core file is present. Missing chunks, changed HTML, stale manifests and network failures reject installation or repair; a version-label match is not success. A repair request should include the expected release, return a structured result and terminate on a bounded timeout. Preserve the previously complete cache on failure.

The neutral static starter uses an explicit `addAll` list. It deletes a failed install cache, reads assets only from its current release, retains older guide caches while windows exist, and returns 503 for a missing core asset rather than mixing in a new unversioned network file. It does **not** implement digest-based repair or an end-user update UI. Bump its cache name for every asset change and close old guide windows for natural activation, or implement and test an explicit update flow. Do not advertise the full architecture contract as a built-in starter feature.
