import os

import numpy as np
import matplotlib.pyplot as plt

from input_reader.InitDataSet import InitDataSet
from utils.Utils import get_doa_of_level


def get_channel_avg(doas, doa_level, channel_number, segment):
    doa = get_doa_of_level(doas, doa_level)
    channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
    channel_trials = []
    for trial in channel.trials:
        temp_trial_values = []
        temp_trial_values.extend(getattr(trial, segment).values)
        if (len(temp_trial_values) == 2672):
            temp_trial_values.extend([0])
        channel_trials.append(temp_trial_values)
    channel_avg = np.mean(channel_trials, axis=0)
    return channel_avg


def plot_erp(doas, doa_level, channels, segment):
    contor = 0

    for i in range(len(channels)):
        channel_avg = get_channel_avg(doas, doa_level, channels[i], segment)[0:500]
        plt.plot(np.arange(0, len(channel_avg)), list(map(lambda x: x + contor, channel_avg)),
                 label='Channel ' + str(channels[i]))
        contor += 10

    plt.ylabel('Amplitudes')
    plt.xlabel('Relative Timestamp')
    plt.title('Segment ' + segment.capitalize() + ' Snapshot - ' + doa_level.capitalize())
    plt.legend(loc='upper center', bbox_to_anchor=(0.2, -0.05),
               fancybox=True, shadow=True, ncol=5)
    plt.show()


data_dir = os.path.join('..', '../..')
initialization = InitDataSet(current_directory=data_dir, subject_directory='m014', filtering_directory='classic',
                             levels=['light1', 'deep2', 'medium3', 'light4', 'medium5'])
doas = initialization.get_dataset_as_doas()
plot_erp(doas, 'light1', [2, 3, 4, 5, 6, 26, 27, 28, 29, 30], 'stimulus')
plot_erp(doas, 'deep2', [2, 3, 4, 5, 6, 26, 27, 28, 29, 30], 'stimulus')
plot_erp(doas, 'medium3', [2, 3, 4, 5, 6, 26, 27, 28, 29, 30], 'stimulus')
plot_erp(doas, 'light4', [2, 3, 4, 5, 6, 26, 27, 28, 29, 30], 'stimulus')
plot_erp(doas, 'medium5', [2, 3, 4, 5, 6, 26, 27, 28, 29, 30], 'stimulus')
