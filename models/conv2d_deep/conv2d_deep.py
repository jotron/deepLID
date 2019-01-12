from comet_ml import Experiment
import keras
from keras import models, layers
from keras.optimizers import RMSprop
import numpy as np
from kapre.time_frequency import Melspectrogram
from kapre.augmentation import AdditiveNoise
from kapre.utils import Normalization2D
from keras import regularizers
from keras.applications.mobilenetv2 import MobileNetV2

import sys
import os
sys.path.append('../')
from utils import DataFeed

# to avoid different initizialization of weights
np.random.seed(42)

callback_stopearly = keras.callbacks.EarlyStopping(monitor='val_acc',
                                                   patience=5)


data_path = '../preprocessing/preprocessed_data'

train_data, train_labels = DataFeed.Dataset.create(data_path, ['train/voxforge', 'train/youtube'], num=50000, use_premade=False)
val_data, val_labels = DataFeed.Dataset.create(data_path, ['val/youtube', 'val/voxforge'], num=-1, shuffle=True)

input_tensor = layers.Input(shape=(1, 80000))
x = Melspectrogram(n_dft=512,
                   padding='same', sr=16000, n_mels=223, n_hop=360,
                   fmin=0.0, fmax=10000, power_melgram=1.0,
                   return_decibel_melgram=False, trainable_fb=False,
                   trainable_kernel=False)(input_tensor)

inception_model = MobileNetV2(include_top=True, input_tensor=x, weights=None,
                              alpha=0.25, classes=3)

x = inception_model.output


model = models.Model(input_tensor, outputs=x)

model.compile(optimizer=RMSprop(),
              metrics=['accuracy'],
              loss='categorical_crossentropy')

if __name__ == '__main__':
    history = model.fit(x=train_data,
                        y=train_labels,
                        batch_size=64, 
                        epochs=13,
                        verbose=2,
                        validation_data=(val_data, val_labels), 
                        shuffle=True,
                        callbacks=[callback_stopearly])