'''
    script to run SVM with Encoding that ignores symbols that intersect bursting regions
'''
import numpy as np
from pandas import DataFrame
from sklearn.metrics import classification_report
from sklearn.svm import SVC

from feature_extraction.TESPAR.EncodingCheckBursts import EncodingCheckBursts
from input_reader.InitDataSetWithBurstsFlags import InitDataSetWithBurstsFlags
from utils.DataSpliting import train_test_doa_check_trials, obtain_features_labels_with_bursts_flags
from utils.MarkOutsidersWithBurstsFlags import mark_outsiders
from utils.SplitDataWithBurstsFlags import SplitDataWithBurstsFlags

csv_results = "svm_with_bursts_flags.csv"

# how many models to train a for a channel-segment pair
run_nr = 5

channel = 5

# channels = [4, 11, 15]

segments = ['spontaneous', 'stimulus', 'poststimulus']

segment = 'spontaneous'

initialization = InitDataSetWithBurstsFlags()
doas = initialization.get_dataset_as_doas()

# mark_outsiders(doas, max_interbursts_dist=200)

encoding = EncodingCheckBursts('./../../data_to_be_saved/alphabet_3.txt')

accuracies = []
f1scores = []

for run in range(run_nr):
    # firstly split the input into train test
    doas_train, doas_test, ind_test = train_test_doa_check_trials(doas, 0.2)

    print("run " + str(run))

    # SplitData(self, doas, channels, levels, segment, orientation):
    train_data = SplitDataWithBurstsFlags(doas_train, [channel], ['light', 'deep'], [segment], ['all'])
    test_data = SplitDataWithBurstsFlags(doas_test, [channel], ['light', 'deep'], [segment], ['all'])

    X_train, y_train = obtain_features_labels_with_bursts_flags(train_data, encoding)
    x_test, y_test = obtain_features_labels_with_bursts_flags(test_data, encoding)

    model = SVC(gamma="auto")

    model.fit(X_train, y_train)
    predictions = model.predict(x_test)

    report = classification_report(y_test, predictions, output_dict=True)

    acc = report['accuracy']
    f1sc = report['weighted avg']['f1-score']
    accuracies.append(acc)
    f1scores.append(f1sc)

# data frame that keeps avr and std of the runs
columns = ['channel', 'segment', 'runs', 'acc avr', 'acc std_dev', 'f1-sc avr', 'f1-sc std_dev']
df_results = DataFrame(columns=columns)
df_results.to_csv(csv_results, mode='a', header=True)

acc_avr = np.mean(np.array(accuracies))
acc_std = np.std(np.array(accuracies))

f1_avr = np.mean(np.array(f1scores))
f1_std = np.std(np.array(f1scores))

df_results = df_results.append({'channel': channel, 'segment': segment, 'runs': run_nr, 'acc avr': acc_avr,
                                'acc std_dev': acc_std, 'f1-sc avr': f1_avr, 'f1-sc std_dev': f1_std},
                               ignore_index=True)

df_results.to_csv(csv_results, mode='a', header=False)