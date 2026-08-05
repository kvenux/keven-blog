# MatSpec Harness self-evolution — numbered evidence-rich loop

Use case: infographic-diagram

Asset type: 16:9 article mechanism diagram.

Style reference: preserve the clean academic schematic style of `self-evolution-history-bucket-v5`: white research-paper background, precise black arrows, thin rounded rectangles, dark navy structure, green ACCEPT, red REJECT, compact sans-serif typography. Increase information density without becoming cluttered.

## Layout and numbered nodes

Use a clockwise loop with eight clearly numbered navy badges. Every number must map to the article explanation.

### 1 — Historical evidence bucket

Large database cylinder on the left titled `1 历史版本与实验记录`. Five visible layers:

- `H0 … Hn：workflow / code / config`
- `完整 sessions 与 Operator decisions`
- `product diff / focused tests`
- `质量 · 完成率 · 时间 · Token · calls`
- `Accepted / Rejected Proposals`

Footer inside bucket: `成功与失败都进入 Evolution Memory`.

### 2 — Cross-generation diagnosis

Top-left/center box `2 Evolver / Trajectory Reviewer`. Four compact findings:

- `遗漏模式`
- `重复探索`
- `无信息增益阶段`
- `质量—成本瓶颈`

### 3 — Change proposal

Document-shaped card `3 Harness Change Proposal`. Five rows:

- `证据与问题归因`
- `单一策略变化`
- `预期指标变化`
- `否决条件`
- `回滚边界`

### 4 — Candidate Harness

Box `4 候选 Harness H′` with four short components:

- `workflow`
- `instructions`
- `context handoff`
- `acceptance rules`

### 5 — Real paid experiment

Box `5 真实任务运行` containing:

- `8 个开源需求 × 3 次`
- `Candidate + GT Operator`
- `相同模型与权限`
- `完整 SDD trajectory`

Show this as an actual run, not replay.

### 6 — New evidence package

Stacked document/report bundle `6 新证据包` with two subheaders:

`Trajectory`:
- `session · decisions · product diff · tests`

`Evaluation Report`:
- `盲评分 · 完成率 · Active time`
- `Token · Tool calls`

### 7 — Compare against historical frontier

Large diamond or gate `7 与历史质量—成本前沿比较`. It receives the new evidence package and a dashed navy arrow from the historical data bucket labeled `历代基准`. Around the gate show three short decision criteria:

- `质量不退化`
- `完成率不下降`
- `质量—成本位置改善`

### 8 — Explicit selection and write-back

From node 7 split into two visible child branches with badges `8A` and `8B`:

- Green `8A ACCEPT｜明显改善` → box `进入下一代谱系` → green return arrow into data bucket labeled `新版本 + 有效策略 + 报告`.
- Red `8B REJECT｜退化或无显著增益` → box `不产生子孙` → red dashed return arrow into data bucket labeled `失败假设 + 反证 + 报告`.

Both paths update the same historical bucket. From the bucket, a large navy arrow returns to node 2 labeled `下一轮：提出新的 Proposal`.

## Text

Title only: `MatSpec Harness 的自进化循环`

No subtitle.

Bottom conclusion: `运行产生证据，证据改变 Proposal，选择决定谁能成为下一代`

## Constraints

- Preserve eight numbered nodes: 1, 2, 3, 4, 5, 6, 7, 8A/8B.
- Historical evidence must be a database cylinder.
- Proposal is its own numbered document stage.
- Explicit green Accept and red Reject branches, both writing evidence back to history.
- Rejected candidate has no descendants.
- No top fixed-condition boxes, no blue replay arrow, no paired T/T-prime notation.
- No people, robots, decorative illustrations, gradients, shadows, watermark.
- High but readable information density; no overlapping arrows; 16:9 landscape.

