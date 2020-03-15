import os

import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV
from sklearn import preprocessing

X_train = []
y_train = []
X_test = []
y_test = []

dir_train = "ch13_spontaneous/train/"
files_train = os.listdir(dir_train)
for file in files_train:
    # print(file)
    f = open(dir_train + file, 'r')
    if f.readline().rstrip() == 'deep':
        y_train.append(0)
    else:
        y_train.append(1)
    x = np.loadtxt(f, dtype='i')
    X_train.append(x)

dir_test = "ch13_spontaneous/test/"
files_test = os.listdir(dir_test)
for file in files_test:
    # print(file)
    f = open(dir_test + file, 'r')
    if f.readline().rstrip() == 'deep':
        y_test.append(0)
    else:
        y_test.append(1)
    x = np.loadtxt(f, dtype='i')
    X_test.append(x)

print('loaded input')

model = SVC()


# ########## bew scaling hereee#################
# scaler = preprocessing.StandardScaler().fit(X_train)
# scaler.transform(X_train)
# model.fit(X_train, y_train)
#
# # ###### apply same scaler on test data
# # scaler.transform(X_test)
# predictions = model.predict(X_test)
#
# print(confusion_matrix(y_test, predictions))
# print('\n')
# print(classification_report(y_test, predictions))

param_grid = {'C': [0.1, 1, 10, 100, 1000], 'gamma': [1, 0.1, 0.01, 0.001, 0.0001, 0.0001]}
grid = GridSearchCV(SVC(), param_grid=param_grid, verbose=3)
grid.fit(X_train, y_train)

print(grid.best_params_)

print(grid.best_estimator_)

grid_predictions = grid.predict(X_test)

print(confusion_matrix(y_test, grid_predictions))
print('\n')
print(classification_report(y_test, grid_predictions))

print('br')

