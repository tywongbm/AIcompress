from PIL import Image

input_image_path = 'test_image_256.jpg'
output_image_path = 'test_image_256_smaller.jpg'

rgba_image = Image.open(input_image_path)
rgba_image.save(output_image_path, 'JPEG')
#rgba_image.save(output_image_path, 'JPEG', quality=100)

#其实就是用pil打开后重新保存，因为用了jpeg压缩算法来保存图像
#默认的quality是70，但哪怕设置成100，也仍然能缩小很多倍（test image从150kb降到50kb）。