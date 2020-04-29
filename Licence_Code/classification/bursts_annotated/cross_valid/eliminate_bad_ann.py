import os

import numpy as np
from pandas import DataFrame
from sklearn.model_selection import StratifiedKFold, cross_validate
from sklearn.svm import SVC

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import obtain_A_features_from_doa_with_bursts_flags, train_test_doa_balanced, \
    obtain_A_features_from_doa, obtain_features_labels_from_doa

csv_results = "remove_bursts_cross_avr.csv"

all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
                31, 32]
segments = ['spontaneous', 'stimulus']

# data frame that keeps avr and std of the runs
columns = ['channel', 'segment', 'acc avr', 'acc std_dev', 'f1-sc avr', 'f1-sc std_dev']
df_results = DataFrame(columns=columns)
df_results.to_csv(csv_results, mode='a', header=True)

data_dir = os.path.join('../..', '..')
initialization = InitDataSet(data_dir=data_dir, directory='no_bursts', trials_to_skip=[1, 2])
doas = initialization.get_dataset_as_doas()

for doa in doas:
    print(f'doa level {doa.level} {len(doa.channels[0].trials)} trials')

encoding = Encoding('./../../../data_to_be_saved/alphabet_3.txt')

for ind_segment, segment in enumerate(segments):
    for chn_ind, channel in enumerate(all_channels):
        print("start running for channel " + str(channel) + ' ' + segment + '\n')

        X, y = obtain_A_features_from_doa(doas, channel, encoding, segments=[segment])

        model = SVC(gamma="auto")

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
        print('debug')

df_results.to_csv(csv_results, mode='a', header=False)
