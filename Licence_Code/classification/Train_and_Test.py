import numpy as np
import pandas as pd
from numpy.random.mtrand import permutation
from sklearn.model_selection import train_test_split

# try to use train and test splitting on this example
# Y = [1, 0, 1, 1, 0, 1, 1, 0, 0, 0]  # 1 is for odds and 0 for evens
# X = [[1, 3, 5, 7], [2, 4, 6, 8], [11, 13, 15, 17], [21, 23, 25, 27], [12, 14, 16, 18], [31, 33, 35, 37],
#      [41, 43, 45, 47], [22, 24, 26, 28], [32, 34, 36, 38], [42, 44, 46, 48]]
#
# df = pd.DataFrame(X)
# y = np.array(Y)
#
# # create training and testing vars
# X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2, shuffle=False)
# print(X_train)
# print(y_train.shape)
# print(X_test.shape)
# print(y_test.shape)

# next we use X_train and y_train
from feature_extraction.TESPAR.Encoding import Encoding


class TrainTestSplitting:
    def __init__(self, inputData, encoding, lag):
        self.inputData = inputData
        self.en = encoding
        self.lag = lag

    def splitData(self, testPercentage):
        X_train = []
        Y_train = []
        X_test = []
        Y_test = []

        for i in range(len(self.inputData.result.arrays)):
            X = []
            Y = []
            for j in range(len(self.inputData.result.arrays[i].array)):
                # call encoding as param
                X.append(np.asarray(self.en.get_a(self.inputData.result.arrays[i].array[j], self.lag)).ravel())
                Y.append(self.inputData.result.arrays[i].name)

            # REMAINS TO BE SEEN
            # shuffle trials
            # X = np.asarray(X)
            # Y = np.asarray(Y)
            # perm = permutation(len(X))
            # X = X[perm]
            # Y = Y[perm]

            df = pd.DataFrame(X)
            y = np.array(Y)
            temp_X_train, temp_X_test, temp_y_train, temp_y_test = train_test_split(df, y, test_size=testPercentage,
                                                                                    shuffle=False)
            X_train.extend(temp_X_train.to_numpy())
            Y_train.extend(temp_y_train)
            X_test.extend(temp_X_test.to_numpy())
            Y_test.extend(temp_y_test)

        # shuffle output
        X_train = np.asarray(X_train)
        Y_train = np.asarray(Y_train)
        perm = permutation(len(X_train))
        X_train = X_train[perm]
        Y_train = Y_train[perm]

        X_test = np.asarray(X_test)
        Y_test = np.asarray(Y_test)
        perm = permutation(len(X_test))
        X_test = X_test[perm]
        Y_test = Y_test[perm]

        # save train deep light
        # save test deep light
        # save this to folders files

        return X_train, X_test, Y_train, Y_test
