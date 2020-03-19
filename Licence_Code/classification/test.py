from classification.SplitData import SplitData
from classification.random_forest.RandomForest import RandomForest
from input_reader.InitDataSet import InitDataSet
from classification.Train_and_Test import TrainTestSplitting
from Tests.Classifiers.decision_tree.DecisionTreeClassificator import DecisionTreeClassificator

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

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()

# dataset, channels, levels, segment, orientation
# split_data = SplitData(doas, [1], ['light', 'deep'], ['spontaneous'], ['all'])
# split_data = SplitData(doas, [1], ['light', 'deep'], ['spontaneous'], [90])
# split_data = SplitData(doas, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], ['light', 'deep'], ['spontaneous'], ['all'])
# # print(split_data.result.arrays[0].array[0])
# trainTestSplit = TrainTestSplitting(split_data, 'alphabet_3hz', 1)
# test_x_train, test_x_test, test_y_train, test_y_test = trainTestSplit.splitData(0.3)
# dtc = DecisionTreeClassificator(test_x_train, test_x_test, test_y_train, test_y_test)
# dtc.classify()
# what are you classifying?
#to test: alphabet, lag, doas, channels, level, segment, orientation
randomFClassifier = RandomForest('1hz', 1, doas, [1], ['light', 'deep'], ['spontaneous'], ['all'])
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
