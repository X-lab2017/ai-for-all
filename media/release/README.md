# 正式发布包 Release 1

统一入口：https://www.x-lab.info/ai-for-all/launch/

English：https://www.x-lab.info/ai-for-all/launch/en.html

## 内容

- 已定稿 conference-v5 中文原片，按原始字节保留。
- 中文音轨与中文画面的中英双语字幕版，音轨与中文原片解码校验一致。
- 英文 AI 配音、英文画面与字幕的完整 90 秒影片。
- 中英文 10 页 PPT，英文版逐项翻译并保留可编辑结构与讲述备注。
- 中英文宣言 PDF、全景图、二维码 PNG/SVG 与会场投屏 PDF。
- 五页中英会场手册：主持人引入、约两分钟致辞、扫码邀请、术语、播放交接。
- SRT/VTT、署名、许可说明、校验值与完整离线 ZIP。

可直接交给会务团队使用的文件放在 `site/launch/downloads/`。发布包作为通用国际会议材料，不标注未确定的会议名、日期或举办方。

## 版本基准

中文影片：`e77fc4b` 中记录的 conference-v5。中文文稿为宣言 v1.1，仍为权威版本。

英文口语稿位于 `source/english-story.json`，逐章保持 8/8/9/8/9/9/12/8/7/12 秒。英文速度依据句长适配，不把中文 v3 的 10% 提速指标错误套用到新英文录音。

英文声音由本地 Qwen3-TTS Base 生成，以先前的合成人声为参考。模型 revision、参考哈希、种子和适配节奏分别记录在 `english-voice-provenance.json` 与 `english-timing.json`。

配乐延续 Heroic Age 和已定稿的递进方式。完整署名及原语音服务使用条件的待确认项见下载包 `CREDITS.txt` 与 `media/manifesto-film/AUDIO-CREDITS.md`。

## 构建

1. `python3 scripts/build_site.py` 生成宣言主站。
2. `python3 scripts/build_release.py` 生成中英文发布入口、打印版源页面与扫码投屏页面。
3. 使用 `source/build_handbook.py` 生成 Word，并用文档渲染工具导出与逐页检查 PDF。
4. 安装 `weasyprint` 及 Source Han Sans SC 字体，运行 `source/export_print.py` 导出宣言和投屏 PDF。浏览器备选为 `source/export_print.cjs`。
5. `python3 media/release/source/package_release.py` 生成字幕、署名、文件校验值与离线包。
6. `python3 scripts/check_release.py` 检查所有发布页资源、字幕、压缩包和扫码目标。

影片构建沿用 `source/render_release.js`、`source/prepare_en.py`、`source/align_en.py` 和 `source/mix_release.py`。音频源、模型权重与字体属于构建依赖，未随网站重复发布。为影片指定 `FILM_OUTPUT`，为英文声音处理指定 `RELEASE_BUILD`。英文 PPT 构建入口为 `source/build_deck_en.mjs`，依赖 Artifact Tool 和本仓库中文 PPT 参考文件。

## 检查结果

三片均完整解码通过：90 秒，1920×1080，30 fps，2700 帧，H.264 / AAC，48 kHz 立体声。

| 影片 | Integrated loudness | True peak | LRA |
|---|---:|---:|---:|
| 中文原片 | -16.01 LUFS | -1.86 dBTP | 4.30 LU |
| 中英字幕 | -16.01 LUFS | -1.86 dBTP | 4.30 LU |
| 英文影片 | -16.06 LUFS | -1.91 dBTP | 4.20 LU |

中英字幕保留原中文音轨。PPT 英文版检查了全部十页，文件结构、页面边界及再导入检查通过。现场播放前仍应在实际屏幕和扩声系统上完整试播。
