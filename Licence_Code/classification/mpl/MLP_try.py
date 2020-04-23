import os
import random

from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.neural_network import MLPClassifier

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import obtain_features_labels_from_doa

# encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')
#
# data_dir = os.path.join('..', '..')
#
# initialization = InitDataSet(data_dir=data_dir, levels=['deep', 'light'])
# doas = initialization.get_dataset_as_doas()
#
# X_train, y_train = obtain_features_labels_from_doa(doas, 2, 'spontaneous', encoding)
#
# model = MLPClassifier(solver='lbfgs', alpha=1e-5, random_state=1)
#
# skf = StratifiedKFold()
# cv_result = cross_val_score(model, X_train, y_train, cv=skf, scoring="accuracy")
# print(cv_result)
# average_res = cv_result.mean()
# print(average_res)

trials_common_to_all = [i for i in range(240)]
print(trials_common_to_all)

random.Random(4).shuffle(trials_common_to_all)
print(trials_common_to_all)