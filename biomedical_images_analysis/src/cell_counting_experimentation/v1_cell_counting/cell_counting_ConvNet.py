#!/usr/bin/env python
# coding: utf-8

from __future__ import absolute_import, division, print_function

import pathlib
from skimage import io
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import os
import numpy as np
from tensorflow import keras
import tensorflow as tf
print(tf.__version__)

# path to Dataset
path = "/content/EDF_norm/"
files = os.listdir(path)
files = sorted([file for file in files if ".png" in file])
X = np.zeros(shape=(len(files), 800, 800, 1), dtype=np.float16)
for index, file in enumerate(files):
  image = io.imread(os.path.join(path, file))
  image = image / np.max(image)
  X[index, :, :, 0] = image

# X = np.array([ np.array(io.imread(path + fname)) for fname in files])
print(X.shape)

# read output / count labels
df = pd.read_csv('/content/output_frame_cells_count.csv')
Y = df['count'].values
Y.shape # type(Y)= numpy.ndarray



x_train = X[:75] # 75 images
x_test = X[75:90] # 25 images

y_train = Y[:75]
y_test = Y[75:90]



def build_model():
    model = keras.models.Sequential([
    keras.layers.Conv2D(16, kernel_size=(3,3), activation='relu', input_shape=(800,800, 1)),
    keras.layers.MaxPooling2D(pool_size=(2,2)),
    keras.layers.Dropout(0.25),
    keras.layers.Conv2D(32, kernel_size=(3,3), activation='relu'),
    keras.layers.MaxPool2D(pool_size=(2,2)),
    keras.layers.Dropout(0.25),
    keras.layers.Conv2D(64, kernel_size=(3,3), activation='relu'),
    keras.layers.MaxPool2D(pool_size=(2,2)),
    keras.layers.Dropout(0.5),
    keras.layers.Flatten(), 
    keras.layers.Dense(500, activation='relu'),
    keras.layers.Dense(1)
    ])
    
    model.compile(optimizer=keras.optimizers.Adam(lr=1e-04), loss='mean_squared_error', metrics=['accuracy'])
    return model

model = build_model()
model.summary()



class TestCallback(keras.callbacks.Callback):
    def __init__(self, test_data):
        self.test_data = test_data

    def on_epoch_end(self, epoch, logs={}):
        x, y = self.test_data
        loss, acc = self.model.evaluate(x, y, verbose=0)
        print('\nTesting loss: {}, acc: {}\n'.format(loss, acc))


        
# Training

EPOCHS = 3000
history = model.fit(
    x_train, y_train,
    epochs=EPOCHS, 
    validation_split = 0.2,
    verbose=2, 
    batch_size= 4,
    callbacks=[TestCallback((x_test, y_test))], 
)


# Model Evaluation on VALIDATINO dataset
print("*"*10, "  MODEL EVALUTION  ", "*"*10 )
print(model.evaluate(x_test, y_test) )


# TEST SCORE

print("*"*10, "  MODEL PREDICTIONS  ", "*"*10 )
print(model.predict(x_test), y_test)


# plot history

# hist = pd.DataFrame(history.history)
# hist['epoch'] = history.epoch￼
# hist.tail()
