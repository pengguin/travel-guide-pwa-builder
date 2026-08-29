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

## Pre-push review

1. Inspect `git status` and the complete staged diff.
2. Confirm `.gitignore` excludes dependencies, build caches, environment files, logs, local archives, and editor state.
3. Run the included audit script against the repository.
4. Search for home-directory paths, email addresses, private URLs, ticket identifiers, tokens, and route-specific leftovers.
5. Inspect binary files manually; text search cannot detect sensitive pixels or embedded metadata.
6. Confirm repository visibility and destination with the user when not already specified.
7. Push only after the local commit is validated.

## Publication boundary

Building, previewing, or creating a ZIP does not authorize publishing. An explicit request to push or deploy authorizes that named destination, not unrelated services. Report visibility, remote URL, and commit after publication.
