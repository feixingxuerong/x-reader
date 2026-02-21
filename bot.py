#!/usr/bin/env python3
"""
X-Reader Discord Bot
自动检测并处理消息中的 X/Twitter 链接
"""

import os
import re
import asyncio
import discord
from discord.ext import commands
from fetch import XReader


# 配置
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "")
PREFIX = os.getenv("PREFIX", "!")

# X/Twitter URL 检测正则
X_URL_PATTERN = re.compile(
    r'(https?://(?:mobile\.)?(?:twitter|x)\.com/\w+/status/\d+)'
)

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)
reader = XReader()


@bot.event
async def on_ready():
    print(f"Bot 已启动: {bot.user}")
    print(f"前缀: {PREFIX}")


@bot.event
async def on_message(message):
    # 忽略机器人消息
    if message.author.bot:
        return
    
    # 检测 X/Twitter 链接
    urls = X_URL_PATTERN.findall(message.content)
    
    if urls:
        for url in urls:
            # 获取嵌入链接
            embed_url = reader.get_fxembed_url(url)
            
            # 回复用户，包含嵌入链接
            await message.reply(f"📌 **X/Twitter 嵌入预览**\n{embed_url}")
    
    await bot.process_commands(message)


@bot.command(name="xembed")
async def x_embed(ctx, *, url: str = None):
    """获取 X/Twitter 嵌入链接"""
    if not url:
        await ctx.send("用法: `!xembed <X/Twitter链接>`")
        return
    
    embed_url = reader.get_fxembed_url(url)
    await ctx.send(f"📌 **Discord 嵌入链接:**\n<{embed_url}>")


@bot.command(name="xfetch")
async def x_fetch(ctx, *, url: str = None):
    """获取并保存 X/Twitter 内容"""
    if not url:
        await ctx.send("用法: `!xfetch <X/Twitter链接>`")
        return
    
    await ctx.send("⏳ 正在获取推文内容...")
    
    parsed = reader.save(url, markdown=True)
    
    if parsed:
        md = reader.to_markdown(parsed)
        # 截断太长的消息
        if len(md) > 1900:
            md = md[:1900] + "..."
        
        await ctx.send(f"✅ **推文内容:**\n\n{md}")
    else:
        await ctx.send("❌ 获取推文失败")


@bot.command(name="xinfo")
async def x_info(ctx, *, url: str = None):
    """获取 X/Twitter 推文详细信息"""
    if not url:
        await ctx.send("用法: `!xinfo <X/Twitter链接>`")
        return
    
    data = reader.fetch_tweet(url)
    if not data:
        await ctx.send("❌ 获取推文失败")
        return
    
    parsed = reader.parse_tweet(data)
    if not parsed:
        await ctx.send("❌ 解析推文失败")
        return
    
    author = parsed['author']
    stats = parsed['stats']
    
    embed = discord.Embed(
        title="🐦 推文信息",
        color=discord.Color.blue()
    )
    embed.set_author(
        name=f"{author['name']} (@{author['username']})",
        icon_url=author.get('avatar_url', '')
    )
    embed.description = parsed['text'][:500]
    
    # 统计
    stats_text = []
    if stats.get('likes'):
        stats_text.append(f"❤️ {stats['likes']:,}")
    if stats.get('retweets'):
        stats_text.append(f"🔁 {stats['retweets']:,}")
    if stats.get('replies'):
        stats_text.append(f"💬 {stats['replies']:,}")
    if stats.get('views'):
        stats_text.append(f"👁️ {stats['views']:,}")
    
    embed.add_field(name="📊 统计数据", value=" | ".join(stats_text) if stats_text else "无")
    embed.add_field(name="🔗 原文", value=f"[点击查看]({parsed['url']})")
    
    await ctx.send(embed=embed)


def main():
    if not DISCORD_TOKEN:
        print("错误: 请设置 DISCORD_TOKEN 环境变量")
        print("用法: DISCORD_TOKEN=your_token python3 bot.py")
        return
    
    print("启动 X-Reader Bot...")
    bot.run(DISCORD_TOKEN)


if __name__ == "__main__":
    main()
