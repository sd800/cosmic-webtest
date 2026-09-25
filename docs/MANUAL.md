# Cosmic WebTest 使用与部署手册

项目简介见仓库根目录的 `README.md`。本手册说明测试内容、本地运行和 GitHub Pages 部署。

左侧切换文档样本、链接与协议、下载路径。自动适配深浅色；刷新时保留当前栏目，不异步插入文件列表或加载网页字体。

## 发布到 GitHub Pages

Cosmic WebTest 是独立仓库。保留 `.github/workflows/pages.yml`，推送到 `main`。

1. 在 GitHub 仓库的 **Settings → Pages → Build and deployment → Source** 中选择 **GitHub Actions**。
2. 推送到 `main`，或在 Actions 中手动运行 **Deploy Cosmic WebTest**。
3. 部署完成后，从 Pages 设置或 workflow 的 deployment 链接访问网站。

无需修改仓库名、域名或路径配置。站内文件和资源使用相对 URL，兼容 `https://用户名.github.io/仓库名/` 和独立域名；栏目使用 hash，不依赖服务器路由重写。

workflow 运行 `python3 tools/prepare-pages.py`，只发布 `.pages/` 中的网页资源、项目简介、手册、域名配置与文件样本。不会重新生成文档，也不会发布本地服务器、生成脚本、截图、测试资料或 `.DS_Store`。`.build/` 与 `.pages/` 已在本站的 `.gitignore` 中排除。

也可以手动运行 `python3 tools/prepare-pages.py`，将生成的 `.pages/` 内容部署到其他静态服务器。

## 可用测试

- 文件名链接：普通网页文件链接。
- 文件右侧的下载按钮：同源 HTML `download` 属性，**不是自定义 attachment 响应头**。
- 下载路径：中文下载文件名、查询参数、新标签页 PDF、PDF 下载与刻意的 404。
- 链接与协议：HTTP/HTTPS、mailto、tel、sms 和虚构应用协议。
- 文档内部的网页及协议链接：用于测试预览器中的 External Links Capture。

GitHub Pages 是静态托管，不能运行本项目的 Python 服务。真正的自定义 Content-Disposition、无扩展名下载响应、HTTP 302、慢速分块与省略 Content-Length 等用例仅由本地 `tools/server.py` 提供，线上页面不显示这些入口。不使用 JavaScript、假重定向或 Service Worker 冒充真实服务端响应。

官方说明：[GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)、[Actions 部署](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)。

## 插件准备

- 开启 Cosmic Gemini 的 Document Preview 和 Mailto Capture，确认当前测试域名未加入 Document Preview 白名单。
- 如果本次网站访问已有记住的预览/下载选择，请先重置该选择。
- 邮件和电话均为虚构测试内容，请勿实际发送或拨号。`cosmic-test:` 没有对应应用，仅测试协议捕获。
- 普通网页的 HTTP/HTTPS 链接正常跳转；文档预览内的外部链接用于测试内部 External Links Capture。
- 线上网站使用 HTTPS，不需要开启扩展的“允许访问文件网址”。本地 HTTP 测试服务也不是 `file://`，但不能替代真实托管环境的所有行为。

## 样本

| 文件 | 内容 |
| --- | --- |
| `web/files/sample.docx` | 中英文、字体、连续空格、列表、表格和 6 个链接 |
| `web/files/sample.doc` | 真正的 Word 97 文档，与 DOCX 对照 |
| `web/files/sample.xlsx` | Data / Links 工作表、数值、公式和 6 个链接 |
| `web/files/sample.xls` | 真正的 Excel 97 工作簿 |
| `web/files/sample.pptx` | 两张幻灯片和 6 个链接 |
| `web/files/sample.ppt` | 真正的 PowerPoint 97 演示文稿 |
| `web/files/sample.pdf` | 白纸与深色纸张、文字层和 URI 链接 |
| `web/files/sample.eml` | 合成邮件，纯文本/HTML 和 6 个链接 |

没有模板、宏或 OpenDocument 等衍生格式。样本没有宏、脚本、嵌入程序或远程图片。网站不会自动下载样本或打开外部链接。

## 本地服务（可选）

双击 `tools/start.command`，或在仓库根目录运行：

```sh
python3 tools/server.py
```

访问 `http://127.0.0.1:8765/`，使用 Control+C 停止；端口已被占用时运行 `python3 tools/server.py --port 8766`。

本地服务在首次响应中开启“本地服务响应”区域，提供附件响应头、无扩展名下载、302、慢速与未知大小测试。普通静态服务器和 GitHub Pages 不显示该区域。

服务器只监听本机回环地址，只开放明确列出的文件，不提供目录浏览。无需安装依赖。不要使用双击 HTML 的方式代替 HTTP/HTTPS 测试。

## 维护

- `web/`：桌面网站、样本文件、域名配置与静态资源。
- `tools/prepare-pages.py`：只拷贝允许公开的文件，并去除本地响应测试区域。
- `tools/server.py` / `tools/start.command`：本地响应测试服务。
- `docs/MANUAL.md`：本手册。
- `VERSION` / `CHANGELOG.md`：日历版本号与按日期记录的更新。
- `.github/workflows/pages.yml`：Pages 部署配置。
- `.build/`：本地保留的生成脚本、独立测试浏览器截图与检查资料，不提交或发布。已有文件可以反复使用；不需要重新生成。

当前开发目录虽存放在 Cosmic Gemini 已忽略的 `dist/` 中，但有独立的 Git 仓库和远端。它不随浏览器扩展打包；网站部署仅使用本仓库中由 `tools/prepare-pages.py` 整理的文件。
