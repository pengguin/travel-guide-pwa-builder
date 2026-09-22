# Day navigation, appearance and foreground recovery

Use this for repeated mobile scroll jumps, interrupted day animations, manual theme changes, or installed-PWA resume defects. Adapt it to the existing shell; it is not a replacement shell implementation.

## Reading position and transitions

Give each navigation intent one scroll owner: primary-page navigation, sibling day selection, detail return, and explicit back-to-top. Date buttons, previous/next buttons and swipes must use the same day-switch contract. Do not combine router restoration, scrollIntoView, browser anchoring and component scroll resets for one transition.

If user preferences are requested, keep page-to-page restoration separate from per-day restoration. Remember stable content IDs, expansion state and an offset relative to the reading frame; pixel offsets alone fail when weather, images or collapsed content change height. Include short-to-long and long-to-short panels, both directions, first/last day and already-pinned/unpinned date bars. Wait for committed day content as well as the new URL in browser tests.

When a device still jumps, a requested return-to-day-top default is a valid fallback. Label remembered position experimental if it remains unreliable. Any preference migration must preserve unrelated choices and allow a subsequent deliberate opt-in; do not reset it on every launch. Do not promise preservation regardless of content or viewport changes.

Swipe thresholds, velocity and vertical drift belong to a documented gesture contract, not universal constants. Exclude buttons, links, form controls, maps, horizontal scrollers, text selection and system edge gestures. A cancelled/vertical/multitouch gesture must not navigate or activate a summary. Respect the product's motion preference and reduced-motion policy.

Cancel pending incoming/outgoing animations and drag transforms on suspension or a superseding navigation. Avoid starting rebound animations in the background. A cancelled outgoing animation must not complete navigation later. Test interruption during drag, outgoing and incoming animation, plus normal tapping and scrolling.

## Distinguish document appearance from system chrome

First record the actual context: browser tab or installed app, OS/browser version, light/dark/system setting, palette, and machine release ID. Separate the webpage's pseudo-elements/gradients/backdrop blur from native statusbar tint and the OS app-switch snapshot. Matching release IDs do not establish what the compositor painted; local viewport emulation does not reproduce system chrome.

Exercise real appearance controls before diagnosing a stale storage value. Read the selected control, resolved theme, root/body/page/scroll computed backgrounds, color-scheme and theme-color metadata across frames. Compare manual changes with background/resume. Only attribute the symptom to a stale value if observed.

Prefer one CSS owner for viewport background and color-scheme, available before hydration. Keep viewport surfaces consistent with all offered palettes. Copying a computed page background into root/body inline styles creates a second update path; use it only for a demonstrated need. If the existing full-screen scroll surface needs an explicit opaque background, use the same semantic token; do not add a safe-area overlay or change its height as an incidental tint workaround.

On hidden documents, preserve the last painted theme where appropriate. If observed system-theme events are transient during resume, coalesce them with a bounded settling policy. Real stable system changes must still apply and intentional in-app choices should remain immediate. A delay is a mitigation, not proof of a platform fix; do not prescribe one magic duration for all browsers.

Preserve existing safe-area ownership. Switching statusbar metadata or viewport-fit can change installed-app content bounds and bottom spacing; a metadata change is not a universal cure for tint. Do not solve a top effect with an unmeasured bottom spacer, repeated reloads, element-remount loops, fake lifecycle events or unconditional paint writes. Clearing storage/reinstalling can discard user state and should not be a routine workaround.

## Evidence and stopping condition

Verify unchanged resumes do not rewrite appearance, recreate content or shift scroll unnecessarily; stable theme changes do update. Background checks must preserve authentication expiry/revocation enforcement. Test map geometry separately from visual viewport transients and keyboard/orientation behavior.

Keep three results distinct: a confirmed application defect, a bounded application mitigation, and an unverified platform hypothesis. Record failed attempts and regressions. A passing mocked focus/visibility test does not close an owner's physical-device report. After an ineffective mitigation, collect the distinguishing device evidence instead of claiming successive speculative releases have solved it. If a custom shade is optional and the user accepts removing it, remove its actual component/styles; do not claim that removes OS-owned effects.
