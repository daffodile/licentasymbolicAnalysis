import numpy as np
from pandas import DataFrame
from sklearn.metrics import classification_report
from sklearn.svm import SVC

from classification.SplitData import SplitData
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import train_test_doa, obtain_features_labels

csv_results = "svm_inter_channels.csv"

# data frame that keeps avr and std of the runs
columns = ['ch train', 'ch test', 'segment', 'acc avr', 'acc std_dev', 'f1-sc avr', 'f1-sc std_dev']
df_results = DataFrame(columns=columns)
df_results.to_csv(csv_results, mode='a', header=True)

indexes_file = "svm_inter_ch_test_indexes.txt"
write_file = open(indexes_file, "w")

train_channels = [1, 5]  # channels with acc > 0,74    Spontaneous
test_channels = [16, 19]  # channels with acc < 0.68

segment = 'stimulus'
# how many models to train a for a channel-segment pair
run_nr = 3

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../../data_to_be_saved/alphabet_1_150hz.txt')

############################## train on good channel, test on good chnannel ###############################3
accuracies = [[[] for i in range(len(train_channels))] for j in range(len(train_channels))]
f1scores = [[[] for i in range(len(train_channels))] for j in range(len(train_channels))]

write_file.write("good-good spliting \n")
for run in range(run_nr):
    # firstly split the input into train test
    doas_train, doas_test, ind_test = train_test_doa(doas, 0.2)
    np.savetxt(write_file, np.array(ind_test), fmt="%s", newline=' ')
    write_file.write('\n')

    for ind_train, ch_train in enumerate(train_channels):
        for ind_test, ch_test in enumerate(train_channels):
            print("start running for channel " + str(ch_train) + ' and ' + str(ch_test) + ' ' + segment + '\n')

            # SplitData(self, doas, channels, levels, segment, orientation):
            train_data = SplitData(doas_train, [ch_train], ['light', 'deep'], [segment], ['all'])
            test_data = SplitData(doas_test, [ch_test], ['light', 'deep'], [segment], ['all'])

            X_train, y_train = obtain_features_labels(train_data, encoding)
            x_test, y_test = obtain_features_labels(test_data, encoding)

            model = SVC()
            model.fit(X_train, y_train)
            predictions = model.predict(x_test)

            report = classification_report(y_test, predictions, output_dict=True)

            acc = report['accuracy']
            f1sc = report['weighted avg']['f1-score']
            accuracies[ind_train][ind_test].append(acc)
            f1scores[ind_train][ind_test].append(f1sc)

for ind_train, ch_train in enumerate(train_channels):
    for ind_test, ch_test in enumerate(train_channels):
        acc_avr = np.mean(np.array(accuracies[ind_train][ind_test]))
        acc_std = np.std(np.array(accuracies[ind_train][ind_test]))

        f1_avr = np.mean(np.array(f1scores[ind_train][ind_test]))
        f1_std = np.std(np.array(f1scores[ind_train][ind_test]))
        df_results = df_results.append(
            {'ch train': ch_train, 'ch test': ch_test, 'segment': segment, 'acc avr': acc_avr,
             'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
            ignore_index=True)

df_results.to_csv(csv_results, mode='a', header=False)

# empty DataFrame to prepare it for next run
df_results = df_results.iloc[0:0]

############################## train on good channel, test on good chnannel ###############################3
accuracies = [[[] for i in range(len(test_channels))] for j in range(len(train_channels))]
f1scores = [[[] for i in range(len(test_channels))] for j in range(len(train_channels))]

write_file.write("good-bad spliting \n")
for run in range(run_nr):
    # firstly split the input into train test
    doas_train, doas_test, ind_test = train_test_doa(doas, 0.2)
    np.savetxt(write_file, np.array(ind_test), fmt="%s", newline=' ')
    write_file.write('\n')

    for ch_train in train_channels:
        for ch_test in test_channels:
            print("start running for channel " + str(ch_train) + ' and ' + str(ch_test) + ' ' + segment + '\n')

            # SplitData(self, doas, channels, levels, segment, orientation):
            train_data = SplitData(doas_train, [ch_train], ['light', 'deep'], [segment], ['all'])
            test_data = SplitData(doas_test, [ch_test], ['light', 'deep'], [segment], ['all'])

            X_train, y_train = obtain_features_labels(train_data, encoding)
            x_test, y_test = obtain_features_labels(test_data, encoding)

            model = SVC()
            model.fit(X_train, y_train)
            predictions = model.predict(x_test)

            report = classification_report(y_test, predictions, output_dict=True)

            acc = report['accuracy']
            f1sc = report['weighted avg']['f1-score']
            accuracies[ch_train - 1][ch_test - 1].append(acc)
            f1scores[ch_train - 1][ch_test - 1].append(f1sc)

for ind_train, ch_train in enumerate(train_channels):
    for ind_test, ch_test in enumerate(test_channels):
        acc_avr = np.mean(np.array(accuracies[ind_train][ind_test]))
        acc_std = np.std(np.array(accuracies[ind_train][ind_test]))

        f1_avr = np.mean(np.array(f1scores[ind_train][ind_test]))
        f1_std = np.std(np.array(f1scores[ind_train][ind_test]))
        df_results = df_results.append(
            {'ch train': ch_train, 'ch test': ch_test, 'segment': segment, 'acc avr': acc_avr,
             'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
            ignore_index=True)

df_results.to_csv(csv_results, mode='a', header=False)

# empty DataFrame to prepare it for next run
df_results = df_results.iloc[0:0]

write_file.close()
