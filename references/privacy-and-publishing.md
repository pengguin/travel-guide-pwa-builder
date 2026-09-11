# Privacy and publishing

Use this reference before turning a completed guide into a reusable skill, template, public repository, or shared deployment.

## Remove or replace

- personal names, emails, phone numbers, account IDs, and GitHub usernames;
- booking references, ticket numbers, QR codes, passport data, loyalty numbers, and payment details;
- exact private budgets or notes when they reveal personal circumstances;
- screenshots of tickets, chats, maps with home locations, or private dashboards;
- absolute local paths, cloud-drive folder names, device names, private hostnames, and local IP addresses;
- API keys, cookies, `.env` files, deployment credentials, and service tokens;
- proprietary or unlicensed photos and copied site assets;
- private deployment URLs and analytics identifiers.

Use neutral placeholders such as `Example Trip`, `YYYY-MM-DD`, `/path/to/project`, `BOOKED_SEGMENT`, and `https://example.com`. Do not use a real person's data as sample content.

## Preserve safely

Preserve the reusable method: information architecture, data contracts, source hierarchy, uncertainty labels, budget formulas, QA checks, and packaging steps. Abstract the itinerary and visual theme.

For a skill update, write neutral instructions and synthetic fixtures instead of copying the live app. Do not include `.openai/hosting.json`, production databases/seeds, `.dev.vars`, member exports, session stores, access-code digests, original screenshots, private attachment storage, analytics or account-specific allowlists. Remove real flight numbers, travel dates, paid prices and named personal equipment from examples. A blanked display name does not anonymize the rest of a booking.

Distinguish four destinations: public client bundle, private authorized server data, Sites source archive, and public skill GitHub repository. A private API is not protection if the same records are shipped in the client bundle or committed to a public source repository. Tests must use fabricated records. Review filenames, binary metadata, staged contents and any history introduced by the push, not only the final web page.

## Pre-push review

1. Inspect `git status` and the complete staged diff.
2. Confirm `.gitignore` excludes dependencies, build caches, environment files, logs, local archives, and editor state.
3. Run the included audit script against generated public projects. For the skill repository, also inspect every tracked file including `assets/starter`, which that script intentionally skips. The audit is a heuristic, not proof of anonymization; inspect warnings and sensitive binary content separately.
4. Search for home-directory paths, email addresses, private URLs, ticket identifiers, tokens, and route-specific leftovers.
5. Inspect binary files manually; text search cannot detect sensitive pixels or embedded metadata.
6. Confirm repository visibility and destination with the user when not already specified.
7. Push only after the local commit is validated.

## Publication boundary

Building, previewing, or creating a ZIP does not authorize publishing. An explicit request to push or deploy authorizes that named destination, not unrelated services. Report visibility, remote URL, and commit after publication.

For website work the official Sites skill controls publication/access approval. Updating and pushing this reusable skill does not authorize publishing or changing the reference travel Site. Preserve the named GitHub repository and its existing visibility; never copy its owner name into generated project defaults.

Repository documentation may identify its own public publisher and license, but demo fixtures and screenshots must remain synthetic or independently anonymized. A public itinerary is not automatically a safe reusable example if its dates, bookings, members, equipment or private workflow can identify a traveler.

For bilingual documentation, keep each language structurally complete rather than alternating sentence by sentence. In a combined README, place the full primary-language document first and the full secondary-language document afterward. Provide language-specific disclaimer pages and, when useful, an explanatory translation of the license while retaining the canonical license text.

Documentation screenshots must be raster captures of a browser-rendered neutral demo, not low-detail vector posters. Chinese and English screenshots must use the same viewport, layout, fictional itinerary and interaction state. Show planning as a conversation before the PWA exists. A requested ChatGPT-style illustration must identify the transcript as fictional and clarify that this local skill is invoked in Codex; do not imply that ordinary ChatGPT has executed the skill.

When documentation uses a browser-rendered illustration of the intended UI, mark it as a synthetic design demonstration rather than a screenshot of the working starter or the current Codex app. A fictional map must be labeled schematic/non-navigational. Document screenshot provenance, viewport, renderer and reproduction command; remove metadata that identifies a real traveler.
