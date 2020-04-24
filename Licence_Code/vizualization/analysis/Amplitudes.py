from input_reader.InitDataSet import InitDataSet
from utils.Utils import get_trial_values_and_outsiders, get_doa_of_level
from utils.mark_bursts.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions
import numpy as np

initialization = InitDataSet(levels=['deep', 'medium', 'light'])
doas = initialization.get_dataset_as_doas()
mark_bursts_regions(doas)

all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
                31, 32]


def get_channel_bursts_mean(doas, doa_level, channel_number):
    doa = get_doa_of_level(doas, doa_level)
    all_bursts = []
    for trial_number in range(240):
        trial_values, trial_values_outsiders = get_trial_values_and_outsiders(doa,
                                                                              channel_number,
                                                                              trial_number + 1)
        trial_bursts = []
        for i in range(len(trial_values_outsiders)):
            if (trial_values_outsiders[i] == 1):
                trial_bursts.append(trial_values[i])
        all_bursts.extend(trial_bursts)
    # return np.mean(all_bursts),np.std(all_bursts)
    return np.mean(np.abs(all_bursts)), np.std(all_bursts)


def get_channel_mean(doas, doa_level, channel_number):
    doa = get_doa_of_level(doas, doa_level)
    channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
    all_trials = []
    for trial in channel.trials:
        all_trials.extend(trial.spontaneous.values)
        all_trials.extend(trial.stimulus.values)
        all_trials.extend(trial.poststimulus.values)

    # return np.mean(all_trials)
    return np.mean(np.abs(all_trials)), np.std(all_trials)


def get_channel_maximum_burst(doas, doa_level, channel_number):
    doa = get_doa_of_level(doas, doa_level)
    channel_max_bursts_amplitudes = []
    for trial_number in range(240):
        trial_values, trial_values_outsiders = get_trial_values_and_outsiders(doa,
                                                                              channel_number,
                                                                              trial_number + 1)
        trial_bursts_amplitudes = []
        for i in range(len(trial_values_outsiders)):
            if (trial_values_outsiders[i] == 1):
                trial_bursts_amplitudes.append(trial_values[i])
        channel_max_bursts_amplitudes.extend(trial_bursts_amplitudes)
    return max(channel_max_bursts_amplitudes)


# for ch_nr in range(len(all_channels)):
#     print('Channel ' + str(all_channels[ch_nr]) + ' deep ' + str(
#         get_channel_maximum_burst(doas, 'deep', all_channels[ch_nr])))
#     print('Channel ' + str(all_channels[ch_nr]) + ' medium ' + str(
#         get_channel_maximum_burst(doas, 'medium', all_channels[ch_nr])))
#     print('Channel ' + str(all_channels[ch_nr]) + ' light ' + str(
#         get_channel_maximum_burst(doas, 'light', all_channels[ch_nr])))

ch_number = 20
print(get_channel_mean(doas, 'deep', ch_number))
print(get_channel_bursts_mean(doas, 'deep', ch_number))
