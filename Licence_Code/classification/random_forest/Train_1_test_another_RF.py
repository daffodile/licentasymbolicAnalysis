import numpy as np
from pandas import DataFrame
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.ensemble import RandomForestClassifier

from classification.SplitData import SplitData
from classification.svm.Train_and_Test_TESPAR import splitData, obtain_features_labels
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet

csv_file = "rf_inter_channel.csv"

# use these channels to train and to test the models
train_channels = [5, 6, 7, 12, 14]

test_channels = [16, 19, 24, 26, 29]

# how many models to train for a pair
run_nr = 10

# create the DataFrame that will be added to .csv file-
column_names = ['channel train', 'channel test', 'segment', 'run', 'accuracy', 'acc avr', 'acc std_dev', 'f1-score',
                'f1-sc avr', 'f1-sc std_dev']

df = DataFrame(columns=column_names)
df.to_csv(csv_file, mode='a', header=True)

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../../data_to_be_saved/alphabet_1_150hz.txt')

# empty line in .csv
df = df.append({'channel train': '', 'channel test': '', 'segment': '', 'run': '',
                'accuracy': '', 'acc avr': '', 'acc std_dev': '', 'f1-score': '', 'f1-sc avr': '',
                'f1-sc std_dev': ''}, ignore_index=True)

# good channels and also test on good channels
for ch_train in train_channels:
    for ch_test in train_channels:
        print("start running for channels " + str(ch_train) + ' and ' + str(ch_test) + '\n')

        # SplitData(self, doas, channels, levels, segment, orientation):
        train_data = SplitData(doas, [ch_train], ['light', 'deep'], ["stimulus"], ['all'])
        test_data = SplitData(doas, [ch_test], ['light', 'deep'], ["stimulus"], ['all'])

        # save the accuracy and f1-score for all the run
        accuracies = []
        f1scores = []

        for run in range(run_nr):
            # train channel data
            X_train_1, x_test_1, y_train_1, y_test_1 = splitData(train_data, encoding, 0.2)
            # test channel data
            x_train_2, x_test_2, y_train_2, y_test_2 = splitData(test_data, encoding, 0.2)

            model = RandomForestClassifier(n_estimators=100)

            model.fit(X_train_1, y_train_1)

            if(ch_train == ch_test):
                predictions = model.predict(x_test_1)
                report = classification_report(y_test_1, predictions, output_dict=True)
            else:
                predictions = model.predict(x_test_2)
                report = classification_report(y_test_2, predictions, output_dict=True)

            acc = report['accuracy']
            f1sc = report['weighted avg']['f1-score']

            df = df.append({'channel train': ch_train, 'channel test': ch_test, 'segment': 'stimulus', 'run': run,
                            'accuracy': acc, 'acc avr': '', 'acc std_dev': '', 'f1-score': f1sc, 'f1-sc avr': '',
                            'f1-sc std_dev': ''}, ignore_index=True)
            accuracies.append(acc)
            f1scores.append(f1sc)
        # calculate and write the mean  and std_dev of the average & f1-score
        df = df.append({'channel train': '', 'channel test': '', 'segment': 'stimulus', 'run': '', 'accuracy': '',
                        'acc avr': np.mean(np.array(accuracies)), 'acc std_dev': np.std(np.array(accuracies)),
                        'f1-score': '', 'f1-sc avr': np.mean(np.array(f1scores)),
                        'f1-sc std_dev': np.std(np.array(f1scores))},
                       ignore_index=True)
        df.to_csv(csv_file, mode='a', header=False)
        # empty DataFrame to prepare it for this run
        df = df.iloc[0:0]

# good channels to train, bad to test
# empty line in .csv
df = df.append({'channel train': '', 'channel test': '', 'segment': '', 'run': '',
                'accuracy': '', 'acc avr': '', 'acc std_dev': '', 'f1-score': '', 'f1-sc avr': '',
                'f1-sc std_dev': ''}, ignore_index=True)

for ch_train in train_channels:
    for ch_test in test_channels:
        print("start running for channels " + str(ch_train) + ' and ' + str(ch_test) + '\n')

        # SplitData(self, doas, channels, levels, segment, orientation):
        train_data = SplitData(doas, [ch_train], ['light', 'deep'], ["stimulus"], ['all'])
        test_data = SplitData(doas, [ch_test], ['light', 'deep'], ["stimulus"], ['all'])

        # save the accuracy and f1-score for all the run
        accuracies = []
        f1scores = []

        for run in range(run_nr):
            # train channel data
            X_train_1, x_test_1, y_train_1, y_test_1 = splitData(train_data, encoding, 0.2)
            # test channel data
            x_train_2, x_test_2, y_train_2, y_test_2 = splitData(test_data, encoding, 0.2)

            model = RandomForestClassifier(n_estimators=100)

            model.fit(X_train_1, y_train_1)

            predictions = model.predict(x_test_2)
            report = classification_report(y_test_2, predictions, output_dict=True)

            acc = report['accuracy']
            f1sc = report['weighted avg']['f1-score']

            df = df.append({'channel train': ch_train, 'channel test': ch_test, 'segment': 'stimulus', 'run': run,
                            'accuracy': acc, 'acc avr': '', 'acc std_dev': '', 'f1-score': f1sc, 'f1-sc avr': '',
                            'f1-sc std_dev': ''}, ignore_index=True)

            accuracies.append(acc)
            f1scores.append(f1sc)

        # calculate and write the mean  and std_dev of the average & f1-score
        df = df.append({'channel train': '', 'channel test': '', 'segment': 'stimulus', 'run': '', 'accuracy': '',
                        'acc avr': np.mean(np.array(accuracies)), 'acc std_dev': np.std(np.array(accuracies)),
                        'f1-score': '', 'f1-sc avr': np.mean(np.array(f1scores)),
                        'f1-sc std_dev': np.std(np.array(f1scores))},
                       ignore_index=True)

        df.to_csv(csv_file, mode='a', header=False)
        # empty DataFrame to prepare it for this run
        df = df.iloc[0:0]

        # print('debug')
