import cv2
import numpy as np
import os

current_directory = os.getcwd()
#input_image_path = os.path.join(current_directory, "./input_image.jpg")
#mask_image_path = os.path.join(current_directory, "./lossy/mask.png")

input_image = cv2.imread(current_directory + "./input_image.jpg")
masking_image = cv2.imread(current_directory + "./lossy/mask.png", 0)  # 以灰度模式读取掩码图像

# 缩小图像：将黑色块对应的像素删除，生成缩小后的图像
masked_image = cv2.bitwise_and(input_image, input_image, mask=masking_image)
#cv2.imwrite('masked_output.jpg', masked_image)

# 还原图像：将掩码区域内的像素还原为白色
restored_image = np.where(masking_image[..., None] > 0, masked_image, 255)
#restored_image_path = os.path.join(current_directory, "./compressed_image.jpg")
cv2.imwrite(current_directory + "./output_image.jpg", restored_image)