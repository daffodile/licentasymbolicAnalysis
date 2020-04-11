import numpy as np

from input_reader.InitDataSet import InitDataSet
from vizualization.classification.Channels_Selection import compute_zscores, get_channels, get_good_bad_channels_indexes

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()

svm_file = 'svm_30_averages.csv'
zscores_svm = compute_zscores(svm_file)

print("SVM")
print("SPONTANEOUS")
spontaneous_indexes_good, spontaneous_indexes_bad = get_good_bad_channels_indexes(zscores_svm[0])
print("GOOD")
spontaneous_channels_good = get_channels(doas, spontaneous_indexes_good)
print("BAD")
spontaneous_channels_bad = get_channels(doas, spontaneous_indexes_bad)

print("------------------------------------------------------------------")
# STIMULUS
print("STIMULUS")
stimulus_indexes_good, stimulus_indexes_bad = get_good_bad_channels_indexes(zscores_svm[1])
print("GOOD")
stimulus_channels_good = get_channels(doas, stimulus_indexes_good)
print("BAD")
stimulus_channels_bad = get_channels(doas, stimulus_indexes_bad)

print("------------------------------------------------------------------")

# POSTSTIMULUS
print("POSTSTIMULUS")
poststimulus_indexes_good, poststimulus_indexes_bad = get_good_bad_channels_indexes(zscores_svm[2])
print("GOOD")
poststimulus_channels_good = get_channels(doas, poststimulus_indexes_good)
print("BAD")
poststimulus_channels_bad = get_channels(doas, poststimulus_indexes_bad)
