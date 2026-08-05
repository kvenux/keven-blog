# MatSpec Harness evolution loop with historical data bucket — imagegen prompt

Use case: infographic-diagram

Asset type: 16:9 article mechanism diagram.

Reference style: match `self-evolution-shared-runner-v4.png` and the earlier MatSpec loop figure: clean white research-paper background, thin black rounded rectangles, strong black arrows, dark navy accents, restrained green/red decision paths, compact sans-serif typography. No hand-drawn characters or commercial poster styling.

## Core model

This is not a paired current-vs-candidate replay diagram. It is a continuous search loop over accumulated history:

`历史数据桶 → 归因与策略搜索 → Harness Change Proposal → 候选 Harness → 真实任务运行 → 新轨迹与评价报告 → 与历史前沿比较 → ACCEPT / REJECT → 写回历史数据桶 → 下一份 Proposal`

## Layout

Draw one large clockwise loop with a visually dominant database/data-bucket cylinder on the left.

### Left: historical data bucket

Draw a large dark-navy outlined database cylinder / data barrel titled `历史版本与实验记录`. It must unmistakably look like a data bucket, not a rectangular card. Inside, show four stacked labeled layers separated by thin lines:

- `H0 … Hn Harness`
- `完整 Trajectory`
- `Evaluation Reports`
- `Accepted / Rejected Proposals`

Add a small label under the cylinder: `进化记忆：成功与失败都保留`.

This bucket has two outgoing information arrows: one to the Evolver for strategy generation, and one dashed reference arrow to the historical comparison gate. Both ACCEPT and REJECT paths write their results back into this same bucket.

### Top-center: strategy and proposal

Draw a box `Evolver / Trajectory Reviewer`, with short text `跨代归因 · 找重复失败 · 搜索下一种策略`.

Arrow into a distinct document-shaped card titled `Harness Change Proposal`. Inside four short rows:

- `问题归因`
- `策略变化`
- `预期收益`
- `否决条件`

Proposal must be a visible separate stage between analysis and candidate implementation.

### Top-right: candidate and run

Arrow from Proposal to a rounded state box `候选 Harness H′` with short text `应用 Proposal 后的工作流`.

Arrow downward to one execution box `运行真实任务`, containing `相同任务集 · 3 次独立运行` and `Candidate sessions`.

### Bottom-center/right: evidence and comparison

Arrow from real run to a report/document bundle titled `新 Trajectory + 评价报告`. Inside:

- `产品质量 · 完成率`
- `时间 · Token · Tool calls`

Arrow to a diamond-shaped decision gate or strong comparison box titled `与历史质量—成本前沿比较`. A dashed arrow from the historical data bucket also enters this comparison gate, labeled `历代基准`.

### Explicit ACCEPT and REJECT branches

From the comparison gate draw two equally visible outgoing branches:

- Green branch labeled `ACCEPT｜明显改善`. It goes to a green box `进入下一代谱系`, then writes `有效策略 + 新版本 + 报告` back into the historical data bucket.
- Red branch labeled `REJECT｜退化或无显著增益`. It goes to a red-outlined dead-end box `不产生子孙`, then writes `失败假设 + 反证 + 报告` back into the historical data bucket.

After both results are written back, one clear navy loop arrow from the bucket returns to `Evolver / Trajectory Reviewer`, labeled `提出下一份 Proposal`. This shows that both acceptance and rejection trigger the next search iteration.

## Exact visible text

Title only: `MatSpec Harness 的自进化循环`

Do not render a subtitle. Do not render keyword slogans beneath the title.

Bottom conclusion: `每次真实运行都更新历史；每份历史都改变下一次策略`

## Strict constraints

- Historical versions and experiment records must be drawn as a large database cylinder/data bucket.
- Proposal must be a separate visible document stage.
- Show one real run after candidate creation, not a blue replay arrow and not a shared-runner A/B diagram.
- ACCEPT and REJECT must be explicit outgoing branches, not text hidden inside the comparison box.
- Rejected candidates do not produce descendants, but their evidence returns to history.
- Accepted candidates enter the lineage and their evidence also returns to history.
- No top row of fixed-condition boxes. No subtitle. No numbered step badges.
- No `Tₜ` / `T′ₜ` paired comparison notation. No people, robots, locks, decorative icons, gradients, 3D effects, watermark, or tiny paragraphs.
- Keep arrows clean and non-crossing. 16:9 landscape.

