from datetime import datetime
from typing import Dict, Any

import cv2
import re
import base64
from flask import Flask, render_template, request, redirect, jsonify, url_for
import numpy as np
from cnn import predict
from cnn import grad_cam
from PIL import Image
import io
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session
from tensorflow.python.keras.preprocessing import image

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
    if request.method == 'POST':
        upload_file = request.files['imageFile'].read()
        # TODO: modelファイルの読み込み

        if request.form['use_model'] == '1':
            model = 'vgg'
        else :
            model = ''

        model = ''

        # 推論結果を取得
        score, gene_image_array = get_answer(upload_file, model)

        # array to Image
        gene_image_array = cv2.cvtColor(gene_image_array, cv2.COLOR_RGB2BGR)
        gene_image = Image.fromarray(np.uint8(gene_image_array))
        gene_image.save('./img/temp/result.png')

        gene_buf = io.BytesIO()
        gene_image.save(gene_buf, format="PNG")
        gene_image = gene_buf.getvalue()
        gene_b64 = base64.b64encode(gene_image).decode("utf-8")
        gene_image_data = "data:image/png;base64,{}".format(gene_b64)

        score_str = str(round(score[0][2], 4))

        return jsonify(gene_image_data=gene_image_data, class_name=score[0][1], score=score_str)

    else:
        return redirect(url_for('index'))

def get_answer(req, model):
    # 元画像をデコード
    img_bistream = io.BytesIO(req)

    if model == 'vgg':
        resize_size = 224
    else:
        resize_size = 48

    img_keras = image.load_img(img_bistream, target_size=(resize_size, resize_size))

    # if model == 'vgg':
    #     img_prend = cv2.imdecode(img_keras, cv2.IMREAD_COLOR)
    # else:
    #     img_keras = cv2.cvtColor(np.float32(img_keras), cv2.COLOR_RGB2GRAY)

    score, cam = predict.predict(img_keras, model)

    return score, cam


if __name__ == "__main__":
    # app.debug = True
    app.run(host="0.0.0.0", port=7000)
