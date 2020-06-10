import os
import numpy as np
from pandas import DataFrame
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import  train_test_doa_balanced_on_train_on_test, \
    obtain_A_features_from_doa, obtain_A_features_from_doa_emphasize_stimulus

encoding = Encoding('./../../data_to_be_saved/m013/32alphabet3_classic_m013.txt', no_symbols=32)
data_dir = os.path.join('..', '..')

run_nr = 20
all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
                31, 32]
segments = ['spontaneous', 'stimulus']

levels = ['light4', 'deep6']
print(F'FIRST  PER SEGMENT INDIVIDUAllY   {levels}')

csv_file_1 = "svm_per_seg_L4D6_M013_classic.csv"
csv_results_1 = "svm_per_seg_L4D6_M013_classic_avr.csv"

output_name = "classification_svm_per_seg_L4D6_M013_classic.txt"
output_file = open(output_name, 'w')

output_file.write("Classify bt 2 levels,  classic, no mark or remove bursts\n")
output_file.write("LIGHT4 DEEP6 a single segment A matrix \n")
output_file.write("train_test_doa_remake_balanced 80% for train \n")

# data frame that keeps all runs for all channels, that will be added to .csv file
column_names = ['channel', 'segment', 'accuracy', 'f1-score']
df_all = DataFrame(columns=column_names)
df_all.to_csv(csv_file_1, mode='a', header=True)

# def __init__(self, current_directory, subject_directory, filtering_directory, levels=['deep', 'medium', 'light'], trials_to_skip=None):
initialization = InitDataSet(current_directory=data_dir, subject_directory="m013",
                                            filtering_directory="classic",
                                            levels=levels)
doas = initialization.get_dataset_as_doas()

print(f'initialized with {doas[0].level} and {doas[1].level}')

accuracies = [[[] for i in range(len(all_channels))] for j in range(len(segments))]
f1scores = [[[] for i in range(len(all_channels))] for j in range(len(segments))]

for run in range(run_nr):
    print('************************ RUN ' + str(run) + '************************')
    # firstly split the input into train test
    doas_train, doas_test = train_test_doa_balanced_on_train_on_test(doas)

    for ind_segment, segment in enumerate(segments):
        for chn_ind, channel in enumerate(all_channels):
            print("start running" + str(run) + " for channel " + str(channel) + ' seg ' + segment)
            output_file.write(f'####### run {run} channel {channel}  seg {segment} #########\n')

            X_train, y_train = obtain_A_features_from_doa(doas_train, channel, encoding,
                                                                       segments=[segment])
            x_test, y_test = obtain_A_features_from_doa(doas_test, channel, encoding, segments=[segment])

            model = SVC(gamma="auto")

            model.fit(X_train, y_train)

            # just for overfitting
            report_train = classification_report(y_train, model.predict(X_train), output_dict=True)
            acc_train = report_train['accuracy']
            print(f'predict on train  acc {acc_train}')
            output_file.write(f'predict train acc {acc_train}\n')

            predictions = model.predict(x_test)
            report = classification_report(y_test, predictions, output_dict=True)

            print(classification_report(y_test, predictions))
            print(confusion_matrix(y_test, predictions))

            output_file.write(classification_report(y_test, predictions))
            np.savetxt(output_file, np.array(confusion_matrix(y_test, predictions)), fmt="%s", newline=' ')
            output_file.write('\n')

            # calculate and write the mean  and std_dev of the average & f1-score
            acc = report['accuracy']
            f1sc = report['weighted avg']['f1-score']
            accuracies[ind_segment][chn_ind].append(acc)
            f1scores[ind_segment][chn_ind].append(f1sc)

            df_all = df_all.append(
                {'channel': channel, 'segment': segment, 'accuracy': acc, 'f1-score': f1sc}, ignore_index=True)

        # print('debug')
    df_all.to_csv(csv_file_1, mode='a', header=False)
    df_all = df_all.iloc[0:0]

output_file.close()

# data frame that keeps avr and std of the runs
columns = ['channel', 'segment', 'acc avr', 'acc std_dev', 'f1-sc avr', 'f1-sc std_dev']
df_results = DataFrame(columns=columns)
df_results.to_csv(csv_results_1, mode='a', header=True)

