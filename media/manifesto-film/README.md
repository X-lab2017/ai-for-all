# AI 普惠宣言 · 90 秒品牌宣言视频

以十章互动演示为叙事基础，为 16:9 视频重新排版，移除网页导航与操作提示。

- 规格：1920×1080，30 fps，90 秒，H.264 / AAC。
- 语音：中文 AI 合成男声 `zh-CN-YunjianNeural`，非真人录音。
- 字幕：依据语音词组时间戳估算自然断句位置，画面内嵌字幕，另存 SRT。
- 风格：统一暗绿底、暖白文字、青绿强调；核心双轮与全景保留；五家模型同等呈现。
- 结尾：最后 5 秒完整框架停留，保留 GitHub 参与入口。
- 音频：v3 大会宣言男声与管弦打击乐配乐，详见 [声音与署名](AUDIO-CREDITS.md)。

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

视频按实际配音重分配时长，与网页总长相同。v3 改写为宣言式短句，增加行动号召；多数片段不变速，少数约 1.09 倍适配。

## 复现

依赖：Node.js、`@napi-rs/canvas`、Python `edge-tts` / `cairosvg`、FFmpeg，以及思源黑体。

设置 `CODEX_PRIMARY_RUNTIME_NODE_MODULES` 为 Node 依赖目录；可用 `FILM_OUTPUT` 指定工作目录，用 `FILM_FONT` 指定字体文件。默认输出到仓库相邻 `video-build`。

1. `python3 media/manifesto-film/source/voice.py`：生成逐章配音、对齐时间戳和归一化旁白。
2. `python3 media/manifesto-film/source/align.py`：保留原稿标点，生成自然断句字幕（词组内部的句段边界为插值估算）。
3. 将 `site/presentation/assets/glm.svg` 使用 CairoSVG 栅格化为输出目录中的 `glm.png`（200×200），保留其 SVG 样式。
4. `node media/manifesto-film/source/render.js --preview`：检查十章静帧。
5. `node media/manifesto-film/source/render.js`：生成无声画面。
6. 按 `AUDIO-CREDITS.md` 从作者网站下载 `Heroic-Age.mp3` 至工作目录；执行 `python3 media/manifesto-film/source/mix.py`，生成带配乐的 H.264/AAC MP4。

素材和许可说明沿用 [网页素材记录](../../site/presentation/assets/SOURCES.md)。品牌、Linux 周年图片与模型标识归各自权利人所有，不代表合作或背书。动态图解不表示实时数据或已实现的普惠成效。

成片通过对话交付，尚未向 B 站、YouTube 等平台投稿。
