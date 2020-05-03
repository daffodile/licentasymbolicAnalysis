import os

from feature_extraction.TESPAR.Encoding import Encoding
from feature_extraction.TESPAR.EncodingCheckBursts import EncodingCheckBursts
from input_reader.InitDataSet import InitDataSet
from input_reader.InitDataSetWithBurstsFlags import InitDataSetWithBurstsFlags
from utils.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions
from utils.MarkOutsidersWithBurstsFlags import remove_bursted_trials_when_segment
from vizualization.TESPAR.PlotTESPARMatrices import get_channel_matrix_A, get_channels_difference_matrix_A

current_dir = os.path.join('..', '..')

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

levels = ['deep2', 'light4']

initialization = InitDataSetWithBurstsFlags(current_directory=current_dir, subject_directory="m014", filtering_directory="highpass10",
                             levels=levels)
doas = initialization.get_dataset_as_doas()
print('doas is initialized')

# mark_bursts_regions(doas)
#
# remove_bursted_trials_when_segment(doas)

encoding = EncodingCheckBursts('./../../data_to_be_saved/alphabet_3.txt')

channels = [2, 6, 20, 29]

# for level in levels:
#     for channel in channels:
#         # get_channel_matrix_A(encoding, doas, level, 'stimulus', channel, log=False)
#         # get_channel_matrix_A(encoding, doas, level, 'stimulus', channel, log=True)


for channel in channels:
    # def get_channels_difference_matrix_A(encoding, doas, doa_levels, segment, channels, log):
    get_channels_difference_matrix_A(encoding, doas, levels, 'stimulus', [channel, channel], log=False)
