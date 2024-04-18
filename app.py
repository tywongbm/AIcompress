from flask import Flask, render_template, request, send_file
import io
from process import modify_image


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    processed_image = modify_image(file)
    processed_image.save('test.jpg')

    output_buffer = io.BytesIO()
    processed_image.save(output_buffer, format='JPEG')
    output_buffer.seek(0)

    return send_file(output_buffer, mimetype='image/jpeg', as_attachment=True, download_name='process_iamge.jpg')


if __name__ == '__main__':
    app.run()