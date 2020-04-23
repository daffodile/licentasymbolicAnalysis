import os

import numpy as np
import pandas as pd

# to be tested in debug
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.svm import SVC

from input_reader.InitDataSet import InitDataSet


def get_A_multiple_channels(doas, encoding, channels=[], segments=['spontaneous'], average=False, all_channels=True):
    '''
    methods assumes all channels have the same number of trials

    :param doas: dataset as DOAs, same amount of trials in each channel
    :param encoding: Encoding for getting TESPAR A matrices
    :param channels: selected channels if only some are targeted
    :param segments: targeted segments to concatenate
    :param all_channels: bool if to use all existing channels
    :return: X, Y features prepared for training
    '''
    X = []
    Y = []

    if all_channels:
        for doa in doas:
            if average:
                channels_number = len(channels)
            else:
                channels_number = len(doa.channels)

            # same number of trials is needed
            a_matrices = [
                np.zeros((encoding.no_symbols, encoding.no_symbols)) for i in range(len(doa.channels[0].trials))]

            for channel in doa.channels:
                for ind_trial, trial in enumerate(channel.trials):
                    trial_values = []
                    for segment in segments:
                        trial_values.extend(getattr(trial, segment).values)

                    a_matrices[ind_trial] = np.add(a_matrices[ind_trial], encoding.get_a(trial_values))

            for matrix in a_matrices:
                if average:
                    matrix = matrix / channels_number
                X.append(np.asarray(matrix).ravel())
                Y.append(doa.level)
    else:
        for doa in doas:
            if average:
                channels_number = len(channels)
            else:
                channels_number = len(doa.channels)

            a_matrices = [
                np.zeros((encoding.no_symbols, encoding.no_symbols)) for i in range(len(doa.channels[0].trials))]

            for channel in doa.channels:
                if channel.number in channels:
                    for ind_trial, trial in enumerate(channel.trials):
                        trial_values = []
                        for segment in segments:
                            trial_values.extend(getattr(trial, segment).values)

                        a_matrices[ind_trial] = np.add(a_matrices[ind_trial], encoding.get_a(trial_values))

            for matrix in a_matrices:
                if average:
                    matrix = matrix / channels_number
                X.append(np.asarray(matrix).ravel())
                Y.append(doa.level)

    return pd.DataFrame(X), np.array(Y)


def get_A_multiple_channels_bursts(doas, encoding, channels=[], segments=['spontaneous'], average=False,
                                   all_channels=True):
    '''
    methods assumes all channels have the same number of trials

    :param doas: dataset as DOAs, same amount of trials in each channel
    :param encoding: Encoding for getting TESPAR A matrices
    :param channels: selected channels if only some are targeted
    :param segments: targeted segments to concatenate
    :param all_channels: bool if to use all existing channels
    :return: X, Y features prepared for training
    '''
    X = []
    Y = []

    if all_channels:
        for doa in doas:
            if average:
                channels_number = len(channels)
            else:
                channels_number = len(doa.channels)

            # same number of trials is needed
            a_matrices = [
                np.zeros((encoding.no_symbols, encoding.no_symbols)) for i in range(len(doa.channels[0].trials))]

            for channel in doa.channels:
                for ind_trial, trial in enumerate(channel.trials):
                    trial_values = []
                    trial_outliers = []
                    for segment in segments:
                        trial_values.extend(getattr(trial, segment).values)
                        trial_outliers.extend(getattr(trial, segment).values_outsiders)

                    a_matrices[ind_trial] = np.add(a_matrices[ind_trial], encoding.get_a(trial_values, trial_outliers))

            for matrix in a_matrices:
                if average:
                    matrix = matrix / channels_number
                X.append(np.asarray(matrix).ravel())
                Y.append(doa.level)
    else:
        for doa in doas:
            if average:
                channels_number = len(channels)
            else:
                channels_number = len(doa.channels)

            a_matrices = [
                np.zeros((encoding.no_symbols, encoding.no_symbols)) for i in range(len(doa.channels[0].trials))]

            for channel in doa.channels:
                if channel.number in channels:
                    for ind_trial, trial in enumerate(channel.trials):
                        trial_values = []
                        trial_outliers = []
                        for segment in segments:
                            trial_values.extend(getattr(trial, segment).values)
                            trial_outliers.extend(getattr(trial, segment).values_outsiders)

                        a_matrices[ind_trial] = np.add(a_matrices[ind_trial],
                                                       encoding.get_a(trial_values, trial_outliers))

            for matrix in a_matrices:
                if average:
                    matrix = matrix / channels_number
                X.append(np.asarray(matrix).ravel())
                Y.append(doa.level)

    return pd.DataFrame(X), np.array(Y)


