from sklearn.ensemble import RandomForestClassifier
from sklearn.feature_selection import SelectFromModel, RFECV, RFE
from sklearn.metrics import classification_report
from sklearn.model_selection import StratifiedKFold
from sklearn.svm import SVC

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import train_test_doa, obtain_features_labels, train_test_doa_check_trials
from utils.ExtractData import ExtractData
import numpy as np

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')


good_channels_stim = [1, 2, 5, 6, 8]
good_channels_spont = [1, 3, 5, 12, 14]

run_nr = 5

channel = 5
segment = 'stimulus'

print('test for overfitting RF 0.2')

for run in range(run_nr):
    # firstly split the input into train test
    # doas_train, doas_test, ind_test = train_test_doa(doas, 0.2)
    doas_train, doas_test, ind_test = train_test_doa_check_trials(doas, 0.2)
    #
    print()

    train_data = ExtractData(doas_train, [channel], ['light', 'deep'], [segment], ['all'])
    test_data = ExtractData(doas_test, [channel], ['light', 'deep'], [segment], ['all'])

    X_train, y_train = obtain_features_labels(train_data, encoding)
    x_test, y_test = obtain_features_labels(test_data, encoding)

    #classify with parameters tunning
    # model = RandomForestClassifier(n_estimators=5000,max_depth=5, min_samples_split=5,  min_samples_leaf=10)
    #
    # model.fit(X_train, y_train)
    #
    # predictions_train = model.predict(X_train)
    # predictions_test = model.predict(x_test)
    #
    # report_train = classification_report(y_train, predictions_train, output_dict=True)
    # report_test = classification_report(y_test, predictions_test, output_dict=True)
    #end

    #classify with feature selection

    print("---------classify normal 800 features---------")
    model = RandomForestClassifier(n_estimators=5000, max_depth=5, min_samples_leaf=10)
    model.fit(X_train, y_train)

    clf = RandomForestClassifier()

    # Train the classifier
    clf.fit(X_train, y_train)
    sfm = SelectFromModel(clf)
    # Train the selector
    sfm.fit(X_train, y_train)
    sfm.get_support()
    selected_feat = X_train.columns[(sfm.get_support())]
    print(len(selected_feat))
    print(selected_feat)

    X_important_train = sfm.transform(X_train)
    X_important_test = sfm.transform(x_test)

    clf_important = RandomForestClassifier(n_estimators=5000,max_depth=5, min_samples_split=5,  min_samples_leaf=10)
    cfl_all_features = RandomForestClassifier(n_estimators=5000,max_depth=5, min_samples_split=5,  min_samples_leaf=10)
    # Train the new classifier on the new dataset containing the most important features
    clf_important.fit(X_important_train, y_train)
    cfl_all_features.fit(X_train, y_train)

    predictions_train = clf_important.predict(X_important_train)
    predictions_test = clf_important.predict(X_important_test)

    predictions_train_all = cfl_all_features.predict(X_train)
    predictions_test_all = cfl_all_features.predict(x_test)

    report_train = classification_report(y_train, predictions_train, output_dict=True)
    report_test = classification_report(y_test, predictions_test, output_dict=True)

    report_train_all = classification_report(y_train, predictions_train_all, output_dict=True)
    report_test_all = classification_report(y_test, predictions_test_all, output_dict=True)
    #end

    #classify with Recursive Feature Elimination
    # model = RandomForestClassifier(n_estimators=1000)
    # model.fit(X_train, y_train)
    # # print("classify with best 800 features")
    # rfe_selector = RFE(model)
    # rfe_selector = rfe_selector.fit(X_train, y_train)
    #
    # X_important_train = rfe_selector.transform(X_train)
    # X_important_test = rfe_selector.transform(x_test)
    #
    # clf_important = RandomForestClassifier(n_estimators=5000,max_depth=5, min_samples_split=5,  min_samples_leaf=10)
    # clf_allF = RandomForestClassifier(n_estimators=5000,max_depth=5, min_samples_split=5,  min_samples_leaf=10)
    #
    # # Train the new classifier on the new dataset containing the most important features
    # clf_important.fit(X_important_train, y_train)
    # clf_allF.fit(X_train, y_train)
    #
    # predictions_train = clf_important.predict(X_important_train)
    # predictions_test = clf_important.predict(X_important_test)
    #
    # predictions_train_all = clf_allF.predict(X_train)
    # predictions_test_all = clf_allF.predict(x_test)
    #
    # report_train = classification_report(y_train, predictions_train, output_dict=True)
    # report_test = classification_report(y_test, predictions_test, output_dict=True)
    #
    # report_train_all = classification_report(y_train, predictions_train_all, output_dict=True)
    # report_test_all = classification_report(y_test, predictions_test_all, output_dict=True)
    #end

    #feature recursive elimination with corss validation
    # Create the RFE object and compute a cross-validated score.
    # svc = SVC(kernel="linear")
    # The "accuracy" scoring is proportional to the number of correct
    # classifications
    # rfecv = RFECV(estimator=RandomForestClassifier(), step=1, cv=StratifiedKFold(5),
    #               scoring='accuracy')
    # rfecv.fit(X_train, y_train)
    #
    # predictions_train = rfecv.predict(X_train)
    # predictions_test = rfecv.predict(x_test)
    #
    # report_train = classification_report(y_train, predictions_train, output_dict=True)
    # report_test = classification_report(y_test, predictions_test, output_dict=True)

    #end

    acc_train = report_train['accuracy']
    f1sc_train = report_train['weighted avg']['f1-score']

    acc_train_all = report_train_all['accuracy']
    f1sc_train_all = report_train_all['weighted avg']['f1-score']

    acc_test = report_test['accuracy']
    f1sc_test = report_test['weighted avg']['f1-score']

    acc_test_all = report_test_all['accuracy']
    f1sc_test_all= report_test_all['weighted avg']['f1-score']

    print("accuracy train " + str(acc_train) + ' vs ' + str(acc_test) + ' test')
    print("f1-score train " + str(f1sc_train) + ' vs ' + str(f1sc_test) + ' test')

    print("accuracy train all features " + str(acc_train_all) + ' vs ' + str(acc_test_all) + ' test')
    print("f1-score train all features" + str(f1sc_train_all) + ' vs ' + str(f1sc_test_all) + ' test')