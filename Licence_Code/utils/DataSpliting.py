import random
import numpy as np
import pandas as pd

from input_reader.InitDataSet import InitDataSet
from input_reader.Models import *


def obtain_features_labels_log(inputData, encoding):
    X = []
    Y = []

    for i in range(len(inputData.result.arrays)):
        for j in range(len(inputData.result.arrays[i].array)):
            X.append(np.asarray(
                np.log10([[v + 1 for v in r] for r in encoding.get_a(inputData.result.arrays[i].array[j], 1)])).ravel())
            Y.append(inputData.result.arrays[i].name)

    return pd.DataFrame(X), Y


def obtain_features_labels(inputData, encoding):
    X = []
    Y = []

    for i in range(len(inputData.result.arrays)):
        for j in range(len(inputData.result.arrays[i].array_data)):
            X.append(np.asarray(encoding.get_a(inputData.result.arrays[i].array_data[j],
                                               inputData.result.arrays[i].array_validate[j])).ravel())
            Y.append(inputData.result.arrays[i].name)

    return pd.DataFrame(X), Y

def obtain_S_TESPAR_features(inputData, encoding):
    X = []
    Y = []

    for i in range(len(inputData.result.arrays)):
        for j in range(len(inputData.result.arrays[i].array)):
            X.append(np.asarray(encoding.get_s(inputData.result.arrays[i].array[j])))
            Y.append(inputData.result.arrays[i].name)

    return pd.DataFrame(X), Y

def train_test_doa(doas, percent):
    doas_train = []
    doas_test = []

    minim = 240
    for doa in doas:
        if minim > len(doas[0].channels[0].trials):
            minim = len(doas[0].channels[0].trials)

    indexes = [i for i in range(minim)]
    random.shuffle(indexes)
    test_size = int(minim * percent)
    ind_test = indexes[-test_size:]
    # print('debug')

    for doa in doas:
        doa_train = DOA(doa.level)
        doa_test = DOA(doa.level)
        for channel in doa.channels:
            ch_train = Channel(channel.number)
            ch_test = Channel(channel.number)
            for index in range(len(channel.trials)):
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

    # print('debug')
    return doas_train, doas_test, ind_test

# initialization = InitDataSet()
# doas = initialization.get_dataset_as_doas()
# train_test_doa(doas, 0.33)
