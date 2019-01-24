import os
import numpy as np
import librosa

# returns list of files in directory
def get_paths(path):
    files = os.listdir(path)
    for i in range(len(files)):
        files[i] = os.path.join(path, files[i])
    return files

# returns duration in s of file at path
def get_duration(path, bitdepth=16, samplerate=16000):
    return os.path.getsize(path)/bitdepth*8/samplerate

# returns number of subsamples possible (in one file)
def file_num_samples(file, min_duration=3.5, sample_duration=5, margin=0):
    duration = get_duration(file, 16, 16000)
    # file is too small
    if duration < (margin*2+min_duration):
        return 0
    else:
        return int((duration+sample_duration-min_duration-2*margin) // 5)

# returns number of samples available in path
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

# returns sum of duration of all files in path
def get_total_time(path):

    # for all files
    time = 0
    for j, file in enumerate(get_paths(path)):
        # individual duration
        duration = get_duration(file, 16, 16000)

        # sum up every possible sample
        time += duration

    return time / 3600

# returns array with files and indexes
def get_sample_pointers(path, min_duration=3.5, sample_duration=5, margin=0):
    # number of samples available in path
    tot_num_samples = get_num_samples(path, min_duration=min_duration, margin=margin)
    # Empty array to hole index of all samples
    sample_pointers = np.empty((tot_num_samples, 2), dtype='int32')
    # Log number of samples
    print(tot_num_samples, min_duration, margin)
    
    # index goes over all subsamples
    sample_index = 0
    # for all files
    for j, file in enumerate(get_paths(path)):
        
        # compute number of subsamples in file
        num_samples = file_num_samples(file, min_duration=min_duration, 
                                              sample_duration=sample_duration, margin=margin)
        
        # for every subsample
        for i in range(num_samples):
            # start of sample in file
            start = margin+i*sample_duration
            # first dimension refers to index of the file
            sample_pointers[sample_index][0] = j
            # second dimentsion refers to starting point inside file
            sample_pointers[sample_index][1] = start
            # go to next index
            sample_index += 1
            
    # Sample pointers has shape:
    # [[index of file a, start of sample in file a], [index of file b, start of sample in file b], ...]
    # index of files is relative to order in operating system
            
    return sample_pointers
                        
# returns actual samples
def make_samples(sample_pointers, input_path, total_output_path, sample_duration=5*16000):
    
    # Log function call
    print("function call")
    # Get all array of all files in path
    paths = get_paths(input_path)
    # Log end of first step
    print("got paths")
    
    # for all pointers that refer to subsamples
    for i, pointer in enumerate(sample_pointers):
        
        # Empty array to hold sample in the future
        sample = np.zeros((1, sample_duration))
        
        # process pointer
        file = paths[pointer[0]]
        file_start = pointer[1]
        
        # Load sample with librosa
        part, sr = librosa.load(file, sr=16000, offset=file_start, duration=5.0)
        
        # save sample in array
        sample[0,:len(part)] = part
        
        # save sample on disk in output path
        if not os.path.exists(total_output_path):
            os.makedirs(total_output_path)
        np.save(os.path.join(total_output_path, os.path.basename(file))+ str(file_start), sample)

      