# Comfy Desktop：从便携网页端迁移 / 关联

> 目标：**桌面端与便携端共用同一套模型**，工作流可导入；不要复制两份大模型。  
> 假设便携包模型根目录为：  
> `D:\AI\ComfyUI\ComfyUI_windows_portable\ComfyUI\models`  
> 若你的路径不同，改脚本里的 `$PortableModels` 即可。

---

## 0. 两者关系（先搞清）

| | 便携网页端 | Comfy Desktop |
|--|------------|---------------|
| 启动 | 运行 `.bat` → 浏览器 `127.0.0.1:8188` | 桌面应用 |
| 模型默认位置 | 便携包内 `ComfyUI\models\` | 首次安装时你选的 **basePath** |
| 额外路径配置 | `ComfyUI\extra_model_paths.yaml` | `%APPDATA%\ComfyUI\extra_models_config.yaml` |
| 自定义节点 | 便携包 `custom_nodes\` | basePath 下 `custom_nodes\` |

**推荐策略：** 模型只保留一份（便携包里已下好的）；Desktop 用配置 **挂载** 过去。工作流 JSON 复制或 Load。一次只开一个 Comfy，避免抢 4080S 显存。

---

## 1. 安装 Desktop 时注意

1. 「启用中国镜像」：在国内建议 **启用**（有 VPN 也可启）。  
2. 文件存储位置（basePath）：可仍选例如 `D:\AI\ComfyUI\DesktopData`，**模型不必再下**。  
3. 装完先能进主界面即可，再做下面关联。

---

## 2. 关联模型（推荐：改 YAML，不拷贝）

### 2.1 打开配置文件

资源管理器地址栏进入：

```text
%APPDATA%\ComfyUI\
```

编辑（建议先复制一份备份）：

```text
extra_models_config.yaml
```

也可在 Desktop：**设置 → 相关路径 / Extra Model Paths**（若版本有入口）打开同一文件。

### 2.2 追加便携包路径（保留文件里原有段落，只追加）

把下面整块贴到文件 **末尾**（路径按你本机修改）：

```yaml
# ===== 关联便携版已有模型（勿删上面 Desktop 默认段）=====
portable_shared:
    base_path: D:\AI\ComfyUI\ComfyUI_windows_portable\ComfyUI\
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
    # 若要把便携端自定义节点也挂过来，取消下一行注释（可能有版本冲突，慎用）
    # custom_nodes: custom_nodes/
```

保存后 **完全退出并重启 Comfy Desktop**。

### 2.3 验收

在 Desktop 里打开任意 `Load Diffusion Model` / `Load Checkpoint` / `Load LoRA`：

- [ ] 能看到 Qwen / 国漫 / Wan 相关文件  
- [ ] 能看到美术电影 LoRA  
- [ ] 能看到 `qwen_image_vae`、`wan2.2_vae`、`umt5…`、`qwen_2.5_vl…`

没有 → 检查 `base_path` 是否指向带 `models` 的那层 `ComfyUI\` 目录，反斜杠与缩进是否为 YAML 合法空格。

---

## 3. 一键脚本（可选）

仓库提供：`tools/link_comfy_desktop_models.ps1`

**以管理员打开 PowerShell**（若只用 YAML 追加，普通权限即可跑「生成配置片段」）：

```powershell
cd D:\AI\guofeng
git pull origin cursor/guofeng-animation-pipeline-d13b

# 预览将写入的 YAML 片段
powershell -ExecutionPolicy Bypass -File .\tools\link_comfy_desktop_models.ps1 -PortableRoot "D:\AI\ComfyUI\ComfyUI_windows_portable\ComfyUI"

# 自动备份并追加到 Desktop 配置（推荐）
powershell -ExecutionPolicy Bypass -File .\tools\link_comfy_desktop_models.ps1 -PortableRoot "D:\AI\ComfyUI\ComfyUI_windows_portable\ComfyUI" -Apply
```

然后重启 Desktop。

---

## 4. 工作流迁移

便携端保存的 workflow（JSON）常见位置：

```text
D:\AI\ComfyUI\ComfyUI_windows_portable\ComfyUI\user\default\workflows\
```

或你手动另存的目录。

操作：

1. 复制 `.json` 到 Desktop 的 workflows 目录（在 basePath 下，或 Desktop 的 Open Workflow）  
2. 或直接 **Load** / 拖进画布  
3. 打开后检查：模型下拉是否仍能选中同名文件（关联成功则一般不用改）

建议在工程仓库也留一份：

```text
workflows/
  qwen_t2i_handbuild.json
  wan22_i2v_stable.json
```

（从本机导出后放入，便于版本管理。）

---

## 5. 输出与输入目录（建议）

| 用途 | 建议路径 |
|------|----------|
| 工程关键帧 | `D:\AI\guofeng\04-keyframes\` |
| 工程动画条 | `D:\AI\guofeng\05-animation\` |
| Comfy 临时 output | 仍可用各端默认 `output\`，出片后 **改名拷进工程目录** |

避免只堆在 Comfy `output` 里不管。

---

## 6. 自定义节点

- **先不整包联接** `custom_nodes`（版本差易炸）。  
- Desktop 需要的节点（如以后 SAM2、LivePortrait）：在 Desktop 的管理器里 **按需重装**。  
- Phase A（Qwen+Wan 手搭）通常 **核心已自带**，可不迁节点。

---

## 7. 迁移检查清单

- [ ] `extra_models_config.yaml` 已备份  
- [ ] 已追加 `portable_shared` 段并重启  
- [ ] Desktop 能选到 Qwen / Wan / LoRA / VAE / text encoder  
- [ ] 手搭 Qwen 工作流在 Desktop 跑通 1 张图  
- [ ] Wan I2V 能 Load 到定妆图并出 1 段  
- [ ] 确认同时只开 Desktop **或** 便携端其中一个  

---

## 8. 出问题怎么办

| 现象 | 处理 |
|------|------|
| 下拉仍空 | 路径层级多/少一层 `ComfyUI`；或 YAML 缩进用了 Tab |
| 重名模型两份 | 正常（默认库+挂载库）；选便携包那份即可 |
| 显存不足 | 关掉另一个 Comfy；降分辨率/batch |
| 想撤销 | 用备份还原 `extra_models_config.yaml` |

---

## 版本

- v01 · Desktop 关联便携模型 + 工作流迁移要点
