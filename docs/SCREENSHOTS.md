# Documentation image provenance

All ten PNGs in `docs/images/` are original browser-rendered **synthetic UI illustrations**. They use fictional travel names and illustrative dates. They are not current Codex screenshots, screenshots of a deployed guide, a real map or proof of implemented starter features. Each image includes a permanent demonstration label; the map includes a non-navigation label.

| Pair | Purpose | Viewport |
| --- | --- | --- |
| chat-zh / chat-en | Illustrative conversation entry and compact planning intake | 1600 × 1000 |
| home-zh / home-en | Intended field-home information hierarchy | 1600 × 1000 |
| map-zh / map-en | Intended automatic landscape layout with schematic points | 1600 × 900 |
| logistics-zh / logistics-en | Daily meals, conditional base-hotel storage and recovery preparation | 1600 × 1000 |
| interaction-zh / interaction-en | Task ownership and previously authorized personal offline reading | 1600 × 1000 |

Sources: `docs/demo-screenshots.html` and `docs/interaction-demo.html`. Renderer: local Chrome/Chromium headless, device scale 1, isolated temporary profile, no authenticated session. No reference traveler's assets or records are copied. Browser text/CSS create the illustration; screenshots are stored as PNG rather than substituted vector posters.

Reproduce on macOS with Chrome installed:

```sh
sh scripts/render_readme_screenshots.sh
python3 scripts/check_docs.py
```

On other systems set `CHROME` to the browser executable. Node.js encodes the local file URI. Font availability may change exact pixels; compare layout, language pairing and text completeness rather than expecting identical cross-platform raster hashes.

## 中文说明

十张图片均为浏览器渲染的虚构界面示意，中英严格对应。对话图不是当前Codex的真实截图；地图图不是可导航地图；功能图不是起步项目已经实现所有功能的证明。图内标注示意性质，来源HTML与重现脚本随仓库提供。没有使用旅行者的私人票据、站点截图或个人数据。

Rendering requires Node.js, Playwright (`npm install --no-save playwright` in a disposable tools directory), and Chromium/Chrome. Set `NODE_PATH` to that directory’s node_modules when needed, and `CHROME` to an installed browser executable. The renderer uses an isolated temporary browser and blocks remote assets. It never opens a user profile.
