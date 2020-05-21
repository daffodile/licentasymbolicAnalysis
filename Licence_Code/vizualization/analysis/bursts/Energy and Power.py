import numpy as np
from utils.Utils import get_doa_of_level, get_trial_values_and_outsiders
from utils.mark_bursts.MarkOutsidersWithBurstsFlags import remove_bursted_trials_when_segment


def get_channel_bursts_energy_power(doas, doa_level, channel_number):
    doa = get_doa_of_level(doas, doa_level)
    channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
    all_bursts = []
    for trial in channel.trials:
        trial_values, trial_values_outsiders = get_trial_values_and_outsiders(doa,
                                                                              channel_number,
                                                                              trial.trial_number)
        trial_bursts = []
        for i in range(len(trial_values_outsiders)):
            if (trial_values_outsiders[i] == 1):
                trial_bursts.append(trial_values[i])
        all_bursts.extend(trial_bursts)
    bursts_energy = 0
    for i in range(len(all_bursts)):
        bursts_energy += np.math.pow(np.abs(all_bursts[i]), 2)
    bursts_power = bursts_energy / len(all_bursts)
    return bursts_energy, bursts_power


def get_channel_energy_power(doas, doa_level, channel_number):
    doa = get_doa_of_level(doas, doa_level)
    channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
    all_trials = []
    for trial in channel.trials:
        all_trials.extend(trial.spontaneous.values)
        all_trials.extend(trial.stimulus.values)
        all_trials.extend(trial.poststimulus.values)
    channel_energy = 0
    for i in range(len(all_trials)):
        channel_energy += np.math.pow(np.abs(all_trials[i]), 2)
    channel_power = channel_energy / len(all_trials)
    return channel_energy, channel_power


def get_doa_means_statistics(doas, doa_level, all_channels):
    channels_eng_pow = []
    channels_bursts_eng_pow = []

    for ch_nr in range(len(all_channels)):
        channels_eng_pow.append(get_channel_energy_power(doas, doa_level, all_channels[ch_nr]))
        channels_bursts_eng_pow.append(get_channel_bursts_energy_power(doas, doa_level, all_channels[ch_nr]))

    return channels_eng_pow, channels_bursts_eng_pow


import os
from input_reader.InitDataSet import InitDataSet
from utils.mark_bursts.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions

levels = ['medium1', 'light2', 'deep3', 'light4', 'medium5', 'deep6']
data_dir = os.path.join('..', '../..')
initialization = InitDataSet(current_directory=data_dir, subject_directory='m013', filtering_directory='classic',
                             levels=levels)
doas = initialization.get_dataset_as_doas()
mark_bursts_regions(doas, subject='m013')
# REMOVE BURSTS TO SEE HOW THINGS CHANGED
# remove_bursted_trials_when_segment(doas)

all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
                31, 32] 

labels = ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17',
          'C18', 'C19', 'C20', 'C21', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30',
          'C31', 'C32']

medium1_channels_eng_pow, medium1_channels_bursts_eng_pow = get_doa_means_statistics(doas, 'medium1', all_channels)
light2_channels_eng_pow, light2_channels_bursts_eng_pow = get_doa_means_statistics(doas, 'light2', all_channels)
deep3_channels_eng_pow, deep3_channels_bursts_eng_pow = get_doa_means_statistics(doas, 'deep3', all_channels)
light4_channels_eng_pow, light4_channels_bursts_eng_pow = get_doa_means_statistics(doas, 'light4', all_channels)
medium5_channels_eng_pow, medium5_channels_bursts_eng_pow = get_doa_means_statistics(doas, 'medium5', all_channels)
deep6_channels_eng_pow, deep6_channels_bursts_eng_pow = get_doa_means_statistics(doas, 'deep6', all_channels)

print("############################ only bursts####################")

if (len(medium1_channels_bursts_eng_pow) != 0):
    print("medium1")
    print("energy")
    for i in range(len(medium1_channels_bursts_eng_pow)):
        print(str(medium1_channels_bursts_eng_pow[i][0]))
    print("power")
    for i in range(len(medium1_channels_bursts_eng_pow)):
        print(str(medium1_channels_bursts_eng_pow[i][1]))
