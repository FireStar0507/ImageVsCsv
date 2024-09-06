import csv
from PIL import Image
import time
from tqdm import tqdm  # 导入 tqdm 库

def imageToCsv(imageName):
    st = time.time()  # 记录开始时间
    im = Image.open(imageName).convert("RGBA")  # 打开图像并转换为 RGBA 格式
    w, h = im.size  # 获取图像的宽度和高度
    fileName = f"{imageName}_{im.mode}.csv"  # 创建输出文件名
    
    with open(fileName, "w", newline="") as imageFile:
        csvObj = csv.DictWriter(imageFile, fieldnames=["x", "y", im.mode])  # 创建 CSV 写入对象
        csvObj.writeheader()  # 写入表头
        
        # 使用 tqdm 添加进度条
        for x in tqdm(range(w), desc="正在转换图像", unit="列"):  # 添加进度条，描述为“正在转换图像”，单位为“列”
            for y in range(h):
                pixel_value = im.getpixel((x, y))  # 获取每个像素的值
                csvObj.writerow({"x": x, "y": y, im.mode: pixel_value})  # 写入 CSV
    
    et = time.time()  # 记录结束时间
    print(f"{imageName}已经转换为{fileName}")
    print(f"使用了{et - st} 秒")  # 修正为正确的耗时计算

# 使用图像文件转换为 CSV 文件
imageToCsv('th.jpg')  # 替换为正确的图像文件名

