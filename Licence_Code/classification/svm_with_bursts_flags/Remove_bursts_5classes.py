import os
import numpy as np
from pandas import DataFrame
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC
from feature_extraction.TESPAR.EncodingCheckBursts import EncodingCheckBursts
from input_reader.InitDataSet import InitDataSet
from input_reader.InitDataSetWithBurstsFlags import InitDataSetWithBurstsFlags
from utils.DataSpliting import obtain_A_features_from_doa, train_test_doa_balanced_on_train_on_test, \
    obtain_A_features_from_doa_check_bursts
from utils.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions
from utils.MarkOutsidersWithBurstsFlags import remove_bursted_trials_when_segment

csv_file = "svm_5classes_M014_remove_bursts.csv"
csv_results = "svm_5classes_M014_remove_bursts_avr.csv"

output_name = "classification_svm_5classes_M014_remove_bursts.txt"
output_file = open(output_name, 'w')

output_file.write("Classify bt all 5 levels remove bursting trials and  skip symbols\n")
output_file.write(" A matrix alphabet3 most common\n")
output_file.write(
    "train_test_doa_balanced_on_train_on_test 80% for train: 93 trials at a time bc balance on test too \n")

run_nr = 20

all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
                31, 32]

segment = 'spon_stim'

# data frame that keeps all runs for all channels, that will be added to .csv file
column_names = ['channel', 'segment', 'accuracy', 'f1-score']
df_all = DataFrame(columns=column_names)
df_all.to_csv(csv_file, mode='a', header=True)

encoding = EncodingCheckBursts('./../../data_to_be_saved/alphabet_3.txt')

data_dir = os.path.join('..', '..')

levels = ['deep1', 'deep2', 'medium3', 'light4', 'medium5']

# def __init__(self, current_directory, subject_directory, filtering_directory, levels=['deep', 'medium', 'light'], trials_to_skip=None):
initialization = InitDataSetWithBurstsFlags(current_directory=data_dir, subject_directory="m014", filtering_directory="classic",
                             levels=levels)
doas = initialization.get_dataset_as_doas()

mark_bursts_regions(doas)

remove_bursted_trials_when_segment(doas)

accuracies = [[] for i in range(len(all_channels))]
f1scores = [[] for i in range(len(all_channels))]

for run in range(run_nr):
    print('************************RUN ' + str(run) + '************************')
    # firstly split the input into train test
    doas_train, doas_test = train_test_doa_balanced_on_train_on_test(doas)

    for chn_ind, channel in enumerate(all_channels):
        print("start running for channel " + str(channel))
        output_file.write(f'####### run {run} channel {channel} #########\n')

        X_train, y_train = obtain_A_features_from_doa_check_bursts(doas_train, channel, encoding)
        x_test, y_test = obtain_A_features_from_doa_check_bursts(doas_test, channel, encoding)

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

        output_file.write(classification_report(y_test, predictions))
        np.savetxt(output_file, np.array(confusion_matrix(y_test, predictions)), fmt="%s", newline=' ')
        output_file.write('\n')

        acc = report['accuracy']
        f1sc = report['weighted avg']['f1-score']
        accuracies[chn_ind].append(acc)
        f1scores[chn_ind].append(f1sc)

        # calculate and write the mean  and std_dev of the average & f1-score
        df_all = df_all.append(
            {'channel': channel, 'segment': segment, 'accuracy': acc, 'f1-score': f1sc}, ignore_index=True)

        # print('debug')
    df_all.to_csv(csv_file, mode='a', header=False)
    df_all = df_all.iloc[0:0]

output_file.close()

# data frame that keeps avr and std of the runs
columns = ['channel', 'segment', 'acc avr', 'acc std_dev', 'f1-sc avr', 'f1-sc std_dev']
df_results = DataFrame(columns=columns)
df_results.to_csv(csv_results, mode='a', header=True)

for ind_ch, channel in enumerate(all_channels):
    acc_avr = np.mean(np.array(accuracies[ind_ch]))
    acc_std = np.std(np.array(accuracies[ind_ch]))

    f1_avr = np.mean(np.array(f1scores[ind_ch]))
    f1_std = np.std(np.array(f1scores[ind_ch]))
    df_results = df_results.append({'channel': channel, 'segment': segment, 'acc avr': acc_avr,
                                    'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
                                   ignore_index=True)

df_results.to_csv(csv_results, mode='a', header=False)
