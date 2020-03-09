import os
import sys

import numpy as np

from input_reader.CreateDOA import CreateDOA
# write the results here
from feature_extraction.TESPAR.Encoding import Encoding

path = os.getcwd()
fileName = path + "/results_3hz.txt"
results_file = open(fileName, "w")

# lags value to be tested
lags_values = [0, 1, 3, 5]

# encoder used
encoder = Encoding('../VQ_REMAKE/alphabet.txt')
a_size = (len(encoder.a_matrix), len(encoder.a_matrix[0]))

#  read input doas
data_dir = os.path.join('', '..')
data_dir = os.path.join(data_dir, 'Data/cutoff3hz', '')
sys.path.append(data_dir)

doa_info = {
    'deep': {
        'epd': 'M014_S001_SRCS3L_25,50,100_0002.epd',
        'eti': 'Results M014_S001_SRCS3L_25,50,100_0002 Variable contrast, all orientations.eti'
    },

    'light': {
        'epd': 'M014_S001_SRCS3L_25,50,100_0004.epd',
        'eti': 'Results M014_S001_SRCS3L_25,50,100_0004 Variable contrast, all orientations.eti'
    }
}
doas = []

print("Load dataset in doas...")
for key, value in doa_info.items():
    doa_factory = CreateDOA(data_dir, value['epd'], value['eti'], key)
    doa = doa_factory.create()
    doas.append(doa)

ch_numbers = len(doas[0].channels)
trials_numbers = len(doas[0].channels[0].trials)

print('Dataset is loaded')
max_spontaneous = 0
lag_max_spontaneous = -1
max_stimulus = 0
lag_max_stimulus = -1
max_poststimulus = 0
lag_max_poststimulus = -1
max_total = 0
lag_max = -1

'''
            2 * 30 * 3 =

        am 3 doas = >> ma intereseaza doa DEEP si doa LIGHT !!
                30 de canale pe fiecare => 30 de medii de diferente intre matricile TESPAR A si S
                  UN canal are 240 trials cu cate 3 segmente each


    - 30 de matrici diferenta => pe fiecare canal va fi suma de diferente pe diff pre, stim, post
'''

print('Start computing')
for lag in lags_values:
    results_file.write('\nlag ' + str(lag) + '\n')
    print('lag ' + str(lag) + '\n')
    # total sums for this lag
    lag_diff_spontaneous = 0
    lag_diff_stimulus = 0
    lag_diff_poststimulus = 0
    lag_diff_total = 0

    for ch_index in range(ch_numbers):
        # at ch_index in range [1 .. 30]
        diff_spontaneous = np.zeros(a_size, dtype='i')
        diff_stimulus = np.zeros(a_size, dtype='i')
        diff_poststimulus = np.zeros(a_size, dtype='i')

        # here sum of the differeces matrix between DEEP and LIGHT
        for trial_index in range(trials_numbers):
            t_deep = doas[0].channels[ch_index].trials[trial_index]
            t_light = doas[1].channels[ch_index].trials[trial_index]
            diff_spontaneous += np.absolute(np.array(encoder.get_a(t_deep.spontaneous.values, lag)) -
                                            np.array(encoder.get_a(t_light.spontaneous.values, lag)))

            diff_stimulus += np.absolute(np.array(encoder.get_a(t_deep.stimulus.values, lag)) -
                                         np.array(encoder.get_a(t_light.stimulus.values, lag)))

            diff_poststimulus += np.absolute(np.array(encoder.get_a(t_deep.poststimulus.values, lag)) -
                                             np.array(encoder.get_a(t_light.poststimulus.values, lag)))

        results_file.write('channel ' + str(ch_index) + ' \n')
        print('channel ' + str(ch_index) + ' \n')

        # average of the trials_numbers trials
        diff_spontaneous = diff_spontaneous / trials_numbers
        # sum of the averages  in this channel
        res_spontaneous = diff_spontaneous.sum()
        results_file.write(str(res_spontaneous) + ' spontaneous\n')
        print(str(res_spontaneous) + ' spontaneous\n')
        lag_diff_spontaneous += res_spontaneous

        diff_stimulus = diff_stimulus / trials_numbers
        res_stimulus = diff_stimulus.sum()
        results_file.write(str(res_stimulus) + ' stimulus\n')
        print(str(res_stimulus) + ' stimulus\n')
        lag_diff_stimulus += res_stimulus

        diff_poststimulus = diff_poststimulus / trials_numbers
        res_poststimulus = diff_poststimulus.sum()
        results_file.write(str(res_poststimulus) + ' poststimulus\n')
        print(str(res_poststimulus) + ' poststimulus\n')
        lag_diff_poststimulus += res_poststimulus

        # write down the sum of the averages on the 3 segments
        diff_total = res_spontaneous + res_stimulus + res_poststimulus
        results_file.write(str(diff_total) + ' total\n')
        print(str(diff_total) + ' total\n')
        lag_diff_total += diff_total

        print('done for channel ' + str(ch_index))

    # write down the averages of the channel_numbers for this lag
    results_file.write('\naverages for this lag ' + str(lag) + '\n')
    lag_diff_spontaneous /= ch_numbers
    results_file.write(str(lag_diff_spontaneous) + ' spontaneous lag\n')
    print(str(lag_diff_spontaneous) + ' average spontaneous')
    if lag_diff_spontaneous > max_spontaneous:
        max_spontaneous = lag_diff_spontaneous
        lag_max_spontaneous = lag

    lag_diff_stimulus /= ch_numbers
    results_file.write(str(lag_diff_stimulus) + ' stimulus\n')
    print(str(lag_diff_stimulus) + ' average stimulus')
    if lag_diff_stimulus > max_stimulus:
        max_stimulus = lag_diff_stimulus
        lag_max_stimulus = lag

    lag_diff_poststimulus /= ch_numbers
    results_file.write(str(lag_diff_poststimulus) + ' poststimulus\n')
    print(str(lag_diff_poststimulus) + ' average poststimulus')
    if lag_diff_poststimulus > max_poststimulus:
        max_poststimulus = lag_diff_poststimulus
        lag_max_poststimulus = lag

    lag_diff_total = lag_diff_total / ch_numbers
    results_file.write(str(lag_diff_total) + ' total\n')
    print(str(lag_diff_total) + ' average total')
    if lag_diff_total > max_total:
        max_total = lag_diff_total  # :|
        lag_max = lag

results_file.write('best results for spontaneous ' + str(lag_max_spontaneous) + ' \n')
results_file.write('best results for stimulus ' + str(lag_max_stimulus) + ' \n')
results_file.write('best results for poststimulus ' + str(lag_max_poststimulus) + ' \n')
results_file.write('best results total ' + str(lag_max) + ' \n')

results_file.close()
