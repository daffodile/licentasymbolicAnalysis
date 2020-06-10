import os
import numpy as np
from pandas import DataFrame
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC
from feature_extraction.TESPAR.Encoding import Encoding
from feature_extraction.TESPAR.EncodingCheckBursts import EncodingCheckBursts
from input_reader.InitDataSet import InitDataSet
from input_reader.InitDataSetWithBurstsFlags import InitDataSetWithBurstsFlags
from utils.DataSpliting import obtain_A_features_from_doa, train_test_doa_remake_balanced, \
    obtain_A_features_from_doa_check_bursts, train_test_doa_balanced_on_train_on_test
from utils.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions
from utils.MarkOutsidersWithBurstsFlags import remove_bursted_trials_when_segment

run_nr = 20
all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
                31, 32]
segment = 'stim_spon'

data_dir = os.path.join('..', '..')

column_names_all = ['channel', 'segment', 'accuracy', 'f1-score']
columns_results_avr = ['channel', 'segment', 'acc avr', 'acc std_dev', 'f1-sc avr', 'f1-sc std_dev']

# this part was completed

# encoding = Encoding('./../../data_to_be_saved/m013/32alphabet3_classic_m013.txt')

# #######################################################  L4M5D6 classicv ##########################################
# print(
#     '################################################ L4M5D6 classic ################################################################')
# csv_file_4 = "svm_L4M5D6_M013_classic.csv"
# csv_results_4 = "svm_L4M5D6_M013_classic_avr.csv"
#
# output_name_4 = "classification_svm_L4M5D6_M013_classic.txt"
# output_file_4 = open(output_name_4, 'w')
#
# output_file_4.write("Classify bt LAST 3 levels, classic, without marking bursts\n")
# output_file_4.write("LIGHT4 MEDIUM5 DEEP6  stim_spon concatenate A matrix \n")
# output_file_4.write("train_test_doa_remake_balanced 80% for train \n")
#
# # data frame that keeps all runs for all channels, that will be added to .csv file
# df_all_4 = DataFrame(columns=column_names_all)
# df_all_4.to_csv(csv_file_4, mode='a', header=True)
#
# levels = ['light4', 'medium5', 'deep6']
#
# # def __init__(self, current_directory, subject_directory, filtering_directory, levels=['deep', 'medium', 'light'], trials_to_skip=None):
# initialization = InitDataSet(current_directory=data_dir, subject_directory="m013", filtering_directory="classic",
#                              levels=levels)
# doas = initialization.get_dataset_as_doas()
# print(f'initialized with {doas[0].level}  {doas[1].level}')
#
# accuracies_4 = [[] for i in range(len(all_channels))]
# f1scores_4 = [[] for i in range(len(all_channels))]
#
# for run in range(run_nr):
#     print('************************RUN ' + str(run) + ' of ' + str(levels) + '************************')
#     # firstly split the input into train test
#     doas_train, doas_test = train_test_doa_remake_balanced(doas)
#
#     for chn_ind, channel in enumerate(all_channels):
#         print("start running " + str(run) + " for channel " + str(channel))
#         output_file_4.write(f'####### run {run} channel {channel} #########\n')
#
#         # obtain_A_features_from_doa(doas, channel_number, encoding, segments=['spontaneous', 'stimulus'],
#         #                                selected_symbols=None):
#         X_train, y_train = obtain_A_features_from_doa(doas_train, channel, encoding)
#         x_test, y_test = obtain_A_features_from_doa(doas_test, channel, encoding)
#
#         model = SVC(gamma="auto")
#
#         model.fit(X_train, y_train)
#
#         # just for overfitting
#         report_train = classification_report(y_train, model.predict(X_train), output_dict=True)
#         acc_train = report_train['accuracy']
#         print(f'predict on train  acc {acc_train}')
#         output_file_4.write(f'predict train acc {acc_train}\n')
#
#         predictions = model.predict(x_test)
#         report = classification_report(y_test, predictions, output_dict=True)
#
#         print(classification_report(y_test, predictions))
#         print(confusion_matrix(y_test, predictions))
#
#         output_file_4.write(classification_report(y_test, predictions))
#         np.savetxt(output_file_4, np.array(confusion_matrix(y_test, predictions)), fmt="%s", newline=' ')
#         output_file_4.write('\n')
#
#         acc = report['accuracy']
#         f1sc = report['weighted avg']['f1-score']
#         accuracies_4[chn_ind].append(acc)
#         f1scores_4[chn_ind].append(f1sc)
#
#         # calculate and write the mean  and std_dev of the average & f1-score
#         df_all_4 = df_all_4.append(
#             {'channel': channel, 'segment': segment, 'accuracy': acc, 'f1-score': f1sc}, ignore_index=True)
#
#         # print('debug')
#     df_all_4.to_csv(csv_file_4, mode='a', header=False)
#     df_all_4 = df_all_4.iloc[0:0]
#
# output_file_4.close()
#
# # data frame that keeps avr and std of the runs
# df_results_4 = DataFrame(columns=columns_results_avr)
# df_results_4.to_csv(csv_results_4, mode='a', header=True)
#
# for ind_ch, channel in enumerate(all_channels):
#     acc_avr = np.mean(np.array(accuracies_4[ind_ch]))
#     acc_std = np.std(np.array(accuracies_4[ind_ch]))
#
#     f1_avr = np.mean(np.array(f1scores_4[ind_ch]))
#     f1_std = np.std(np.array(f1scores_4[ind_ch]))
#     df_results_4 = df_results_4.append({'channel': channel, 'segment': segment, 'acc avr': acc_avr,
#                                         'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
#                                        ignore_index=True)
#
# df_results_4.to_csv(csv_results_4, mode='a', header=False)

