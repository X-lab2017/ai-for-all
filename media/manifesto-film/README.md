# AI 普惠宣言 · 90 秒品牌宣言视频

**当前版本：conference-v5，基于用户重新选定的 conference-v3。** 保留 v3 的配音声线与 Heroic Age 配乐，人声相对 v3 加速 10%，开场与收场加入仪式感动效。

- 规格：1920×1080，30 fps，90 秒，H.264 / AAC 48 kHz 立体声。
- 开场：“AI 普惠宣言”作为最大视觉焦点；环形光轨与光点汇聚，随后呈现目标和愿景。
- 中段：保留已确认的八章内容、排版和动态图解，五家模型按既定顺序同等呈现。
- 收场：五个框架部分逐步组成全景，双轮以价值/支持双向连接，共同内核说明证据汇入与评价反馈；约最后 6 秒保留完整框架和共建邀请，最后 5 秒保持稳定。
- 人声：复用 v3 的 Microsoft AI 男声，统一 1.10 倍速度并保持音高，保留原稿及表演。
- 字幕：沿用 v3 已确认字幕，同步变换时间码，内嵌字幕并提供 SRT。
- 配乐及声音来源见 [AUDIO-CREDITS.md](AUDIO-CREDITS.md)。

## 十章节奏

| 宣言 | Linux | 开放模型 | 两股力量 | 公共品 | 数据与评价 | 双飞轮 | 实践基础 | 共建 | 全景 |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 8 秒 | 8 秒 | 9 秒 | 8 秒 | 9 秒 | 9 秒 | 12 秒 | 8 秒 | 7 秒 | 12 秒 |

总长仍为 90 秒。人声加速腾出的时间用于音乐与画面停留；开场额外保留 0.45 秒音乐引入。

## 复现

依赖：Node.js、`@napi-rs/canvas`、Python、FFmpeg、思源黑体。当前版本无需重新调用语音服务。

设置 `CODEX_PRIMARY_RUNTIME_NODE_MODULES` 为 Node 依赖目录；`FILM_OUTPUT` 指定统一工作目录（建议仓库相邻 `conference-v5-build`）；`FILM_FONT` 可指定字体。

1. 从随片音频归档恢复 `source-v3/narration.flac` 和 `source-v3/captions.json` 至工作目录。FLAC 保留 v3 原始人声母带采样，不使用成片中的配乐混音作语音来源。
2. 从归档或已署名的作者来源恢复 `Heroic-Age.mp3`，放入工作目录。
3. 运行 `python3 media/manifesto-film/source/prepare_conference.py`，逐章按 1.10 倍处理并生成旁白、字幕和时间校验记录。
4. 将 `site/presentation/assets/glm.svg` 用 CairoSVG 栅格化为工作目录的 `glm.png`（200×200）。
5. 运行 `node media/manifesto-film/source/render.js --preview` 检查静帧，可用 `PREVIEW_TIME=6` 指定每章取样时刻；移除 `--preview` 生成完整画面。
6. 运行 `python3 media/manifesto-film/source/mix_conference.py`，重新计算人声侧链与两遍响度，生成 24-bit WAV 母带及 `AI-for-All-90s-conference-v5.mp4`。

## 版本与交付

- v3：`8c20b95`，用户本轮重新选定的声音基准。
- A v4：`f179605`，历史声线与 Reign 配乐方案，完整重建须使用该提交对应的文案；[声音记录](AUDIO-CREDITS-A-v4.md)。
- conference-v5：v3 配音加速 10%、保留配乐，并升级开场与片尾。

素材许可沿用 [网页素材记录](../../site/presentation/assets/SOURCES.md)。动态图解是框架表达，不表示实时数据或已实现的普惠成效。成片通过对话交付。
