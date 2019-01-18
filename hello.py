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
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    # TODO: jinja2でmodelのクラス名などを読み込む

    if request.method == 'POST':
        upload_file = request.files['imageFile'].read()
        # upload_file = Image.open(io.BytesIO(upload_file))
        # upload_file = re.search(r'base64,(.*)', upload_file).group(1)
        # decode_file = base64.b64decode(upload_file)
        # decode_img = Image.open(BytesIO(decode_file))
        # decode_img.show()
        score, gene_image_array = get_answer(upload_file)
        print(gene_image_array)

        gene_image = Image.fromarray(np.uint8(gene_image_array))
        gene_image.save('/home/murashige/Workspace/vnn/result.png')
        gene_buf = io.BytesIO()

        gene_image.save(gene_buf, format="PNG")
        gene_image = gene_buf.getvalue()

        gene_b64 = base64.b64encode(gene_image).decode("utf-8")
        gene_image_data = "data:image/png;base64,{}".format(gene_b64)

        return render_template('index.html', gene_image_data=gene_image_data)

    else:
        return redirect(url_for('index'))

def get_answer(req):
    # 元画像をデコード
    img_bistream = io.BytesIO(req)
    img_pil = Image.open(img_bistream)
    img_numpy = np.asarray(img_pil)
    img_original = cv2.cvtColor(img_numpy, cv2.COLOR_RGBA2BGR)

    array = np.fromstring(req, np.uint8)
    img_src = cv2.imdecode(array, cv2.IMREAD_COLOR)

    # img_roll = 255 - img_src
    # img_gray = cv2.cvtColor(img_roll, cv2.COLOR_BGR2GRAY)
    img_resize = cv2.resize(img_src, (64, 64))
    # cv2.imwrite(f"images/{datetime.now().strftime('%s')}.jpg", img_resize)
    heat, score = predict.gradcam(img_resize)

    heat = cv2.resize(heat, (img_original.shape[1], img_original.shape[0]))
    heat = cv2.applyColorMap(np.uint8(255 * heat), cv2.COLORMAP_JET)

    merged = (np.float32(heat) + img_original / 2)

    return score, merged

if __name__ == "__main__":
    # app.debug = True
    app.run(host="192.168.13.117", port=5550)