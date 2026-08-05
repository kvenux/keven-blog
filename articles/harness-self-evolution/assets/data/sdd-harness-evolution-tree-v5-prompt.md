# SDD Harness evolution tree v5 — imagegen prompt

Use case: infographic-diagram

Asset type: 16:9 article hero / mechanism diagram.

Primary request: Redraw the referenced whiteboard infographic as a true evolutionary genealogy for an SDD Harness. Preserve the expert hand-drawn whiteboard character, but replace the linear H-card conveyor belt with a branching evolutionary tree. Do not mention Lean anywhere.

## Composition

Create a wide 16:9 expert whiteboard diagram on warm off-white paper. Use mostly black and dark blue marker, muted green for surviving lineage, muted red for extinct branches, and a little amber for experiments. Avoid colorful poster styling. The picture has three visual zones plus one outer feedback arc.

### Left 38% — H0 full workflow anatomy

This must be the densest and most complete zone. Draw one tall framed panel titled `H0｜完整 SDD 流程`. Inside it, draw eight stacked stages with an arrow between every stage. Each stage has a stage name on the left and its durable process deliverable on the right, as if a document comes off an assembly line:

1. `需求澄清` → `proposal.md`
2. `行为规格` → `delta-spec.md`
3. `技术设计` → `delta-design.md`
4. `任务拆解` → `tasks.md`
5. `独立验证` → `validation.md`
6. `实现与测试` → `code + tests`
7. `代码评审` → `review.md`
8. `合并归档` → `spec.md + design.md`

Show the GT-backed Operator at the upper-left of this panel, holding a hidden booklet marked `GT`, driving the workflow end to end through repeated dialogue/review arrows. At the bottom of H0, stamp `交付件多｜阶段多｜上下文反复加载`. The point of this panel is to show exactly what the original Harness externalized, not merely generic inputs and outputs.

### Middle 42% — evolutionary genealogy, not a timeline

Title this zone `Harness 进化谱图`. Draw a left-to-right organic tree with a thick green surviving trunk and short red/amber dead-end branches. Every H node is a small circle or compact label with ONLY its mutation name; do not put miniature sessions, S1/S2/Sn, repeated workflows, or internal pipelines inside any H node.

The surviving solid-green trunk is:

`H0 全流程外显` → `H1 去独立验证` → `H3 阶段契约` → `H5 语义门禁` → `H11 公共契约` → `H12 delta-spec 核心`

Extinct branches grow from the latest surviving ancestor and end immediately with a blunt broken twig and red X; they must have no children and must never reconnect to the green trunk:

- from H1: `H2 批量实现｜未闭环`
- from H3: `H4 硬门禁｜卡死`
- from H5: `H6 多会话拆分｜重复探索`
- from H5: `H7 持续 review｜未交付`
- from H5: `H8 全量 spec｜收益不稳`
- from H5: `H9 多轮澄清｜不收敛`
- from H5: `H10 单轮澄清｜契约仍漏`

Make ancestry unmistakable: only the green trunk produces descendants. Failed/abandoned variants are leaves with no offspring. Do not display the nodes as equal cards in rows. Do not add `S1`, `S2`, `Sn`, version boxes, or a serpentine conveyor.

### Right 20% — converged H12 mechanism

Draw a compact destination panel titled `H12｜收敛形态`. Show exactly one simple horizontal mechanism:

`原始需求` + `GT Operator` → `delta-spec` → `编码 Agent` → `外部测试`

Make `delta-spec` the largest object in this panel: a single blue-edged durable document with three visible short labels inside: `增量行为`, `不变约束`, `验收示例`. Add a small green note beneath it: `唯一过程交付件`. The final code and tests are product outputs, not extra planning documents.

### Outer feedback arc

At the bottom, draw one broad blue feedback arc from real executions back toward the branching point, with four spaced icons and short labels: `Trajectory` → `盲评` → `成本` → `选择`. Show that GT Operator, candidate Agent, trajectory reviewer, and blind judge are agents in the evaluation system. The selection arrow points to the surviving green trunk, never to a dead branch.

## Exact visible text

Main title: `SDD Harness 的自演进之路`

Subtitle: `H0 → H12：保留信息增益，淘汰流程负担`

Bottom conclusion: `不可恢复的产品决策进入 delta-spec；可恢复的实现过程交还模型；结果由外部测试验收`

Render all identifiers verbatim, especially `delta-spec`, `proposal.md`, `delta-spec.md`, `delta-design.md`, `tasks.md`, `validation.md`, `review.md`, `spec.md + design.md`, `GT Operator`, `Trajectory`, and H0–H12. Chinese handwriting must be clear and legible.

## Visual constraints

- Expert whiteboard / research notebook feel, not a commercial infographic, PPT, cartoon, or flat vector poster.
- High information density on the left, visual focus on the green genealogy in the middle, conceptual compression on the right.
- Muted palette: black, dark blue, muted green, restrained amber and red only.
- 16:9 landscape, generous margins, no vertical poster composition.
- No formulas. No `Lean`. No `S1`, `S2`, `Sn`. No duplicated per-version process diagrams.
- No descendant arrows from extinct variants. No branch reconnection. No vague phrase such as `一份耐久文档`; use the technical term `delta-spec`.
- No watermark, no decorative gradients, no tiny illegible paragraphs.

