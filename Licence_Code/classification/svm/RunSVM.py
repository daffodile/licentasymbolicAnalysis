import numpy as np
from pandas import DataFrame
from sklearn.metrics import classification_report
from sklearn.svm import SVC

from tests.Classifiers.SplitData import SplitData
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import train_test_doa, obtain_features_labels

####### to change for each  classifier this 3 files #################################
csv_file = "svm_30_all.csv"
csv_results = "svm_30_averages.csv"
# open file to write the indices of  each splitting
indexes_file = "svm_30_test_indexes.txt"
write_file = open(indexes_file, "w")

# how many models to train a for a channel-segment pair
run_nr = 30

# # once per filter hereee
channels_range = 31

segments = ['spontaneous', 'stimulus', 'poststimulus']
# segments = ['spontaneous', 'stimulus']

# data frame that keeps all runs for all channels, that will be added to .csv file
column_names = ['channel', 'segment', 'accuracy', 'f1-score']
df_all = DataFrame(columns=column_names)
df_all.to_csv(csv_file, mode='a', header=True)

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../../data_to_be_saved/m014_classic_alphabet_3.txt')

'''
for calculating the average acc or af1-score
we need
dictionary to keep array of 30 values for 3 segments for 30 channels
'''
accuracies = [[[] for i in range(channels_range - 1)] for j in range(len(segments))]
f1scores = [[[] for i in range(channels_range - 1)] for j in range(len(segments))]

for run in range(run_nr):
    # firstly split the input into train test
    doas_train, doas_test, ind_test = train_test_doa(doas, 0.2)
    np.savetxt(write_file, np.array(ind_test), fmt="%s", newline=' ')
    write_file.write('\n')

    for ind_segment, segment in enumerate(segments):
        for channel in range(1, channels_range):
            print("start running for channel " + str(channel) + ' ' + segment + '\n')

            # SplitData(self, doas, channels, levels, segment, orientation):
            train_data = SplitData(doas_train, [channel], ['light', 'deep'], [segment], ['all'])
            test_data = SplitData(doas_test, [channel], ['light', 'deep'], [segment], ['all'])

            X_train, y_train = obtain_features_labels(train_data, encoding)
            x_test, y_test = obtain_features_labels(test_data, encoding)

            model = SVC()
            model.fit(X_train, y_train)
            predictions = model.predict(x_test)

            report = classification_report(y_test, predictions, output_dict=True)

            acc = report['accuracy']
            f1sc = report['weighted avg']['f1-score']
            accuracies[ind_segment][channel - 1].append(acc)
            f1scores[ind_segment][channel - 1].append(f1sc)

            # calculate and write the mean  and std_dev of the average & f1-score
            df_all = df_all.append({'channel': channel, 'segment': segment, 'accuracy': acc, 'f1-score': f1sc},
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
    for channel in range(1, channels_range):
        acc_avr = np.mean(np.array(accuracies[ind_segment][channel - 1]))
        acc_std = np.std(np.array(accuracies[ind_segment][channel - 1]))

        f1_avr = np.mean(np.array(f1scores[ind_segment][channel - 1]))
        f1_std = np.std(np.array(f1scores[ind_segment][channel - 1]))
        df_results = df_results.append({'channel': channel, 'segment': segment, 'acc avr': acc_avr,
                                        'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
                                       ignore_index=True)

df_results.to_csv(csv_results, mode='a', header=False)
