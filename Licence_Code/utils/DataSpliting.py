import random
import numpy as np
import pandas as pd
from matplotlib.cbook import flatten

from input_reader.Models import *

MAX_NR_OF_TRIALS = 240


def obtain_features_labels_log(inputData, encoding, selected_symbols=32):
    X = []
    Y = []

    for i in range(len(inputData.result.arrays)):
        for j in range(len(inputData.result.arrays[i].array_data)):
            X.append(np.asarray(
                np.log10([[v + 1 for v in r] for r in encoding.get_a(inputData.result.arrays[i].array_data[j],
                                                                     inputData.result.arrays[i].array_validate[j],
                                                                     selected_symbols=selected_symbols)])).ravel())
            Y.append(inputData.result.arrays[i].name)

    return pd.DataFrame(X), Y


def obtain_A_features_from_doa_emphasize_stimulus(doas, channel_number, encoding, selected_symbols=None):
    X = []
    Y = []

    for doa in doas:
        channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
        for trial in channel.trials:
            # extract the values from the selected segments
            trial_spontaneous = getattr(trial, 'spontaneous').values
            trial_spontaneous_validate = getattr(trial, 'spontaneous').values_outsiders
            trial_stimulus = getattr(trial, 'stimulus').values
            trial_stimulus_validate = getattr(trial, 'stimulus').values_outsiders

            scale_f = len(trial_stimulus) / len(trial_spontaneous)  # scale to multiply spontaneous with

            a_spontaneous = np.asarray(encoding.get_a(trial_spontaneous,trial_spontaneous_validate, selected_symbols=selected_symbols))
            a_stimulus = np.asarray(encoding.get_a(trial_stimulus, trial_stimulus_validate,selected_symbols=selected_symbols))

            a_spontaneous = a_spontaneous * scale_f

            a_feature = a_stimulus - a_spontaneous
            X.append(a_feature.ravel())
            Y.append(doa.level)

    return pd.DataFrame(X), Y


def obtain_features_labels(inputData, encoding, selected_symbols=32):
    X = []
    Y = []

    for i in range(len(inputData.result.arrays)):
        for j in range(len(inputData.result.arrays[i].array_data)):
            X.append(np.asarray(encoding.get_a(inputData.result.arrays[i].array_data[j],
                                               inputData.result.arrays[i].array_validate[j],
                                               selected_symbols=selected_symbols)).ravel())
            # if(inputData.result.arrays[i].name == 'deep1' or inputData.result.arrays[i].name == 'deep2'):
            #     Y.append('deep')
            # else:
            #     Y.append('medium')
            Y.append(inputData.result.arrays[i].name)
    return pd.DataFrame(X), Y


def obtain_features_labels_quality(inputData, encoding, selected_symbols=32):
    X = []
    Y = []

    for i in range(len(inputData.result.arrays)):
        for j in range(len(inputData.result.arrays[i].array_data)):
            Tespar_features = np.asarray(encoding.get_a(inputData.result.arrays[i].array_data[j],
                                                        inputData.result.arrays[i].array_validate[j],
                                                        selected_symbols=selected_symbols))

            Tespar_features = Tespar_features.ravel()

            quality_feature = [np.count_nonzero(inputData.result.arrays[i].array_validate[j])]
            # nu e necesar pentru DTC sa normalizez
            # quality_feature = (len(inputData.result.arrays[i].array_validate[j]) -
            #                    np.count_nonzero(inputData.result.arrays[i].array_validate[j])) / (
            #                       len(inputData.result.arrays[i].array_validate[j]))

            Features_Array = []
            Features_Array.append(Tespar_features.tolist())
            Features_Array.append(quality_feature)

            Features_List = list(flatten(Features_Array))

            X.append(np.asarray(Features_List).ravel())
            Y.append(inputData.result.arrays[i].name)

    return pd.DataFrame(X), Y


