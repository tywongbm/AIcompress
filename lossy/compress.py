import cv2
import numpy as np

# 读取输入图像和掩码图像
input_image = cv2.imread('../input_image.jpg')
masking_image = cv2.imread('./mask.png', 0)  # 以灰度模式读取掩码图像

# 缩小图像
masked_image = cv2.bitwise_and(input_image, input_image, mask=masking_image)
# 将黑色块对应的像素删除，生成缩小后的图像

# 还原图像
restored_image = np.where(masking_image[..., None] > 0, masked_image, 255)
# 将掩码区域内的像素还原为白色

# 保存缩小后的图像
#cv2.imwrite('masked_output.jpg', masked_image)

# 保存还原后的图像
cv2.imwrite('../compressed_image.jpg', restored_image)