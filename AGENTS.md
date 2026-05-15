# 仓库协作规则

本仓库是 Hugo 博客和多平台内容资产库。后续 Agent 或人工协作时，必须遵守下面的目录边界。

## 目录边界

`content/posts/` 是 Hugo 唯一的博客发布目录。

- 已发布博客文章保留在 `content/posts/<slug>/index.md`。
- 文章图片放在 `content/posts/<slug>/images/`。
- 修改这里会影响博客页面和 GitHub Pages 发布结果。

`articles/` 是长期内容资产库，不参与 Hugo 构建。

- 每篇文章使用 `articles/<slug>/source.md` 作为主原稿。
- `articles/<slug>/assets/` 放源图片和素材。
- `articles/<slug>/notes.md` 可放备注、参考、改写计划。
- 这里不是草稿目录，里面可以放已成稿、已发布或准备改写到其他平台的正式稿。

`channels/` 是平台版本库，不参与 Hugo 构建。

- `channels/zhihu/` 放知乎版。
- `channels/wechat/` 放公众号版。
- `channels/podcast/` 放播客稿、shownotes 或播客衍生文本。
- 平台版本可以根据平台语境改写，但不要反向污染主原稿和博客发布版。

## 自动化边界

GitHub Pages 自动化只处理博客站点：

```text
content/posts/ -> Hugo build -> GitHub Pages
```

当前不要把知乎、公众号、播客等平台发布接入 CI，也不要在 GitHub Actions 中调用 Wechatsync。

平台发布先手动：

```powershell
wechatsync sync channels/zhihu/<slug>.md -p zhihu
wechatsync sync channels/wechat/<slug>.md -p weixin
```

## 图片规则

- 源图片优先放在 `articles/<slug>/assets/`。
- 博客发布版使用 `content/posts/<slug>/images/`。
- 平台版本发布时允许引用本地图片，由 Wechatsync 上传到目标平台图床。
- 不要把平台图床 URL 写回 `articles/<slug>/source.md`。

## 图片生成自动化

需要批量生成图片时，优先使用 Codex 订阅可用的内置 `image_gen` 工具。批量任务通过启动多个 `codex exec` 子进程并发完成，不要求额外配置 `OPENAI_API_KEY`。

约定：

- 批量生成默认按并发 5 组织任务，除非用户明确要求调整；每个子进程负责一张图或一个独立资产。
- 批量输入 JSONL 临时文件放在 `tmp/imagegen/`。
- 批量输出先放在 `output/imagegen/` 或 `articles/<slug>/assets/`，确认用于博客发布后再复制到 `content/posts/<slug>/images/`。
- 内置 `image_gen` 生成的图片如落在 `$CODEX_HOME/generated_images/`，需要再移动或复制到上面的项目目录。
- `gpt-image-2` 不支持 `background=transparent`；透明图优先走纯色背景生成后本地抠图，确需原生透明时再改用 `gpt-image-1.5`。
- 只有在用户明确要求 API/CLI fallback、需要 `generate-batch` 子命令，或内置工具不可用时，才使用 Codex imagegen skill 的 `scripts/image_gen.py`；该 fallback 是 OpenAI Images API 路径，可能需要 `OPENAI_API_KEY`。

订阅路径的批量任务清单示例：

```jsonl
{"prompt":"A clean editorial hero image for an AI coding blog","size":"1536x1024","quality":"high","out":"ai-coding-hero.png"}
{"prompt":"A minimalist desk setup with terminal, notebook, and warm side light","size":"1536x1024","quality":"medium","out":"desk-terminal.png"}
```

PowerShell 并发执行形态：

```powershell
$tasks = @(
  @{ Name = "ai-coding-hero"; Prompt = "Generate one image using built-in image_gen, save to output/imagegen/ai-coding-hero.png." },
  @{ Name = "desk-terminal"; Prompt = "Generate one image using built-in image_gen, save to output/imagegen/desk-terminal.png." }
)

$jobs = foreach ($task in $tasks) {
  Start-Job -Name $task.Name -ScriptBlock {
    param($prompt, $cwd)
    Set-Location $cwd
    codex exec -C $cwd -s workspace-write $prompt
  } -ArgumentList $task.Prompt, (Get-Location).Path
}

Wait-Job $jobs | Receive-Job
```

## 修改原则

- 不要删除 `content/posts/` 中已有文章，除非用户明确要求。
- 不要为了平台发布改动博客发布版正文。
- 不要为了博客排版改动主原稿语义。
- 结构性迁移前先复制保护内容，再做目录调整。
- Hugo 构建必须保持只依赖 `content/`、`layouts/`、`static/`、`data/` 等站点目录。

## 图谱规则

图谱抽取以 `content/posts/<slug>/index.md` 为输入：

```powershell
powershell -ExecutionPolicy Bypass -File tools/graph-all.ps1 -Parallel
```

生成结果：

- 单篇图谱：`data/graph/articles/<slug>.json`
- 跨文章桥接：`data/graph/bridges.json`
- 前端图谱：`static/graph/knowledge-graph.json`

图谱是博客站点能力的一部分，平台版本不参与图谱抽取，除非用户另行要求。
