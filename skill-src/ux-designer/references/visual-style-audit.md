# Visual style audit: Soft UI and macOS Vibrancy

Read only for these requested styles or a related light/dark audit. This is a concise interpretation of style requirements, not a claim that every product should adopt them. Current user-supplied references take precedence. Do not load their web-specific class names into a native UI implementation unchanged.

## Audit method

1. Inspect supplied references and implementation for surfaces, typography, component geometry, shadows, state feedback, motion, and theme switching. Include popups, menus, canvas content, disabled controls, and focus.
2. Report each finding as conforming, partial, conflicting, or unverified, supported by code or rendered evidence. Source inspection establishes implementation choices; screenshots establish appearance; interaction and user testing establish behavior and usability.
3. Identify contradictory requirements before implementation: examples may contradict prohibition lists; dark gray-only rules may conflict with category colors; blur may be unsupported; pale body text may fail contrast. Follow the stated precedence and obtain a decision for material deviations.
4. Keep the existing product's information architecture unless a layout change serves the user task. A style reference's three-column page or large marketing section is not automatically a product requirement.

## Soft UI

- Use soft light backgrounds, white or lightly tinted surfaces, low-saturation accents, generous spacing, and rounded primary components. Typical starting radii: 24px panels and 16px controls; adapt to the actual platform and supplied reference.
- Use blurred, low-opacity, subtly tinted shadows rather than hard offset silhouettes or heavy outlines. Avoid pure-black decorative surfaces and saturated large fills.
- Keep readable text contrast despite the soft palette. Soft surfaces do not justify faint labels or controls whose affordances disappear.
- Where requested, use restrained hover lift and soft press feedback, around 200–300ms. Preserve layout and hit targets; suppress hover displacement during drag. Do not move entire work areas merely because a reference animates cards.
- Provide visible focus and disabled states. Offer reduced-motion behavior appropriate to the platform, not a nonexistent CSS preference in a native application.
- Start major touch targets at 44 logical pixels when appropriate; handle density through grouping, disclosure, and scrolling rather than making essential targets inaccessible.

## macOS Vibrancy style

- Use three principal gray depths: #1c1c1e, #2c2c2e, #3a3a3c. Distinguish base surfaces from approved hover/focus overlays, which may require precomposed colors on native widgets.
- Use restrained 1px separators, typically white at 8–12% opacity over the actual surface; moderate radii, typically 8px controls and at most 12px panels.
- Use gray buttons with light text. #0a84ff is the reference interaction accent, not a license for bright filled backgrounds. Measure contrast before using it for small text; adjust text tokens when needed.
- The supplied style convention uses serif headings (Georgia plus available CJK serif fallback), system sans-serif body, and monospace technical text. Treat this as that reference's choice, not a universal rule of native macOS design.
- Avoid gradients, glow, thick borders, large shadows, hover lift, scale changes, and decorative motion. If transitions are requested, keep them to approximately 200ms color changes. Direct manipulation and genuine progress feedback remain functional behavior.
- Distinguish genuine background blur from opaque depth styling. Determine framework support before promising blur. Discuss a native adapter and cross-platform fallback versus a lower-cost opaque approximation. Whole-window opacity and desktop screenshots are not substitutes for background blur.
- Category/emotion fills may be retained as an explicit data-visualization exception if approved. Keep text labels and selection cues; do not extend that exception to all UI backgrounds.

## Theme acceptance

Both themes should preserve the same task flow, information hierarchy, data, focus, selection, scroll, and playback where applicable. Refresh typography, image assets, canvas surfaces, radius, shadow, and animation policy as well as colors. Avoid color-value replacement that accidentally recolors data categories.

Measure actual foreground/background contrast; target at least 4.5:1 for normal body text. Check visible keyboard focus and redundant state cues. Test representative supported sizes and scaling, long labels, empty/loading/error states, expanded details, and repeated theme switches. Do not claim all-platform or accessibility compliance from a token table alone.

Deliver explicit exceptions and evidence gaps: for example, “opaque Vibrancy-inspired adaptation; native blur not implemented; category fills approved.”