else:
    print("no medium1 values")

if (len(light2_channels_bursts_eng_pow) != 0):
    print("light2")
    print("energy")
    for i in range(len(light2_channels_bursts_eng_pow)):
        print(str(light2_channels_bursts_eng_pow[i][0]))
    print("power")
    for i in range(len(light2_channels_bursts_eng_pow)):
        print(str(light2_channels_bursts_eng_pow[i][1]))
else:
    print("no light2 values")

if (len(deep3_channels_bursts_eng_pow) != 0):
    print("deep3")
    print("energy")
    for i in range(len(deep3_channels_bursts_eng_pow)):
        print(str(deep3_channels_bursts_eng_pow[i][0]))
    print("power")
    for i in range(len(deep3_channels_bursts_eng_pow)):
        print(str(deep3_channels_bursts_eng_pow[i][1]))
else:
    print("no deep3 values")

if (len(light4_channels_bursts_eng_pow) != 0):
    print("light4")
    print("energy")
    for i in range(len(light4_channels_bursts_eng_pow)):
        print(str(light4_channels_bursts_eng_pow[i][0]))
    print("power")
    for i in range(len(light4_channels_bursts_eng_pow)):
        print(str(light4_channels_bursts_eng_pow[i][1]))
else:
    print("no light4 values")

if (len(medium5_channels_bursts_eng_pow) != 0):
    print("medium5")
    print("energy")
    for i in range(len(medium5_channels_bursts_eng_pow)):
        print(str(medium5_channels_bursts_eng_pow[i][0]))
    print("power")
    for i in range(len(medium5_channels_bursts_eng_pow)):
        print(str(medium5_channels_bursts_eng_pow[i][1]))
else:
    print("no medium5 values")

if (len(deep6_channels_bursts_eng_pow) != 0):
    print("deep6")
    print("energy")
    for i in range(len(deep6_channels_bursts_eng_pow)):
        print(str(deep6_channels_bursts_eng_pow[i][0]))
    print("power")
    for i in range(len(deep6_channels_bursts_eng_pow)):
        print(str(deep6_channels_bursts_eng_pow[i][1]))
else:
    print("no medium5 values")

print("############################ full channels####################")
print("medium1")
print("energy")
for i in range(len(medium1_channels_eng_pow)):
    print(str(medium1_channels_eng_pow[i][0]))
print("power")
for i in range(len(medium1_channels_eng_pow)):
    print(str(medium1_channels_eng_pow[i][1]))
print("light2")
print("energy")
for i in range(len(light2_channels_eng_pow)):
    print(str(light2_channels_eng_pow[i][0]))
print("power")
for i in range(len(light2_channels_eng_pow)):
    print(str(light2_channels_eng_pow[i][1]))
print("deep3")
print("energy")
for i in range(len(deep3_channels_eng_pow)):
    print(str(deep3_channels_eng_pow[i][0]))
print("power")
for i in range(len(deep3_channels_eng_pow)):
    print(str(deep3_channels_eng_pow[i][1]))
print("light4")
print("energy")
for i in range(len(light4_channels_eng_pow)):
    print(str(light4_channels_eng_pow[i][0]))
print("power")
for i in range(len(light4_channels_eng_pow)):
    print(str(light4_channels_eng_pow[i][1]))
print("medium5")
print("energy")
for i in range(len(medium5_channels_eng_pow)):
    print(str(medium5_channels_eng_pow[i][0]))
print("power")
for i in range(len(medium5_channels_eng_pow)):
    print(str(medium5_channels_eng_pow[i][1]))
print("deep6")
print("energy")
for i in range(len(deep6_channels_eng_pow)):
    print(str(deep6_channels_eng_pow[i][0]))
print("power")
for i in range(len(deep6_channels_eng_pow)):
    print(str(deep6_channels_eng_pow[i][1]))
