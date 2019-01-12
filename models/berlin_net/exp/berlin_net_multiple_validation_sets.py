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
# experiment = Experiment(api_key="P9qHCZEUF514fowP4zfVDbGBl",
#                        project_name="BerlinNetMelBn", workspace="jotron")


# Let's you validate Accuracy on multiple validationsets simultaneously -> for comparison
class AdditionalValidationSets(keras.callbacks.Callback):
    def __init__(self, validation_sets, verbose=0, batch_size=None):
        """
        Source: https://stackoverflow.com/questions/47731935/using-multiple-validation-sets-with-keras
        :param validation_sets:
        a list of 3-tuples (validation_data, validation_targets, validation_set_name)
        or 4-tuples (validation_data, validation_targets, sample_weights, validation_set_name)
        :param verbose:
        verbosity mode, 1 or 0
        :param batch_size:
        batch size to be used when evaluating on the additional datasets
        """
        super(AdditionalValidationSets, self).__init__()
        self.validation_sets = validation_sets
        for validation_set in self.validation_sets:
            if len(validation_set) not in [2, 3]:
                raise ValueError()
        self.epoch = []
        self.history = {}
        self.verbose = verbose
        self.batch_size = batch_size

    def on_train_begin(self, logs=None):
        self.epoch = []
        self.history = {}

    def on_epoch_end(self, epoch, logs=None):
        logs = logs or {}
        self.epoch.append(epoch)

        # record the same values as History() as well
        for k, v in logs.items():
            self.history.setdefault(k, []).append(v)

        # evaluate on the additional validation sets
        for validation_set in self.validation_sets:
            if len(validation_set) == 3:
                validation_data, validation_targets, validation_set_name = validation_set
                sample_weights = None
            elif len(validation_set) == 4:
                validation_data, validation_targets, sample_weights, validation_set_name = validation_set
            else:
                raise ValueError()

            results = self.model.evaluate(x=validation_data,
                                          y=validation_targets,
                                          verbose=self.verbose,
                                          sample_weight=sample_weights,
                                          batch_size=self.batch_size)

            for i, result in enumerate(results):
                if i == 0:
                    valuename = validation_set_name + '_loss'
                else:
                    valuename = validation_set_name + '_' + self.model.metrics[i-1].__name__
                self.history.setdefault(valuename, []).append(result)


data_path = '../preprocessing/preprocessed_data'

training_generator = DataFeed.DataGenerator(data_path, ['train/voxforge', 'train/youtube'], num=-1, batch_size=64)
val_data, val_labels = DataFeed.Dataset.create(data_path, ['test/guru'], num=-1, shuffle=True)
val_data2, val_labels2 = DataFeed.Dataset.create(data_path, ['val/librivox'], num=-1, shuffle=True)

callbacks = [keras.callbacks.EarlyStopping(monitor='val_acc', patience=5),
             keras.callbacks.ModelCheckpoint('berlin_net_custom.h5', monitor='val_loss', save_best_only=True),
             AdditionalValidationSets([(val_data2, val_labels2, 'librivox')], verbose=1)]

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

model.compile(optimizer=RMSprop(),
              metrics=['accuracy'],
              loss='categorical_crossentropy')

if __name__ == '__main__':
    history = model.fit_generator(generator=training_generator,
                        epochs=13,
                        verbose=2,
                        validation_data=(val_data[:-1], val_labels[:-1]), 
                        shuffle=True,
                        use_multiprocessing=True,
                        workers=8,
                        max_queue_size=20,          
                        callbacks=callbacks)