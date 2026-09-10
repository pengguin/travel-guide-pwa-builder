# Offline identity and personal reading

Use for a server-backed guide with optional personal offline data. This is an architecture and acceptance contract, **not an authentication implementation in the static starter**. Follow the host's current authentication/storage guidance and the product's explicit offline-access policy.

## Separate four concerns

Model online identity/session, prior offline-read authorization, cached member records, and connectivity independently. A failed request says something about connectivity or the server session; it does not by itself determine whether a previously downloaded, still-authorized record may be read locally.

An offline grant must originate from a successful authorized server response and the user's device-storage choice. Bind it to the site/trip/member, schema version and permitted expiry. Validate all fields before hydrating the UI; no grant, invalid schema or ambiguous ownership means no private read. Do not manufacture a grant from a display name, a role label or a saved arbitrary JSON profile. First login, account creation and first private download require a working server.

The local grant is a device convenience under the product policy, not proof for server APIs or protection from a hostile user modifying their own browser storage. Stronger secrecy needs an explicit encryption/unlock design. A disconnected device cannot learn about a newly revoked server membership until reconnecting or reaching local expiry.

## State decisions

| Event | Personal local reading | Network operations |
| --- | --- | --- |
| New visitor, no valid prior grant | Public guide only | Authenticate before private fetch |
| Valid prior grant and matching cached records | Render immediately, including offline cold start | Background refresh when possible |
| Timeout, offline, 5xx or malformed response | Retain valid local reading; show truthful connection/sync state | No successful-sync claim; retry with bounds |
| Online session expired or anonymous response | Follow the explicit API/grant policy; do not silently treat transport failure or session expiry as membership revocation | Private API calls remain denied until reauthentication |
| Confirmed membership revocation for this identity, or local grant expiry | Invalidate access and clear affected private presentation/storage under policy | Respect server denial |
| Explicit sign-out | Invalidate grant; prevent resurrection on reload | Cancel outstanding requests |
| Verified switch to another identity | Clear previous identity from view before the new fetch can fail | Fetch only the new identity's authorized records |

Define which response proves revocation. Status 401/403 alone may mean session expiry, a wrong endpoint or insufficient action permission. Do not ignore authorization errors, retry indefinitely, or keep server writes available using a local role. Conversely, do not erase a valid offline grant on every unsuccessful session check. If the API cannot distinguish these states, fix its contract before claiming reliable personal offline access.

## Lifecycle and data ownership

- Use one state owner with explicit transitions. Persist an explicit sign-out marker where needed; generation guards must reject responses from a previous identity even after reconnect, focus refresh or another tab's login.
- Validate grant expiry on startup, resume and during a long open session. Account-switch and sign-out events must also update other open tabs. Hydrating a storage event must not create a new verification loop.
- Scope checklist progress, ticket overrides, stays and attachments to immutable member/trip IDs. Public and guest stores contain only generic data. Never use one member's sample equipment as the guest fallback.
- Keep app-cache readiness, personal-download readiness and sync status separate. Device online status does not prove the API is reachable or that data was saved remotely.
- Merge the latest permitted fields before saving one collection so changing a stay cannot erase ticket edits or unrelated notes. Track revisions/pending writes and handle conflicts explicitly.

## Acceptance scenarios

1. With no prior grant, start offline: public pages work and every route, search result and export stays free of personal records.
2. With authorized synthetic data stored, restart offline and open previously unvisited personal routes: no online check blocks valid reading.
3. Repeat with timeout, 5xx, malformed response and documented session expiry. Confirm the intended local-read policy and denied server writes independently.
4. Expire the local grant; separately return a confirmed revocation. Private data must no longer appear, including stale tabs and exported views.
5. Sign out while a delayed successful fetch is pending; then reload offline. The old profile cannot return.
6. Switch from member A to B, fail B's fetch and return A's late response. Never display A's records to B. Repeat with equal display names.
7. Confirm guest/member checklist isolation, manual sync conflict handling and attachment cleanup separately from public service-worker caching.

Record which checks use pure state tests, mock API browser tests, real server authorization tests and physical-device storage tests. These are different evidence levels.
