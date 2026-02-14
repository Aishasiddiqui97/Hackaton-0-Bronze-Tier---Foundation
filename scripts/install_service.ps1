# Gmail Watcher - Windows Service Setup Script
# Run this script as Administrator to install Gmail Watcher as a scheduled task

$ErrorActionPreference = "Stop"

Write-Host "=== Gmail Watcher Service Setup ===" -ForegroundColor Cyan
Write-Host ""

# Get the script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDir
$BatchFile = Join-Path $ScriptDir "start_gmail_watcher.bat"

Write-Host "Project Root: $ProjectRoot" -ForegroundColor Yellow
Write-Host "Batch File: $BatchFile" -ForegroundColor Yellow
Write-Host ""

# Check if running as Administrator
$isAdmin = ([Security.Principal.WindowsPrincipal] [Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "ERROR: This script must be run as Administrator!" -ForegroundColor Red
    Write-Host "Right-click PowerShell and select 'Run as Administrator'" -ForegroundColor Yellow
    pause
    exit 1
}

# Task name
$TaskName = "GmailWatcherService"

# Check if task already exists
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if ($ExistingTask) {
    Write-Host "Task '$TaskName' already exists." -ForegroundColor Yellow
    $response = Read-Host "Do you want to remove and recreate it? (Y/N)"

    if ($response -eq "Y" -or $response -eq "y") {
        Write-Host "Removing existing task..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
        Write-Host "Existing task removed." -ForegroundColor Green
    } else {
        Write-Host "Installation cancelled." -ForegroundColor Yellow
        pause
        exit 0
    }
}

# Create the scheduled task
Write-Host "Creating scheduled task..." -ForegroundColor Cyan

# Task action - run the batch file
$Action = New-ScheduledTaskAction -Execute $BatchFile -WorkingDirectory $ProjectRoot

# Task trigger - at system startup
$Trigger = New-ScheduledTaskTrigger -AtStartup

# Task settings
$Settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartCount 3 `
    -RestartInterval (New-TimeSpan -Minutes 1) `
    -ExecutionTimeLimit (New-TimeSpan -Days 365)

# Task principal - run as current user
$Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest

# Register the task
Register-ScheduledTask `
    -TaskName $TaskName `
    -Action $Action `
    -Trigger $Trigger `
    -Settings $Settings `
    -Principal $Principal `
    -Description "Gmail Watcher Service - Monitors Gmail and processes emails automatically"

Write-Host ""
Write-Host "=== Installation Complete ===" -ForegroundColor Green
Write-Host ""
Write-Host "Gmail Watcher has been installed as a scheduled task." -ForegroundColor Green
Write-Host "It will start automatically when Windows boots." -ForegroundColor Green
Write-Host ""
Write-Host "Management Commands:" -ForegroundColor Cyan
Write-Host "  Start:   Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor White
Write-Host "  Stop:    Stop-ScheduledTask -TaskName '$TaskName'" -ForegroundColor White
Write-Host "  Status:  Get-ScheduledTask -TaskName '$TaskName' | Select State" -ForegroundColor White
Write-Host "  Remove:  Unregister-ScheduledTask -TaskName '$TaskName'" -ForegroundColor White
Write-Host ""
Write-Host "Do you want to start the service now? (Y/N)" -ForegroundColor Yellow
$startNow = Read-Host

if ($startNow -eq "Y" -or $startNow -eq "y") {
    Write-Host "Starting Gmail Watcher Service..." -ForegroundColor Cyan
    Start-ScheduledTask -TaskName $TaskName
    Start-Sleep -Seconds 2

    $TaskState = (Get-ScheduledTask -TaskName $TaskName).State
    Write-Host "Service Status: $TaskState" -ForegroundColor Green
}

Write-Host ""
Write-Host "Setup complete! Press any key to exit..." -ForegroundColor Green
pause
