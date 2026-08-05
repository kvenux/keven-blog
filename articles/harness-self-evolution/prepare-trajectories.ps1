Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$articleRoot = $PSScriptRoot
$playgroundRoot = (Resolve-Path (Join-Path $articleRoot '..\..\..')).Path
$experimentRoot = Join-Path $playgroundRoot 'sdd-exp'
$visualizerRoot = Join-Path $playgroundRoot 'trajtory-visualizer'
$python = Join-Path $visualizerRoot '.venv\Scripts\python.exe'
$cli = Join-Path $visualizerRoot 'cli.py'
$config = Join-Path $visualizerRoot 'config.yaml'
$scratch = Join-Path $experimentRoot '.scratch\harness-self-evolution-trajectories'
$dataRoot = Join-Path $articleRoot 'assets\data'
$outputPath = Join-Path $articleRoot 'assets\pytest-addini-standard-light-lean-trajectory-visualizer.png'
$standardBareOutputPath = Join-Path $articleRoot 'assets\pytest-addini-standard-vs-bare-trajectory-visualizer.png'

if (-not (Test-Path -LiteralPath $python)) {
    throw "Trajectory Visualizer Python not found: $python"
}

New-Item -ItemType Directory -Force -Path $scratch, $dataRoot | Out-Null

function Merge-CandidateTurns {
    param(
        [Parameter(Mandatory)]
        [string]$RunRoot,
        [Parameter(Mandatory)]
        [string[]]$Actors,
        [Parameter(Mandatory)]
        [string]$OutputPath
    )

    $processPath = Join-Path $RunRoot 'processes.jsonl'
    $processes = Get-Content -LiteralPath $processPath |
        Where-Object { -not [string]::IsNullOrWhiteSpace($_) } |
        ForEach-Object { $_ | ConvertFrom-Json }
    $actorCounts = @{}
    $chunks = [System.Collections.Generic.List[string]]::new()

    foreach ($process in $processes) {
        $actor = [string]$process.actor
        if ($Actors -notcontains $actor) {
            continue
        }
        if (-not $actorCounts.ContainsKey($actor)) {
            $actorCounts[$actor] = 0
        }
        $actorCounts[$actor]++
        $turnName = '{0}-turn-{1:D2}.jsonl' -f $actor, $actorCounts[$actor]
        $turnPath = Join-Path $RunRoot $turnName
        if (-not (Test-Path -LiteralPath $turnPath)) {
            throw "Missing turn log referenced by process order: $turnPath"
        }
        $chunks.Add([System.IO.File]::ReadAllText($turnPath))
    }

    if ($chunks.Count -eq 0) {
        throw "No candidate turns found under $RunRoot"
    }
    $merged = [string]::Join([Environment]::NewLine, $chunks)
    [System.IO.File]::WriteAllText($OutputPath, $merged, [System.Text.UTF8Encoding]::new($false))
}

$runs = [ordered]@{
    'standard' = @{
        Root = Join-Path $experimentRoot 'campaigns\pytest-addini-type-expressions-matrixspec-profiled-v1\runs\pa-s1-r1'
        Actors = @('candidate-main', 'candidate-validation')
    }
    'light' = @{
        Root = Join-Path $experimentRoot 'campaigns\pytest-addini-type-expressions-matrixspec-profiled-no-baseline-v1\runs\pan-l0-r3'
        Actors = @('candidate-main')
    }
    'lean' = @{
        Root = Join-Path $experimentRoot 'campaigns\pytest-addini-type-expressions-matrixspec-lean-v1\runs\paln-r3'
        Actors = @('candidate-spec', 'candidate-main')
    }
}

foreach ($entry in $runs.GetEnumerator()) {
    $mergedPath = Join-Path $scratch "$($entry.Key)-merged.jsonl"
    $parsedPath = Join-Path $dataRoot "$($entry.Key)-pytest-addini-trajectory.json"
    Merge-CandidateTurns -RunRoot $entry.Value.Root -Actors $entry.Value.Actors -OutputPath $mergedPath
    & $python $cli parse --config $config --input $mergedPath --format codex --output $parsedPath
    if ($LASTEXITCODE -ne 0) {
        throw "Trajectory parsing failed for $($entry.Key)"
    }
}

