param(
  [Parameter(Mandatory = $true)]
  [string]$Slug,

  [Parameter(Mandatory = $true)]
  [string]$ArticlePath
)

$ErrorActionPreference = "Stop"

$root = (Resolve-Path ".").Path
$promptPath = Join-Path $root "tools/graph-prompt.txt"
$schemaPath = Join-Path $root "tools/graph-schema.json"
$outDir = Join-Path $root "data/graph/articles"
$outPath = Join-Path $outDir "$Slug.json"

New-Item -ItemType Directory -Force -Path $outDir | Out-Null

$prompt = Get-Content $promptPath -Raw
$article = Get-Content $ArticlePath -Raw
$input = "$prompt`n`n$article"

$tmp = New-TemporaryFile
try {
  Set-Content -LiteralPath $tmp -Value $input -Encoding UTF8
  Get-Content -LiteralPath $tmp -Raw | codex exec --cd $root --output-schema $schemaPath --output-last-message $outPath -
}
finally {
  Remove-Item -LiteralPath $tmp -Force -ErrorAction SilentlyContinue
}
