import os

import numpy as np
from pandas import DataFrame
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import train_test_doa_remake_balanced, obtain_A_features_from_doa

csv_file = "svm_remove_annotated_balanced.csv"
csv_results = "svm_remove_annotated_balanced_avr.csv"

output_name = "classification_results_annotated_balanced.txt"
output_file = open(output_name, 'w')

output_file.write("Remove annotated trials balanced train test split 25 apr \n")
output_file.write("train_test_doa_remake_balanced 80% of smallest class \n")

# how many models to train a for a channel-segment pair
run_nr = 20

all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
                31, 32]

segments = ['spontaneous', 'stimulus']

# data frame that keeps all runs for all channels, that will be added to .csv file
column_names = ['channel', 'segment', 'accuracy', 'f1-score']
df_all = DataFrame(columns=column_names)
df_all.to_csv(csv_file, mode='a', header=True)

# DEFAULT DATASET CONTAINS DEEP LIGHT CLASSES
data_dir = os.path.join('..', '..')
initialization = InitDataSet(data_dir=data_dir, directory='no_bursts', trials_to_skip=[1, 2])
doas = initialization.get_dataset_as_doas()

encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')

accuracies = [[[] for i in range(len(all_channels))] for j in range(len(segments))]
f1scores = [[[] for i in range(len(all_channels))] for j in range(len(segments))]

for run in range(run_nr):
    print('************************RUN ' + str(run) + '************************')
    # firstly split the input into train test
    doas_train, doas_test = train_test_doa_remake_balanced(doas)

    for ind_segment, segment in enumerate(segments):
        for chn_ind, channel in enumerate(all_channels):
            print("start running for channel " + str(channel) + ' ' + segment + '\n')
            output_file.write(f'run {run} channel {channel} \n')

            # def obtain_A_features_from_doa(doas, channel_number, encoding, segments=['spontaneous', 'stimulus'],
            X_train, y_train = obtain_A_features_from_doa(doas_train, channel, encoding, segments=[segment])
            x_test, y_test = obtain_A_features_from_doa(doas_test, channel, encoding, segments=[segment])

            model = SVC(gamma="auto")

            model.fit(X_train, y_train)
            predictions = model.predict(x_test)

            report = classification_report(y_test, predictions, output_dict=True)

            print(classification_report(y_test, predictions))
            print(confusion_matrix(y_test, predictions))

            output_file.write(classification_report(y_test, predictions))
            np.savetxt(output_file, np.array(confusion_matrix(y_test, predictions)), fmt="%s", newline=' ')
            output_file.write('\n')

            acc = report['accuracy']
            f1sc = report['weighted avg']['f1-score']
            accuracies[ind_segment][chn_ind].append(acc)
            f1scores[ind_segment][chn_ind].append(f1sc)

            # calculate and write the mean  and std_dev of the average & f1-score
            df_all = df_all.append(
                {'channel': channel, 'segment': segment, 'accuracy': acc, 'f1-score': f1sc}, ignore_index=True)

            # print('debug')
    df_all.to_csv(csv_file, mode='a', header=False)
    df_all = df_all.iloc[0:0]

output_file.close()

# data frame that keeps avr and std of the runs
columns = ['channel', 'segment', 'acc avr', 'acc std_dev', 'f1-sc avr', 'f1-sc std_dev']
df_results = DataFrame(columns=columns)
df_results.to_csv(csv_results, mode='a', header=True)

for ind_segment, segment in enumerate(segments):
    for ind_ch, channel in enumerate(all_channels):
        acc_avr = np.mean(np.array(accuracies[ind_segment][ind_ch]))
        acc_std = np.std(np.array(accuracies[ind_segment][ind_ch]))

        f1_avr = np.mean(np.array(f1scores[ind_segment][ind_ch]))
        f1_std = np.std(np.array(f1scores[ind_segment][ind_ch]))
        df_results = df_results.append({'channel': channel, 'segment': segment, 'acc avr': acc_avr,
                                        'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
                                       ignore_index=True)

df_results.to_csv(csv_results, mode='a', header=False)