def get_S_multiple_channels(doas, encoding, channels=[], segments=['spontaneous'], average=False, all_channels=True):
    '''
    methods assumes all channels have the same number of trials

    :param doas: dataset as DOAs, same ampunt of trials in each channel
    :param encoding: Encoding for getting TESPAR A matrices
    :param channels: selected channels if only some are targeted
    :param segments: targeted segments to concatenate
    :param all_channels: bool if to use all existing channels
    :return: X, Y features prepared for training
    '''
    X = []
    Y = []

    if all_channels:
        for doa in doas:
            if average:
                channels_number = len(channels)
            else:
                channels_number = len(doa.channels)

            # same number of trials is needed
            s_matrices = [
                np.zeros(encoding.no_symbols) for i in range(len(doa.channels[0].trials))]

            for channel in doa.channels:
                for ind_trial, trial in enumerate(channel.trials):
                    trial_values = []
                    for segment in segments:
                        trial_values.extend(getattr(trial, segment).values)

                    s_matrices[ind_trial] = np.add(s_matrices[ind_trial], encoding.get_s(trial_values))

            for matrix in s_matrices:
                if average:
                    matrix = matrix / channels_number
                X.append(np.asarray(matrix).ravel())
                Y.append(doa.level)
    else:
        for doa in doas:
            if average:
                channels_number = len(channels)
            else:
                channels_number = len(doa.channels)

            s_matrices = [
                np.zeros(encoding.no_symbols) for i in range(len(doa.channels[0].trials))]

            for channel in doa.channels:
                if channel.number in channels:
                    for ind_trial, trial in enumerate(channel.trials):
                        trial_values = []
                        for segment in segments:
                            trial_values.extend(getattr(trial, segment).values)

                        s_matrices[ind_trial] = np.add(s_matrices[ind_trial], encoding.get_s(trial_values))

            for matrix in s_matrices:
                if average:
                    matrix = matrix / channels_number
                X.append(np.asarray(matrix).ravel())
                Y.append(doa.level)

    return pd.DataFrame(X), np.array(Y)

# encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')
#
# data_dir = os.path.join('..', '..')
#
# initialization = InitDataSet(data_dir=data_dir, levels=['deep', 'light'])
# doas = initialization.get_dataset_as_doas()
#
# # X, y = obtain_features_labels_from_doa(doas, 20, 'spontaneous', encoding)
#
# # X, y = get_A_multiple_channels(doas, encoding, channels=[2, 5, 6, 7, 13, 15], average=True, all_channels=False)
# X, y = get_A_multiple_channels(doas, encoding, segments=['stimulus'])
#
# # X, y = get_S_multiple_channels(doas, encoding, average=True)
#
# model = SVC(gamma="auto")
#
# skf = StratifiedKFold(n_splits=10)
#
# skf.get_n_splits(X, y)
#
# results = cross_validate(model, X, y, scoring=['accuracy', 'f1_weighted'], cv=skf)
#
# accuracy = results['test_accuracy']
# f1score = results['test_f1_weighted']
#
# print(accuracy)
# print("Accuracy of Model with Cross Validation is:", accuracy.mean() * 100)
# print(f1score)
#
# print("f1 score of Model with Cross Validation is:", f1score.mean() * 100)
