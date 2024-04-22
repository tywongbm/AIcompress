from flask import Flask, render_template, request, send_file
import io
from process import modify_image
import subprocess


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    file.save('input_image.jpg')


    ###### Modify the following code to test your model ######
    command = "python lossy/test.py --model lossy/model/model_celeba.pth --img input_image.jpg --mask lossy/mask.png --output lossy/output --merge"
    subprocess.call(command, shell=True)
    output_path = 'lossy/output/result/result-input_image-mask.png'



    return send_file(output_path, mimetype='image/jpeg', as_attachment=True, download_name='process_iamge.jpg')

'''
    output_buffer = io.BytesIO()
    processed_image.save(output_buffer, format='JPEG')
    output_buffer.seek(0)

    return send_file(output_buffer, mimetype='image/jpeg', as_attachment=True, download_name='process_iamge.jpg')
'''

if __name__ == '__main__':
    app.run()