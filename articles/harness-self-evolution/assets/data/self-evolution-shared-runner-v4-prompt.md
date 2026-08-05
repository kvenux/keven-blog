# MatSpec self-evolution with one shared runner — imagegen prompt

Use case: infographic-diagram

Asset type: article mechanism figure, 16:9.

Reference role: preserve the clean research-paper diagram style of `self-evolution-loop-imagegen-v3.png`: white background, thin black rounded rectangles, strong black arrows, dark navy numbered circles, restrained red/green selection accents, compact sans-serif typography. Redraw the information architecture completely.

## Main correction

The previous figure incorrectly showed `Run Real Tasks` and `Replay + Evaluate` as two different stages. They are one shared operator applied to two Harness states. The new figure must contain exactly ONE large box labeled `统一运行与外部评测器` / `RUN + EVALUATE`. Both `当前 Harness Hₜ` and `候选 Harness H′ₜ` must feed back into this same box. Never draw a second runner, replay box, or duplicate evaluation pipeline.

## Layout

Draw one clockwise loop centered around the single shared runner.

Top-left: navy-numbered state box `1 当前 Harness Hₜ`, with small line `workflow · instructions · context handoff · acceptance rules`.

Top-center: the largest box, navy-numbered `2 统一运行与外部评测器`, with code-style line `Run(H, D, E)`. Inside or directly underneath, four compact items: `真实任务`, `聚焦测试`, `双盲评审`, `时间 · Token · Tool calls`.

Top-right: navy-numbered evidence box `3 基线轨迹 Tₜ`, with `sessions · decisions · product outcomes · cost`.

Right-center: navy-numbered box `4 Evolver Agent`, with `归因失败 · 识别重复劳动 · 提出受限修改 ΔHₜ`.

Bottom-right: navy-numbered state box `5 候选 Harness H′ₜ`, visually identical in shape to `当前 Harness Hₜ`, with small line `同一种对象，不是新阶段`. From this candidate box, draw a thick blue return arrow labeled `同一执行器回放` back into the SINGLE shared `RUN + EVALUATE` box.

When the candidate passes through the same runner, show a small evidence card adjacent to the runner labeled `候选轨迹 T′ₜ`; this is not another stage box and must not have a separate runner.

Bottom-left: navy-numbered selection box `6 Compare + Select`. It receives both `Tₜ` and `T′ₜ`. Inside show:

- green `ACCEPT → Hₜ₊₁ = H′ₜ`
- red `REJECT → Hₜ₊₁ = Hₜ`

From selection, a thick arrow labeled `下一代` returns to `当前 Harness Hₜ`.

Center-bottom: a small dashed navy memory box `Evolution Memory`, with `accepted + rejected changes · observed outcomes`. Selection writes to it; it feeds the Evolver. It is supporting state, not a numbered stage.

## Fixed outer boundary

Enclose the whole loop in a subtle thin gray frame titled `固定在循环之外`. Along the top edge of that frame place four lock-marked labels: `任务与代码起点 D`, `Ground Truth 与 Rubric E`, `模型与权限`, `统一成本口径`. These feed the single shared runner and cannot be modified by Evolver.

## Text

Main title: `MATSPEC 如何用同一个执行器进化自己`

Subtitle: `同一任务 · 同一验收 · 只改变 Harness`

Bottom conclusion in navy: `执行器不变，Harness 才是被优化对象`

## Constraints

- Exactly one `RUN + EVALUATE` / `统一运行与外部评测器` box.
- `当前 Harness Hₜ` and `候选 Harness H′ₜ` use the same visual shape because they are the same type of object.
- Show two evidence states `Tₜ` and `T′ₜ`, compared symmetrically.
- Do not reuse the old seven-step conveyor. Do not add `Replay + Evaluate` as a separate box.
- Preserve clean paper-like research schematic styling, not hand-drawn cartoon whiteboard, not colorful poster, not 3D.
- No people, robots, decorative icons, gradients, shadows, watermark, or tiny paragraphs.
- 16:9 landscape, strong whitespace, arrows must not cross labels.
- Render all math identifiers and English labels exactly.

