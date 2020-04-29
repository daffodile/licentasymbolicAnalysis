import os

from sklearn.model_selection import cross_val_score, StratifiedKFold, cross_validate
from sklearn.svm import SVC

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import obtain_features_labels_from_doa

channel = 5

segment = 'spontaneous'

data_dir = os.path.join('..', '..')

initialization = InitDataSet(data_dir=data_dir)
doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')

X, y = obtain_features_labels_from_doa(doas, channel, segment, encoding)

model = SVC(gamma="auto")

skf = StratifiedKFold(n_splits=10)

skf.get_n_splits(X, y)

print(skf)

print('### cross_val_score  ### ')
accuracy = cross_val_score(model, X, y, scoring='accuracy', cv=skf)
print(accuracy)
# get the mean of each fold
print("Accuracy of Model with Cross Validation is:", accuracy.mean() * 100)

print('### cross_validate  ### ')
results = cross_validate(model, X, y, scoring=['accuracy', 'f1_weighted'], cv=skf)
print(results['test_accuracy'])
print(results['test_f1_weighted'])

# always this output: for StratifiedKFold of 5
# [0.64583333 0.70833333 0.59375    0.76041667 0.69791667]
# Accuracy of Model with Cross Validation is: 68.125


# StratifiedKFold(n_splits=10, random_state=None, shuffle=False)
# [0.75       0.58333333 0.66666667 0.72916667 0.58333333 0.625
#  0.75       0.75       0.83333333 0.60416667]
# Accuracy of Model with Cross Validation is: 68.75
