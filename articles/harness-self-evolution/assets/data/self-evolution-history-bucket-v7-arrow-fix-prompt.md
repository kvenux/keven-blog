# MatSpec self-evolution v7 — feedback arrow correction

Use case: infographic-diagram

Edit `self-evolution-history-bucket-v6.png` while preserving every node, badge, label, position, style, and main-flow arrow.

Make one category of correction: clean up the history feedback wiring.

1. Remove the redundant short black arrow from the data bucket directly into the left side of `2 Evolver / Trajectory Reviewer`. Keep only the large navy arrow labeled `下一轮：提出新的 Proposal`, which must clearly start from the updated history bucket and end at node 2.
2. Reroute the two write-back paths so they never cross:
   - Green ACCEPT: exit the left side of `进入下一代谱系`, travel horizontally left in an upper return lane, and enter a green port on the lower-right side of the data bucket. Label `新版本 + 有效策略 + 报告`.
   - Red REJECT: exit the bottom of `不产生子孙`, travel down and then left in a separate lower return lane, and enter a red port on the bottom-left side of the data bucket. Label `失败假设 + 反证 + 报告`.
3. Do not let either return line cross the other, the Accept/Reject branch lines, the bottom conclusion, or any box.

Do not change the correct main flow `2 → 3 → 4 → 5 → 6 → 7`, the dashed `历代基准` arrow from bucket to node 7, or the split from node 7 into 8A and 8B.

