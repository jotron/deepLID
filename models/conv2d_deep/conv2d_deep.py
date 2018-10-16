from comet_ml import Experiment
import keras
from keras import models, layers
from keras.optimizers import RMSprop
import numpy as np
from kapre.time_frequency import Melspectrogram
from kapre.augmentation import AdditiveNoise
from kapre.utils import Normalization2D
from keras import regularizers
from keras_contrib.applications.resnet import ResNet18, ResNet

import sys
import os
sys.path.append('../')
from utils import DataFeed

# to avoid different initizialization of weights
np.random.seed(42)

# monitoring
experiment = Experiment(api_key="P9qHCZEUF514fowP4zfVDbGBl",
                        project_name="conv2d_deep", workspace="jotron")

callback_stopearly = keras.callbacks.EarlyStopping(monitor='val_acc',
                                                   patience=5)


data_path = '../preprocessing/preprocessed_data'

train_data, train_labels = DataFeed.Dataset.create(data_path, ['train/voxforge', 'train/youtube'], num=50000, use_premade=False)
val_data, val_labels = DataFeed.Dataset.create(data_path, ['val/youtube', 'val/voxforge'], num=-1, shuffle=True)

model = models.Sequential()
model.add(Melspectrogram(n_dft=512, input_shape=(1, 5 * 16000,),
                         padding='same', sr=16000, n_mels=192, n_hop=418,
                         fmin=0.0, fmax=8000, power_melgram=1.0,
                         return_decibel_melgram=False, trainable_fb=False,
                         trainable_kernel=False))
model.add(ResNet(input_shape=(192, 192, 1), classes=3, block='basic', repetitions=[2, 2, 2], dropout=0.5))

model.compile(optimizer=RMSprop(lr=0.001, decay=1e-8),
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