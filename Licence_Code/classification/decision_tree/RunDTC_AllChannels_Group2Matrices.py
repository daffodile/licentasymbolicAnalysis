import numpy as np
from pandas import DataFrame
from sklearn.metrics import classification_report
from sklearn.tree import DecisionTreeClassifier

from classification.decision_tree.SplitData_Old import SplitData
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet

####### to change for each  classifier this 3 files #################################
from utils.DataSpliting import train_test_doa_check_trials, obtain_features_labels

csv_file = "dtc_30_all_test.csv"
csv_results = "dtc_30_avg_all_test.csv"
# open file to write the indices of  each splitting
indexes_file = "dtc_30_avg_all_test.txt"
write_file = open(indexes_file, "w")

# how many models to train a for a channel-segment pair
run_nr = 10

# # once per filter hereee
channels_range = 31
all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
                31, 32]

# segments = ['spontaneous', 'stimulus', 'poststimulus']
segments = ['spontaneous', 'stimulus']

# data frame that keeps all runs for all channels, that will be added to .csv file
column_names = ['channel', 'segment', 'accuracy', 'f1-score']
df_all = DataFrame(columns=column_names)
df_all.to_csv(csv_file, mode='a', header=True)

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')

'''
for calculating the average acc or af1-score
we need
dictionary to keep array of 30 values for 3 segments for 30 channels
'''
accuracies = [[] for i in range(channels_range - 1) for j in range(1)]
f1scores = [[] for i in range(channels_range - 1) for j in range(1)]

for run in range(run_nr):
    print('************************RUN ' + str(run) + '************************')
    # firstly split the input into train test
    doas_train, doas_test, ind_test = train_test_doa_check_trials(doas, 0.2)
    np.savetxt(write_file, np.array(ind_test), fmt="%s", newline=' ')
    write_file.write('\n')

    # for ind_segment, segment in enumerate(segments):
    for ind_channel, channel in enumerate(all_channels):
        print("start running for channel " + str(channel) + '\n')

        # SplitData(self, doas, channels, levels, segment, orientation):
        train_data = SplitData(doas_train, [channel], ['light', 'deep'], segments, ['all'])
        test_data = SplitData(doas_test, [channel], ['light', 'deep'], segments, ['all'])

        X_train, y_train = obtain_features_labels(train_data, encoding, 32)
        x_test, y_test = obtain_features_labels(test_data, encoding, 32)

        model = DecisionTreeClassifier(random_state=99, criterion='gini', max_depth=2)
        model.fit(X_train, y_train)
        predictions = model.predict(x_test)

        report = classification_report(y_test, predictions, output_dict=True)

        acc = report['accuracy']
        f1sc = report['weighted avg']['f1-score']
        accuracies[ind_channel].append(acc)
        f1scores[ind_channel].append(f1sc)

        # calculate and write the mean  and std_dev of the average & f1-score
        df_all = df_all.append(
            {'channel': channel, 'segment': segments[0] + '+' + segments[1], 'accuracy': acc,
             'f1-score': f1sc},
            ignore_index=True)

    # print('debug')
    df_all.to_csv(csv_file, mode='a', header=False)
    df_all = df_all.iloc[0:0]

write_file.close()

# data frame that keeps avr and std of the runs
columns = ['channel', 'segment', 'acc avr', 'acc std_dev', 'f1-sc avr', 'f1-sc std_dev']
df_results = DataFrame(columns=columns)
df_results.to_csv(csv_results, mode='a', header=True)

# for ind_segment, segment in enumerate(segments):
for channel in range(len(all_channels)):
    acc_avr = np.mean(np.array(accuracies[channel]))
    acc_std = np.std(np.array(accuracies[channel]))

    f1_avr = np.mean(np.array(f1scores))
    f1_std = np.std(np.array(f1scores[channel]))
    df_results = df_results.append(
        {'channel': all_channels[channel], 'segment': segments[0] + '+' + segments[1], 'acc avr': acc_avr,
         'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
        ignore_index=True)

df_results.to_csv(csv_results, mode='a', header=False)
