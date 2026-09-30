# 现有 ComfyUI 体检报告（4080S · 用户机）

体检日期：2026-09-27  
安装路径：`D:\PS2025ComfyUI\PhotoshopComfyUIAI\...`（Photoshop 整合包）

## 结论（一句话）

**能用，插件底子够做国风静帧；核心版本偏旧（约 2024-06），刚才主要是 Manager 拉依赖/缓存，不是整包升到 2025/2026 最新。**  
先换国风底模做冒烟测试即可；成片视频仍建议可灵。

## 好消息

| 项 | 日志证据 | 对短片的意义 |
|----|----------|--------------|
| 显卡识别正确 | `RTX 4080 SUPER`，VRAM **16376 MB**，`NORMAL_VRAM` | 跑 SDXL + ControlNet + IP-Adapter 足够 |
| 内存充足 | RAM **65366 MB** | 批量出图、剪辑同机也稳 |
| Python 合适 | **3.11.8** | 与手册建议一致 |
| 关键插件已在 | IPAdapter_plus、ControlNet aux、Advanced-ControlNet、Impact Pack、VideoHelperSuite、Manager | 锁脸、控线、修脸链路具备 |
| UI 正常 | `http://127.0.0.1:8188`，有 **经理/Manager** 按钮 | 可继续装节点与下模型 |
| 启动无致命崩溃 | `Starting server` 成功，状态「闲置的」 | 环境可工作 |

## 关于「有没有更新」

| 现象 | 含义 |
|------|------|
| 启动时 `[START] Security scan`、`installing dependencies done` | **ComfyUI-Manager** 在检查并补依赖 |
| `default cache updated: ... model-list.json` 等 | Manager **刷新了在线插件/模型目录缓存**（今天 2026-09-27） |
| `ComfyUI Revision: 2284 … Released on '2024-06-25'` | **ComfyUI 本体停在 2024-06-25**，并非 2026 最新主干 |
| `pytorch 2.2.1+cu121` | 可用，但偏旧；新 Flux 工作流可能吃力 |

**判断：** 两年前的 Photoshop 整合包被 Manager「维护性更新」了一下，**看起来像在更新，但核心并未升到最新一代。**  
对当前目标（SDXL 国风静帧 + 可灵视频）**够用**；若以后要大规模上 Flux / 新视频节点，再考虑另装一份干净新版 ComfyUI（旧包可保留）。

## 需要立刻注意的问题

### 1. 当前底模不对路（最重要）

界面加载的是：

`maginMixReal(更真实写实，电影感摄影…)…safetensors`

这是 **写实摄影风**，和《天书奇谈》水墨/工笔相反。  
默认工作流也是 **512×512**（偏 SD1.5），国风短片请改用 **SDXL 约 1344×768 或 1216×832**。

### 2. AnimateDiff 报错（可暂缓）

```
[AnimateDiff] - ERROR - No models available
```

插件在，**运动模没下**。本片主力视频用 **可灵**，这条可先忽略；以后想本机试动再补 motion 模型。

### 3. 小警告（不影响开干）

- `no module 'xformers'`：已用 pytorch attention，4080S 可接受  
- WAS 未配置 `ffmpeg_bin_path`：有系统 FFmpeg 即可  
- 启动偏慢：AlekPet / art-venture / SUPIR 等节点很重（整合包通病）

## 是否符合「阶段 0」使用需求

| 需求 | 是否达标 | 说明 |
|------|----------|------|
| 本机出静帧 | ✅ | GPU/启动正常 |
| 角色一致性 | ✅ 条件具备 | 需确认 IP-Adapter **模型文件**已放入对应目录 |
| 线稿/姿态控制 | ✅ 条件具备 | 需补 SDXL ControlNet 权重（若还没有） |
| 国风风格 | ⚠️ 未就绪 | **必须换 SDXL/国风底模 + LoRA** |
| 本机长镜头成片 | ❌ 非目标 | 用可灵；AnimateDiff 缺模型 |
| Flux 最新工作流 | ⚠️ 勉强/不优先 | 核心偏旧，先 SDXL |

**总评：符合「先跑通国风静帧」需求；差的是模型和分辨率，不是显卡或能否启动。**

## 你现在按这 5 步做（今天）

1. **不要用** 当前 `maginMixReal` 做正片  
2. 在 Liblib/Civitai 下 **1 个 SDXL 插画/国风底模** → `ComfyUI\models\checkpoints\`  
3. 再下 **1 个水墨或工笔 LoRA** → `models\loras\`  
4. 空潜空间改成 **宽 1344 × 高 768**（或 1216×832），Steps 28、CFG 6 左右  
5. 用 `prompts/00-冒烟测试.md` 出一张狐女/荒庙，确认有水墨味  

可选：在 Manager 里检查 IP-Adapter、ControlNet 模型是否显示已安装；缺了就按红字下载。

## 建议策略（针对这个 Photoshop 整合包）

- **立即：旁路安装官方最新便携包**（见 `docs/05-升级最新ComfyUI.md`），不要原地覆盖旧包  
- **短期：** 新包做出图；旧包仅在需要 Photoshop 联用时打开  
- **模型：** 用 `mklink /J` 复用同一 `models` 目录，避免重复下载  
- **视频：** 全程可灵，不必先修 AnimateDiff
