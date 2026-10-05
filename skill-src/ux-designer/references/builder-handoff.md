# Builder handoff

Use this reference when the requested output is an implementation prompt, including a Herdr builder prompt. The handoff itself does not authorize sending it to an agent, creating panes, publishing, or installing dependencies.

## Resolve before handing off

Confirm consequential workflow and style choices. Inspect discoverable implementation facts instead of asking the user to identify files. If a decision remains unresolved, continue the design discussion rather than writing a falsely complete implementation brief.

Keep the prompt self-contained and proportionate. Include actual project identifiers only when verified and needed in the private handoff; never bake a user's machine paths into this reusable skill.

## Prompt structure

Write direct instructions to the builder covering the following, merging sections when the task is small:

- **Goal and scope:** audience, target task, success criteria, approved depth of changes, and exclusions that prevent plausible scope mistakes.
- **Repository grounding:** actual checkout/entrypoint if verified, read local instructions, inspect current state, preserve unrelated edits, and avoid editing hidden legacy screens instead of the active view.
- **Layout and hierarchy:** regions, primary actions, progressive disclosure, key dimensions/breakpoints, scrolling, and reachability. Include a wireframe only when useful.
- **Behavior:** meaningful defaults, selection versus mutation, keyboard/button alternatives, loading/failure recovery, undo/save/output identity, and compatibility. Avoid inventing irrelevant edge cases.
- **Visual system:** approved style tokens and state variants, data-color exceptions, typography fallbacks, accessibility, reduced motion, and theme refresh behavior. Name approved approximations and unresolved limitations honestly.
- **Implementation constraints:** reuse current components and APIs; state necessary interface changes, or explicitly retain existing contracts when this guards against a likely regression. Do not turn a visual task into an unsolicited framework migration.
- **Validation and delivery:** repository-required checks, behavior-level acceptance scenarios, relevant window/platform matrix, visual evidence, and clear unverified items. Require real output only when the workflow actually needs it and the environment supports it.

Include reasons for non-obvious decisions, but omit conversational history and abandoned proposals. When revising the handoff, issue a coherent replacement rather than a chain of conflicting addenda.

## Review examples

- If the user wants only an audit, deliver findings and evidence; do not instruct a builder to mutate files without an implementation request.
- If a theme has no native blur support, require an explicit fallback decision; do not promise true vibrancy using whole-window opacity.
- If a workflow distinguishes current edits from generated versions, require playback/export to identify their actual source, and preserve snapshot identity during asynchronous work.
- If the user will paste the prompt into Herdr, provide the prompt. Live Herdr control is a separate request and must use the available Herdr workflow and current CLI rather than guessed commands.
