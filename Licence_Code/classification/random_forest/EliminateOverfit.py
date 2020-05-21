from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel
from sklearn.metrics import classification_report, confusion_matrix

from classification.random_forest.Utils_classification import train_test_doa_remake_balanced
from feature_extraction.FFT.FFTFeatures import obtain_FFT_features_labels, obtain_TESPAR_A_FFT_features, \
    obtain_TESPAR_S_FFT_features, obtain_concatenate_segments_FFT_TESPAR_A, obtain_concatenate_segments_fft
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import train_test_doa, obtain_features_labels, obtain_S_TESPAR_features, \
    train_test_doa_check_trials, split_train_test_balance
from utils.ExtractData import ExtractData
from utils.mark_bursts.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions
from utils.mark_bursts.MarkOutsidersWithBurstsFlags import remove_bursted_trials_when_segment

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../../data_to_be_saved/m014_classic_alphabet_3.txt')
# SAU 1 SAU 2
#  1 th
# mark_bursts_regions_one_threshold(doas)
#
# # diff th
mark_bursts_regions(doas)
#
remove_bursted_trials_when_segment(doas)

good_channels_stim = [1, 2, 5, 6, 8]
good_channels_spont = [1, 3, 5, 12, 14]

run_nr = 5

channel = 2
segment = 'stimulus'

print('test for overfitting RF 0.2')

for run in range(run_nr):
    # firstly split the input into train test
    doas_train, doas_test = train_test_doa_remake_balanced(doas)
    #
    print()

    train_data = ExtractData(doas_train, [2], ['light', 'medium', 'deep'], ['spontaneous', 'stimulus'], ['all'])
    test_data = ExtractData(doas_test, [2], ['light', 'medium', 'deep'], ['spontaneous', 'stimulus'], ['all'])

    X_train, y_train = obtain_concatenate_segments_fft(train_data)
    x_test, y_test = obtain_concatenate_segments_fft(test_data)

    # classify with parameters tunning
    model = RandomForestClassifier(n_estimators=5000, max_depth=5, min_samples_split=5, min_samples_leaf=10)
    # model = RandomForestClassifier()
    model.fit(X_train, y_train)
    predictions_train = model.predict(X_train)
    predictions_test = model.predict(x_test)

    report_train = classification_report(y_train, predictions_train, output_dict=True)
    report_test = classification_report(y_test, predictions_test, output_dict=True)
    # end

    # classify with feature selection

    # print("classify normal 800 features")
    # # model = RandomForestClassifier(n_estimators=5000, max_depth=5, min_samples_leaf=10)
    # # model.fit(X_train, y_train)
    # sfm = SelectFromModel(model, max_features=45)
    # # Train the selector
    # sfm.fit(X_train, y_train)
    # #
    # X_important_train = sfm.transform(X_train)
    # X_important_test = sfm.transform(x_test)
    #
    # clf_important = RandomForestClassifier(n_estimators=5000, max_depth=5, min_samples_split=5, min_samples_leaf=10)
    # #
    # # # Train the new classifier on the new dataset containing the most important features
    # clf_important.fit(X_important_train, y_train)
    # #
    # predictions_train2 = clf_important.predict(X_important_train)
    # predictions_test2 = clf_important.predict(X_important_test)
    #
    #
    # report_train2= classification_report(y_train, predictions_train2, output_dict=True)
    # report_test2 = classification_report(y_test, predictions_test2, output_dict=True)

    # end

    # classify with Recursive Feature Elimination
    # model = RandomForestClassifier(n_estimators=1000)
    # model.fit(X_train, y_train)
    # # print("classify with best 800 features")
    # rfe_selector = RFE(model, 800)
    # rfe_selector = rfe_selector.fit(X_train, y_train)
    #
    # X_important_train = rfe_selector.transform(X_train)
    # X_important_test = rfe_selector.transform(x_test)
    #
    # clf_important = RandomForestClassifier(n_estimators=5000, max_depth=5, min_samples_leaf=10)
    #
    # # Train the new classifier on the new dataset containing the most important features
    # clf_important.fit(X_important_train, y_train)
    #
    # predictions_train = clf_important.predict(X_important_train)
    # predictions_test = clf_important.predict(X_important_test)
    #
    # report_train = classification_report(y_train, predictions_train, output_dict=True)
    # report_test = classification_report(y_test, predictions_test, output_dict=True)
    # end

    acc_train = report_train['accuracy']
    f1sc_train = report_train['weighted avg']['f1-score']

    acc_test = report_test['accuracy']
    f1sc_test = report_test['weighted avg']['f1-score']

    # acc_test2 = report_test2['accuracy']
    # f1sc_test2 = report_test2['weighted avg']['f1-score']
    #
    # acc_train2 = report_train2['accuracy']
    # f1sc_train2 = report_train2['weighted avg']['f1-score']

    #
    print("accuracy train " + str(acc_train) + ' vs ' + str(acc_test) + ' test')
    print("f1-score train " + str(f1sc_train) + ' vs ' + str(f1sc_test) + ' test')
    #
    # print("accuracy train " + str(acc_train2) + ' vs ' + str(acc_test2) + ' test')
    # print("f1-score train " + str(f1sc_train2) + ' vs ' + str(f1sc_test2) + ' test')

    print('\nClasification report:\n', classification_report(y_test, predictions_test))
    print('\nConfussion matrix:\n', confusion_matrix(y_test, predictions_test))
