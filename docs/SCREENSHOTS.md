# Documentation image provenance

The twelve PNGs in `docs/images/` form six Chinese/English pairs. They are original browser-rendered **synthetic UI illustrations**, with fictional places, dates and an example account. They are not captures of a deployed guide or proof of implemented starter features. The opening image is a ChatGPT-style fictional conversation; the reusable local skill is invoked in Codex. The public ChatGPT interface was inspected as a visual reference on 2026-09-11, without copying a real conversation.

| Pair | Purpose | PNG dimensions |
| --- | --- | --- |
| chat-zh / chat-en | Planning conversation in a desktop chat interface | 2700 × 1680 |
| home-zh / home-en | Portrait phone: daily route, deadline and next action | 2700 × 1680 |
| overview-zh / overview-en | All six primary pages in one composition | 3600 × 1800 |
| map-zh / map-en | Portrait map, date/route filters and numbered stops | 2700 × 1680 |
| interaction-zh / interaction-en | Tools hub and shared-ticket selection | 2700 × 1680 |
| logistics-zh / logistics-en | Daily meals and base-hotel arrangements | 2700 × 1680 |

Both languages share composition templates, fictional records and interaction states. Chinese typography has small map-height and meal-card spacing accommodations to keep all stops clear of navigation. Every image carries a demonstration label; the map is explicitly non-navigational.

## Source and reproduction

Current sources: [artwork HTML](artwork/artwork.html), [styles](artwork/artwork.css), [shared compositions](artwork/artwork.js), [Chinese text](artwork/localize.js). The earlier `demo-screenshots.html` and `interaction-demo.html` are retained as historical source files; they no longer generate the current README images.

```sh
sh scripts/render_readme_screenshots.sh
python3 scripts/check_docs.py
```

Requires Node.js, Playwright and Chrome/Chromium. Set `NODE_PATH` to a tools directory containing Playwright when necessary and `CHROME` to a browser executable. Rendering uses an isolated browser, blocks remote HTTP assets and never opens an authenticated user profile. Normal panels use an 1800 × 1120 CSS viewport; the overview uses 2400 × 1200. Device scale is 1.5. Font availability can change pixels; the authored Chinese version uses PingFang SC on macOS, with Microsoft YaHei as a fallback.

The [render checks](artwork/render-checks.json) record complete translations, image loading, canvas size, six icons per phone and content clearance above navigation. Visual review remains necessary for typography and composition. These checks do not validate the live application, an authentication backend or physical-device behavior.

## Generated scenic asset

[alpine-lake.png](artwork/assets/alpine-lake.png) is an AI-generated fictional landscape produced with OpenAI image generation on 2026-09-11. It is reused unchanged in the home and sights views, including both languages. No private photographs or reference traveler records were supplied. All UI text and icons are rendered from HTML/CSS/SVG; the model did not generate interface text.

Prompt:

> Create one premium editorial travel photograph, horizontal 3:2 composition, no text or borders or logos or people. A fictional alpine journey: a glacial turquoise lake beneath craggy pale limestone mountains, a small wooded shore with dark fir trees and open meadow, early autumn soft golden morning light. Restrained natural colors, cool blue atmosphere, beautiful realistic detail, believable hiking destination, photographed on a professional camera with an understated travel magazine aesthetic. Wide quiet composition with mountains across upper half and lake across lower half. It will be a synthetic scenic illustration in English travel-app documentation, not evidence of a real destination. Save as a high quality image.

## 中文说明

十二张图片为六组中英对应的虚构界面示意，采用同一构图、行程和选择状态。规划图参考 ChatGPT 的公开界面，但对话内容为创作示例，本机技能在 Codex 中调用。手机页面不是实际部署截图，地图不可用于导航。湖泊照片为生图模型创作的虚构景观，未使用私人照片；文字和图标由浏览器精确渲染。图源、中文译文、生成提示词和检查记录均随仓库公开。
