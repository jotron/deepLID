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
def make_samples(sample_pointers, input_path, total_output_path, sample_duration=5*16000):
    
    # all files
    print("function call")
    paths = get_paths(input_path)
    print("got paths")
    
    # all pointers
    for i, pointer in enumerate(sample_pointers):
        
         # all samples, labels
        sample = np.zeros((1, sample_duration))
        
        file = paths[pointer[0]]
        file_start = pointer[1]

        part, sr = librosa.load(file, sr=16000, offset=file_start, duration=5.0)
        sample[0,:len(part)] = part
        
        if not os.path.exists(total_output_path):
            os.makedirs(total_output_path)
        np.save(os.path.join(total_output_path, os.path.basename(file))+ str(file_start), sample)

      