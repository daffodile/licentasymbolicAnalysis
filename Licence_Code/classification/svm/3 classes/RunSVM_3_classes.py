import numpy as np
from pandas import DataFrame
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import train_test_doa, obtain_A_features_from_doa

####### to change for each  classifier this 3 files #################################
csv_file = "svm_3classes_all.csv"
csv_results = "svm_3classes_averages.csv"
# open file to write the indices of  each splitting
indexes_file = "svm_3classes_indexes.txt"
write_file = open(indexes_file, "w")

# how many models to train a for a channel-segment pair
run_nr = 20

# # once per filter hereee
# all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
#                 31, 32]
all_channels = [2, 3, 5, 6, 7, 13, 15, 19, 20, 21, 25, 26, 27, 29]

# segments = ['spontaneous']
# segments = ['spontaneous', 'stimulus']

# data frame that keeps all runs for all channels, that will be added to .csv file
column_names = ['channel', 'segment', 'accuracy', 'f1-score']
df_all = DataFrame(columns=column_names)
df_all.to_csv(csv_file, mode='a', header=True)

encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')

initialization = InitDataSet(levels=['deep', 'medium', 'light'])
doas = initialization.get_dataset_as_doas()

accuracies = [[] for i in range(len(all_channels))]
f1scores = [[] for i in range(len(all_channels))]
for run in range(run_nr):
    # firstly split the input into train test
    doas_train, doas_test, ind_test = train_test_doa(doas, 0.2)
    np.savetxt(write_file, np.array(ind_test), fmt="%s", newline=' ')
    write_file.write('\n')

    # for ind_segment, segment in enumerate(segments):
    for ind_ch, channel in enumerate(all_channels):
        print("start running for channel " + str(channel) + '\n')

        X_train, y_train = obtain_A_features_from_doa(doas_train, channel, encoding)
        x_test, y_test = obtain_A_features_from_doa(doas_test, channel, encoding)

        model = SVC(gamma='auto')

        model.fit(X_train, y_train)

        predictions_train = model.predict(X_train)
        print('train subset')
        print(confusion_matrix(y_train, predictions_train))
        print(classification_report(y_train, predictions_train))

        predictions_test = model.predict(x_test)
        print('test subset')
        print(confusion_matrix(y_test, predictions_test))
        print(classification_report(y_test, predictions_test))

        report_train = classification_report(y_train, predictions_train, output_dict=True)
        report_test = classification_report(y_test, predictions_test, output_dict=True)

        acc_train = report_train['accuracy']
        f1sc_train = report_train['weighted avg']['f1-score']

        acc_test = report_test['accuracy']
        f1sc_test = report_test['weighted avg']['f1-score']

        print('ch=' + str(channel) + " accuracy train " + str(acc_train) + ' vs ' + str(
            acc_test) + ' test')

        # acc = report['accuracy']
        # f1sc = report['weighted avg']['f1-score']
        accuracies[ind_ch].append(acc_test)
        f1scores[ind_ch].append(f1sc_test)

        # calculate and write the mean  and std_dev of the average & f1-score
        df_all = df_all.append(
            {'channel': channel, 'segment': 'spon_stim', 'accuracy': acc_test, 'f1-score': f1sc_test},
            ignore_index=True)

        # print('debug')
df_all.to_csv(csv_file, mode='a', header=False)
df_all = df_all.iloc[0:0]

write_file.close()

# data frame that keeps avr and std of the runs
columns = ['channel', 'segment', 'acc avr', 'acc std_dev', 'f1-sc avr', 'f1-sc std_dev']
df_results = DataFrame(columns=columns)
df_results.to_csv(csv_results, mode='a', header=True)

for ind_ch, channel in enumerate(all_channels):
    acc_avr = np.mean(np.array(accuracies[ind_ch]))
    acc_std = np.std(np.array(accuracies[ind_ch]))

    f1_avr = np.mean(np.array(f1scores[ind_ch]))
    f1_std = np.std(np.array(f1scores[ind_ch]))
    df_results = df_results.append({'channel': channel, 'segment': 'spon_stim', 'acc avr': acc_avr,
                                    'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
                                   ignore_index=True)

df_results.to_csv(csv_results, mode='a', header=False)
