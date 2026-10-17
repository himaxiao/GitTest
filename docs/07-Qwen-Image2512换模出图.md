# Qwen-Image 2512：现阶段可跑通的换模方法（修正版）

> 适用：Unpack 之后出现 `Load Diffusion Model` / `Load CLIP` / `Load VAE` / `Load LoRA`，  
> 但 **下拉点不开、只能接线**，小圆点右键也没有 Convert。

这是新版前端 + 子图/控件的常见坑，**不是你操作错了**。不要再找 COMBO 节点硬连。

---

## 结论先说

| 目标 | 现阶段正确做法 |
|------|----------------|
| 先出第一张天书奇谈风图 | **保留官方** `qwen_image_2512_fp8…` 作底；用 **属性面板** 把 LoRA 换成「美术电影」@0.8；改提示词后 Run |
| 换国漫底模 | 用右侧 **Properties Panel** 填/选文件名；且文件必须在 `diffusion_models\` |
| Liblib「国漫大模型」 | 未必能当 2512 的 diffusion 权重用；不通就放弃硬换 unet，**风格交给美术电影 LoRA** |

官方模板本身认的是这些文件（见 [官方文档](https://docs.comfy.org/tutorials/image/qwen/qwen-image-2512)）：

```text
models/diffusion_models/qwen_image_2512_fp8_e4m3fn.safetensors
models/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors
models/vae/qwen_image_vae.safetensors
models/loras/…（Lightning 或你的美术电影）
```

你截图里 **CLIP / VAE / 官方 fp8 已经对上了**——先别拆这条链。

---

## 方法 A（推荐）：右侧属性面板改模型 / LoRA

社区对「子图里下拉选不了」的可行绕过：

1. **左键单击**选中节点（例如 `Load LoRA` 或 `Load Diffusion Model`）  
2. 打开右侧 **Properties / 属性面板**  
   - 右键节点 → **Properties Panel**  
   - 或点界面右侧栏 / 按常见快捷键打开属性  
3. 在面板里找到模型名 / LoRA 名相关字段  
4. **在面板里选择或粘贴完整文件名**（不要在画布下拉上死磕）

### 你现在该改什么

**`Load Diffusion Model`（可先不动）**

- 保持：`qwen_image_2512_fp8_e4m3fn.safetensors`  
- 只有当你确认国漫文件已在 `diffusion_models\` 且属性面板能选到时，再改国漫名  

**`Load CLIP` / `Load VAE`**

- 一律保持官方，不要换  

**`Load LoRA`（重点）**

- 属性面板里把文件改成你的 **美术电影** `.safetensors`  
- `strength_model` = **0.8**  
- 第一次若怕翻车：先把 strength 设 **0** 跑通，再改 0.8、再换文件名  

**提示词**

- 在 Prompt 组的 `CLIP Text Encode` 里改中文美影句（或同样用属性面板改 text）

然后点 **Run**。

---

## 方法 B：键盘刷新模型列表后再试属性面板

模型是新拷进文件夹的时：

1. 确认文件在正确目录（见上）  
2. 画布上按 **`R`** 刷新节点定义，或重启 `run_nvidia_gpu.bat`  
3. 再回到方法 A 用属性面板选  

ComfyUI **不会**在运行中自动发现新文件。

---

## 方法 C：官方 JSON 重来一遍（画布已经拧巴时）

1. 打开官方说明页的 Workflow JSON：  
   https://docs.comfy.org/tutorials/image/qwen/qwen-image-2512  
2. 把 JSON **拖进** ComfyUI 画布  
3. 用模板自带 **Model links** 把缺的官方 fp8 / clip / vae 下齐  
4. **不要 Unpack、不要从控件往外拖线**  
5. 选中子图或内部节点 → **只通过右侧属性面板** 改 LoRA 为美术电影、改提示词  
6. Run  

---

## 关于「国漫底模」要有心理预期

- 2512 模板的 `Load Diffusion Model` 吃的是 **Qwen-Image 2512 扩散权重**（官方命名那套）  
- Liblib 的「Qwen-国漫…大模型」若是另一套封装 / 旧版 Qwen / 整包 checkpoint，**放进 `checkpoints` 或硬塞 unet 都会选不了或一跑就报错**  
- **可持续做法：**  
  - 底：官方 `qwen_image_2512_fp8`  
  - 风：美术电影 LoRA @0.8  
  - 词：天书奇谈提示词 + refs 参考  

等第一张图稳定后，再单独验证国漫是否出现在属性面板的模型列表里。

---

## 今天唯一验收标准

1. [ ] `Load Diffusion Model` = 官方 fp8（已有即可）  
2. [ ] CLIP / VAE = 官方（已有即可）  
3. [ ] **属性面板** 把 LoRA 换成美术电影，强度 0.8（或先 0 跑通）  
4. [ ] 提示词改成美影/聊斋  
5. [ ] Run 出一张图  

成功回：「属性面板通了」。  
若属性面板里也没有 LoRA/模型列表：发 **Properties 面板截图** + 国漫/美术电影的**完整文件名**。
