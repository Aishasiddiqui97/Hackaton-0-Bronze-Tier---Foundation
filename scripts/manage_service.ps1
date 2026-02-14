# Gmail Watcher - Service Management Script
# Quick commands to manage the Gmail Watcher service

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("start", "stop", "restart", "status", "logs")]
    [string]$Action = "status"
)

$TaskName = "GmailWatcherService"
$LogFile = "logs\actions.log"

function Show-Status {
    $Task = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

    if (-not $Task) {
        Write-Host "Gmail Watcher Service: NOT INSTALLED" -ForegroundColor Red
        return
    }

    $State = $Task.State
    $LastRunTime = (Get-ScheduledTaskInfo -TaskName $TaskName).LastRunTime
    $NextRunTime = (Get-ScheduledTaskInfo -TaskName $TaskName).NextRunTime

    Write-Host "=== Gmail Watcher Service Status ===" -ForegroundColor Cyan
    Write-Host "Status: $State" -ForegroundColor $(if ($State -eq "Running") { "Green" } else { "Yellow" })
    Write-Host "Last Run: $LastRunTime"
    Write-Host "Next Run: $NextRunTime"
    Write-Host ""
}

function Start-Service {
    Write-Host "Starting Gmail Watcher Service..." -ForegroundColor Cyan
    Start-ScheduledTask -TaskName $TaskName
    Start-Sleep -Seconds 2
    Show-Status
}

function Stop-Service {
    Write-Host "Stopping Gmail Watcher Service..." -ForegroundColor Cyan
    Stop-ScheduledTask -TaskName $TaskName
    Start-Sleep -Seconds 2
    Show-Status
}

function Restart-Service {
    Write-Host "Restarting Gmail Watcher Service..." -ForegroundColor Cyan
    Stop-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2
    Start-ScheduledTask -TaskName $TaskName
    Start-Sleep -Seconds 2
    Show-Status
}

function Show-Logs {
    if (Test-Path $LogFile) {
        Write-Host "=== Recent Logs (Last 20 lines) ===" -ForegroundColor Cyan
        Get-Content $LogFile -Tail 20
    } else {
        Write-Host "Log file not found: $LogFile" -ForegroundColor Yellow
    }
}

# Execute action
switch ($Action) {
    "start" { Start-Service }
    "stop" { Stop-Service }
    "restart" { Restart-Service }
    "status" { Show-Status }
    "logs" { Show-Logs }
}
