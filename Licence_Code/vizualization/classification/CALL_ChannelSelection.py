import numpy as np

from input_reader.InitDataSet import InitDataSet
from vizualization.classification.Channels_Selection import compute_zscores, get_channels

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()

# dtc_file = '../../classification/results/dtc_30_averages.csv'
dtc_file = '../../classification/results/dtc_30_good_averages20.csv'
zscores_dtc = compute_zscores(dtc_file)

rfc_file = '../../classification/results/rf_30_averages.csv'
zscores_rfc = compute_zscores(rfc_file)

svm_file = '../../classification/results/svm_30_averages.csv'
zscores_svm = compute_zscores(svm_file)

avg_spontaneous = np.mean([zscores_dtc[0], zscores_rfc[0], zscores_svm[0]], axis=0)
avg_stimulus = np.mean([zscores_dtc[1], zscores_rfc[1], zscores_svm[1]], axis=0)
avg_poststimulus = np.mean([zscores_dtc[2], zscores_rfc[2], zscores_svm[2]], axis=0)

# GENERAL
# print("SPONTANEOUS")
# get_channels(doas, avg_spontaneous)
# print("STIMULUS")
# get_channels(doas, avg_stimulus)
# print("POSTSTIMULUS")
# get_channels(doas, avg_poststimulus)

print("------------------------------------------------------------------")

print("DTC")
print("SPONTANEOUS")
get_channels(doas, zscores_dtc[0])
print("STIMULUS")
get_channels(doas, zscores_dtc[1])
print("POSTSTIMULUS")
get_channels(doas, zscores_dtc[2])

print("------------------------------------------------------------------")

# print("RFC")
# print("SPONTANEOUS")
# get_channels(doas, zscores_rfc[0])
# print("STIMULUS")
# get_channels(doas, zscores_rfc[1])
# print("POSTSTIMULUS")
# get_channels(doas, zscores_rfc[2])

print("------------------------------------------------------------------")

# print("SVM")
# print("SPONTANEOUS")
# get_channels(doas, zscores_svm[0])
# print("STIMULUS")
# get_channels(doas, zscores_svm[1])
# print("POSTSTIMULUS")
# get_channels(doas, zscores_svm[2])
