import os

import numpy as np
from pandas import DataFrame
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import train_test_doa, obtain_features_labels_from_doa

csv_results = "svm_runs.csv"

# how many models to train a for a channel-segment pair
run_nr = 10
# run_nr = 100

channel = 5

# channels = [4, 11, 15]

segment = 'spontaneous'

data_dir = os.path.join('../..', '..')

initialization = InitDataSet(data_dir=data_dir)
doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../../../data_to_be_saved/alphabet_3.txt')

accuracies = []
f1scores = []

for run in range(run_nr):
    # firstly split the input into train test
    doas_train, doas_test, ind_test = train_test_doa(doas, 0.2)

    print("run " + str(run))

    # SplitData(self, doas, channels, levels, segment, orientation):
    X_train, y_train = obtain_features_labels_from_doa(doas_train, channel, segment, encoding)
    x_test, y_test = obtain_features_labels_from_doa(doas_test, channel, segment, encoding)

    # maybe increases
    model = SVC(gamma=0.0001, C=10.0)

    model.fit(X_train, y_train)
    predictions = model.predict(x_test)

    report = classification_report(y_test, predictions, output_dict=True)
    print(report)
    print(confusion_matrix(y_test, predictions))

    acc = report['accuracy']
    f1sc = report['weighted avg']['f1-score']

    print(f'Accuracy {acc} f-1 score {f1sc}')
    accuracies.append(acc)
    f1scores.append(f1sc)

# data frame that keeps avr and std of the runs
columns = ['channel', 'segment', 'runs', 'acc avr', 'acc std_dev', 'f1-sc avr', 'f1-sc std_dev']
df_results = DataFrame(columns=columns)
# df_results.to_csv(csv_results, mode='a', header=True)

acc_avr = np.mean(np.array(accuracies))
acc_std = np.std(np.array(accuracies))

f1_avr = np.mean(np.array(f1scores))
f1_std = np.std(np.array(f1scores))

df_results = df_results.append({'channel': channel, 'segment': segment, 'runs': run_nr, 'acc avr': acc_avr,
                                'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
                               ignore_index=True)

df_results.to_csv(csv_results, mode='a', header=False)
