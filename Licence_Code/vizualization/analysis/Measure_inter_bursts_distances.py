import os

from input_reader.InitDataSetWithBurstsFlags import InitDataSetWithBurstsFlags
import numpy as np


# def mak_burst_basic(doas, threshold):
#     for doa in doas:
#         for channel in doa.channels:
#             for trial in channel.trials:
#                 values_outsiders_1 = np.where(np.abs(trial.spontaneous.values) < threshold, 0, 1)
#                 trial.spontaneous.set_values_outsiders(values_outsiders_1)
#                 values_outsiders_2 = np.where(np.abs(trial.stimulus.values) < threshold, 0, 1)
#                 trial.stimulus.set_values_outsiders(values_outsiders_2)
#                 values_outsiders_3 = np.where(np.abs(trial.poststimulus.values) < threshold, 0, 1)
#                 trial.poststimulus.set_values_outsiders(values_outsiders_3)
#


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


data_dir = os.path.join('..', '..')
initialization = InitDataSetWithBurstsFlags(data_dir, levels=['deep', 'medium', 'light'])
doas = initialization.get_dataset_as_doas()

# thresholds = {2: 23.263285, 3: 22.366724, 4: 27.422037, 5: 22.331213, 6: 23.394754, 7: 22.354338, 8: 27.749441, 9: 29.266874, 10: 22.621815, 11: 22.75086, 12: 22.371376, 13: 21.829714, 14: 27.50188, 15: 23.687954, 16: 29.949093, 17: 25.198391, 18: 32.699684, 19: 25.501558, 20: 21.380661, 21: 25.648182, 23: 25.984198, 24: 26.205786, 25: 25.768787, 26: 20.381828, 27: 25.502258, 28: 20.292067, 29: 25.598713, 30: 27.259365, 31: 25.049229, 32: 30.300776}

# 1,75  quantile=601.0 for q = 0.95
thresholds_175 = {'2': [-26.212846755981445, 26.881168365478516], '3': [-25.215452194213867, 26.072696685791016],
                  '4': [-30.9038143157959, 31.774932861328125], '5': [-25.17731475830078, 26.05272102355957],
                  '6': [-26.361085891723633, 27.034509658813477], '7': [-25.202640533447266, 26.071456909179688],
                  '8': [-31.2733097076416, 32.16081619262695], '9': [-32.98964309692383, 34.0227165222168],
                  '10': [-25.499446868896484, 26.299909591674805], '11': [-25.644441604614258, 26.44139289855957],
                  '12': [-25.216604232788086, 25.997833251953125], '13': [-24.607534408569336, 25.39472198486328],
                  '14': [-31.00367546081543, 32.03046417236328], '15': [-26.711227416992188, 27.708641052246094],
                  '16': [-33.771724700927734, 35.04311752319336], '17': [-28.37746238708496, 28.851322174072266],
                  '18': [-36.84759521484375, 37.8336296081543], '19': [-28.71183204650879, 29.077007293701172],
                  '20': [-24.10072898864746, 24.055879592895508], '21': [-28.872180938720703, 29.162824630737305],
                  '23': [-29.252010345458984, 29.577116012573242], '24': [-29.501731872558594, 29.827238082885742],
                  '25': [-29.01862144470215, 29.47837257385254], '26': [-22.955995559692383, 23.385568618774414],
                  '27': [-28.718482971191406, 29.174833297729492], '28': [-22.854778289794922, 23.280752182006836],
                  '29': [-28.826929092407227, 29.291156768798828], '30': [-30.71279525756836, 31.460893630981445],
                  '31': [-28.2097110748291, 28.684202194213867], '32': [-34.140865325927734, 34.98889923095703]}

# 2   quantile=709.0 for q = 0.95
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

mark_burst_basic_thresholds(doas, thresholds_2)
print('burstst are marked')
see_procents_distances(doas)

