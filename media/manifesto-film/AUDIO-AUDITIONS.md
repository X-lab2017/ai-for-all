# 结尾声音 A/B 试听 · 2026-10-09

**选型结果：** 用户已选择 A“庄严磅礴”，要求语速加快约 15%；已据此制作完整 A v4 影片，见 [当前制作说明](README.md)。以下保留试听阶段的制作记录。

视觉已获用户认可，本轮专门选择配音与配乐方向。两版均为 25 秒、同一文案、同一完整全景静帧，保留约 2.7 秒音乐收束。样片通过对话交付，尚未替换 v3 的 90 秒影片。音乐和人声均同时变化，比较的是完整声音方向，而非单一变量实验。

| 版本 | 配音指导 | 配乐与剪辑 |
| --- | --- | --- |
| A · 庄严磅礴 | 成熟、浑厚、稳健，逐层加强宣言与行动邀请 | Kevin MacLeod《Reign》，原曲 01:41.2–02:06.2；钢琴引入，管弦强段在“让技术”附近进入 |
| B · 昂扬共创 | 温暖明亮、真诚而昂扬，突出共同参与 | Kevin MacLeod《Americana》，原曲 02:35–03:00；使用后段管弦推进与高潮 |

以上是制作方向。感染力、自然度和大会适配度由用户审听选择，不以响度数值替代听感判断。

## 统一文案

分享一个需要，贡献一个工具，开放一个场景。
让技术，成为机会！
让创造，惠及更多人！
加入我们。
现在——就一起行动！

## 配音与剪辑

- 改用 Qwen3-TTS-12Hz-1.7B-VoiceDesign，通过 Qwen 官方公开演示 API 生成两种原创 AI 男声。未指定或模仿真人。
- 模型通过自然语言接受音色、情绪和韵律指令；完整指令保存在 `source/audio_ab.py`。
- 模型说明：https://huggingface.co/Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign （模型许可 Apache 2.0）。
- 演示：https://huggingface.co/spaces/Qwen/Qwen3-TTS 。公开演示的可用性和生成结果不保证固定。
- 以实测静音处切分八个意群，统一入点为 1.0 / 3.4 / 5.8 / 8.3 / 12.2 / 16.5 / 19.0 / 20.7 秒。不变调、不变速。
- 原始配音及最终 48 kHz / 24-bit 立体声无损混音随试听交付归档。原始片段用于保留音色和本轮编辑结果；重新合成后必须重新检查切点。
- A 原始声音 SHA-256：`2c9c48caf95b73145b20001e31c32a90dc5dad030be0418970bd6141e374a25a`。
- B 原始声音 SHA-256：`bb6d284b90a8dc9eae30996771a26f665a7a383d08aac9e9cf6517b65993427f`。

## 配乐来源与署名

“Reign” / “Americana” — Kevin MacLeod (incompetech.com)

Licensed under Creative Commons: By Attribution 4.0
https://creativecommons.org/licenses/by/4.0/

- Reign，ISRC USUAN1100373：https://incompetech.com/music/royalty-free/index.html?Search=Search&isrc=USUAN1100373
- Americana，ISRC USUAN1200092：https://incompetech.com/music/royalty-free/index.html?Search=Search&isrc=USUAN1200092
- 作者许可页：https://incompetech.com/music/royalty-free/licenses/
- 作者文件：https://incompetech.com/music/royalty-free/mp3-royaltyfree/Reign.mp3
- 作者文件：https://incompetech.com/music/royalty-free/mp3-royaltyfree/Americana.mp3

两版均进行了选段、均衡、人声侧链压低、混音和淡入淡出；样片画面及文件元数据保留署名与改动标记。发布时保留曲名、作者、来源、许可链接和改动说明。音乐不属于本仓库自有原创素材。

此前候选 Titan / In Dreams 因来源站下载被拦截，未用于交付样片。

## 校验与复现

- A 成片：25 秒，1920×1080 / 30fps，AAC 48 kHz 立体声，-16.27 LUFS，-1.96 dBTP，LRA 4.8 LU。
- B 成片：同规格，-16.01 LUFS，-3.33 dBTP，LRA 7.9 LU。
- 使用本地语音识别核对原始音频的意群与完整性；同音词“惠及”被识别成“汇集”，字幕依据授权原稿保留“惠及”。机器校验不替代人工审听。
- 抽帧检查全景、字幕、版本标识和音乐署名；媒体容器及音频测量通过。

设置 `FILM_OUTPUT` 为素材目录，依赖 Python `gradio_client` / `numpy`、FFmpeg 及现有 Canvas 渲染环境。完整复现当前样片时，使用归档的 `voice-A-raw.wav`、`voice-B-raw.wav`，从作者页面获取 `Reign.mp3`、`Americana.mp3`。

1. 依照主 README 准备 `glm.png`，运行 `source/render.js --preview` 生成已有全景 `scene-10.png`。
2. `python3 media/manifesto-film/source/audio_ab_mix.py`：重建旁白时序及两遍响度处理的无损混音。
3. `node media/manifesto-film/source/audio_ab_preview.js`：生成两版试听 MP4。

若需重新设计音色，再运行 `source/audio_ab.py`。这个步骤不会覆盖现有原始音频；新合成片段需要重新测量和编辑，不能直接沿用本轮固定切点。

该阶段的声音选型已完成；后续 90 秒影片采用 A 声线和 Reign 配乐，统一加速 15%。
