# Travel Guide PWA Builder

This skill turns a one-line trip idea, a substantially fixed itinerary, or an existing guide into a field-ready, offline-capable, maintainable travel PWA. Current version: **2.4.0**.

The images below are synthetic UI illustrations rendered from self-contained HTML, not screenshots of Codex or a deployed guide. See [image provenance](docs/SCREENSHOTS.md).

![Invoke the skill in Codex and complete the minimal planning intake](docs/images/chat-en.png)

## Use cases

- Planning mode: resolve route-changing decisions in no more than five stages, then build a structured route and first guide.
- Execution mode: lock confirmed dates, tickets, and stays, then add timelines, deadlines, transfers, and fallback branches.
- Update mode: change normalized data, remove retired facts, and rebuild the complete PWA release.

## Main deliverables

A dynamic field home, day execution pages, interactive map, sight/transport/stay-and-food guides, offline core pages, checklists and clean print output, explicit whole-app updates, and optional public/private data separation.

![The field home leads with the next action, hard deadline, and fallback branch](docs/images/home-en.png)

![The landscape map, place list, and aligned controls form one operational workspace](docs/images/map-en.png)

## Environment boundary

Local utilities require Python 3.10 or newer and a modern browser; repository workflows require Git. Network access is required for source checks, dependency installation, online maps/live data, Sites publishing, and first private-data synchronization. Without ChatGPT Sites, the skill can still create a local public static PWA, but it does not implement or recommend a specific multi-user hosting substitute.

See the bilingual [README.md](README.md) for the complete method, installation commands, validation gates, usage guidance, and privacy boundaries.

- Disclaimer: [DISCLAIMER.en.md](DISCLAIMER.en.md)
- License: [LICENSE](LICENSE)
- Unofficial Chinese license explanation: [LICENSE.zh-CN.md](LICENSE.zh-CN.md)


## 2.4.0: itinerary changes with clear capability boundaries

- Keep booked flights/trains immutable. Fit meals, base hotels, luggage and sleep around prioritized operator products and personal themes.
- Prefer one primary and one backup for each daily lunch/dinner. State late arrival, early checkout, breakfast and cross-reservation storage conditions; a candidate is not a booking.
- Synchronize the home, days, maps, guide dates, reminders, calendar, budget and complete offline release.
- Detect static and Sites/Vinext public output, check icons and optional SHA-256 manifests; choose a source scan explicitly.

![Synthetic daily meal, hotel and prior-evening preparation illustration](docs/images/logistics-en.png)

| Capability | Included in this package | Still requires implementation/verification |
| --- | --- | --- |
| Portable static starter | Local data, date state, checklists, calendar, print entry and basic offline cache | Final itinerary, real images and actual map integration |
| Itinerary updates | Fixed-ticket, food/stay, recovery/storage and derived-view workflow | Applying the delta to the existing project |
| Release audit | Public directory, assets, icons, optional SHA-256 and heuristic leakage checks | API permissions, browser behavior and every possible private datum |
| Whole-app updates | Starter cache isolation/failure behavior and full-app architecture guidance | No starter digest repair, member backend or end-user update button |
| Documentation images | Browser-rendered bilingual fictional UI illustrations | Not current Codex screenshots, real travel maps or device acceptance evidence |

Audit examples:

```sh
python3 scripts/audit_travel_guide.py /path/to/guide --release
python3 scripts/audit_travel_guide.py /path/to/guide --release --public-dir custom/output
python3 scripts/audit_travel_guide.py /path/to/guide --release --source
python3 scripts/check_docs.py
```

`--release` scans deployed public files by default. `--source` adds a source-tree review, which may include legitimate authorized server records. Neither replaces manual privacy review or browser/device acceptance.

See the [changelog](CHANGELOG.md), [verification and packaging](docs/releases/2.4.0.md), [image provenance](docs/SCREENSHOTS.md), [contributing](CONTRIBUTING.md) and [GitHub Release](https://github.com/pengguin/travel-guide-pwa-builder/releases/tag/v2.4.0). Verify the ZIP with its SHA-256 file; the extracted skill folder is `travel-guide-pwa-builder`.
