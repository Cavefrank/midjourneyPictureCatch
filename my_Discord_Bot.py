import discord
from aiohttp import TCPConnector
from discord.ext import commands

from Upscaled_Picture_save import create_directory, specific_text_check

intents = discord.Intents.default()
intents.message_content = True
SAVE_FOLDER = 'G:\\BaiduSyncdisk'
# 确保文件夹存在
create_directory(SAVE_FOLDER)


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

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await specific_text_check(SAVE_FOLDER, message)


if __name__ == "__main__":
    # ✅ 安全启动方式
    # 包含具体Token的代码会被拒绝推送
    bot.run("Token")
