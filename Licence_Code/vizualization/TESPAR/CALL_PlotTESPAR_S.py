import os

from feature_extraction.TESPAR.Encoding import Encoding
from feature_extraction.TESPAR.EncodingCheckBursts import EncodingCheckBursts
from input_reader.InitDataSet import InitDataSet
from input_reader.InitDataSetWithBurstsFlags import InitDataSetWithBurstsFlags
from utils.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions
from utils.MarkOutsidersWithBurstsFlags import remove_bursted_trials_when_segment
from vizualization.TESPAR.PlotTESPARMatrices import get_channel_matrix_S, get_matrices_S_more_doas, \
    get_symbols_full_doa, plot_average_matrix_S, plot_average_matrix_S_per_trial

# levels = ['deep2', 'medium3', 'light4']
# levels = ['deep1', 'medium3', 'medium5']
# levels = ['deep1']

# # def __init__(self, current_directory, subject_directory, filtering_directory, levels=['deep', 'medium', 'light'], trials_to_skip=None):
# initialization = InitDataSetWithBurstsFlags(current_directory=current_dir, subject_directory="m014", filtering_directory="highpass10",
#                              levels=levels)
#
# doas = initialization.get_dataset_as_doas()

# current_dir = os.path.join('..', '..')
#
# levels = ['deep1', 'deep2', 'medium3', 'light4', 'medium5']
#

# # M016
# levels = ['light7', 'medium8', 'medium10', 'light11']
# # levels = ['deep6', 'deep9']
#
# initialization = InitDataSetWithBurstsFlags(current_directory=current_dir, subject_directory="m016",
#                                             filtering_directory="classic",
#                                             levels=levels)
# doas = initialization.get_dataset_as_doas()
# print('doas is initialized')
#
# # mark_bursts_regions(doas)
# # remove_bursted_trials_when_segment(doas)
#
# encoding = EncodingCheckBursts('./../../data_to_be_saved/32alphabet5_m016.txt')
#
# channels = [1, 6, 7, 11, 17, 24, 28]
#
# for level in levels:
#     for channel in channels:
#         get_channel_matrix_S(encoding, doas, level, 'stimulus', channel, log=True)


# levels = ['deep1', 'medium5']
#
# levels = ['deep2', 'medium3', 'light4', 'deep1', 'medium5']
#
# initialization = InitDataSetWithBurstsFlags(current_directory=current_dir, subject_directory="m014",
#                                             filtering_directory="classic",
#                                             levels=levels)
# doas = initialization.get_dataset_as_doas()
# print('doas is initialized')
#
# # mark_bursts_regions(doas)
# # remove_bursted_trials_when_segment(doas)
#
# encoding = EncodingCheckBursts('./../../data_to_be_saved/alphabet_3.txt')
#
# channels = [2, 6, 7, 19, 20, 24, 29]
#
# for level in levels:
#     for channel in channels:
#         get_channel_matrix_S(encoding, doas, level, 'stimulus', channel, log=True)

##################################################################################
#  plot S matrix the average on 15 channels on a hist, comparing 2 conditions
# encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')
# current_dir = os.path.join('..', '..')
# channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
#
# levels = ['light1', 'light4']
# initialization = InitDataSet(current_directory=current_dir, subject_directory="m014", filtering_directory="classic",
#                              levels=levels)
# doas = initialization.get_dataset_as_doas()
# print('doas is initialized')
# get_matrices_S_more_doas(encoding, doas, levels, segments=['spontaneous', 'stimulus'], channels=channels,
#                          string_about_channels="first 15 channels")
#
# channels = [17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
#
# get_matrices_S_more_doas(encoding, doas, levels, segments=['spontaneous', 'stimulus'], channels=channels,
#                          string_about_channels="last 15 channels")
#
# levels = ['medium3', 'medium5']
# initialization = InitDataSet(current_directory=current_dir, subject_directory="m014", filtering_directory="classic",
#                              levels=levels)
# doas = initialization.get_dataset_as_doas()
# print('doas is initialized')
# channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
#
# get_matrices_S_more_doas(encoding, doas, levels, segments=['spontaneous', 'stimulus'], channels=channels,
#                          string_about_channels="first 15 channels")
#
# channels = [17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32]
# get_matrices_S_more_doas(encoding, doas, levels, segments=['spontaneous', 'stimulus'], channels=channels,
#                          string_about_channels="last 15 channels")

