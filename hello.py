from datetime import datetime
import cv2
import re
import base64
from flask import Flask, render_template, request, redirect, url_for
import numpy as np
from cnn import predict

app = Flask(__name__)

@app.route('/')
def index():
    html = render_template('index.html')
    return html

@app.route('/toPostURL', methods=['POST'])
def post():
    if request.method == 'POST':
        img = get_image()
        answer = get_answer(img)
        return render_template('index.html')
    else:
        return redirect(url_for('index'))

def get_image():
    input_img = request.form['input_img'];
    response = Responce()
    response.status_code = 200
    return response

def get_answer(req):
    img_str = re.search(r'base64,(.*)', req.form['img']).group(1)
    nparr = np.fromstring(base64.b64decode(img_str), np.unit8)
    img_src = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    img_roll = 255 - img_src
    img_gray = cv2.cvtColor(img_roll, cv2.COLOR_BGR2GRAY)
    img_resize = cv2.resize(img_gray, (28, 28))
    # cv2.imwrite(f"images/{datetime.now().strftime('%s')}.jpg", img_resize)
    ans = predict.result(img_resize)
    return ans

if __name__ == "__main__":
    app.run(host="192.168.13.117", port=5880)