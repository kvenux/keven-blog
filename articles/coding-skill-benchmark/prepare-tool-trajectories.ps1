Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$visualizer = 'C:\Users\kvenu\playground\trajtory-visualizer'
$experiment = 'C:\Users\kvenu\playground\sdd-exp'
$python = Join-Path $visualizer '.venv\Scripts\python.exe'
$cli = Join-Path $visualizer 'cli.py'
$config = Join-Path $visualizer 'config.yaml'
$scratch = Join-Path $experiment '.scratch\article-trajectory-tool'
$assets = Join-Path $PSScriptRoot 'assets'

New-Item -ItemType Directory -Force -Path $scratch | Out-Null

$cases = [ordered]@{
    'eslint-terse' = 'campaigns\eslint-error-class-names-6arm-v1\runs\a-r3\raw-sessions\candidate'
    'eslint-detailed' = 'campaigns\eslint-error-class-names-6arm-v1\runs\b-r3\raw-sessions\candidate'
    'eslint-grill' = 'campaigns\eslint-grill-me-v1\runs\eg-r3\raw-sessions\candidate'
    'bat-bare' = 'campaigns\bat-sanitize-5arm-v1\runs\b-r2\raw-sessions\candidate'
    'bat-pony' = 'campaigns\bat-sanitize-5arm-v1\runs\p-r1\raw-sessions\candidate'
    'prom-bare' = 'campaigns\prometheus-utf8-negotiation-5arm-v1\runs\b-r3\raw-sessions\candidate'
    'prom-pony' = 'campaigns\prometheus-utf8-negotiation-5arm-v1\runs\p-r1\raw-sessions\candidate'
}

foreach ($entry in $cases.GetEnumerator()) {
    $treePath = Join-Path $scratch "$($entry.Key)-tree.json"
    $rawPath = Join-Path $experiment $entry.Value
    & $python $cli parse-tree --config $config --session-dir $rawPath --output $treePath
    if ($LASTEXITCODE -ne 0) { throw "parse-tree failed: $($entry.Key)" }

    $tree = Get-Content -Raw -LiteralPath $treePath | ConvertFrom-Json
    $root = $tree.sessions | Where-Object { $null -eq $_.parent_thread_id } | Select-Object -First 1
    if ($null -eq $root -or $root.steps.Count -eq 0) { throw "No root steps: $($entry.Key)" }
    $flatPath = Join-Path $scratch "$($entry.Key)-flat.json"
    $json = $root.steps | ConvertTo-Json -Depth 20
    [System.IO.File]::WriteAllText($flatPath, $json, [System.Text.UTF8Encoding]::new($false))
}

$eslintGrillOutput = Join-Path $assets 'eslint-grill-vs-terse-bare-tool.png'
& $python $cli plot-tree --config $config --tree (Join-Path $scratch 'eslint-grill-tree.json') `
    --root-label 'GRILL ME' --annotations (Join-Path $assets 'eslint-grill-annotations.json') `
    --compare-trace (Join-Path $scratch 'eslint-terse-flat.json') --compare-label 'TERSE BARE' `
    --show-returns --output $eslintGrillOutput
if ($LASTEXITCODE -ne 0) { throw 'ESLint Grill Me tree plot failed' }

$batOutput = Join-Path $assets 'bat-ponytail-vs-bare-tool.png'
& $python $cli plot-tree --config $config --tree (Join-Path $scratch 'bat-pony-tree.json') `
    --root-label 'PONYTAIL' --annotations (Join-Path $assets 'bat-ponytail-annotations.json') `
    --compare-trace (Join-Path $scratch 'bat-bare-flat.json') --compare-label 'BARE' `
    --show-returns --output $batOutput
if ($LASTEXITCODE -ne 0) { throw 'bat Ponytail tree plot failed' }

$promOutput = Join-Path $assets 'prometheus-ponytail-vs-bare-tool.png'
& $python $cli plot-tree --config $config --tree (Join-Path $scratch 'prom-pony-tree.json') `
    --root-label 'PONYTAIL' --annotations (Join-Path $assets 'prometheus-ponytail-annotations.json') `
    --compare-trace (Join-Path $scratch 'prom-bare-flat.json') --compare-label 'BARE' `
    --show-returns --output $promOutput
if ($LASTEXITCODE -ne 0) { throw 'Prometheus Ponytail tree plot failed' }

$superTree = Join-Path $scratch 'eslint-super-tree.json'
$superAnnotations = Join-Path $assets 'eslint-super-annotations.json'
$superRaw = Join-Path $experiment 'campaigns\eslint-error-class-names-6arm-v1\runs\f-r1\raw-sessions\candidate'
& $python $cli parse-tree --config $config --session-dir $superRaw --output $superTree
if ($LASTEXITCODE -ne 0) { throw 'Superpowers parse-tree failed' }
$superOutput = Join-Path $assets 'eslint-superpowers-tree-tool.png'
& $python $cli plot-tree --config $config --tree $superTree --annotations $superAnnotations `
    --root-label 'SUPERPOWERS' `
    --compare-trace (Join-Path $scratch 'eslint-detailed-flat.json') --compare-label 'DETAILED BARE' `
    --show-returns --output $superOutput
if ($LASTEXITCODE -ne 0) { throw 'Superpowers tree plot failed' }

Get-Item -LiteralPath $eslintGrillOutput, $superOutput, $batOutput, $promOutput | Select-Object Name,Length,LastWriteTime
