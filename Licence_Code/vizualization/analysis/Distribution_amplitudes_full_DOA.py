import os

import numpy as np

from input_reader.InitDataSet import InitDataSet
from utils.Utils import get_doa_of_level
from utils.Utils_master import get_channel_trials_values_more_seg
from vizualization.analysis.ploting_functions import plot_hist


def get_channel_from_doa(doas, level, ch_number):
    doa = get_doa_of_level(doas, level)
    channel = list(filter(lambda ch: (ch.number == ch_number), doa.channels))[0]
    return channel


all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
                31, 32]

data_dir = os.path.join('..', '..')

levels = ['deep2', 'medium3', 'light4']

# def __init__(self, current_directory, subject_directory, filtering_directory, levels=['deep', 'medium', 'light'], trials_to_skip=None):
initialization = InitDataSet(current_directory=data_dir, subject_directory="m014", filtering_directory="classic",
                             levels=levels)
doas = initialization.get_dataset_as_doas()

print('doas is initialized')

# distribution of amplitudes for channel 20 DEEP

for level in levels:

    current_level_amplitudes = []

    for channel in all_channels:
        channel_trials_values = get_channel_trials_values_more_seg(doas, level, channel,
                                                                   segments=['spontaneous', 'stimulus', 'poststimulus'])
        for trial_values in channel_trials_values:
            current_level_amplitudes.extend(trial_values)

    # def plot_hist(values, bins=None, log=False, to_save=False, file_name="hist", title=None, x_label=None, y_label=None):
    #     n, bins, patches = plt.hist(values, bins=bins, log=log)
    plot_hist(values=current_level_amplitudes, bins=200, log=False, to_save=True, file_name=f'{level}_ampl_distr.png',
              title=f'Distribution of the amplitudes {level} log10(#)', x_label='Amplitudes space', y_label='Frequency of amplitudes')

    plot_hist(values=current_level_amplitudes, bins=200, log=True, to_save=True, file_name=f'{level}_ampl_distr.png',
              title=f'Distribution of the amplitudes {level}', x_label='Amplitudes space',
              y_label='Frequency of amplitudes')
