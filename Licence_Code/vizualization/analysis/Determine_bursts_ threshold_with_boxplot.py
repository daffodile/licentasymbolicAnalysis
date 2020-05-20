'''
    call once to determine the threshold used for marking bursts
'''
from scipy.signal import hilbert
import os
from input_reader.InitDataSetWithBurstsFlags import InitDataSetWithBurstsFlags
from pylab import *

all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
                31, 32]


def determine_thresholds(doas, iterations=8, whis=2.0):
    '''
    :param doas: full data set
    :param iterations=how many times re-calculate the threshold after marking bursts
    :return:
    '''
    print("START determining  outliers of channels")

    # get the minimum value from the ouliers of the whole dataset
    init_thresholds = get_initial_thresholds(doas, whis)

    # mark the bursts for the first time, according to first threshold
    mark_burst_basic_thresholds(doas, init_thresholds)

    for it in range(iterations):
        new_thresholds = get_thresholds_non_bursts_values(doas, whis)
        print(f'{it}th iteration updated ')
        mark_burst_basic_thresholds(doas, new_thresholds)

    print('DONE interating')


def mark_burst_basic_thresholds(doas, all_thresholds: dict):
    for doa in doas:
        for channel in doa.channels:
            ths = all_thresholds[f'{channel.number}']
            for trial in channel.trials:
                # ddf = np.where(array < =-16 or array > 16, 1, 0)
                values_outsiders_1 = np.where(trial.spontaneous.values < ths[0], 1,
                                              (np.where(trial.spontaneous.values > ths[1], 1, 0)))

                trial.spontaneous.set_values_outsiders(values_outsiders_1)

                values_outsiders_2 = np.where(trial.stimulus.values < ths[0], 1,
                                              (np.where(trial.stimulus.values > ths[1], 1, 0)))

                trial.stimulus.set_values_outsiders(values_outsiders_2)

                values_outsiders_3 = np.where(trial.poststimulus.values < ths[0], 1,
                                              (np.where(trial.poststimulus.values > ths[1], 1, 0)))
                trial.poststimulus.set_values_outsiders(values_outsiders_3)


# def mark_burst_hilbert_thresholds(doas, thresholds):
#     for doa in doas:
#         for channel in doa.channels:
#             threshold = thresholds[channel.number]
#             for trial in channel.trials:
#                 values_outsiders_1 = np.where(
#                     hilbert(trial.spontaneous.values) < thresholds[0] or hilbert(trial.spontaneous.values) > thresholds[
#                         1], 0, 1)
#                 trial.spontaneous.set_values_outsiders(values_outsiders_1)
#
#                 values_outsiders_2 = np.where(
#                     hilbert(trial.stimulus.values) < thresholds[0] or hilbert(trial.stimulus.values) > thresholds[
#                         1], 0, 1)
#                 trial.stimulus.set_values_outsiders(values_outsiders_2)
#
#                 values_outsiders_3 = np.where(
#                     hilbert(trial.poststimulus.values) < thresholds[0] or hilbert(trial.poststimulus.values) >
#                     thresholds[
#                         1], 0, 1)
#                 trial.poststimulus.set_values_outsiders(values_outsiders_3)


def get_initial_thresholds(doas, whis):
    print('get initial thresholds set')

    ch_number = len(doas[0].channels)

    all_values_per_channel = [[] for i in range(ch_number)]

    for doa in doas:
        for ind_channel, channel in enumerate(doa.channels):
            for trial in channel.trials:
                all_values_per_channel[ind_channel].extend(trial.spontaneous.values)
                all_values_per_channel[ind_channel].extend(trial.stimulus.values)

    thresholds = {}

    for ind_ch in range(ch_number):
        r = boxplot(x=all_values_per_channel[ind_ch], whis=whis)

        whiskers_jos = r['whiskers'][0].get_data()[1][1]
        whiskers_sus = r['whiskers'][1].get_data()[1][1]
        # print(whiskers_jos)
        #         # print(whiskers_sus)
        #         # # from boxplot get the outliers from above and bellow it
        #         # top_points = r["fliers"][0].get_data()[1]
        #         # print(top_points)
        #         # aboslute_values = np.abs(top_points)
        #         #
        #         # current_threshold = np.amin(aboslute_values)

        thresholds.update({str(all_channels[ind_ch]): [whiskers_jos, whiskers_sus]})

    print('initial thresholds')
    print(thresholds)
    return thresholds


def get_thresholds_non_bursts_values(doas, whis):
    ch_number = len(doas[0].channels)

    all_values_per_channel = [[] for i in range(ch_number)]

    for doa in doas:
        for ind_channel, channel in enumerate(doa.channels):
            for trial in channel.trials:
                sp_values = trial.spontaneous.values
                sp_outsiders = trial.spontaneous.values_outsiders

                for index in range(len(sp_values)):
                    if (sp_outsiders[index] != 1):
                        all_values_per_channel[ind_channel].append(sp_values[index])

                stim_values = trial.stimulus.values
                stim_outsiders = trial.stimulus.values_outsiders

                for index in range(len(stim_values)):
                    if (stim_outsiders[index] != 1):
                        all_values_per_channel[ind_channel].append(stim_values[index])

    thresholds = {}

    for ind_ch in range(ch_number):
        r = boxplot(x=all_values_per_channel[ind_ch], whis=whis)

        whiskers_jos = r['whiskers'][0].get_data()[1][1]
        whiskers_sus = r['whiskers'][1].get_data()[1][1]

        thresholds.update({str(all_channels[ind_ch]): [whiskers_jos, whiskers_sus]})

    print('thresholds:')
    print(thresholds)
    return thresholds


######### call the above methods


data_dir = os.path.join('..', '..')
levels = ['deep9', 'medium10', 'light11']
# levels = ['deep6', 'light7', 'medium8']
# initialization = InitDataSetWithBurstsFlags(data_dir, levels=levels)
initialization = InitDataSetWithBurstsFlags(current_directory=data_dir, subject_directory="m016",
                                            filtering_directory="classic",
                                            levels=levels)

doas = initialization.get_dataset_as_doas()
# determine_thresholds(doas)

get_initial_thresholds(doas, 2.0)
