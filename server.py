from flask import Flask, render_template, request, send_file
import os
import shutil
from process import modify_image
import subprocess

current_directory = os.getcwd()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save('input_image.jpg')

    option1 = request.form.get('option1')

    if (option1 == "lossless"):
        ### Modify Here
        '''
        command = "python" 
        subprocess.call(command, shell=True)
        '''
        print("hi")
    elif (option1 == "lossy"):
        command1 = "python lossy/compress.py"
        subprocess.call(command1, shell=True)
        command2 = "python lossy/test.py --model lossy/model/model_celeba.pth --img compressed_image.jpg --mask lossy/mask.png --output lossy/output --merge"
        subprocess.call(command2, shell=True)
        shutil.copy(current_directory + "./lossy/output/result/result-compressed_image-mask.png", current_directory + "./decompressed_image.jpg")
    else:
        print("Invalide options")

    compressed_image_path = current_directory+'./compressed_image.jpg'
    decompressed_image_path = current_directory+'./decompressed_image.jpg'
    
    try:
        #compressed_image = send_file(compressed_image_path, mimetype='image/jpeg', as_attachment=True, download_name='compressed_image.jpg')
        #decompressed_image = send_file(decompressed_image_path, mimetype='image/jpeg', as_attachment=True, download_name='decompressed_image.jpg')
        #return [compressed_image, decompressed_image]
        return {
            'compressed_image_path': compressed_image_path,
            'decompressed_image_path': decompressed_image_path
        }
    
    finally:
        #os.remove("input_image.jpg")
        print("input_image.jpg deleted.")
        #os.remove("compressed_image.jpg")
        print("compressed_image.jpg deleted.")
        #os.remove("decompressed_image.jpg")
        print("decompressed_image.jpg deleted.")
        #shutil.rmtree("lossy/output") #删除整个文件夹，如果lossless也有文件夹要删的话可以用这个指令
        print("lossy/output folder deleted.")
        
'''
    output_buffer = io.BytesIO()
    processed_image.save(output_buffer, format='JPEG')
    output_buffer.seek(0)

    return send_file(output_buffer, mimetype='image/jpeg', as_attachment=True, download_name='process_iamge.jpg')
'''

if __name__ == '__main__':
    app.run()