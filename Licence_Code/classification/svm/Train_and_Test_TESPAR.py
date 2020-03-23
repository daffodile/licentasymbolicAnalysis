import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def splitData(inputData, encoding, testPercentage):
    X = []
    Y = []

    for i in range(len(inputData.result.arrays)):
        for j in range(len(inputData.result.arrays[i].array)):
            X.append(np.asarray(encoding.get_a(inputData.result.arrays[i].array[j], 1)).ravel())
            Y.append(inputData.result.arrays[i].name)

    df_x = pd.DataFrame(X)
    y = np.array(Y)

    x_train, x_test, y_train, y_test = train_test_split(df_x, y, test_size=testPercentage,
                                                        shuffle=True, stratify=y, random_state=None)
    #  to verify the right count from each class
    # df_ytrain = pd.DataFrame(y_train)
    # df_ytest = pd.DataFrame(y_test)
    #
    # # print("with stratify and shuffle of data")
    # # print(df_ytrain[0].value_counts())
    # # print(df_ytest[0].value_counts())

    return x_train, x_test, y_train, y_test
