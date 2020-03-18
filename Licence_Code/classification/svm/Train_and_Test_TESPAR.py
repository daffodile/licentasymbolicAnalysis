import numpy as np
import pandas as pd
from numpy.random.mtrand import permutation
from sklearn.model_selection import train_test_split


class TrainTestSplitting:
    def __init__(self, inputData, encoding):
        self.inputData = inputData
        self.encoding = encoding

    def splitData(self, testPercentage):
        X_train = []
        Y_train = []
        X_test = []
        Y_test = []

        for i in range(len(self.inputData.result.arrays)):
            X = []
            Y = []
            for j in range(len(self.inputData.result.arrays[i].array)):
                X.append(np.asarray(self.encoding.get_a(self.inputData.result.arrays[i].array[j], 1)).ravel())
                Y.append(self.inputData.result.arrays[i].name)

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

        return X_train, X_test, Y_train, Y_test
