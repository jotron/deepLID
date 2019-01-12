from comet_ml import Experiment
import keras
from keras import models, layers
from keras.optimizers import RMSprop
import numpy as np
from kapre.time_frequency import Melspectrogram
from kapre.augmentation import AdditiveNoise
from kapre.utils import Normalization2D
from keras import regularizers
from keras.regularizers import l2

import sys
import os
sys.path.append('../')
from utils import DataFeed

# to avoid different initizialization of weights
np.random.seed(42)

callbacks = [keras.callbacks.EarlyStopping(monitor='val_acc', patience=5),
             keras.callbacks.ModelCheckpoint('conv2d_to_rnn_decibel.h5', monitor='val_loss', save_best_only=True)]


data_path = '../preprocessing/preprocessed_data'

train_data, train_labels = DataFeed.Dataset.create(data_path, ['train/voxforge', 'train/youtube'], num=50000, use_premade=True)
val_data, val_labels = DataFeed.Dataset.create(data_path, ['val/youtube', 'val/voxforge'], num=-1, shuffle=True)

weight_decay = 0.01

model1 = models.Sequential()
model1.add(Melspectrogram(n_dft=512, input_shape=(1, 5 * 16000,),
                         padding='same', sr=16000, n_mels=32,
                         fmin=0.0, fmax=5000, power_melgram=1.0,
                         return_decibel_melgram=True, trainable_fb=False,
                         trainable_kernel=False))
model1.add(Normalization2D(str_axis='data_sample'))

model1.add(layers.Conv2D(16, (4, 4), activation='relu', padding='same', kernel_regularizer=l2(weight_decay)))
model1.add(layers.MaxPooling2D((2, 2 )))
model1.add(layers.BatchNormalization())

model1.add(layers.Conv2D(32, (2, 2), activation='relu', padding='same', kernel_regularizer=l2(weight_decay)))
model1.add(layers.MaxPooling2D((2, 1)))
model1.add(layers.BatchNormalization())

model1.add(layers.Conv2D(32, (2, 2), activation='relu', padding='same', kernel_regularizer=l2(weight_decay)))
model1.add(layers.MaxPooling2D((2, 1)))
model1.add(layers.BatchNormalization())

model1.add(layers.Conv2D(64, (2, 2), activation='relu', padding='same', kernel_regularizer=l2(weight_decay)))
model1.add(layers.MaxPooling2D((2, 1)))
model1.add(layers.BatchNormalization())

model1.add(layers.Conv2D(64, (2, 2), activation='relu', padding='same', kernel_regularizer=l2(weight_decay)))
model1.add(layers.MaxPooling2D((2, 1)))
model1.add(layers.BatchNormalization())

model1.add(layers.Reshape((-1, 64)))
model1.add(layers.GRU(64, dropout=0.3))
model1.add(layers.Dense(3, activation='softmax'))
#model.summary()

model.compile(optimizer=RMSprop(),
              metrics=['accuracy'],
              loss='categorical_crossentropy')

if __name__ == '__main__':
    history = model.fit(x=train_data,
                        y=train_labels,
                        batch_size=64, 
                        epochs=25,
                        verbose=2,
                        validation_data=(val_data, val_labels), 
                        shuffle=True,
                        callbacks=callbacks)