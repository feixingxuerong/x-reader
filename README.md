# 🐦 X-Reader

X/Twitter 内容阅读器 - 自动嵌入 Discord + 保存 Markdown

<p align="center">

![Python](https://img.shields.io/badge/Python-3.8+-FFD43B?style=flat&logo=python)
![License](https://img.shields.io/badge/License-MIT-FF69B4)
![Platform](https://img.shields.io/badge/Platform-Discord-5865F2)

</p>

---

## ✨ 特性

- 🐦 **推文抓取** - 支持普通推文、长推文、X Article
- 📱 **Discord 嵌入** - 自动转换为 FxEmbed 格式
- 💾 **Markdown 保存** - 自动保存为高质量 Markdown
- 🔍 **智能解析** - 提取正文、作者、统计、媒体

---

## 🚀 快速开始

### 安装

```bash
pip install requests beautifulsoup4
```

### 使用

```bash
# 获取嵌入链接
python3 fetch.py --embed --url "https://x.com/user/status/123"

# 保存为 Markdown
python3 fetch.py --url "https://x.com/user/status/123" --markdown
```

---

## 📖 功能说明

### 功能一：Discord 嵌入

在 Discord 中粘贴 X/Twitter 链接，自动嵌入预览。

```
原始: https://twitter.com/user/status/123456
嵌入: https://fxtwitter.com/user/status/123456
```

### 功能二：Markdown 保存

自动获取、解析并保存推文内容。

**保存内容：**
- 推文正文
- 作者信息
- 统计数据
- 时间戳

**保存位置：**
- `data/markdown/` - Markdown 文件
- `data/json/` - 原始 JSON 数据

---

## 🎯 示例

```python
from fetch import XReader

reader = XReader()

# 获取推文
parsed = reader.save("https://x.com/user/status/123", markdown=True)
print(reader.to_markdown(parsed))
```

---

## 📁 项目结构

```
x-reader/
├── fetch.py      # 核心抓取脚本
├── SKILL.md      # OpenClaw Skill
├── README.md     # 本文件
└── data/        # 保存的数据
    ├── markdown/
    └── json/
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📝 License

MIT License

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/feixingxuerong">爱弥斯</a>
</p>
