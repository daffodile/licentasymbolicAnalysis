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

# levels = ['light1', 'deep2', 'medium3', 'light4', 'medium5']
levels = ['medium3', 'medium5']
#
# # # def __init__(self, current_directory, subject_directory, filtering_directory, levels=['deep', 'medium', 'light'], trials_to_skip=None):
initialization = InitDataSet(current_directory=current_dir, subject_directory="m014",
                             filtering_directory="highpass10",
                             levels=levels)

doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../../data_to_be_saved/32alphabet5_hp10_m014.txt')
for level in levels:
    # get_average_matrix_A_doa_per_trial(encoding, doas, level, log=False)
    # get_average_matrix_A_doa_per_trial(encoding, doas, level, log=True)
    get_average_matrix_A_doa(encoding, doas, level, log=True)

# channels = [2, 6, 19, 20, 21, 23]
# trials = [5, 6, 11, 14]
#
# for doa_level in levels:
#     for channel in channels:
#         for trial_no in trials:
#             get_channel_trial_matrix_A(encoding, doas, doa_level, channel_number=channel, trial_number=trial_no, log=False)
