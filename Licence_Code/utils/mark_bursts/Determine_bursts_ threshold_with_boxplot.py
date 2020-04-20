'''
    call once to determine the threshold used for marking bursts
'''
from pylab import *

from utils.MarkOutsidersWithBurstsFlags_OneThreshold import mark_burst_basic_one_threshold

from input_reader.InitDataSet import InitDataSet


def determine_threshold(doas, iterations=8):
    '''
    :param doas: full data set
    :param iterations=how many times re-calculate the threshold after marking bursts
    :return:
    '''
    print("START marking outliners of trials")

    # get the minimum value from the ouliers of the whole dataset
    threshold = get_initial_threshold(doas)

    # mark the bursts for the first time, according to first threshold
    mark_burst_basic_one_threshold(doas, threshold)

    new_th = 0
    for it in range(iterations):
        new_th = get_threshold_non_bursts_values(doas)
        print(f'{it}th iteration updated_th {new_th}')
        mark_burst_basic_one_threshold(doas, new_th)

    print(f'final threshold is {new_th}')
    return new_th


def get_initial_threshold(doas):
    all_values_full = []

    for doa in doas:
        for channel in doa.channels:
            for trial in channel.trials:
                all_values_full.extend(trial.spontaneous.values)
                all_values_full.extend(trial.stimulus.values)

    r = boxplot(x=all_values_full)
    # from boxplot get the outliers from above and bellow it
    top_points = r["fliers"][0].get_data()[1]
    aboslute_values = np.abs(top_points)

    threshold = np.amin(aboslute_values)
    print(f"min fliers {threshold}")
    return threshold


def get_threshold_non_bursts_values(doas):
    all_values_nonbursts = []

    for doa in doas:
        for channel in doa.channels:
            for trial in channel.trials:
                sp_values = trial.spontaneous.values
                sp_outsiders = trial.spontaneous.values_outsiders

                for index in range(len(sp_values)):
                    if (sp_outsiders[index] != 1):
                        all_values_nonbursts.append(sp_values[index])

                stim_values = trial.stimulus.values
                stim_outsiders = trial.stimulus.values_outsiders

                for index in range(len(stim_values)):
                    if (stim_outsiders[index] != 1):
                        all_values_nonbursts.append(stim_values[index])

    r = boxplot(x=all_values_nonbursts)

    top_points = r["fliers"][0].get_data()[1]
    aboslute_values = np.abs(top_points)

    return np.amin(aboslute_values)


######### call the above methods

initialization = InitDataSet(levels=['deep', 'medium', 'light'])
doas = initialization.get_dataset_as_doas()
determine_threshold(doas)
