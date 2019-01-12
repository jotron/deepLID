import keras
from keras import models, layers
from keras.optimizers import RMSprop
import numpy as np
from kapre.time_frequency import Melspectrogram
from kapre.augmentation import AdditiveNoise
from kapre.utils import Normalization2D
from keras import regularizers

# For effortless data importing
import sys
import os
sys.path.append('../')
from utils import DataFeed

# to avoid different initizialization of weights
np.random.seed(42)


# Stop when accuracy doesnt't improve in five epochs straight
# Always keep the best model saved on disk
callbacks = [keras.callbacks.EarlyStopping(monitor='val_acc', patience=5),
             keras.callbacks.ModelCheckpoint('berlin_net_train.h5', monitor='val_loss', save_best_only=True)]


data_path = '../preprocessing/preprocessed_data'

# Import Data
train_data, train_labels = DataFeed.Dataset.create(data_path, ['train/voxforge', 'train/youtube'], num=50000, use_premade=True)
val_data, val_labels = DataFeed.Dataset.create(data_path, ['val/youtube', 'val/voxforge'], num=-1, shuffle=True)

# Define Model
model = models.Sequential()
model.add(Melspectrogram(n_dft=512, input_shape=(1, 5 * 16000,),
                         padding='same', sr=16000, n_mels=28,
                         fmin=0.0, fmax=10000, power_melgram=1.0,
                         return_decibel_melgram=True, trainable_fb=False,
                         trainable_kernel=False))
model.add(Normalization2D(str_axis='data_sample'))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.Dropout(0.3))
model.add(layers.Flatten())
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.Dense(3, activation='softmax'))
model.summary()

model.compile(optimizer=RMSprop(),
              metrics=['accuracy'],
              loss='categorical_crossentropy')

# Train Model
if __name__ == '__main__':
    history = model.fit(x=train_data,
                        y=train_labels,
                        batch_size=128, 
                        epochs=20,
                        verbose=2,
                        validation_data=(val_data, val_labels), 
                        shuffle=True,
                        callbacks=callbacks)