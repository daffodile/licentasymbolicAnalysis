import os

from sklearn.model_selection import GridSearchCV
from sklearn.neural_network import MLPClassifier

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import obtain_features_labels_from_doa, train_test_doa_remake_balanced

encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')

data_dir = os.path.join('..', '..')

initialization = InitDataSet(data_dir=data_dir, levels=['deep', 'light'])
doas = initialization.get_dataset_as_doas()

doas_train, doas_test = train_test_doa_remake_balanced(doas)

X_train, y_train = obtain_features_labels_from_doa(doas_train, 2, 'spontaneous', encoding)
X_test, y_test = obtain_features_labels_from_doa(doas_test, 2, 'spontaneous', encoding)

parameter_space = {
    'hidden_layer_sizes': [(50, 50, 50), (50, 100, 50), (100, 100, 100), (10, 10, 10), (100,)],
    'activation': ['tanh', 'relu'],
    'solver': ['lbfgs', 'sgd', 'adam'],
    'alpha': [0.0001, 0.05, 0.1, 0.5],
    'learning_rate': ['constant', 'adaptive', 'invscaling'],
}
model = MLPClassifier(max_iter=100)

clf = GridSearchCV(model, parameter_space, n_jobs=-1, cv=5)
clf.fit(X_train, y_train)

# Best paramete set
print('Best parameters found:\n', clf.best_params_)

# All results
means = clf.cv_results_['mean_test_score']
stds = clf.cv_results_['std_test_score']
for mean, std, params in zip(means, stds, clf.cv_results_['params']):
    print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))

y_pred = clf.predict(X_test)

from sklearn.metrics import classification_report, confusion_matrix

print('Results on the test set:')
print(classification_report(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
