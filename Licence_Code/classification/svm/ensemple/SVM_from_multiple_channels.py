import os
import numpy as np
from pandas import DataFrame
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import train_test_doa_remake_balanced, obtain_A_features_from_doa

csv_file = "svm_classic_deep2_light4.csv"
csv_results = "svm_classic_deep2_light4_avr.csv"

classification_reports = "classification_reports_svm_classic_deep2_light4.txt"
output_classification_reports = open(classification_reports, 'w')

confusion_file = 'confusion_matrix_svm_classic_deep2_light4.txt'
output_confusion_matrix = open(confusion_file, 'w')

output_classification_reports.write(
    "Classify bt DEEP2 and LIGHT4:  classic, no remove no marking \n")
output_classification_reports.write(
    "Get a big dataset from more channels \n")
output_classification_reports.write("spon_stim concatenate A matrix alfabet3 classic\n")
output_classification_reports.write("train_test_doa_remake_balanced 80% for train \n")

run_nr = 20

all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
np.savetxt(output_classification_reports, np.array(all_channels), fmt="%s", newline=' ')

segment = 'spon_stim'

# data frame that keeps all runs for all channels, that will be added to .csv file
column_names = ['channel', 'segment', 'accuracy', 'f1-score']
df_all = DataFrame(columns=column_names)
df_all.to_csv(csv_file, mode='a', header=True)

encoding = Encoding('./../../../data_to_be_saved/alphabet_3.txt')

data_dir = os.path.join('..', '..', '..')

levels = ['deep2', 'light4']
initialization_train = InitDataSet(current_directory=data_dir, subject_directory="m014", filtering_directory="classic",
                                   levels=levels)

doas = initialization_train.get_dataset_as_doas()

accuracies = []
f1scores = []

for run in range(run_nr):
    print('************************RUN ' + str(run) + '************************')
    # firstly split the input into train test
    doas_train, doas_test = train_test_doa_remake_balanced(doas)

    # empty data frame for each run in order to add data from channels
    X_train = DataFrame()
    y_train = []
    x_test = DataFrame()
    y_test = []

    for chn_ind, channel in enumerate(all_channels):
        X_train_ch, y_train_ch = obtain_A_features_from_doa(doas_train, channel, encoding)
        x_test_ch, y_test_ch = obtain_A_features_from_doa(doas_test, channel, encoding)

        X_train = X_train.append(X_train_ch, ignore_index=True)
        y_train.extend(y_train_ch)

        x_test = x_test.append(x_test_ch, ignore_index=True)
        y_test.extend(y_test_ch)

    model = SVC(gamma="auto")

    model.fit(X_train, y_train)

    # just for overfitting
    report_train = classification_report(y_train, model.predict(X_train), output_dict=True)
    acc_train = report_train['accuracy']
    print(f'predict on train  acc {acc_train}')

    predictions = model.predict(x_test)

    report = classification_report(y_test, predictions, output_dict=True)

    print(classification_report(y_test, predictions))
    print(confusion_matrix(y_test, predictions))

    output_classification_reports.write(f'{run}\n')
    output_classification_reports.write(classification_report(y_test, predictions))
    output_classification_reports.write('\n')

    output_confusion_matrix.write(f'{run}\n')
    np.savetxt(output_confusion_matrix, np.array(confusion_matrix(y_test, predictions)), fmt="%s", newline=' ')
    output_confusion_matrix.write('\n')

    acc = report['accuracy']
    f1sc = report['weighted avg']['f1-score']
    accuracies.append(acc)
    f1scores.append(f1sc)

    # calculate and write the mean  and std_dev of the average & f1-score
    df_all = df_all.append(
        {'channel': 'all', 'segment': segment, 'accuracy': acc, 'f1-score': f1sc}, ignore_index=True)

    # print('debug')

df_all.to_csv(csv_file, mode='a', header=False)
df_all = df_all.iloc[0:0]

output_classification_reports.close()
output_confusion_matrix.close()

# data frame that keeps avr and std of the runs
columns = ['channel', 'segment', 'acc avr', 'acc std_dev', 'f1-sc avr', 'f1-sc std_dev']
df_results = DataFrame(columns=columns)
df_results.to_csv(csv_results, mode='a', header=True)

acc_avr = np.mean(np.array(accuracies))
acc_std = np.std(np.array(accuracies))

f1_avr = np.mean(np.array(f1scores))
f1_std = np.std(np.array(f1scores))
df_results = df_results.append({'channel': channel, 'segment': segment, 'acc avr': acc_avr,
                                'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
                               ignore_index=True)
df_results.to_csv(csv_results, mode='a', header=False)
