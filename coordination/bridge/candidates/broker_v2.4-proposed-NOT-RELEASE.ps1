# Внимание: Транспорт отключен.
$geminiPanelEndpoint = $null 

# --- 1. ЗАЩИТА ОТ ДВОЙНОГО ЗАПУСКА (SINGLETON) ---
$mutexCreated = $false
$mutex = New-Object System.Threading.Mutex($true, "Global\JarvisGeminiBrokerMutex", [ref]$mutexCreated)
if (-not $mutexCreated) {
    Write-Host "CRITICAL: Брокер уже запущен в другом процессе. Выход." -ForegroundColor Red
    exit 1
}

$basePath = "C:\dr\Universal-AI-Factory\coordination\bridge"
$ledgerPath = Join-Path $basePath "ledger.json"
$ledgerBakPath = Join-Path $basePath "ledger.bak.json"
$logPath = Join-Path $basePath "bridge_sync.log"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $timestamp = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    $logLine = "[$timestamp] [$Level] $Message"
    Write-Host $logLine
    Add-Content -Path $logPath -Value $logLine
}

function Convert-PSObjectToHashtable {
    param($obj)
    if ($null -eq $obj) { return $null }
    if ($obj -is [System.Management.Automation.PSCustomObject]) {
        $hash = @{}
        foreach ($prop in $obj.psobject.properties) {
            $hash[$prop.Name] = Convert-PSObjectToHashtable -obj $prop.Value
        }
        return $hash
    }
    return $obj
}

function Load-Ledger {
    $targetPath = $null
    if (Test-Path $ledgerPath) {
        $targetPath = $ledgerPath
    } elseif (Test-Path $ledgerBakPath) {
        Write-Log "Используем резервный Ledger (ledger.bak.json)." "WARN"
        $targetPath = $ledgerBakPath
    }
    
    if ($null -ne $targetPath) {
        try {
            $json = Get-Content $targetPath -Raw | ConvertFrom-Json
            $hash = Convert-PSObjectToHashtable -obj $json
            if ($hash -is [hashtable]) { 
                return $hash 
            }
        } catch { 
            Write-Log "Ошибка чтения Ledger: $($_.Exception.Message)" "CRITICAL" 
        }
    }
    return @{}
}

function Save-Ledger {
    param($Ledger)
    $tmpPath = "$ledgerPath.tmp"
    
    if (Test-Path $ledgerPath) { 
        Copy-Item -Path $ledgerPath -Destination $ledgerBakPath -Force 
    }
    
    $Ledger | ConvertTo-Json -Depth 5 | Out-File -FilePath $tmpPath -Encoding UTF8 -Force
    Move-Item -Path $tmpPath -Destination $ledgerPath -Force
}

function Parse-Yaml {
    param([string]$Content)
    if ($Content -match '(?s)^---\r?\n(.*?)\r?\n---\r?\n(.*)') {
        $yamlBlock = $matches[1]
        $body = $matches[2]
        $meta = @{}
        
        $lines = $yamlBlock -split '\r?\n'
        foreach ($line in $lines) {
            if ($line -match '^([a-zA-Z0-9_]+):\s*"?([^"]*)"?$') {
                $meta[$matches[1]] = $matches[2]
            }
        }
        return @{ Meta = $meta; Body = $body; Valid = $true }
    }
    return @{ Valid = $false }
}

Write-Log "Message Broker v2.4 (PS 5.1 Strict) инициализирован." "START"

