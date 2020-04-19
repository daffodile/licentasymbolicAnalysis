import os

from pandas import DataFrame
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from train_test_split.Train_Test_Doa import train_test_doa_consistent
from utils.DataSpliting import train_test_doa, obtain_features_labels, obtain_A_features_from_doa, \
    obtain_features_labels_from_doa

####### to change for each  classifier this 3 files #################################
csv_file = "svm_all_3cls.csv"

channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
            31, 32]

# segments = ['spontaneous']
segments = ['spontaneous', 'stimulus', 'poststimulus']

# data frame that keeps all runs for all channels, that will be added to .csv file
column_names = ['channel', 'segment', 'accuracy', 'f1-score']
df_all = DataFrame(columns=column_names)
df_all.to_csv(csv_file, mode='a', header=True)

encoding = Encoding('./../data_to_be_saved/alphabet_3.txt')

data_dir = os.path.join('', '..')

initialization = InitDataSet(data_dir=data_dir, levels=['deep', 'medium', 'light'])

doas = initialization.get_dataset_as_doas()

# firstly split the input into train test
doas_train, doas_test, ind_test = train_test_doa_consistent(doas, 0.2)

for segment in segments:
    for channel in channels:
        # obtain_features_labels_from_doa(doas, channel_number, segment, encoding, selected_symbols=None):
        X_train, y_train = obtain_features_labels_from_doa(doas_train, channel, segment, encoding)
        x_test, y_test = obtain_features_labels_from_doa(doas_test, channel, segment, encoding)


        model = SVC(gamma='auto', verbose=True)

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
        # calculate and write the mean  and std_dev of the average & f1-score
        df_all = df_all.append(
            {'channel': channel, 'segment': segment, 'accuracy': acc_test, 'f1-score': f1sc_test},
            ignore_index=True)

df_all.to_csv(csv_file, mode='a', header=False)

#  # for ind_segment, segment in enumerate(segments):
#
# for ind_ch, channel in enumerate(channels):
#     print("start running for channel " + str(channel) + '\n')
#
#     X_train, y_train = obtain_features_labels_from_doa(doas_train, channel, encoding)
#     x_test, y_test = obtain_features_labels_from_doa(doas_test, channel, encoding)
#
#     model = SVC(gamma='auto')
#
#     model.fit(X_train, y_train)
#
#     predictions_train = model.predict(X_train)
#     print('train subset')
#     print(confusion_matrix(y_train, predictions_train))
#     print(classification_report(y_train, predictions_train))
#
#     predictions_test = model.predict(x_test)
#     print('test subset')
#     print(confusion_matrix(y_test, predictions_test))
#     print(classification_report(y_test, predictions_test))
#
#     report_train = classification_report(y_train, predictions_train, output_dict=True)
#     report_test = classification_report(y_test, predictions_test, output_dict=True)
#
#     acc_train = report_train['accuracy']
#     f1sc_train = report_train['weighted avg']['f1-score']
#
#     acc_test = report_test['accuracy']
#     f1sc_test = report_test['weighted avg']['f1-score']
#
#     print('ch=' + str(channel) + " accuracy train " + str(acc_train) + ' vs ' + str(
#         acc_test) + ' test')
#
#     # calculate and write the mean  and std_dev of the average & f1-score
#     df_all = df_all.append(
#         {'channel': channel, 'segment': 'spon_stim', 'accuracy': acc_test, 'f1-score': f1sc_test},
#         ignore_index=True)
#
#
#     # calculate and write the mean  and std_dev of the average & f1-score
#     df_all = df_all.append(
#         {'channel': channel, 'segment': segment, 'accuracy': acc_test, 'f1-score': f1sc_test},
#         ignore_index=True)
#
# df_all.to_csv(csv_file, mode='a', header=False)
