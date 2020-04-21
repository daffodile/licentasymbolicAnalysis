import scipy

import numpy as np

from input_reader.InitDataSet import InitDataSet
from utils.mark_bursts.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_burst_basic


def mak_burst_basic(doas, threshold):
    for doa in doas:
        for channel in doa.channels:
            for trial in channel.trials:
                values_outsiders_1 = np.where(np.abs(trial.spontaneous.values) < threshold, 0, 1)
                trial.spontaneous.set_values_outsiders(values_outsiders_1)
                values_outsiders_2 = np.where(np.abs(trial.stimulus.values) < threshold, 0, 1)
                trial.stimulus.set_values_outsiders(values_outsiders_2)
                values_outsiders_3 = np.where(np.abs(trial.poststimulus.values) < threshold, 0, 1)
                trial.poststimulus.set_values_outsiders(values_outsiders_3)


def see_procents_distances(doas, q=0.95):
    distances = []

    for doa in doas:
        for channel in doa.channels:
            for trial in channel.trials:

                burst_detection_flag = False
                burst_detection_flag = (1 in trial.spontaneous.values_outsiders) or (
                        1 in trial.stimulus.values_outsiders) or (1 in trial.poststimulus.values_outsiders)

                if burst_detection_flag:

                    trial_values = []
                    trial_values.extend(trial.spontaneous.values)
                    trial_values.extend(trial.stimulus.values)
                    trial_values.extend(trial.poststimulus.values)

                    trial_values_outsiders = []
                    trial_values_outsiders.extend(trial.spontaneous.values_outsiders)
                    trial_values_outsiders.extend(trial.stimulus.values_outsiders)
                    trial_values_outsiders.extend(trial.poststimulus.values_outsiders)

                    outside_in = []
                    outside_out = []

                    if trial_values_outsiders[0] == 1:
                        outside_in.append((0, trial_values[0]))
                    for i in range(len(trial_values_outsiders) - 1):
                        if trial_values_outsiders[i] == 0 and trial_values_outsiders[i + 1] == 1:
                            outside_in.append((i + 1, trial_values[i + 1]))
                        if trial_values_outsiders[i] == 1 and trial_values_outsiders[i + 1] == 0:
                            outside_out.append((i, trial_values[i]))
                    if trial_values_outsiders[len(trial_values_outsiders) - 1] == 1:
                        outside_out.append(
                            (len(trial_values_outsiders) - 1, trial_values[len(trial_values_outsiders) - 1]))

                    if len(outside_in) == len(outside_out):
                        for ind_tuple in range(len(outside_in) - 1):
                            # get the beginning and ending of the inter bursts zone
                            index_start = outside_out[ind_tuple][0]
                            index_end = outside_in[ind_tuple + 1][0]
                            dist_within = index_end - index_start

                            distances.append(dist_within)

    quantile = np.quantile(distances, q=q)

    print(f'quantile={quantile} for q = {q}')

    return quantile


initialization = InitDataSet(levels=['deep', 'medium', 'light'])
doas = initialization.get_dataset_as_doas()

# print('start marking interbursts')
# mark_burst_basic_one_threshold(doas, threshold=19.94)
# print('see inter bursts distances')
# see_procents_distances(doas)
#
# '''
#     output of the script: quantile=364.0 for q = 0.95
#
# '''

mark_burst_basic(doas, thresholds={'deep': 19.74, 'medium': 24.97, 'light': 32.00})
see_procents_distances(doas)

'''
    output: quantile=594.0 for q = 0.95
'''
