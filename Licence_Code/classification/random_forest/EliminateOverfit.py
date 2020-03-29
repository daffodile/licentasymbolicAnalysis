import numpy as np
import pandas as pd
from matplotlib.pyplot import hist
from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectKBest, f_classif, SelectFromModel, RFE
from sklearn.metrics import classification_report
from matplotlib import pyplot as plt
from classification.SplitData import SplitData
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import train_test_doa, obtain_features_labels

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../../data_to_be_saved/alphabet_1_150hz.txt')

doas_train, doas_test, ind_test = train_test_doa(doas, 0.2)

good_channels_stim = [1, 2, 5, 6, 8]
good_channels_spont = [1, 3, 5, 12, 14]

run_nr = 5

channel = 5
segment = 'stimulus'

print('test for overfitting RF 0.2')

for run in range(run_nr):
    # firstly split the input into train test
    doas_train, doas_test, ind_test = train_test_doa(doas, 0.2)
    #
    print()

    train_data = SplitData(doas_train, [channel], ['light', 'deep'], [segment], ['all'])
    test_data = SplitData(doas_test, [channel], ['light', 'deep'], [segment], ['all'])

    X_train, y_train = obtain_features_labels(train_data, encoding)
    x_test, y_test = obtain_features_labels(test_data, encoding)

    #classify with parameters tunning
    model = RandomForestClassifier(n_estimators=5000,max_depth=5, min_samples_split=5,  min_samples_leaf=10)
    model.fit(X_train, y_train)
    predictions_train = model.predict(X_train)
    predictions_test = model.predict(x_test)

    report_train = classification_report(y_train, predictions_train, output_dict=True)
    report_test = classification_report(y_test, predictions_test, output_dict=True)
    #end

    #classify with feature selection

    # print("classify normal 800 features")
    # model = RandomForestClassifier(n_estimators=5000, max_features=800, max_depth=5, min_samples_leaf=10)
    # model.fit(X_train, y_train)
    # sfm = SelectFromModel(model, max_features=500)
    # # Train the selector
    # sfm.fit(X_train, y_train)
    #
    # X_important_train = sfm.transform(X_train)
    # X_important_test = sfm.transform(x_test)
    #
    # clf_important = RandomForestClassifier(n_estimators=5000,  max_depth=5,min_samples_leaf=10)
    #
    # # Train the new classifier on the new dataset containing the most important features
    # clf_important.fit(X_important_train, y_train)
    #
    # predictions_train = clf_important.predict(X_important_train)
    # predictions_test = clf_important.predict(X_important_test)
    #
    # report_train = classification_report(y_train, predictions_train, output_dict=True)
    # report_test = classification_report(y_test, predictions_test, output_dict=True)
    #end

    #classify with Recursive Feature Elimination
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
    #end

    acc_train = report_train['accuracy']
    f1sc_train = report_train['weighted avg']['f1-score']

    acc_test = report_test['accuracy']
    f1sc_test = report_test['weighted avg']['f1-score']

    print("accuracy train " + str(acc_train) + ' vs ' + str(acc_test) + ' test')
    print("f1-score train " + str(f1sc_train) + ' vs ' + str(f1sc_test) + ' test')
