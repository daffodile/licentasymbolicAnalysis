import os

from feature_extraction.TESPAR.Encoding import Encoding
from feature_extraction.TESPAR.EncodingCheckBursts import EncodingCheckBursts
from input_reader.InitDataSet import InitDataSet
from input_reader.InitDataSetWithBurstsFlags import InitDataSetWithBurstsFlags
from utils.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions
from utils.MarkOutsidersWithBurstsFlags import remove_bursted_trials_when_segment
from vizualization.TESPAR.PlotTESPARMatrices import get_channel_matrix_A, get_channels_difference_matrix_A, \
    get_average_matrix_A_doa, get_average_matrix_A_doa_per_trial, get_channel_trial_matrix_A, \
    get_average_matrix_A_doa_per_trial_remove_bursts, get_average_matrix_A_doa_remove_bursts, get_difference_matrix_A

current_dir = os.path.join('..', '..')

encoding = EncodingCheckBursts('./../../data_to_be_saved/alphabet_3.txt')
#
# levels = ['light1']
# channels = [7]
# trials = [5]

levels = ['light1', 'deep2', 'medium3', 'light4', 'medium5']
channels = [2, 6, 19, 20, 21, 23]
trials = [2,5, 6, 11, 14]

initialization = InitDataSetWithBurstsFlags(current_directory=current_dir, subject_directory="m014",
                                            filtering_directory="classic",
                                            levels=levels)
doas = initialization.get_dataset_as_doas()
print('doas is initialized')
# mark_bursts_regions(doas)
# remove_bursted_trials_when_segment(doas)
# print('done removed bursts')


for level in levels:
    for channel in channels:
        get_channel_matrix_A(encoding, doas, level, 'spontaneous', channel, log=True)
        get_channel_matrix_A(encoding, doas, level, 'stimulus', channel, log=True)


for level in levels:
    get_average_matrix_A_doa_per_trial_remove_bursts(encoding, doas, level, log=False)
    get_average_matrix_A_doa_per_trial_remove_bursts(encoding, doas, level, log=True)
    get_average_matrix_A_doa_remove_bursts(encoding, doas, level, log=True)

get_difference_matrix_A(encoding=encoding, doas=doas, doa_levels=['light1', 'light4'],
                        segments=['stimulus', 'spontaneous'], log=False)
print('done for L1 L4')

get_difference_matrix_A(encoding=encoding, doas=doas, doa_levels=['light1', 'deep2'],
                        segments=['stimulus', 'spontaneous'], log=False)
print('done for L1 D2')
get_difference_matrix_A(encoding=encoding, doas=doas, doa_levels=['light4', 'deep2'],
                        segments=['stimulus', 'spontaneous'], log=False)
print('done for L4 D2')


get_difference_matrix_A(encoding=encoding, doas=doas, doa_levels=['light1', 'medium5'],
                        segments=['stimulus', 'spontaneous'], log=False)
print('done for L1 M5')

get_difference_matrix_A(encoding=encoding, doas=doas, doa_levels=['medium3', 'medium5'],
                        segments=['stimulus', 'spontaneous'], log=False)
print('done for M3 M5')

get_difference_matrix_A(encoding=encoding, doas=doas, doa_levels=['deep2', 'medium3'],
                        segments=['stimulus', 'spontaneous'], log=False)
print('done for D2 M3')
