import numpy as np
from keras.models import load_model
from keras import backend as k
import os
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session

config = tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True))
session = tf.Session(config=config)
config.gpu_options.visible_device_list = "0,1"
set_session(session)


def prediction(x):
    k.clear_session()
    model = load_model(os.path.abspath(os.path.dirname(__file__)) + '/model.h5')
    x = np.expand_dims(x, axis=0)
    x = x.reshape(x.shape[0], 64, 64, 3)
    pred = model.predict(x)

    blossoms = [
        'cherry blossom',
        'peach blossom',
    ]

    print(pred)
    acc = str(pred[0])
    res = blossoms[np.argmax(pred)]

    data = dict(result=res, acuracy=acc)
    return data