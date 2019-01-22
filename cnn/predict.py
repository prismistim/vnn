import cv2
import numpy as np
from keras.models import load_model
from keras import backend as k
import os

layer_name = 'conv2d_2'

def gradcam(x):
    # TODO: 最終の畳み込み層のレイヤー名を取る
    k.clear_session()

    print(os.path.abspath(os.path.dirname(__file__)) + '\model.h5')

    #linuxの場合パスの指定は'/'だが、Winは\なので注意
    model = load_model(os.path.abspath(os.path.dirname(__file__)) + '\model.h5')
    model.summary()

    x = np.expand_dims(x, axis=0)
    x = x.reshape(x.shape[0], 64, 64, 3)

    predictions = model.predict(x)
    class_idx = np.argmax(predictions[0])

    conv_output = model.get_layer(layer_name).output
    class_output = model.output[:, class_idx]
    grads = k.gradients(class_output, conv_output)[0]
    gradient_function = k.function([model.input], [conv_output, grads])

    output, grads_val = gradient_function([x])
    output, grads_val = output[0], grads_val[0]

    weights = np.mean(grads_val, axis=(0, 1))
    cam = np.dot(output, weights)

    cam = np.maximum(cam, 0)
    cam = cam / np.max(cam)

    # jetcam = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
    # jetcam = cv2.cvtColor(jetcam, cv2.COLOR_BGR2RGB)

    return cam, class_idx

# def prediction(x):
#     # TODO: Grad-cam導入
#     k.clear_session()
#     model = load_model(os.path.abspath(os.path.dirname(__file__)) + '/model.h5')
#     x = np.expand_dims(x, axis=0)
#     x = x.reshape(x.shape[0], 64, 64, 3)
#     pred = model.predict(x)
#
#     blossoms = [
#         'cherry blossom',
#         'peach blossom',
#     ]
#
#     print(pred)
#     acc = str(pred[0])
#     res = blossoms[np.argmax(pred)]
#
#     data = dict(result=res, acuracy=acc)
#     return data