$ErrorActionPreference="Stop"
$broker=(Resolve-Path (Join-Path $PSScriptRoot "..\candidates\broker_v2.5-proposed-NOT-RELEASE.ps1")).Path
$testRoot=Join-Path $env:TEMP ("JarvisBrokerV25_"+[guid]::NewGuid().ToString("N"))
$script:passed=0
function Assert-True{param([bool]$Condition,[string]$Message);if(-not $Condition){throw $Message};Write-Host ("PASS: "+$Message) -ForegroundColor Green;$script:passed++}
function New-TestRoot{param([string]$Name);$path=Join-Path $testRoot $Name;foreach($folder in @("outbox_jarvis","outbox_gemini","processing","processed","errors","inbox_jarvis","inbox_gemini")){New-Item -ItemType Directory -Path (Join-Path $path $folder) -Force|Out-Null};return $path}
function Write-Task{
    param([string]$Path,[string]$TaskId,[string]$From,[string]$To,[string]$Extra="")
    $nl=[Environment]::NewLine
    $content="---"+$nl+"task_id: $TaskId"+$nl+"from: $From"+$nl+"to: $To"+$nl+$Extra+"---"+$nl+"Body for $TaskId"+$nl
    [IO.File]::WriteAllText($Path,$content,(New-Object System.Text.UTF8Encoding($false)))
}
function Invoke-BrokerOnce{param([string]$Root);& $broker -BasePath $Root -Once -MutexName ("Local\JarvisBrokerTest_"+[guid]::NewGuid().ToString("N"))}
try{
    New-Item -ItemType Directory -Path $testRoot -Force|Out-Null
    Write-Host "=== Jarvis Broker v2.5 integration tests: Windows PowerShell 5.1 ===" -ForegroundColor Cyan
    foreach($path in @($broker,$PSCommandPath)){$tokens=$null;$errors=$null;[System.Management.Automation.Language.Parser]::ParseFile($path,[ref]$tokens,[ref]$errors)|Out-Null;Assert-True ($errors.Count -eq 0) ("Parser accepts "+(Split-Path $path -Leaf))}
    $root=New-TestRoot "duplicates"
    Write-Task (Join-Path $root "outbox_jarvis\one.md") "same-task" "jarvis" "gemini"
    Write-Task (Join-Path $root "outbox_jarvis\two.md") "same-task" "jarvis" "gemini"
    Invoke-BrokerOnce $root
    $ledger=Get-Content (Join-Path $root "ledger.json") -Raw|ConvertFrom-Json
    $errors=@(Get-ChildItem (Join-Path $root "errors") -Filter "*.md" -File)
    $processing=@(Get-ChildItem (Join-Path $root "processing") -Filter "*.md" -File)
    Assert-True ($ledger.PSObject.Properties.Count -eq 1) "Duplicate task_id produces one Ledger record"
    Assert-True ($errors.Count -eq 1) "Duplicate task_id is quarantined"
    Assert-True ($processing.Count -eq 1) "Original task remains in processing"
    Assert-True ($ledger.'same-task'.Status -eq "TRANSPORT_NOT_CONFIGURED") "Gemini transport stays disabled"
    $root=New-TestRoot "ack"
    Write-Task (Join-Path $root "processing\original.md") "original-id" "jarvis" "gemini"
    Write-Task (Join-Path $root "outbox_gemini\ack.md") "ack-record" "gemini" "jarvis" ("ack_task_id: original-id"+[Environment]::NewLine)
    Invoke-BrokerOnce $root
    $ledger=Get-Content (Join-Path $root "ledger.json") -Raw|ConvertFrom-Json
    Assert-True ($ledger.'original-id'.Status -eq "COMPLETED") "ACK marks original task completed"
    Assert-True ($ledger.'ack-record'.Status -eq "COMPLETED") "ACK record is completed"
    Assert-True (Test-Path (Join-Path $root "processed\original.md")) "Original task moves to processed"
    Assert-True (Test-Path (Join-Path $root "processed\ack.md")) "ACK file moves to processed"
    $root=New-TestRoot "forged-ack"
    Write-Task (Join-Path $root "processing\original.md") "original-id" "jarvis" "gemini"
    Write-Task (Join-Path $root "outbox_gemini\forged.md") "forged-ack" "attacker" "jarvis" ("ack_task_id: original-id"+[Environment]::NewLine)
    Invoke-BrokerOnce $root
    $ledger=Get-Content (Join-Path $root "ledger.json") -Raw|ConvertFrom-Json
    Assert-True ($ledger.'original-id'.Status -ne "COMPLETED") "ACK with mismatched sender cannot complete original task"
    Assert-True (Test-Path (Join-Path $root "processing\forged.md")) "Mismatched ACK is retained for investigation"
    $root=New-TestRoot "orphan"
    Write-Task (Join-Path $root "processing\orphan.md") "orphan-id" "jarvis" "gemini"
    Invoke-BrokerOnce $root
    $ledger=Get-Content (Join-Path $root "ledger.json") -Raw|ConvertFrom-Json
    Assert-True ($ledger.'orphan-id'.Status -eq "TRANSPORT_NOT_CONFIGURED") "Orphan processing file is recovered into Ledger"
    $root=New-TestRoot "backup"
    [IO.File]::WriteAllText((Join-Path $root "ledger.json"),"{ invalid json")
    $backup=@{"backup-id"=@{Status="QUEUED";File="backup.md";Attempts=0;Source="jarvis";Target="jarvis"}}|ConvertTo-Json -Depth 5
    [IO.File]::WriteAllText((Join-Path $root "ledger.bak.json"),$backup,(New-Object System.Text.UTF8Encoding($false)))
    Invoke-BrokerOnce $root
    $ledger=Get-Content (Join-Path $root "ledger.json") -Raw|ConvertFrom-Json
    Assert-True ($null -ne $ledger.PSObject.Properties["backup-id"]) "Corrupt primary recovers from backup"
    $root=New-TestRoot "mutex"
    $mutexName="Local\JarvisBrokerMutex_"+[guid]::NewGuid().ToString("N")
    $powershell=Join-Path $PSHOME "powershell.exe"
    $firstArgs=@("-NoProfile","-ExecutionPolicy","Bypass","-File",$broker,"-BasePath",$root,"-MaxIterations","3","-SleepSeconds","2","-MutexName",$mutexName)
    $first=Start-Process -FilePath $powershell -ArgumentList $firstArgs -PassThru -WindowStyle Hidden
    Start-Sleep -Milliseconds 700
    $secondArgs=@("-NoProfile","-ExecutionPolicy","Bypass","-File",$broker,"-BasePath",$root,"-Once","-MutexName",$mutexName)
    $second=Start-Process -FilePath $powershell -ArgumentList $secondArgs -PassThru -Wait -WindowStyle Hidden
    $first.WaitForExit()
    Assert-True ($second.ExitCode -ne 0) "Second concurrent process is rejected by OS mutex"
    Assert-True ($first.ExitCode -eq 0) "Mutex owner exits and releases mutex"
    Write-Host ("=== RESULT: {0} assertions passed ===" -f $script:passed) -ForegroundColor Cyan
}finally{if(Test-Path $testRoot){Remove-Item $testRoot -Recurse -Force}}
