import sys
import numpy as np
from matplotlib.pyplot import boxplot


def mark_outsiders(doas, liberty=2, max_interbursts_dist=500):
    """
    function to mark the values that ore outside interval
          [ mean - liberty*std_dev,  mean + liberty*std_dev]
    on each channel in each DOA

    :param doas: array of DOAs to mark
    :param liberty: coeff for multiplying with std_dev on a channel
    :param max_interbursts_dist: limit distance where considering to unify consecutive bursting regions
    :return: modify doas in situ, no return type
    """
    print("START marking outliners of trials")
    for doa in doas:
        for channel in doa.channels:
            all_trials = []
            for trial in channel.trials:
                all_trials.extend(trial.spontaneous.values)
                all_trials.extend(trial.stimulus.values)
                all_trials.extend(trial.poststimulus.values)

            channel.mean = np.mean(all_trials)
            channel.std_der = np.std(all_trials)

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

                if burst_detection_flag:
                    trial_values = []
                    trial_values.extend(trial.spontaneous.values)
                    stimulus_start = len(trial.spontaneous.values)
                    trial_values.extend(trial.stimulus.values)
                    poststimulus_start = len(trial_values)
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
                            # unify only for inter bursts region of length less than max_interbursts_dist
                            if dist_within < max_interbursts_dist and dist_within is not 0:
                                #  update inter bursts segment to also be marked as burst
                                if index_start < stimulus_start:
                                    # inter burst zone begins and ends in spontaneous part
                                    if index_end < stimulus_start:
                                        for i in range(index_start, index_end):
                                            trial.spontaneous.values_outsiders[i] = 1  # mark as outsider too
                                    else:
                                        # inter bursting zone overlaps with the pass between segments
                                        for i in range(index_start, stimulus_start - 1):
                                            trial.spontaneous.values_outsiders[i] = 1
                                        for j in range(0, index_end - stimulus_start):
                                            trial.stimulus.values_outsiders[j] = 1
                                else:
                                    if index_start < poststimulus_start:
                                        # starts and also ends in spontaneous part
                                        if index_end < poststimulus_start:
                                            for i in range(index_start - stimulus_start,
                                                           index_end - stimulus_start):
                                                trial.stimulus.values_outsiders[i] = 1
                                        else:
                                            # burst zone overlaps with the pass between  segments
                                            for i in range(index_start - stimulus_start,
                                                           poststimulus_start - stimulus_start - 1):
                                                trial.stimulus.values_outsiders[i] = 1
                                            for j in range(0, index_end - poststimulus_start):
                                                trial.poststimulus.values_outsiders[j] = 1
                                    else:
                                        # inter burst zone in
                                        for j in range(index_start - poststimulus_start,
                                                       index_end - poststimulus_start):
                                            trial.poststimulus.values_outsiders[j] = 1
                    else:
                        print('AnalyseBurstsIntervals: outside_in and outside_out of different lengths ',
                              file=sys.stderr)
                        sys.exit()
        print(f'DONE FOR DOA {doa.level}')

    print("COMPLETED marking outline regions for trials")


def mark_outsiders_boxplot(doas, max_interbursts_dist=500):
    """
    function to mark the values that ore outside interval
          [ mean - liberty*std_dev,  mean + liberty*std_dev]
    on each channel in each DOA
    :param doas: array of DOAs to mark
    :param liberty: coeff for multiplying with std_dev on a channel
    :param max_interbursts_dist: limit distance where considering to unify consecutive bursting regions
    :return: modify doas in situ, no return type
    """
    print("START marking outliners of trials")

    all_values_full = []

    for doa in doas:
        for channel in doa.channels:
            # all_trials = []
            for trial in channel.trials:

                all_values_full.extend(trial.spontaneous.values)
                all_values_full.extend(trial.stimulus.values)

    r = boxplot(x=all_values_full)

    # from boxplot get the outliers from above and bellow it
    top_points = r["fliers"][0].get_data()[1]
    aboslute_values = np.abs(top_points)

    threshold = np.amin(aboslute_values)
    print(f"min fliers {threshold}")

    for doa in doas:
        for channel in doa.channels:
            for trial in channel.trials:

                burst_detection_flag = False

                values_outsiders_1 = np.where(np.abs(trial.spontaneous.values) < threshold, 0, 1)
                trial.spontaneous.set_values_outsiders(values_outsiders_1)

                values_outsiders_2 = np.where(np.abs(trial.stimulus.values) < threshold, 0, 1)
                trial.stimulus.set_values_outsiders(values_outsiders_2)

                values_outsiders_3 = np.where(np.abs(trial.poststimulus.values) < threshold, 0, 1)
                trial.poststimulus.set_values_outsiders(values_outsiders_3)

                burst_detection_flag = (1 in values_outsiders_1) or (1 in values_outsiders_2) or (
                        1 in values_outsiders_3)

                if burst_detection_flag:
                    trial_values = []
                    trial_values.extend(trial.spontaneous.values)
                    stimulus_start = len(trial.spontaneous.values)
                    trial_values.extend(trial.stimulus.values)
                    poststimulus_start = len(trial_values)
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
                            # unify only for inter bursts region of length less than max_interbursts_dist
                            if dist_within < max_interbursts_dist and dist_within is not 0:
                                #  update inter bursts segment to also be marked as burst
                                if index_start < stimulus_start:
                                    # inter burst zone begins and ends in spontaneous part
                                    if index_end < stimulus_start:
                                        for i in range(index_start, index_end):
                                            trial.spontaneous.values_outsiders[i] = 1  # mark as outsider too
                                    else:
                                        # inter bursting zone overlaps with the pass between segments
                                        for i in range(index_start, stimulus_start - 1):
                                            trial.spontaneous.values_outsiders[i] = 1
                                        for j in range(0, index_end - stimulus_start):
                                            trial.stimulus.values_outsiders[j] = 1
                                else:
                                    if index_start < poststimulus_start:
                                        # starts and also ends in spontaneous part
                                        if index_end < poststimulus_start:
                                            for i in range(index_start - stimulus_start,
                                                           index_end - stimulus_start):
                                                trial.stimulus.values_outsiders[i] = 1
                                        else:
                                            # burst zone overlaps with the pass between  segments
                                            for i in range(index_start - stimulus_start,
                                                           poststimulus_start - stimulus_start - 1):
                                                trial.stimulus.values_outsiders[i] = 1
                                            for j in range(0, index_end - poststimulus_start):
                                                trial.poststimulus.values_outsiders[j] = 1
                                    else:
                                        # inter burst zone in
                                        for j in range(index_start - poststimulus_start,
                                                       index_end - poststimulus_start):
                                            trial.poststimulus.values_outsiders[j] = 1
                    else:
                        print('AnalyseBurstsIntervals: outside_in and outside_out of different lengths ',
                              file=sys.stderr)
                        sys.exit()

    print("COMPLETED marking outline regions for trials")
