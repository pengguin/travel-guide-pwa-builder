# 旅行路书 PWA 构建技能

本技能把一句旅行想法、已经确认的行程，或一套正在使用的路书，转成适合手机现场执行、可离线阅读、能够持续更新的旅行 PWA。当前版本为 **2.4.0**。

以下图片均为自包含 HTML 渲染的虚构界面示意，不是 Codex 或实际路书截图；详见[图片来源](docs/SCREENSHOTS.md)。

![虚构对话中的技能调用与最小化规划输入](docs/images/chat-zh.png)

## 应用场景

- 规划模式：不超过五个决策阶段，从一句话生成结构化路线和初版路书；
- 执行模式：锁定票面、日期、酒店等硬事实，补齐时间线、硬时限、转场和备用方案；
- 更新模式：修改规范化数据，清理旧口径，并重新构建完整 PWA 发布包。

## 主要交付

动态首页、逐日执行页、互动地图、景点/交通/食宿指南、离线核心页面、清单与白底黑字打印、显式整包更新，以及可选的公开/私人数据分层。

![现场首页把下一步、硬时限与失败分枝放在首屏](docs/images/home-zh.png)

![横屏地图、点位清单与等高控件共同形成现场工作区](docs/images/map-zh.png)

## 环境边界

本地工具需要 Python 3.10 或更高版本和现代浏览器；仓库工作流需要 Git。联网核查、依赖安装、在线地图/实时信息、Sites 发布和首次私人数据同步需要网络。没有 ChatGPT Sites 时仍可生成本地公开静态 PWA，但本技能不提供或推荐具体的多用户替代托管方案。

详细方法、安装命令、验证要求、使用技巧和隐私边界见双语主文档 [README.md](README.md)。

- 免责声明：[DISCLAIMER.zh-CN.md](DISCLAIMER.zh-CN.md)
- 许可说明：[LICENSE.zh-CN.md](LICENSE.zh-CN.md)
- 标准许可证：[LICENSE](LICENSE)


## 2.4.0：按行程更新，按实际能力交付

- 已订机票/火车保持不变；团与个人主题优先，餐饮、酒店、取箱和睡眠围绕它们调整。
- 每天午餐/晚餐各一主一备；酒店列出晚到、早退、早餐和跨订单寄存条件，候选不等于预订。
- 同步首页、逐日行程、地图、深导日期、提醒、日历、预算和完整离线发布包。
- 审计自动识别静态与Sites/Vinext公开目录，检查缺失图标和可选摘要清单；源码检查需显式选择。

![虚构行程的按日食宿与次日准备示意](docs/images/logistics-zh.png)

| 能力 | 本包实际提供 | 仍需项目实现/验证 |
| --- | --- | --- |
| 便携静态起步 | 本地数据、日期状态、清单、日历、打印入口、基础离线缓存 | 最终行程、实景图与实际地图集成 |
| 行程更新 | 固定票务、食宿/恢复/寄存与派生视图的执行方法 | 在已有项目中完成数据与页面同步 |
| 发布审计 | 公开目录、资源、图标、可选SHA-256与启发式泄露检查 | API权限、浏览器行为、所有私人内容识别 |
| 整包更新 | 起步缓存隔离与失败行为；完整应用更新架构说明 | 起步项目没有摘要修复、成员后端或用户更新按钮 |
| 文档图片 | 浏览器渲染的双语虚构界面示意 | 不是真实Codex截图、实际路书地图或真机验收证据 |

新增审计用法：

```sh
python3 scripts/audit_travel_guide.py /path/to/guide --release
python3 scripts/audit_travel_guide.py /path/to/guide --release --public-dir custom/output
python3 scripts/audit_travel_guide.py /path/to/guide --release --source
python3 scripts/check_docs.py
```

`--release`默认只审部署后的公开资源；`--source`另查源码，可能包括合法的私有服务端记录。检查结果不代替人工隐私审查或浏览器/真机验收。

发布说明：[CHANGELOG](CHANGELOG.md) · [验证与打包流程](docs/releases/2.4.0.md) · [截图来源](docs/SCREENSHOTS.md) · [参与维护](CONTRIBUTING.md) · [GitHub Release](https://github.com/pengguin/travel-guide-pwa-builder/releases/tag/v2.4.0)。下载ZIP与SHA-256文件核对；解压后的技能目录应为`travel-guide-pwa-builder`。
