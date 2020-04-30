import numpy as np
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

from classification.random_forest.Utils_classification import train_test_doa_remake_balanced
from feature_extraction.FFT.FFTFeatures import obtain_FFT_features_labels, obtain_TESPAR_A_FFT_features, \
    obtain_concatenate_segments_fft
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import train_test_doa, obtain_features_labels, train_test_doa_check_trials, \
    split_train_test_balance

####### to change for each  classifier this 3 files #################################
from utils.ExtractData import ExtractData
from utils.mark_bursts.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions
from utils.mark_bursts.MarkOutsidersWithBurstsFlags import remove_bursted_trials_when_segment

csv_file = "rf_30_fft_burst_concatenate_segments_deep_medium.csv"
csv_results = "rf_30_averages_fft_burst_concatenate_segments_deep_medium.csv"
# open file to write the indices of  each splitting
indexes_file = "rf_30_indexes_fft_concatenate_seg_dm.txt"
write_file = open(indexes_file, "w")

# how many models to train a for a channel-segment pair
run_nr = 10

# # once per filter hereee
channels_range = 31
all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
                31, 32]
segments = [['spontaneous',   'stimulus']]
# segments = ['spontaneous', 'stimulus']

# data frame that keeps all runs for all channels, that will be added to .csv file
column_names = ['channel', 'segment', 'accuracy', 'f1-score']
df_all = DataFrame(columns=column_names)
df_all.to_csv(csv_file, mode='a', header=True)

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')
mark_bursts_regions(doas)
#
remove_bursted_trials_when_segment(doas)

'''
for calculating the average acc or af1-score
we need
dictionary to keep array of 30 values for 3 segments for 30 channels
'''
accuracies = [[[] for i in range(channels_range - 1)] for j in range(len(segments))]
f1scores = [[[] for i in range(channels_range - 1)] for j in range(len(segments))]

for run in range(run_nr):
    # firstly split the input into train test
    doas_train, doas_test = train_test_doa_remake_balanced(doas)
    # np.savetxt(write_file, np.array(ind_test), fmt="%s", newline=' ')
    # write_file.write('\n')

    for ind_segment, segment in enumerate(segments):
        for channel in range(len(all_channels)):
            print("start running for channel " + str(channel) + '\n')

            # SplitData(self, doas, channels, levels, segment, orientation):
            train_data = ExtractData(doas_train, [all_channels[channel]], [ 'medium','deep'], ['spontaneous', 'stimulus'], ['all'])
            test_data = ExtractData(doas_test, [all_channels[channel]], ['medium', 'deep'], ['spontaneous', 'stimulus'], ['all'])

            X_train, y_train = obtain_concatenate_segments_fft(train_data)
            x_test, y_test = obtain_concatenate_segments_fft(test_data)

            model = RandomForestClassifier(n_estimators=5000, max_depth=5, min_samples_split=5, min_samples_leaf=10)
            model.fit(X_train, y_train)
            predictions = model.predict(x_test)

            report = classification_report(y_test, predictions, output_dict=True)

            acc = report['accuracy']
            f1sc = report['weighted avg']['f1-score']
            accuracies[ind_segment][channel - 1].append(acc)
            f1scores[ind_segment][channel - 1].append(f1sc)

            # calculate and write the mean  and std_dev of the average & f1-score
            df_all = df_all.append({'channel': all_channels[channel], 'segment': 'spont&stim', 'accuracy': acc, 'f1-score': f1sc},
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
    for channel in range(len(all_channels)):
        acc_avr = np.mean(np.array(accuracies[ind_segment][channel - 1]))
        acc_std = np.std(np.array(accuracies[ind_segment][channel - 1]))

        f1_avr = np.mean(np.array(f1scores[ind_segment][channel - 1]))
        f1_std = np.std(np.array(f1scores[ind_segment][channel - 1]))
        df_results = df_results.append({'channel': all_channels[channel], 'segment': segment, 'acc avr': acc_avr,
                                        'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
                                       ignore_index=True)

df_results.to_csv(csv_results, mode='a', header=False)
