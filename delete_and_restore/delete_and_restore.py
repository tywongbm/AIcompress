from PIL import Image
import numpy as np

def mask_to_binary_array(mask_image_path, binary_array):
    mask_image = Image.open(mask_image_path).convert('1')
    width, height = mask_image.size

    for y in range(height):
        for x in range(width):
            pixel = mask_image.getpixel((x, y))
            if (pixel > 127):
                binary_array.append(0)
            else:
                binary_array.append(1)

def process_image_based_on_binary_array(image_path, binary_array, trans_image_path):

    with Image.open(image_path) as img:

        img = img.convert("RGBA")
        width, height = img.size
        pixels = list(img.getdata())
        
        if len(binary_array) != width * height:
            raise ValueError("The length of the binary array does not match the number of pixels in the image.")
        
        new_pixels = []
        for i, pixel in enumerate(pixels):
            if binary_array[i] == 1:
                new_pixels.append((0, 0, 0, 0))
            else:
                new_pixels.append(pixel)
        
        new_img = Image.new("RGBA", (width, height))
        new_img.putdata(new_pixels)
        
        new_img.save(trans_image_path)

def remove_transparent_pixels(trans_image_path, delete_image_path):
    # 打开图像
    img = Image.open(trans_image_path)
    img = img.convert("RGBA")  # 确保图像是RGBA格式

    # 获取图像尺寸和像素数据
    pixels = img.load()
    width, height = img.size

    # 准备一个列表来存储不透明的像素
    non_transparent_pixels = []

    # 遍历图像中的每一个像素
    for y in range(height):
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a != 0:  # a是透明度，如果不为0则表示不透明
                non_transparent_pixels.append((r, g, b))

    # 计算新图像的尺寸
    num_pixels = len(non_transparent_pixels)
    new_width = 256
    new_height = (num_pixels + new_width - 1) // new_width  # 计算所需高度

    # 创建一个新的图像
    new_img = Image.new('RGB', (new_width, new_height))

    # 设置新图像的像素
    new_pixels = new_img.load()
    for i, pixel in enumerate(non_transparent_pixels):
        x = i % new_width
        y = i // new_width
        new_pixels[x, y] = pixel

    # 保存新图像
    new_img.save(delete_image_path)
def expand_image_with_white_pixels(image_path, binary_array, final_size=(256, 256)):
    # 打开原始图像
    img = Image.open(image_path)
    img = img.convert('RGB')
    width, height = img.size

    # 创建一个新的图像，最初是空的，最终大小256x256
    new_img = Image.new('RGB', final_size, (255, 255, 255))  # 默认填充白色
    new_pixels = new_img.load()

    # 初始化坐标和索引
    new_x, new_y = 0, 0
    index = 0  # 在原图中的像素索引

    # 遍历二进制数组
    for value in binary_array:
        # 根据当前值决定是插入白色像素还是原图像素
        if value == 1:
            # 插入白色像素
            if new_x < final_size[0] and new_y < final_size[1]:
                new_pixels[new_x, new_y] = (255, 255, 255)
                new_x += 1
        else:
            # 插入原图像素
            if index < width * height and new_x < final_size[0] and new_y < final_size[1]:
                orig_x, orig_y = index % width, index // width
                new_pixels[new_x, new_y] = img.getpixel((orig_x, orig_y))
                new_x += 1
                index += 1

        # 检查是否需要换行
        if new_x >= final_size[0]:
            new_x = 0
            new_y += 1
            if new_y >= final_size[1]:
                break

    # 保存新图像
    new_img.save('expanded_image.jpg')

image_path = "test_image_256_rgb.jpg"
mask_image_path = 'mask_image.jpg'
trans_image_path = "trans_image.png"
delete_image_path = "delete_image.jpg"

binary_array = []
mask_to_binary_array(mask_image_path, binary_array)
process_image_based_on_binary_array(image_path, binary_array, trans_image_path)
remove_transparent_pixels(trans_image_path, delete_image_path)

expand_image_with_white_pixels(delete_image_path, binary_array)