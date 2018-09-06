import glob
import re
import os
import keras
import numpy as np

class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    
    def __init__(self, path, sources, num=-1, batch_size=32, dim=(1, 80000), shuffle=True):
        'Initialization'
        self.dim = dim
        self.batch_size = batch_size
        self.path = path
        self.shuffle = shuffle
        self.sources = sources
        
        self.id_list, self.labels = self.scan_path()
        self.indexes = np.arange(len(self.id_list))
        
        # If a certain number of samples is specified
        if num != -1 and num != len(self.indexes):
            self.indexes = np.random.choice(self.indexes, num, replace=False)
            
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
        return int(np.floor(len(self.id_list) / self.batch_size))

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

        return X, keras.utils.to_categorical(y, num_classes=3)