'''
SCRIPT TO SEE DIFFERENCE WITHOUT BURSTS
'''
from pandas import DataFrame, np
from sklearn.metrics import classification_report
from sklearn.svm import SVC

from tests.Classifiers.SplitData import SplitData
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import train_test_doa, obtain_features_labels

################## file to save ###########################
csv_file = "svm_bursts_all.csv"
csv_results = "svm_bursts_avr.csv"

# data frame that keeps all runs for all channels, that will be added to .csv file
column_names = ['bursts', 'channel', 'segment', 'accuracy', 'f1-score']
df_all = DataFrame(columns=column_names)
df_all.to_csv(csv_file, mode='a', header=True)

# data frame that keeps avr and std of the runs
columns = ['bursts', 'channel', 'segment', 'acc avr', 'acc std_dev', 'f1-sc avr', 'f1-sc std_dev']
df_results = DataFrame(columns=columns)
df_results.to_csv(csv_results, mode='a', header=True)

# how many models to train a for a channel-segment pair
run_nr = 30

intervals = [[], [2], [1, 2]]
bursts = ['all', 'no_2', 'no1_2']

channel = 1
segment = 'spontaneous'

encoding = Encoding('./../../data_to_be_saved/m014_classic_alphabet_3.txt')

print('SVM 0.2 seg=' + str(segment) + ' ch=' + str(segment))

for ind_interval, interval in enumerate(intervals):

    print('interval= ' + str(interval))

    accuracies = []
    f1scores = []

    initialization = InitDataSet(trials_to_skip=interval)
    doas = initialization.get_dataset_as_doas()

    for run in range(run_nr):
        # firstly split the input into train test
        doas_train, doas_test, ind_test = train_test_doa(doas, 0.2)
        print('lengths: train deep {}, light {}'.format(len(doas_train[0].channels[0].trials),
                                                        len(doas_train[1].channels[0].trials)))
        print('lengths: test deep {}, light {}'.format(len(doas_test[0].channels[0].trials),
                                                       len(doas_test[1].channels[0].trials)))
        #
        print("run: {}".format(run))

        train_data = SplitData(doas_train, [channel], ['light', 'deep'], [segment])
        test_data = SplitData(doas_test, [channel], ['light', 'deep'], [segment])

        X_train, y_train = obtain_features_labels(train_data, encoding)
        x_test, y_test = obtain_features_labels(test_data, encoding)

        model = SVC(gamma="auto")

        model.fit(X_train, y_train)
        predictions_train = model.predict(X_train)
        # print('train subset')
        # print(confusion_matrix(y_train, predictions_train))
        # print(classification_report(y_train, predictions_train))

        predictions_test = model.predict(x_test)
        # print('test subset')
        # print(confusion_matrix(y_test, predictions_test))
        # print(classification_report(y_test, predictions_test))

        report_train = classification_report(y_train, predictions_train, output_dict=True)
        report_test = classification_report(y_test, predictions_test, output_dict=True)

        acc_train = report_train['accuracy']
        f1sc_train = report_train['weighted avg']['f1-score']

        acc_test = report_test['accuracy']
        f1sc_test = report_test['weighted avg']['f1-score']

        accuracies.append(acc_test)
        f1scores.append(f1sc_test)

        df_all = df_all.append(
            {'bursts': bursts[ind_interval], 'channel': channel, 'segment': segment, 'accuracy': acc_test,
             'f1-score': f1sc_test},
            ignore_index=True)

        print(" accuracy train " + str(acc_train) + ' vs ' + str(acc_test) + ' test')
        print("f1-score train " + str(f1sc_train) + ' vs ' + str(f1sc_test) + ' test')

    df_all.to_csv(csv_file, mode='a', header=False)
    df_all = df_all.iloc[0:0]

    acc_avr = np.mean(np.array(accuracies))
    acc_std = np.std(np.array(accuracies))

    f1_avr = np.mean(np.array(f1scores))
    f1_std = np.std(np.array(f1scores))
    df_results = df_results.append(
        {'bursts': bursts[ind_interval], 'channel': channel, 'segment': segment, 'acc avr': acc_avr,
         'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
        ignore_index=True)

df_results.to_csv(csv_results, mode='a', header=False)
