import numpy as np
from pandas import DataFrame
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

from tests.Classifiers.SplitData import SplitData
from classification.random_forest.Train_and_Test_TESPAR import obtain_concatenate_segments
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet


####### to change for each  classifier this 3 files #################################
from utils.DataSpliting import train_test_doa

csv_file = "rf_30_all_3levels.csv"
# open file to write the indices of  each splitting
indexes_file = "rf_30_3lvl_test_indexes.txt"
write_file = open(indexes_file, "w")

# how many models to train a for a channel-segment pair
run_nr = 30

# # once per filter hereee
channels_range = 6
good_channels_stim = [1, 2, 5, 6, 8]
good_channels_spont = [1, 3, 5, 12, 14]


segments = ['spontaneous', 'stimulus']
# segments = ['spontaneous', 'stimulus']

# data frame that keeps all runs for all channels, that will be added to .csv file
column_names = ['channel', 'segment', 'accuracy', 'f1-score']
df_all = DataFrame(columns=column_names)
df_all.to_csv(csv_file, mode='a', header=True)

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../../data_to_be_saved/alphabet_1_150hz.txt')

'''
for calculating the average acc or af1-score
we need
dictionary to keep array of 30 values for 3 segments for 30 channels
'''


for run in range(run_nr):
    # firstly split the input into train test
    doas_train, doas_test, ind_test = train_test_doa(doas, 0.2)
    np.savetxt(write_file, np.array(ind_test), fmt="%s", newline=' ')
    write_file.write('\n')

    for channel in good_channels_stim:
            print("start running for channel " + str(channel) + ' ' + str(segments) + '\n')

            # SplitData(self, doas, channels, levels, segment, orientation):
            train_data = SplitData(doas_train, [channel], ['light', 'deep'], segments, ['all'])
            test_data = SplitData(doas_test, [channel], ['light', 'deep'], segments, ['all'])

            X_train, y_train = obtain_concatenate_segments(train_data, encoding)
            x_test, y_test = obtain_concatenate_segments(test_data, encoding)

            model = RandomForestClassifier(n_estimators=5000, max_depth=5, min_samples_split=5, min_samples_leaf=10)
            model.fit(X_train, y_train)
            # sfm = SelectFromModel(model, threshold=-np.inf, max_features=800)
            # # Train the selector
            # sfm.fit(X_train, y_train)
            #
            # X_important_train = sfm.transform(X_train)
            # X_important_test = sfm.transform(x_test)
            #
            # clf_important = RandomForestClassifier(n_estimators=5000, max_depth=5, min_samples_leaf=10)
            #
            # # Train the new classifier on the new dataset containing the most important features
            # clf_important.fit(X_important_train, y_train)
            predictions = model.predict(x_test)

            report = classification_report(y_test, predictions, output_dict=True)

            acc = report['accuracy']
            f1sc = report['weighted avg']['f1-score']


            # calculate and write the mean  and std_dev of the average & f1-score
            df_all = df_all.append({'channel': channel, 'segment': 'spontaneous&stimulus', 'accuracy': acc, 'f1-score': f1sc},
                                   ignore_index=True)

            # print('debug')
    df_all.to_csv(csv_file, mode='a', header=False)
    df_all = df_all.iloc[0:0]

write_file.close()











