# x-reader

一个轻量的 X/Twitter 内容抓取与格式化工具（基于 FxTwitter 公共 API），支持输出 Markdown、保存 JSON，以及生成 Discord 可嵌入链接。

## 快速使用

```bash
# 生成 Discord 嵌入链接
PYTHONPATH=src python3 fetch.py --embed --url "https://x.com/<user>/status/<id>"

# 保存 JSON + Markdown
PYTHONPATH=src python3 fetch.py --markdown --url "https://x.com/<user>/status/<id>"
```

## 结构

- `src/x_reader/`：核心逻辑（URL 解析 / API Client / 解析 / Markdown 格式化 / 存储 / CLI）
- `fetch.py`：兼容入口（继续支持 `python3 fetch.py ...`）
- `tests/`：最小单测与冒烟测试

## 测试

```bash
PYTHONPATH=src python3 -m unittest discover -s tests -p "test_*.py"
```
