from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier

from classification.SplitData import SplitData
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from Tests.Classifiers.decision_tree.Train_and_Test import TrainTestSplitting

# A = [[[1, 2],
#       [3, 4]],
#
#      [[7, 8],
#       [9, 10]],
#
#      [[13, 14],
#       [15, 16]]
#      ]
#
# for i in range(len(A)):
#     A[i] = np.asarray(A[i]).ravel()
#
# print(A)
encoding = Encoding('./../data_to_be_saved/alphabet_1_150hz.txt')
initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()

# dataset, channels, levels, segment, orientation
split_data = SplitData(doas, [1], ['light', 'medium', 'deep'], ['spontaneous','stimulus'], ['all'])
# split_data.concatenate_segments()
# split_data = SplitData(doas, [1], ['light', 'deep'], ['spontaneous'], [90])
# split_data = SplitData(doas, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ['light', 'deep'], ['spontaneous'], ['all'])
# # print(split_data.result.arrays[0].array[0])
t = TrainTestSplitting(split_data, encoding, 1)
X_train, x_test, y_train, y_test = t.splitData_concatenate_segment(0.2)
clf = RandomForestClassifier(n_estimators=100)
clf.fit(X_train, y_train)
y_pred = clf.predict(x_test)
print("Accuracy:", metrics.accuracy_score(y_test, y_pred))

# dtc = DecisionTreeClassificator(test_x_train, test_x_test, test_y_train, test_y_test)
# dtc.classify()
# what are you classifying?
# to test: alphabet, lag, doas, channels, level, segment, orientation
# randomFClassifier = RandomForest('1-150hz', 1, doas, [1], ['light', 'medium', 'deep'], ['spontaneous', 'stimulus'], ['all'])
#
#
# doa_light = np.extract(condition=(lambda x: x.level == "light"), arr=doas)[0]
# doa_deep = np.extract(condition=(lambda x: x.level == "deep"), arr=doas)[1]
# doa_medium = np.extract(condition=(lambda x: x.level == "deep"), arr=doas)[2]
#
#
# random_forest = RandomForest(init_data.get_dataset_as_doas(), )

# shuffle two arrays
# X = [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]
# Y = [1, 2, 3, 4, 5]
#
# X = np.asarray(X)
# Y = np.asarray(Y)
# perm = permutation(len(X))
# X = X[perm]
# Y = Y[perm]
# print(X)
# print(Y)
