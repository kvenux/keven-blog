# SDD Harness family tree v6 — imagegen prompt

Use case: infographic-diagram

Asset type: 16:9 article mechanism diagram.

Primary request: Completely redraw the referenced image. The middle must look like a real top-down family tree / evolutionary cladogram, not a vertical trunk with attributes. Remove every Operator/person/agent-role illustration from the left and right. The right side must explain the first-principles filter that produced the final Harness.

## Overall layout

Warm off-white paper, expert marker-whiteboard style, 16:9 landscape. Three columns: full H0 anatomy on the left (34%), a broad top-down binary genealogy in the middle (42%), and a first-principles decision filter on the right (24%). Mostly black and dark blue; muted green means selected/surviving; amber/red means rejected/extinct. No commercial infographic look.

## Left — complete H0 workflow, no people

Title: `H0｜完整 SDD 流程`

Show eight stacked phases as a dense but readable pipeline. Each phase produces a visible durable artifact:

1. `需求澄清` → `proposal.md`
2. `行为规格` → `delta-spec.md`
3. `技术设计` → `delta-design.md`
4. `任务拆解` → `tasks.md`
5. `独立验证` → `validation.md`
6. `实现与测试` → `code + tests`
7. `代码评审` → `review.md`
8. `合并归档` → `spec.md + design.md`

Bottom red stamp: `交付件多｜阶段多｜上下文反复加载`

There must be no human, Operator, GT booklet, robot, agent role, or dialogue icon in this column.

## Middle — broad binary family tree descending from top to bottom

Title: `Harness 进化族谱`

This is the visual focus. It must resemble a real genealogy chart or biological cladogram: one ancestor at the top, horizontal sibling pairs under fork connectors, later generations lower down. Use broad horizontal spread and at least six distinct vertical generations. Do not draw a single straight green spine. The selected lineage should zig-zag through the tree. Every split is binary.

Topology:

- Generation 0: `H0 全流程外显` at top center.
- H0 descends to `H1 去独立验证`.
- H1 forks into two children: left terminal leaf `H2 批量实现｜未闭环` with red X; right surviving child `H3 阶段契约`.
- H3 forks into: right terminal leaf `H4 硬门禁｜卡死` with red X; left surviving child `H5 语义门禁`.
- Below H5, use small unlabeled fork junctions to form a broad binary experimental family. Each rejected H version is a terminal leaf and has no descendants: `H6 多会话｜重复探索`, `H7 持续 review｜未交付`, `H8 全量 spec｜收益不稳`, `H9 多轮澄清｜不收敛`, `H10 单轮澄清｜契约仍漏`. These leaves should be distributed on both sides at different generations, never in one horizontal list.
- The only surviving branch from that experimental family reaches `H11 公共契约`, then ends at a large green leaf `H12 delta-spec 核心` near the bottom center.

Use green connectors only along the selected ancestry. Rejected variants use short amber/red connectors, end with a dead twig/red X, have no children, and never reconnect. Unlabeled fork junctions are allowed; do not invent new H versions. Do not place explanatory pipelines, S1/S2/Sn, or equal cards inside nodes.

At the bottom of the middle column, show a compact feedback loop around the tree roots: `Trajectory → 盲评 → 成本 → 选择 → 下一代`. No people or agent-role portraits.

## Right — first-principles decision filter

Title: `第一性原理：Harness 应该留下什么？`

Draw four stacked decision rows with a question on the left and its disposition on the right. Use simple icons only, no people and no robots:

1. `模型无法知道？` → `写入 delta-spec`
   small note: `产品决策不可恢复`
2. `仓库可以恢复？` → `按需读取`
   small note: `不重复搬运上下文`
3. `模型已经内化？` → `交还模型`
   small note: `规划与实现不外显`
4. `模型无法自证？` → `外部测试`
   small note: `结果必须可验收`

Under the four rows, derive one concise green conclusion panel:

`最终保留`

large document `delta-spec` containing `增量行为`, `不变约束`, `验收示例`

plus a shield/check icon labeled `外部验收`

The right column explains the reasoning, not an execution workflow.

## Exact text

Main title: `SDD Harness 的自演进之路`

Subtitle: `H0 → H12：在真实回放中选择，而不是一次裁剪`

Bottom conclusion: `保留不可恢复的信息增益；删除模型可恢复的流程负担；外部验证不能自证的结果`

## Constraints

- Absolutely no Operator, GT Operator, candidate Agent, reviewer, judge, human portrait, or robot anywhere.
- Middle is a broad top-down binary family tree, not a straight trunk, not a timeline, not rows of equal cards.
- Failed variants are childless leaves. No dead branch reconnects.
- No `Lean`, no `S1`, `S2`, `Sn`, no formulas, no repeated miniature workflows.
- Keep exact identifiers legible: H0–H12, `delta-spec`, and all `.md` filenames.
- No gradients, no watermark, no tiny paragraphs, no decorative clutter.

