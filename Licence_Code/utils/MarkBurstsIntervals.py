import sys

import numpy as np

from input_reader.InitDataSet import InitDataSet
from vizualization.analysis.ploting_functions import plot_hist


def analyse_interburst_intervals(doas, liberty=2, max_interbursts_dist=500):
    """
    function to mark the values that ore outside interval
          [ mean - liberty*std_dev,  mean + liberty*std_dev]
    on each channel in each DOA
    :param doas: array of DOAs to mark
    :param liberty: coeff for multiplying with std_dev on a channel
    :param use_hilbert_transform: bool, choose if using hilbert trasnform
    :return: modify doas in situ, no return type
    """
    inter_bursts_distribution = []

    print("START marking outliners for trials")
    for doa in doas:
        print(f'doa {doa.level}')
        for channel in doa.channels:
            all_trials = []
            for trial in channel.trials:
                all_trials.extend(trial.spontaneous.values)
                all_trials.extend(trial.stimulus.values)
                all_trials.extend(trial.poststimulus.values)

            channel.mean = np.mean(all_trials)
            channel.std_der = np.std(all_trials)
            # print(f'ch {channel.number} mean:{channel.mean} std_dev {channel.std_der}')

            for trial in channel.trials:
                burst_detection_flag = False

                values_outsiders_1 = np.where(np.abs(trial.spontaneous.values) < liberty * channel.std_der, 0, 1)
                trial.spontaneous.set_values_outsiders(values_outsiders_1)

                values_outsiders_2 = np.where(np.abs(trial.stimulus.values) < liberty * channel.std_der, 0, 1)
                trial.stimulus.set_values_outsiders(values_outsiders_2)

                values_outsiders_3 = np.where(np.abs(trial.poststimulus.values) < liberty * channel.std_der, 0, 1)
                trial.poststimulus.set_values_outsiders(values_outsiders_3)

                burst_detection_flag = (1 in values_outsiders_1) or (1 in values_outsiders_2) or (
                        1 in values_outsiders_3)
                # print(f' trial {trial.trial_number}   flag {burst_detection_flag}')

                if burst_detection_flag:
                    trial_values = []
                    trial_values.extend(trial.spontaneous.values)
                    trial_values.extend(trial.stimulus.values)
                    trial_values.extend(trial.poststimulus.values)

                    trial_values_outsiders = []
                    trial_values_outsiders.extend(trial.spontaneous.values_outsiders)
                    trial_values_outsiders.extend(trial.stimulus.values_outsiders)
                    trial_values_outsiders.extend(trial.poststimulus.values_outsiders)

                    outsider_points = []
                    outside_in = []
                    outside_out = []
                    if trial_values_outsiders[0] == 1:
                        outsider_points.append((0, trial_values[0]))
                        outside_in.append((0, trial_values[0]))
                    for i in range(len(trial_values_outsiders) - 1):
                        if trial_values_outsiders[i] == 0 and trial_values_outsiders[i + 1] == 1:
                            outsider_points.append((i + 1, trial_values[i + 1]))
                            outside_in.append((i + 1, trial_values[i + 1]))
                        if trial_values_outsiders[i] == 1 and trial_values_outsiders[i + 1] == 0:
                            outsider_points.append((i, trial_values[i]))
                            outside_out.append((i, trial_values[i]))
                    if trial_values_outsiders[len(trial_values_outsiders) - 1] == 1:
                        outsider_points.append(
                            (len(trial_values_outsiders) - 1, trial_values[len(trial_values_outsiders) - 1]))
                        outside_out.append(
                            (len(trial_values_outsiders) - 1, trial_values[len(trial_values_outsiders) - 1]))

                    # print(outsider_points)
                    # print(outside_in)
                    # print(outside_out)

                    if len(outside_in) == len(outside_out):
                        for ind_tuple in range(len(outside_in) - 1):
                            dist_within = outside_in[ind_tuple + 1][0] - outside_out[ind_tuple][0]
                            if dist_within < max_interbursts_dist:
                                inter_bursts_distribution.append(dist_within)

                    else:
                        print('AnalyseBurstsIntervals: outside_in and outside_out of different lengths ',
                              file=sys.stderr)
                        sys.exit()

                # print("debug")

    print(f'mean {np.mean(inter_bursts_distribution)}')
    print(f'std {np.std(inter_bursts_distribution)}')
    plot_hist(inter_bursts_distribution, bins=50, title="Interbursts distances distrib", x_label="distance",
              y_label="count")
    print("COMPLETED marking outliners for trials")


initialization = InitDataSet(levels=['deep', 'medium', 'light'])
doas = initialization.get_dataset_as_doas()
analyse_interburst_intervals(doas)
