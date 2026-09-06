# Travel Guide PWA Builder

This skill turns a one-line trip idea, a substantially fixed itinerary, or an existing guide into a field-ready, offline-capable, maintainable travel PWA. Current version: **2.3.0**.

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
