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


def obtain_features_labels_from_doa(doas, channel_number, segment, encoding, selected_symbols=None):
    X = []
    Y = []

    for doa in doas:
        channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
        for trial in channel.trials:
            seg = getattr(trial, segment)
            X.append(np.asarray(encoding.get_a(seg.values, selected_symbols=selected_symbols)).ravel())
            Y.append(doa.level)

    return pd.DataFrame(X), np.array(Y)


def obtain_features_labels_from_doa_bursts_marks(doas, channel_number, segment, encoding, selected_symbols=None):
    X = []
    Y = []

    for doa in doas:
        channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
        for trial in channel.trials:
            seg = getattr(trial, segment)
            X.append(np.asarray(encoding.get_a(seg.values, seg.values_outsiders,
                                               selected_symbols=selected_symbols)).ravel())
            Y.append(doa.level)

    return pd.DataFrame(X), np.array(Y)


def obtain_A_features_from_doa_with_bursts_flags(doas, channel_number, segment, encoding, selected_symbols=None):
    X = []
    Y = []

    for doa in doas:
        channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
        for trial in channel.trials:
            seg = getattr(trial, segment)
            X.append(
                np.asarray(encoding.get_a(seg.values, seg.values_outsiders, selected_symbols=selected_symbols)).ravel())
            Y.append(doa.level)

    return pd.DataFrame(X), Y


def obtain_S_features_from_doa_with_bursts_flags(doas, channel_number, segment, encoding):
    X = []
    Y = []

    for doa in doas:
        channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
        for trial in channel.trials:
            seg = getattr(trial, segment)
            X.append(
                np.asarray(encoding.get_s(seg.values, seg.values_outsiders)).ravel())
            Y.append(doa.level)

    return pd.DataFrame(X), Y


def obtain_A_features_from_doa(doas, channel_number, encoding, segments=['spontaneous', 'stimulus'],
                               selected_symbols=None):
    X = []
    Y = []

    for doa in doas:
        channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
        for trial in channel.trials:
            # extract the values from the selected segments
            trial_values = []
            for segment in segments:
                seg = getattr(trial, segment)
                trial_values.extend(seg.values)
                # trial_values.extend( getattr(trial, segment).values)

            X.append(np.asarray(encoding.get_a(trial_values, selected_symbols=selected_symbols)).ravel())
            Y.append(doa.level)
            # if doa.level == 'deep1' or doa.level == 'deep2':
            #     Y.append('deep')
            # else:
            #     Y.append('medium')

    return pd.DataFrame(X), Y


def obtain_A_features_from_doa_check_bursts(doas, channel_number, encoding, segments=['spontaneous', 'stimulus'],
                                            selected_symbols=None):
    X = []
    Y = []

    for doa in doas:
        channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
        for trial in channel.trials:
            # extract the values from the selected segments
            trial_values = []
            outliers_values = []
            for segment in segments:
                seg = getattr(trial, segment)
                trial_values.extend(seg.values)
                outliers_values.extend(seg.values_outsiders)

            X.append(
                np.asarray(encoding.get_a(trial_values, outliers_values, selected_symbols=selected_symbols)).ravel())
            Y.append(doa.level)

    return pd.DataFrame(X), Y


#  METHOD TO BE CHECKED IN DEBUG!!!!!
def obtain_more_A_features_from_doa(doas, channel_number, encoding, segments=['spontaneous', 'stimulus'],
                                    selected_symbols=None):
    X = []
    Y = []

    for doa in doas:
        channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
        for trial in channel.trials:
            a_concatenate_matrix = []
            for segment in segments:
                seg = getattr(trial, segment)
                a_concatenate_matrix.extend(encoding.get_a(seg.values, selected_symbols=selected_symbols).flatten())
            X.append(np.asarray(a_concatenate_matrix))
            Y.append(doa.level)

    return pd.DataFrame(X), Y


