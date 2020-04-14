import numpy as np
from pandas import DataFrame
from sklearn.metrics import classification_report
from sklearn.svm import SVC

####### to change for each  classifier this 3 files #################################
from feature_extraction.TESPAR.EncodingCheckBursts import EncodingCheckBursts
from input_reader.InitDataSetWithBurstsFlags import InitDataSetWithBurstsFlags
from utils.DataSpliting import train_test_doa_check_trials, obtain_features_labels_with_bursts_flags
from utils.MarkOutsidersWithBurstsFlags import mark_outsiders, remove_bursted_trials_when_full_trial
from utils.SplitDataWithBurstsFlags import SplitDataWithBurstsFlags
from vizualization.classification.Accuracy_distribution import plot_distributions

csv_file = "svm_remove_bursts.csv"
csv_results = "svm_remove_bursts_avr.csv"
# open file to write the indices of  each splitting
indexes_file = "svm_remove_bursts_indexes.txt"
write_file = open(indexes_file, "w")

# how many models to train a for a channel-segment pair
run_nr = 10

# # once per filter hereee
# channels_range = 31
# all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
#                 31, 32]
all_channels = [3, 5, 7, 13, 15]
segments = ['spontaneous', 'stimulus', 'poststimulus']

# data frame that keeps all runs for all channels, that will be added to .csv file
column_names = ['channel', 'segment', 'accuracy', 'f1-score']
df_all = DataFrame(columns=column_names)
df_all.to_csv(csv_file, mode='a', header=True)

initialization = InitDataSetWithBurstsFlags()
doas = initialization.get_dataset_as_doas()

mark_outsiders(doas, max_interbursts_dist=200)

remove_bursted_trials_when_full_trial(doas)

encoding = EncodingCheckBursts('./../../data_to_be_saved/alphabet_3.txt')

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

            # SplitData(self, doas, channels, levels, segment, orientation):
            train_data = SplitDataWithBurstsFlags(doas_train, [channel], ['light', 'deep'], [segment], ['all'])
            test_data = SplitDataWithBurstsFlags(doas_test, [channel], ['light', 'deep'], [segment], ['all'])

            X_train, y_train = obtain_features_labels_with_bursts_flags(train_data, encoding)
            x_test, y_test = obtain_features_labels_with_bursts_flags(test_data, encoding)

            model = SVC(gamma="auto", verbose=True)

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
    # d_i = []
    # n = []
    for ind_ch, channel in enumerate(all_channels):
        acc_avr = np.mean(np.array(accuracies[ind_segment][ind_ch]))
        acc_std = np.std(np.array(accuracies[ind_segment][ind_ch]))

        f1_avr = np.mean(np.array(f1scores[ind_segment][ind_ch]))
        f1_std = np.std(np.array(f1scores[ind_segment][ind_ch]))
        df_results = df_results.append({'channel': channel, 'segment': segment, 'acc avr': acc_avr,
                                        'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
                                       ignore_index=True)
        # d_i.append([acc_avr, acc_std])
        # n.append(channel)
    # plot_distributions(d_i, n, str(segment) + str(3))

df_results.to_csv(csv_results, mode='a', header=False)
