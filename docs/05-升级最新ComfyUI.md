# 升级到最新 ComfyUI（4080S · 旁路新装）

## 先说结论

**要升级，但不要在旧的 Photoshop 整合包里点“原地升级”。**

| 做法 | 建议 |
|------|------|
| 在 `D:\PS2025ComfyUI\...` 里硬升本体 | ❌ 容易把 Photoshop 联用、旧节点一起弄崩 |
| **另装一份官方最新便携包**，旧包先留着 | ✅ 推荐 |
| 用目录联接复用已有 `models` | ✅ 省下载、省空间 |

新版本通常更好：Flux/新节点兼容、采样与显存管理更优、安全与 Manager 更稳。  
你的旧包（2024-06）可以当备份；**国风短片日常改用新包。**

---

## 第 0 步：升级前检查（5 分钟）

1. **记下旧路径**（已有）  
   `D:\PS2025ComfyUI\PhotoshopComfyUIAI\App\Program Files\ComfyUI\`
2. **确认磁盘空间**：新便携包解压约 **2–4GB**，另加模型（可复用旧模型则几乎不占）
3. **更新 NVIDIA 驱动到较新版本**（官网 Game Ready / Studio）  
   新便携包常带较新 CUDA/PyTorch；驱动太旧可能启动失败
4. **关掉正在跑的旧 ComfyUI** 命令行窗口

---

## 第 1 步：下载官方最新 Windows 便携包

打开官方发布页（选 **NVIDIA** 版）：

- Releases：https://github.com/Comfy-Org/ComfyUI/releases  
  （或 https://github.com/comfyanonymous/ComfyUI/releases ）

**当前最新 NVIDIA 包直链示例（版本号会变，以 Releases 页为准）：**

```text
https://github.com/Comfy-Org/ComfyUI/releases/download/v0.37.0/ComfyUI_windows_portable_nvidia.7z
```

### 浏览器很慢 / 易断：改用命令行（推荐）

1. 在浏览器下载列表里 **取消** 未完成的下载  
2. 打开 **PowerShell** 或 **CMD**，先建目录：

```bat
mkdir D:\AI
cd /d D:\AI
```

3. **方案 A：Windows 自带 curl（可断点续传）**

```bat
curl.exe -L --retry 99 --retry-all-errors -C - -o ComfyUI_windows_portable_nvidia.7z "https://github.com/Comfy-Org/ComfyUI/releases/download/v0.37.0/ComfyUI_windows_portable_nvidia.7z"
```

断了再执行同一条命令即可从断点续传（`-C -`）。

4. **方案 B：aria2 多线程（通常比浏览器快很多）**

先安装 aria2（https://github.com/aria2/aria2/releases），把 `aria2c.exe` 加入 PATH 或放在当前目录，然后：

```bat
aria2c -c -x 16 -s 16 -k 1M -o ComfyUI_windows_portable_nvidia.7z "https://github.com/Comfy-Org/ComfyUI/releases/download/v0.37.0/ComfyUI_windows_portable_nvidia.7z"
```

`-c` 断点续传，`-x 16 -s 16` 多连接。

5. **GitHub 仍极慢时（国内常见）**  
   可换镜像前缀后再下（镜像站点会变，失效就换一个）：

```bat
curl.exe -L --retry 99 --retry-all-errors -C - -o ComfyUI_windows_portable_nvidia.7z "https://ghfast.top/https://github.com/Comfy-Org/ComfyUI/releases/download/v0.37.0/ComfyUI_windows_portable_nvidia.7z"
```

或使用你常用的 GitHub 加速器 / 代理后再跑方案 A/B。

下完用 7-Zip 看属性，大小应约 **1.8GB**（与发布页一致），再解压。

**4080 SUPER 下载哪个：**

| 文件名大致包含 | 是否选 |
|----------------|--------|
| `ComfyUI_windows_portable_nvidia.7z`（常规 NVIDIA，20 系及以上） | ✅ **首选** |
| `..._nvidia_cu128...` / 更新 CUDA 变体 | ✅ 也可（驱动够新时） |
| `..._cu126...` / 更旧 CUDA | 备选（新包起不来再试） |
| `..._amd...` / CPU only | ❌ 不要 |
| `...50XX...`（给 50 系） | ❌ 你是 40 系，别下错 |

用 **7-Zip** 解压到**无中文、无空格**路径，例如：

```text
D:\AI\ComfyUI_windows_portable\
```

解压后应能看到类似：

```text
D:\AI\ComfyUI_windows_portable\
  run_nvidia_gpu.bat
  update\
  ComfyUI\
  python_embeded\
  ...
```

若 Windows 拦截：右键 7z → 属性 → **解除锁定** 再解压。

---

## 第 2 步：先空启动一次（验证新环境）

1. 双击 `run_nvidia_gpu.bat`
2. 浏览器打开提示的地址（一般是 `http://127.0.0.1:8188`）
3. 看命令行是否出现类似：
   - `Device: cuda:0 NVIDIA GeForce RTX 4080 SUPER`
   - 无立刻崩溃

**验收：** 新 UI 能开、状态空闲。  
此时可能还没有你的旧模型——正常，下一步复用。

启动成功后先关掉（后面要做模型联接时更干净）。

---

## 第 3 步：复用旧模型（强烈建议，免重复下载）

### 方案 A：目录联接（推荐）

把**新包**的 `models` 指到**旧包**的 `models`（或你统一的模型库）。

