# AI 普惠宣言 · 十章互动演示

线上地址：https://www.x-lab.info/ai-for-all/presentation/

1. **AI 普惠宣言** · 6 秒
2. **Linux 35 年** · 8 秒
3. **开放模型** · 8 秒
4. **两股力量** · 9 秒
5. **公共品路径** · 10 秒
6. **数据与评价** · 10 秒
7. **两个飞轮** · 12 秒
8. **实践基础** · 8 秒
9. **参与共建** · 7 秒
10. **全景与邀请** · 12 秒

开放模型统一使用：阿里巴巴（Qwen）、深度求索（DeepSeek）、智谱 AI（GLM）、月之暗面（Kimi）、腾讯（混元 / Hunyuan）。点击卡片访问官方项目，版本为代表性示例，各版本许可分别适用。

## 演讲与探索

- 选择底部章节，或使用左右方向键；Home / End 跳至首章 / 末章。
- 点击公共品路径、评价工作、飞轮节点与全景要素，查看解释。
- 桌面支持全屏演讲，F 切换全屏。
- “90 秒导览”完整播放十章，无配音；可暂停、继续和重播。
- “暂停动效”独立控制图解动画。系统偏好减少动态效果时默认关闭循环动效。
- 页面进入后台会暂停导览计时；打开来源或讲述稿时暂停导览。
- “讲述稿”显示本章旁白与现场提示，提供[完整稿件下载](narrative.md)。
- 手机采用纵向布局和章节选择器；旧版 #origins、#flywheels、#panorama 锚点继续有效。

## 维护

原生 HTML、CSS、SVG、JavaScript，无第三方运行时；所有图像本地托管。

index.html 是页面源文件，其中 story-data 为十章时长、旁白与讲述提示。修改叙事时同步 narrative.md；图解关系以仓库宣言为准。新增素材同步 [assets/SOURCES.md](assets/SOURCES.md)。主站入口由 scripts/build_site.py 生成。

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
python3 scripts/check_presentation.py
node --check site/presentation/app.js
```

部署前更新 index.html 中 CSS 与 JS 的版本参数，避免旧资源缓存。本版完成网页、交互图解、素材与讲述稿；AI 配音和正式视频需要另行制作。
