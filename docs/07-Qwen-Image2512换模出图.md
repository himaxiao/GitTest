# Qwen Image 2512：换国漫底模 + 出第一张图

适用：你已打开模板 **`Qwen Image 2512`**（**Node graph**，无 `API` 标签），画布上是**一体化节点**（左栏有 Model links，底部有 `unet_name` / `clip_name` / `vae_name` / LoRA）。

官方参考：https://docs.comfy.org/tutorials/image/qwen/qwen-image-2512

---

## 先说结论

| 你现在的情况 | 要做什么 |
|--------------|----------|
| 国漫底模放在 `models\checkpoints\` | **不够**：2512 模板的 `unet_name` 只扫 `diffusion_models\` |
| 模板是一体化节点 | **不用**再拖 `Load LoRA`；改节点里的下拉框即可 |
| CLIP / VAE | **先保持官方默认**，不要换成 SDXL 那套 |
| 第一次出图 | 先跑通官方/国漫 unet → 再换「美术电影」LoRA |

---

## 1. 文件必须放到这些目录

假设便携包在 `D:\AI\ComfyUI_windows_portable\`（按你实际路径改）：

```text
ComfyUI\models\
  diffusion_models\   ← 主模型（unet_name）
  text_encoders\      ← 文本编码器（clip_name）
  vae\                ← VAE（vae_name）
  loras\              ← LoRA（节点底部 LoRA 下拉）
```

### 你已下的「Qwen-国漫…」

从 `checkpoints` **复制或移动**到：

```text
...\ComfyUI\models\diffusion_models\
```

资源管理器操作，或 CMD：

```bat
mkdir "D:\AI\ComfyUI_windows_portable\ComfyUI\models\diffusion_models" 2>nul
copy /Y "D:\AI\ComfyUI_windows_portable\ComfyUI\models\checkpoints\你的国漫文件名.safetensors" "D:\AI\ComfyUI_windows_portable\ComfyUI\models\diffusion_models\"
```

（若 models 是联接到旧包的，改成联接目标里的同名路径。）

### 官方配套件（`clip_name` / `vae_name` 下拉里没有时必下）

| 文件 | 目录 |
|------|------|
| `qwen_2.5_vl_7b_fp8_scaled.safetensors` | `text_encoders\` |
| `qwen_image_vae.safetensors` | `vae\` |
| （可选）`qwen_image_2512_fp8_e4m3fn.safetensors` | `diffusion_models\` |
| （可选加速）`Qwen-Image-Lightning-4steps-V1.0.safetensors` 或模板写的 2512 Lightning | `loras\` |

模板左栏 **Model links** 可一键下；也可从 Hugging Face 的 Comfy-Org 拆件仓库下。

**4080 SUPER 建议：** 官方底模用 **fp8**（`qwen_image_2512_fp8_e4m3fn`）；bf16 更吃显存，非必须。

---

## 2. 打开正确模板（回顾）

1. 浏览器 `http://127.0.0.1:8188`
2. 左侧栏点 **Templates**
3. 顶部筛选点 **`Node graph`**（不要停在 All）
4. 搜索 `Qwen`
5. 打开 **`Qwen Image 2512`**（有 Text to Image，**没有** `API`）

不要点：`Qwen Image 3.0 Pro…`（API 云端）。

---

## 3. 在一体化节点里换模

从上往下改下拉框：

1. **`unet_name`**  
   - 选你的 **Qwen-国漫…**（须已在 `diffusion_models`）  
   - 列表没有 → 点界面刷新，或关黑窗口再开 `run_nvidia_gpu.bat`，浏览器 **Ctrl+F5**  
   - 仍没有 → 文件不在该目录，或不是该模板认的扩散权重

2. **`clip_name`**  
   - 保持：`qwen_2.5_vl_7b_fp8_scaled.safetensors`

3. **`vae_name`**  
   - 保持：`qwen_image_vae.safetensors`

4. **LoRA（最下面一行）**  
   - **第一次**：保留 Lightning / 或先不挂风格 LoRA，只求跑通  
   - **第二次**：改成 **美术电影** LoRA（文件在 `loras\`），强度约 **0.8**（若有强度滑条）

5. 大框提示词改成中文美影/聊斋句（见下）  
6. 分辨率先用 **1328×1328**，通后再改 **1664×928（16:9）**  
7. 点右上角蓝色 **Run**

---

## 4. 第一张测试提示词

```text
中国上影美影动画风格，天书奇谈气质，工笔勾线，平涂着色，
聊斋狐女，冷青夜色，烛火，水墨远山，电影静帧
```

负面：

```text
写实照片，3D渲染，霓虹，现代都市，网红脸，模糊，水印
```

成功后存到：

```text
02-visual-bible/角色_狐女_定妆_qwen_v01.png
```

（本机工程目录若尚未克隆本仓库，先建同名文件夹即可。）

---

## 5. 若 `unet_name` 里始终没有国漫 / 一点就报错

按优先级排查：

| 现象 | 处理 |
|------|------|
| 下拉里没有国漫文件名 | 确认在 `diffusion_models\`，重启 ComfyUI + Ctrl+F5 |
| 报找不到 clip / vae | 按第 1 节补官方 text_encoder + vae |
| 报 key missing / unexpected / 不是 unet | 该「国漫」可能是 **整包 checkpoint** 或旧版 Qwen 权重，**不能**直接塞进 2512 的 unet 槽 |
| 国漫不兼容 | `unet_name` 先选官方 **`qwen_image_2512_fp8_e4m3fn`**，风格靠提示词 + **美术电影 LoRA**；国漫文件先留着备用 |

把下面两样发助手即可精确定位：

1. 国漫**完整文件名**（含 `.safetensors`）  
2. 红字报错全文（或说明「下拉没有」）

---

## 6. 今天执行清单

1. [ ] 国漫文件已在 `models\diffusion_models\`
2. [ ] `text_encoders\` 有 `qwen_2.5_vl_7b_fp8_scaled.safetensors`
3. [ ] `vae\` 有 `qwen_image_vae.safetensors`
4. [ ] `loras\` 有美术电影 LoRA（可选加速 Lightning）
5. [ ] 打开 **Qwen Image 2512**（Node graph）
6. [ ] `unet_name` 选国漫或官方 fp8；clip/vae 保持官方
7. [ ] 先不加风格 LoRA 跑通 1328²
8. [ ] 再挂美术电影 @0.8，出定妆候选

完成后回：「Qwen 通了」或贴报错全文。
