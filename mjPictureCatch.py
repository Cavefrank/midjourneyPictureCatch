import os

import discord
import requests

# 你的 Discord Bot Token
TOKEN = "Token码1"

# 保存图片的本地文件夹
SAVE_FOLDER = 'G:\\'

# 确保文件夹存在
if not os.path.exists(SAVE_FOLDER):
    os.makedirs(SAVE_FOLDER)


class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

        # 检查消息内容是否包含触发器文字
        if "- Upscaled (Subtle) by" in message.content:
            # 查找图片 URL (假设只有一个)
            if message.attachments:
                image_url = message.attachments[0].url

                # 下载图片
                try:
                    response = requests.get(image_url)
                    response.raise_for_status()  # 检查是否下载成功

                    # 构建文件名 (使用消息ID)
                    filename = f"{SAVE_FOLDER}/{message.id}.png"  # or .jpg, 根据实际图片类型修改

                    # 保存图片
                    with open(filename, "wb") as f:
                        f.write(response.content)

                    print(f"Image saved to {filename}")

                except requests.exceptions.RequestException as e:
                    print(f"Error downloading image: {e}")


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(TOKEN)
