param(
    [string]$Model = "qwen3.5:4b",
    [string]$OllamaUrl = "http://127.0.0.1:11434",
    [string[]]$Channel = @(),
    [int]$MaxTasks = 1,
    [switch]$Health,
    [switch]$DryRun,
    [switch]$Once
)

$ErrorActionPreference = "Stop"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..\..")).Path
$WorkerPy = Join-Path $PSScriptRoot "local_factory_worker.py"

$Py = if (Test-Path "c:\Users\user\Desktop\codex\soup_env\Scripts\python.exe") {
    "c:\Users\user\Desktop\codex\soup_env\Scripts\python.exe"
} else {
    "python"
}

$env:PYTHONIOENCODING = "utf-8"
$cmdArgs = @($WorkerPy, "--repo", $RepoRoot, "--ollama-url", $OllamaUrl, "--model", $Model, "--max-tasks", "$MaxTasks")
foreach ($ch in $Channel) { $cmdArgs += @("--channel", $ch) }
if ($Health) { $cmdArgs += "--health" }
elseif ($DryRun) { $cmdArgs += "--dry-run" }
elseif ($Once) { $cmdArgs += "--once" }
else { $cmdArgs += "--dry-run" }

& $Py @cmdArgs
exit $LASTEXITCODE
