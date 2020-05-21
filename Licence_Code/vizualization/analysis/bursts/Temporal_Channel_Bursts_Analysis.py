import os

import numpy as np
import matplotlib.pyplot as plt

from input_reader.InitDataSet import InitDataSet
from utils.Utils import get_doa_of_level, get_trial_values_and_outsiders, get_channel_index
from utils.mark_bursts.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions
from utils.mark_bursts.MarkOutsidersWithBurstsFlags import remove_bursted_trials_when_segment


def get_channel_stats(doas, doa_level, channel_number):
    doa = get_doa_of_level(doas, doa_level)

    for trial_index in range(240):

        trial_values, trial_values_outsiders = get_trial_values_and_outsiders(doa,
                                                                              channel_number,
                                                                              trial_index + 1)

        trial_bursts_amplitudes = []
        for i in range(len(trial_values_outsiders)):
            if (trial_values_outsiders[i] == 1):
                trial_bursts_amplitudes.append(trial_values[i])
        trial_avg_bursts_amplitudes = np.mean(trial_bursts_amplitudes)

        trial_bursts_percentage = (len(trial_bursts_amplitudes) * 100) / (len(trial_values))

        trial_max_burst_amplitude = 0
        if (len(trial_bursts_amplitudes) != 0):
            trial_max_burst_amplitude = max(trial_bursts_amplitudes)

        outsider_points = []
        if (trial_values_outsiders[0] == 1):
            outsider_points.append((0, trial_values[0]))
        for i in range(len(trial_values_outsiders) - 1):
            if (trial_values_outsiders[i] == 0 and trial_values_outsiders[i + 1] == 1):
                outsider_points.append((i + 1, trial_values[i + 1]))
            if (trial_values_outsiders[i] == 1 and trial_values_outsiders[i + 1] == 0):
                outsider_points.append((i, trial_values[i]))
        if (trial_values_outsiders[len(trial_values_outsiders) - 1] == 1):
            outsider_points.append((len(trial_values_outsiders) - 1, trial_values[len(trial_values_outsiders) - 1]))

        trial_bursts_intervals_lengths = []
        if (len(outsider_points) != 0):
            for i in range(0, len(outsider_points), 2):
                trial_bursts_intervals_lengths.append(outsider_points[i + 1][0] - outsider_points[i][0] + 1)
        trial_avg_bursts_intervals_length = np.mean(trial_bursts_intervals_lengths)

        print("Trial " + str(
        trial_index+1) + " " + str(trial_avg_bursts_amplitudes) + " " + str(trial_max_burst_amplitude) + " " + str(
        trial_avg_bursts_intervals_length))

        # print("Trial " + str(
        #     trial_index + 1) + " " + str(trial_bursts_percentage))


data_dir = os.path.join('..', '../..')

levels = ['light1', 'deep2','medium3', 'light4', 'medium5']
all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28,
                29, 30,
                31, 32]

initialization = InitDataSet(current_directory=data_dir, subject_directory='m014',
                             filtering_directory='classic',
                             levels=levels)
doas = initialization.get_dataset_as_doas()
mark_bursts_regions(doas)
# remove_bursted_trials_when_segment(doas)


for level_ind, level in enumerate(levels):
    print(level)
    for ch_ind, channel in enumerate(all_channels):
        print("Channel" + str(channel))
        get_channel_stats(doas, level, channel)
