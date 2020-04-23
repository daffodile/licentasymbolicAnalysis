from pylab import *


def mark_burst_basic_thresholds(doas, all_thresholds: dict):
    for doa in doas:
        for channel in doa.channels:
            ths = all_thresholds[f'{channel.number}']
            for trial in channel.trials:
                # ddf = np.where(array < =-16 or array > 16, 1, 0)
                values_1 = np.array(trial.spontaneous.values)
                values_outsiders_1 = np.where(values_1 < ths[0], 1,
                                              (np.where(values_1 > ths[1], 1, 0)))

                trial.spontaneous.set_values_outsiders(values_outsiders_1)

                values_2 = np.array(trial.stimulus.values)
                values_outsiders_2 = np.where(values_2 < ths[0], 1,
                                              (np.where(values_2 > ths[1], 1, 0)))

                trial.stimulus.set_values_outsiders(values_outsiders_2)

                values_3 = np.array(trial.poststimulus.values)
                values_outsiders_3 = np.where(values_3 < ths[0], 1,
                                              (np.where(values_3 > ths[1], 1, 0)))
                trial.poststimulus.set_values_outsiders(values_outsiders_3)


def unify_interbursts(doas, max_interbursts_dist):
    for doa in doas:
        for channel in doa.channels:
            for trial in channel.trials:

                burst_detection_flag = False
                burst_detection_flag = (1 in trial.spontaneous.values_outsiders) or (
                        1 in trial.stimulus.values_outsiders) or (1 in trial.poststimulus.values_outsiders)

                if burst_detection_flag:
                    trial_values = []
                    trial_values_outsiders = []

                    trial_values.extend(trial.spontaneous.values)
                    trial_values_outsiders.extend(trial.spontaneous.values_outsiders)

                    stimulus_start = len(trial.spontaneous.values)
                    trial_values.extend(trial.stimulus.values)
                    trial_values_outsiders.extend(trial.stimulus.values_outsiders)

                    poststimulus_start = len(trial_values)
                    trial_values.extend(trial.poststimulus.values)
                    trial_values_outsiders.extend(trial.poststimulus.values_outsiders)

                    # outside = zone with burst
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
                            index_start = outside_out[ind_tuple][0]  # an outsiders zone ends here
                            index_end = outside_in[ind_tuple + 1][0]  # next outsider zone begins at outside_in[i+1]
                            dist_within_bursts = index_end - index_start

                            # unify only for inter bursts region of length less than max_interbursts_dist
                            if dist_within_bursts < max_interbursts_dist and dist_within_bursts is not 0:
                                for i in range(index_start, index_end):
                                    trial_values_outsiders[i] = 1

                        trial.spontaneous.set_values_outsiders(trial_values_outsiders[0:stimulus_start])
                        trial.stimulus.set_values_outsiders(trial_values_outsiders[stimulus_start:poststimulus_start])
                        trial.poststimulus.set_values_outsiders(trial_values_outsiders[poststimulus_start:])

                    else:
                        print('AnalyseBurstsIntervals: outside_in and outside_out of different lengths ',
                              file=sys.stderr)
                        sys.exit()


