from datetime import datetime
from typing import Dict, Any

import cv2
import re
import base64
from flask import Flask, render_template, request, redirect, jsonify
import numpy as np
from cnn import predict
from PIL import Image
import io

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
        answer = get_answer(upload_file)

        return jsonify(answer)

def get_answer(req):
    array = np.fromstring(req, np.uint8)
    img_src = cv2.imdecode(array, cv2.IMREAD_COLOR)
    # img_roll = 255 - img_src
    # img_gray = cv2.cvtColor(img_roll, cv2.COLOR_BGR2GRAY)
    img_resize = cv2.resize(img_src, (64, 64))
    # cv2.imwrite(f"images/{datetime.now().strftime('%s')}.jpg", img_resize)
    heat, score = predict.prediction(img_resize)
    marged = (np.float32(heat) + req / 2)
    return score, marged

if __name__ == "__main__":
    # app.debug = True
    app.run(host="192.168.13.117", port=5550)