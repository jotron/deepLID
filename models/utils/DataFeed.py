import glob
import re
import os
import keras
import numpy as np
import pickle
from keras.preprocessing.image import ImageDataGenerator
from kapre.time_frequency import Melspectrogram
from keras import models, layers


class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    
    def __init__(self, path, sources, num=-1, batch_size=32, dim=(1, 80000), shuffle=True, data_augmentation=False):
        'Initialization'
        self.dim = dim
        self.batch_size = batch_size
        self.path = path
        self.shuffle = shuffle
        self.sources = sources
        self.data_augmentation = data_augmentation
        
        self.id_list, self.labels = self.scan_path()
        self.indexes = np.arange(len(self.id_list))
        
        # If a certain number of samples is specified
        if num != -1 and num != len(self.indexes):
            self.indexes = np.random.choice(self.indexes, num, replace=False)
            
        if data_augmentation:
            self.datagen = ImageDataGenerator(
                            featurewise_center=True,
                            featurewise_std_normalization=True,
                            rotation_range=20,
                            width_shift_range=0.2,
                            height_shift_range=0.2,
                            horizontal_flip=True)
            self.model = models.Sequential([Melspectrogram(n_dft=512, input_shape=(1,80000),
                         padding='same', sr=16000, n_mels=192, n_hop=418,
                         fmin=0.0, fmax=8000, power_melgram=1.0,
                         return_decibel_melgram=False, trainable_fb=False,
                         trainable_kernel=False)])
            self.model.compile('SGD', loss='binary_crossentropy')
            
        self.on_epoch_end()
    def scan_path(self):
        # Head Directories to fetch data from
        source_pathes = [os.path.join(self.path, source)+'/**/*.npy' for source in self.sources]
        
        # List all files
        id_list = []
        for source_path in source_pathes:
            id_list += glob.glob(source_path, recursive=True)
            
        # Assign Labels to each file
        labels = {}
        regs = ['.*/fr/.*', '.*/en/.*', '.*/de/.*']
        for i, ID in enumerate(id_list):
            i = 0
            while not re.match(regs[i], ID):
                i+=1
                
            labels[ID] = i
        
        return id_list, labels
        

    def __len__(self):
        'Denotes the number of batches per epoch'
        return int(np.floor(len(self.indexes) / self.batch_size))

    def __getitem__(self, index):
        'Generate one batch of data'
        # Generate indexes of the batch
        indexes = self.indexes[index*self.batch_size:(index+1)*self.batch_size]

        # Find list of IDs
        id_list_temp = [self.id_list[k] for k in indexes]

        # Generate data
        X, y = self.__data_generation(id_list_temp)

        return X, y

    def on_epoch_end(self):
        'Updates indexes after each epoch'
        if self.shuffle == True:
            np.random.shuffle(self.indexes)
            
    def data_augmentor(self, x):
        x = self.model.predict_on_batch(x)
        x = self.datagen.flow(x, batch_size=32)[0]
        return x
    def __data_generation(self, id_list_temp):
        'Generates data containing batch_size samples' 
        # Initialization
        X = np.empty((self.batch_size, *self.dim))
        y = np.empty((self.batch_size), dtype=int)

        # Generate data
        for i, ID in enumerate(id_list_temp):
            # Store sample
            X[i,] = np.load(ID)

            # Store class
            y[i] = self.labels[ID]
        
        if self.data_augmentation:
            X = self.data_augmentor(X)

        return X, keras.utils.to_categorical(y, num_classes=3)
    
class Dataset():
    @classmethod
    def create(self, path, sources, num=-1, dim=(1, 80000), shuffle=True, use_premade=False, make_premade=False):
        'Initialization'
        self.dim = dim
        self.path = path
        self.shuffle = shuffle
        self.sources = sources
        
        if use_premade:
            with open (os.path.join(self.path,'premade_50000'), 'rb') as fp:
                self.id_list = pickle.load(fp)
            self.num = len(self.id_list)
            self.labels = self.labelize()
            self.indexes = np.arange(self.num)
            
        else:
            self.id_list, self.labels = self.scan_path()
            self.indexes = np.arange(len(self.id_list))
        
            #shuffle
            if shuffle:
                np.random.shuffle(self.indexes)
        
            #only take num
            if num == -1:
                self.num = len(self.id_list)
            else:
                self.num=num
            self.indexes = self.indexes[:num]
            
            if make_premade:
                self.save_premade()
            
        return self.set_generation()
    @classmethod
    def set_generation(self):
        dataset = np.empty((self.num, 1, 80000), dtype='float16')
        targets = np.zeros((self.num, 3), dtype='float16')
        
        for i, index in enumerate(self.indexes):
            # get id
            ID = self.id_list[index]
            
            # Store sample
            dataset[i,] = np.load(ID)

            # Store class
            targets[i, self.labels[ID]] = 1.0
            
        return dataset, targets
        
    @classmethod    
    def scan_path(self):
        # Head Directories to fetch data from
        source_pathes = [os.path.join(self.path, source)+'/**/*.npy' for source in self.sources]
        
        # List all files
        id_list = []
        for source_path in source_pathes:
            id_list += glob.glob(source_path, recursive=True)
            
        # Assign Labels to each file
        labels = {}
        regs = ['.*/fr/.*', '.*/en/.*', '.*/de/.*']
        for i, ID in enumerate(id_list):
            i = 0
            while not re.match(regs[i], ID):
                i+=1
                
            labels[ID] = i
        
        return id_list, labels
    
    @classmethod
    def labelize(self):
        labels = {}
        regs = ['.*/fr/.*', '.*/en/.*', '.*/de/.*']
        for i, ID in enumerate(self.id_list):
            i = 0
            while not re.match(regs[i], ID):
                i+=1
                
            labels[ID] = i
        
        return labels
    
    @classmethod
    def save_premade(self):
        id_list = [self.id_list[i] for i in self.indexes]
        with open('../preprocessing/preprocessed_data/premade_50000', 'wb') as fp:
            pickle.dump(id_list, fp)