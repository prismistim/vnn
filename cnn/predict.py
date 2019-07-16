import os, cv2, re
import numpy as np
from keras.applications.vgg16 import VGG16, preprocess_input, decode_predictions
from keras.models import load_model
from keras.layers.core import Lambda
from keras import backend as k


def predict(x, model):
    k.clear_session()

    # modelの読み込みとレイヤーの指定
    if model == 'vgg':
        model = VGG16(weights='imagenet')
    else:
        model = load_model(os.path.abspath(os.path.dirname(__file__)) + '/model.h5')
    
    pattern = r"conv"
    repattern = re.compile(pattern)

    for layer in model.layers:
        if repattern.match(layer.name):
            print("in")
            last_layer = layer.name
            print(last_layer)

    # modelの構成を表示
    model.summary()

    pre_x = np.expand_dims(x, axis=0)
    pre_x = preprocess_input(pre_x)

    # 推論/予測クラスの算出
    predictions = model.predict(pre_x)

    if model == VGG16:
        results = decode_predictions(predictions, top=1)[0]
        print(results)

    predict_class = np.argmax(predictions)

    cam, heatmap = gradcam(model, preprocess_input, predict_class, last_layer)

    return results, cam

def gradcam(input_model, image, category_index, last_layer):

    # クラス数
    nb_classes = 1000

    target_layer = lambda x: target_category_loss(x, category_index, nb_classes)

    # 引数のinput_modelの出力層の後にtarget_layerレイヤーを追加
    x = input_model.layers[-1].output
    x = Lambda(target_layer, output_shape=target_category_loss_output_shape)(x)
    model = keras.models.Models(input_model.layers[0].input, x)

    loss = k.sum(model.layers[-1].output)
    conv_output = [l for l in model.layers if l.name == last_layer][0].output

    grads = normalize(k.gradients(loss, conv_output)[0])
    gradient_function = k.function([model.layers[0].input], [conv_output, grads])

    output, grads_val = gradient_function([image])
    output, grads_val = output[0, :], grads_val[0, :, :, :]

    weights = np.mean(grads_val, axis = (0, 1))
    cam = np.zero(output_shape[0 : 2], dtype = np.float32)

    for i, w in enumerate(weights):
        cam += w * output[:, :, i]

    # 任意のサイズにリサイズ
    cam = cv2.resize(cam, (224, 224))
    cam = np.maximum(cam, 0)
    heatmap = (cam - np.min(cam)) / (np.max(cam) - np.min(cam))

    image = image[0, :]
    image -= np.min(image)

    image = np.minimum(image, 255)

    cam = cv2.applyColorMap(np.unit8(255 * heatmap), cv2.COLORMAP_JET)
    cam = np.float32(cam) + np.float32(image)

    cam = 255 * cam / np.max(cam)

    return np.uint8(cam), heatmap
