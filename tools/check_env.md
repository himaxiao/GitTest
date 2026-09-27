# 环境自检（人工）· 4080S 路线

按顺序执行，全部通过即可进入剧本阶段。

## A. 本机 GPU / ComfyUI

1. [ ] `nvidia-smi` 显示 RTX 4080 SUPER
2. [ ] ComfyUI 能启动（`http://127.0.0.1:8188`）
3. [ ] SDXL 底模可出图；已加载至少 1 个国风/水墨 LoRA
4. [ ] IP-Adapter 或垫图能锁同一角色出 2 个角度
5. [ ] 16:9 尺寸出图成功（如 1344×768）

## B. 成片链路

6. [ ] 用 `prompts/00-冒烟测试.md` 出 1 张角色定妆图，归档 `02-visual-bible/`
7. [ ] 可灵上传该图，生成 1 段 4s 视频，归档 `05-animation/`
8. [ ] 剪辑软件导入并导出 MP4 到 `08-export/_smoke/`
9. [ ] Audacity 能打开 WAV/MP3
10. [ ] （可选）`ffmpeg -version` 有输出

## C. 风格锚定

11. [ ] `docs/02-天书奇谈风格圣经.md` 已填写视觉三支柱
12. [ ] `refs/` 至少 10 张参考图

通过后开始填写 `01-script/故事核模板.md`。  
专项安装步骤：`docs/03-RTX4080S本机安装手册.md`。
