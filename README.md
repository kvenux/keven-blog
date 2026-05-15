# Keven Blog

一个面向 GitHub Pages 的 Hugo 个人博客，同时保留主原稿和多平台发布版本。

## 目录职责

这个仓库把“内容资产”“博客发布”“平台版本”分开管理。

```text
articles/
  <slug>/
    source.md
    notes.md
    assets/

content/
  posts/
    <slug>/
      index.md
      images/

channels/
  zhihu/
  wechat/
  podcast/
```

### `articles/`

`articles/` 是长期内容资产库，不参与 Hugo 构建。

- `source.md` 是文章主原稿，也可以是已经成稿的母版。
- `notes.md` 可放素材、结构备注、改写提示、参考链接。
- `assets/` 放该文章的源图片和其他素材。

这里不是草稿目录。里面的文章可以是已发布文章，也可以是准备改写到知乎、公众号、播客等渠道的正式稿。

### `content/posts/`

`content/posts/` 是 Hugo 实际发布目录，也是 GitHub Pages 构建站点时使用的博客内容。

每篇文章使用 page bundle：

```text
content/posts/<slug>/index.md
content/posts/<slug>/images/
```

博客页面 URL 由这里决定。不要为了平台发布去改这里的正文风格、图片路径或排版。

### `channels/`

`channels/` 是平台版本库，不参与 Hugo 构建。

- `channels/zhihu/` 放知乎版。
- `channels/wechat/` 放公众号版。
- `channels/podcast/` 放播客稿、shownotes 或播客衍生文本。

平台版本可以根据平台语境改标题、开头、摘要、图片说明和结尾，但不要反向污染 `articles/<slug>/source.md` 和 `content/posts/<slug>/index.md`。

当前不把平台发布接入自动化流程。知乎、公众号等平台发布先手动处理，可以使用 Wechatsync：

```powershell
wechatsync sync channels/zhihu/<slug>.md -p zhihu
wechatsync sync channels/wechat/<slug>.md -p weixin
```

## 图片规则

文章图片按来源和发布目标分开：

- 源图片放在 `articles/<slug>/assets/`。
- Hugo 博客使用 `content/posts/<slug>/images/`。
- 平台版本里的本地图片可以引用源图片或平台版旁边的图片；发布时由 Wechatsync 上传到目标平台图床。

不要把知乎、公众号等平台图床 URL 写回 `articles/` 主原稿。

## 写作流程

推荐流程：

1. 在 `articles/<slug>/source.md` 写主原稿。
2. 需要发布博客时，整理到 `content/posts/<slug>/index.md`。
3. 需要发布知乎、公众号或播客时，复制并改写到 `channels/<platform>/<slug>.md`。
4. 博客发布走 GitHub Pages 自动化；平台发布先手动。

## 本地预览

```powershell
hugo server -D
```

然后打开 `http://127.0.0.1:1313`。

## 发布到 GitHub Pages

项目已包含 `.github/workflows/hugo.yml`。推送到 `main` 分支后，GitHub Actions 会构建 Hugo 站点并部署到 Pages。

在 GitHub 仓库里进入 `Settings -> Pages`，Source 选择 `GitHub Actions`。

GitHub Pages 自动化只发布博客站点，不会发布 `articles/` 或 `channels/` 里的平台版本。

## 知识图谱

文章迁移到 `content/posts/<slug>/index.md` 后，可以用 Codex CLI 抽取图谱元数据：

```powershell
powershell -ExecutionPolicy Bypass -File tools/extract-graph.ps1 -Slug my-post -ArticlePath content/posts/my-post/index.md
node tools/build-graph.mjs
```

批量处理所有还没有图谱 JSON 的文章：

```powershell
powershell -ExecutionPolicy Bypass -File tools/graph-all.ps1 -Parallel
```

抽取结果放在 `data/graph/articles/`，跨文章的人工桥接关系放在 `data/graph/bridges.json`。前端图谱读取 `static/graph/knowledge-graph.json`。

## 配置

站点标题、语言、固定链接等配置在 `hugo.toml`。

如果是用户站点，仓库名通常是 `username.github.io`。如果是项目站点，当前 workflow 会自动使用 GitHub Pages 提供的 base URL 构建，不需要手动改 `baseURL`。