for ind_segment, segment in enumerate(segments):
    for ind_ch, channel in enumerate(all_channels):
        acc_avr = np.mean(np.array(accuracies[ind_segment][ind_ch]))
        acc_std = np.std(np.array(accuracies[ind_segment][ind_ch]))

        f1_avr = np.mean(np.array(f1scores[ind_segment][ind_ch]))
        f1_std = np.std(np.array(f1scores[ind_segment][ind_ch]))
        df_results = df_results.append({'channel': channel, 'segment': segment, 'acc avr': acc_avr,
                                        'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
                                       ignore_index=True)

    df_results.to_csv(csv_results_1, mode='a', header=False)
    df_results = df_results.iloc[0:0]

print('EMPHASIZE IMPORTANCE OF STIMULUS')

segment_here = 'stim-spon'
csv_file_2 = "svm_ephasize_stim_L4D6_M013_classic.csv"
csv_results_2 = "svm_ephasize_stim_L4D6_M013_classic_avr.csv"

output_name = "classification_svm_ephasize_stim_L4D6_M013_classic_avr.txt"
output_file = open(output_name, 'w')

output_file.write("Classify bt 2 levels, classic with mark and remove bursts\n")
output_file.write("LIGHT4 DEEP6 emphasize stimulus =  A matrix \n")
output_file.write("train_test_doa_remake_balanced 80% for train \n")

# data frame that keeps all runs for all channels, that will be added to .csv file
column_names = ['channel', 'segment', 'accuracy', 'f1-score']
df_all_2 = DataFrame(columns=column_names)
df_all_2.to_csv(csv_file_2, mode='a', header=True)

accuracies = [[] for i in range(len(all_channels))]
f1scores = [[] for i in range(len(all_channels))]

for run in range(run_nr):
    print('************************ RUN ' + str(run) + '************************')
    # firstly split the input into train test
    doas_train, doas_test = train_test_doa_balanced_on_train_on_test(doas)

    for chn_ind, channel in enumerate(all_channels):
        print("start running" + str(run) + " for channel " + str(channel) + ' seg ' + segment_here)
        output_file.write(f'####### run {run} channel {channel}  seg {segment_here} #########\n')

        X_train, y_train = obtain_A_features_from_doa_emphasize_stimulus(doas_train, channel, encoding)
        x_test, y_test = obtain_A_features_from_doa_emphasize_stimulus(doas_test, channel, encoding)

        model = SVC(gamma="auto")

        model.fit(X_train, y_train)

        # just for overfitting
        report_train = classification_report(y_train, model.predict(X_train), output_dict=True)
        acc_train = report_train['accuracy']
        print(f'predict on train  acc {acc_train}')
        output_file.write(f'predict train acc {acc_train}\n')

        predictions = model.predict(x_test)
        report = classification_report(y_test, predictions, output_dict=True)

        print(classification_report(y_test, predictions))
        print(confusion_matrix(y_test, predictions))

        output_file.write(classification_report(y_test, predictions))
        np.savetxt(output_file, np.array(confusion_matrix(y_test, predictions)), fmt="%s", newline=' ')
        output_file.write('\n')

        acc = report['accuracy']
        f1sc = report['weighted avg']['f1-score']
        accuracies[chn_ind].append(acc)
        f1scores[chn_ind].append(f1sc)

        # calculate and write the mean  and std_dev of the average & f1-score
        df_all_2 = df_all_2.append(
            {'channel': channel, 'segment': segment_here, 'accuracy': acc, 'f1-score': f1sc}, ignore_index=True)

        # print('debug')
    df_all_2.to_csv(csv_file_2, mode='a', header=False)
    df_all_2 = df_all_2.iloc[0:0]

output_file.close()

# data frame that keeps avr and std of the runs
columns = ['channel', 'segment', 'acc avr', 'acc std_dev', 'f1-sc avr', 'f1-sc std_dev']
df_results_2 = DataFrame(columns=columns)
df_results_2.to_csv(csv_results_2, mode='a', header=True)

for ind_ch, channel in enumerate(all_channels):
    acc_avr = np.mean(np.array(accuracies[ind_ch]))
    acc_std = np.std(np.array(accuracies[ind_ch]))

    f1_avr = np.mean(np.array(f1scores[ind_ch]))
    f1_std = np.std(np.array(f1scores[ind_ch]))
    df_results_2 = df_results_2.append({'channel': channel, 'segment': segment_here, 'acc avr': acc_avr,
                                        'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
                                       ignore_index=True)

df_results_2.to_csv(csv_results_2, mode='a', header=False)
df_results_2 = df_results_2.iloc[0:0]

print('DONE FOR EMPHASIZE STIM ')
