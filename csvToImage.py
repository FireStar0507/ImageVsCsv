import csv
from PIL import Image
import time
from tqdm import tqdm  # Import tqdm library

def csvToImage(csvFileName, mbgs="png"):
    st = time.time()  # Record start time
    width, height = 0, 0
    pixel_data = []
    
    # Read CSV file
    with open(csvFileName, mode='r', newline='') as csvFile:
        csvReader = csv.DictReader(csvFile)
        for row in tqdm(csvReader, desc="读取CSV文件数据"):  # Add progress bar for CSV reading
            x = int(row["x"])    # Read x coordinate
            y = int(row["y"])    # Read y coordinate
            pixel_value_str = row[list(row.keys())[2]].strip()  # Get the pixel value string and strip whitespace            
            pixel_value_str = pixel_value_str.strip('()')  # Clean up the string
            pixel_value = tuple(map(int, pixel_value_str.split(',')))  # Convert to tuple of integers       
            pixel_data.append(((x, y), pixel_value))
            width = max(width, x + 1)  # Update width
            height = max(height, y + 1)  # Update height   
    
    # Create a new image object
    im = Image.new("RGBA", (width, height))    
    
    # Set pixel values
    for (x, y), pixel_value in tqdm(pixel_data, desc="设置像素值"):  # Add progress bar for setting pixel values
        im.putpixel((x, y), pixel_value)

    # Fixing the output image name
    output_image_name = f"{csvFileName.partition('.')[0]}_output.{mbgs}"
    
    # Save the restored image
    im.save(output_image_name)
    print(f"{csvFileName}已经转换为{output_image_name}")
    
    et = time.time()  # Record end time
    print(f"使用了{et - st} 秒")  # Print time taken

# Use the CSV file to restore the image
csvToImage('th.jpg_RGBA.csv')  # Replace with the correct CSV file name