''' deep 185, medium 132, light 90
deep in a channel there are 185 trials left
[1, 2, 3, 4, 7, 8, 9, 10, 11, 14, 19, 22, 23, 25, 29, 30, 31, 32, 34, 36, 38, 41, 42, 43, 44, 45, 46, 47, 48, 50, 52, 53, 54, 55, 60, 63, 64, 67, 70, 71, 73, 76, 79, 83, 84, 87, 91, 92, 94, 95, 96, 99, 102, 104, 110, 111, 112, 117, 118, 119, 120, 122, 123, 124, 125, 126, 127, 128, 129, 131, 132, 133, 134, 135, 136, 137, 138, 143, 145, 147, 148, 149, 150, 152, 153, 154, 162, 165, 166, 168, 170, 172, 173, 175, 178, 183, 189, 191, 194, 199, 215, 219, 220, 226, 228, 230, 234, 240]
medium in a channel there are 132 trials left
[2, 4, 8, 9, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34, 35, 37, 38, 39, 40, 41, 42, 43, 45, 46, 48, 49, 50, 51, 52, 54, 56, 58, 59, 60, 62, 76, 81, 86, 88, 89, 90, 92, 93, 95, 96, 98, 99, 101, 102, 103, 104, 105, 106, 108, 111, 112, 113, 115, 116, 117, 118, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 140, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 155, 156, 157, 158, 160, 162, 164, 165, 166, 167, 168, 169, 171, 172, 173, 175, 176, 177, 178, 181, 192, 194, 195, 198, 199, 201, 202, 204, 205, 206, 207, 209, 210, 211, 212, 215, 219, 225, 228, 229, 232, 234, 235, 238, 239, 240]
light in a channel there are 90 trials left
'''

'''
2 0.33
[6, 7, 14, 20, 22, 24, 25, 29, 35, 39, 42, 45, 73, 80, 100, 102, 103, 104, 105, 107, 108, 110, 113, 114, 124, 130, 137, 147, 149, 157, 162, 166, 195, 196, 220, 221, 222, 224, 227, 228, 230, 232, 235, 236, 239]
deep in a channel there are 195 trials left
[1, 2, 3, 4, 7, 9, 10, 11, 13, 14, 19, 22, 25, 31, 32, 34, 36, 41, 43, 44, 45, 46, 47, 50, 52, 53, 54, 55, 60, 63, 67, 70, 73, 76, 83, 84, 87, 91, 92, 94, 95, 96, 99, 102, 104, 111, 112, 117, 118, 119, 120, 122, 123, 125, 126, 127, 128, 129, 131, 132, 133, 134, 135, 136, 137, 138, 145, 147, 148, 149, 150, 152, 153, 154, 162, 165, 168, 170, 172, 173, 175, 178, 183, 189, 191, 194, 199, 215, 220, 226, 228, 230, 234, 240]
medium in a channel there are 146 trials left
[4, 8, 9, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 34, 35, 37, 38, 39, 40, 41, 42, 43, 45, 46, 48, 49, 50, 51, 52, 54, 56, 58, 59, 60, 62, 76, 81, 86, 92, 93, 95, 96, 98, 99, 102, 103, 104, 106, 111, 112, 113, 116, 117, 118, 121, 122, 123, 124, 125, 126, 127, 128, 129, 130, 131, 132, 133, 134, 135, 136, 137, 138, 140, 143, 144, 145, 146, 147, 148, 149, 150, 151, 152, 153, 155, 156, 157, 158, 160, 162, 164, 165, 166, 167, 168, 169, 171, 172, 173, 175, 176, 177, 178, 181, 192, 198, 199, 201, 204, 205, 206, 207, 209, 211, 212, 215, 219, 225, 228, 229, 232, 234, 235, 238, 239]
light in a channel there are 105 trials left

2 0.5 deep 220, medium 195, light 168
[22, 42, 73, 80, 102, 103, 104, 105, 114, 124, 137, 149, 162, 220, 221, 222, 224, 228, 230, 236]
deep in a channel there are 220 trials left
[2, 4, 11, 19, 22, 25, 31, 32, 46, 47, 63, 67, 76, 91, 92, 94, 95, 96, 102, 111, 117, 118, 119, 120, 122, 127, 131, 132, 133, 136, 137, 138, 148, 152, 165, 168, 175, 178, 189, 199, 215, 220, 228, 230, 240]
medium in a channel there are 195 trials left
[4, 9, 13, 15, 17, 19, 20, 21, 23, 24, 26, 31, 35, 37, 41, 43, 45, 48, 49, 62, 76, 92, 93, 96, 99, 103, 106, 111, 112, 113, 118, 123, 125, 127, 131, 132, 133, 134, 135, 136, 137, 138, 140, 143, 145, 149, 151, 152, 155, 158, 160, 162, 164, 165, 168, 171, 172, 175, 177, 178, 181, 192, 198, 199, 204, 206, 219, 228, 232, 234, 238, 239]
light in a channel there are 168 trials left
'''