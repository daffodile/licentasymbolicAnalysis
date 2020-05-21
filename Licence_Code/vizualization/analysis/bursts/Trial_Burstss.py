import os

import numpy as np
import matplotlib.pyplot as plt

from input_reader.InitDataSet import InitDataSet
from utils.Utils import get_doa_of_level, get_trial_values_and_outsiders, get_channel_index
from utils.mark_bursts.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions


def get_channel_avg_bursts_length(doas, doa_level):
    doa = get_doa_of_level(doas, doa_level)

    channels_bursts_length_avg = []

    for channel_index in range(len(doa.channels)):

        channel_trials_bursts_length_avg = []

        for trial_index in range(240):

            trial_values, trial_values_outsiders = get_trial_values_and_outsiders(doa,
                                                                                  doa.channels[channel_index].number,
                                                                                  trial_index + 1)
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

            # print(outsider_points)

            trial_bursts_intervals_length = []
            if (len(outsider_points) != 0):
                for i in range(0, len(outsider_points), 2):
                    trial_bursts_intervals_length.append(outsider_points[i + 1][0] - outsider_points[i][0] + 1)
                channel_trials_bursts_length_avg.append(np.mean(trial_bursts_intervals_length))
            else:
                channel_trials_bursts_length_avg.append(0)

        channels_bursts_length_avg.append(
            (doa.channels[channel_index].number, np.mean(channel_trials_bursts_length_avg)))

    return channels_bursts_length_avg

data_dir = os.path.join('..', '../..')

levels = ['light1', 'deep2', 'medium3', 'light4', 'medium5']
initialization = InitDataSet(current_directory=data_dir, subject_directory='m014', filtering_directory='classic',
                             levels=levels)
doas = initialization.get_dataset_as_doas()
mark_bursts_regions(doas)
for level_ind, level in enumerate(levels):
    print(get_channel_avg_bursts_length(doas, level))
