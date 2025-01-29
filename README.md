# ImageVsCSV 

这是一个用于将图像文件转换为CSV文件并从CSV文件恢复图像的工具。它支持将图像的像素数据导出为CSV格式，并能够从CSV文件中还原图像。

## 功能
- **图像转CSV**：将图像文件的像素数据导出为CSV文件，支持RGBA格式。
- **CSV转图像**：从CSV文件中恢复图像，支持自定义输出格式（如PNG）。
- **色标优化**：在导出CSV时，会统计色标出现次数，对于出现超过128次的色标，会为其分配记号，优化CSV文件大小。

## 使用方法

### 安装依赖
确保你的环境中已安装以下Python库：
```
pip install pillow tqdm
```

### 图像转CSV
运行以下代码将图像文件转换为CSV文件：
```
imageToCsv('your_image.jpg')  # 替换为你的图像文件名
```
生成的CSV文件将包含图像的像素数据。

### CSV转图像
运行以下代码从CSV文件恢复图像：

csvToImage('your_image_RGBA.csv')  # 替换为你的CSV文件名

生成的图像将保存为your_image_output.png`。

## 示例
假设你有一个名为th.jpg的图像文件，运行以下代码：

imageToCsv('th.jpg')
csvToImage('th.jpg_RGBA.csv')

这将生成 th.jpg_RGBA.csv 文件，并从CSV文件中恢复图像为th_output.png。

## 更新日志
查看[更新日志](CHANGELOG.md)了解版本更新的详细信息。

## 贡献
欢迎提交Pull Request或Issue来帮助改进这个项目。

## 许可
本项目遵循MIT许可证，详情见[许可证文件](LICENSE)。
