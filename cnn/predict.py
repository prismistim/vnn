import cv2
import numpy as np
from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.models import load_model
from keras import backend as k
import os

def gradcam(x, use_vgg):
    k.clear_session()

    # modelの読み込みとレイヤーの指定
    if use_vgg == 1:
        model = VGG16(weights='imagenet')

        # VGGの場合モデルの最終層はblock5_conv3
        layer_name = 'block5_conv3'

    else:
        model = load_model(os.path.abspath(os.path.dirname(__file__)) + '/model.h5')
        layer_name = 'conv2d_2'

    # modelの構成を表示
    model.summary()

    x = np.expand_dims(x, axis=0)

    # 推論 / 予測クラスの算出
    if use_vgg == 1:
        x = np.array(x, dtype=np.float)

        predictions = model.predict(preprocess_input(x))
        results = decode_predictions(predictions, top=5)[0]

        class_idx = np.argmax(results)

    else :
        x = x.reshape(x.shape[0], 64, 64, 3)

        predictions = model.predict(x)
        class_idx = np.argmax(predictions[0])

    # 勾配を取得
    conv_output = model.get_layer(layer_name).output
    class_output = model.output[:, class_idx]
    grads = k.gradients(class_output, conv_output)[0]
    gradient_function = k.function([model.input], [conv_output, grads])

    output, grads_val = gradient_function([x])
    output, grads_val = output[0], grads_val[0]

    weights = np.mean(grads_val, axis=(0, 1))
    cam = np.dot(output, weights)

    if use_vgg == 1:
        cam = cv2.resize(cam, (224, 224))

    cam = np.maximum(cam, 0)

    # jetcam = cv2.applyColorMap(np.uint8(255 * cam), cv2.COLORMAP_JET)
    # jetcam = cv2.cvtColor(jetcam, cv2.COLOR_BGR2RGB)

    if use_vgg == 1:
        print(results)
        return cam, results

    else :
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