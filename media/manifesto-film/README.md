# AI 普惠宣言 · 90 秒品牌宣言视频

以十章互动演示为叙事基础，为 16:9 视频重新排版，移除网页导航与操作提示。

**当前版本：A v4。** 用户选定“庄严磅礴”并要求语速加快约 15%。全片采用同一 A 版原创 AI 声线，语音统一按 1.15 倍速度处理并保持音高。已选中的结尾录音直接复用。A/B 阶段见 [试听记录](AUDIO-AUDITIONS.md)。

- 规格：1920×1080，30 fps，90 秒，H.264 / AAC。
- 语音：Qwen3-TTS 原创 AI 男声 A，基于用户选定的合成录音延展全片。
- 字幕：依据加速后音频的识别时间戳对齐原稿意群，画面内嵌字幕，另存 SRT。
- 风格：统一暗绿底、暖白文字、青绿强调；核心双轮与全景保留；五家模型同等呈现。
- 结尾：最后 5 秒完整框架停留，保留 GitHub 参与入口。
- 音频：A v4 庄严男声与 Reign 管弦配乐，详见 [声音与署名](AUDIO-CREDITS.md)。

## 视频节奏

| 章节 | 秒数 |
| --- | ---: |
| 宣言 | 8 |
| Linux | 8 |
| 开放模型 | 9 |
| 两股力量 | 8 |
| 公共品 | 9 |
| 数据与评价 | 9 |
| 双飞轮 | 12 |
| 实践基础 | 8 |
| 共建 | 7 |
| 全景 | 12 |

视频按实际配音重分配时长，与网页总长相同。A v4 全部人声以 1.15 倍速度处理；保持原有十章画面时序，并用音乐和留白承接加速后释放出的空间。

## 复现

依赖：Node.js、`@napi-rs/canvas`、Python `qwen-tts` / `numpy` / `soundfile` / `faster-whisper` / `opencc-python-reimplemented` / `cairosvg`、FFmpeg，以及思源黑体。

设置 `CODEX_PRIMARY_RUNTIME_NODE_MODULES` 为 Node 依赖目录；用 `FILM_OUTPUT` 指定统一工作目录（建议仓库相邻 `final-a-build`），用 `FILM_FONT` 指定字体文件。

1. 从随片音频归档恢复 `reference-A.wav` 及 `raw-01.wav` 至 `raw-10.wav`。这些原始片段是精确重建当前声音的依据。
2. 若需重新合成：下载 `Qwen/Qwen3-TTS-12Hz-1.7B-Base` 至工作目录的 `qwen-base-model`，revision `fd4b254389122332181a7c3db7f27e918eec64e3`；运行 `python3 media/manifesto-film/source/voice_a.py`。脚本使用本地 CPU / BF16 / SDPA，复用 A 版合成参考，跳过已保留片段。不同环境重新合成可能有差异。
3. `python3 media/manifesto-film/source/prepare_a.py`：所有人声统一 1.15 倍速度，保持音高，排入原 90 秒时序。
4. `python3 media/manifesto-film/source/align_a.py`：识别实际音频，核对转写，再将原稿意群对齐为字幕。查看 `speech-review.json`；字符匹配并非音素级强制对齐。
5. 将 `site/presentation/assets/glm.svg` 使用 CairoSVG 栅格化为工作目录中的 `glm.png`（200×200），保留 SVG 样式。
6. `node media/manifesto-film/source/render.js --preview`：检查静帧；移除 `--preview` 生成完整无声影片。
7. 按 [声音与署名](AUDIO-CREDITS.md) 从作者网站下载 `Reign.mp3`；运行 `python3 media/manifesto-film/source/mix_a.py` 生成 24-bit 无损混音和完整 MP4。

旧版 `voice.py` / `align.py` / `mix.py` 作为 v3 制作记录保留；A v4 使用上面的 `_a.py` 流程。

素材和许可说明沿用 [网页素材记录](../../site/presentation/assets/SOURCES.md)。品牌、Linux 周年图片与模型标识归各自权利人所有，不代表合作或背书。动态图解不表示实时数据或已实现的普惠成效。

成片通过对话交付，尚未向 B 站、YouTube 等平台投稿。
