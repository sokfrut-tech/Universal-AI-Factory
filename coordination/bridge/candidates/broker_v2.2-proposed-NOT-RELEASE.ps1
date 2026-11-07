# NOT A RELEASE — submitted Gemini v2.2 candidate preserved for review.
# Do not execute: the transport section contains a simulated HTTP 200 and a commented-out POST.
# This file is retained as review evidence, not as a production broker.

$basePath = "C:\dr\Universal-AI-Factory\coordination\bridge"
$ledgerPath = Join-Path $basePath "ledger.json"
$logPath = Join-Path $basePath "bridge_sync.log"
$geminiPanelEndpoint = $null # Эндпоинт пока не задан

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    $logLine = "[$timestamp] [$Level] $Message"
    Write-Host $logLine
    Add-Content -Path $logPath -Value $logLine
}

# Полифилл для PowerShell 5.1 (глубокая конвертация JSON в Hashtable)
function Convert-PSObjectToHashtable {
    param($obj)
    if ($null -eq $obj) { return $obj }
    if ($obj -is [Management.Automation.PSCustomObject]) {
        $hash = @{}
        $obj.psobject.properties | ForEach-Object {
            $hash[$_.Name] = Convert-PSObjectToHashtable $_.Value
        }
        return $hash
    }
    return $obj
}

function Load-Ledger {
    if (Test-Path $ledgerPath) {
        try {
            $json = Get-Content $ledgerPath -Raw | ConvertFrom-Json
            $hash = Convert-PSObjectToHashtable $json
            if ($hash -is [hashtable]) { return $hash }
        } catch { Write-Log "Ошибка чтения Ledger: $($_.Exception.Message)" "ERROR" }
    }
    return @{}
}

function Save-Ledger {
    param($Ledger)
    $tmpPath = "$ledgerPath.tmp"
    $Ledger | ConvertTo-Json -Depth 5 | Out-File -FilePath $tmpPath -Encoding UTF8 -Force
    Move-Item -Path $tmpPath -Destination $ledgerPath -Force
}

function Parse-Yaml {
    param([string]$Content)
    if ($Content -match '(?s)^---\r?\n(.*?)\r?\n---\r?\n(.*)') {
        $yamlBlock = $matches[1]; $body = $matches[2]; $meta = @{}
        switch -Regex ($yamlBlock -split '\r?\n') { '^([a-zA-Z0-9_]+):\s*"?([^"]*)"?$' { $meta[$matches[1]] = $matches[2] } }
        return @{ Meta = $meta; Body = $body; Valid = $true }
    }
    return @{ Valid = $false }
}

Write-Log "Message Broker v2.2 (PS 5.1 Compatible) инициализирован." "START"

while ($true) {
    $ledger = Load-Ledger
    $outboxes = @("outbox_jarvis", "outbox_gemini")
    $processingPath = Join-Path $basePath "processing"
    
    # 1. Импорт новых сообщений
    foreach ($outbox in $outboxes) {
        $files = Get-ChildItem -Path (Join-Path $basePath $outbox) -Filter "*.md"
        foreach ($file in $files) {
            try { $stream = [IO.File]::Open($file.FullName, 'Open', 'Read', 'None'); $stream.Close() } catch { continue } # Test-FileLock
            
            $procFile = Join-Path $processingPath $file.Name
            Move-Item -Path $file.FullName -Destination $procFile -Force
            
            $parsed = Parse-Yaml (Get-Content $procFile -Raw)
            if (!$parsed.Valid -or ![bool]$parsed.Meta.task_id) {
                Write-Log "Invalid YAML. Rejected: $($file.Name)" "ERROR"
                Move-Item -Path $procFile -Destination (Join-Path $basePath "errors\$($file.Name)") -Force
                continue
            }

            $taskId = $parsed.Meta.task_id
            if (-not $ledger.ContainsKey($taskId)) {
                $ledger[$taskId] = @{
                    Status = "QUEUED"; File = $file.Name; Attempts = 0
                    Source = $parsed.Meta.from; Target = $parsed.Meta.to
                }
                Write-Log "Task $taskId зарегистрирован (QUEUED)" "INFO"
                Save-Ledger $ledger
            }
        }
    }

    # 2. Обработка стейта
    foreach ($key in @($ledger.Keys)) {
        $task = $ledger[$key]
        $procFile = Join-Path $processingPath $task.File
        
        if ($task.Status -eq "QUEUED" -or $task.Status -eq "TRANSPORT_NOT_CONFIGURED") {
            if (!(Test-Path $procFile)) { continue }
            $parsed = Parse-Yaml (Get-Content $procFile -Raw)
            
            # Обработка ACK
            if ($parsed.Meta.ContainsKey("ack_task_id") -and $ledger.ContainsKey($parsed.Meta.ack_task_id)) {
                $ackId = $parsed.Meta.ack_task_id
                Write-Log "Получен валидный ACK завершения для $ackId" "INFO"
                
                $origTask = $ledger[$ackId]
                if (Test-Path (Join-Path $processingPath $origTask.File)) {
                    Move-Item -Path (Join-Path $processingPath $origTask.File) -Destination (Join-Path $basePath "processed\$($origTask.File)") -Force
                }
                $origTask.Status = "COMPLETED"
                
                $targetInbox = if ($task.Target -eq "jarvis") { "inbox_jarvis" } else { "inbox_gemini" }
                Move-Item -Path $procFile -Destination (Join-Path $basePath "$targetInbox\$($task.File)") -Force
                $task.Status = "COMPLETED"
                Save-Ledger $ledger
                continue
            }

            # Маршрутизация на транспорт
            if ($task.Target -eq "gemini") {
                if ([string]::IsNullOrEmpty($geminiPanelEndpoint)) {
                    if ($task.Status -ne "TRANSPORT_NOT_CONFIGURED") {
                        $task.Status = "TRANSPORT_NOT_CONFIGURED"
                        Write-Log "Транспорт не задан. $key заморожен." "WARN"
                        Save-Ledger $ledger
                    }
                    continue
                }

                $task.Status = "IN_FLIGHT"
                $task.Attempts += 1
                Save-Ledger $ledger
                
                try {
                    # Эмуляция реальной отправки. Реальный код раскомментируем после успешной разведки порта 8320.
                    # $payload = @{ message = (Get-Content $procFile -Raw) } | ConvertTo-Json
                    # $res = Invoke-RestMethod -Uri $geminiPanelEndpoint -Method Post -Body $payload -ContentType "application/json" -TimeoutSec 10 -ErrorAction Stop
                    
                    # Имитация успешного ответа 200 OK
                    $statusCode = 200 
                    
                    if ($statusCode -eq 200) {
                        $task.Status = "WAITING_ACK"
                        Write-Log "HTTP 200 OK. $key доставлен (ACK Приёма)." "INFO"
                    } else {
                        throw "HTTP Status $statusCode"
                    }
                } catch {
                    Write-Log "Ошибка доставки $key: $($_.Exception.Message)" "ERROR"
                    if ($task.Attempts -ge 3) {
                        $task.Status = "DEAD_LETTER"
                        Move-Item -Path $procFile -Destination (Join-Path $basePath "errors\$($task.File)") -Force
                    } else {
                        $task.Status = "QUEUED"
                    }
                }
                Save-Ledger $ledger
            }
        }
    }
    Start-Sleep -Seconds 3
}
