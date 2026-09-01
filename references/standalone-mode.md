# Standalone generation mode

Read this reference when the user provides no existing guide, design sample, or codebase.

## Initialize

Run the bundled initializer from the skill directory:

```bash
python3 scripts/create_project.py \
  --output /path/to/new-guide \
  --title "Trip title" \
  --short-title "Short title" \
  --start-date YYYY-MM-DD \
  --end-date YYYY-MM-DD \
  --origin "Origin" \
  --destinations "Stop A" "Stop B" "Stop C" \
  --theme auto
```

The output is a dependency-free static PWA with five hash-routed views: overview, itinerary, route map, practical guides, and tools. It includes a visible local launch shell, offline app shell, install manifest, schematic route visualization, expandable daily cards, phase filtering, budget totals, a device-local checklist, print styles, and calendar export. `--theme auto` uses conservative destination-name hints; choose `heritage`, `desert`, `mountain`, `coast`, `forest`, `tropical`, `polar`, or `urban` explicitly when research or representative imagery indicates a better fit. Read [destination-theming.md](destination-theming.md) before making that choice final.

## Complete the content

Edit `data/trip-data.js` using the final user brief and current research. Remove the final-itinerary scaffold marker only after all scaffold content has been replaced.

Complete these fields:

- trip title, subtitle, dates, party size, route text, summary, and verification date;
- phases, rhythm labels, core highlights, and 3–5 critical risks;
- ordered route points with verified coordinates;
- every travel day, including schedule, transport, intensity, hotel change, stay, food, notes, and recheck state;
- practical guides appropriate to the destination;
- budget items with scope and evidence basis;
- final checklist of no more than eight decisive actions;
- sources supporting dynamic or high-risk claims.

Replace the neutral SVG app icon and theme colors when destination-specific branding materially helps. The starter contains no external photos; add only relevant, locally packaged, credited images if the content benefits from them.

Before a production iPhone release, replace the neutral SVG-only install icon with local PNG `apple-touch-icon`, 192px, 512px, and maskable variants. Keep the SVG only as an optional browser favicon. Read [pwa-offline.md](pwa-offline.md) for the cold-start and offline acceptance test.

## Preview and package

The generated source is already the deployable directory. Preview it with a local static server, test it according to `qa-and-release.md`, then ZIP its contents at archive root. If a hosting provider needs a build directory, copy the verified files into `dist/` before using the release audit.

## Completion condition

The standalone guide is not complete while the scaffold marker remains, any placeholder budget is presented as final, route coordinates are generic, sources are missing for dynamic claims, or browser/PWA checks have not been performed.
