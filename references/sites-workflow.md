# Sites integration

Sites is the only supported publishing path in this skill. Keep local-only generation available; do not carry provider-specific deployment scripts from a previous guide into new projects.

## Authoritative dependency

Before creating, editing or publishing a Site, read the currently installed official `sites-building` and `sites-hosting` SKILL.md files and their required environment references. Those skills own initialization, runtime capabilities, preview, source credentials, packaging, access approval and deployment. Do not embed an obsolete CLI version, tool schema, plugin installation path or copy of their scaffold here.

If unavailable, explain that hosted functionality needs the Sites plugin. Discover available tools before requesting installation. Continue explicitly local-only work when useful; do not simulate a deployment, substitute another provider or claim authentication exists.

## Choose the project shape

- Existing `.openai/hosting.json`: preserve project identity, architecture, package manager and lockfile. Do not create another Site or initialize over it.
- New hosted travel guide: use the current official scaffold and capability path; multi-route travel guides rarely qualify for a one-shot static landing-page flow.
- Public reading only: a static build may be sufficient. Declare `static.directory` only for a supported, public output directory according to the current hosting contract.
- Accounts, persistent personal records or uploads: use the server-backed path and read the official authentication, persistence and SQLite references as applicable. Configure only requested logical capabilities. Never place runtime values or real resource IDs in a reusable template.
- Portable starter: no design sample required; complete its neutral data from the brief. It is an alternative for local static delivery, not a backend/auth scaffold.

## Public guide and optional private area

Keep public guide routes independent of sign-in. An owner-only platform access policy blocks anonymous readers before application code runs; it is not equivalent to a public site with a private My area. Check the actual platform policy and obtain the required approval before changing it.

For ChatGPT authentication, use current dispatch-owned helpers and top-level sign-in navigation, not fetch/preloaded client links to auth endpoints. ChatGPT identity is not authorization: enforce explicit server-side ownership/membership. Read `member-data.md` before implementing member access codes. Confirm current platform support before adding app-owned external sign-in; do not promise an unsupported auth stack.

## Release sequence

1. Separate public output from private records, attachments, local test databases and secrets before building. Inspect both public assets and source to be uploaded; a private server bundle is still source disclosure when pushed to a public GitHub repository.
2. Complete content reconciliation and relevant tests. For server output, verify the Worker-compatible ESM entry with a callable default `fetch`; include inspected migrations when required. For static output, verify public entry HTML and offline assets.
3. Follow the official source/version/archive sequence with current native tools. Keep credentials ephemeral, out of Git URLs/config, archives and logs. Use the official packaging helper rather than a generic ZIP command for a server-backed Site.
4. Inspect existing Site access before deployment. Follow the official public/shared approval gate. A skill GitHub push is not a Site publication request.
5. Wait for a successful deployment status, then hand off the exact returned URL. Do not invent project identifiers, versions, domains, or successful deployments.

Browser preview/testing and image-generation behavior follow the official Sites skill. A skill-only maintenance task requires neither a new Site nor publishing a reference Site.
