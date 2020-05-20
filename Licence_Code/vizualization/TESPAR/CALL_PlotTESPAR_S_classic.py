import os

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from vizualization.TESPAR.PlotTESPARMatrices import get_symbols_full_doa, plot_average_matrix_S_per_trial, \
    get_matrices_S_more_doas

encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')
current_dir = os.path.join('..', '..')

# levels = ['light1', 'medium5']
levels = ['light1', 'deep2', 'medium3', 'light4', 'medium5']
initialization = InitDataSet(current_directory=current_dir, subject_directory="m014", filtering_directory="classic",
                             levels=levels)
doas = initialization.get_dataset_as_doas()
print('doas is initialized')

for level in levels:
    all_symbols = get_symbols_full_doa(encoding, doas, level)
    plot_average_matrix_S_per_trial(all_symbols, level, f'Average S matrix of {level} per trial',
                                    f'average_s_matrix_full_{level}', len(doas[0].channels),
                                    len(doas[0].channels[0].trials), log=True)

    plot_average_matrix_S_per_trial(all_symbols, level, f'Average S matrix of {level} per trial',
                                    f'average_s_matrix_full_{level}', len(doas[0].channels),
                                    len(doas[0].channels[0].trials), log=False)

channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31,
            32]

get_matrices_S_more_doas(encoding, doas, ['light1', 'medium5'], segments=['spontaneous', 'stimulus'],
                         channels=channels, string_about_channels="all 30 channels")
print('done for L1 M5')


# get_matrices_S_more_doas(encoding, doas, ['light1', 'light4'], segments=['spontaneous', 'stimulus'], channels=channels,
#                          string_about_channels="all 30 channels")
# print('done for L1 L4')
# get_matrices_S_more_doas(encoding, doas, ['light1', 'deep2'], segments=['spontaneous', 'stimulus'],
#                          channels=channels, string_about_channels="all 30 channels")
# print('done for L1 D2')
#
# get_matrices_S_more_doas(encoding, doas, ['light4', 'deep2'], segments=['spontaneous', 'stimulus'],
#                          channels=channels, string_about_channels="all 30 channels")
# print('done for L4 D2')
#
# get_matrices_S_more_doas(encoding, doas, ['medium3', 'medium5'], segments=['spontaneous', 'stimulus'],
#                          channels=channels, string_about_channels="all 30 channels")
# print('done for M3 M5')
#
# get_matrices_S_more_doas(encoding, doas, ['deep2', 'medium3'], segments=['spontaneous', 'stimulus'],
#                          channels=channels, string_about_channels="all 30 channels")
# print('done for D2 M3')



#################################################################################################
# # plot average S over a DOA
# encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')
# current_dir = os.path.join('..', '..')
#
# # channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30, 31,
# #             32]
#
# # level = 'light4'
# levels = ['light1', 'deep2', 'medium3', 'medium5']
# initialization = InitDataSet(current_directory=current_dir, subject_directory="m014", filtering_directory="classic",
#                              levels=levels)
# doas = initialization.get_dataset_as_doas()
# print('doas is initialized')
#
# for level in levels:
#     all_symbols = get_symbols_full_doa(encoding, doas, level)
#     plot_average_matrix_S(all_symbols, level, f'Average S matrix of {level}', f'average_s_matrix_full_{level}',
#                           len(doas[0].channels))

