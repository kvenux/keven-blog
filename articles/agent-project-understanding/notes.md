
## 2026-09-23：实验说明与费用核对

> **实验说明**：使用源码提交 `a397130845f89d12368fe7059e87cc4dd34c2e03`。首轮启动因连接超时中止，未进入探索；表中统计后续完成的会话。Codex CLI 0.154.0 对指定模型报告元数据回退警告，首条命令出现 PowerShell profile 加载警告，后续自行使用 `-NoProfile`。这些环境差异已保留，不能将单次结果当作跨模型效率对照。原始会话持久化保存，未使用 `--ephemeral`。

正文精简重复限定，实验异常仍保留于原始报告。场景题为研究者构造，不对应真实PR。

费用使用2026-09-23官方Standard短上下文价格：非缓存输入$2/M、缓存输入$0.20/M、输出$10/M、缓存写入$2.50/M。记录中缓存写入为0；累计输入255468低于272K，因此无单次请求超过该阈值。按API费率等价折算，并非Codex订阅的实付账单。


## 第四、第五章数据来源（本轮核对）

- CodeWiki N/W/F：D:/repo-exploration-gt/codewiki-docs/evaluation/full30/RESULTS.md；阅读率口径参考同目录 metrics.json 及 myexp/output/slides/agent-project-understanding/build.py 的逐项审计提取。
- 任务定向 O/R：D:/repo-exploration-gt/codewiki-targeted/20260914-all6/RESULTS.md。
- 同一 Agent 自行选段 S：D:/repo-exploration-gt/codewiki-self-select/20260914-five/RESULTS.md。
- Django 文档与源码窗口五题三次：D:/repotrace-30/preflight/20260917-django-five-repeat3/RESULTS.md。质量未由 token 推断，缓存题两次来源审计失败、六次重连写入正文。
- Django 短卡稳定性/复用：D:/repotrace-30/projects/django/20260919-stability-reuse-v1/RESULTS.md、ANALYSIS.md、knowledge/card.txt、knowledge/addition-K.txt。
- 各批 Native 仅与所在批处理组比较；模型、提示词、评分、材料不同，不作跨批效率排名。正文费用为在线解题估算，知识制作/评分成本不混入；短卡批全流程45个模型会话9,471,428 token/$12.63见原报告，未将其当解题费用。


## RQ3 切换为 Astra 卡片对照

按用户要求，RQ3 改用 D:/repo-exploration-gt/codewiki-cards/20260914-two/RESULTS.md。解题与评分均为 gpt-6-astra medium，两项目十题三组各一次，共30次新解题。原 Terra high 稳定性/复用结果从正文删除。RQ1 解题仍为 Astra medium，评分维持原 Terra high 协议；未把历史评分模型改写成 Astra。RQ2 各批评分强度维持原记录。


## RQ3 改回 Astra 单题重复与迁移

按用户要求，以单题正向收益→重复→冻结知识迁移串起 RQ2/RQ3。来源为 D:/repotrace-30/preflight/20260917-django-five-repeat3/RESULTS.md 与 QUALITY-SPOTCHECK.json。正文用“定向知识/知识增强”准确描述文档＋源码窗口方案，不将其冒称605字短卡片。三次token变化按对应重复编号计算；三次节省不等同于更广泛稳定性证明。迁移结果选择文中说明的三题；剩余缓存题两次来源审计失败，原表与说明完整保留。未做全量数值评分，正文标记固定样本抽查。


## 收尾章节的依据与表述范围

- 神经连接可塑性与学习：[Structural plasticity and memory](https://www.nature.com/articles/nrn1301)。仅支持经验可改变神经结构，不把概念网络等同于逐节点神经连线。
- 代码追踪中的工作记忆负担：[The Role of Working Memory in Program Tracing](https://arxiv.org/abs/2101.06305)。图文减负作为信息组织机制解释，不宣称人普遍不擅长代码或LLM不存在形式差异。
- 恢复项目隐性知识的成本：[Maintaining mental models](https://www.microsoft.com/en-us/research/publication/maintaining-mental-models-a-study-of-developer-work-habits/)。
- 大规模代码训练的公开先例：[Evaluating Large Language Models Trained on Code](https://arxiv.org/abs/2107.03374)。不能据此断言被测模型读过人类大部分代码仓；正文将“文明级”作为作者对知识广度的比喻。
- 便宜的探索相对知识供给成本，由本文实验支撑；未测量同题人类用时，不声称实验已量化人机成本比。后训练的烦躁与移动靶为作者体验，不将跨版本变化归因为已验证的特定训练方法。


## 2026-09-23 配图完成

采用内置 image_gen，四张细笔白板手绘图已存 assets 并插入 source.md。最终提示词见 image-prompts-v4.md（封面）和 image-prompts-final.md（三张正文图）。v1卡通、v2论文风、v3编辑插画均未采用。封面复核后移除生成模型擅自补写的Python代码与虚构目录，改为案例对应的职责与事实；四张最终图均目视复核文字、反馈方向与实验证据边界。只修改内容资产，没有发布或同步渠道版本。


## 白板视觉增强

用户反馈细笔版太素，保留文字和机制，使用内置image_gen为四张图增加马克笔涂色、节点层次、手绘小线稿和主次箭头。逐张目视复核，正文已切换为 assets/*-rich.png；原细笔版保留。提示词见 image-prompts-rich-whiteboard.md。
