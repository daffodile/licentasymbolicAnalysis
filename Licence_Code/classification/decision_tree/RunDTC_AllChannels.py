import numpy as np
from pandas import DataFrame
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import train_test_doa_check_trials, obtain_features_labels, obtain_features_labels_log, \
    obtain_features_labels_quality, obtain_S_TESPAR_features
from utils.ExtractData import ExtractData
from utils.mark_bursts.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions
from utils.mark_bursts.MarkOutsidersWithBurstsFlags import remove_bursted_trials_when_segment

csv_file = "dtc_30_alph3_s.csv"
csv_results = "dtc_30_avg_alph3_s.csv"
# open file to write the indices of  each splitting
indexes_file = "dtc_30_indexes_alph3_s.txt"
write_file = open(indexes_file, "w")

# how many models to train a for a channel-segment pair
run_nr = 10

channels_range = 31
all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
                31, 32]

segments = ['spontaneous', 'stimulus']

# data frame that keeps all runs for all channels, that will be added to .csv file
column_names = ['channel', 'segment', 'accuracy', 'f1-score']
df_all = DataFrame(columns=column_names)
df_all.to_csv(csv_file, mode='a', header=True)

initialization = InitDataSet()

doas = initialization.get_dataset_as_doas()

# mark_bursts_regions(doas)

# remove_bursted_trials_when_segment(doas)

encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')
# encoding = Encoding('./../../data_to_be_saved/alphabet_5.txt')

'''
for calculating the average acc or af1-score
we need
dictionary to keep array of 30 values for 3 segments for 30 channels
'''
accuracies = [[[] for i in range(channels_range - 1)] for j in range(len(segments))]
f1scores = [[[] for i in range(channels_range - 1)] for j in range(len(segments))]

for run in range(run_nr):
    print('************************RUN ' + str(run) + '************************')
    # firstly split the input into train test
    doas_train, doas_test, ind_test = train_test_doa_check_trials(doas, 0.2)
    np.savetxt(write_file, np.array(ind_test), fmt="%s", newline=' ')
    write_file.write('\n')

    for ind_segment, segment in enumerate(segments):
        for channel in range(len(all_channels)):
            print("start running for channel " + str(all_channels[channel]) + ' ' + segment + '\n')

            train_data = ExtractData(doas_train, [all_channels[channel]], ['light', 'deep'], [segment], ['all'])
            test_data = ExtractData(doas_test, [all_channels[channel]], ['light', 'deep'], [segment], ['all'])

            X_train, y_train = obtain_S_TESPAR_features(train_data, encoding)
            x_test, y_test = obtain_S_TESPAR_features(test_data, encoding)

            model = DecisionTreeClassifier(random_state=99, criterion='gini', max_depth=2)
            model.fit(X_train, y_train)
            predictions = model.predict(x_test)

            report = classification_report(y_test, predictions, output_dict=True)

            acc = report['accuracy']
            f1sc = report['weighted avg']['f1-score']
            accuracies[ind_segment][channel - 1].append(acc)
            f1scores[ind_segment][channel - 1].append(f1sc)

            # calculate and write the mean  and std_dev of the average & f1-score
            df_all = df_all.append(
                {'channel': all_channels[channel], 'segment': segment, 'accuracy': acc, 'f1-score': f1sc},
                ignore_index=True)

            # print('debug')
    df_all.to_csv(csv_file, mode='a', header=False)
    df_all = df_all.iloc[0:0]

write_file.close()

# data frame that keeps avr and std of the runs
columns = ['channel', 'segment', 'acc avr', 'acc std_dev', 'f1-sc avr', 'f1-sc std_dev']
df_results = DataFrame(columns=columns)
df_results.to_csv(csv_results, mode='a', header=True)

for ind_segment, segment in enumerate(segments):
    d_i = []
    n = []
    for channel in range(len(all_channels)):
        acc_avr = np.mean(np.array(accuracies[ind_segment][channel - 1]))
        acc_std = np.std(np.array(accuracies[ind_segment][channel - 1]))

        f1_avr = np.mean(np.array(f1scores[ind_segment][channel - 1]))
        f1_std = np.std(np.array(f1scores[ind_segment][channel - 1]))
        df_results = df_results.append({'channel': all_channels[channel], 'segment': segment, 'acc avr': acc_avr,
                                        'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
                                       ignore_index=True)
        d_i.append([acc_avr, acc_std])
        n.append(all_channels[channel])
    # plot_distributions(d_i, n, str(segment) + str(3))

df_results.to_csv(csv_results, mode='a', header=False)