def obtain_features_labels_with_bursts_flags(inputData, encoding, selected_symbols=32):
    X = []
    Y = []

    for i in range(len(inputData.result.arrays)):
        for j in range(len(inputData.result.arrays[i].array)):
            values_trial = inputData.result.arrays[i].array[j]
            flags_trial = inputData.result.arrays[i].array_validate[j]
            flatten_A_matrix = np.asarray(encoding.get_a(values_trial, flags_trial,
                                                         selected_symbols=selected_symbols)).ravel()
            X.append(flatten_A_matrix)
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


def obtain_S_TESPAR_features_from_doa(doas, channel_number, segment, encoding):
    X = []
    Y = []

    for doa in doas:
        channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
        for trial in channel.trials:
            seg = getattr(trial, segment)
            X.append(np.asarray(encoding.get_s(seg.values)).ravel())
            Y.append(doa.level)

    return pd.DataFrame(X), Y


def train_test_doa(doas, percent):
    doas_train = []
    doas_test = []

    minim = MAX_NR_OF_TRIALS
    for doa in doas:
        if minim > len(doa.channels[0].trials):
            minim = len(doa.channels[0].trials)

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

    print('train test split: trials common to all')
    print(trials_common_to_all)
    len_trials_common_to_all = len(trials_common_to_all)
    if needed_test_samples > len_trials_common_to_all:
        ind_test = trials_common_to_all
    else:
        # random.Random(4).shuffle(trials_common_to_all)
        random.shuffle(trials_common_to_all)
        ind_test = trials_common_to_all[-needed_test_samples:]
    print("train test split: trials in test")
    print(ind_test)
    print(f'test len {len(ind_test)}')
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


# balanced pethod PER COMMON TRIALS wrong wrong wrong

# def train_test_doa_balanced(doas, percent_train=0.8):
#     if percent_train < 0.0 or percent_train > 1.0:
#         print('train_test_doa_balanced: percent_train param should be a value in [0.0, 1.0]',
#               file=sys.stderr)
#         sys.exit()
#
#     doas_train = []
#     doas_test = []
#
#     min_nr_of_trials = MAX_NR_OF_TRIALS
#     for doa in doas:
#         for channel in doa.channels:
#             if min_nr_of_trials > len(channel.trials):
#                 min_nr_of_trials = len(channel.trials)
#
#     needed_train_samples = int(percent_train * min_nr_of_trials)
#     print(f"Needed train samples {needed_train_samples}")
#
#     number_of_channels = len(doas[0].channels)
#
#     for doa in doas:
#         if len(doa.channels) != number_of_channels:
#             print('DOAs in train_test_doa have different number of channels ', file=sys.stderr)
#             sys.exit()
#
#     trials_frequency = [[0 for i in range(MAX_NR_OF_TRIALS)] for j in range(len(doas))]
#
#     for ind_doa, doa in enumerate(doas):
#         for channel in doa.channels:
#             for trial in channel.trials:
#                 trials_frequency[ind_doa][trial.trial_number - 1] += 1
#
#     presence_of_trials = [True for i in range(MAX_NR_OF_TRIALS)]
#
#     # mark the trials that are present in all DOAs
#     for ind_doa in range(len(doas)):
#         for ind_trial in range(MAX_NR_OF_TRIALS):
#             presence_of_trials[ind_trial] &= (trials_frequency[ind_doa][ind_trial] == number_of_channels)
#
#     all_trials_numbers = [i + 1 for i in range(MAX_NR_OF_TRIALS)]
#
#     trials_common_to_all = []
#     for tr_num in all_trials_numbers:
#         if presence_of_trials[tr_num - 1]:
#             trials_common_to_all.append(tr_num)
#
#     print('train test split: trials common to all')
#     print(trials_common_to_all)
#     len_trials_common_to_all = len(trials_common_to_all)
#     # establish how many trials to have in train
#     if needed_train_samples > len_trials_common_to_all:
#         ind_train = trials_common_to_all
#     else:
#         # random.Random(4).shuffle(trials_common_to_all)
#         random.shuffle(trials_common_to_all)
#         ind_train = trials_common_to_all[-needed_train_samples:]
#     print(f"train test split: nr of trials in train per class {len(ind_train)}")
#     print(ind_train)
#     for doa in doas:
#         doa_train = DOA(doa.level)
#         doa_test = DOA(doa.level)
#         for channel in doa.channels:
#             ch_train = Channel(channel.number)
#             ch_test = Channel(channel.number)
#             for trial in channel.trials:
#                 if trial.trial_number not in ind_train:
#                     # put trials in doa_test
#                     ch_test.trials.append(trial)
#                 else:
#                     # put trials in doa_train
#                     ch_train.trials.append(trial)
#             doa_train.channels.append(ch_train)
#             doa_test.channels.append(ch_test)
#         doas_train.append(doa_train)
#         doas_test.append(doa_test)
#
#     for doa in doas_test:
#         print(f'{doa.level} test size: {len(doa.channels[0].trials)}')
#
#     return doas_train, doas_test, ind_train

