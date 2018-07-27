import os
import numpy as np
import librosa

# return list of files in directory
def get_paths(path):
    files = os.listdir(path)
    for i in range(len(files)):
        files[i] = os.path.join(path, files[i])
    return files

# returns duration in s of files
def get_duration(path, bitdepth=16, samplerate=16000):
    return os.path.getsize(path)/bitdepth*8/samplerate

# number of samples possible
def file_num_samples(file, min_duration=3.5, sample_duration=5, margin=0):
    duration = get_duration(file, 16, 16000)
    if duration < (margin*2+min_duration):
        return 0
    else:
        return int((duration+sample_duration-min_duration-2*margin) // 5)

# returns number of samples available
def get_num_samples(path, min_duration=3.5, sample_duration=5, margin=0):

    # for all files
    samples_per_language = 0
    for j, file in enumerate(get_paths(path)):

        # determine number of non_overlapping 5s samples
        num_signal_samples = file_num_samples(file, min_duration=min_duration, 
                                              sample_duration=sample_duration, margin=margin)

        # for every possible sample
        samples_per_language += num_signal_samples

    return samples_per_language

# get total time
def get_total_time(path):

    # for all files
    time = 0
    for j, file in enumerate(get_paths(path)):
        #load file with librosa
        duration = get_duration(file, 16, 16000)

        # for every possible sample
        time += duration

    return time / 3600

# returns array with files and indexes
def get_sample_pointers(path, min_duration=3.5, sample_duration=5, margin=0):
    # path, index, lang
    tot_num_samples = get_num_samples(path, min_duration=min_duration, margin=margin)
    sample_pointers = np.empty((tot_num_samples, 2), dtype='int32')
    print(tot_num_samples, min_duration, margin)
    
    sample_index = 0
    # for all files
    for j, file in enumerate(get_paths(path)):
        
        num_samples = file_num_samples(file, min_duration=min_duration, 
                                              sample_duration=sample_duration, margin=margin)
        
        for i in range(num_samples):
            start = margin+i*sample_duration
            sample_pointers[sample_index][0] = j
            sample_pointers[sample_index][1] = start
            sample_index += 1
            
    return sample_pointers
                        
# returns actual samples
def get_samples(sample_pointers, path, sample_duration=5*16000):
    
    # all files
    print("function call")
    paths = get_paths(path)
    print("got paths")
    
    # all samples, labels
    samples = np.zeros((len(sample_pointers), sample_duration))
    
    # all pointers
    for i, pointer in enumerate(sample_pointers):
        
        file = paths[pointer[0]]
        file_start = pointer[1]

        part, sr = librosa.load(file, sr=16000, offset=file_start, duration=5.0)
        samples[i,:len(part)] = part
        #print(i)
        
    return samples

def get_split(path, lang_index, num_training, num_validation, num_test, margin=0, min_duration=3.5):
    
    # relation
    division1 = num_training/(num_training+num_validation+num_test)
    division2 = (num_training+num_validation)/(num_training+num_validation+num_test)
    
    # Choice of samples
    print("pointers...")
    pointers = get_sample_pointers(path, min_duration=min_duration, margin=margin)
    train_pool, val_pool, test_pool = np.split(pointers, [int(len(pointers)*division1), int(len(pointers)*division2)])

    train_choice = np.random.choice(len(train_pool), num_training)
    val_choice = np.random.choice(len(val_pool), num_validation)
    test_choice = np.random.choice(len(test_pool), num_test)
    
    train_pointers = train_pool[train_choice]
    val_pointers = val_pool[val_choice]
    test_pointers = test_pool[test_choice]

    # Numpy arrays filled with samples
    print("samples...")
    train_data = get_samples(train_pointers, path)
    val_data = get_samples(val_pointers, path)
    test_data = get_samples(test_pointers, path)

    # labels
    train_labels = np.zeros((num_training, 3), dtype='float32')
    train_labels[:, lang_index] = 1.0
    
    val_labels = np.zeros((num_validation, 3), dtype='float32')
    val_labels[:, lang_index] = 1.0
    
    test_labels = np.zeros((num_test, 3), dtype='float32')
    test_labels[:, lang_index] = 1.0
    
    return train_data, train_labels, val_data, val_labels, test_data, test_labels

def compute_partitions(x, y):
    part = np.full((y), int(x//y), dtype='int32')
    part[-1] = int(x - ((y-1)*(x//y)))
    return part
      