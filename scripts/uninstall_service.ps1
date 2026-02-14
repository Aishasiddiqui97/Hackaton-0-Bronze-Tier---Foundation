# Gmail Watcher - Service Uninstall Script
# Run this script as Administrator to remove Gmail Watcher service

$ErrorActionPreference = "Stop"

Write-Host "=== Gmail Watcher Service Uninstall ===" -ForegroundColor Cyan
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

# Check if task exists
$ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue

if (-not $ExistingTask) {
    Write-Host "Task '$TaskName' is not installed." -ForegroundColor Yellow
    Write-Host ""
    pause
    exit 0
}

Write-Host "Found task: $TaskName" -ForegroundColor Yellow
Write-Host "Status: $($ExistingTask.State)" -ForegroundColor Yellow
Write-Host ""
Write-Host "Are you sure you want to remove Gmail Watcher Service? (Y/N)" -ForegroundColor Red
$response = Read-Host

if ($response -eq "Y" -or $response -eq "y") {
    Write-Host "Stopping task if running..." -ForegroundColor Cyan
    Stop-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    Start-Sleep -Seconds 2

    Write-Host "Removing scheduled task..." -ForegroundColor Cyan
    Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false

    Write-Host ""
    Write-Host "=== Uninstall Complete ===" -ForegroundColor Green
    Write-Host "Gmail Watcher Service has been removed." -ForegroundColor Green
} else {
    Write-Host "Uninstall cancelled." -ForegroundColor Yellow
}

Write-Host ""
pause
