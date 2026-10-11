# 维护与发布

当前发布资料仅使用四项定稿：v1.2 宣言全文、13 章中英文网页演示、V5 影片、2026-10-11 定稿推文。推文源文件在 publication/，视觉和文档在 site/launch/。不再发布讲稿、早期影片、PPT 或框架图。

构建与验证：

```sh
python3 scripts/build_site.py
python3 scripts/build_release.py
python3 scripts/check_site.py
python3 scripts/check_presentation.py
python3 scripts/check_release.py
python3 scripts/stage_public_site.py
```

GitHub Actions 将 .publish-site 发布至 GitHub Pages。完整包由四项当前源文件生成，包内附 SHA-256，不能混入历史文件。

宣言核心原则调整先经 Issue 讨论。品牌资产与文字使用边界见 NOTICE.md。
