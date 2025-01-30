import csv
from PIL import Image
import time
from tqdm import tqdm
from collections import Counter

def imageToCsv(imageName):
    st = time.time()  # 记录开始时间
    im = Image.open(imageName).convert("RGBA")  # 打开图像并转换为 RGBA 格式
    w, h = im.size  # 获取图像的宽度和高度
    fileName = f"{imageName}_{im.mode}.csv"  # 创建输出文件名

    color_counter = Counter()

    # 统计色标出现次数
    pixels = im.getdata()
    for pixel_value in tqdm(pixels, desc="统计色标", unit="像素"):
        color_counter[pixel_value] += 1

    # 找出所有色标并为其分配记号
    color_mapping = {}
    marker_index = 1
    for color in color_counter:
        color_mapping[color] = f"*{marker_index}"
        marker_index += 1

    with open(fileName, "w", newline="") as imageFile:
        # 写入图像尺寸
        imageFile.write(f"width={w}\n")
        imageFile.write(f"height={h}\n")

        # 写入记号定义
        for color, marker in color_mapping.items():
            color_str = ','.join(str(c) if c != 0 else '' for c in color)
            imageFile.write(f"{marker}={color_str}\n")

        # 直接写入像素数据
        index = 0
        for y in tqdm(range(h), desc="写入像素数据", unit="行"):
            for x in range(w):
                pixel_value = pixels[index]
                pixel_str = color_mapping[pixel_value]
                imageFile.write(f"{x},{y},{pixel_str}\n")
                index += 1

    et = time.time()  # 记录结束时间
    print(f"{imageName}已经转换为{fileName}")
    print(f"使用了{et - st} 秒")  # 修正为正确的耗时计算

def csvToImage(csvFileName, mbgs="png"):
    st = time.time()  # 记录开始时间
    width, height = 0, 0
    color_mapping = {}

    # 读取图像尺寸和记号定义
    with open(csvFileName, mode='r', newline='') as csvFile:
        width = int(csvFile.readline().strip().split('=')[1])
        height = int(csvFile.readline().strip().split('=')[1])
        for line in csvFile:
            if not line.startswith('*'):
                break
            marker, color_str = line.strip().split('=')
            color_values = [int(c) if c else 0 for c in color_str.split(',')]
            color_mapping[marker] = tuple(color_values)

    # 创建一个新的图像对象
    im = Image.new("RGBA", (width, height))

    # 设置像素值
    with open(csvFileName, mode='r', newline='') as csvFile:
        # 跳过图像尺寸和记号定义
        for _ in range(2):
            csvFile.readline()
        while csvFile.readline().startswith('*'):
            pass
        for line in tqdm(csvFile, desc="设置像素值"):
            parts = line.strip().split(',')
            x = int(parts[0])
            y = int(parts[1])
            pixel_value_str = parts[2]
            pixel_value = color_mapping[pixel_value_str]
            im.putpixel((x, y), pixel_value)

    # 修正输出图像名称
    output_image_name = f"{csvFileName.partition('.')[0]}_output.{mbgs}"

    # 保存恢复的图像
    im.save(output_image_name)
    print(f"{csvFileName}已经转换为{output_image_name}")

    et = time.time()  # 记录结束时间
    print(f"使用了{et - st} 秒")  # 打印耗时

# 使用图像文件转换为 CSV 文件
imageToCsv('th.jpg')

# 使用 CSV 文件恢复图像
csvToImage('th.jpg_RGBA.csv')