$bareRunRoot = Join-Path $experimentRoot 'campaigns\pytest-addini-type-expressions-bare-v1\runs\b-r1'
$bareMergedPath = Join-Path $scratch 'bare-merged.jsonl'
$bareParsedPath = Join-Path $dataRoot 'bare-pytest-addini-trajectory.json'
Merge-CandidateTurns -RunRoot $bareRunRoot -Actors @('candidate') -OutputPath $bareMergedPath
& $python $cli parse --config $config --input $bareMergedPath --format codex --output $bareParsedPath
if ($LASTEXITCODE -ne 0) {
    throw 'Bare trajectory parsing failed.'
}

$standardSteps = Get-Content -Raw -LiteralPath (Join-Path $dataRoot 'standard-pytest-addini-trajectory.json') | ConvertFrom-Json
$lightSteps = Get-Content -Raw -LiteralPath (Join-Path $dataRoot 'light-pytest-addini-trajectory.json') | ConvertFrom-Json
$leanSteps = Get-Content -Raw -LiteralPath (Join-Path $dataRoot 'lean-pytest-addini-trajectory.json') | ConvertFrom-Json
$tree = [ordered]@{
    schema_version = 1
    root_thread_id = 'standard'
    sessions = @(
        [ordered]@{
            thread_id = 'standard'; parent_thread_id = 'comparison-root'; lane = 0; lane_id = 'STANDARD'
            agent_path = '/PROJECT FULL SPEC'; nickname = 'STANDARD'; steps = @($standardSteps)
        },
        [ordered]@{
            thread_id = 'light'; parent_thread_id = 'comparison-root'; lane = 1; lane_id = 'LIGHT'
            agent_path = '/NO PROJECT FULL SPEC'; nickname = 'LIGHT'; steps = @($lightSteps)
        },
        [ordered]@{
            thread_id = 'lean'; parent_thread_id = 'comparison-root'; lane = 2; lane_id = 'LEAN'
            agent_path = '/DELTA>IMPLEMENT+VERIFY'; nickname = 'LEAN'; steps = @($leanSteps)
        }
    )
    edges = @()
    returns = @()
}
$treePath = Join-Path $dataRoot 'pytest-addini-standard-light-lean-tree.json'
$treeJson = $tree | ConvertTo-Json -Depth 100
[System.IO.File]::WriteAllText($treePath, $treeJson, [System.Text.UTF8Encoding]::new($false))

$trajectoryRenderer = Join-Path $articleRoot 'render-trajectory.py'
& $python $trajectoryRenderer --visualizer-root $visualizerRoot --config $config --tree $treePath --output $outputPath
if ($LASTEXITCODE -ne 0) {
    throw 'Compact trajectory tree rendering failed.'
}

