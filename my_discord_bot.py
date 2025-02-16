import os

import aiohttp
import discord
from aiohttp import TCPConnector
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
SAVE_FOLDER = 'G:\\'
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


async def download_file(url, filename, proxy=None):  # 添加 proxy 参数
    async with aiohttp.ClientSession(connector=TCPConnector(ssl=False)) as session:
        async with session.get(url, proxy=proxy) as resp:  # 传递 proxy 参数
            if resp.status == 200:
                with open(filename, 'wb') as f:
                    f.write(await resp.read())
                print(f'Downloaded {filename}')
            else:
                print(f'Failed to download {url}: Status code {resp.status}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    print(f"Received message: {message.content}")

    # 检查消息是否包含特定文本
    if " - Upscaled (Subtle) by" in message.content:
        print(f"发现包含目标文本的消息: {message.content}")
        print("触发器检测通过，即将开始打印图片")
        # 检查消息是否有附件
        if message.attachments:
            for attachment in message.attachments:
                # 获取附件的 URL 和文件名
                image_url = attachment.url
                filename = os.path.join(SAVE_FOLDER, attachment.filename)  # 将文件名添加到保存目录路径中
                # 下载附件
                await download_file(image_url, filename, proxy="http://127.0.0.1:10809") #传递代理参数
        else:
            print("消息中包含目标文本，但没有附件。")
    else:
        print("消息中不包含目标文本")


if __name__ == "__main__":
    # ✅ 安全启动方式
    # 包含具体Token的代码会被拒绝推送
    bot.run("Token")
