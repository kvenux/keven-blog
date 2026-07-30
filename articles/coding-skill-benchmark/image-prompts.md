# 图片生成记录

所有trajectory从raw rollout重新解析，并使用`C:\Users\kvenu\playground\trajtory-visualizer`的fixed-cell、Return-aware renderer生成，命令封装在`prepare-tool-trajectories.ps1`。RQ1的质量—Token二维图使用Matplotlib按精确坐标生成，脚本为`build-rq1-frontier.py`。其余解释性配图使用内置ImageGen生成，均在复制到文章目录后以原始分辨率人工检查。精确矩阵由正文HTML表格承载，不让生成式图片替代可审计数据表。

## `hero-skill-value.png`

横版16:9高密度专家白板机制图。顶部六张能力卡依次展示Bare、Grill Me、OpenSpec、Ponytail、Superpowers和MatrixSpec L0及其主要机制。中央“压缩不确定性”分为需求信息、跨阶段决策、验收证据三层；跨阶段层明确画出`proposal → spec → tasks`和“artifact压缩状态”。右侧使用盲评分、Tool Call和Token成本三只仪表盘表达质量—成本账本。底部画出“无新信息→重复review→上下文回放→Token黑洞”的失败闭环，并以“Skill ROI = 新信息 + 确认状态 + 新证据 − 流程成本”收束。禁止卡通人物、段落和自由增加小字。

## `experiment-protocol.png`

横版16:9高密度实验协议白板。六列从左到右依次为冻结任务、六个被测Agent、psmux受控交互、冻结证据、hidden suite与两名judge、结果矩阵。顶部显示`8 tasks × 6 arms × 3 runs = 144 trajectories`。Ground Truth区包含原始需求、参考实现和隐藏测试；证据区包含产品diff、Git状态、测试输出、过程日志和Token账本；judge只标注“处理标签盲化”，不使用“完全双盲”。底部显示同一baseline、网络关闭、remote移除、失败不替换、每格独立运行，并明确“operator协议是treatment差异”。

## `skill-routing.png`

横版16:9高密度不确定性路由图。中央是“先识别主导不确定性”，五条分支分别为需求不清、实现风险、跨阶段决策丢失、验收不明和过度实现；每个分支都列出触发、机制、停止三行。MatrixSpec L0的紫色分支为视觉中心，展示`proposal → spec → tasks`、阶段内复用thread、阶段间旋转thread和只传确认状态。底部红色传送带表示“默认全流程”，依次经过spec、plan、sub-agent和多轮review，同时推高Tool Call和Token；绿色闸门表示停止。底部公式为“最小机制 × 信息增益 × 明确停止 = 可持续Skill”。图中禁止出现“状态断裂”。

## `quality-token-frontier-matplotlib.png`

横轴为Candidate Token/run，纵轴为八任务盲评分。六个点使用正式矩阵数值；虚线连接当前任务面板中的描述性Pareto前沿，红色箭头标记Superpowers约10×Bare Token。首轮图的OpenSpec标签被底边裁切，扩大纵轴留白后重新生成并验图。
