param(
    [Parameter(Mandatory = $false)]
    [string]$ConfigPath = ".\training\soup\configs\jarvis-ru-3b-sft.yaml",
    [Parameter(Mandatory = $false)]
    [string]$SoupVenv = "c:\Users\user\Desktop\codex\soup_env",
    [switch]$ExportGguf,
    [string]$GgufQuant = "q4_k_m"
)

$ErrorActionPreference = "Stop"
$SoupExe = Join-Path $SoupVenv "Scripts\soup.exe"
if (-not (Test-Path $SoupExe)) {
    throw "Soup CLI не найден в $SoupExe. Сначала создайте окружение soup_env."
}

Write-Host "[1/3] Проверка конфигурации Soup doctor..."
& $SoupExe doctor --config $ConfigPath
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Host "[2/3] Запуск обучения Soup train..."
& $SoupExe train --config $ConfigPath --yes
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

if ($ExportGguf) {
    $yamlLines = Get-Content $ConfigPath
    $outLine = ($yamlLines | Where-Object { $_ -match "^output:\s*(.+)$" } | Select-Object -First 1)
    if ($outLine -match "^output:\s*(.+)$") {
        $adapterDir = $Matches[1].Trim().Trim('"').Trim("'")
        $mergedDir = "${adapterDir}_merged"
        Write-Host "[3/3] Слияние адаптера и экспорт GGUF ($GgufQuant)..."
        & $SoupExe merge --adapter $adapterDir --output $mergedDir
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
        & $SoupExe export --model $mergedDir --format gguf --quant $GgufQuant
        if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
    }
}