def train_test_doa_remake_balanced(doas, percent_train=0.8):
    if percent_train < 0.0 or percent_train > 1.0:
        print('train_test_doa_balanced: percent_train param should be a value in [0.0, 1.0]',
              file=sys.stderr)
        sys.exit()

    doas_train = []
    doas_test = []

    # find which doa has the minimum number of trials so we determine the BALANCED size of TRAIN set
    min_nr_of_trials = MAX_NR_OF_TRIALS
    for doa in doas:
        for channel in doa.channels:
            if min_nr_of_trials > len(channel.trials):
                min_nr_of_trials = len(channel.trials)

    # numbers of train trials from one DOA (class)
    train_size = int(percent_train * min_nr_of_trials)
    print(f"\n train_test_doa_remake_balanced {train_size} TRAIN size per DOA \n")

    number_of_channels = len(doas[0].channels)

    for doa in doas:
        if len(doa.channels) != number_of_channels:
            print('DOAs in train_test_doa have different number of channels ', file=sys.stderr)
            sys.exit()

    for ind_doa, doa in enumerate(doas):

        # count how many times a trial appean over the channels
        trials_frequency = [0 for i in range(MAX_NR_OF_TRIALS)]

        for channel in doa.channels:
            for trial in channel.trials:
                trials_frequency[trial.trial_number - 1] += 1

        all_trials_numbers = [i + 1 for i in range(MAX_NR_OF_TRIALS)]

        # array of trial numbers that are present in each channel of the DOA
        trials_common_to_all_channels = []

        for tr_num in all_trials_numbers:
            if trials_frequency[tr_num - 1] is number_of_channels:
                trials_common_to_all_channels.append(tr_num)

        print(f'{doa.level} train test split: trials in all channels: {len(trials_common_to_all_channels)}')
        # print(trials_common_to_all_channels)
        len_comm_trials = len(trials_common_to_all_channels)

        # establish how many trials to have in train
        if train_size > len_comm_trials:
            print(f'###############################################################################')
            print(f'in {doa.level} the trials common to channels are less than the desired train size')
            print(f'train size ={train_size}  trials on channels ={len_comm_trials}')
            print(f'###############################################################################')
            ind_train = trials_common_to_all_channels
        else:
            # random.Random(4).shuffle(trials_common_to_all)
            random.shuffle(trials_common_to_all_channels)

            ind_train = trials_common_to_all_channels[-train_size:]

        print(f'{doa.level} train trials: ')
        print(ind_train)

        doa_train = DOA(doa.level)
        doa_test = DOA(doa.level)
        for channel in doa.channels:
            ch_train = Channel(channel.number)
            ch_test = Channel(channel.number)
            for trial in channel.trials:
                if trial.trial_number not in ind_train:
                    # put trials in doa_test
                    ch_test.trials.append(trial)
                else:
                    # put trials in doa_train
                    ch_train.trials.append(trial)
            doa_train.channels.append(ch_train)
            doa_test.channels.append(ch_test)
        doas_train.append(doa_train)
        doas_test.append(doa_test)

    for doa in doas_test:
        print(f'{doa.level} test size: {len(doa.channels[0].trials)}')

    return doas_train, doas_test
