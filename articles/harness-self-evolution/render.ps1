Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$articleRoot = $PSScriptRoot
$sourcePath = Join-Path $articleRoot 'source.md'
$outputPath = Join-Path $articleRoot 'source.html'
$markdown = Get-Content -Raw -LiteralPath $sourcePath

$titleMatch = [regex]::Match($markdown, '(?m)^title:\s*"(?<value>.+)"\s*$')
$descriptionMatch = [regex]::Match($markdown, '(?m)^description:\s*"(?<value>.+)"\s*$')
if (-not $titleMatch.Success -or -not $descriptionMatch.Success) {
    throw 'Missing title or description in Markdown front matter.'
}

$title = $titleMatch.Groups['value'].Value
$description = $descriptionMatch.Groups['value'].Value
$bodyMarkdown = [regex]::Replace($markdown, '(?s)^---\s*.*?\s*---\s*', '')
$bodyHtml = (ConvertFrom-Markdown -InputObject $bodyMarkdown).Html
$bodyHtml = [regex]::Replace($bodyHtml, '\*\*(?<text>[^*\r\n]+)\*\*', '<strong>${text}</strong>')
$bodyHtml = $bodyHtml.Replace('<table>', '<div class="table-wrap"><table>')
$bodyHtml = $bodyHtml.Replace('</table>', '</table></div>')
$bodyHtml = [regex]::Replace(
    $bodyHtml,
    '<p><img src="(?<src>[^"]+)" alt="(?<alt>[^"]*)" /></p>',
    '<figure><a href="${src}" target="_blank" rel="noopener"><img loading="lazy" src="${src}" alt="${alt}" /></a><figcaption>${alt}</figcaption></figure>'
)