# ######################################################  L4M5D6 remove bursts ##########################################
# print(
#     '################################################ L4M5D6 remove bursts ################################################################')
# csv_file_3 = "svm_L4M5D6_M013_remove_bursts.csv"
# csv_results_3 = "svm_L4M5D6_M013_remove_bursts_avr.csv"
#
# output_name_3 = "classification_svm_L4M5D6_M013_remove_bursts.txt"
# output_file_3 = open(output_name_3, 'w')
#
# output_file_3.write("Classify bt 3 levels, remove bursting trials and marking bursts\n")
# output_file_3.write("LIGHT4  MEDIUM5 DEEP6  stim_spon concatenate A matrix \n")
# output_file_3.write("train_test_doa_remake_balanced 80% for train \n")
#
# # data frame that keeps all runs for all channels, that will be added to .csv file
# df_all_3 = DataFrame(columns=column_names_all)
# df_all_3.to_csv(csv_file_3, mode='a', header=True)
#
# encoding_burst = EncodingCheckBursts('./../../data_to_be_saved/m013/32alphabet3_classic_m013.txt')
#
# levels = ['light4', 'medium5', 'deep6']
#
# # def __init__(self, current_directory, subject_directory, filtering_directory, levels=['deep', 'medium', 'light'], trials_to_skip=None):
# initialization = InitDataSetWithBurstsFlags(current_directory=data_dir, subject_directory="m013",
#                                             filtering_directory="classic",
#                                             levels=levels)
# doas = initialization.get_dataset_as_doas()
# print(f'initialized with {doas[0].level}  {doas[1].level}')
#
# # m013 ar trebui, nu o fost
# mark_bursts_regions(doas, subject='m013')
#
# remove_bursted_trials_when_segment(doas)
#
# accuracies_3 = [[] for i in range(len(all_channels))]
# f1scores_3 = [[] for i in range(len(all_channels))]
#
# for run in range(run_nr):
#     print('************************RUN ' + str(run) + ' of ' + str(levels) + '************************')
#     # firstly split the input into train test
#     doas_train, doas_test = train_test_doa_balanced_on_train_on_test(doas)
#
#     for chn_ind, channel in enumerate(all_channels):
#         print("start running " + str(run) + " for channel " + str(channel))
#         output_file_3.write(f'####### run {run} channel {channel} #########\n')
#
#         X_train, y_train = obtain_A_features_from_doa_check_bursts(doas_train, channel, encoding_burst)
#         x_test, y_test = obtain_A_features_from_doa_check_bursts(doas_test, channel, encoding_burst)
#
#         model = SVC(gamma="auto")
#
#         model.fit(X_train, y_train)
#
#         # just for overfitting
#         report_train = classification_report(y_train, model.predict(X_train), output_dict=True)
#         acc_train = report_train['accuracy']
#         print(f'predict on train  acc {acc_train}')
#         output_file_3.write(f'predict train acc {acc_train}\n')
#
#         predictions = model.predict(x_test)
#         report = classification_report(y_test, predictions, output_dict=True)
#
#         print(classification_report(y_test, predictions))
#         print(confusion_matrix(y_test, predictions))
#
#         output_file_3.write(classification_report(y_test, predictions))
#         np.savetxt(output_file_3, np.array(confusion_matrix(y_test, predictions)), fmt="%s", newline=' ')
#         output_file_3.write('\n')
#
#         acc = report['accuracy']
#         f1sc = report['weighted avg']['f1-score']
#         accuracies_3[chn_ind].append(acc)
#         f1scores_3[chn_ind].append(f1sc)
#
#         # calculate and write the mean  and std_dev of the average & f1-score
#         df_all_3 = df_all_3.append(
#             {'channel': channel, 'segment': segment, 'accuracy': acc, 'f1-score': f1sc}, ignore_index=True)
#
#         # print('debug')
#     df_all_3.to_csv(csv_file_3, mode='a', header=False)
#     df_all_3 = df_all_3.iloc[0:0]
#
# output_file_3.close()
#
# # data frame that keeps avr and std of the runs
# df_results_3 = DataFrame(columns=columns_results_avr)
# df_results_3.to_csv(csv_results_3, mode='a', header=True)
#
# for ind_ch, channel in enumerate(all_channels):
#     acc_avr = np.mean(np.array(accuracies_3[ind_ch]))
#     acc_std = np.std(np.array(accuracies_3[ind_ch]))
#
#     f1_avr = np.mean(np.array(f1scores_3[ind_ch]))
#     f1_std = np.std(np.array(f1scores_3[ind_ch]))
#     df_results_3 = df_results_3.append({'channel': channel, 'segment': segment, 'acc avr': acc_avr,
#                                         'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
#                                        ignore_index=True)
#
# df_results_3.to_csv(csv_results_3, mode='a', header=False)

