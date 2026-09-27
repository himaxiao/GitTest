# 下载 ComfyUI 期间：同步下载清单（4080S）

ComfyUI 便携包下完并解压后，按下面顺序补齐。打勾即过。

---

## A. 本机软件（与 ComfyUI 同级必需）

| 状态 | 名称 | 用途 | 获取 |
|------|------|------|------|
| [ ] | **7-Zip** | 解压 `.7z` 便携包/模型 | https://www.7-zip.org |
| [ ] | **Git** | 装 Manager/插件 | https://git-scm.com |
| [ ] | **NVIDIA 驱动（较新）** | 新版 Torch/CUDA 能跑 | https://www.nvidia.com/drivers |
| [ ] | **FFmpeg** + 加入 PATH | 转码、抽帧、合并 | https://ffmpeg.org |
| [ ] | **剪映专业版** 或 DaVinci Resolve | 剪辑成片 | 剪映官网 / Blackmagic |
| [ ] | **Audacity** | 旁白降噪、音轨整理 | https://www.audacityteam.org |
| [ ] | **VLC**（可选） | 检查成片 | https://www.videolan.org |
| [ ] | **Krita** 或 Photopea | 修线、补图 | https://krita.org / photopea.com |

> Photoshop 若已有可继续用；没有不必新买，Photopea/Krita 够用。

---

## B. ComfyUI 装好后立刻要的「模型」（比再下软件更急）

放到 `ComfyUI\models\`（或你联接的统一模型库）：

| 状态 | 文件 | 目录 | 说明 |
|------|------|------|------|
| [ ] | **SDXL 插画/国风底模 ×1** | `checkpoints\` | 正片主力；不要用写实 `maginMixReal` |
| [ ] | **水墨 或 工笔 LoRA ×1** | `loras\` | Liblib/Civitai 搜：水墨、工笔、国风 |
| [ ] | SDXL VAE（若底模说明需要） | `vae\` | 很多 SDXL 已内嵌，按说明 |

**可稍后（定妆稳定后再下）：**

| 状态 | 文件 | 目录 |
|------|------|------|
| [ ] | ControlNet SDXL：lineart / softedge / depth | `controlnet\` |
| [ ] | IP-Adapter 相关权重 + CLIP Vision | `ipadapter\` 等（跟插件说明） |
| [ ] | Flux Dev fp8（精品定妆，非必须先下） | 按 Flux 工作流目录 |

搜索站：

- 国内：https://www.liblib.art  
- 国际：https://civitai.com  

---

## C. ComfyUI 插件（Manager 里装，不是另下安装包）

新便携包启动后装：

| 状态 | 插件 | 用途 |
|------|------|------|
| [ ] | **ComfyUI-Manager** | 管理插件（没有就先装它） |
| [ ] | **ComfyUI_IPAdapter_plus** | 锁角色脸/服饰 |
| [ ] | **comfyui_controlnet_aux** | 线稿/深度预处理 |
| [ ] | **ComfyUI-Impact-Pack** | 修脸、细节 |

先别装旧包那一大堆（SUPIR/AlekPet 全家桶等）。

---

## D. 云端账号（视频/声音，ComfyUI 替代不了）

| 状态 | 账号 | 用途 | 优先级 |
|------|------|------|--------|
| [ ] | **可灵 Kling** | 图生视频（成片主力） | ★★★ |
| [ ] | **Suno** 或国内音乐 AI | 古风配乐 | ★★ |
| [ ] | 中文 TTS（讯飞/微软/海螺/ElevenLabs） | 旁白对白 | ★★ |
| [ ] | 爱给网 / Freesound | 雨声、脚步等音效 | ★ |

即梦/Liblib 网页端：可选，作风格对比；**正片静帧以本机新 ComfyUI 为准**。

---

## E. 建议下载顺序（今天）

```
1. 等 ComfyUI 下完 → 7-Zip 解压到 D:\AI\
2. 更新显卡驱动（若很久没更）
3. 装 Git、FFmpeg、剪映、Audacity
4. 启动新 ComfyUI → 装 Manager + 三个插件
5. 下载 SDXL 国风底模 + 水墨/工笔 LoRA
6. 出一张 16:9 冒烟图
7. 注册可灵（明天再深度用也行）
```

---

## F. 现在不必下的

- AnimateDiff 运动模（视频用可灵）
- 一堆写实摄影底模
- 旧包全量插件搬家
- 付费 PS（已有 Krita/Photopea 可暂缓）

---

完成 A+B+C 并成功出一张国风样张后，回：「新 ComfyUI 通了」。
