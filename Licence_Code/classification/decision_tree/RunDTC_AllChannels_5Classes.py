import os
import numpy as np
from pandas import DataFrame
from sklearn.metrics import classification_report, confusion_matrix

from sklearn.tree import DecisionTreeClassifier

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import train_test_doa_remake_balanced, obtain_features_labels
from utils.ExtractData import ExtractData

csv_file = "dtc_5classes_all_hp.csv"
csv_results = "dtc_5classes_all_avr_hp.csv"

classification_reports = "classification_reports_dtc_5classes_hp.txt"
output_classification_reports = open(classification_reports, 'w')

confusion_file = 'confusion_matrix_5classes_hp.txt'
output_confusion_matrix = open(confusion_file, 'w')

output_classification_reports.write("Classify all 5 levels: higpass10 and without marking bursts\n")
output_classification_reports.write("spon_stim concatenate A matrix 32 symbols\n")
output_classification_reports.write("train_test_doa_remake_balanced 80% for train \n")

run_nr = 10

all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
                31, 32]

segments = ['spontaneous', 'stimulus']

# data frame that keeps all runs for all channels, that will be added to .csv file
column_names = ['channel', 'segment', 'accuracy', 'f1-score']
df_all = DataFrame(columns=column_names)
df_all.to_csv(csv_file, mode='a', header=True)

encoding = Encoding('./../../data_to_be_saved/m014_highpass_alphabet_5.txt')
# encoding = Encoding('./../../data_to_be_saved/m014_classic_alphabet_3.txt')

data_dir = os.path.join('..', '..')

levels = ['light1', 'deep2', 'medium3', 'light4', 'medium5']

# def __init__(self, current_directory, subject_directory, filtering_directory, levels=['deep', 'medium', 'light'], trials_to_skip=None):
initialization = InitDataSet(current_directory=data_dir, subject_directory="m014", filtering_directory="highpass10",
                             levels=levels)
doas = initialization.get_dataset_as_doas()

accuracies = [[] for i in range(len(all_channels))]
f1scores = [[] for i in range(len(all_channels))]

for run in range(run_nr):
    print('************************RUN ' + str(run) + '************************')
    # firstly split the input into train test
    doas_train, doas_test = train_test_doa_remake_balanced(doas)

    for ind_channel, channel in enumerate(all_channels):
        print("start running for channel " + str(channel))
        output_classification_reports.write(f'####### run {run} channel {channel} #########\n')

        # SplitData(self, doas, channels, levels, segment, orientation):
        train_data = ExtractData(doas_train, [all_channels[ind_channel]], levels, segments,
                                 ['all'])
        test_data = ExtractData(doas_test, [all_channels[ind_channel]], levels, segments, ['all'])

        X_train, y_train = obtain_features_labels(train_data, encoding)
        x_test, y_test = obtain_features_labels(test_data, encoding)

        model = DecisionTreeClassifier(random_state=99, criterion='gini', max_depth=2)

        model.fit(X_train, y_train)

        # just for overfitting
        report_train = classification_report(y_train, model.predict(X_train), output_dict=True)
        acc_train = report_train['accuracy']
        print(f'predict on train  acc {acc_train}')

        predictions = model.predict(x_test)

        report = classification_report(y_test, predictions, output_dict=True)

        print(classification_report(y_test, predictions))
        print(confusion_matrix(y_test, predictions))

        output_classification_reports.write(classification_report(y_test, predictions))
        output_classification_reports.write('\n')

        output_confusion_matrix.write(f'{run} {channel} \n')
        np.savetxt(output_confusion_matrix, np.array(confusion_matrix(y_test, predictions)), fmt="%s", newline=' ')
        output_confusion_matrix.write('\n')

        acc = report['accuracy']
        f1sc = report['weighted avg']['f1-score']
        accuracies[ind_channel].append(acc)
        f1scores[ind_channel].append(f1sc)

        # calculate and write the mean  and std_dev of the average & f1-score
        df_all = df_all.append(
            {'channel': channel, 'segment': segments[0] + '+' + segments[1],  'accuracy': acc, 'f1-score': f1sc}, ignore_index=True)

        # print('debug')
    df_all.to_csv(csv_file, mode='a', header=False)
    df_all = df_all.iloc[0:0]

output_classification_reports.close()
output_confusion_matrix.close()

# data frame that keeps avr and std of the runs
columns = ['channel', 'segment', 'acc avr', 'acc std_dev', 'f1-sc avr', 'f1-sc std_dev']
df_results = DataFrame(columns=columns)
df_results.to_csv(csv_results, mode='a', header=True)

for ind_ch, channel in enumerate(all_channels):
    acc_avr = np.mean(np.array(accuracies[ind_ch]))
    acc_std = np.std(np.array(accuracies[ind_ch]))

    f1_avr = np.mean(np.array(f1scores[ind_ch]))
    f1_std = np.std(np.array(f1scores[ind_ch]))
    df_results = df_results.append({'channel': channel, 'segment': segments[0] + '+' + segments[1],  'acc avr': acc_avr,
                                    'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
                                   ignore_index=True)

df_results.to_csv(csv_results, mode='a', header=False)
