import os

import numpy as np
from pandas import DataFrame
from sklearn.metrics import classification_report
from sklearn.svm import SVC

####### to change for each  classifier this 3 files #################################
from feature_extraction.TESPAR.Encoding import Encoding
from feature_extraction.TESPAR.EncodingCheckBursts import EncodingCheckBursts
from input_reader.InitDataSetWithBurstsFlags import InitDataSetWithBurstsFlags
from utils.DataSpliting import train_test_doa_check_trials, obtain_features_labels_from_doa, \
    obtain_A_features_from_doa_with_bursts_frags, obtain_S_TESPAR_features_from_doa
from utils.MarkOutsidersWithBurstsFlags import remove_bursted_trials_when_segment
from utils.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions

csv_file = "svm_remove_bursts_s.csv"
csv_results = "svm_remove_bursts_s_avr.csv"
# open file to write the indices of  each splitting
indexes_file = "svm_remove_bursts_s_indexes.txt"
write_file = open(indexes_file, "w")

# how many models to train a for a channel-segment pair
run_nr = 30

# all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
#                 31, 32]

all_channels = [2, 3, 5, 6, 7, 13, 15, 19, 20, 21, 25, 26, 27, 29]
segments = ['spontaneous', 'stimulus']

# data frame that keeps all runs for all channels, that will be added to .csv file
column_names = ['channel', 'segment', 'accuracy', 'f1-score']
df_all = DataFrame(columns=column_names)
df_all.to_csv(csv_file, mode='a', header=True)

# encoding = EncodingCheckBursts('./../../data_to_be_saved/alphabet_3.txt')
encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')

data_dir = os.path.join('..', '..')
initialization = InitDataSetWithBurstsFlags(data_dir)
doas = initialization.get_dataset_as_doas()

'''
default settings are:
def mark_bursts_regions(doas, thresholds={'deep': 19.74, 'medium': 24.97, 'light': 32.00}, max_interbursts_dist=364,
                        to_extend_margins=False, percent_margins=0.1, hilbert=False):
def remove_bursted_trials_when_segment(doas, segments=['spontaneous', 'stimulus'], tolerance_inside_trial=0.33,
               tolerance_over_channels=0.33):
'''
mark_bursts_regions(doas)

remove_bursted_trials_when_segment(doas)

accuracies = [[[] for i in range(len(all_channels))] for j in range(len(segments))]
f1scores = [[[] for i in range(len(all_channels))] for j in range(len(segments))]

for run in range(run_nr):
    print('************************RUN ' + str(run) + '************************')
    # firstly split the input into train test
    doas_train, doas_test, ind_test = train_test_doa_check_trials(doas, 0.2)

    np.savetxt(write_file, np.array(ind_test), fmt="%s", newline=' ')
    write_file.write('\n')

    for ind_segment, segment in enumerate(segments):
        for chn_ind, channel in enumerate(all_channels):
            print("start running for channel " + str(channel) + ' ' + segment + '\n')

            # already run as this:
            # obtain_A_features_from_doa_with_bursts_frags(doas, channel_number, segment, encoding, selected_symbols=None):
            # X_train, y_train = obtain_A_features_from_doa_with_bursts_frags(doas_train, channel, segment, encoding)
            # x_test, y_test = obtain_A_features_from_doa_with_bursts_frags(doas_test, channel, segment, encoding)

            X_train, y_train = obtain_S_TESPAR_features_from_doa(doas_train, channel, segment, encoding)
            x_test, y_test = obtain_S_TESPAR_features_from_doa(doas_test, channel, segment, encoding)

            model = SVC(gamma="auto")

            model.fit(X_train, y_train)
            predictions = model.predict(x_test)

            report = classification_report(y_test, predictions, output_dict=True)

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

write_file.close()

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
