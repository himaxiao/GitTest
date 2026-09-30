@echo off
chcp 65001 >nul
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0一键关联ComfyDesktop模型.ps1" -PortableRoot "D:\AI\ComfyUI\ComfyUI_windows_portable\ComfyUI"
if errorlevel 1 pause
