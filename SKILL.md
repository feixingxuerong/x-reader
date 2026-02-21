---
name: x-reader
description: 爱弥斯的 X/Twitter 阅读技能 - 自动嵌入 Discord + 保存 Markdown
metadata: {"openclaw": {"requires": {"bins": ["python3"], "pip": ["requests", "beautifulsoup4"]}}}
---

# X-Reader (爱弥斯技能)

我是爱弥斯的 X/Twitter 阅读技能！✨

## 功能

### 功能一：Discord 嵌入

当检测到 X/Twitter 链接时，自动转换为 FxEmbed 格式。

**我这样做：**
1. 检测消息中的 X/Twitter URL
2. 转换为 fxtwitter.com 嵌入链接
3. 回复你预览链接

### 功能二：Markdown 保存

自动获取、解析并保存推文为 Markdown。

**我会保存到：**
- `projects/x-reader/data/markdown/` - Markdown 文件
- `projects/x-reader/data/json/` - 原始 JSON

## 使用方式

### 自动处理

直接粘贴 X/Twitter 链接，我会自动处理！

```
你: https://twitter.com/elonmusk/status/123456789
我: 📌 X/Twitter 嵌入预览
    https://fxtwitter.com/elonmusk/status/123456789
```

### 手动命令

- `/x-embed <url>` — 获取嵌入链接
- `/x-save <url>` — 保存为 Markdown
- `/x-info <url>` — 获取详细信息

## 项目位置

`/root/.openclaw/workspace/projects/x-reader/`

## 实现原理

1. 使用 FxTwitter API 获取推文数据
2. 解析推文内容（正文、作者、统计）
3. 用 FxEmbed 生成 Discord 嵌入
4. 可选保存为 Markdown 供后续使用
