import csv
from scipy import stats
import numpy as np


def compute_zscores(file_name):
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        accuracies = []
        ch = 0
        for row in csv_reader:
            if line_count == 0:
                print(file_name + ' was processed')
            else:
                accuracies.append(float(row[4]))
            line_count += 1
        zscores = []

        spontaneous_zscore = stats.zscore(accuracies[:30])
        zscores.append(spontaneous_zscore)

        stimulus_zscore = stats.zscore(accuracies[30:60])
        zscores.append(stimulus_zscore)

        poststimulus_zscore = stats.zscore(accuracies[60:90])
        zscores.append(poststimulus_zscore)

        return zscores


def convert_to_tuples_array(simple_array):
    tuples_array = []
    for i in range(len(simple_array)):
        tuples_array.append((i + 1, simple_array[i]))
    return tuples_array


def get_good_bad_channels(avg_array):
    tuples_array = convert_to_tuples_array(avg_array)
    sorted_array = sorted(tuples_array, key=lambda tup: tup[1], reverse=True)
    good_channels = sorted_array[:5]
    bad_channels = sorted_array[-5:]
    print('Good Channels' + str(good_channels))
    print('Bad Channels' + str(bad_channels))


dtc_file = '../../classification/results/dtc_30.csv'
zscores_dtc = compute_zscores(dtc_file)

rfc_file = '../../classification/results/rf_30.csv'
zscores_rfc = compute_zscores(rfc_file)

svm_file = '../../classification/results/svm_30.csv'
zscores_svm = compute_zscores(svm_file)

avg_spontaneous = np.mean([zscores_dtc[0], zscores_rfc[0], zscores_svm[0]], axis=0)
avg_stimulus = np.mean([zscores_dtc[1], zscores_rfc[1], zscores_svm[1]], axis=0)
avg_poststimulus = np.mean([zscores_dtc[2], zscores_rfc[2], zscores_svm[2]], axis=0)

# SPONTANEOUS
print("SPONTANEOUS")
get_good_bad_channels(avg_spontaneous)

# STIMULUS
print("STIMULUS")
get_good_bad_channels(avg_stimulus)

# POSTSTIMULUS
print("POSTSTIMULUS")
get_good_bad_channels(avg_poststimulus)
