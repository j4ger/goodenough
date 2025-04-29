import os
import re
import requests
from bs4 import BeautifulSoup

def download_enemy_profiles():
    """
    从 enemies.txt 中读取敌人名称，从 wiki.html 中提取对应头像，并下载保存。
    """

    try:
        # 1. 读取 enemies.txt 文件，获取敌人名称列表
        with open('enemies.txt', 'r', encoding='utf-8') as f:
            enemy_names = [line.strip() for line in f]  # 读取每行并去除首尾空格

        # 2. 读取 wiki.html 文件
        with open('wiki.html', 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 3. 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(html_content, 'html.parser')

        # 4. 创建保存头像的目录 (如果不存在)
        output_dir = './assets/profiles'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 5. 遍历敌人名称列表，查找对应的头像并下载
        for enemy_name in enemy_names:
            # 使用 alt 属性查找 img 标签
            img_tag = soup.find('img', {'alt': enemy_name})

            if img_tag:
                # 获取图片 URL
                image_url = img_tag['src']

                # 构建保存路径
                output_path = os.path.join(output_dir, f"{enemy_name}.png")

                try:
                    # 下载图片
                    response = requests.get(image_url, stream=True)
                    response.raise_for_status()  # 检查下载是否成功

                    # 保存图片
                    with open(output_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=8192):
                            f.write(chunk)

                    print(f"Successfully downloaded profile image for {enemy_name} to {output_path}")

                except requests.exceptions.RequestException as e:
                    print(f"Error downloading profile image for {enemy_name}: {e}")

            else:
                print(f"Could not find profile image for {enemy_name}")

    except FileNotFoundError as e:
        print(f"Error: File not found: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    download_enemy_profiles()
