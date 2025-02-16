import discord
from aiohttp import TCPConnector
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True


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

# 基础操作，输入!hello，返回Hello!
@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")


if __name__ == "__main__":
    # ✅ 安全启动方式
    bot.run("Token码")
