import numpy as np
from pandas import DataFrame
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.svm import SVC

from classification.SplitData import SplitData
from classification.svm.Train_and_Test_TESPAR import *
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet

csv_file = "svm_inter_channel.csv"

# use these channels to train and to test the models
# train_channels = [1, 2, 5, 6, 14]  # channels with acc > 0,74    STIMULUS
# test_channels = [10, 16, 19, 24, 29]  # channels with acc < 0.68
train_channels = [1, 5, 6, 10, 13]  # channels with acc > 0,74    Spontaneous
test_channels = [16, 19, 20, 26, 29]  # channels with acc < 0.68
segment = 'stimulus'
segments = [segment]

# how many models to train for a pair
run_nr = 3

# create the DataFrame that will be added to .csv file-
column_names = ['channel train', 'channel test', 'segment', 'acc avr', 'acc std_dev', 'f1-sc avr', 'f1-sc std_dev']
df = DataFrame(columns=column_names)

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../../data_to_be_saved/alphabet_1_150hz.txt')

print('train and test on good channels')
for ch_train in train_channels:
    for ch_test in train_channels:
        print("start running for channels " + str(ch_train) + ' and ' + str(ch_test) + '\n')

        # SplitData(self, doas, channels, levels, segment, orientation):
        train_data = SplitData(doas, [ch_train], ['light', 'deep'], segments, ['all'])
        test_data = SplitData(doas, [ch_test], ['light', 'deep'], segments, ['all'])

        # save the accuracy and f1-score for all the run
        accuracies = []
        f1scores = []

        for run in range(run_nr):
            # train channel data
            X_train, x_test, y_train, y_test = split_2_channels(train_data, test_data, encoding, 0.2, run)

            model = SVC()
            model.fit(X_train, y_train)

            predictions = model.predict(x_test)
            report = classification_report(y_test, predictions, output_dict=True)

            acc = report['accuracy']
            f1sc = report['weighted avg']['f1-score']

            accuracies.append(acc)
            f1scores.append(f1sc)

        # calculate and write the mean  and std_dev of the average & f1-score
        # column_names = ['channel train', 'channel test', 'segment', 'acc avr', 'acc std_dev', 'f1-sc avr','f1-sc std_dev']
        df = df.append({'channel train': ch_train, 'channel test': ch_test, 'segment': segment,
                        'acc avr': np.mean(np.array(accuracies)), 'acc std_dev': np.std(np.array(accuracies)),
                        'f1-sc avr': np.mean(np.array(f1scores)), 'f1-sc std_dev': np.std(np.array(f1scores))},
                       ignore_index=True)
        print('debug')

df.to_csv(csv_file, mode='a', header=True)

# empty DataFrame to prepare it for this run
df = df.iloc[0:0]

print('train in good train_channels and test on bad')
for ch_train in train_channels:
    for ch_test in test_channels:
        print("start running for channels " + str(ch_train) + ' and ' + str(ch_test) + '\n')

        # SplitData(self, doas, channels, levels, segment, orientation):
        train_data = SplitData(doas, [ch_train], ['light', 'deep'], segments, ['all'])
        test_data = SplitData(doas, [ch_test], ['light', 'deep'], segments, ['all'])

        # save the accuracy and f1-score for all the run
        accuracies = []
        f1scores = []

        for run in range(run_nr):
            # train channel data
            X_train, x_test, y_train, y_test = split_2_channels(train_data, test_data, encoding, 0.2, run)

            model = SVC()
            model.fit(X_train, y_train)

            predictions = model.predict(x_test)
            report = classification_report(y_test, predictions, output_dict=True)

            acc = report['accuracy']
            f1sc = report['weighted avg']['f1-score']

            accuracies.append(acc)
            f1scores.append(f1sc)

        # calculate and write the mean  and std_dev of the average & f1-score
        # column_names = ['channel train', 'channel test', 'segment', 'acc avr', 'acc std_dev', 'f1-sc avr','f1-sc std_dev']
        df = df.append({'channel train': ch_train, 'channel test': ch_test, 'segment': segment,
                        'acc avr': np.mean(np.array(accuracies)), 'acc std_dev': np.std(np.array(accuracies)),
                        'f1-sc avr': np.mean(np.array(f1scores)), 'f1-sc std_dev': np.std(np.array(f1scores))},
                       ignore_index=True)

df.to_csv(csv_file, mode='a', header=False)

