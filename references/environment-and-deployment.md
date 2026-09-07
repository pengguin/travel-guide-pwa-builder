# Environment and deployment boundary

## Local development

The skill itself uses Python standard-library utilities and a dependency-free static starter. Use Python 3.10 or newer for the included initializer and audit scripts. A modern browser with Service Worker support is required for PWA preview and offline checks. Git is optional for local generation and required only for repository workflows.

A hosted Sites project must follow the runtime and package-manager versions declared by the current official Sites scaffold and its lockfile. Do not freeze a Node, vinext, Worker or Sites plugin version in this skill. Inspect the existing project's `package.json`, lockfile and `.openai/hosting.json`; use the currently installed official Sites skills to resolve supported dependencies.

## Network use

Local starter generation, editing and static tests can run without internet. Network access is needed for:

- current official-source verification and licensed media retrieval;
- map tiles, live weather, fares, schedules and external navigation;
- installing missing packages;
- ChatGPT Sites authentication, source push, saving and production deployment;
- first member login, private-data download/upload and cloud synchronization.

Core public reading should work offline after a successful online install. Do not claim that dynamic or private functions work offline unless that exact path was implemented and tested.

## ChatGPT Sites dependency

ChatGPT Sites is this skill's only implemented hosted publishing path. When Sites is unavailable, the skill can still produce the bundled local/portable public PWA. It does not currently provide an automated substitute for public hosting, authentication, multi-user data, uploads or synchronization.

A conceptual substitute would combine a static host, HTTPS, serverless or edge functions, an identity provider, durable database/object storage and a carefully scoped PWA cache. That architecture needs provider-specific security, privacy, migration and deployment work. This repository deliberately documents the idea but does not ship or endorse an alternative provider implementation.

## Responsibility and disclaimer

Generated routes, schedules, prices, border/visa notes, weather advice, health/safety notes and provider benefits can change. Mark dynamic facts for recheck and direct travelers to the responsible official authority/operator before acting. The guide is planning assistance, not a guarantee and not legal, immigration, medical, safety or financial advice. Users remain responsible for eligibility, bookings, insurance, documents, local rules and safe decisions.

## Public output audit

`audit_travel_guide.py PROJECT --release` selects `dist/client/` for Sites/Vinext, `dist/` for a flat build, or the root for a portable static project. Supported static hosting metadata can select a custom output; `--public-dir relative/output` makes that selection explicit. Worker presence is checked for detected Sites/Vinext packages. Pass `--source` separately when intending to review the source tree, which may legitimately contain authorized server-only records. Neither mode proves permissions, absence of every possible private datum or correct behavior on a physical device.

For server-rendered Sites/Vinext projects, pass the project or dist root. An existing Worker entry may generate HTML without a static index; the audit reports that as a live/offline verification reminder. Passing only client assets cannot prove the server entry.
