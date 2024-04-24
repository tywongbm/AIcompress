from flask import Flask, render_template, request, send_file, jsonify
import io
import os
import shutil
import subprocess
from PIL import Image

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save('input_image.jpg')

    option1 = request.form.get('option1') #lossy or lossless
    option2 = request.form.get('option2') #compress or decompress
    option3 = request.form.get('option3') #vae or ae
    option4 = request.form.get('option4') #1(less quality) to 7(best quality)
    command = "dir" 


    if (option1 == "lossless" and option2 == "compress"):
        ### Modify here ###
        ### 输入文件名字是input.image.jpg，quality level是option3
        #command = "python" 
        print("hi")
    elif (option1 == "lossless" and option2 == "decompress"):
        ### Modify here ###
        #command = "python" 
        print("hi")

    elif (option1 == "lossy" and option2 == "compress"):
        command = "python lossy/compress.py"
    
    elif (option1 == "lossy" and option2 == "decompress"):
        command = "python lossy/test.py --model lossy/model/model_celeba.pth --img input_image.jpg --mask lossy/mask.png --output lossy/output --merge"
    
    else:
        print("Invalide options")
    
    subprocess.call(command, shell=True)
    ###如果输出文件不在根目录，可以用shutil.copy复制到根目录
    ###另外输出文件必须是ouput_image.jpg的名字
    if (option1 == "lossy" and option2 == "decompress"):
        shutil.copy("./lossy/output/result/result-input_image-mask.png", "./output_image.jpg")

    
    output_file_type = 'image'
    output_file_path = 'output_image.jpg'
    if (option1 == "lossless" and option2 == "compress"):
        output_file_type = 'python'
        output_file_path = 'output_file.py'
    
    return jsonify({'type': output_file_type, 'path': output_file_path})
    '''
    output_image = Image.open('output_image.jpg')

    try:
        output_buffer = io.BytesIO()
        output_image.save(output_buffer, format='JPEG')
        output_buffer.seek(0)
        return send_file(output_buffer, mimetype='image/jpeg', as_attachment=True, download_name='output_image.jpg')
    
    finally:
        if os.path.exists("input_image.jpg"):
            os.remove("input_image.jpg")
            print("input_image.jpg deleted.")
        if os.path.exists("output_image.jpg"):
            os.remove("output_image.jpg")
            print("output_image.jpg deleted.")
'''

@app.route('/download/<file_type>/<file_path>', methods=['GET'])
def download_file(file_type, file_path):

    if file_type == 'image':
        output_image = open(file_path, 'rb') 
        return send_file(io.BytesIO(output_image.read()), mimetype='image/jpeg', as_attachment=True, download_name='output_image.jpg')
    elif file_type == 'python':
        output_python = open(file_path, 'rb') 
        return send_file(io.BytesIO(output_python.read()), mimetype='text/x-python', as_attachment=True, download_name='output_file.py')
    else:
        return jsonify({'message': 'Invalid file type requested'}), 400
    


if __name__ == '__main__':
    app.run()