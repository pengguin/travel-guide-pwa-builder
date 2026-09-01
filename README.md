# Travel Guide PWA Builder

A reusable Codex skill for building mobile-first, offline-capable travel guide PWAs from itinerary information alone or from an existing guide codebase.

## What it provides

- structured itinerary, transport, stay, budget, packing, and risk models;
- destination-aware visual themes with accessible semantic color tokens;
- a dependency-free static PWA starter;
- App Shell, service-worker, offline fallback, and iOS standalone guidance;
- privacy, content, asset, and release audits;
- production-oriented browser and offline QA gates.

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
python3 scripts/audit_travel_guide.py /path/to/guide --release
```

The repository contains no real itinerary, ticket, account, traveler, credential, or private deployment data.
