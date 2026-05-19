# CC 的丝滑，是 CLI 给的

**—— PodDeck 复盘**

---

我做了个网站叫 **PodDeck**，把几十期 2-3 小时的长播客，自动转成 20-30 页可翻的 deck，扔在 GitHub Pages 上。

地址：[kvenux.github.io/poddeck](https://kvenux.github.io/poddeck/)。不知道从哪开始，就先翻这几张：

- [Dario Amodei — "We are near the end of the exponential"](https://kvenux.github.io/poddeck/episodes/n1E9IZfvGMA/) —— A 社 CEO：AI 算力指数曲线已经接近尾声
- [Boris Cherny — Head of Claude Code](https://kvenux.github.io/poddeck/episodes/We7BZVKbCVw/) —— CC 作者：AI coding 已经解题，公司里大部分人开始用 CC 干编码以外的事
- [Jensen Huang — Will Nvidia's moat persist?](https://kvenux.github.io/poddeck/episodes/Hrbq66XqtCo/) —— 老黄：跟台积电从来不签合同，60 个人直接汇报，不搞 1:1
- [Andrej Karpathy — From Vibe Coding to Agentic Engineering](https://kvenux.github.io/poddeck/episodes/96jN2OCOfLs/) —— vibe coding 之后，工程的真正形态是什么
- [Terence Tao — How the world's top mathematician uses AI](https://kvenux.github.io/poddeck/episodes/Q8Fkpi18QXU/) —— 顶级数学家把 AI 当协作工具的具体方式

整个东西是一个**周末带娃的间隙**搞出来的——零零散散几个小时的碎片，从我问"有没有下字幕的 cli"，到能发朋友圈的版本部署上线。我没敲过一条命令，也没写过一行代码。

唯一不便宜的地方是 token：每一集要走理解 → 编辑 → 视觉 → 事实校验 → playwright 自审，单期消耗不亚于开发一个新需求。能这么干，是因为接口的摩擦力小到可以忽略，钱花在了内容本身上。

这件事复盘到底，结论是反直觉的：让它这么快搭起来的不是模型变聪明了，是**字符接口时代**早就把 AI 友好的工具链做完了，AI 只是终于来用。

## 一个周末分几段干完的

- **第一段**：问 cli → 装 `yt-dlp` → 拿到 Boris、Jensen、Dario 三期字幕 → 让 CC 去 GitHub 上搜"播客转 slides"的项目 → 撞上 Slidev
- **第二段**：跑第一版 deck → 视觉审查 → 把硬规则注进 subprocess 的系统提示词 → 并行 3 个进程生成
- **第三段**：建仓、配 Actions、部署 Pages
- **最后一段**：发朋友圈

中间我做的事就三件：**提诉求、提愿望、验收**。剩下的全是几条 CLI 串起来跑完的。

## yt-dlp：一条命令把字幕拿到

```bash
yt-dlp --write-auto-sub --sub-lang en --skip-download <url>
```

输入一个 URL，输出一个 VTT。flag 全在 `--help` 里，失败有标准报错，可枚举、可组合、可重试。AI 看一眼就会用，出错也知道怎么自愈。

这个工具的前身 `youtube-dl` 始于 2008，作者当年想的不是"让 LLM 能下视频"。他只是按 Unix 那套做事：单一职责、文本进文本出、文档贴在 `--help`。十几年后这套接口刚好就是 AI 最舒服的输入。

## gh：建仓、跑 Actions、部署 Pages 都不用打开浏览器

`gh repo create`、`gh pr view`、`gh run watch`——这些命令我自己几乎没敲过，全是让 AI 干。所以"建 GitHub 仓库 + 配 Actions + 部署 Pages"那一步我没担心，知道这条路在 CLI 上通。

`gh` 把原本只能在网页里点的事折叠成了命令。**这种把 GUI 操作还原回字符接口的产品，给 AI 留了一条干净的代理通道**——它读得到输出、看得见 exit code、能自己重试。要是只剩网页 UI，AI 要么去解 DOM 要么去做视觉点击，摩擦力大一个量级。

## Slidev：markdown 直接出 deck

让 AI 写 PPT 是个尴尬场景：OOXML 太重，python-pptx 的 API 不直观，Google Slides 要走 OAuth。但 Slidev 把 deck 退回成 markdown：

```bash
slidev build slides.md --base /poddeck/episodes/<id>/
```

输入是 markdown，输出是个静态 SPA。AI 写 markdown 是它的母语。我在 `CLAUDE.md` 里定的所有视觉规范——two-cols 大图、卡片网格的配色、Excalidraw 的引用——subprocess 都直接照着写 markdown，全程不碰任何 GUI。

## CC 的丝滑，是 CLI 给的

把这三个工具放一起看，会发现一个共同模式：**它们没有为 AI 做任何特殊适配，但它们刚好长成了 AI 最容易使的样子**。

Claude Code 这个产品本身也是同一个机制。它真正赢的地方不是模型更聪明，是它**活在一个接口已经为它准备好的世界里**——terminal、git、npm、kubectl、ffmpeg、grep、jq、make，全是字符进字符出、副作用可观测、错误码标准化。这套接口最早是为"会 grep 的人"设计的，今天发现它对 LLM 也是最低摩擦。

反观大部分 SaaS 的"AI 战略"——在 GUI 里塞一个 chatbox。方向是反的。GUI 是给眼睛和手做的，把眼睛和手抠掉以后剩下的是空的。真正能让 AI 干活的地方，是产品本身就有一个干净的 CLI。

## AI 时代不是新时代，是字符接口时代被重新放大

这件事让我重新看待"AI 时代"这个词。

它不是一个全新时代。它是**字符接口时代**重新被放大的时代。`yt-dlp`、`gh`、`ffmpeg`、`sed`、`make` 这一堆工具，过去只在"会 grep 的人"手里发挥作用，今天被 AI 接管后，任何能提需求的人都用得动了。

反过来，那些一开始就只活在 GUI 里、没有干净 CLI 的产品——大部分企业 SaaS、大部分 BI、大部分 IT 系统——反而是 AI 最难下手的地方。它们留给 AI 的接口太窄。

PodDeck 这件事我能用周末几小时碎片搭出来，功劳不在我，也不在模型。是 `yt-dlp` 的维护者、`gh` 的团队、Slidev 的作者，过去这些年一直按 Unix 哲学做事，**不小心把 AI 时代的接口提前交付了**。

开源社区从来不是为 AI 准备的。但他们一直在做的事——单一职责、文本输入输出、错误码标准化、文档塞进 `--help`——刚好就是 AI 友好。

---

**PodDeck**：[kvenux.github.io/poddeck](https://kvenux.github.io/poddeck/)
**源码**：[github.com/kvenux/poddeck](https://github.com/kvenux/poddeck)
