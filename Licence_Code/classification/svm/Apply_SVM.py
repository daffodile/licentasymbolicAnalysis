'''
SCRIPT TO TEST OVERFITTING
'''

from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC

from classification.SplitData import SplitData
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import train_test_doa, obtain_features_labels

# how many models to train a for a channel-segment pair
run_nr = 10

# channel = 23
channel = 1
segment = 'spontaneous'

initialization = InitDataSet(trials_to_skip=[2])
doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../../data_to_be_saved/alphabet_1_150hz.txt')

print('test for overfitting SVM 0.2 seg=' + str(segment))
for run in range(run_nr):
    # firstly split the input into train test
    doas_train, doas_test, ind_test = train_test_doa(doas, 0.2)
    #
    print(run)

    train_data = SplitData(doas_train, [channel], ['light', 'deep'], [segment], ['all'])
    test_data = SplitData(doas_test, [channel], ['light', 'deep'], [segment], ['all'])

    X_train, y_train = obtain_features_labels(train_data, encoding)
    x_test, y_test = obtain_features_labels(test_data, encoding)

    model = SVC(gamma="auto")

    model.fit(X_train, y_train)
    predictions_train = model.predict(X_train)
    print('train subset')
    print(confusion_matrix(y_train, predictions_train))
    print(classification_report(y_train, predictions_train))
    predictions_test = model.predict(x_test)
    print('test subset')
    print(confusion_matrix(y_test, predictions_test))
    print(classification_report(y_test, predictions_test))
    report_train = classification_report(y_train, predictions_train, output_dict=True)
    report_test = classification_report(y_test, predictions_test, output_dict=True)

    acc_train = report_train['accuracy']
    f1sc_train = report_train['weighted avg']['f1-score']

    acc_test = report_test['accuracy']
    f1sc_test = report_test['weighted avg']['f1-score']

    print('ch=' + str(channel) + ' seg=' + str(segment) + " accuracy train " + str(acc_train) + ' vs ' + str(
        acc_test) + ' test')
    # print("f1-score train " + str(f1sc_train) + ' vs ' + str(f1sc_test) + ' test')
