from datetime import datetime
import cv2
import re
import base64
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
from cnn import predict
from PIL import Image
from io import BytesIO

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    # TODO: jinja2でmodelのクラス名などを読み込む

    if request.method == 'POST':
        upload_file = request.form['img']
        upload_file = re.search(r'base64,(.*)', upload_file).group(1)
        decode_file = base64.b64decode(upload_file)
        # decode_img = Image.open(BytesIO(decode_file))
        # decode_img.show()
        answer = get_answer(decode_file)

        return answer
    else:
        return render_template('index.html')

def get_answer(req):
    array = np.fromstring(req, np.uint8)
    img_src = cv2.imdecode(array, cv2.IMREAD_COLOR)
    # img_roll = 255 - img_src
    # img_gray = cv2.cvtColor(img_roll, cv2.COLOR_BGR2GRAY)
    img_resize = cv2.resize(img_src, (64, 64))
    # cv2.imwrite(f"images/{datetime.now().strftime('%s')}.jpg", img_resize)
    ans = predict.prediction(img_resize)
    return ans

if __name__ == "__main__":
    # app.debug = True
    app.run(host="192.168.13.117", port=5550)