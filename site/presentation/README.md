# AI 普惠互动演示 · 三个关键场景

线上地址：https://www.x-lab.info/ai-for-all/presentation/

1. **开放的力量**：Linux 35 年官方图片 → DeepSeek、Kimi、GLM 代表版本 → AI 普惠主张。
2. **双飞轮**：每环四个节点，双向价值与资源关系，共同内核“数据与评价”；点击节点查看解释。
3. **全景与邀请**：五部分完整框架、数字公共品到真实帮助的路径，以及参与入口。

这是网页演示的首轮三个关键场景，不是十页完整演示或已配音的正式宣传片。

## 操作

- 鼠标或触摸选择章节、点击节点；方向键切换章节。
- “全屏演讲”或 F 切换全屏（浏览器支持时）。
- “90 秒导览”按每场景 30 秒自动播放，无配音；暂停后可继续，完成后可以重播。
- 空格控制导览（焦点位于按钮或链接时保留该控件的原生键盘操作）。
- “暂停动效”停止图解动画，独立于导览计时。系统偏好减少动态效果时，默认关闭循环动效。
- 切换到后台时暂停计时；素材来源弹窗打开时暂停导览。
- 手机采用纵向布局；桌面采用横向双飞轮。每个场景支持 `#origins`、`#flywheels`、`#panorama` 直接链接。

## 维护

原生 HTML、CSS、SVG、JavaScript，无构建依赖与第三方运行时。所有展示素材本地托管；第三方链接仅由用户点击后打开。

修改本目录直接随 `site/` 发布。主站演示入口由 `scripts/build_site.py` 生成，避免手动编辑主站生成文件后被覆盖。运行：

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
python3 scripts/check_presentation.py
node --check site/presentation/app.js
```

素材来源及使用说明见 [assets/SOURCES.md](assets/SOURCES.md)。
