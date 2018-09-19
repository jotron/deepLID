from comet_ml import Experiment
import keras
from keras import models, layers
from keras.optimizers import RMSprop
import numpy as np
from kapre.time_frequency import Melspectrogram
import sys
# Add the ptdraft folder path to the sys.path list
sys.path.append('../')
from DataFeed import DataGenerator, Dataset

# to avoid different initizialization of weights
np.random.seed(42)

# monitoring
experiment = Experiment(api_key="P9qHCZEUF514fowP4zfVDbGBl",
                        project_name="BerlinNetMelBn", workspace="jotron")



data_path='../preprocessing/preprocessed_data'

train_data, train_labels = Dataset.create(data_path, ['train/voxforge', 'train/youtube'], num=50000, use_premade=True)
val_data, val_labels = Dataset.create(data_path, ['val/youtube', 'val/voxforge'], num=10000, shuffle=True)

model = models.Sequential()
model.add(Melspectrogram(n_dft=512, input_shape=(1, 5 * 16000,),
                         padding='same', sr=16000, n_mels=28,
                         fmin=0.0, fmax=10000, power_melgram=1.0,
                         return_decibel_melgram=False, trainable_fb=False,
                         trainable_kernel=False))
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.BatchNormalization())
model.add(layers.Conv2D(64, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.BatchNormalization())
model.add(layers.Conv2D(128, (3, 3), activation='relu'))
model.add(layers.MaxPooling2D((2, 2)))
model.add(layers.BatchNormalization())
model.add(layers.Flatten())
model.add(layers.Dense(1024, activation='relu'))
model.add(layers.Dense(3, activation='softmax'))

model.compile(optimizer=RMSprop(),
              metrics=['accuracy'],
              loss='categorical_crossentropy')

if __name__ == '__main__':
    history = model.fit(x=train_data,
                        y=train_labels,
                        batch_size=128, 
                        epochs=12,
                        verbose=2,
                        validation_data=(val_data, val_labels), 
                        shuffle=True)