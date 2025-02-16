# image_downloader.py
import os

import aiohttp
from aiohttp import TCPConnector


async def download_file(url, filename, proxy=None):
    """
    异步下载文件到本地。

    Args:
        url (str): 文件的 URL。
        filename (str): 保存的文件名（包括完整路径）。
        proxy (str, optional): 代理服务器地址。 Defaults to None.
    """
    # 再次关闭ssl验证
    async with aiohttp.ClientSession(connector=TCPConnector(ssl=False)) as session:
        try:
            async with session.get(url, proxy=proxy) as resp:
                if resp.status == 200:
                    with open(filename, 'wb') as f:
                        f.write(await resp.read())
                    print(f'已成功下载：{filename}')
                else:
                    print(f'Failed to download {url}: Status code {resp.status}')
        except aiohttp.ClientError as e:
            print(f"AIOHTTP ClientError: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


def create_directory(directory):
    """
    创建目录，如果目录不存在。

    Args:
        directory (str): 要创建的目录路径。
    """
    if not os.path.exists(directory):
        print("指定的目录不存在，正在创建...")
        os.makedirs(directory)


async def specific_text_check(SAVE_FOLDER, message):
    # 检查消息是否包含特定文本
    if " - Upscaled (Subtle) by" in message.content:
        print(f"发现包含目标文本的消息: {message.content}")
        # 检查消息是否有附件
        if message.attachments:
            for attachment in message.attachments:
                # 获取附件的 URL 和文件名
                image_url = attachment.url
                filename = os.path.join(SAVE_FOLDER, attachment.filename)  # 将文件名添加到保存目录路径中
                # 下载附件
                await download_file(image_url, filename, proxy="http://127.0.0.1:10809")  # 传递代理参数
        else:
            print("消息中包含目标文本，但没有附件")
    else:
        print("未发现包含目标文本的消息")
