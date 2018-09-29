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
                        project_name="all_dense", workspace="jotron")

callback_stopearly = keras.callbacks.EarlyStopping(monitor='val_acc',
                                                   patience=4)


data_path = '../preprocessing/preprocessed_data'

train_data, train_labels = DataFeed.Dataset.create(data_path, ['train/voxforge', 'train/youtube'], num=50000, use_premade=True)
val_data, val_labels = DataFeed.Dataset.create(data_path, ['val/youtube', 'val/voxforge'], num=-1, shuffle=True)


model = models.Sequential()
model.add(layers.Flatten())
model.add(layers.Dropout(0.5))
model.add(layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.0001)))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.0001)))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.0001)))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l2(0.0001)))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(256, activation='relu', kernel_regularizer=regularizers.l1(0.0005)))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(3, activation='softmax'))

model.compile(optimizer=RMSprop(),
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