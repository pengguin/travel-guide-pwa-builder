# QA and release gate

Use this checklist for every deployable handoff.

## Content reconciliation

- Compare the rendered day count, dates, route order, hotel nights, and fixed tickets with the final user brief.
- Search the complete source tree for retired dates, destinations, flight numbers, budgets, names, and headings.
- Confirm optional items, assumptions, and dynamic facts carry the correct labels.
- Confirm sources directly support the claims attached to them.

## Asset checks

- Resolve every local image, icon, manifest icon, and social preview asset.
- Hash raster assets and inspect duplicates. Repetition is acceptable only for intentional brand assets.
- Check image subject, crop, alt text, dimensions, compression, and credit record.
- Test maskable icons at square, circular, and rounded-square crops.

## Build and browser checks

- Run the production build with a clean exit.
- Serve the production output locally.
- Test at least one narrow phone viewport and one desktop viewport.
- Open every primary route and representative detail page.
- Reload nested routes; verify routing survives static hosting.
- Exercise expandable cards, filters, map layers, navigation, calculators, and calendar export.
- Inspect console errors, failed requests, broken images, and horizontal overflow.
- Test a production reload after service-worker registration and check the offline fallback where supported.
- Confirm page title, manifest name, theme color, icons, and service-worker cache version match the current guide.

## Release archive

- Build output should contain the entry HTML, manifest, icons, service worker, and versioned assets.
- ZIP the contents of the deploy directory at archive root; do not wrap them in an extra project folder unless the host explicitly requires it.
- List the archive and perform an integrity test.
- Record the archive path, size, checksum, build command, and preview command.

## Evidence standard

A passing static build proves compilation only. Do not report browser, PWA, offline, or deployment behavior as verified unless each was tested. State untested areas plainly.
