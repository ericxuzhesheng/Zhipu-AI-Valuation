# local_sync_schedule.ps1 — 注册 Windows 计划任务，每月1号自动同步
# Register a Windows Scheduled Task to auto-sync on the 1st of each month.
#
# 用法 / Usage（以管理员身份运行 / Run as Administrator）:
#   powershell -File local_sync_schedule.ps1
#
# 第一次运行后，可在 taskschd.msc 中查看 "ZhipuAI-AutoSync" 任务

$taskName   = "ZhipuAI-AutoSync"
$scriptPath = Join-Path $PSScriptRoot "local_sync.ps1"
$repoPath   = Split-Path $PSScriptRoot -Parent
$logFile    = Join-Path $repoPath "sync.log"

# 检查是否已存在，存在则先删除 / Remove existing task if any
$existing = Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "[INFO] Removing existing task '$taskName'..."
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
}

# 创建计划任务动作 / Create task action
$action = New-ScheduledTaskAction `
    -Execute "powershell.exe" `
    -Argument "-NoProfile -ExecutionPolicy Bypass -File `"$scriptPath`"" `
    -WorkingDirectory $repoPath

# 触发器：每月1号上午9:00 / Trigger: 1st of every month at 9:00 AM
$trigger = New-ScheduledTaskTrigger `
    -Daily `
    -At "09:00AM"

# 注意：New-ScheduledTaskTrigger 不直接支持 Monthly，改用 Daily + 脚本内判断日期
# 如果只在1号运行，用以下 Monthly 触发器：
# $trigger = New-ScheduledTaskTrigger -Monthly -DaysOfMonth 1 -At "09:00AM"

$trigger = New-ScheduledTaskTrigger `
    -Monthly `
    -DaysOfMonth 1 `
    -At "09:00AM"

# 设置：唤醒运行、允许按需运行、失败后重试 / Settings
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable `
    -RestartInterval (New-TimeSpan -Minutes 10) `
    -RestartCount 3 `
    -MultipleInstances IgnoreNew

# 注册任务（以当前用户身份运行）/ Register task (run as current user)
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

Register-ScheduledTask `
    -TaskName $taskName `
    -Action $action `
    -Trigger $trigger `
    -Settings $settings `
    -Principal $principal `
    -Description "每月1号自动从 GitHub 拉取智谱AI估值项目的最新数据 / Auto-pull latest ZhipuAI valuation data from GitHub on 1st of each month"

Write-Host "[OK] Task '$taskName' registered successfully."
Write-Host "      Script: $scriptPath"
Write-Host "      Schedule: Monthly on day 1 at 09:00 AM"
Write-Host "      Log: $logFile"
Write-Host ""
Write-Host "View/Edit: taskschd.msc -> search 'ZhipuAI-AutoSync'"
Write-Host "Run now:   Start-ScheduledTask -TaskName '$taskName'"
