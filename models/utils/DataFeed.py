import glob
import re
import os
import keras
import numpy as np
import pickle
from keras.preprocessing.image import ImageDataGenerator
from kapre.time_frequency import Melspectrogram
from keras import models, layers

# Data Generator Helper Class: Continually loads batches of data to train
# This is particularly useful if your data is to large to fit into RAM
# Help found: https://stanford.edu/~shervine/blog/keras-how-to-generate-data-on-the-fly
class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    
    def __init__(self, path, sources, num=-1, batch_size=32, dim=(1, 80000), shuffle=True, data_augmentation=False):
        """
        Initialization:
            dim=(1,80000) comes from 5s * sr = 5*16000
            data_augmentation is not working!
        """
        self.dim = dim
        self.batch_size = batch_size
        self.path = path
        self.shuffle = shuffle
        self.sources = sources
        self.data_augmentation = data_augmentation
        
        # Scrap Samples with labels in path
        # id_list contains all paths
        self.id_list, self.labels = self.scan_path()
        
        # Abstraction of id_list, only paths with their index in indexes will actually be used
        self.indexes = np.arange(len(self.id_list))
        
        # If a certain number of samples is specified
        if num != -1 and num != len(self.indexes):
            # Make a random selection of indexes
            self.indexes = np.random.choice(self.indexes, num, replace=False)
        
        # If Data aufmentation enabled -> NOT WORKING!
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
        
        # If enabled reshuffle data
        self.on_epoch_end()
        
    def scan_path(self):
        """
        Fetches Files in path
        return array with paths and array with labels
        """
        # Head Directories to fetch data from
        source_pathes = [os.path.join(self.path, source)+'/**/*.npy' for source in self.sources]
        
        # List all files
        id_list = []
        for source_path in source_pathes:
            id_list += glob.glob(source_path, recursive=True)
            
        # Assign Labels to each file
        labels = {}
        # Regex expressions to find language of file
        regs = ['.*/fr/.*', '.*/en/.*', '.*/de/.*']
        # For all files, if regex matches, label=language
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
        'NOT WORKING! : supposed to augment data'
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
            x = np.load(ID)
            
            # If lenght of sample not totally 5s, correct
            if (len(x) > 80000):
                x = x[:80000]
            else:
                X[i, 0, :x.shape[1]] = x[0]

            # Store class
            y[i] = self.labels[ID]
        
        # Augment data if enabled
        if self.data_augmentation:
            X = self.data_augmentor(X)
        
        # returns samples, labels
        # to_categorical transforms array of form [0, 1, 2] to [[1,0,0],[0,1,0],[0,0,1]]
        return X, keras.utils.to_categorical(y, num_classes=3)

# Load all data at once
# Needs sufficient RAM, but slightly faster
class Dataset():
    @classmethod
    def create(self, path, sources, num=-1, dim=(1, 80000), shuffle=True, use_premade=False, make_premade=False):
        'Initialization'
        self.dim = dim
        self.path = path
        self.shuffle = shuffle
        self.sources = sources
        
        # Use a premade selection of samples saved on disk
        # Useful if wanting to compare models, that aren't training on the whole dataset
        if use_premade:
            # Load selection
            with open (os.path.join(self.path,'premade_50000'), 'rb') as fp:
                self.id_list = pickle.load(fp)
            # Count number of samples
            self.num = len(self.id_list)
            # Get labels
            self.labels = self.labelize()
            # Create indexes abstraction
            self.indexes = np.arange(self.num)
            
        else:
            # Find all samples in path
            self.id_list, self.labels = self.scan_path()
            # Create index abstraction, only indexed samples will be used
            self.indexes = np.arange(len(self.id_list))
        
            # shuffle if enabled
            if shuffle:
                np.random.shuffle(self.indexes)
        
            # Num==-1 means use all data
            if num == -1:
                self.num = len(self.id_list)
            else:
                self.num=num
                
            # Just take the first num of indexes
            self.indexes = self.indexes[:num]
            
            # If enabled, save selection
            if make_premade:
                self.save_premade()
        
        # Return Set from selection
        return self.set_generation()
    
    @classmethod
    def set_generation(self):
        # Empty array for inputs
        dataset = np.empty((self.num, 1, 80000), dtype='float16')
        # Empty array for outputs
        targets = np.zeros((self.num, 3), dtype='float16')
        
        # For all samples
        for i, index in enumerate(self.indexes):
            # Get path of sample (ID)
            ID = self.id_list[index]
            
            # Load sample and store in dataset
            dataset[i,] = np.load(ID)

            # Store class of sample
            targets[i, self.labels[ID]] = 1.0
        
        # return data, targets
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
        # Regex expressions to find language of file
        regs = ['.*/fr/.*', '.*/en/.*', '.*/de/.*']
        # For all files, if regex matches, label=language
        for i, ID in enumerate(id_list):
            i = 0
            while not re.match(regs[i], ID):
                i+=1
                
            labels[ID] = i
        
        # return list of paths and labels
        return id_list, labels
    
    @classmethod
    def labelize(self):
        'used whit premade selection, get labels from paths'
        # Assign Labels to each file
        labels = {}
        # Regex expressions to find language of file
        regs = ['.*/fr/.*', '.*/en/.*', '.*/de/.*']
        # For all files, if regex matches, label=language
        for i, ID in enumerate(self.id_list):
            i = 0
            while not re.match(regs[i], ID):
                i+=1
                
            labels[ID] = i
        
        return labels
    
    @classmethod
    def save_premade(self):
        'Save premade set on disk'
        # Get paths from indexes-abstraction
        id_list = [self.id_list[i] for i in self.indexes]
        # Save selection as blob with pickle
        with open('../preprocessing/preprocessed_data/premade_50000', 'wb') as fp:
            pickle.dump(id_list, fp)