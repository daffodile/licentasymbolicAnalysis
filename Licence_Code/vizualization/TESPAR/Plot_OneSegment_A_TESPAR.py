import os
import numpy as np
from feature_extraction.TESPAR.EncodingCheckBursts import EncodingCheckBursts
from input_reader.InitDataSetWithBurstsFlags import InitDataSetWithBurstsFlags
from utils.Utils import get_all_trials_values_from_doa_by_segment_with_bursts_flags
from vizualization.TESPAR.PlotTESPARMatrices import plot_matrix_A, get_channel_matrix_A

encoding = EncodingCheckBursts('./../../data_to_be_saved/alphabet_3.txt')
current_dir = os.path.join('..', '..')

channel = 7
# levels = ['deep2']
levels = ['light1', 'deep2', 'medium3', 'light4', 'medium5']
initialization = InitDataSetWithBurstsFlags(current_directory=current_dir, subject_directory="m014",
                                            filtering_directory="classic",
                                            levels=levels)
doas = initialization.get_dataset_as_doas()

# for level in levels:
#     spontaneous_values, spontaneous_outliers = get_all_trials_values_from_doa_by_segment_with_bursts_flags(doas, level,
#                                                                                                            'spontaneous',
#                                                                                                            channel)
#     stimulus_values, stimulus_outliers = get_all_trials_values_from_doa_by_segment_with_bursts_flags(doas, level,
#                                                                                                      'stimulus',
#                                                                                                      channel)
#     emphasize_stim_respunse_matrices = []
#     for i in range(len(spontaneous_values)):
#         a_sponaneous = encoding.get_a(spontaneous_values[i], spontaneous_outliers[i])
#         a_stimulus = encoding.get_a(stimulus_values[i], stimulus_outliers[i])
#         a_sponaneous = a_sponaneous * len(stimulus_values) / len(spontaneous_values)  # normalizare la lungime
#         a_stim_resp = a_stimulus - a_sponaneous
#         print(a_stim_resp)
#         emphasize_stim_respunse_matrices.append(a_stim_resp)
#
#     x = np.sum(emphasize_stim_respunse_matrices, axis=0)
#     t = np.sign(x) * np.log10(abs(x) + 1)
#     plot_matrix_A(values=t, title=f"Stimulus reps {level}",
#                   plot_name=f'stim_response_{level}_ch{channel}.png')
#
#     x_trial = x / 240
#     t_trial = np.sign(x_trial) * np.log10(abs(x_trial) + 1)
#
#     plot_matrix_A(values=t_trial, title=f"Stimulus reps {level}",
#                   plot_name=f'stim_response_{level}_ch{channel}_per_trial.png')


for level in levels:
    # get_channel_matrix_A(encoding, doas, doa_level, segment, channel_number, log)
    get_channel_matrix_A(encoding=encoding, doas=doas, doa_level=level, segment='spontaneous', channel_number=channel,
                         log=True)
    get_channel_matrix_A(encoding=encoding, doas=doas, doa_level=level, segment='stimulus', channel_number=channel,
                         log=True)
