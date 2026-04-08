# 在本机首次初始化 Git 并提交（.env 已被 .gitignore 排除）
# 用法：
#   .\scripts\init-and-commit.ps1 -Email "你的邮箱" [-Name "显示名"]
#   同上并推送：加 -RemoteUrl "https://github.com/用户/仓库.git" -Push
# 依赖：已安装 Git 并在终端可用 git

param(
    [Parameter(Mandatory = $true)]
    [string]$Email,
    [string]$Name = "User",
    [string]$RemoteUrl = "",
    [switch]$Push
)

$ErrorActionPreference = "Stop"
$Root = Split-Path $PSScriptRoot -Parent
Set-Location $Root

if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Error "未找到 git。请安装 Git for Windows 后重开终端：https://git-scm.com/download/win"
    exit 1
}

if (-not (Test-Path ".git")) {
    git init -b main
}

git config user.email $Email
git config user.name $Name
git config core.hooksPath githooks

git add -A
git status

if (git diff --cached --quiet 2>$null) {
    Write-Host "没有已暂存的变更，跳过 commit。" -ForegroundColor Yellow
} else {
    git commit -m "chore: 初始化竞争情报工具仓库（.env 忽略、提交钩子、密钥脱敏）"
}

if ($Push) {
    if (-not $RemoteUrl) {
        Write-Error "使用 -Push 时必须提供 -RemoteUrl（例如 https://github.com/t0moon/competitorsmart.git）"
        exit 1
    }
    git remote get-url origin 2>$null | Out-Null
    $hasOrigin = ($LASTEXITCODE -eq 0)
    if ($hasOrigin) {
        git remote set-url origin $RemoteUrl
    } else {
        git remote add origin $RemoteUrl
    }
    git push -u origin main
    Write-Host "`n已推送到: $RemoteUrl" -ForegroundColor Green
} else {
    Write-Host "`n完成。若要推送: git remote add origin <仓库URL>; git push -u origin main" -ForegroundColor Green
}
