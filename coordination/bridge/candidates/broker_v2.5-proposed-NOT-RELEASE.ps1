param([string]$BasePath=(Join-Path $PSScriptRoot ".."),[switch]$Once,[int]$MaxIterations=0,[int]$SleepSeconds=3,[string]$MutexName="Global\JarvisGeminiBrokerMutex")
$ErrorActionPreference="Stop"
$geminiPanelEndpoint=$null
$BasePath=[IO.Path]::GetFullPath($BasePath)
$ledgerPath=Join-Path $BasePath "ledger.json"
$ledgerBakPath=Join-Path $BasePath "ledger.bak.json"
$logPath=Join-Path $BasePath "bridge_sync.log"
$processingPath=Join-Path $BasePath "processing"
$script:BrokerMutex=$null
$script:MutexOwned=$false
function Ensure-BrokerDirectories {
    foreach($name in @("outbox_jarvis","outbox_gemini","processing","processed","errors","inbox_jarvis","inbox_gemini")){
        $path=Join-Path $BasePath $name
        if(-not(Test-Path -LiteralPath $path)){New-Item -ItemType Directory -Path $path -Force|Out-Null}
    }
}
function Write-Log {
    param([string]$Message,[string]$Level="INFO")
    $line="[{0}] [{1}] {2}" -f (Get-Date).ToString("yyyy-MM-dd HH:mm:ss.fff"),$Level,$Message
    Write-Host $line
    Add-Content -LiteralPath $logPath -Value $line -Encoding UTF8
}
function Convert-PSObjectToHashtable {
    param($Object)
    if($null -eq $Object){return $null}
    if($Object -is [System.Management.Automation.PSCustomObject]){
        $result=@{}
        foreach($property in $Object.PSObject.Properties){$result[$property.Name]=Convert-PSObjectToHashtable -Object $property.Value}
        return $result
    }
    if($Object -is [System.Array]){
        $items=@()
        foreach($item in $Object){$items+=,(Convert-PSObjectToHashtable -Object $item)}
        return ,$items
    }
    return $Object
}
function Read-LedgerFile {
    param([string]$Path)
    $parsed=ConvertFrom-Json -InputObject ([IO.File]::ReadAllText($Path,[Text.Encoding]::UTF8)) -ErrorAction Stop
    $ledger=Convert-PSObjectToHashtable -Object $parsed
    if($null -eq $ledger){return @{}}
    if($ledger -isnot [hashtable]){throw "Ledger root must be a JSON object."}
    return $ledger
}
function Load-Ledger {
    if(Test-Path -LiteralPath $ledgerPath){
        try{return (Read-LedgerFile -Path $ledgerPath)}
        catch{Write-Log ("Primary Ledger invalid; trying backup: {0}" -f $_.Exception.Message) "CRITICAL"}
    }
    if(Test-Path -LiteralPath $ledgerBakPath){
        try{$value=Read-LedgerFile -Path $ledgerBakPath;[IO.File]::Copy($ledgerBakPath,$ledgerPath,$true);Write-Log "Ledger recovered from backup and primary restored." "WARN";return $value}
        catch{throw ("Both primary and backup Ledger are unusable: {0}" -f $_.Exception.Message)}
    }
    return @{}
}
function Save-Ledger {
    param([hashtable]$Ledger)
    $temp=Join-Path $BasePath ("ledger.{0}.{1}.tmp" -f $PID,[guid]::NewGuid().ToString("N"))
    $utf8=New-Object System.Text.UTF8Encoding($false)
    [IO.File]::WriteAllText($temp,(ConvertTo-Json -InputObject $Ledger -Depth 10),$utf8)
    try{
        if(Test-Path -LiteralPath $ledgerPath){[IO.File]::Replace($temp,$ledgerPath,$ledgerBakPath,$true)}
        else{[IO.File]::Move($temp,$ledgerPath)}
    }finally{if(Test-Path -LiteralPath $temp){Remove-Item -LiteralPath $temp -Force}}
}
function Parse-Yaml {
    param([string]$Content)
    if($Content -notmatch '(?s)\A---\r?\n(.*?)\r?\n---\r?\n(.*)\z'){return @{Valid=$false;Meta=@{};Body=""}}
    $meta=@{}
    foreach($line in ($matches[1] -split '\r?\n')){
        if($line -match '^([a-zA-Z0-9_]+):\s*(.*?)\s*$'){
            $value=$matches[2].Trim()
            if($value.Length -ge 2 -and $value.StartsWith('"') -and $value.EndsWith('"')){$value=$value.Substring(1,$value.Length-2)}
            $meta[$matches[1]]=$value
        }
    }
    $valid=(-not[string]::IsNullOrWhiteSpace($meta.task_id)) -and (-not[string]::IsNullOrWhiteSpace($meta.from)) -and (-not[string]::IsNullOrWhiteSpace($meta.to))
    return @{Valid=$valid;Meta=$meta;Body=$matches[2]}
}
function Move-ToUniquePath {
    param([string]$Source,[string]$Destination)
    $dir=Split-Path -Parent $Destination
    if(-not(Test-Path -LiteralPath $dir)){New-Item -ItemType Directory -Path $dir -Force|Out-Null}
    if(Test-Path -LiteralPath $Destination){
        $base=[IO.Path]::GetFileNameWithoutExtension($Destination)
        $ext=[IO.Path]::GetExtension($Destination)
        $Destination=Join-Path $dir ("{0}.{1}{2}" -f $base,[guid]::NewGuid().ToString("N"),$ext)
    }
    Move-Item -LiteralPath $Source -Destination $Destination
}
function New-TaskRecord {
    param([string]$FileName,[hashtable]$Meta)
    return @{Status="QUEUED";File=$FileName;Attempts=0;Source=[string]$Meta.from;Target=[string]$Meta.to}
}
function Import-Outboxes {
    param([hashtable]$Ledger)
    foreach($box in @("outbox_jarvis","outbox_gemini")){
        $files=@(Get-ChildItem -LiteralPath (Join-Path $BasePath $box) -Filter "*.md" -File|Sort-Object Name)
        foreach($file in $files){
            $stream=$null
            try{$stream=[IO.File]::Open($file.FullName,[IO.FileMode]::Open,[IO.FileAccess]::Read,[IO.FileShare]::None)}
            catch{continue}
            finally{if($null -ne $stream){$stream.Dispose()}}
            $destination=Join-Path $processingPath $file.Name
            if(Test-Path -LiteralPath $destination){
                Move-ToUniquePath -Source $file.FullName -Destination (Join-Path (Join-Path $BasePath "errors") $file.Name)
                Write-Log ("Filename collision quarantined: {0}" -f $file.Name) "ERROR"
                continue
            }
            Move-Item -LiteralPath $file.FullName -Destination $destination
            $parsed=Parse-Yaml -Content ([IO.File]::ReadAllText($destination,[Text.Encoding]::UTF8))
            if(-not $parsed.Valid){
                Move-ToUniquePath -Source $destination -Destination (Join-Path (Join-Path $BasePath "errors") $file.Name)
                Write-Log ("Invalid task quarantined: {0}" -f $file.Name) "ERROR"
                continue
            }
            $id=[string]$parsed.Meta.task_id
            if($Ledger.ContainsKey($id)){
                Move-ToUniquePath -Source $destination -Destination (Join-Path (Join-Path $BasePath "errors") $file.Name)
                Write-Log ("Duplicate task_id quarantined: {0}" -f $id) "WARN"
                continue
            }
            $Ledger[$id]=New-TaskRecord -FileName $file.Name -Meta $parsed.Meta
            Save-Ledger -Ledger $Ledger
            Write-Log ("Task {0} imported." -f $id)
        }
    }
}
function Recover-OrphanedProcessingFiles {
    param([hashtable]$Ledger)
    foreach($file in @(Get-ChildItem -LiteralPath $processingPath -Filter "*.md" -File|Sort-Object Name)){
        $parsed=Parse-Yaml -Content ([IO.File]::ReadAllText($file.FullName,[Text.Encoding]::UTF8))
        if(-not $parsed.Valid){
            Move-ToUniquePath -Source $file.FullName -Destination (Join-Path (Join-Path $BasePath "errors") $file.Name)
            Write-Log ("Invalid processing orphan quarantined: {0}" -f $file.Name) "ERROR"
            continue
        }
        $id=[string]$parsed.Meta.task_id
        if(-not $Ledger.ContainsKey($id)){
            $Ledger[$id]=New-TaskRecord -FileName $file.Name -Meta $parsed.Meta
            Save-Ledger -Ledger $Ledger
            Write-Log ("Recovered processing orphan: {0}" -f $id) "WARN"
        }
    }
}
function Complete-Acknowledgement {
    param([hashtable]$Ledger,[string]$AckId,[string]$AckFileName,[string]$AckTaskId)
    if(-not $Ledger.ContainsKey($AckId)){return $false}
    $original=$Ledger[$AckId]
    $originalPath=Join-Path $processingPath $original.File
    if(Test-Path -LiteralPath $originalPath){
        Move-ToUniquePath -Source $originalPath -Destination (Join-Path (Join-Path $BasePath "processed") $original.File)
    }
    $original.Status="COMPLETED"
    $ackPath=Join-Path $processingPath $AckFileName
    if(Test-Path -LiteralPath $ackPath){
        Move-ToUniquePath -Source $ackPath -Destination (Join-Path (Join-Path $BasePath "processed") $AckFileName)
    }
    $Ledger[$AckTaskId].Status="COMPLETED"
    Save-Ledger -Ledger $Ledger
    Write-Log ("ACK completed task {0}" -f $AckId)
    return $true
}
function Invoke-BrokerIteration {
    $ledger=Load-Ledger
    Recover-OrphanedProcessingFiles -Ledger $ledger
    Import-Outboxes -Ledger $ledger
    foreach($id in @($ledger.Keys)){
        $task=$ledger[$id]
        if($task.Status -notin @("QUEUED","TRANSPORT_NOT_CONFIGURED")){continue}
        $path=Join-Path $processingPath $task.File
        if(-not(Test-Path -LiteralPath $path)){continue}
        $parsed=Parse-Yaml -Content ([IO.File]::ReadAllText($path,[Text.Encoding]::UTF8))
        if(-not $parsed.Valid){
            Move-ToUniquePath -Source $path -Destination (Join-Path (Join-Path $BasePath "errors") $task.File)
            $task.Status="DEAD_LETTER";Save-Ledger -Ledger $ledger;continue
        }
        if($parsed.Meta.ContainsKey("ack_task_id")){
            $ackId=[string]$parsed.Meta.ack_task_id
            if($ledger.ContainsKey($ackId)){
                $original=$ledger[$ackId]
                if(([string]$parsed.Meta.from -ne [string]$original.Target) -or ([string]$parsed.Meta.to -ne [string]$original.Source)){
                    Write-Log ("ACK route mismatch for {0}; retained for investigation." -f $ackId) "ERROR"
                    continue
                }
            }
            if(Complete-Acknowledgement -Ledger $ledger -AckId $ackId -AckFileName $task.File -AckTaskId $id){continue}
            Write-Log ("Unknown ACK target {0}; retained." -f $ackId) "WARN";continue
        }
        if($task.Target -eq "gemini" -and [string]::IsNullOrWhiteSpace($geminiPanelEndpoint)){
            if($task.Status -ne "TRANSPORT_NOT_CONFIGURED"){$task.Status="TRANSPORT_NOT_CONFIGURED";Save-Ledger -Ledger $ledger}
        }
    }
}
function Start-BrokerMutex {
    $created=$false
    $script:BrokerMutex=New-Object System.Threading.Mutex($false,$MutexName,[ref]$created)
    try{$script:MutexOwned=$script:BrokerMutex.WaitOne(0,$false)}
    catch [System.Threading.AbandonedMutexException]{$script:MutexOwned=$true;Write-Log "Recovered abandoned mutex." "WARN"}
    if(-not $script:MutexOwned){Write-Host "CRITICAL: Broker already running." -ForegroundColor Red;return $false}
    return $true
}
Ensure-BrokerDirectories
if(-not(Start-BrokerMutex)){if($null -ne $script:BrokerMutex){$script:BrokerMutex.Dispose()};exit 1}
try{
    Write-Log "Message Broker v2.5 initialized; transport disabled." "START"
    $iteration=0
    do{
        Invoke-BrokerIteration
        $iteration++
        if($Once){break}
        if($MaxIterations -gt 0 -and $iteration -ge $MaxIterations){break}
        Start-Sleep -Seconds ([Math]::Max(1,$SleepSeconds))
    }while($true)
    Write-Log ("Broker stopped after {0} iteration(s)." -f $iteration) "STOP"
}finally{
    if($script:MutexOwned -and $null -ne $script:BrokerMutex){$script:BrokerMutex.ReleaseMutex()}
    if($null -ne $script:BrokerMutex){$script:BrokerMutex.Dispose()}
}