1. 先备份：把新包里空的 `ComfyUI\models` 改名为 `models_bak_empty`
2. 以**管理员**打开 CMD，执行（路径按你实际改）：

```bat
mklink /J "D:\AI\ComfyUI_windows_portable\ComfyUI\models" "D:\PS2025ComfyUI\PhotoshopComfyUIAI\App\Program Files\ComfyUI\ComfyUI\models"
```

若旧包 models 路径不同，先在资源管理器里确认真实 `checkpoints` 所在目录再联接。

更干净的做法（长期推荐）：

```text
D:\AI\models\          ← 唯一模型库
  checkpoints\
  loras\
  controlnet\
  ipadapter\
  vae\
  ...
```

然后新旧 ComfyUI 的 `models` 都 `mklink /J` 到 `D:\AI\models`。

### 方案 B：只拷贝需要的

至少拷这些子目录到新包 `ComfyUI\models\`：

- `checkpoints\`
- `loras\`
- `vae\`
- `controlnet\`（若有）
- `ipadapter\` / `clip_vision\`（若有）

---

## 第 4 步：安装 ComfyUI-Manager（新包通常要补）

新便携包有的已带 Manager，没有就装：

```bat
cd /d D:\AI\ComfyUI_windows_portable\ComfyUI\custom_nodes
git clone https://github.com/ltdrdata/ComfyUI-Manager.git
```

或按官方/Manager 说明用便携包一键脚本。  
重启后侧边应有 **Manager**。

---

## 第 5 步：只装短片必需节点（别把旧包几十个全搬过来）

在 Manager → Install 搜索安装：

| 优先级 | 节点 | 用途 |
|--------|------|------|
| ★★★ | ComfyUI-Manager | 已装 |
| ★★★ | ComfyUI_IPAdapter_plus | 锁角色 |
| ★★★ | comfyui_controlnet_aux | 线稿/深度预处理 |
| ★★ | ComfyUI-Impact-Pack | 修脸/细节 |
| ★★ | ComfyUI-VideoHelperSuite | 视频辅助（可选） |
| ★ | rgthree-comfy / essentials | 工作流体验 |

**先不要**一次性安装旧包里的 SUPIR、art-venture、AlekPet 全家桶——那是启动变慢的主因。  
Photoshop 联用节点（`Comfy-Photoshop-SD`）只在你还要用 PS 插件时再装，并可继续用**旧包**专门给 PS。

装完重启，按红字把缺失的 **IP-Adapter / ControlNet 模型**下齐。

---

## 第 6 步：更新 ComfyUI 本体（以后日常升级用这个）

便携包一般自带更新脚本，常见位置：

```text
D:\AI\ComfyUI_windows_portable\update\update_comfyui.bat
```

或：

```text
update_comfyui_and_python_dependencies.bat
```

**习惯：** 每周或开工前跑一次 update，再启动。  
不要与旧 Photoshop 包混用同一套乱改的 `python_embeded`。

---

## 第 7 步：新环境冒烟验收

对照 `tools/check_env.md`，在**新包**上完成：

- [ ] `nvidia-smi` / 日志里仍是 4080 SUPER  
- [ ] 能选到 SDXL 国风底模（不要用 `maginMixReal` 做正片）  
- [ ] 16:9（如 1344×768）出一张水墨/工笔样张  
- [ ] IP-Adapter 或垫图锁脸出第二角度  
- [ ] 命令行里 ComfyUI 日期/版本明显新于 `2024-06-25`

通过后，旧包可保留但**日常只开新包**。桌面建快捷方式：

```text
D:\AI\ComfyUI_windows_portable\run_nvidia_gpu.bat
```

命名：`ComfyUI 新版-国风短片`

---

## 新旧怎么分工

| 用途 | 用哪个 |
|------|--------|
| 国风短片静帧、定妆、分镜 | **新便携包** |
| Photoshop 插件联用（若你还用） | 旧 `PS2025ComfyUI` 包 |
| 图生视频成片 | 仍然 **可灵**（两边都一样） |

---

## 常见问题

### Q：新的一定全面优于两年前吗？
**对你这项目：是。** 尤其 SDXL/Flux 工作流、新节点、显存与采样效率。  
唯一代价是要重装精简插件集、旧工作流可能缺节点（Manager 一键补即可）。

### Q：能不能直接覆盖旧目录升级？
不建议。Photoshop 整合包路径深、节点杂、Python/Torch 被钉死，覆盖后难回滚。旁路新装可随时切回旧包。

### Q：启动报 CUDA / torch 错？
1. 更新显卡驱动后重启  
2. 换下载页另一个 CUDA 变体的 portable（如 cu126）  
3. 把报错全文发我

### Q：端口 8188 被旧包占用？
先关旧命令行；或新包启动参数改端口（高级）。

---

## 今天执行清单（复制打勾）

1. [ ] 更新 NVIDIA 驱动  
2. [ ] 下载 `ComfyUI_windows_portable_nvidia` 并解压到 `D:\AI\`  
3. [ ] `run_nvidia_gpu.bat` 空启动成功  
4. [ ] `mklink /J` 复用 models（或拷贝 checkpoint/lora）  
5. [ ] 安装 Manager + IPAdapter + ControlNet aux + Impact  
6. [ ] 国风 SDXL 出一张 16:9 样张  
7. [ ] 回我：「新 ComfyUI 通了」

完成后进入：换国风底模定妆 → 故事核/分镜。
