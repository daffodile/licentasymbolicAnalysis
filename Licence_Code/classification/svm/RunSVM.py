import numpy as np
from pandas import DataFrame
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.svm import SVC

from classification.SplitData import SplitData
from classification.svm.Train_and_Test_TESPAR import splitData
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet

csv_file = "svm_report.csv"
# # once per filter hereee
channels_range = 31
segments = ['spontaneous', 'stimulus', 'poststimulus']
# segments = ['spontaneous', 'stimulus']

# how many models to train a for a channel-segment pair
run_nr = 10

# create the DataFrame that will be added to .csv file
column_names = ['channel', 'segment', 'run', 'accuracy', 'acc avr', 'acc std_dev', 'f1-score',
                'f1-sc avr', 'f1-sc std_dev']
df = DataFrame(columns=column_names)
df.to_csv(csv_file, mode='a', header=True)

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../../data_to_be_saved/alphabet_1_150hz.txt')

for segment in segments:
    for channel in range(1, channels_range):
        print("start running for channel " + str(channel) + ' ' + segment + '\n')

        # SplitData(self, doas, channels, levels, segment, orientation):
        split_data = SplitData(doas, [channel], ['light', 'deep'], [segment], ['all'])

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
            df = df.append({'channel': channel, 'segment': segment, 'run': run, 'accuracy': acc, 'acc avr': '',
                            'acc std_dev': '', 'f1-score': f1sc, 'f1-sc avr': '', 'f1-sc std_dev': ''},
                           ignore_index=True)

            accuracies.append(acc)
            f1scores.append(f1sc)

        # calculate and write the mean  and std_dev of the average & f1-score
        df = df.append({'channel train': '', 'channel test': '', 'segment': '', 'run': '', 'accuracy': '',
                        'acc avr': np.mean(np.array(accuracies)), 'acc std_dev': np.std(np.array(accuracies)),
                        'f1-score': '', 'f1-sc avr': np.mean(np.array(f1scores)),
                        'f1-sc std_dev': np.std(np.array(f1scores))},
                       ignore_index=True)

        df.to_csv(csv_file, mode='a', header=False)
        # empty DataFrame to prepare it for this run
        df = df.iloc[0:0]
        # print('debug')
