# MatSpec Harness self-evolution architecture prompt, v2

Use case: infographic-diagram

Asset type: lead architecture figure for a Chinese technical essay about autonomous Harness self-evolution.

Primary request:

Create a publication-quality, information-dense but instantly understandable 16:9 landscape systems diagram titled "HOW MATSPEC IMPROVES ITSELF". Use the spatial logic of a genetic algorithm cycle: execute, observe, generate a candidate, evaluate fitness, select, then advance to the next generation. Do not include biological imagery or inappropriate GA operators such as crossover. No formulas.

Composition — the outer loop must be the dominant visual:

Arrange the seven stages CLOCKWISE around one large horizontal oval / rounded-rectangular loop, leaving a clean center. Do NOT make a straight one-row pipeline.

- Upper left: "CURRENT MATSPEC"
- Upper middle-left: "RUN TASK PANEL"
- Upper middle-right: "TRAJECTORY DATASET"
- Right side: "EVOLVER AGENT"
- Lower right: "CANDIDATE MATSPEC"
- Lower middle: "REPLAY + EVALUATE"
- Lower left: "SELECT"
- A short, strong upward arrow from SELECT to CURRENT MATSPEC labeled "NEXT GENERATION" must visibly close the loop.

The clockwise reading order and every arrowhead must be unambiguous.

Exact supporting copy:

CURRENT MATSPEC
"workflow · instructions · context handoff · review gates"

RUN TASK PANEL
"8 real tasks × 3 runs"

TRAJECTORY DATASET
"Candidate sessions · Operator decisions · product outcomes"
"time · tokens · tool calls"

Small annotation: "append-only after each run"

EVOLVER AGENT
"find failure causes · repeated work"
"useful vs redundant stages"

CANDIDATE MATSPEC
"bounded Harness edits"

REPLAY + EVALUATE
"same tasks · focused tests · 2 blind judges"
"completion · quality · cost"

SELECT

- Green branch: "ACCEPT — promote candidate"
- Red branch: "REJECT — keep current"

Both decisions feed the short NEXT GENERATION arrow back to CURRENT MATSPEC. ACCEPT and REJECT are decision outcomes, not two giant perimeter return lines.

Compact nested execution detail:

Inside the visual region of RUN TASK PANEL, or directly attached beneath it as one concise expansion panel, show a small closed loop headed "OPERATOR-DRIVEN SDD".

Exact nodes:

"GT / Reference" → "OPERATOR AGENT" → "MATSPEC WORKFLOW" → "CANDIDATE AGENT"

Forward control label:

"start · answer · review · accept / revise · archive"

Return evidence arrow from CANDIDATE AGENT back to OPERATOR AGENT:

"questions · artifacts · code · tests"

Small note: "repeat until archived"

Make it clear that GT / Reference flows only to OPERATOR AGENT. Candidate must not have a direct arrow from GT / Reference. The Operator drives the whole SDD process.

Persistent memory:

Place a restrained central supporting node in the open center of the outer loop:

"EVOLUTION MEMORY"
"accepted + rejected changes · observed outcomes"

One arrow from SELECT to EVOLUTION MEMORY. One arrow from EVOLUTION MEMORY to EVOLVER AGENT. Memory is secondary support, not the main hub and not the task execution path.

Visual style:

- True 16:9 horizontal composition, wide and shallow, approximately 1920×1080.
- White or very light warm-gray paper background.
- Mostly black, charcoal, gray, and one restrained dark navy accent.
- Green only for ACCEPT; red only for REJECT.
- Editorial research-blog / systems-paper quality: crisp vector-like lines, disciplined spacing, fine rules, strong typographic hierarchy.
- Use semantic regions, fine outlines, and well-routed arrows. Avoid a row of equal colorful cards.
- Flat 2D. No gradients, no shadows, no glossy UI, no 3D, no clip-art, no robots, no DNA, no chromosomes, no decorative icons, no rainbow palette.
- English labels only, rendered verbatim and legibly. Avoid tiny text.
- Keep the title modest, not oversized; maximize the diagram area.
- No top control-setting strip, no experiment-protocol banner, no "Candidate cannot access" banner.
- No watermark, no logos, no extra text.

Reading hierarchy:

- In 5 seconds: current Harness produces trajectories, Evolver creates a candidate, replay evaluates it, selection creates the next generation.
- In 30 seconds: task execution is Operator-driven using GT; trajectories include decisions and costs; accepted and rejected outcomes accumulate in evolution memory.
