# Private records and optional members

Use only when requested. The portable static starter does not implement this backend. Build it through the supported Sites capability path, using current official auth and storage guidance.

## Data boundary and identity

- Public: generic itinerary, recommendations, publicly shareable overview and generic equipment categories.
- Private: actual ticket numbers/times/prices when designated private, booking screenshots, hotel confirmations, personal equipment models, individual notes and editable amounts.
- Store `tripId`, immutable `memberId`, role and record ownership server-side. Display names are labels, never lookup/authorization keys. A duplicate name must not inherit another person's records; offer disambiguation or explicitly selecting the existing member.
- ChatGPT sign-in identifies a user; it must not grant access to the owner's data by default. Use a configured server-side owner identity or explicit membership binding. Never make the first arbitrary public visitor the owner. Do not embed a real owner ID/email in this skill or public client assets.
- Derive current member identity from the trusted server session, not a client-supplied member ID. Check trip membership and authorization on every read/write/attachment endpoint. Test ID substitution and cross-trip access.

## Access codes and renewal

When requested and supported, distinguish one-use invitation redemption from reusable member login. If a code is intended for repeated login, test sign-out/sign-in and a second device; do not invalidate it on first claim. Show clear creation/claim/revocation states without creating extra invitation records as a side effect of login.

Use cryptographically random high-entropy codes; store a secure hash, not plaintext. Apply rate limits, expiry and revocation checks server-side, generic rejection messages, secure sessions, and CSRF/origin protections for writes. Do not put codes in URLs, analytics, public JS, screenshots or Git history. Prefer HttpOnly Secure session cookies where supported.

Keep code-redemption expiry, member access expiry and session expiry separate. Offer configurable duration choices (for example 7/30/60/180 days) rather than a fixed maximum. Extend the existing member's lease without changing identity or copying data. Specify whether extension starts from now or the later of now/current expiry. Rotation revokes the old code but retains the member's data.

When no different product rule is supplied, 30 days is a reasonable visible default for a newly created travel-access lease; it is not a security maximum. Put the create/invite action before historical management lists. On mobile, collapse current-member and credential-history sections by default when they would otherwise make the page excessively long. Do not duplicate profile editing or sync controls that already belong to the parent My page.

For requested expiry reminders, persist lease start/end and compute remaining fraction from that lease, not from an assumed duration. At the final 10%, show readable expiry text plus a restrained navigation badge. Dismissal must work without renewal and be scoped by member and lease version; renewal creates a new reminder period. Show expiry on both member cards and the signed-in profile. Expired access remains a server denial even if a warning was dismissed.

## Personal editing and immediately refreshed UI

- Roles should distinguish owner/admin, member-self editor and read-only viewer. Hiding UI is insufficient: whitelist editable personal fields on the server, reject role/owner/lease changes by members.
- Members may edit their own amounts, private transport additions/overrides, stays and notes when requested. Shared route changes require separate permission; do not silently edit other travelers or the public itinerary.
- Present saved tickets and stays as compact summaries with the same Details → inline edit → Save/Cancel pattern. New items scroll to a single draft editor and collapse after save. Keep checkbox selection hit areas independent from row-level editing actions.
- Resolve selected shared segment IDs plus member-specific segments into one chronological ticket list. Preserve a same-number flight with different boarding point as a distinct segment. Show admin preview of the selected member's resolved list, not just the owner's checkbox list.
- Keep one auth/profile state source. After login, await a fresh authorized profile, update shared state, invalidate ticket/stay/home selectors, and render immediately. Handle login-return/focus refresh, stale requests after logout and account switching; use cancellation or a session generation guard.
- Use explicit guest, loading, ready, empty and failed states. Distinguish 'structured ticket information available', 'original attachment not linked' and 'data fetch failed'; never say 'not provided' just because an upload has not been imported.
- Parent navigation should return editor → selected member/profile → My, not jump every screen to Tools. Preserve unsaved data deliberately and restore list context.

## Accommodation organization

Model a booked stay separately from a recommendation: member/trip IDs, property/local name, city, coordinates/address, check-in/out calendar dates, room/occupancy, currency/price basis, payment status, cancellation deadline with timezone, arrival instructions, contact and private attachment IDs. Unknown fields stay unconfirmed. Link the stay to each covered night and the day's arrival Transport Box. Distinguish shared booking from each member's cost share; avoid double counting. Request review of extracted screenshot data before overwriting confirmed fields.

## Local/offline and synchronization

Public reading and guest checklists may stay local. Private offline availability requires prior authorized download and explicit device storage choice; first login and first private fetch cannot work offline. Use separate namespaced stores keyed by site/trip/member, not one global profile cache. Do not runtime-cache private APIs in the shared service worker.

On logout/account switch/revocation detected online, clear private UI, records and attachments for that session as specified; do not erase unrelated members' server data. Local expiry is a usability/privacy control, not a guarantee of remote revocation while disconnected. Explain that downloaded data can persist and browser storage is not protection against an unlocked shared device; stronger offline secrecy requires encryption and an unlock design, not just a hidden tab.

Sync only the current member's records. Track revision/updatedAt and explicit pending writes; resolve conflicts rather than overwriting a newer server profile with an old offline copy. Provide a manual sync control when automatic sync is unreliable, with actual success/error/pending status. Do not report success merely because the device is online.

Acceptance: guest cannot read private endpoints/assets; unrelated signed-in user cannot read owner data; each member sees/edits only their own records; reusable code works twice; same-name user is isolated; extension preserves data; login updates every dependent screen without repeated taps; logout/account switch cannot flash or restore the prior user's data; expiry reminder can be dismissed; concurrent/offline edits do not silently overwrite one another.
