import random

from input_reader.InitDataSet import InitDataSet
from input_reader.Models import *


def train_test_doa(doas, percent):
    doas_train = []
    doas_test = []

    indexes_nr = len(doas[0].channels[0].trials)
    indexes = [i for i in range(indexes_nr)]
    random.shuffle(indexes)
    test_size = int(indexes_nr * percent)
    ind_test = indexes[-test_size:]
    # print('debug')

    for doa in doas:
        doa_train = DOA(doa.level)
        doa_test = DOA(doa.level)
        for channel in doa.channels:
            ch_train = Channel(channel.number)
            ch_test = Channel(channel.number)
            for index in range(indexes_nr):
                if index in ind_test:
                    # put trials in doa_test
                    ch_test.trials.append(channel.trials[index])
                else:
                    # put trials in doa_train
                    ch_train.trials.append(channel.trials[index])
            doa_train.channels.append(ch_train)
            doa_test.channels.append(ch_test)
        doas_train.append(doa_train)
        doas_test.append(doa_test)

    print('debug')
    return doas_train, doas_test, ind_test

# initialization = InitDataSet()
# doas = initialization.get_dataset_as_doas()
# train_test_doa(doas, 0.33)