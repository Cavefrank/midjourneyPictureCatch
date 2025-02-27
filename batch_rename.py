import os


def batch_rename(folder_path, prefix):
    # 获取文件夹中的所有文件
    files = os.listdir(folder_path)
    # 对文件进行排序，确保按顺序重命名
    files.sort()

    # 初始化序号
    count = 1

    for file in files:
        # 构造新的文件名
        new_file_name = f"{prefix}-{count:03d}{os.path.splitext(file)[1]}"
        # 构造旧文件的完整路径
        old_file_path = os.path.join(folder_path, file)
        # 构造新文件的完整路径
        new_file_path = os.path.join(folder_path, new_file_name)

        # 重命名文件
        os.rename(old_file_path, new_file_path)

        # 序号递增
        count += 1


if __name__ == "__main__":
    # 示例用法
    folder_path = "G:\\BaiduSyncdisk\\GlowPower壁纸社\\A040-宇宙系列（兔子与瓶子）-手机壁纸共4张"  # 替换为你的文件夹路径
    prefix = folder_path.split('\\')[-1][:4]  # 提取文件夹名称的前四个字符作为前缀
    batch_rename(folder_path, prefix)
