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


thresholds_m014 = {'2': [-29.16208267211914, 29.830608367919922], '3': [-28.065452575683594, 28.921966552734375],
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

inter_bursts_m014 = 709

# thresholds_m016 = {'1': [-33.448509216308594, 33.67782211303711], '3': [-31.78066062927246, 32.354591369628906],
#                    '4': [-33.7597770690918, 34.57509231567383], '5': [-29.101037979125977, 29.538536071777344],
#                    '6': [-31.66200828552246, 32.05733871459961], '7': [-36.37326431274414, 35.907569885253906],
#                    '8': [-34.31382369995117, 34.79298400878906], '9': [-32.546085357666016, 32.921714782714844],
#                    '10': [-30.97686195373535, 31.548189163208008], '11': [-31.286720275878906, 31.75687026977539],
#                    '12': [-25.35161781311035, 25.605083465576172], '13': [-26.0643310546875, 26.101621627807617],
#                    '14': [-36.21009826660156, 36.85982894897461], '15': [-31.04300308227539, 31.034828186035156],
#                    '16': [-32.7509651184082, 33.21724319458008], '17': [-30.617645263671875, 30.9529972076416],
#                    '18': [-34.696929931640625, 35.1765251159668], '19': [-29.86421012878418, 30.23371696472168],
#                    '20': [-31.82549285888672, 32.13880920410156], '21': [-27.53139305114746, 27.762067794799805],
#                    '22': [-38.594818115234375, 39.108680725097656], '23': [-33.15806198120117, 33.412574768066406],
#                    '24': [-29.366539001464844, 29.562366485595703], '25': [-28.169172286987305, 28.062923431396484],
#                    '26': [-23.876577377319336, 24.04102325439453], '27': [-32.84303283691406, 33.144290924072266],
#                    '28': [-30.906526565551758, 31.318443298339844], '29': [-32.203800201416016, 32.6241455078125],
#                    '30': [-35.43271255493164, 36.15224075317383], '31': [-26.111417770385742, 26.030183792114258],
#                    '32': [-33.13913345336914, 33.61216354370117]}
#
# inter_bursts_m016 = 750


def mark_bursts_regions(doas, thresholds=thresholds_m014, max_interbursts_dist=inter_bursts_m014,
                        to_extend_margins=False,
                        percent_margins=0.1):
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
