#Requires -Version 5.1
<#
  一键：创建/补全 Comfy Desktop 模型关联到便携版 models
  双击同目录的「一键关联ComfyDesktop模型.bat」即可，或在 PowerShell 执行本脚本。
#>
param(
    [string]$PortableRoot = "D:\AI\ComfyUI\ComfyUI_windows_portable\ComfyUI"
)

$ErrorActionPreference = "Stop"

function Fail([string]$msg) {
    Write-Host ""
    Write-Host "失败: $msg" -ForegroundColor Red
    Write-Host "按任意键退出..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}

Write-Host "=== Comfy Desktop 模型一键关联 ===" -ForegroundColor Cyan
Write-Host "便携 ComfyUI: $PortableRoot"

if (-not (Test-Path -LiteralPath $PortableRoot)) {
    Fail "找不到便携目录。请确认存在: $PortableRoot"
}

$models = Join-Path $PortableRoot "models"
if (-not (Test-Path -LiteralPath $models)) {
    Fail "找不到 models 文件夹: $models"
}

$root = (Resolve-Path -LiteralPath $PortableRoot).Path
if (-not $root.EndsWith("\")) { $root += "\" }

$configDir = Join-Path $env:APPDATA "ComfyUI"
$configPath = Join-Path $configDir "extra_models_config.yaml"

Write-Host "配置目录: $configDir"
Write-Host "配置文件: $configPath"

New-Item -ItemType Directory -Force -Path $configDir | Out-Null

$fragment = @"
portable_shared:
    base_path: $root
    checkpoints: models/checkpoints/
    loras: models/loras/
    vae: models/vae/
    text_encoders: models/text_encoders/
    diffusion_models: models/diffusion_models/
    unet: models/unet/
    clip: models/clip/
    clip_vision: models/clip_vision/
    controlnet: models/controlnet/
    upscale_models: models/upscale_models/
    embeddings: models/embeddings/
    hypernetworks: models/hypernetworks/
"@

if (Test-Path -LiteralPath $configPath) {
    $stamp = Get-Date -Format "yyyyMMdd_HHmmss"
    $backup = Join-Path $configDir "extra_models_config.backup_$stamp.yaml"
    Copy-Item -LiteralPath $configPath -Destination $backup -Force
    Write-Host "已备份: $backup" -ForegroundColor Green

    $existing = Get-Content -LiteralPath $configPath -Raw -ErrorAction SilentlyContinue
    if ($null -eq $existing) { $existing = "" }

    if ($existing -match "(?m)^\s*portable_shared\s*:") {
        # Replace existing portable_shared block (simple: rewrite file keeping non-portable parts is hard;
        # safer: append marker only if missing — here we rebuild: keep original + ensure our block at end)
        Write-Host "检测到旧的 portable_shared，将在文件末尾覆盖追加最新块..." -ForegroundColor Yellow
        # Remove old portable_shared section roughly
        $cleaned = [regex]::Replace($existing, "(?ms)# ===== portable_shared.*?(\r?\n)(?=\S|\z)|(?ms)^\s*portable_shared\s*:.*?(?=(\r?\n)\S|\z)", "")
        $cleaned = $cleaned.TrimEnd() + "`r`n`r`n# ===== portable_shared (auto) =====`r`n" + $fragment
        Set-Content -LiteralPath $configPath -Value $cleaned -Encoding UTF8
    } else {
        Add-Content -LiteralPath $configPath -Value "`r`n# ===== portable_shared (auto) =====`r`n$fragment" -Encoding UTF8
    }
} else {
    $content = @"
# Comfy Desktop extra models — auto-created
# Default Desktop paths (if any) can be added above by the app later.

# ===== portable_shared (auto) =====
$fragment
"@
    Set-Content -LiteralPath $configPath -Value $content -Encoding UTF8
    Write-Host "已新建配置文件" -ForegroundColor Green
}

Write-Host ""
Write-Host "写入完成。请确认 models 子目录：" -ForegroundColor Green
@("diffusion_models","text_encoders","vae","loras","checkpoints") | ForEach-Object {
    $p = Join-Path $models $_
    if (Test-Path $p) {
        $n = (Get-ChildItem $p -File -ErrorAction SilentlyContinue | Measure-Object).Count
        Write-Host ("  [OK] {0}  ({1} files)" -f $_, $n)
    } else {
        Write-Host ("  [--] {0}  (文件夹不存在，可忽略)" -f $_) -ForegroundColor Yellow
    }
}

Write-Host ""
Write-Host "下一步：" -ForegroundColor Cyan
Write-Host "1. 完全退出 Comfy Desktop（托盘图标也要退出）"
Write-Host "2. 重新打开 Desktop"
Write-Host "3. 新建空白工作流，不要用自带缺模型的示例"
Write-Host "4. 添加 Load Diffusion Model，看下拉是否有 qwen / wan"
Write-Host ""
Write-Host "配置文件已打开供你核对。"
notepad $configPath

Write-Host "按任意键退出..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
