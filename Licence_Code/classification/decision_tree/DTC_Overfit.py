import numpy as np
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV
from sklearn.tree import DecisionTreeClassifier

from classification.SplitData import SplitData
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import train_test_doa, obtain_features_labels

# how many models to train a for a channel-segment pair
run_nr = 10

all_channels = [1, 5, 14, 16, 19, 26]

channel = 29
segment = 'stimulus'

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')

print('test for overfitting DTC 0.2')

for run in range(run_nr):
    # firstly split the input into train test
    doas_train, doas_test, ind_test = train_test_doa(doas, 0.2)

    train_data = SplitData(doas_train, [channel], ['light', 'deep'], [segment], ['all'])
    test_data = SplitData(doas_test, [channel], ['light', 'deep'], [segment], ['all'])

    X_train, y_train = obtain_features_labels(train_data, encoding)
    x_test, y_test = obtain_features_labels(test_data, encoding)
    #
    # check_params = {'criterion': ['gini', 'entropy'],
    #                 'max_depth': np.arange(2, 20)}
    # # 'max_leaf_nodes': np.arange(2, 100)
    # for cv in range(3, 20):
    #     create_grid = GridSearchCV(DecisionTreeClassifier(random_state=99), param_grid=check_params, cv=cv)
    #     create_grid.fit(X_train, y_train)
    #     print("score for %d fold CV := %3.2f" % (cv, create_grid.score(X_train, y_train)))
    #     print("score for %d fold CV := %3.2f" % (cv, create_grid.score(x_test, y_test)))
    #     print("!!! best fit parameters from GridSearchCV !!!")
    #     print(create_grid.best_params_)

    # model = DecisionTreeClassifier()
    model = DecisionTreeClassifier(random_state=99, criterion='gini', max_depth=2)
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
