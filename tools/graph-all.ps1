param(
  [switch]$Force,
  [switch]$Parallel
)

$ErrorActionPreference = "Stop"

$root = (Resolve-Path ".").Path
$articleRoot = Join-Path $root "content/posts"
$graphRoot = Join-Path $root "data/graph/articles"
$extract = Join-Path $root "tools/extract-graph.ps1"

New-Item -ItemType Directory -Force -Path $graphRoot | Out-Null

$posts = Get-ChildItem -LiteralPath $articleRoot -Directory |
  Where-Object { Test-Path (Join-Path $_.FullName "index.md") } |
  ForEach-Object {
    [PSCustomObject]@{
      Slug = $_.Name
      ArticlePath = Join-Path $_.FullName "index.md"
      GraphPath = Join-Path $graphRoot "$($_.Name).json"
    }
  } |
  Where-Object { $Force -or -not (Test-Path $_.GraphPath) }

if (-not $posts) {
  Write-Host "No graph extraction needed."
  node tools/build-graph.mjs
  exit 0
}

if ($Parallel) {
  $jobs = foreach ($post in $posts) {
    Start-Job -ArgumentList $root, $extract, $post.Slug, $post.ArticlePath -ScriptBlock {
      param($Root, $Extract, $Slug, $ArticlePath)
      Set-Location $Root
      powershell -ExecutionPolicy Bypass -File $Extract -Slug $Slug -ArticlePath $ArticlePath
    }
  }

  $jobs | Wait-Job | Receive-Job
  $jobs | Remove-Job
} else {
  foreach ($post in $posts) {
    powershell -ExecutionPolicy Bypass -File $extract -Slug $post.Slug -ArticlePath $post.ArticlePath
  }
}

node tools/build-graph.mjs