$bareSteps = Get-Content -Raw -LiteralPath $bareParsedPath | ConvertFrom-Json
$standardBareTree = [ordered]@{
    schema_version = 1
    root_thread_id = 'standard'
    sessions = @(
        [ordered]@{
            thread_id = 'standard'; parent_thread_id = 'comparison-root'; lane = 0; lane_id = 'STANDARD'
            agent_path = '/NO IMPLEMENTATION'; nickname = 'STANDARD'; steps = @($standardSteps)
        },
        [ordered]@{
            thread_id = 'bare'; parent_thread_id = 'comparison-root'; lane = 1; lane_id = 'BARE'
            agent_path = '/IMPLEMENTED'; nickname = 'BARE'; steps = @($bareSteps)
        }
    )
    edges = @()
    returns = @()
    annotations = @(
        [ordered]@{ thread_id = 'standard'; start_step = 1; end_step = 44; kind = 'plan'; label = 'proposal：五轮提交与退回'; status = 'neutral'; source = 'processes.jsonl + parsed turn counts' },
        [ordered]@{ thread_id = 'standard'; start_step = 45; end_step = 68; kind = 'plan'; label = 'delta-spec：四轮提交与退回'; status = 'neutral'; source = 'processes.jsonl + parsed turn counts' },
        [ordered]@{ thread_id = 'standard'; start_step = 69; end_step = 84; kind = 'plan'; label = 'tasks：首次编排'; status = 'neutral'; source = 'processes.jsonl + parsed turn counts' },
        [ordered]@{ thread_id = 'standard'; start_step = 85; end_step = 110; kind = 'verify'; label = 'validation：三轮检查'; status = 'neutral'; source = 'processes.jsonl + parsed turn counts' },
        [ordered]@{ thread_id = 'standard'; start_step = 111; end_step = 122; kind = 'plan'; label = '退回 tasks 修订'; status = 'neutral'; source = 'processes.jsonl + parsed turn counts' },
        [ordered]@{ thread_id = 'standard'; start_step = 123; end_step = 161; kind = 'verify'; label = 'validation：再次检查'; status = 'neutral'; source = 'processes.jsonl + parsed turn counts' },
        [ordered]@{ thread_id = 'standard'; start_step = 162; end_step = 183; kind = 'plan'; label = '再次退回 tasks'; status = 'neutral'; source = 'processes.jsonl + parsed turn counts' },
        [ordered]@{ thread_id = 'standard'; start_step = 184; end_step = 219; kind = 'verify'; label = 'validation：仍未通过'; status = 'fail'; source = 'processes.jsonl + parsed turn counts' },
        [ordered]@{ thread_id = 'bare'; start_step = 1; end_step = 36; kind = 'implement'; label = '直接探索、实现与验证'; status = 'pass'; source = 'parsed candidate session' }
    )
}
$standardBareTreePath = Join-Path $dataRoot 'pytest-addini-standard-vs-bare-tree.json'
$standardBareTreeJson = $standardBareTree | ConvertTo-Json -Depth 100
[System.IO.File]::WriteAllText($standardBareTreePath, $standardBareTreeJson, [System.Text.UTF8Encoding]::new($false))
& $python $trajectoryRenderer --visualizer-root $visualizerRoot --config $config --tree $standardBareTreePath --output $standardBareOutputPath
if ($LASTEXITCODE -ne 0) {
    throw 'Standard versus Bare trajectory rendering failed.'
}

$metadata = [ordered]@{
    schemaVersion = 1
    selection = 'Median reported token run within each pytest-addini arm'
    visualizer = $visualizerRoot
    note = 'The Standard project-level full-specification baseline is generated before candidate turns and is not shown, so the rendered Standard trace understates total Standard work.'
    runs = [ordered]@{
        standard = [ordered]@{ profile = 'Standard'; baselineCondition = 'project-level full specification available'; runId = 'pa-s1-r1'; status = 'failed'; blindScore = 8.5; reportedTokens = 6610000; workflow = 'Standard with a pre-existing full specification baseline' }
        light = [ordered]@{ profile = 'Light'; baselineCondition = 'no pre-existing project-level full specification'; runId = 'pan-l0-r3'; status = 'completed'; blindScore = 86.5; reportedTokens = 8460000; workflow = 'Light without a pre-existing full specification baseline' }
        lean = [ordered]@{ profile = 'Lean'; baselineCondition = 'confirmed change delta specification'; runId = 'paln-r3'; status = 'completed'; blindScore = 91.5; implementationTokens = 2860000; workflow = 'Confirmed delta-specification followed by a fresh implementation session' }
    }
}
$metadataPath = Join-Path $dataRoot 'trajectory-selection.json'
$metadataJson = $metadata | ConvertTo-Json -Depth 8
[System.IO.File]::WriteAllText($metadataPath, $metadataJson, [System.Text.UTF8Encoding]::new($false))

Get-Item -LiteralPath $outputPath, $standardBareOutputPath, $metadataPath | Select-Object FullName, Length, LastWriteTime
