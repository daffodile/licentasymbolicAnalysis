import os

import numpy as np
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.svm import SVC

from feature_extraction.FFT.FFTFeatures import obtain_FFT_features_labels
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.ExtractData import ExtractData
from utils.mark_bursts.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions

csv_results = "rf_3_levels_FFT_NO_burst.csv"

# data frame that keeps avr and std of the runs
columns = ['channel', 'segment', 'acc avr', 'acc std_dev', 'f1-sc avr', 'f1-sc std_dev']
df_results = DataFrame(columns=columns)
df_results.to_csv(csv_results, mode='a', header=True)

segments = ['spontaneous', 'stimulus', 'poststimulus']
all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
                31, 32]

encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')

data_dir = os.path.join('../..', '..')

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
mark_bursts_regions(doas)

for segment in segments:
    for channel in all_channels:
        print("start running for channel " + str(channel) + ' ' + segment)
        data = ExtractData(doas, [channel], ['light', 'medium', 'deep'], [segment], ['all'])
        X, y = obtain_FFT_features_labels(data)

        model = RandomForestClassifier(n_estimators=5000, max_depth=5, min_samples_split=5, min_samples_leaf=10)

        skf = StratifiedKFold(n_splits=10)

        skf.get_n_splits(X, y)

        results = cross_validate(model, X, y, scoring=['accuracy', 'f1_weighted'], cv=skf)

        accuracy = results['test_accuracy']
        f1score = results['test_f1_weighted']

        print("Accuracy of Model with Cross Validation is:", accuracy.mean() * 100)

        df_results = df_results.append({'channel': channel, 'segment': segment, 'acc avr': np.mean(np.array(accuracy)),
                                        'acc std_dev': np.std(np.array(accuracy)),
                                        'f1-sc avr': np.mean(np.array(accuracy)),
                                        'f1-sc std_dev': np.std(np.array(f1score))}, ignore_index=True)

df_results.to_csv(csv_results, mode='a', header=False)
