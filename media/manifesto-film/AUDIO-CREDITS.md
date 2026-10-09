# A v4 完整影片 · 声音与音乐署名

用户选择 25 秒试听中的 A“庄严磅礴”，并要求语速加快约 15%。本版保持原有 90 秒画面和十章顺序，仅更新人声、配乐、字幕与署名。

## 人声

- A 版为 Qwen3-TTS VoiceDesign 生成的原创 AI 男声，无指定真人参考。
- 前八章采用 `Qwen/Qwen3-TTS-12Hz-1.7B-Base`，以获选 A 版录音为参考在本地延展音色；最后两章直接切分使用获选录音。
- Base 模型 revision：`fd4b254389122332181a7c3db7f27e918eec64e3`。
- 参考录音 SHA-256：`2c9c48caf95b73145b20001e31c32a90dc5dad030be0418970bd6141e374a25a`。
- 官方流程：https://github.com/QwenLM/Qwen3-TTS （Voice Design then Clone；代码及模型 Apache 2.0）。
- 本轮 `qwen-tts 0.1.1`、`transformers 4.57.3`、`torch 2.14.1`，CPU / BF16 / SDPA，8 线程。逐章固定种子 `20261009 + 章节编号`，归档原始录音以便精确重建。
- 全部人声使用 FFmpeg `atempo=1.15` 加速，保持音高。没有额外加速来挤压章节；每章保留 0.28 秒引入及适量音乐留白。
- 轻度均衡、压缩和响度处理；中心声像，不加人声混响。

## 音乐

“Reign” — Kevin MacLeod (incompetech.com)

Licensed under Creative Commons: By Attribution 4.0
https://creativecommons.org/licenses/by/4.0/

来源：https://incompetech.com/music/royalty-free/index.html?Search=Search&isrc=USUAN1100373

作者文件：https://incompetech.com/music/royalty-free/mp3-royaltyfree/Reign.mp3

作者许可页：https://incompetech.com/music/royalty-free/licenses/

ISRC：USUAN1100373。延续 A 版获选配乐，将其钢琴引入与管弦强段编辑为完整的 90 秒结构。

- 第一段：原曲 01:24–02:20（56 秒）。
- 第二段：原曲 01:44–02:20（36 秒）。
- 两段用 2 秒交叉淡化连接，总长 90 秒；首尾淡化，最后 2 秒收束。
- 音乐在影片约 26 秒、60 秒两次进入管弦强段，配合行动机制与后半段邀请。
- 编辑包含选段、交叉淡化、均衡、人声侧链压低、混音、响度处理及首尾淡化。
- 片尾和文件元数据包含署名、许可及改动标记；公开发布时将以上署名一并保留于发布说明。音乐不属于本仓库自有原创素材。

## 字幕和校验

- 按实际加速后的语音识别时间戳，对齐经确认的原稿意群；识别拼写不直接替换原文。
- 人名、模型名、项目名及中文同音词单独核对转写差异。字符匹配用于估算字幕边界，不是音素级强制对齐。
- 检查十章字幕的顺序、边界与时长，检查结尾全景和署名；以原始音频校验及最终媒体解码、时长和响度测量作技术验证。
- 感染力和会场效果仍以用户审听为准。

音频原始片段、参考音色、完整人声、24-bit 无损混音及校验记录随片归档；制作脚本位于 `source/voice_a.py`、`prepare_a.py`、`align_a.py`、`mix_a.py`。

## 最终文件实测

90.000 秒，1920×1080，30fps，H.264 / AAC 48 kHz 立体声。成片 -16.03 LUFS、-1.97 dBTP、LRA 5.20 LU；完整媒体解码通过。27 条字幕，无重叠、无超出片长，最后字幕结束于 87.86 秒。
