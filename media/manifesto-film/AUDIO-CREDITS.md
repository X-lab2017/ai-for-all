# Conference v5 · 声音与音乐署名

用户重新选择 conference-v3 的平衡声音组合。本版保留 v3 的实际配音表演与 Heroic Age 配乐，仅将各章人声提高 10% 语速，并升级开场、片尾。

## 人声

- 原始声音：Microsoft AI 男声 `zh-CN-YunjianNeural`，复用 v3 已合成录音，没有重新选声或生成。
- 以 v3 完整人声母带逐章切分，FFmpeg `atempo=1.10` 保持音高。速度相对用户选定的 v3 成片增加 10%，不是相对 A v4。
- 保留原有均衡、压缩和声音处理。首章增加 0.45 秒音乐引入，其他章节起点保持一致；每章尾部补足至原时长。
- 旁白全文恢复为 v3，其中第九章包含“改变，就从我们开始”，第十章包含“加入 X-lab AI”。
- 原始合成接口及使用条件记录保留于 v3 提交 `8c20b95`；本版不扩大此前对服务使用权利的判断。

## 音乐

“Heroic Age” — Kevin MacLeod (incompetech.com)

Licensed under Creative Commons: By Attribution 4.0
https://creativecommons.org/licenses/by/4.0/

来源：https://incompetech.com/music/royalty-free/index.html?Search=Search&isrc=USUAN1100848

作者文件：https://incompetech.com/music/royalty-free/mp3-royaltyfree/Heroic%20Age.mp3

ISRC：USUAN1100848。

保留 v3 原曲 00:07–01:37 选段、均衡与分段电平。随提速后的人声重新计算侧链压低；音乐自身不加速。首 0.8 秒渐入，最后 1.5 秒渐出。采用两遍响度处理，目标 -16 LUFS、真峰值 -2 dBTP，48 kHz 立体声、24-bit 无损母带。

改动包含 excerpt / equalization / ducking / mix；署名和 CC BY 4.0 链接保留于影片末页及文件元数据，公开发布说明亦应保留。历史许可与平台识别记录见 v3 提交的 AUDIO-CREDITS.md。

## 字幕与验证

v3 已确认字幕依据相同的逐章 1.10 倍时间变换同步；保持文案和标点。字幕时长、章节边界、全片解码、视频帧数及成片响度经过检查。原始 v3 人声、字幕基准、当前母带及校验记录随本版音频归档交付。

制作入口：`source/prepare_conference.py`、`source/ceremony.js`、`source/render.js`、`source/mix_conference.py`。

此前 A v4 的声音记录保留于 [AUDIO-CREDITS-A-v4.md](AUDIO-CREDITS-A-v4.md)，其完整代码与文案版本为 `f179605`。

## 成片实测

90.000 秒，1920×1080，30fps，2700 帧；H.264 / AAC 48 kHz 立体声。成片 -16.01 LUFS、-1.86 dBTP、LRA 4.30 LU；完整媒体解码通过。23 条字幕，无重叠、无越界，最后一条结束于 85.25 秒。
