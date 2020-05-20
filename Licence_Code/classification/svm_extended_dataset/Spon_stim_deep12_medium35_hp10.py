import os
import numpy as np
from pandas import DataFrame
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import obtain_A_features_from_doa, train_test_doa_remake_balanced

csv_file = "svm_deep12_medium35_2segs.csv"
# csv_results = "svm_20_deep12_medium35_2segs_avr.csv"

output_name = "results_svm_deep12_medium35_2segs.txt"
output_file = open(output_name, 'w')

output_file.write("Classify bt 2 levels, affter filtering and without marking bursts 2 may \n")
output_file.write("trained on DEEP2 MEDIUM3 A matrix \n")
output_file.write("tested on DEEP1 MEDIUM5 A matrix \n")
output_file.write("NO TRAIN TEST splitting, results in 50-50 \n")

all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
                31, 32]

segment = 'spon_stim'

# data frame that keeps all runs for all channels, that will be added to .csv file
column_names = ['channel', 'segment', 'accuracy', 'f1-score']
df_all = DataFrame(columns=column_names)
df_all.to_csv(csv_file, mode='a', header=True)

encoding = Encoding('./../../data_to_be_saved/12alphabet5_hp10.txt', no_symbols=12)

data_dir = os.path.join('..', '..')

# TRAIN DATA
levels_train = ['deep2', 'light4']
initialization_train = InitDataSet(current_directory=data_dir, subject_directory="m014",
                                   filtering_directory="classic", levels=levels_train)
doas_train = initialization_train.get_dataset_as_doas()

# TEST DATA
levels_test = ['deep1', 'medium5']
initialization_test = InitDataSet(current_directory=data_dir, subject_directory="m014",
                                  filtering_directory="classic", levels=levels_test)
doas_test = initialization_test.get_dataset_as_doas()

# accuracies = [[] for i in range(len(all_channels))]
# f1scores = [[] for i in range(len(all_channels))]

for chn_ind, channel in enumerate(all_channels):
    print("start running for channel " + str(channel))
    output_file.write(f'####### channel {channel} #########\n')

    # obtain_A_features_from_doa(doas, channel_number, encoding, segments=['spontaneous', 'stimulus'],
    #                                selected_symbols=None):
    X_train, y_train = obtain_A_features_from_doa(doas_train, channel, encoding)
    x_test, y_test = obtain_A_features_from_doa(doas_test, channel, encoding)

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
    # accuracies[chn_ind].append(acc)
    # f1scores[chn_ind].append(f1sc)

    # calculate and write the mean  and std_dev of the average & f1-score
    df_all = df_all.append(
        {'channel': channel, 'segment': segment, 'accuracy': acc, 'f1-score': f1sc}, ignore_index=True)

    # print('debug')
df_all.to_csv(csv_file, mode='a', header=False)
df_all = df_all.iloc[0:0]

output_file.close()
