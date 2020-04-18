'''
    written by Ioana Onofrei
'''
import numpy as np
import matplotlib.pyplot as plt

from utils.Utils import get_doa_of_level, get_channel_index, \
    get_one_trial__all_segments_values_from_doa_by_channel_with_bursts_flags


def plot_channels_trial(doas, doa_level, channel_numbers, trial_number, stdX):
    contor = 0

    doa = get_doa_of_level(doas, doa_level)

    for ch_number in range(len(channel_numbers)):
        channel_index = get_channel_index(doa, channel_numbers[ch_number])

        # channel_mean = doa.channels[channel_index].mean
        channel_mean = 0

        trial_values, trial_values_outsiders = get_one_trial__all_segments_values_from_doa_by_channel_with_bursts_flags(
            doas, level=doa_level, channel_number=channel_numbers[ch_number], trial_number=trial_number)
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

        print(outsider_points)

        plt.plot(np.arange(0, len(trial_values)), list(map(lambda x: x + contor, trial_values)),
                 label='Channel ' + str(channel_numbers[ch_number]))

        plt.axhline(y=channel_mean + contor, linewidth=0.3, color='r')

        for i in range(0, len(outsider_points), 2):
            x_values = [outsider_points[i][0], outsider_points[i + 1][0]]
            y_values = [channel_mean + contor, channel_mean + contor]
            plt.plot(x_values, y_values, color='black')
        contor += 100

    plt.ylabel('Amplitudes')
    plt.xlabel('Relative Timestamp')
    plt.title('Trial ' + str(trial_number) + ' Snapshot')
    plt.legend(loc='upper center', bbox_to_anchor=(0.2, -0.05),
               fancybox=True, shadow=True, ncol=5)
    plt.savefig(f'{doa_level}_t{trial_number}')
    plt.show()
