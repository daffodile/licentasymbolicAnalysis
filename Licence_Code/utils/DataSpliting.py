import random
import sys

import numpy as np
import pandas as pd

from models.Models import *

MAX_NR_OF_TRIALS = 240


def obtain_features_labels_log(inputData, encoding):
    X = []
    Y = []

    for i in range(len(inputData.result.arrays)):
        for j in range(len(inputData.result.arrays[i].array)):
            X.append(np.asarray(
                np.log10([[v + 1 for v in r] for r in encoding.get_a(inputData.result.arrays[i].array[j], 1)])).ravel())
            Y.append(inputData.result.arrays[i].name)

    return pd.DataFrame(X), Y


def obtain_features_labels(inputData, encoding, selected_symbols=32):
    X = []
    Y = []

    for i in range(len(inputData.result.arrays)):
        for j in range(len(inputData.result.arrays[i].array)):
            X.append(np.asarray(
                encoding.get_a(inputData.result.arrays[i].array[j], selected_symbols=selected_symbols)).ravel())
            Y.append(inputData.result.arrays[i].name)

    return pd.DataFrame(X), Y


def obtain_features_labels_with_bursts_flags(inputData, encoding, selected_symbols=32):
    X = []
    Y = []

    for i in range(len(inputData.result.arrays)):
        for j in range(len(inputData.result.arrays[i].array_data)):
            X.append(np.asarray(encoding.get_a(inputData.result.arrays[i].array_data[j],
                                               inputData.result.arrays[i].array_validate[j],
                                               selected_symbols)).ravel())
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

    minim = MAX_NR_OF_TRIALS
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


def train_test_doa_check_trials(doas, percent):
    doas_train = []
    doas_test = []

    min_nr_of_trials = MAX_NR_OF_TRIALS
    for doa in doas:
        for channel in doa.channels:
            if min_nr_of_trials > len(channel.trials):
                min_nr_of_trials = len(channel.trials)

    needed_test_samples = int(percent * min_nr_of_trials)

    number_of_channels = len(doas[0].channels)
    for doa in doas:
        if len(doa.channels) != number_of_channels:
            print('DOAs in train_test_doa have different number of channels ', file=sys.stderr)
            sys.exit()

    trials_frequency = [[0 for i in range(MAX_NR_OF_TRIALS)] for j in range(len(doas))]

    for ind_doa, doa in enumerate(doas):
        for channel in doa.channels:
            for trial in channel.trials:
                trials_frequency[ind_doa][trial.trial_number - 1] += 1

    presence_of_trials = [True for i in range(MAX_NR_OF_TRIALS)]

    # mark the trials that are present in all DOAs
    for ind_doa in range(len(doas)):
        for ind_trial in range(MAX_NR_OF_TRIALS):
            presence_of_trials[ind_trial] &= (trials_frequency[ind_doa][ind_trial] == number_of_channels)

    all_trials_numbers = [i + 1 for i in range(MAX_NR_OF_TRIALS)]

    trials_common_to_all = []
    for tr_num in all_trials_numbers:
        if presence_of_trials[tr_num - 1]:
            trials_common_to_all.append(tr_num)

    len_trials_common_to_all = len(trials_common_to_all)
    if needed_test_samples > len_trials_common_to_all:
        ind_test = trials_common_to_all
    else:
        random.shuffle(trials_common_to_all)
        ind_test = trials_common_to_all[-needed_test_samples:]

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
