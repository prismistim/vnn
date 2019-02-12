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

    pre_x = np.expand_dims(x, axis=0)
    pre_x = preprocess_input(pre_x)

    # 推論/予測クラスの算出
    if use_vgg == 1:
        predictions = model.predict(pre_x)
        results = decode_predictions(predictions, top=5)[0]
        print(results)

        class_idx = np.argmax(results)

    else:
        x = x.reshape(x.shape[0], 64, 64, 3)

        predictions = model.predict(x)
        class_idx = np.argmax(predictions[0])

    # 勾配を取得
    conv_output = model.get_layer(layer_name).output

    # class_idxはforの場合iに置き換える(単純に結果に対して番号を
    class_output = model.output[:, class_idx]

    grads = k.gradients(class_output, conv_output)[0]
    gradient_function = k.function([model.layers[0].input], [conv_output, grads])

    output, grads_val = gradient_function([pre_x])
    output, grads_val = output[0], grads_val[0]

    weights = np.mean(grads_val, axis=(0, 1))
    cam = np.dot(output, weights)

    if use_vgg == 1:
        cam = cv2.resize(cam, (224, 224))

    cam = np.maximum(cam, 0)

    if use_vgg == 1:
        return cam, results

    else:
        return cam, class_idx
