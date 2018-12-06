# 取得した画像を

import glob
import traceback

import numpy as np
import sys
from PIL import Image

photo_count = 250

X = []
Y = []

def convert_image(folder, label, count):
    images = glob.glob('./get_image/' + folder + '/*.jpg')

    for i, image in enumerate(images):
        if i >
