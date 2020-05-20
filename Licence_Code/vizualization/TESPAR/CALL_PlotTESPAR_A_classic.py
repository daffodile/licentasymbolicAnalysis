import os

from feature_extraction.TESPAR.Encoding import Encoding
from feature_extraction.TESPAR.EncodingCheckBursts import EncodingCheckBursts
from input_reader.InitDataSet import InitDataSet
from input_reader.InitDataSetWithBurstsFlags import InitDataSetWithBurstsFlags
from utils.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions
from utils.MarkOutsidersWithBurstsFlags import remove_bursted_trials_when_segment
from vizualization.TESPAR.PlotTESPARMatrices import get_channel_matrix_A, get_channels_difference_matrix_A, \
    get_average_matrix_A_doa, get_average_matrix_A_doa_per_trial, get_channel_trial_matrix_A

current_dir = os.path.join('..', '..')

# levels = ['deep6', 'light7', 'medium8', 'deep9', 'medium10', 'light11']
# levels = ['deep6', 'light7', 'medium8']
# levels = ['deep9', 'medium10', 'light11']

# initialization = InitDataSetWithBurstsFlags(current_directory=current_dir, subject_directory="m016",
#                                             filtering_directory="highpass10", levels=levels)
# doas = initialization.get_dataset_as_doas()
# print('doas is initialized')

# mark_bursts_regions(doas)
#
# remove_bursted_trials_when_segment(doas)
#
levels = ['light1', 'deep2', 'medium3', 'light4', 'medium5']
# # levels = ['light1', 'deep2']
#
# # # def __init__(self, current_directory, subject_directory, filtering_directory, levels=['deep', 'medium', 'light'], trials_to_skip=None):
initialization = InitDataSet(current_directory=current_dir, subject_directory="m014",
                             filtering_directory="classic",
                             levels=levels)

doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')

# for level in levels:
#     for channel in channels:
#         get_channel_matrix_A(encoding, doas, level, 'stimulus', channel, log=True)
#
# for channel in channels:
#     # def get_channels_difference_matrix_A(encoding, doas, doa_levels, segment, channels, log):
#     get_channels_difference_matrix_A(encoding, doas, levels, 'stimulus', [channel, channel], log=False)
for level in levels:
    get_average_matrix_A_doa_per_trial(encoding, doas, level, log=False)
    get_average_matrix_A_doa_per_trial(encoding, doas, level, log=True)
    # get_average_matrix_A_doa(encoding, doas, level, log=True)
