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
    for x in tqdm(range(w), desc="统计色标", unit="列"):
        for y in range(h):
            pixel_value = im.getpixel((x, y))
            color_counter[pixel_value] += 1

    # 找出出现超过 128 次的色标并为其分配记号
    color_mapping = {}
    marker_index = 1
    for color, count in color_counter.items():
        if count > 128:
            color_mapping[color] = f"*{marker_index}"
            marker_index += 1

    with open(fileName, "w", newline="") as imageFile:
        # 写入记号定义
        for color, marker in color_mapping.items():
            color_str = ','.join(str(c) if c != 0 else '' for c in color)
            imageFile.write(f"{marker}={color_str}\n")

        csvObj = csv.DictWriter(imageFile, fieldnames=["x", "y", im.mode])  # 创建 CSV 写入对象
        csvObj.writeheader()  # 写入表头

        # 直接写入像素数据
        for x in tqdm(range(w), desc="写入像素数据", unit="列"):
            for y in range(h):
                pixel_value = im.getpixel((x, y))
                if pixel_value in color_mapping:
                    pixel_str = color_mapping[pixel_value]
                else:
                    pixel_str = ','.join(str(c) if c != 0 else '' for c in pixel_value)
                csvObj.writerow({"x": x, "y": y, im.mode: pixel_str})

    et = time.time()  # 记录结束时间
    print(f"{imageName}已经转换为{fileName}")
    print(f"使用了{et - st} 秒")  # 修正为正确的耗时计算

def csvToImage(csvFileName, mbgs="png"):
    st = time.time()  # 记录开始时间
    width, height = 0, 0
    color_mapping = {}

    # 读取记号定义
    with open(csvFileName, mode='r', newline='') as csvFile:
        for line in csvFile:
            if not line.startswith('*'):
                break
            marker, color_str = line.strip().split('=')
            color_values = [int(c) if c else 0 for c in color_str.split(',')]
            color_mapping[marker] = tuple(color_values)

    def pixel_generator():
        with open(csvFileName, mode='r', newline='') as csvFile:
            # 跳过记号定义
            while csvFile.readline().startswith('*'):
                pass
            csvReader = csv.DictReader(csvFile)
            for row in csvReader:
                x = int(row["x"])
                y = int(row["y"])
                pixel_value_str = row[list(row.keys())[2]].strip()
                if pixel_value_str.startswith('*'):
                    pixel_value = color_mapping[pixel_value_str]
                else:
                    pixel_value = tuple(int(c) if c else 0 for c in pixel_value_str.split(','))
                yield (x, y, pixel_value)

    # 确定图像尺寸
    for x, y, _ in tqdm(pixel_generator(), desc="确定图像尺寸"):
        width = max(width, x + 1)
        height = max(height, y + 1)

    # 创建一个新的图像对象
    im = Image.new("RGBA", (width, height))

    # 设置像素值
    for x, y, pixel_value in tqdm(pixel_generator(), desc="设置像素值"):
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
csvToImage('th.jpg_RGBA.csv')  # 替换为正确的 CSV 文件名称