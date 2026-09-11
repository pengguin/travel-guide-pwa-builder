# Changelog

All notable changes to this skill are documented here. This project uses semantic versioning. Version numbers describe the skill package, not a generated travel website.

## [2.5.1] - 2026-09-11

### Documentation

- Replaced five Chinese/English image pairs with detailed portrait-phone compositions and a ChatGPT-style fictional planning conversation.
- Added a sixth pair showing all six primary pages, between the home and map illustrations.
- Added editable shared artwork, complete Chinese text mapping, an isolated renderer and translation/layout checks. Navigation icons, ticket checkboxes and selected states now match across the bilingual set.
- Disclosed the generated fictional alpine photo, its prompt and the distinction between illustrative UI and runtime evidence.
- Updated both full READMEs and release/install links. Starter code, audit logic and production guide are unchanged.

### 中文摘要

更新六组中英图文：规划对话、随行首页、一级页面总览、互动地图、工具与票务、食宿安排。公开可重现的图源与来源说明；本版不修改起步项目功能或个人路书网站。

## [2.5.0] - 2026-09-10

### Added

- Offline identity decision table separating a server session, prior offline-read permission, cached records and connectivity; lifecycle and synthetic acceptance scenarios cover sign-out, expiry, revocation, account switching and late responses.
- Interaction architecture for Tools/My ownership, collection editors, public packing, shared spacing, sticky reading frames, safe areas and top-of-page overscroll regression checks.
- A paired Chinese/English synthetic illustration for the tools hub and personal offline reading; full language READMEs now preserve the same substantive sections.

### Changed

- Revalidation no longer universally gates previously authorized offline reading. Initial authentication and server API authorization remain mandatory.
- Independent utility modules may use subpages; accordions remain appropriate inside a task. Menu counts and visual frameworks are product choices.
- Release guidance distinguishes mock/browser/server/device evidence, requires complete asset readback where digests exist, and avoids unrelated lockfile-version edits.
- Regenerated the corrupted home documentation image from its existing neutral source; no private production screenshots were imported.

### Scope

This is a skill/reference/documentation update. Starter runtime, audit engine and server capabilities are unchanged. Guidance and illustrations are not proof of implemented member authentication or physical-device behavior. No reference Site is modified or republished.

### 中文摘要

补齐个人离线读取、工具与我的分工、就地编辑、安全区与下拉回弹验收约定；同步完整中英 README 和虚构图示。静态模板与审计引擎保持原有能力，不把开发指导写成已实现后端。

## [2.4.0] - 2026-09-08

### Added

- An itinerary-update workflow for immutable bookings, prioritized experiences, recovery days, meal routing, base hotels, cross-reservation storage and map fidelity.
- Sites/Vinext public-output detection, explicit source/public audit scopes, deployed icon checks and optional precache SHA-256 validation.
- Eight synthetic audit regressions and five service-worker failure/lifecycle regressions.
- Paired Chinese/English logistics documentation illustrations, screenshot provenance and a reproducible release workflow.

### Fixed

- The audit no longer expects a Sites/Vinext client entry at the Worker archive root or mistakes authorized server-only content for public client content by default.
- Missing deployed assets cannot pass merely because a source copy exists.
- The starter cleans incomplete installs, reads its own release cache, retains old caches while windows remain and rejects missing unversioned files instead of mixing releases.
- Documentation separates intended architecture from actual starter capabilities, and preserves the installed skill's narrow discovery description.

### Clarified

- Account/request-generation races, member-scoped local state and print blank-page checks.
- Documentation imagery is synthetic UI illustration, not proof of a working backend, real map or physical-device acceptance.
- Existing user publishing authority persists; updating a skill alone does not authorize changes to a referenced personal Site.

### 中文摘要

固定票务下进行行程级同步；新增按日食宿、恢复与跨订单寄存方法。审计兼容Sites/Vinext并区分公开输出与源码，检查图标及预缓存摘要。修正起步项目缓存混用/清理问题；同步中英文图文、验证边界与发布规范。

## [2.3.0] - 2026-09-06

Historical source release: field-execution and maintenance references, bilingual documentation and synthetic PNG illustrations. The existing repository commit and prior history are preserved; this entry does not assert that a GitHub Release asset was published at that time.