$template = @'
<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{{DESCRIPTION}}">
  <title>{{TITLE}}</title>
  <style>
    :root {
      color-scheme: light;
      --ink: #17211b;
      --muted: #667269;
      --paper: #f5f2e9;
      --card: #fffdf7;
      --line: #d9d4c7;
      --green: #145c43;
      --green-soft: #e7f1ea;
      --red: #a23a2b;
      --code: #17231d;
      --shadow: 0 18px 60px rgba(43, 50, 43, .10);
    }
    * { box-sizing: border-box; }
    html { scroll-behavior: smooth; }
    body {
      margin: 0;
      color: var(--ink);
      background:
        radial-gradient(circle at 8% 2%, rgba(20, 92, 67, .09), transparent 28rem),
        radial-gradient(circle at 92% 7%, rgba(162, 58, 43, .08), transparent 25rem),
        var(--paper);
      font-family: "Noto Serif SC", "Source Han Serif SC", "Songti SC", Georgia, serif;
      font-size: 18px;
      line-height: 1.86;
      text-rendering: optimizeLegibility;
    }
    a { color: var(--green); text-underline-offset: 3px; }
    .hero { padding: 72px 24px 54px; border-bottom: 1px solid var(--line); }
    .hero-inner, main { width: min(960px, calc(100% - 40px)); margin: 0 auto; }
    .eyebrow {
      margin-bottom: 14px;
      color: var(--red);
      font: 700 13px/1.4 "Segoe UI", "Microsoft YaHei", sans-serif;
      letter-spacing: .14em;
      text-transform: uppercase;
    }
    h1 {
      max-width: 880px;
      margin: 0;
      font-size: clamp(38px, 6.3vw, 68px);
      line-height: 1.12;
      letter-spacing: -.035em;
    }
    .dek { max-width: 800px; margin: 24px 0 0; color: #465149; font-size: 20px; line-height: 1.72; }
    .stats { display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 12px; margin-top: 34px; }
    .stat { padding: 17px 18px; border: 1px solid var(--line); border-radius: 12px; background: rgba(255, 253, 247, .72); }
    .stat strong { display: block; font: 800 25px/1.25 "Segoe UI", "Microsoft YaHei", sans-serif; }
    .stat span { color: var(--muted); font: 13px/1.5 "Segoe UI", "Microsoft YaHei", sans-serif; }
    main {
      margin-top: 42px;
      margin-bottom: 84px;
      padding: 42px clamp(20px, 5vw, 68px) 68px;
      border: 1px solid var(--line);
      border-radius: 18px;
      background: var(--card);
      box-shadow: var(--shadow);
    }
    main > p:first-child::first-letter {
      float: left;
      margin: .08em .12em 0 0;
      color: var(--green);
      font-size: 4.2em;
      font-weight: 800;
      line-height: .82;
    }
    h2 {
      margin: 2.6em 0 .85em;
      padding-top: .25em;
      color: #122b20;
      font-size: clamp(27px, 4vw, 38px);
      line-height: 1.3;
      letter-spacing: -.02em;
    }
    h2::before { content: ""; display: block; width: 42px; height: 4px; margin-bottom: 14px; background: var(--red); }
    h3 { margin: 2.25em 0 .75em; color: #173f2e; font-size: clamp(22px, 3vw, 29px); line-height: 1.4; }
    p { margin: 1.05em 0; }
    strong { color: #102b20; }
    blockquote {
      margin: 2em 0;
      padding: 20px 24px;
      border-left: 5px solid var(--green);
      background: var(--green-soft);
      font-size: 1.12em;
    }
    blockquote p { margin: 0; }
    pre {
      overflow-x: auto;
      margin: 1.7em 0;
      padding: 20px 22px;
      border-radius: 12px;
      color: #eef8f1;
      background: var(--code);
      font: 14px/1.7 "Cascadia Code", Consolas, monospace;
    }
    code {
      padding: .12em .34em;
      border-radius: 4px;
      color: #8b2f24;
      background: #f0e9dc;
      font-family: "Cascadia Code", Consolas, monospace;
      font-size: .88em;
    }
    pre code { padding: 0; color: inherit; background: transparent; }
    ul, ol { padding-left: 1.35em; }
    li { margin: .45em 0; }
    .table-wrap { overflow-x: auto; margin: 1.8em -12px; padding: 0 12px 8px; }
    table {
      width: 100%;
      min-width: 700px;
      border-spacing: 0;
      border-collapse: separate;
      border: 1px solid var(--line);
      border-radius: 10px;
      background: #fff;
      font-family: "Segoe UI", "Microsoft YaHei", sans-serif;
      font-size: 14px;
      line-height: 1.55;
    }
    th, td { padding: 11px 12px; border-right: 1px solid var(--line); border-bottom: 1px solid var(--line); text-align: left; vertical-align: top; }
    th:last-child, td:last-child { border-right: 0; }
    tr:last-child td { border-bottom: 0; }
    th { position: sticky; top: 0; color: #f7faf8; background: var(--green); font-weight: 700; white-space: nowrap; }
    tbody tr:nth-child(even) { background: #f8f6ef; }
    figure { margin: 2.3em calc(50% - 47vw); text-align: center; }
    figure a { display: inline-block; max-width: min(1600px, 94vw); }
    figure img {
      display: block;
      width: auto;
      max-width: 100%;
      max-height: 84vh;
      margin: 0 auto;
      border: 1px solid var(--line);
      border-radius: 12px;
      background: #fff;
      box-shadow: 0 10px 35px rgba(34, 44, 37, .11);
    }
    figcaption { max-width: 900px; margin: 10px auto 0; color: var(--muted); font: 13px/1.55 "Segoe UI", "Microsoft YaHei", sans-serif; }
    @media (max-width: 720px) {
      body { font-size: 16px; }
      .hero { padding-top: 48px; }
      .stats { grid-template-columns: 1fr; }
      main { width: calc(100% - 20px); margin-top: 18px; padding: 28px 18px 50px; border-radius: 12px; }
      figure { margin-left: -8px; margin-right: -8px; }
      .table-wrap { margin-left: -18px; margin-right: -18px; }
    }
    @media print {
      body { background: #fff; }
      .hero { padding-top: 24px; }
      main { width: 100%; margin: 0; border: 0; box-shadow: none; }
      figure { margin-left: 0; margin-right: 0; break-inside: avoid; }
    }
  </style>
</head>
<body>
  <header class="hero">
    <div class="hero-inner">
      <div class="eyebrow">Harness Evolution · SDD · 2026</div>
      <h1>{{TITLE}}</h1>
      <p class="dek">{{DESCRIPTION}}</p>
      <div class="stats" aria-label="核心实验数字">
        <div class="stat"><strong>8 个真实任务</strong><span>每个任务 3 次 Lean 运行、2 次独立盲评</span></div>
        <div class="stat"><strong>92.19 分</strong><span>Lean 的八任务等权盲评分</span></div>
        <div class="stat"><strong>Token −64.9%</strong><span>Lean 相对早期 Standard 的描述性变化</span></div>
      </div>
    </div>
  </header>
  <main>
{{BODY}}
  </main>
</body>
</html>
'@

$html = $template.Replace('{{TITLE}}', [System.Net.WebUtility]::HtmlEncode($title))
$html = $html.Replace('{{DESCRIPTION}}', [System.Net.WebUtility]::HtmlEncode($description))
$html = $html.Replace('{{BODY}}', $bodyHtml)
[System.IO.File]::WriteAllText($outputPath, $html, [System.Text.UTF8Encoding]::new($false))
Write-Output $outputPath
