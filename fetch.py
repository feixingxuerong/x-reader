#!/usr/bin/env python3
"""
X-Reader: X/Twitter 内容抓取工具
结合 x-tweet-fetcher 和 FxEmbed
支持：推文、长推文、X Article
"""

import argparse
import json
import os
import re
import sys
import urllib.parse
from datetime import datetime
from pathlib import Path

import requests
from bs4 import BeautifulSoup


class XReader:
    """X/Twitter 内容读取器"""
    
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.json_dir = self.data_dir / "json"
        self.markdown_dir = self.data_dir / "markdown"
        self.json_dir.mkdir(parents=True, exist_ok=True)
        self.markdown_dir.mkdir(parents=True, exist_ok=True)
    
    def extract_tweet_id(self, url):
        """从 URL 中提取推文 ID"""
        patterns = [
            r'twitter\.com/\w+/status/(\d+)',
            r'x\.com/\w+/status/(\d+)',
            r'twitter\.com/\w+/(\d+)',
            r'x\.com/\w+/(\d+)',
        ]
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None
    
    def get_fxembed_url(self, url):
        """转换为 FxEmbed URL 用于嵌入 Discord"""
        result = url
        if 'x.com' in result:
            result = result.replace('x.com', 'fixupx.com')
        elif 'twitter.com' in result:
            result = result.replace('twitter.com', 'fxtwitter.com')
        return result
    
    def fetch_tweet(self, url, text_only=False):
        """获取推文内容"""
        tweet_id = self.extract_tweet_id(url)
        if not tweet_id:
            print(f"无法从 URL 中提取推文 ID: {url}")
            return None
        
        # 使用 FxTwitter API (公开 API，无需认证)
        api_url = f"https://api.fxtwitter.com/status/{tweet_id}"
        
        try:
            response = requests.get(api_url, timeout=30)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
            print(f"获取推文失败: {e}")
            return None
    
    def parse_tweet(self, data):
        """解析推文数据"""
        if not data or 'tweet' not in data:
            return None
        
        tweet = data['tweet']
        author = tweet.get('author', {})
        
        result = {
            'id': tweet.get('id'),
            'url': tweet.get('url'),
            'text': tweet.get('text'),
            'raw_text': tweet.get('raw_text', {}).get('text', ''),
            'created_at': tweet.get('created_at'),
            'author': {
                'id': author.get('id'),
                'name': author.get('name'),
                'username': author.get('screen_name'),
                'avatar_url': author.get('avatar_url'),
                'verified': author.get('verified', False),
                'blue': author.get('blue', False),
            },
            'stats': {
                'likes': tweet.get('likes'),
                'retweets': tweet.get('retweets'),
                'replies': tweet.get('replies'),
                'views': tweet.get('views'),
            },
            'media': tweet.get('media', []),
            'entities': tweet.get('entities', {}),
            'is_note_tweet': tweet.get('is_note_tweet', False),
        }
        
        # 处理 X Article
        if tweet.get('article'):
            result['article'] = self.parse_article(tweet['article'])
        
        return result
    
    def parse_article(self, article):
        """解析 X Article 内容"""
        if not article:
            return None
        
        # 解析 blocks 为纯文本
        content_text = ""
        blocks = article.get('content', {}).get('blocks', [])
        for block in blocks:
            block_type = block.get('type', '')
            block_text = block.get('text', '')
            
            if block_type == 'header-one':
                content_text += f"# {block_text}\n\n"
            elif block_type == 'header-two':
                content_text += f"## {block_text}\n\n"
            elif block_type == 'blockquote':
                content_text += f"> {block_text}\n\n"
            elif block_type == 'unstyled':
                content_text += f"{block_text}\n\n"
            elif block_type == 'atomic':
                # 图片/媒体
                media = block.get('data', {})
                if media.get('entityKey'):
                    content_text += f"[媒体内容]\n\n"
            else:
                if block_text:
                    content_text += f"{block_text}\n\n"
        
        return {
            'id': article.get('id'),
            'title': article.get('title'),
            'preview_text': article.get('preview_text'),
            'content_text': content_text.strip(),
            'created_at': article.get('created_at'),
            'blocks': blocks,
        }
    
    def to_markdown(self, parsed):
        """转换为 Markdown 格式"""
        if not parsed:
            return None
        
        md = []
        
        # 检查是否是 X Article
        article = parsed.get('article')
        if article:
            # X Article 格式
            md.append(f"# {article.get('title', 'Untitled')}")
            md.append("")
            md.append(f"*{parsed['author']['name']}*")
            md.append("")
            md.append("---")
            md.append("")
            md.append(article.get('content_text', ''))
            md.append("")
            md.append("---")
            md.append(f"🔗 [查看原文]({parsed['url']})")
            return "\n".join(md)
        
        # 普通推文格式
        author = parsed['author']
        badge = " ✅" if author.get('verified') else ""
        if author.get('blue'):
            badge += " 💙"
        
        md.append(f"## 🐦 {author['name']}{badge}")
        md.append(f"**@{author['username']}**")
        md.append("")
        
        # 正文 - 优先使用 raw_text
        text = parsed.get('raw_text') or parsed.get('text', '')
        if text:
            # 处理提及、话题标签、链接
            text = re.sub(r'@(\w+)', r'**@\1**', text)
            text = re.sub(r'#(\w+)', r'**#\1**', text)
            text = re.sub(r'https?://\S+', r'', text)  # 移除链接
            md.append(text)
            md.append("")
        
        # 统计数据
        stats = parsed['stats']
        stats_str = []
        if stats.get('likes'):
            stats_str.append(f"❤️ {stats['likes']:,}")
        if stats.get('retweets'):
            stats_str.append(f"🔁 {stats['retweets']:,}")
        if stats.get('replies'):
            stats_str.append(f"💬 {stats['replies']:,}")
        if stats.get('views'):
            stats_str.append(f"👁️ {stats['views']:,}")
        
        if stats_str:
            md.append(" | ".join(stats_str))
            md.append("")
        
        # 时间
        if parsed.get('created_at'):
            md.append(f"*发布时间: {parsed['created_at']}*")
        
        # 原文链接
        md.append("")
        md.append(f"🔗 [查看原文]({parsed['url']})")
        
        return "\n".join(md)
    
    def save(self, url, markdown=True, json_save=True):
        """保存推文内容"""
        data = self.fetch_tweet(url)
        if not data:
            return None
        
        parsed = self.parse_tweet(data)
        if not parsed:
            return None
        
        tweet_id = parsed['id']
        filename = f"tweet_{tweet_id}"
        
        # 保存 JSON
        if json_save:
            json_path = self.json_dir / f"{filename}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"JSON 已保存: {json_path}")
        
        # 保存 Markdown
        if markdown:
            md_content = self.to_markdown(parsed)
            md_path = self.markdown_dir / f"{filename}.md"
            with open(md_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            print(f"Markdown 已保存: {md_path}")
        
        return parsed


def main():
    parser = argparse.ArgumentParser(description="X-Reader: X/Twitter 内容抓取工具")
    parser.add_argument("--url", help="推文 URL")
    parser.add_argument("--markdown", action="store_true", help="保存为 Markdown")
    parser.add_argument("--text-only", action="store_true", help="仅文本输出")
    parser.add_argument("--embed", action="store_true", help="显示 Discord 嵌入链接")
    parser.add_argument("--output-dir", default="data", help="输出目录")
    
    args = parser.parse_args()
    
    if not args.url:
        print("请提供 URL: python3 fetch.py --url <url>")
        sys.exit(1)
    
    reader = XReader(args.output_dir)
    
    # 显示嵌入链接
    if args.embed:
        embed_url = reader.get_fxembed_url(args.url)
        print(f"Discord 嵌入链接:")
        print(f"<{embed_url}>")
        return
    
    # 获取并保存
    parsed = reader.save(args.url, markdown=args.markdown)
    
    if parsed and args.text_only:
        print(reader.to_markdown(parsed))


if __name__ == "__main__":
    main()
