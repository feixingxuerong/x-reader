# x-reader

X/Twitter 内容阅读器：支持将链接转换为 Discord 可预览链接，并抓取内容保存为 JSON / Markdown。

## ✨ 特性

- 🧩 **模块化架构**：`src/x_reader/*` 按职责拆分（CLI、解析、渲染、存储、Bot）
- 🔗 **FxEmbed 转换**：`x.com` / `twitter.com` 自动转换为 `fixupx.com` / `fxtwitter.com`
- 💾 **内容落盘**：原始 JSON + Markdown 输出
- 🤖 **Discord Bot**：自动识别消息中的 X/Twitter 链接，支持 `xembed / xfetch / xinfo`
- ✅ **单元测试**：`tests/test_*.py`

## 安装

```bash
python3 -m pip install -r requirements.txt
```

## CLI 用法

兼容旧入口：

```bash
python3 fetch.py --embed --url "https://x.com/user/status/123"
python3 fetch.py --url "https://x.com/user/status/123" --markdown
```

也可直接调用模块：

```bash
PYTHONPATH=src python3 -m x_reader.cli --embed --url "https://x.com/user/status/123"
```

## Discord Bot

兼容旧入口：

```bash
DISCORD_TOKEN=your_token python3 bot.py
```

## 测试

```bash
python3 -m unittest discover -s tests -p "test_*.py"
```

## 项目结构

```text
x-reader/
├── bot.py                  # 兼容 wrapper（委托到 src/x_reader/discord_bot.py）
├── fetch.py                # 兼容 wrapper（委托到 src/x_reader/cli.py）
├── requirements.txt
├── src/
│   └── x_reader/
│       ├── __init__.py
│       ├── cli.py
│       ├── client.py
│       ├── discord_bot.py
│       ├── parser.py
│       ├── reader.py
│       ├── renderer.py
│       ├── storage.py
│       └── url_utils.py
└── tests/
    ├── test_cli.py
    ├── test_parser_renderer.py
    ├── test_reader_save.py
    └── test_url_utils.py
```
