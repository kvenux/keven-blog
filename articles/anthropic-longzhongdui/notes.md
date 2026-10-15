# notes

- 原稿来源：Downloads/anthropic-longzhongdui-opening (1).md（2026-10-15 导入；正文保持原稿原文，只插入配图）。
- 待核实（原稿给出，未独立验证）：路线图随Bartz案公开及2026-10在X上热议；Opus 5.5 Terminal-Bench 4.0 66.4%；2026-03 Claude Code源码泄露中验证代理、员工版提示词、补丁退役注释等细节。
- 已配封面+4张正文图（见下），尚未发布到content/posts/，也未做知乎/公众号版本。
- 配图01：assets/01-roadmap-review.png（评审会场景，codex exec无头模式+内置image_gen，whiteboard-infographic风格，画法参考model-provider-knows-your-work/assets/whiteboard-v4/04-feedback.png）。并行出a/b两张，选b（对话气泡直接指向发言人）；a保留为01-roadmap-review-a.png备选。提示词见01-roadmap-review.prompt.md。
- codex exec注意：`-i`是多值参数，会吞掉后面的位置参数，提示词要经stdin传入（末尾用`-`）。
- 封面00-cover：隆中对卷轴（荆州→益州→汉中）对照路线图（编程→工具使用→Claude Code），中间"五年复利"曲线。
- 配图02-compounding-loop（第二章开头）、03-copilot-vs-colleague（"为什么是Anthropic"一节）、04-patch-lifecycle（第三章，"下一代模型训练"节点用虚线标"推测"）。四张并行用codex exec生成，均一次通过；04的"办"字残缺，用image_gen编辑模式局部修正，提示词见04-patch-lifecycle.fix.prompt.md。
