import torch
from torchvision import transforms
from torchvision.transforms import transforms, ToPILImage
from PIL import Image
import time

'''
def modify_image(image_path):

    time.sleep(3)

    image = Image.open(image_path)

    transform = transforms.Compose([
        transforms.ToTensor(),
    ])
    
    tensor_image = transform(image).unsqueeze(0)
    modified_tensor_image = torch.zeros_like(tensor_image)
    width = tensor_image.size(3)
    modified_tensor_image[:, :, :, :width // 2] = 0.0
    modified_tensor_image[:, :, :, width // 2:] = 1.0
    modified_image = transforms.ToPILImage()(modified_tensor_image.squeeze(0))

    return modified_image
'''
def modify_image(image_path):
    time.sleep(1)
    
    image = Image.open(image_path)
    width, height = image.size
    
    pixels = image.load()
    for i in range(0, width, 5):
        for j in range(0, height, 5):
            for x in range(i, i+5):
                for y in range(j, j+5):
                    if x < width and y < height:
                        pixels[x, y] = (0, 0, 0, 0)  # 设置像素为透明
    
    return image