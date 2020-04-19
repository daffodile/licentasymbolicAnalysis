import numpy as np
import pandas as pd


# to be tested in debug
# def get_A_multimple_channels(doas, encoding, channels=[], segments=['spontaneous'], all_channels=False):
#     '''
#
#     :param doas: dataset as DOAs, same ampunt of trials in each channel
#     :param encoding: Encoding for getting TESPAR A matrices
#     :param channels: selected channels if only some are targeted
#     :param segments: targeted segments to concatenate
#     :param all_channels: bool if to use all existing channels
#     :return: X, Y features prepared for training
#     '''
#     X = []
#     Y = []
#
#     if all_channels:
#         for doa in doas:
#             a_matrices = [
#                 np.zeros((encoding.no_symbols, encoding.no_symbols)) in range(len(doas[0].channels[0].trials))]
#
#             for channel in doa.channels:
#                 for ind_trial, trial in enumerate(channel.trials):
#                     trial_values = []
#                     for segment in segments:
#                         trial_values.extend(getattr(trial, segment).values)
#
#                     a_matrices[ind_trial] = np.add(a_matrices[ind_trial], encoding.get_a(trial_values))
#
#             for matrix in a_matrices:
#                 X.append(np.asarray(matrix).ravel())
#                 Y.append(doa.level)
#     else:
#         for doa in doas:
#             a_matrices = [
#                 np.zeros((encoding.no_symbols, encoding.no_symbols)) in range(len(doas[0].channels[0].trials))]
#
#             for channel in doa.channels:
#                 if channel.number in channels:
#                     for ind_trial, trial in enumerate(channel.trials):
#                         trial_values = []
#                         for segment in segments:
#                             trial_values.extend(getattr(trial, segment).values)
#
#                         a_matrices[ind_trial] = np.add(a_matrices[ind_trial], encoding.get_a(trial_values))
#
#             for matrix in a_matrices:
#                 X.append(np.asarray(matrix).ravel())
#                 Y.append(doa.level)
#
#     return pd.DataFrame(X), Y