try {
    while ($true) {
        $ledger = Load-Ledger
        $outboxes = @("outbox_jarvis", "outbox_gemini")
        $processingPath = Join-Path $basePath "processing"
        
        # --- ИМПОРТ ---
        foreach ($outbox in $outboxes) {
            $files = Get-ChildItem -Path (Join-Path $basePath $outbox) -Filter "*.md"
            foreach ($file in $files) {
                try { 
                    $stream = [IO.File]::Open($file.FullName, 'Open', 'Read', 'None')
                    $stream.Close() 
                } catch { 
                    continue 
                }
                
                $procFile = Join-Path $processingPath $file.Name
                Move-Item -Path $file.FullName -Destination $procFile -Force
                
                $parsed = Parse-Yaml -Content (Get-Content $procFile -Raw)
                if (-not $parsed.Valid -or -not $parsed.Meta.ContainsKey('task_id')) {
                    Write-Log "Invalid YAML. Rejected: $($file.Name)" "ERROR"
                    Move-Item -Path $procFile -Destination (Join-Path $basePath "errors\$($file.Name)") -Force
                    continue
                }

                $taskId = $parsed.Meta.task_id
                if (-not $ledger.ContainsKey($taskId)) {
                    $ledger[$taskId] = @{
                        Status = "QUEUED"
                        File = $file.Name
                        Attempts = 0
                        Source = $parsed.Meta.from
                        Target = $parsed.Meta.to
                    }
                    Write-Log "Task $taskId QUEUED" "INFO"
                    Save-Ledger -Ledger $ledger
                } else {
                    Write-Log "Дубликат task_id: $taskId. Игнорируем перезапись стейта." "WARN"
                }
            }
        }

        # --- ОБРАБОТКА ---
        $keys = @($ledger.Keys)
        foreach ($k in $keys) {
            $task = $ledger[$k]
            $procFile = Join-Path $processingPath $task.File
            
            if ($task.Status -eq "QUEUED" -or $task.Status -eq "TRANSPORT_NOT_CONFIGURED") {
                if (-not (Test-Path $procFile)) { 
                    continue 
                }
                
                $parsed = Parse-Yaml -Content (Get-Content $procFile -Raw)
                
                # Проверка ACK
                if ($parsed.Meta.ContainsKey("ack_task_id")) {
                    $ackId = $parsed.Meta.ack_task_id
                    if ($ledger.ContainsKey($ackId)) {
                        Write-Log "Получен ACK завершения для $ackId" "INFO"
                        
                        $origTask = $ledger[$ackId]
                        $origProcFile = Join-Path $processingPath $origTask.File
                        if (Test-Path $origProcFile) {
                            Move-Item -Path $origProcFile -Destination (Join-Path $basePath "processed\$($origTask.File)") -Force
                        }
                        $origTask.Status = "COMPLETED"
                        
                        $targetInbox = if ($task.Target -eq "jarvis") { "inbox_jarvis" } else { "inbox_gemini" }
                        Move-Item -Path $procFile -Destination (Join-Path $basePath "$targetInbox\$($task.File)") -Force
                        $task.Status = "COMPLETED"
                        Save-Ledger -Ledger $ledger
                        continue
                    }
                }

                # Транспорт
                if ($task.Target -eq "gemini") {
                    if ([string]::IsNullOrEmpty($geminiPanelEndpoint)) {
                        if ($task.Status -ne "TRANSPORT_NOT_CONFIGURED") {
                            $task.Status = "TRANSPORT_NOT_CONFIGURED"
                            Write-Log "Транспорт не задан. Task $k заморожен." "WARN"
                            Save-Ledger -Ledger $ledger
                        }
                        continue
                    }

                    $task.Status = "IN_FLIGHT"
                    $task.Attempts += 1
                    Save-Ledger -Ledger $ledger
                    
                    try {
                        $payload = @{ message = (Get-Content $procFile -Raw) } | ConvertTo-Json
                        $res = Invoke-RestMethod -Uri $geminiPanelEndpoint -Method Post -Body $payload -ContentType "application/json" -TimeoutSec 10 -ErrorAction Stop
                        
                        $task.Status = "WAITING_ACK"
                        Write-Log "Task $k отправлен (HTTP 200)." "INFO"
                    } catch {
                        Write-Log "Ошибка отправки $k: $($_.Exception.Message)" "ERROR"
                        if ($task.Attempts -ge 3) {
                            $task.Status = "DEAD_LETTER"
                            Move-Item -Path $procFile -Destination (Join-Path $basePath "errors\$($task.File)") -Force
                        } else {
                            $task.Status = "QUEUED"
                        }
                    }
                    Save-Ledger -Ledger $ledger
                }
            }
        }
        Start-Sleep -Seconds 3
    }
} finally {
    if ($null -ne $mutex) {
        $mutex.ReleaseMutex()
        $mutex.Dispose()
    }
}