import numpy as np
from pandas import DataFrame
from sklearn.metrics import classification_report
from sklearn.svm import SVC

from classification.SplitData import SplitData
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import obtain_features_labels, train_test_doa, train_test_doa_check_trials

'''
    to change  this files
'''
csv_file = "svm_truncate_A25.csv"
csv_results = "svm_truncate_A25_avr.csv"

# how many models to train a for a channel-segment pair
run_nr = 30

# channels = [2, 3, 4, 5, 6, 7, 8, 9, 19, 13]
channels = [3, 5, 6, 7, 13, 15]

segments = ['spontaneous', 'stimulus', 'poststimulus']

# data frame that keeps all runs for all channels, that will be added to .csv file
column_names = ['channel', 'segment', 'accuracy', 'f1-score']
df_all = DataFrame(columns=column_names)
# df_all.to_csv(csv_file, mode='a', header=True)

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()

encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')
# selected_symbols = [10, 15, 20, 25]
selected_symbols = 25

'''
for calculating the average acc or af1-score
we need
dictionary to keep array of 30 values for 3 segments for 30 channels
'''
accuracies = [[[] for i in range(len(channels))] for j in range(len(segments))]
f1scores = [[[] for i in range(len(channels))] for j in range(len(segments))]

for run in range(run_nr):
    # firstly split the input into train test
    doas_train, doas_test, ind_test = train_test_doa_check_trials(doas, 0.2)

    for ind_segment, segment in enumerate(segments):
        for ind_ch, channel in enumerate(channels):
            print("start running for channel " + str(channel) + ' ' + segment + '\n')

            # SplitData(self, doas, channels, levels, segment, orientation):
            train_data = SplitData(doas_train, [channel], ['light', 'deep'], [segment], ['all'])
            test_data = SplitData(doas_test, [channel], ['light', 'deep'], [segment], ['all'])

            X_train, y_train = obtain_features_labels(train_data, encoding, selected_symbols=selected_symbols)
            x_test, y_test = obtain_features_labels(test_data, encoding, selected_symbols=selected_symbols)

            model = SVC(gamma='auto')

            model.fit(X_train, y_train)

            predictions = model.predict(x_test)

            report = classification_report(y_test, predictions, output_dict=True)

            acc = report['accuracy']
            f1sc = report['weighted avg']['f1-score']
            accuracies[ind_segment][ind_ch].append(acc)
            f1scores[ind_segment][ind_ch].append(f1sc)

            # calculate and write the mean  and std_dev of the average & f1-score
            df_all = df_all.append({'channel': channel, 'segment': segment, 'accuracy': acc, 'f1-score': f1sc},
                                   ignore_index=True)

    df_all.to_csv(csv_file, mode='a', header=False)
    df_all = df_all.iloc[0:0]

# data frame that keeps avr and std of the runs
columns = ['channel', 'segment', 'acc avr', 'acc std_dev', 'f1-sc avr', 'f1-sc std_dev']
df_results = DataFrame(columns=columns)
df_results.to_csv(csv_results, mode='a', header=True)

for ind_segment, segment in enumerate(segments):
    for ind_ch, channel in enumerate(channels):
        acc_avr = np.mean(np.array(accuracies[ind_segment][ind_ch]))
        acc_std = np.std(np.array(accuracies[ind_segment][ind_ch]))

        f1_avr = np.mean(np.array(f1scores[ind_segment][ind_ch]))
        f1_std = np.std(np.array(f1scores[ind_segment][ind_ch]))
        df_results = df_results.append({'channel': channel, 'segment': segment, 'acc avr': acc_avr,
                                        'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
                                       ignore_index=True)

df_results.to_csv(csv_results, mode='a', header=False)
