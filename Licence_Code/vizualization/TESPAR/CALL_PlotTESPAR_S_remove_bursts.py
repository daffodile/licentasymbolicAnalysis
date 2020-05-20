import os

from feature_extraction.TESPAR.EncodingCheckBursts import EncodingCheckBursts
from input_reader.InitDataSetWithBurstsFlags import InitDataSetWithBurstsFlags
from utils.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions
from utils.MarkOutsidersWithBurstsFlags import remove_bursted_trials_when_segment
from vizualization.TESPAR.PlotTESPARMatrices import get_matrices_S_more_doas_remove_bursts, \
    get_s_matrices_full_doa_remove_burst, plot_average_sum_S_matrix_doa, \
    plot_average_sum_S_matrix_doa_per_trial

encoding = EncodingCheckBursts('./../../data_to_be_saved/alphabet_3.txt')
current_dir = os.path.join('..', '..')

# levels = ['light1']
levels = ['light1', 'deep2', 'medium3', 'light4', 'medium5']
initialization = InitDataSetWithBurstsFlags(current_directory=current_dir, subject_directory="m014",
                                            filtering_directory="classic",
                                            levels=levels)
doas = initialization.get_dataset_as_doas()
print('doas is initialized')
mark_bursts_regions(doas)
remove_bursted_trials_when_segment(doas)
print('done removed bursts')

#  5 levels * 3 plots  = 15
# for level in levels:
# #     all_histograms_doa = get_s_matrices_full_doa_remove_burst(encoding=encoding, doas=doas, doa_level=level,
# #                                                               segments=['spontaneous', 'stimulus'])
# #     # print(f'for  {level} the are {len(all_histograms_doa)} trials')
# #     # plot_average_sum_S_matrix_doa(all_histograms_doa=all_histograms_doa, doa_level=level,
# #     #                               title=f'Average S matrix of {level}',
# #     #                               plot_name=f'scaled_average_s_matrix_full_{level}', nr_channels=len(doas[0].channels))
# #
# #     plot_average_sum_S_matrix_doa_per_trial(all_histograms_doa=all_histograms_doa, doa_level=level,
# #                                             title=f'Average S matrix of {level} per trial',
# #                                             plot_name=f'scaled_average_s_matrix_full_{level}_per_trial', log=True)
# #
# #     plot_average_sum_S_matrix_doa_per_trial(all_histograms_doa=all_histograms_doa, doa_level=level,
# #                                             title=f'Average S matrix of {level} per trial',
# #                                             plot_name=f'scaled_average_s_matrix_full_{level}_per_trial', log=False)
# #     print(f'done for {level}')


# # 4 plots * 6 = 24
get_matrices_S_more_doas_remove_bursts(encoding, doas, ['light1', 'light4'], segments=['spontaneous', 'stimulus'],
                                       string_about_channels="all 30 channels")
print('done for L1 L4')
get_matrices_S_more_doas_remove_bursts(encoding, doas, ['light1', 'deep2'], segments=['spontaneous', 'stimulus'],
                                       string_about_channels="all 30 channels")
print('done for L1 D2')

get_matrices_S_more_doas_remove_bursts(encoding, doas, ['light4', 'deep2'], segments=['spontaneous', 'stimulus'],
                                       string_about_channels="all 30 channels")
print('done for L4 D2')

get_matrices_S_more_doas_remove_bursts(encoding, doas, ['medium3', 'medium5'], segments=['spontaneous', 'stimulus'],
                                       string_about_channels="all 30 channels")
print('done for M3 M5')

get_matrices_S_more_doas_remove_bursts(encoding, doas, ['deep2', 'medium3'], segments=['spontaneous', 'stimulus'],
                                       string_about_channels="all 30 channels")
print('done for D2 M3')

get_matrices_S_more_doas_remove_bursts(encoding, doas, ['light1', 'medium5'], segments=['spontaneous', 'stimulus'],
                                       string_about_channels="all 30 channels")
print('done for L1 M5')
