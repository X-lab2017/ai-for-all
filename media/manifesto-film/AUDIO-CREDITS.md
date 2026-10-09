# 声音设计与音乐署名 · v2

定位：面向国际公共事务发布场合，克制、可信、温暖。该版本为声音审听稿；不表示联合国制作、认可或背书。

## 人声

- AI 合成语音：Microsoft `zh-CN-YunyangNeural`，专业叙述方向。实际接口使用基础语音，并未启用 Azure 的专门 style 参数。
- 合成设置：rate -3%，pitch -3Hz；精简原稿，避免大幅加速。
- 处理：65Hz 高通，160Hz 轻微提升，300Hz 轻微衰减，轻压缩；不添加混响。
- 语音信息：https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts
- AI 语音不是指定真人的声音克隆。接口可用性与主观试听效果不是发布权利的证明；正式放映应由制作方核对所用语音服务及活动方的使用条件。

## 音乐

“Light Awash” — Kevin MacLeod (incompetech.com)

Licensed under Creative Commons Attribution 4.0:
https://creativecommons.org/licenses/by/4.0/

Source: https://incompetech.com/music/royalty-free/index.html?Search=Search&isrc=USUAN1100175

Official file: https://incompetech.com/music/royalty-free/mp3-royaltyfree/Light%20Awash.mp3

ISRC: USUAN1100175. 原作者标注 Bright / Uplifting / Relaxed，慢起音合成器氛围作品。

改动：选取原曲 00:30–02:00，淡入淡出、均衡、响度处理及旁白侧链压低。没有重新作曲。片尾保留作者、曲名、来源域名、许可证与编辑说明；发布说明也应保留上述完整署名。

音乐是按 CC BY 4.0 条件使用，并非公有领域、独家购买或无条件免署名作品。

## 混音

- 90 秒、立体声；旁白保持居中。
- 音乐轻铺底，人声出现时自动压低；句间缓慢恢复。
- 全片目标 -18 LUFS、真峰值不超过 -1.5 dBTP；实际 AAC 测量记录随版本保存。
- 片尾 4 秒音乐渐出，保留完整全景。

完整音乐文件不在本仓库重复分发；重建时从作者网站下载，并保留署名。

成片 AAC 实测：-18.60 LUFS，-1.75 dBTP，LRA 5.50 LU。
