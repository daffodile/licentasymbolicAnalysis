from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from classification.SplitData import SplitData
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import train_test_doa, obtain_features_labels

# how many models to train a for a channel-segment pair
run_nr = 10

channel = 14
segment = 'spontaneous'

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../../data_to_be_saved/alphabet_1_150hz.txt')

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

    model = RandomForestClassifier(n_estimators=100)
    model.fit(X_train, y_train)
    predictions_train = model.predict(X_train)
    predictions_test = model.predict(x_test)

    report_train = classification_report(y_train, predictions_train, output_dict=True)
    report_test = classification_report(y_test, predictions_test, output_dict=True)

    acc_train = report_train['accuracy']
    f1sc_train = report_train['weighted avg']['f1-score']

    acc_test = report_test['accuracy']
    f1sc_test = report_test['weighted avg']['f1-score']

    print("accuracy train " + str(acc_train) + ' vs ' + str(acc_test) + ' test')
    print("f1-score train " + str(f1sc_train) + ' vs ' + str(f1sc_test) + ' test')


print('test for overfitting DTC 0.2')
for run in range(run_nr):
    # firstly split the input into train test
    doas_train, doas_test, ind_test = train_test_doa(doas, 0.2)
    #
    print()

    train_data = SplitData(doas_train, [channel], ['light', 'deep'], [segment], ['all'])
    test_data = SplitData(doas_test, [channel], ['light', 'deep'], [segment], ['all'])

    X_train, y_train = obtain_features_labels(train_data, encoding)
    x_test, y_test = obtain_features_labels(test_data, encoding)

    model = DecisionTreeClassifier()
    model.fit(X_train, y_train)
    predictions_train = model.predict(X_train)
    predictions_test = model.predict(x_test)

    report_train = classification_report(y_train, predictions_train, output_dict=True)
    report_test = classification_report(y_test, predictions_test, output_dict=True)

    acc_train = report_train['accuracy']
    f1sc_train = report_train['weighted avg']['f1-score']

    acc_test = report_test['accuracy']
    f1sc_test = report_test['weighted avg']['f1-score']

    print("accuracy train " + str(acc_train) + ' vs ' + str(acc_test) + ' test')
    print("f1-score train " + str(f1sc_train) + ' vs ' + str(f1sc_test) + ' test')
