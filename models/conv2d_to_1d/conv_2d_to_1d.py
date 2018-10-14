from comet_ml import Experiment
import keras
from keras import models, layers
from keras.optimizers import RMSprop
import numpy as np
from kapre.time_frequency import Melspectrogram
from kapre.augmentation import AdditiveNoise
from kapre.utils import Normalization2D
from keras import regularizers

import sys
import os
sys.path.append('../')
from utils import DataFeed

# to avoid different initizialization of weights
np.random.seed(42)

# monitoring
experiment = Experiment(api_key="P9qHCZEUF514fowP4zfVDbGBl",
                        project_name="conv_2d_to_1d", workspace="jotron")

callback_stopearly = keras.callbacks.EarlyStopping(monitor='val_acc',
                                                   patience=4)


data_path = '../preprocessing/preprocessed_data'

train_data, train_labels = DataFeed.Dataset.create(data_path, ['train/voxforge', 'train/youtube'], num=50000, use_premade=True)
val_data, val_labels = DataFeed.Dataset.create(data_path, ['val/youtube', 'val/voxforge'], num=-1, shuffle=True)

model = models.Sequential()
model.add(Melspectrogram(n_dft=512, input_shape=(1, 5 * 16000,),
                         padding='same', sr=16000, n_mels=28,
                         fmin=0.0, fmax=10000, power_melgram=1.0,
                         return_decibel_melgram=False, trainable_fb=False,
                         trainable_kernel=False))
#model.add(layers.SpatialDropout2D(0.2))
model.add(layers.SeparableConv2D(128, (5, 1), activation='relu'))
model.add(layers.MaxPooling2D((3, 1)))
#model.add(layers.SpatialDropout2D(0.2))
model.add(layers.SeparableConv2D(128, (5, 1), activation='relu'))
model.add(layers.MaxPooling2D((4, 1)))
model.add(layers.Reshape((-1, 128)))
#model.add(layers.SpatialDropout2D(0.2))
model.add(layers.SeparableConv1D(128, 14, activation='relu'))
model.add(layers.MaxPooling1D(4))
model.add(layers.SeparableConv1D(128, 14, activation='relu'))
model.add(layers.MaxPooling1D(4))
model.add(layers.SeparableConv1D(128, 14, activation='relu'))
model.add(layers.MaxPooling1D(2))
model.add(layers.Flatten())
model.add(layers.Dense(3, activation='softmax'))

model.compile(optimizer=RMSprop(lr=0.003, decay=1e-4),
              metrics=['accuracy'],
              loss='categorical_crossentropy')

if __name__ == '__main__':
    history = model.fit(x=train_data,
                        y=train_labels,
                        batch_size=128, 
                        epochs=13,
                        verbose=2,
                        validation_data=(val_data, val_labels), 
                        shuffle=True,
                        callbacks=[callback_stopearly])