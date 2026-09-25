# Cosmic WebTest

Cosmic WebTest is a small website for testing how browser extensions handle document previews, downloads, and external links in a real HTTPS page.

这是一个用于测试浏览器扩展文档预览、下载及外部链接处理的网站。

[Open Cosmic WebTest](https://test.songming.org/) · [使用与部署手册](docs/MANUAL.md)

## What you can test

- **Documents:** Open or download sample Word documents, spreadsheets, slides, a PDF, and an email file.
- **Links and protocols:** Try web, email, telephone, SMS, and sample application links. The documents also contain clickable links.
- **Download paths:** Compare ordinary file links, HTML download attributes, URLs with query parameters, opening a PDF in a new tab, and an intentional missing file.

The site follows the browser's light or dark appearance. Its sample files are included in this repository; visiting the site does not open their links automatically.

GitHub Pages hosts the website as static files. The optional local server in [MANUAL.md](docs/MANUAL.md) adds tests that require real HTTP response headers, redirects, or delayed responses.

Current version: [26.9.25.1](CHANGELOG.md). Versions use `YY.M.D.NUM`, with the last number counting releases on that date.
