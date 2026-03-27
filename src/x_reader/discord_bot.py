"""Discord bot entrypoint and command handlers for X-Reader."""

from __future__ import annotations

import os

import discord
from discord.ext import commands

from .reader import XReader
from .url_utils import find_x_urls


def create_bot(prefix: str | None = None, data_dir: str = "data") -> commands.Bot:
    actual_prefix = prefix or os.getenv("PREFIX", "!")

    intents = discord.Intents.default()
    intents.message_content = True

    bot = commands.Bot(command_prefix=actual_prefix, intents=intents)
    reader = XReader(data_dir=data_dir)

    @bot.event
    async def on_ready():
        print(f"Bot 已启动: {bot.user}")
        print(f"前缀: {actual_prefix}")

    @bot.event
    async def on_message(message):
        if message.author.bot:
            return

        urls = find_x_urls(message.content)
        if urls:
            for url in urls:
                embed_url = reader.get_fxembed_url(url)
                await message.reply(f"📌 **X/Twitter 嵌入预览**\n{embed_url}")

        await bot.process_commands(message)

    @bot.command(name="xembed")
    async def x_embed(ctx, *, url: str | None = None):
        if not url:
            await ctx.send("用法: `!xembed <X/Twitter链接>`")
            return

        embed_url = reader.get_fxembed_url(url)
        await ctx.send(f"📌 **Discord 嵌入链接:**\n<{embed_url}>")

    @bot.command(name="xfetch")
    async def x_fetch(ctx, *, url: str | None = None):
        if not url:
            await ctx.send("用法: `!xfetch <X/Twitter链接>`")
            return

        await ctx.send("⏳ 正在获取推文内容...")
        parsed = reader.save(url, markdown=True)

        if parsed:
            md = reader.to_markdown(parsed) or ""
            if len(md) > 1900:
                md = md[:1900] + "..."
            await ctx.send(f"✅ **推文内容:**\n\n{md}")
        else:
            await ctx.send("❌ 获取推文失败")

    @bot.command(name="xinfo")
    async def x_info(ctx, *, url: str | None = None):
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

        author = parsed["author"]
        stats = parsed["stats"]

        embed = discord.Embed(title="🐦 推文信息", color=discord.Color.blue())
        embed.set_author(
            name=f"{author['name']} (@{author['username']})",
            icon_url=author.get("avatar_url", ""),
        )
        embed.description = (parsed.get("text") or "")[:500]

        stats_text: list[str] = []
        if stats.get("likes"):
            stats_text.append(f"❤️ {stats['likes']:,}")
        if stats.get("retweets"):
            stats_text.append(f"🔁 {stats['retweets']:,}")
        if stats.get("replies"):
            stats_text.append(f"💬 {stats['replies']:,}")
        if stats.get("views"):
            stats_text.append(f"👁️ {stats['views']:,}")

        embed.add_field(name="📊 统计数据", value=" | ".join(stats_text) if stats_text else "无")
        embed.add_field(name="🔗 原文", value=f"[点击查看]({parsed['url']})")

        await ctx.send(embed=embed)

    return bot


def run_bot() -> int:
    token = os.getenv("DISCORD_TOKEN", "")
    if not token:
        print("错误: 请设置 DISCORD_TOKEN 环境变量")
        print("用法: DISCORD_TOKEN=your_token python3 bot.py")
        return 1

    print("启动 X-Reader Bot...")
    bot = create_bot()
    bot.run(token)
    return 0
