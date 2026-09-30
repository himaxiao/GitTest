# 国风 / 聊斋风 AI 动画短片制作手册

风格对标：**《天书奇谈》**（水墨奇幻、工笔人物、怪诞神异、上海美影叙事感）

本仓库是一部从零开始的 **AI 动画短片制作工程脚手架**：目录结构、环境清单、工具下载、提示词模板、全流程步骤。

## 当前阶段

双轨并行：

1. **试片轨**：Qwen 关键帧 → Wan2.2 微动 → 剪辑（《青凤》4 镜）  
2. **架构轨**：远期分层管线框架已立项 → [docs/14-远期管线架构总纲.md](docs/14-远期管线架构总纲.md)

桌面端 Comfy 模型关联 → [docs/15-ComfyDesktop迁移与模型关联.md](docs/15-ComfyDesktop迁移与模型关联.md)

| 文档 | 内容 |
|------|------|
| [docs/14-远期管线架构总纲.md](docs/14-远期管线架构总纲.md) | **L0–L7 分层、Phase A–F、资产分库** |
| [docs/15-ComfyDesktop迁移与模型关联.md](docs/15-ComfyDesktop迁移与模型关联.md) | **Desktop ↔ 便携版模型挂载** |
| [docs/00-环境与工具准备.md](docs/00-环境与工具准备.md) | 硬件、软件安装、账号、目录规范 |
| [docs/03-RTX4080S本机安装手册.md](docs/03-RTX4080S本机安装手册.md) | 4080S 专用安装与参数 |
| [docs/05-升级最新ComfyUI.md](docs/05-升级最新ComfyUI.md) | 便携包旁路升级 |
| [docs/08-手搭Qwen2512工作流.md](docs/08-手搭Qwen2512工作流.md) | Qwen 手搭静帧 |
| [docs/10-本地视频稳定配方.md](docs/10-本地视频稳定配方.md) | Wan 微动稳定配方 |
| [docs/11-视频节点框架与长片方法.md](docs/11-视频节点框架与长片方法.md) | 节点模块与长片方法 |
| [docs/01-全流程步骤.md](docs/01-全流程步骤.md) | 从剧本到成片 |
| [docs/02-天书奇谈风格圣经.md](docs/02-天书奇谈风格圣经.md) | 视觉风格定义 |
| [tools/link_comfy_desktop_models.ps1](tools/link_comfy_desktop_models.ps1) | Desktop 模型路径一键追加 |
| [prompts/](prompts/) | 提示词模板 |

**硬件路线：** RTX 4080 SUPER → 本机 Comfy（便携或 Desktop，共用模型）+ 本机剪辑。

## 工程目录

```
01-script/           剧本、分场、对白
02-visual-bible/     锚点 / 训练净板 / 场景板 / 角色包
03-storyboard/       分镜表与分镜图
04-keyframes/        关键帧静帧
05-animation/        动态镜头片段
06-audio/            配音、音效、配乐
07-edit/             剪辑工程文件
08-export/           成片导出
control/             Pose/Depth/表情驱动源（远期）
datasets/            风格/角色 LoRA 数据空位
workflows/           Comfy 工作流 JSON
refs/                参考图
prompts/             提示词库
tools/               脚本与清单
docs/                制作与架构文档
```

## 推荐路径

**试片：** 剧本 → 定妆锚点 → 分镜关键帧 → Wan 微动 → 降帧剪辑  

**系列：** 见架构总纲 Phase A→F（LoRA / ControlNet / LivePortrait / SAM2 等按阶段解锁）
