import numpy as np

from input_reader.InitDataSet import InitDataSet
from vizualization.classification.Channels_Selection import compute_zscores, get_channels, get_good_bad_channels_indexes

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()

dtc_file = '../../classification/results/dtc_30_averages.csv'
zscores_dtc = compute_zscores(dtc_file)

rfc_file = '../../classification/results/rf_30_averages.csv'
zscores_rfc = compute_zscores(rfc_file)

svm_file = '../../classification/results/svm_30_averages.csv'
zscores_svm = compute_zscores(svm_file)

avg_spontaneous = np.mean([zscores_dtc[0], zscores_rfc[0], zscores_svm[0]], axis=0)
avg_stimulus = np.mean([zscores_dtc[1], zscores_rfc[1], zscores_svm[1]], axis=0)
avg_poststimulus = np.mean([zscores_dtc[2], zscores_rfc[2], zscores_svm[2]], axis=0)

# SPONTANEOUS
print("SPONTANEOUS")
spontaneous_indexes_good, spontaneous_indexes_bad = get_good_bad_channels_indexes(avg_spontaneous)
print("GOOD")
spontaneous_channels_good = get_channels(doas, spontaneous_indexes_good)
print("BAD")
spontaneous_channela_bad = get_channels(doas, spontaneous_indexes_bad)

print("------------------------------------------------------------------")

# STIMULUS
print("STIMULUS")
stimulus_indexes_good, stimulus_indexes_bad = get_good_bad_channels_indexes(avg_stimulus)
print("GOOD")
stimulus_channels_good = get_channels(doas, stimulus_indexes_good)
print("BAD")
stimulus_channels_bad = get_channels(doas, stimulus_indexes_bad)

print("------------------------------------------------------------------")

# POSTSTIMULUS
print("POSTSTIMULUS")
poststimulus_indexes_good, poststimulus_indexes_bad = get_good_bad_channels_indexes(avg_poststimulus)
print("GOOD")
poststimulus_channels_good = get_channels(doas, poststimulus_indexes_good)
print("BAD")
poststimulus_channels_bad = get_channels(doas, poststimulus_indexes_bad)

# # DTC
# # SPONTANEOUS
# print("DTC")
# print("SPONTANEOUS")
# get_good_bad_channels_indexes(zscores_dtc[0])
#
# # STIMULUS
# print("STIMULUS")
# get_good_bad_channels_indexes(zscores_dtc[1])
#
# # POSTSTIMULUS
# print("POSTSTIMULUS")
# get_good_bad_channels_indexes(zscores_dtc[2])
#
# # RFC
# # SPONTANEOUS
# print("RFC")
# print("SPONTANEOUS")
# get_good_bad_channels_indexes(zscores_rfc[0])
#
# # STIMULUS
# print("STIMULUS")
# get_good_bad_channels_indexes(zscores_rfc[1])
#
# # POSTSTIMULUS
# print("POSTSTIMULUS")
# get_good_bad_channels_indexes(zscores_rfc[2])
#
# # SVM
# # SPONTANEOUS
# print("SVM")
# print("SPONTANEOUS")
# get_good_bad_channels_indexes(zscores_svm[0])
#
# # STIMULUS
# print("STIMULUS")
# get_good_bad_channels_indexes(zscores_svm[1])
#
# # POSTSTIMULUS
# print("POSTSTIMULUS")
# get_good_bad_channels_indexes(zscores_svm[2])
