from datetime import datetime
from typing import Dict, Any

import cv2
import re
import base64
from flask import Flask, render_template, request, redirect, jsonify, url_for
import numpy as np
from cnn import predict
from PIL import Image
import io
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session

config = tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True))
session = tf.Session(config=config)
config.gpu_options.visible_device_list = "0,1"
set_session(session)

app = Flask(__name__)

@app.route('/')
def index():
    username = 'snowsphere'
    return render_template('index.html', username=username)

@app.route('/result', methods=['POST'])
def result():
    # TODO: jinja2でmodelのクラス名などを読み込む

    if request.method == 'POST':
        upload_file = request.files['imageFile'].read()
        use_vgg = 1
        # upload_file = Image.open(io.BytesIO(upload_file))
        # upload_file = re.search(r'base64,(.*)', upload_file).group(1)
        # decode_file = base64.b64decode(upload_file)
        # decode_img = Image.open(BytesIO(decode_file))
        # decode_img.show()
        score, gene_image_array = get_answer(upload_file, use_vgg)
        print(gene_image_array)

        gene_image = Image.fromarray(np.uint8(gene_image_array))
        gene_image.save('/home/murashige/Workspace/vnn/result.png')
        gene_buf = io.BytesIO()

        gene_image.save(gene_buf, format="PNG")
        gene_image = gene_buf.getvalue()

        gene_b64 = base64.b64encode(gene_image).decode("utf-8")
        gene_image_data = "data:image/png;base64,{}".format(gene_b64)

        score = str(score)

        return jsonify(gene_image_data=gene_image_data, score=score)

    else:
        return redirect(url_for('index'))

def get_answer(req, use_vgg):
    # 元画像をデコード
    img_bistream = io.BytesIO(req)
    img_pil = Image.open(img_bistream)
    img_numpy = np.asarray(img_pil)
    img_original = cv2.cvtColor(img_numpy, cv2.COLOR_RGBA2BGR)

    array = np.fromstring(req, np.uint8)
    img_src = cv2.imdecode(array, cv2.IMREAD_COLOR)

    # img_roll = 255 - img_src
    # img_gray = cv2.cvtColor(img_roll, cv2.COLOR_BGR2GRAY)
    if use_vgg == 1:
        resize_size = 224
    else:
        resize_size = 64
    img_resize = cv2.resize(img_src, (resize_size, resize_size))
    # cv2.imwrite(f"images/{datetime.now().strftime('%s')}.jpg", img_resize)
    cam, score = predict.gradcam(img_resize, use_vgg)
    heat = cam / np.max(cam)

    # cam = cv2.resize(cam, (img_original.shape[1], img_original.shape[0]), cv2.INTER_LINEAR)
    cam = cv2.applyColorMap(np.uint8(255 * heat), cv2.COLORMAP_JET)

    cam = np.float32(cam) + np.float32(img_original)
    cam = 255 * cam / np.max(cam)

    return score, np.uint8(cam)

if __name__ == "__main__":
    # app.debug = True
    app.run(host="192.168.13.117", port=5550)