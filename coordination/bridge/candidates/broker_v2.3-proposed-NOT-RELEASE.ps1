# NOT A RELEASE — submitted v2.3 candidate preserved for review.
# Static review only. Do not execute on a user's machine.
$basePath = "C:\dr\Universal-AI-Factory\coordination\bridge"
$ledgerPath = Join-Path $basePath "ledger.json"
$ledgerBakPath = Join-Path $basePath "ledger.bak.json"
$logPath = Join-Path $basePath "bridge_sync.log"

# Внимание: Транспорт отключен.
# Для активации в будущем: $geminiPanelEndpoint = "http://127.0.0.1:8320/api/chat/send"
$geminiPanelEndpoint = $null 

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    $logLine = "[$timestamp] [$Level] $Message"
    Write-Host $logLine
    Add-Content -Path $logPath -Value $logLine
}

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
    $targetPath = if (Test-Path $ledgerPath) { $ledgerPath } elseif (Test-Path $ledgerBakPath) { Write-Log "Используем резервный Ledger." "WARN"; $ledgerBakPath } else { $null }
    
    if ($targetPath) {
        try {
            $json = Get-Content $targetPath -Raw | ConvertFrom-Json
            $hash = Convert-PSObjectToHashtable $json
            if ($hash -is [hashtable]) { return $hash }
        } catch { Write-Log "Ошибка чтения Ledger: $($_.Exception.Message)" "CRITICAL" }
    }
    return @{}
}

function Save-Ledger {
    param($Ledger)
    $tmpPath = "$ledgerPath.tmp"
    
    # Резервная копия перед перезаписью
    if (Test-Path $ledgerPath) { Copy-Item -Path $ledgerPath -Destination $ledgerBakPath -Force }
    
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

Write-Log "Message Broker v2.3 инициализирован. Транспорт: $(if($geminiPanelEndpoint){'ON'}else{'OFF'})" "START"

while ($true) {
    $ledger = Load-Ledger
    $outboxes = @("outbox_jarvis", "outbox_gemini")
    $processingPath = Join-Path $basePath "processing"
    
    # 1. ИМПОРТ
    foreach ($outbox in $outboxes) {
        $files = Get-ChildItem -Path (Join-Path $basePath $outbox) -Filter "*.md"
        foreach ($file in $files) {
            try { $stream = [IO.File]::Open($file.FullName, 'Open', 'Read', 'None'); $stream.Close() } catch { continue }
            
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
            } else {
                # Если task_id уже существует, просто перезаписываем файл в processing (возможно повторная отправка от агента)
                Write-Log "Обнаружен дубликат task_id: $taskId. Переписываем файл." "WARN"
            }
        }
    }

    # 2. ОБРАБОТКА ACK И ТРАНСПОРТА
    foreach ($key in @($ledger.Keys)) {
        $task = $ledger[$key]
        $procFile = Join-Path $processingPath $task.File
        
        if ($task.Status -eq "QUEUED" -or $task.Status -eq "TRANSPORT_NOT_CONFIGURED") {
            if (!(Test-Path $procFile)) { continue }
            $parsed = Parse-Yaml (Get-Content $procFile -Raw)
            
            if ($parsed.Meta.ContainsKey("ack_task_id")) {
                $ackId = $parsed.Meta.ack_task_id
                if ($ledger.ContainsKey($ackId)) {
                    Write-Log "Получен валидный ACK завершения для $ackId" "INFO"
                    
                    $origTask = $ledger[$ackId]
                    if (Test-Path (Join-Path $processingPath $origTask.File)) {
                        Move-Item -Path (Join-Path $processingPath $origTask.File) -Destination (Join-Path $basePath "processed\$($origTask.File)") -Force
                    }
                    $origTask.Status = "COMPLETED"
                    
                    # Доставляем ответное сообщение адресату
                    $targetInbox = if ($task.Target -eq "jarvis") { "inbox_jarvis" } else { "inbox_gemini" }
                    Move-Item -Path $procFile -Destination (Join-Path $basePath "$targetInbox\$($task.File)") -Force
                    $task.Status = "COMPLETED"
                    Save-Ledger $ledger
                    continue
                } else {
                    Write-Log "Получен ACK для неизвестной задачи $ackId. Игнорируем закрытие." "WARN"
                }
            }

            if ($task.Target -eq "gemini") {
                if ([string]::IsNullOrEmpty($geminiPanelEndpoint)) {
                    if ($task.Status -ne "TRANSPORT_NOT_CONFIGURED") {
                        $task.Status = "TRANSPORT_NOT_CONFIGURED"
                        Write-Log "Транспорт не задан. Task $key заморожен (TRANSPORT_NOT_CONFIGURED)." "WARN"
                        Save-Ledger $ledger
                    }
                    continue
                }

                $task.Status = "IN_FLIGHT"
                $task.Attempts += 1
                Save-Ledger $ledger
                
                try {
                    $payload = @{ message = (Get-Content $procFile -Raw) } | ConvertTo-Json
                    $res = Invoke-RestMethod -Uri $geminiPanelEndpoint -Method Post -Body $payload -ContentType "application/json" -TimeoutSec 10 -ErrorAction Stop
                    $task.Status = "WAITING_ACK"
                    Write-Log "Task $key успешно отправлен (HTTP 200). Ожидание ответа." "INFO"
                } catch {
                    Write-Log "Ошибка отправки $key: $($_.Exception.Message)" "ERROR"
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
