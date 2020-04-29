import os
import numpy as np
from sklearn.metrics import classification_report, confusion_matrix

from sklearn.model_selection import StratifiedShuffleSplit, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import obtain_features_labels_from_doa, train_test_doa_remake_balanced

encoding = Encoding('./../../../data_to_be_saved/alphabet_3.txt')

data_dir = os.path.join('../..', '..')

initialization = InitDataSet(data_dir=data_dir)
doas = initialization.get_dataset_as_doas()

runs_number = 5

for run in range(runs_number):
    print(f'######################### run  {run} #####################')
    doas_train, doas_test = train_test_doa_remake_balanced(doas)

    X_train, y_train = obtain_features_labels_from_doa(doas_train, 2, 'stimulus', encoding)
    x_test, y_test = obtain_features_labels_from_doa(doas_test, 2, 'stimulus', encoding)

    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train = scaler.transform(X_train)
    x_test = scaler.transform(x_test)

    param_grid = dict(gamma=[0.0001], C=[10.0])
    cv = StratifiedShuffleSplit(n_splits=4, test_size=0.2, random_state=42)
    grid = GridSearchCV(SVC(), param_grid=param_grid, cv=cv)
    grid.fit(X_train, y_train)

    #
    print("The best parameters are %s with a score of %0.2f"
          % (grid.best_params_, grid.best_score_))

    # All results
    means = grid.cv_results_['mean_test_score']
    stds = grid.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, grid.cv_results_['params']):
        print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))

    predictions = grid.predict(x_test)

    report = classification_report(y_test, predictions, output_dict=True)

    print(report)
    print(confusion_matrix(y_test, predictions))
    acc = report['accuracy']
    f1sc = report['weighted avg']['f1-score']

    print(f"accuracy {acc},  f-1 score {f1sc}")
