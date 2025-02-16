# image_processor.py
import os
from io import BytesIO

from PIL import Image

async def combine_images(image_urls, output_filename, proxy=None):
    """
    将四张图片组合成一张缩略图。

    Args:
        image_urls (list): 包含四张图片 URL 的列表。
        output_filename (str): 输出文件名（包括完整路径）。
        proxy (str, optional): 代理服务器地址。 Defaults to None.
    """
    try:
        images = await download_images(image_urls, proxy)  # 下载图片
        if len(images) != 4:
            print(f"Error: Expected 4 images, but got {len(images)}")
            return

        # 创建一个新的图片，大小为 2x2 的网格
        new_image = Image.new('RGB', (images[0].width * 2, images[0].height * 2))

        # 将图片粘贴到新的图片上
        new_image.paste(images[0], (0, 0))
        new_image.paste(images[1], (images[0].width, 0))
        new_image.paste(images[2], (0, images[0].height))
        new_image.paste(images[3], (images[0].width, images[0].height))

        # 保存新的图片
        new_image.save(output_filename, "PNG")
        print(f"Successfully combined images and saved to {output_filename}")

    except Exception as e:
        print(f"Error combining images: {e}")


async def download_images(image_urls, proxy=None):
  """
  下载图片列表，返回PIL图像对象列表。
  """
  import aiohttp
  from aiohttp import TCPConnector
  images = []
  async with aiohttp.ClientSession(connector=TCPConnector(ssl=False)) as session:
      for url in image_urls:
          try:
              async with session.get(url, proxy=proxy) as resp:
                  if resp.status == 200:
                      image_data = await resp.read()
                      image = Image.open(BytesIO(image_data))
                      images.append(image)
                  else:
                      print(f"Failed to download {url}: Status code {resp.status}")
                      return [] # 如果任何一张图片下载失败，则返回空列表
          except aiohttp.ClientError as e:
              print(f"AIOHTTP ClientError: {e}")
              return []
          except Exception as e:
              print(f"An unexpected error occurred: {e}")
              return []
  return images


def is_mj_upscale_message(message_content):
    """
    判断消息内容是否是 MJ upscale 的消息，根据特定文本特征。
    """
    return "Oil painting with extremely fine brushstrokes" in message_content and "--ar" in message_content


def extract_job_id(message_content):
    """
    从消息内容中提取 Job ID（假设 Job ID 在特定文本之后）。
    :param message_content: 消息内容文本
    :return: 提取出的 job_id，如果未找到则返回 None
    """
    import re
    match = re.search(r'Job ID: (\w+)', message_content)
    if match:
        return match.group(1)
    else:
        return None