def obtain_S_TESPAR_features(inputData, encoding):
    X = []
    Y = []

    for i in range(len(inputData.result.arrays)):
        for j in range(len(inputData.result.arrays[i].array_data)):
            X.append(np.asarray(
                encoding.get_s(inputData.result.arrays[i].array_data[j],
                               inputData.result.arrays[i].array_validate[j])))
            Y.append(inputData.result.arrays[i].name)

    return pd.DataFrame(X), Y


def obtain_features_labels_from_doa(doas, channel_number, segment, encoding, selected_symbols=32):
    X = []
    Y = []

    for doa in doas:
        channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
        for trial in channel.trials:
            seg = getattr(trial, segment)
            X.append(
                np.asarray(encoding.get_a(seg.values, seg.values_outsiders, selected_symbols=selected_symbols)).ravel())
            Y.append(doa.level)

    return pd.DataFrame(X), pd.DataFrame(Y)
    # return pd.DataFrame(X), Y


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


def split_train_test_balance(doas, percent, balance_test=True):
    doas_train = []
    doas_test = []

    min_nr_of_trials = MAX_NR_OF_TRIALS
    for doa in doas:
        for channel in doa.channels:
            if min_nr_of_trials > len(channel.trials):
                min_nr_of_trials = len(channel.trials)
    print(min_nr_of_trials)
    needed_train_samples = int((1 - percent) * min_nr_of_trials)
    print("train samples needed:" + str(needed_train_samples))
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
    print("common to all trisal we have:" + str(len_trials_common_to_all))

    if needed_train_samples > len_trials_common_to_all:
        ind_train = trials_common_to_all
    else:
        random.shuffle(trials_common_to_all)
        ind_train = trials_common_to_all[-needed_train_samples:]
    print("in final raman pentru train:" + str(len(ind_train)))

    min_nr_of_trials_test = min_nr_of_trials - needed_train_samples

    for doa in doas:
        doa_train = DOA(doa.level)
        doa_test = DOA(doa.level)
        for channel in doa.channels:
            count = 0
            ch_train = Channel(channel.number)
            ch_test = Channel(channel.number)
            for trial in channel.trials:
                if trial.trial_number in ind_train:
                    # put trials in doa_test
                    ch_train.trials.append(trial)
                else:
                    # if count < min_nr_of_trials_test:
                    # put trials in doa_train
                    ch_test.trials.append(trial)
                    # count = count + 1
            doa_train.channels.append(ch_train)
            doa_test.channels.append(ch_test)
        doas_train.append(doa_train)
        doas_test.append(doa_test)

    # if balance_test:
    #     min_nr_of_trials_test = min_nr_of_trials - needed_train_samples
    #     print("cate vor fi la test:" + str(min_nr_of_trials_test))
    #     for doa in doas_test:
    #         for channel in doa.channels:
    #             if min_nr_of_trials_test > len(channel.trials):
    #                 min_nr_of_trials_test = len(channel.trials)

    return doas_train, doas_test, ind_train


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


def train_test_doa_check_trials_balanced(doas, percent):
    doas_train = []
    doas_test = []

    min_nr_of_trials = MAX_NR_OF_TRIALS
    for doa in doas:
        for channel in doa.channels:
            if min_nr_of_trials > len(channel.trials):
                min_nr_of_trials = len(channel.trials)

    needed_train_samples = int((1 - percent) * min_nr_of_trials)

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
    if needed_train_samples > len_trials_common_to_all:
        ind_train = trials_common_to_all
    else:
        random.shuffle(trials_common_to_all)
        ind_train = trials_common_to_all[-needed_train_samples:]

    for doa in doas:
        doa_train = DOA(doa.level)
        doa_test = DOA(doa.level)
        for channel in doa.channels:
            ch_train = Channel(channel.number)
            ch_test = Channel(channel.number)
            for trial in channel.trials:
                if trial.trial_number in ind_train:
                    # put trials in doa_train
                    ch_train.trials.append(trial)
                else:
                    # put trials in doa_test
                    ch_test.trials.append(trial)
            doa_train.channels.append(ch_train)
            doa_test.channels.append(ch_test)
        doas_train.append(doa_train)
        doas_test.append(doa_test)

    return doas_train, doas_test, ind_train


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
