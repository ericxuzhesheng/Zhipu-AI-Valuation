# local_sync.ps1 — 本地自动同步脚本 / Local auto-sync script
# 每月1号拉取远端通过 GitHub Actions 更新的数据和图表
# Pulls the latest data/figures pushed by the monthly GitHub Actions workflow.
#
# 用法 / Usage:
#   手动运行:  powershell -File local_sync.ps1
#   计划任务:  见 local_sync_schedule.ps1

param(
    [string]$RepoPath = $PSScriptRoot,
    [string]$Remote = "origin",
    [string]$Branch = "main"
)

Set-Location $RepoPath

$logFile = Join-Path $RepoPath "sync.log"

function Write-Log {
    param([string]$Message)
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$ts] $Message"
    Write-Host $line
    Add-Content -Path $logFile -Value $line -Encoding utf8
}

Write-Log "=== Sync started ==="

# 1. Fetch remote without merging / 先拉取远端信息
try {
    git fetch $Remote $Branch 2>&1 | Out-Null
    if ($LASTEXITCODE -ne 0) {
        Write-Log "ERROR: git fetch failed. Check network or authentication."
        exit 1
    }
    Write-Log "git fetch OK"
}
catch {
    Write-Log "ERROR: git fetch exception — $_"
    exit 1
}

# 2. Check if local is behind / 检查本地是否落后
$localHash  = git rev-parse HEAD 2>$null
$remoteHash = git rev-parse "$Remote/$Branch" 2>$null

if ($localHash -eq $remoteHash) {
    Write-Log "Already up to date. Nothing to pull."
    Write-Log "=== Sync finished (no changes) ==="
    exit 0
}

Write-Log "Remote has new commits. Pulling..."

# 3. Stash local changes if any / 暂存本地未提交变更
$hasChanges = $false
$status = git status --porcelain 2>&1
if ($status) {
    $hasChanges = $true
    Write-Log "Stashing local changes..."
    git stash push -m "auto-sync stash $(Get-Date -Format 'yyyy-MM-dd HH:mm')" 2>&1 | Out-Null
}

# 4. Pull / 拉取
try {
    git pull --ff-only $Remote $Branch 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Log "ERROR: git pull failed."
        if ($hasChanges) { git stash pop 2>&1 | Out-Null }
        exit 1
    }
    Write-Log "git pull OK"
}
catch {
    Write-Log "ERROR: git pull exception — $_"
    if ($hasChanges) { git stash pop 2>&1 | Out-Null }
    exit 1
}

# 5. Restore stashed changes / 恢复暂存
if ($hasChanges) {
    git stash pop 2>&1 | Out-Null
    Write-Log "Stash popped"
}

$newHash = git rev-parse HEAD
Write-Log "Updated: $localHash -> $newHash"
Write-Log "=== Sync finished (pulled) ==="
