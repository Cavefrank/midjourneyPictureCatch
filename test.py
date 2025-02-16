import os

import discord
from aiohttp import TCPConnector
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
SAVE_FOLDER = 'G:\\BaiduSyncdisk'
# 确保文件夹存在
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)


class MyBot(commands.Bot):
    async def setup_hook(self):
        # 在异步上下文中创建连接器（需要关闭ssl验证）
        self.http.connector = TCPConnector(ssl=False)
        await super().setup_hook()


# 配置机器人参数
bot = MyBot(
    command_prefix='!',
    intents=intents,
    proxy="http://127.0.0.1:10809"
)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print("登陆成功")


# 总表，使得各hybrid_command可以“/”形式呼出
@bot.command()
async def snyccommands(ctx):
    await bot.tree.sync()
    await ctx.send("同步完成")


@bot.hybrid_command()
async def ping(ctx):
    """输入Ping返回Pong"""
    await ctx.send("pong")


# 基础操作，输入!hello，返回Hello!
@bot.hybrid_command()
async def add(ctx, a: int, b: int):
    """一个基础的加法计算"""
    await ctx.send(f"两数相加的结果为：{a + b}")


if __name__ == "__main__":
    # ✅ 安全启动方式
    # 包含具体Token的代码会被拒绝推送
    bot.run("Token")
