import numpy as np
from pandas import DataFrame
from sklearn.metrics import classification_report
from sklearn.svm import SVC

from classification.SplitData import SplitData
from classification.svm.Train_and_Test_TESPAR import splitData
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import train_test_doa, obtain_features_labels

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

# data frame that keeps all runs for all channels, that will be added to .csv file
column_names = ['channel', 'segment', 'accuracy', 'f1-score']
df_all = DataFrame(columns=column_names)
df_all.to_csv(csv_file, mode='a', header=True)

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../../data_to_be_saved/alphabet_1_150hz.txt')

for run in range(run_nr):
    # firstly split the input into train test
    doas_train, doas_test, ind_test = train_test_doa(doas, 0.2)
    np.savetxt(indexes_file, np.array(ind_test), fmt="%s", newline=' ')

    for segment in segments:
        for channel in range(1, channels_range):
            print("start running for channel " + str(channel) + ' ' + segment + '\n')

            # SplitData(self, doas, channels, levels, segment, orientation):
            train_data = SplitData(doas_train, [channel], ['light', 'deep'], [segment], ['all'])
            test_data = SplitData(doas_test, [channel], ['light', 'deep'], [segment], ['all'])

            x_train, y_train = obtain_features_labels(train_data, encoding)
            x_test, y_test = obtain_features_labels(test_data, encoding)

            ...
            to
            be
            continued
            ....

            # save the accuracy and f1-score for all the run
            accuracies = []
            f1scores = []

            for run in range(run_nr):
                # divide the input into train-test random slides
                X_train, x_test, y_train, y_test = splitData(split_data, encoding, 0.2)

                model = SVC()
                model.fit(X_train, y_train)
                predictions = model.predict(x_test)

                report = classification_report(y_test, predictions, output_dict=True)
                acc = report['accuracy']
                f1sc = report['weighted avg']['f1-score']
                accuracies.append(acc)
                f1scores.append(f1sc)

            # calculate and write the mean  and std_dev of the average & f1-score
            df = df.append({'channel': channel, 'segment': segment, 'accuracy': '',
                            'acc avr': np.mean(np.array(accuracies)), 'acc std_dev': np.std(np.array(accuracies)),
                            'f1-score': '', 'f1-sc avr': np.mean(np.array(f1scores)),
                            'f1-sc std_dev': np.std(np.array(f1scores))},
                           ignore_index=True)

            # df.to_csv(csv_file, mode='a', header=False)
            # print('debug')

    df.to_csv(csv_file, mode='a', header=True)

write_file.close()
