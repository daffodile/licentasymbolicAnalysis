'''
    script for running the inter channel classification

    select the classifier

    select the csv where results will be saved

    set the train and test channels
'''

csv_results = "svm_inter_channels.csv"

import numpy as np
from pandas import DataFrame
from sklearn.svm import SVC

from sklearn.metrics import classification_report

from classification.SplitData import SplitData
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import train_test_doa, obtain_features_labels

# data frame that keeps avr and std of the runs
columns = ['ch train', 'ch test', 'segment', 'acc avr', 'acc std_dev', 'f1-sc avr', 'f1-sc std_dev']
df_results = DataFrame(columns=columns)
df_results.to_csv(csv_results, mode='a', header=True)

train_channels = [1, 5, 7, 12, 14]  # good over all
test_channels = [16, 19, 20, 27, 29]  # bad over all

segment = 'spontaneous'

# how many models to train a for a channel-segment pair
run_nr = 10

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../../data_to_be_saved/alphabet_1_150hz.txt')

############################## train on good channel, test on good chnannel ###############################3
accuracies = [[[] for i in range(len(train_channels))] for j in range(len(train_channels))]
f1scores = [[[] for i in range(len(train_channels))] for j in range(len(train_channels))]

for run in range(run_nr):
    # firstly split the input into train test
    doas_train, doas_test, ind_test = train_test_doa(doas, 0.2)

    for ind_train, ch_train in enumerate(train_channels):
        for ind_test, ch_test in enumerate(train_channels):
            print("start running for channel " + str(ch_train) + ' and ' + str(ch_test) + ' ' + segment + '\n')

            # SplitData(self, doas, channels, levels, segment, orientation):
            train_data = SplitData(doas_train, [ch_train], ['light', 'deep'], [segment], ['all'])
            test_data = SplitData(doas_test, [ch_test], ['light', 'deep'], [segment], ['all'])

            X_train, y_train = obtain_features_labels(train_data, encoding)
            x_test, y_test = obtain_features_labels(test_data, encoding)

            model = SVC(gamma="auto")

            model.fit(X_train, y_train)
            predictions = model.predict(x_test)

            report = classification_report(y_test, predictions, output_dict=True)

            acc = report['accuracy']
            f1sc = report['weighted avg']['f1-score']
            accuracies[ind_train][ind_test].append(acc)
            f1scores[ind_train][ind_test].append(f1sc)

for ind_train, ch_train in enumerate(train_channels):
    for ind_test, ch_test in enumerate(train_channels):
        acc_avr = np.mean(np.array(accuracies[ind_train][ind_test]))
        acc_std = np.std(np.array(accuracies[ind_train][ind_test]))

        f1_avr = np.mean(np.array(f1scores[ind_train][ind_test]))
        f1_std = np.std(np.array(f1scores[ind_train][ind_test]))
        df_results = df_results.append(
            {'ch train': ch_train, 'ch test': ch_test, 'segment': segment, 'acc avr': acc_avr,
             'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
            ignore_index=True)

df_results.to_csv(csv_results, mode='a', header=False)

# empty DataFrame to prepare it for next run
df_results = df_results.iloc[0:0]

############################## train on good channel, test on good chnannel ###############################3
accuracies = [[[] for i in range(len(test_channels))] for j in range(len(train_channels))]
f1scores = [[[] for i in range(len(test_channels))] for j in range(len(train_channels))]

for run in range(run_nr):
    print('run  ' + str(run))
    # firstly split the input into train test
    doas_train, doas_test, ind_test = train_test_doa(doas, 0.2)

    for ind_train, ch_train in enumerate(train_channels):
        for ind_test, ch_test in enumerate(test_channels):
            print("start running for channel " + str(ch_train) + ' and ' + str(ch_test) + ' ' + segment + '\n')

            # SplitData(self, doas, channels, levels, segment, orientation):
            train_data = SplitData(doas_train, [ch_train], ['light', 'deep'], [segment], ['all'])
            test_data = SplitData(doas_test, [ch_test], ['light', 'deep'], [segment], ['all'])

            X_train, y_train = obtain_features_labels(train_data, encoding)
            x_test, y_test = obtain_features_labels(test_data, encoding)

            model = SVC(gamma="auto")

            model.fit(X_train, y_train)
            predictions = model.predict(x_test)

            report = classification_report(y_test, predictions, output_dict=True)

            acc = report['accuracy']
            f1sc = report['weighted avg']['f1-score']
            accuracies[ind_train][ind_test].append(acc)
            f1scores[ind_train][ind_test].append(f1sc)

for ind_train, ch_train in enumerate(train_channels):
    for ind_test, ch_test in enumerate(test_channels):
        acc_avr = np.mean(np.array(accuracies[ind_train][ind_test]))
        acc_std = np.std(np.array(accuracies[ind_train][ind_test]))

        f1_avr = np.mean(np.array(f1scores[ind_train][ind_test]))
        f1_std = np.std(np.array(f1scores[ind_train][ind_test]))
        df_results = df_results.append(
            {'ch train': ch_train, 'ch test': ch_test, 'segment': segment, 'acc avr': acc_avr,
             'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
            ignore_index=True)

df_results.to_csv(csv_results, mode='a', header=False)