def extend_margins_inter_bursts(doas, percent_margins=0.1):
    '''
    :param doas: full dataset for whicht the bursts are already marked
    :param percent_margins: how much to extend those regions on the left and on the right
    :return:
    '''
    # if(percent_margins<=0.0 or percent_margins>=1.0):

    for doa in doas:
        for channel in doa.channels:
            for trial in channel.trials:

                burst_detection_flag = False

                burst_detection_flag = (1 in trial.spontaneous.values_outsiders) or (
                        1 in trial.stimulus.values_outsiders) or (1 in trial.poststimulus.values_outsiders)

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

                    # entering in bursting zone
                    outside_in = []
                    # exiting the bursting zone
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
                        for ind_tuple in range(len(outside_in)):
                            # get the beginning and ending of the bursts zone
                            index_start = outside_in[ind_tuple][0]
                            index_end = outside_out[ind_tuple][0]

                            bursting_distance = index_end - index_start

                            if bursting_distance is not 0 and bursting_distance > 10:

                                # determine how much to add on each margin
                                extra_distance = int(percent_margins * bursting_distance)

                                # add the extra distance at the begining
                                index_start -= extra_distance
                                if index_start < 0:
                                    index_start = 0
                                # add the extra disance at the end
                                index_end += extra_distance
                                if index_end >= len(trial_values):
                                    index_end = len(trial_values) - 1

                                for i in range(index_start, index_end):
                                    trial_values_outsiders[i] = 1

                        trial.spontaneous.set_values_outsiders(trial_values_outsiders[0:stimulus_start])
                        trial.stimulus.set_values_outsiders(
                            trial_values_outsiders[stimulus_start:poststimulus_start])
                        trial.poststimulus.set_values_outsiders(trial_values_outsiders[poststimulus_start:])

                    else:
                        print('AnalyseBurstsIntervals: outside_in and outside_out of different lengths ',
                              file=sys.stderr)
                        sys.exit()


thresholds_2 = {'2': [-29.16208267211914, 29.830608367919922], '3': [-28.065452575683594, 28.921966552734375],
                '4': [-34.38615417480469, 35.25702667236328], '5': [-28.023412704467773, 28.899110794067383],
                '6': [-29.32749366760254, 30.000972747802734], '7': [-28.051198959350586, 28.920198440551758],
                '8': [-34.79737091064453, 35.684852600097656], '9': [-36.712547302246094, 37.74555969238281],
                '10': [-28.37700843811035, 29.177644729614258], '11': [-28.5379695892334, 29.334697723388672],
                '12': [-28.06175422668457, 28.84296226501465], '13': [-27.38531494140625, 28.172622680664062],
                '14': [-34.50564956665039, 35.53166580200195], '15': [-29.73434829711914, 30.73203468322754],
                '16': [-37.593997955322266, 38.8660888671875], '17': [-31.5568790435791, 32.030128479003906],
                '18': [-40.99643325805664, 41.98263168334961], '19': [-31.922082901000977, 32.28758239746094],
                '20': [-26.776390075683594, 26.731401443481445], '21': [-32.09612274169922, 32.387062072753906],
                '23': [-32.520633697509766, 32.84562683105469], '24': [-32.79780197143555, 33.1236572265625],
                '25': [-32.26771926879883, 32.728233337402344], '26': [-25.530717849731445, 25.960113525390625],
                '27': [-31.93470573425293, 32.3910026550293], '28': [-25.4182186126709, 25.843904495239258],
                '29': [-32.056251525878906, 32.51969909667969], '30': [-34.16683578491211, 34.915077209472656],
                '31': [-31.370412826538086, 31.845157623291016], '32': [-37.98116683959961, 38.829158782958984]}


def mark_bursts_regions(doas, thresholds=thresholds_2, max_interbursts_dist=709,
                        to_extend_margins=False,
                        percent_margins=0.1, hilbert=False):
    '''
    :param doas: dataset as doas
    :param thresholds: dictionary with threshold values for considering burst for each channel
    :param max_interbursts_dist: distances narrower that this are assimilated as bursts
    :param to_extend_margins: bool, if to extend the bursting zones to left and right
    :param percent_margins: if to_extend_margins is TRue, with what range to extend
    :return: no return type, is sets flags in dataset
    '''
    print('START marking bursting regions')
    # initial mark of the bursts based on passed threshold
    mark_burst_basic_thresholds(doas, thresholds)

    # extend the bursts at the inter bursts regions
    unify_interbursts(doas, max_interbursts_dist)

    # extend the bursts regions if it is the case
    if (to_extend_margins):
        extend_margins_inter_bursts(doas, percent_margins)

    print('COMPLETED marking bursting regions')