#######################################################  L4M5D6 highpass ##########################################

encoding_hp10 = Encoding('./../../data_to_be_saved/m013/32alphabet1_highpass10_m013.txt')

print(
    '################################################ L2D6 highpass10 ################################################################')
csv_file_2 = "svm_L4M5D6_M013_highpass10.csv"
csv_results_2 = "svm_L4M5D6_M013_highpass10_avr.csv"

output_name_2 = "classification_svm_L4M5D6_M013_highpass10.txt"
output_file_2 = open(output_name_2, 'w')

output_file_2.write("Classify bt LAST 3 levels, highpass10, without marking bursts\n")
output_file_2.write("LIGHT2 MEDIUM5 DEEP6   stim_spon concatenate A matrix \n")
output_file_2.write("train_test_doa_remake_balanced 80% for train \n")

# data frame that keeps all runs for all channels, that will be added to .csv file
df_all_2 = DataFrame(columns=column_names_all)
df_all_2.to_csv(csv_file_2, mode='a', header=True)

levels = ['light4', 'medium5', 'deep6']

# def __init__(self, current_directory, subject_directory, filtering_directory, levels=['deep', 'medium', 'light'], trials_to_skip=None):
initialization = InitDataSet(current_directory=data_dir, subject_directory="m013", filtering_directory="highpass10",
                             levels=levels)
doas = initialization.get_dataset_as_doas()
print(f'initialized with {doas[0].level}  {doas[1].level}')

accuracies_2 = [[] for i in range(len(all_channels))]
f1scores_2 = [[] for i in range(len(all_channels))]

for run in range(run_nr):
    print('************************RUN ' + str(run) + ' of ' + str(levels) + '************************')
    # firstly split the input into train test
    doas_train, doas_test = train_test_doa_remake_balanced(doas)

    for chn_ind, channel in enumerate(all_channels):
        print("start running " + str(run) + " for channel " + str(channel))
        output_file_2.write(f'####### run {run} channel {channel} #########\n')

        # obtain_A_features_from_doa(doas, channel_number, encoding, segments=['spontaneous', 'stimulus'],
        #                                selected_symbols=None):
        X_train, y_train = obtain_A_features_from_doa(doas_train, channel, encoding_hp10)
        x_test, y_test = obtain_A_features_from_doa(doas_test, channel, encoding_hp10)

        model = SVC(gamma="auto")

        model.fit(X_train, y_train)

        # just for overfitting
        report_train = classification_report(y_train, model.predict(X_train), output_dict=True)
        acc_train = report_train['accuracy']
        print(f'predict on train  acc {acc_train}')
        output_file_2.write(f'predict train acc {acc_train}\n')

        predictions = model.predict(x_test)
        report = classification_report(y_test, predictions, output_dict=True)

        print(classification_report(y_test, predictions))
        print(confusion_matrix(y_test, predictions))

        output_file_2.write(classification_report(y_test, predictions))
        np.savetxt(output_file_2, np.array(confusion_matrix(y_test, predictions)), fmt="%s", newline=' ')
        output_file_2.write('\n')

        acc = report['accuracy']
        f1sc = report['weighted avg']['f1-score']
        accuracies_2[chn_ind].append(acc)
        f1scores_2[chn_ind].append(f1sc)

        # calculate and write the mean  and std_dev of the average & f1-score
        df_all_2 = df_all_2.append(
            {'channel': channel, 'segment': segment, 'accuracy': acc, 'f1-score': f1sc}, ignore_index=True)

        # print('debug')
    df_all_2.to_csv(csv_file_2, mode='a', header=False)
    df_all_2 = df_all_2.iloc[0:0]

output_file_2.close()

# data frame that keeps avr and std of the runs
df_results_2 = DataFrame(columns=columns_results_avr)
df_results_2.to_csv(csv_results_2, mode='a', header=True)

for ind_ch, channel in enumerate(all_channels):
    acc_avr = np.mean(np.array(accuracies_2[ind_ch]))
    acc_std = np.std(np.array(accuracies_2[ind_ch]))

    f1_avr = np.mean(np.array(f1scores_2[ind_ch]))
    f1_std = np.std(np.array(f1scores_2[ind_ch]))
    df_results_2 = df_results_2.append({'channel': channel, 'segment': segment, 'acc avr': acc_avr,
                                        'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
                                       ignore_index=True)

df_results_2.to_csv(csv_results_2, mode='a', header=False)
