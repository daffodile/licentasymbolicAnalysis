import os
import sys

import numpy as np

# file in which to save the shuffled indexes and from where to read them
from input_reader.InitDataSet import InitDataSet
from models.Models import DOA, Channel

file_indexes = 'test_indexes.txt'

'''
    the above sequence shuffles the indexes and save them in a txt file
'''


# import random
# trials_numbers = [i + 1 for i in range(240)]
# random.shuffle(trials_numbers)
# f = open(file_indexes, "w")
# for d in trials_numbers:
#     f.write(str(d) + " ")
#
# f.close()

def get_test_indexes(percent=0.2):
    '''
    :param percent: how many of the trials are gonna be used as test trials
    :return: the test indexes
    '''
    if percent < 0.0 or percent > 1.0:
        print(
            'get_test_indexes: percent param should be a value in [0.0, 1.0] that represents the percent of trials used for testing',
            file=sys.stderr)
        sys.exit()
    indexes = np.loadtxt(fname=file_indexes, dtype='i')
    count_indexes = int(percent * len(indexes))
    return indexes[0:count_indexes]

def train_test_doa_consistent(doas, pecent):
    ind_test = get_test_indexes(pecent)

    doas_train = []
    doas_test = []

    for doa in doas:
        doa_train = DOA(doa.level)
        doa_test = DOA(doa.level)
        for channel in doa.channels:
            ch_train = Channel(channel.number)
            ch_test = Channel(channel.number)
            for trial in channel.trials:
                if trial.trial_number in ind_test:
                    # put trials in doa_test
                    ch_test.trials.append(trial)
                else:
                    # put trials in doa_train
                    ch_train.trials.append(trial)
            doa_train.channels.append(ch_train)
            doa_test.channels.append(ch_test)
        doas_train.append(doa_train)
        doas_test.append(doa_test)

    return doas_train, doas_test, ind_test


###################### call this method of spliting train test doas
data_dir = os.path.join('.', '..')

initialization = InitDataSet(data_dir=data_dir)
doas = initialization.get_dataset_as_doas()
doas_train, doas_test, ind_test = train_test_doa_consistent(doas, 0.2)
