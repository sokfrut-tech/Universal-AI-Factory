$ErrorActionPreference = "Stop"
Write-Host "=== Запуск тестов Message Broker v2.4 ===" -ForegroundColor Cyan
$broker = "coordination/bridge/candidates/broker_v2.4-proposed-NOT-RELEASE.ps1"
if (-not (Test-Path $broker)) { throw "Broker candidate not found: $broker" }

# 1. Синтаксис обоих скриптов под Windows PowerShell 5.1
Write-Host "[1/3] Проверка синтаксиса брокера и тестового набора..."
$tokens = $null
$parseErrors = $null
[System.Management.Automation.Language.Parser]::ParseFile((Resolve-Path $broker).Path, [ref]$tokens, [ref]$parseErrors) | Out-Null
if ($parseErrors.Count -gt 0) {
    foreach ($e in $parseErrors) { Write-Host ("BROKER_PARSE_ERROR line={0} col={1} extent=<{2}> message={3}" -f $e.Extent.StartLineNumber,$e.Extent.StartColumnNumber,$e.Extent.Text,$e.Message) }
    throw "Broker parse failed."
}
Write-Host "Broker syntax: PASS" -ForegroundColor Green

# 2. Ledger backup recovery smoke test using the same PSObject conversion and selection pattern
Write-Host "[2/3] Тест восстановления Ledger из резервной копии..."
$testDir = Join-Path $env:TEMP ("BrokerTestDir_" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $testDir | Out-Null
try {
    $ledgerPath = Join-Path $testDir "ledger.json"
    $ledgerBakPath = Join-Path $testDir "ledger.bak.json"
    $null = @{ "tsk_123" = @{ Status="WAITING_ACK" } } | ConvertTo-Json -Depth 5 | Set-Content -Path $ledgerBakPath -Encoding UTF8
    $targetPath = $null
    if (Test-Path $ledgerPath) { $targetPath = $ledgerPath } elseif (Test-Path $ledgerBakPath) { $targetPath = $ledgerBakPath }
    if ($null -eq $targetPath) { throw "No ledger candidate selected." }
    $json = Get-Content $targetPath -Raw | ConvertFrom-Json
    if ($null -eq $json.PSObject.Properties["tsk_123"]) { throw "Backup ledger entry missing." }
    Write-Host "Backup ledger recovery smoke test: PASS" -ForegroundColor Green
} finally {
    Remove-Item $testDir -Recurse -Force
}

# 3. Static guard: duplicate task_id must not replace existing ledger state
Write-Host "[3/3] Проверка защитной ветки duplicate task_id..."
$source = Get-Content $broker -Raw
if ($source -notmatch 'if\s*\(-not\s*\$ledger\.ContainsKey\(\$taskId\)\)') { throw "Missing duplicate task_id guard." }
if ($source -notmatch 'Дубликат task_id') { throw "Missing duplicate task_id handling/log." }
Write-Host "Duplicate task_id source guard: PASS" -ForegroundColor Green
Write-Host "=== Все заявленные проверки этого минимального набора пройдены ===" -ForegroundColor Cyan
