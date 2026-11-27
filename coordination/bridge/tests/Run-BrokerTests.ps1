$ErrorActionPreference = "Stop"
Write-Host "=== Запуск тестов Message Broker v2.4 ===" -ForegroundColor Cyan

$broker = "coordination/bridge/candidates/broker_v2.4-proposed-NOT-RELEASE.ps1"
if (-not (Test-Path $broker)) { throw "Broker candidate not found: $broker" }
$brokerFullPath = (Resolve-Path $broker).Path
$selfFullPath = (Resolve-Path $MyInvocation.MyCommand.Path).Path

function New-BridgeTestSandbox {
    $dir = Join-Path $env:TEMP ("BrokerTestDir_" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $dir | Out-Null
    foreach ($sub in @("outbox_jarvis", "outbox_gemini", "processing", "processed", "errors", "inbox_jarvis", "inbox_gemini")) {
        New-Item -ItemType Directory -Path (Join-Path $dir $sub) | Out-Null
    }
    return $dir
}

# 1. Синтаксис обоих скриптов под Windows PowerShell 5.1
Write-Host "[1/7] Проверка синтаксиса брокера и тестового набора (PS 5.1)..."
foreach ($fileToParse in @($brokerFullPath, $selfFullPath)) {
    $tokens = $null
    $parseErrors = $null
    [System.Management.Automation.Language.Parser]::ParseFile($fileToParse, [ref]$tokens, [ref]$parseErrors) | Out-Null
    if ($parseErrors.Count -gt 0) {
        foreach ($e in $parseErrors) {
            Write-Host ("PARSE_ERROR file={0} line={1} col={2} extent=<{3}> message={4}" -f $fileToParse, $e.Extent.StartLineNumber, $e.Extent.StartColumnNumber, $e.Extent.Text, $e.Message)
        }
        throw "Syntax parse failed for $fileToParse."
    }
}
Write-Host "Syntax check: PASS" -ForegroundColor Green

# 2. Восстановление Ledger при отсутствии ledger.json
Write-Host "[2/7] Тест восстановления Ledger при отсутствии ledger.json..."
$testDir = New-BridgeTestSandbox
try {
    . $brokerFullPath -BasePath $testDir -LibraryOnly
    @{ "tsk_123" = @{ Status = "WAITING_ACK"; File = "tsk_123.md"; Attempts = 1 } } | ConvertTo-Json -Depth 5 | Out-File -FilePath $ledgerBakPath -Encoding UTF8 -Force
    $loaded = Load-Ledger
    if (-not $loaded.ContainsKey("tsk_123") -or $loaded["tsk_123"].Status -ne "WAITING_ACK") {
        throw "Missing ledger did not recover from ledger.bak.json."
    }
    Write-Host "Missing ledger recovery: PASS" -ForegroundColor Green
} finally {
    Remove-Item $testDir -Recurse -Force
}

# 3. Восстановление Ledger при повреждённом ledger.json
Write-Host "[3/7] Тест fallback при повреждённом ledger.json..."
$testDir = New-BridgeTestSandbox
try {
    . $brokerFullPath -BasePath $testDir -LibraryOnly
    "{ broken json ::: not valid" | Out-File -FilePath $ledgerPath -Encoding UTF8 -Force
    @{ "tsk_corrupt_ok" = @{ Status = "QUEUED"; File = "tsk_corrupt_ok.md"; Attempts = 0 } } | ConvertTo-Json -Depth 5 | Out-File -FilePath $ledgerBakPath -Encoding UTF8 -Force
    $loaded = Load-Ledger
    if (-not $loaded.ContainsKey("tsk_corrupt_ok") -or $loaded["tsk_corrupt_ok"].Status -ne "QUEUED") {
        throw "Corrupted ledger.json did not fall back to ledger.bak.json."
    }
    Write-Host "Corrupted ledger fallback: PASS" -ForegroundColor Green
} finally {
    Remove-Item $testDir -Recurse -Force
}

# 4. Живой тест защиты от дубликата task_id
Write-Host "[4/7] Живой тест защиты от дубликата task_id..."
$testDir = New-BridgeTestSandbox
try {
    . $brokerFullPath -BasePath $testDir -LibraryOnly
    $initialLedger = @{
        "tsk_dup" = @{
            Status = "WAITING_ACK"
            File = "orig_dup.md"
            Attempts = 2
            Source = "jarvis"
            Target = "gemini"
        }
    }
    Save-Ledger -Ledger $initialLedger

    $dupContent = @"
---
task_id: tsk_dup
from: jarvis
to: gemini
---
Duplicate payload that must NOT overwrite existing state.
"@
    $dupContent | Out-File -FilePath (Join-Path $testDir "outbox_jarvis\second_dup.md") -Encoding UTF8 -Force

    Invoke-BrokerStep
    $after = Load-Ledger
    if ($after["tsk_dup"].Status -ne "WAITING_ACK" -or $after["tsk_dup"].File -ne "orig_dup.md" -or $after["tsk_dup"].Attempts -ne 2) {
        throw "Duplicate task_id overwrote existing ledger state!"
    }
    if (-not (Test-Path (Join-Path $testDir "errors\dup_second_dup.md"))) {
        throw "Duplicate file was not quarantined to errors\dup_second_dup.md."
    }
    Write-Host "Duplicate task_id live guard: PASS" -ForegroundColor Green
} finally {
    Remove-Item $testDir -Recurse -Force
}

# 5. Живой тест отключенного транспорта (TRANSPORT_NOT_CONFIGURED)
Write-Host "[5/7] Живой тест заморозки при отключенном транспорте..."
$testDir = New-BridgeTestSandbox
try {
    . $brokerFullPath -BasePath $testDir -LibraryOnly
    $taskContent = @"
---
task_id: tsk_notransport
from: jarvis
to: gemini
---
Test task without configured endpoint.
"@
    $taskContent | Out-File -FilePath (Join-Path $testDir "outbox_jarvis\tsk_notransport.md") -Encoding UTF8 -Force

    Invoke-BrokerStep
    $after = Load-Ledger
    if (-not $after.ContainsKey("tsk_notransport") -or $after["tsk_notransport"].Status -ne "TRANSPORT_NOT_CONFIGURED") {
        throw "Expected TRANSPORT_NOT_CONFIGURED status for disabled transport."
    }
    Write-Host "Disabled transport freeze: PASS" -ForegroundColor Green
} finally {
    Remove-Item $testDir -Recurse -Force
}

# 6. Живой тест ACK-цикла (перенос исходной задачи в processed и ACK в inbox_jarvis)
Write-Host "[6/7] Живой тест полного ACK-цикла..."
$testDir = New-BridgeTestSandbox
try {
    . $brokerFullPath -BasePath $testDir -LibraryOnly
    "original content" | Out-File -FilePath (Join-Path $testDir "processing\orig_task.md") -Encoding UTF8 -Force
    Save-Ledger -Ledger @{
        "tsk_orig" = @{
            Status = "WAITING_ACK"
            File = "orig_task.md"
            Attempts = 1
            Source = "jarvis"
            Target = "gemini"
        }
    }

    $ackContent = @"
---
task_id: tsk_ack_1
ack_task_id: tsk_orig
from: gemini
to: jarvis
---
Done.
"@
    $ackContent | Out-File -FilePath (Join-Path $testDir "outbox_gemini\ack_1.md") -Encoding UTF8 -Force

    Invoke-BrokerStep
    $after = Load-Ledger
    if ($after["tsk_orig"].Status -ne "COMPLETED" -or $after["tsk_ack_1"].Status -ne "COMPLETED") {
        throw "ACK did not mark both original task and ACK task as COMPLETED."
    }
    if (-not (Test-Path (Join-Path $testDir "processed\orig_task.md"))) {
        throw "Original task was not moved to processed/."
    }
    if (-not (Test-Path (Join-Path $testDir "inbox_jarvis\ack_1.md"))) {
        throw "ACK file was not moved to inbox_jarvis/."
    }
    Write-Host "Live ACK cycle: PASS" -ForegroundColor Green
} finally {
    Remove-Item $testDir -Recurse -Force
}

# 7. Живой тест конкуренции OS Mutex (второй экземпляр обязан завершиться с кодом 1)
Write-Host "[7/7] Живой тест блокировки двойного запуска (Mutex contention)..."
$testDir = New-BridgeTestSandbox
$testMutexName = "Local\JarvisBrokerTestMutex_" + [guid]::NewGuid().ToString("N")
$created = $false
$heldMutex = New-Object System.Threading.Mutex($true, $testMutexName, [ref]$created)
try {
    if (-not $created) { throw "Failed to acquire test mutex." }
    $proc = Start-Process -FilePath "powershell.exe" -ArgumentList @(
        "-NoProfile", "-ExecutionPolicy", "Bypass",
        "-File", "`"$brokerFullPath`"",
        "-BasePath", "`"$testDir`"",
        "-MutexName", "`"$testMutexName`"",
        "-RunOnce"
    ) -Wait -PassThru -NoNewWindow
    if ($proc.ExitCode -ne 1) {
        throw "Expected second broker instance to exit with code 1, got $($proc.ExitCode)."
    }
    Write-Host "Mutex contention guard: PASS" -ForegroundColor Green
} finally {
    $heldMutex.ReleaseMutex()
    $heldMutex.Dispose()
    Remove-Item $testDir -Recurse -Force
}

Write-Host "=== Все 7 тестов Message Broker v2.4 пройдены ===" -ForegroundColor Cyan
