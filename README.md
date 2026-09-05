# Travel Guide PWA Builder

A reusable Codex skill for building mobile-first, offline-capable travel guide PWAs from itinerary information alone or from an existing guide codebase.

Version 2.1 uses **ChatGPT Sites as its only built-in publishing workflow**. It delegates platform setup, authentication integration, packaging and release to the current official Sites skills rather than freezing a provider SDK in this repository. Local-only generation still works without Sites, a reference sample, or a prewritten day-by-day itinerary.

## What it provides

- structured itinerary, transport, stay, budget, packing, and risk models;
- a planning mode that turns a one-sentence trip idea into an initial guide after no more than five compact decision stages;
- a bounded research pass focused on entry, season, fragile transport, realistic transfer time, and budget feasibility;
- destination-aware visual themes with accessible semantic color tokens;
- a dependency-free static PWA starter;
- App Shell, service-worker, offline fallback, and iOS standalone guidance;
- privacy, content, asset, and release audits;
- production-oriented browser and offline QA gates;
- destination palettes, light/dark contrast checks, and separate function/appearance settings;
- itinerary-ordered deep guides with list-position restoration and next-place navigation;
- current-day/countdown logic, mobile form and safe-area guidance, consistent navigation and collapsible tools;
- optional My/member workflows, editable private records, repeatable access-code/renewal contracts and isolated offline/sync design;
- privacy-aware Sites integration with explicit public/shared access approval.

## Capability boundaries

The bundled static starter runs locally and includes countdown, day overview, previous/next controls, collapsible tools, local checklist storage and offline public files. It intentionally has no login, private uploads or cloud synchronization. For hosted/member features, the agent uses the installed Sites plugin and implements the requested backend from the contracts in `references/`; no live user's application, accounts or database is bundled here. No alternative hosting-provider deployment scripts are included.

The skill has three operating modes:

- **Planning:** start from a rough idea; make a small number of branch decisions and produce a labeled draft route and guide.
- **Execution:** build from fixed dates, bookings, or a detailed itinerary.
- **Update:** apply requested changes to normalized data, then rebuild and verify the complete release.

## Install

Clone the repository into your Codex skills directory, or copy the repository folder there:

```bash
git clone https://github.com/<owner>/travel-guide-pwa-builder.git ~/.codex/skills/travel-guide-pwa-builder
```

Then invoke it as `$travel-guide-pwa-builder` or describe a request for a deployable travel-guide PWA.

## Create the standalone starter

```bash
python3 scripts/create_project.py \
  --output /path/to/new-guide \
  --title "Example Journey" \
  --short-title "Journey" \
  --start-date 2030-01-02 \
  --end-date 2030-01-08 \
  --origin "Origin City" \
  --destinations "Historic City" "Mountain Lake" \
  --theme auto
```

The generated scaffold is intentionally incomplete. Replace its example itinerary and remove the final-itinerary marker only after the content is real.

## Validate

```bash
python3 -m unittest discover -s tests -v
node --test tests/*.test.cjs
python3 scripts/audit_travel_guide.py /path/to/guide --release
```

The audit script checks static releases, not Sites Worker runtime/authorization. Device/browser and deployed-account checks must be reported separately. The repository contains no real itinerary, ticket, account, traveler, credential, or private deployment data.
