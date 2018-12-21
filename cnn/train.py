# coding:utf-8

import keras
from keras.utils import np_utils
from keras.layers.convolutional import Conv2D, MaxPooling2D
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Flatten
from keras.preprocessing.image import array_to_img, img_to_array, list_pictures, load_img
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
import matplotlib.pyplot as plt
from keras.backend.tensorflow_backend import set_session

config = tf.ConfigProto(gpu_options=tf.GPUOptions(allow_growth=True))
session = tf.Session(config=config)
config.gpu_options.visible_device_list = "0,1"
set_session(session)

x = []
y = []

# class cherry
for pictures in list_pictures('./scrapping/get_image/cherry blossom/'):
    img = img_to_array(load_img(pictures, target_size=(64, 64)))
    x.append(img)
    y.append(0)

# class peach
for pictures in list_pictures('./scrapping/get_image/peach blossom/'):
    img = img_to_array(load_img(pictures, target_size=(64, 64)))
    x.append(img)
    y.append(1)

x = np.asarray(x)
y = np.asarray(y)

# 画素値変換
x = x.astype('float32')
x = x / 255.0

y = np_utils.to_categorical(y, 2)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.33, random_state=111)

# モデル
model = Sequential()

kernel_size = (3, 3)
max_pool_size = (2, 2)

model.add(Conv2D(32, kernel_size, padding='same', input_shape=x_train.shape[1:]))
model.add(Activation('relu'))
model.add(Conv2D(32, kernel_size))
model.add(Activation('relu'))
model.add(MaxPooling2D(pool_size=max_pool_size))

model.add(Flatten())
model.add(Dense(128))
model.add(Activation('relu'))
model.add(Dropout(0.5))
model.add(Dense(2)) # 2class
model.add(Activation('softmax'))

model.summary()

#compile
model.compile(loss='categorical_crossentropy', optimizer='SGD', metrics=['accuracy'])

history = model.fit(x_train, y_train, batch_size=5, epochs=60, validation_data= (x_test, y_test))

plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.xlabel('epoch')
plt.ylabel('accuracy')
plt.legend(['acc', 'val_acc'], loc='lower right')
plt.show()

score = model.evaluate(x_test, y_test, verbose=0)
print('test loss:', score[0])
print('test accuracy:', score[1])

model.summary()

model.save('./model.h5')
