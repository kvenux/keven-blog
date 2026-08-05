# MatSpec self-evolution v8 — merge diagnosis, proposal, candidate

Use case: infographic-diagram

Redraw the numbered MatSpec self-evolution diagram as six top-level stages. Merge old nodes 2, 3, and 4 into one large compound node because they are one mutation operation.

## Top-level numbered loop

1. Large database cylinder `1 历史版本与实验记录`.
2. Large compound box `2 生成候选 Harness`.
3. Box `3 真实任务运行`.
4. Report bundle `4 新证据包`.
5. Diamond `5 与历史质量—成本前沿比较`.
6A green ACCEPT and 6B red REJECT, both writing evidence back to node 1.

## Node 1 data bucket

Keep five layers:
- `H0 … Hn：workflow / code / config`
- `完整 sessions 与 Operator decisions`
- `product diff / focused tests`
- `质量 · 完成率 · 时间 · Token · calls`
- `Accepted / Rejected Proposals`

Footer: `成功与失败都进入 Evolution Memory`.

## Node 2 compound mutation operation

Inside one large navy-outlined box titled `2 生成候选 Harness`, show three internal columns connected left-to-right by small arrows:

`跨代归因`
- `遗漏模式`
- `重复探索`
- `无信息增益阶段`

→ document `Change Proposal`
- `单一策略变化`
- `预期指标变化`
- `否决条件`

→ state `Candidate H′`
- `workflow`
- `instructions`
- `context handoff`
- `acceptance rules`

These are internal substeps, not separately numbered stages.

## Node 3 real run

`3 真实任务运行`
- `8 个开源需求 × 3 次`
- `Candidate + GT Operator`
- `相同模型与权限`
- `完整 SDD trajectory`

## Node 4 evidence

`4 新证据包`
- `Trajectory：session · decisions · diff · tests`
- `Evaluation：盲评分 · 完成率 · Active time`
- `Token · Tool calls`

## Node 5 selection comparison

`5 与历史质量—成本前沿比较`
- `质量不退化`
- `完成率不下降`
- `质量—成本位置改善`

A dashed arrow from node 1 enters node 5 labeled `历代基准`.

## Node 6 branches and feedback

`6A ACCEPT｜明显改善` → `进入下一代谱系` → green write-back to data bucket: `新版本 + 有效策略 + 报告`.

`6B REJECT｜退化或无显著增益` → `不产生子孙` → red write-back to data bucket: `失败假设 + 反证 + 报告`.

Green must be strict serial order: node 5 → 6A → `进入下一代谱系` → data bucket. No direct node-5-to-bucket shortcut.

Red must be strict serial order: node 5 → 6B → `不产生子孙` → data bucket.

The green and red return lanes must not cross. After history is updated, one navy arrow from node 1 to node 2 is labeled `下一轮：生成新的候选 Harness`.

## Text and style

Title only: `MatSpec Harness 的自进化循环`

Bottom conclusion: `历史驱动变异，真实运行产生证据，选择决定谁能成为下一代`

Clean academic paper diagram, white background, thin black lines, dark navy structure, green/red selection. No subtitle, no people/robots, no top fixed boxes, no replay arrow, no T/T-prime notation, no arrow crossings.

