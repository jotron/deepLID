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
                        project_name="conv1d", workspace="jotron")

callback_stopearly = keras.callbacks.EarlyStopping(monitor='val_acc',
                                                   patience=5)


data_path = '../preprocessing/preprocessed_data'

train_data, train_labels = DataFeed.Dataset.create(data_path, ['train/voxforge', 'train/youtube'], num=50000, use_premade=True)
val_data, val_labels = DataFeed.Dataset.create(data_path, ['val/youtube', 'val/voxforge'], num=-1, shuffle=True)

train_data = train_data.reshape((50000, 80000, 1))
val_data= val_data.reshape((10000, 80000, 1))

model = models.Sequential()
model.add(layers.Conv1D(64, 20, activation='relu', input_shape=(80000, 1)))
model.add(layers.MaxPooling1D((4)))
model.add(layers.Conv1D(64, 20, activation='relu'))
model.add(layers.MaxPooling1D((4)))
#model.add(layers.Conv1D(64, 20, activation='relu'))
#model.add(layers.MaxPooling1D((4)))
#model.add(layers.Conv1D(64, 20, activation='relu'))
#model.add(layers.MaxPooling1D((4)))
#model.add(layers.Conv1D(64, 20, activation='relu'))
#model.add(layers.MaxPooling1D((4)))
#model.add(layers.Conv1D(64, 20, activation='relu'))
#model.add(layers.MaxPooling1D((4)))
model.add(layers.Flatten())
model.add(layers.Dropout(0.3))
#model.add(layers.Dense(512, activation='sigmoid'))
model.add(layers.Dense(3, activation='softmax'))

model.compile(optimizer=RMSprop(lr=0.001),
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