# Harness self-evolution image-generation prompt

Mode: built-in `imagegen`.

Reference image: `assets/self-evolution-loop-matplotlib.png`.

```text
Use case: infographic-diagram
Asset type: wide 16:9 architecture figure for a serious AI systems research article
Primary request: Redesign the reference image into a polished AI research-paper architecture diagram for the MatSpec harness self-evolution loop. Preserve the reference image's causal logic, but improve hierarchy, grouping, spacing, and visual clarity.
Style/medium: clean flat vector-like scientific figure rendered as a high-resolution raster; visual language of a top-tier NeurIPS/ICLR systems paper; off-white paper background; thin precise strokes; restrained muted blue, teal, amber, coral, and gray; subtle rounded rectangles; no decoration.
Composition/framing: landscape. A slim locked boundary band across the top. A five-module left-to-right pipeline in the center. External evaluation below the candidate harness. A green acceptance feedback arrow returns to the current harness. A red rejection arrow goes to a preserved-failure-evidence capsule. Clear generous whitespace.
Text (verbatim):
Title: "HARNESS SELF-EVOLUTION"
Top band title: "FIXED OUTER BOUNDARY — NOT EDITABLE"
Top band chips: "Frozen Tasks" · "Code Baseline" · "Model + Reasoning" · "Ground Truth" · "Evaluators" · "Permissions"
Core modules:
"Current Harness Hₜ"
"workflow · commands · context"
"Candidate Agent"
"run real task"
"Frozen Trajectory Tₜ"
"diff · tests · usage"
"Evolver Agent"
"diagnose · propose ΔHₜ"
"Candidate Harness"
"Hₜ + ΔHₜ"
Evaluation module:
"External Evaluation E"
"blind review · focused tests · completion · time · tokens · tool calls"
Green feedback label: "ACCEPT → Hₜ₊₁"
Red branch label: "REJECT → preserve failure evidence"
Footer note: "Operator · Candidate · Evolver · Judges are independent agents"
Constraints: Every module and arrow must have an unambiguous direction. External evaluation and the top fixed boundary must be visually outside the evolvable harness. Preserve exactly one accept loop and one reject branch. All text must be legible and spelled exactly as supplied. Use mathematical subscripts where shown.
Avoid: glossy 3D, gradients, shadows, people, robots, circuit-board imagery, decorative icons, fake logos, watermark, tiny unreadable labels, duplicated modules, extra arrows, garbled text.
```
