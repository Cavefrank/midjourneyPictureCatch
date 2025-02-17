import discord
from aiohttp import TCPConnector
from discord.ext import commands

from Upscaled_Picture_save import create_directory, specific_text_check

intents = discord.Intents.default()
intents.message_content = True
SAVE_FOLDER = 'G:\\BaiduSyncdisk\\0217生成库'
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


# 反馈登录结果
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')
    print("登陆成功")


# 自动获取2K图片
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    await specific_text_check(SAVE_FOLDER, message)
    # 这里存在一个“拦截”机制，暂时不明白
    # 不添加下述这行代码的话，command()都会被拦截，且也不是被“if message.author == bot.user”拦截
    await bot.process_commands(message)


# 错误处理机制
@bot.event
async def on_command_error(ctx, error):
    print(f"命令执行错误: {error}")
    await ctx.send(f"命令执行失败: {str(error)}")


# 待完善
@bot.command()
async def F(ctx, *, prompt: str): # 需要使用*获取所有输入内容，否则自动按照空格隔开
    """输入部分提示词，自动发送完整提示词"""
    await ctx.send(f"/imagine prompt: {prompt} --ar 9:20 --q 2 --v 6.1 --style raw --s 218")


if __name__ == "__main__":
    # ✅ 安全启动方式
    # 包含具体Token的代码会被拒绝推送
    bot.run(input("请输入Token:"))
