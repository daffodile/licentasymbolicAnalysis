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


def obtain_features_labels(inputData, encoding):
    X = []
    Y = []

    for i in range(len(inputData.result.arrays)):
        for j in range(len(inputData.result.arrays[i].array)):
            X.append(np.asarray(encoding.get_a(inputData.result.arrays[i].array[j], 1)).ravel())
            Y.append(inputData.result.arrays[i].name)

    return X, Y


def split_2_channels(data_train, data_test, encoding, percent, seed):
    X1 = []
    Y1 = []

    for i in range(len(data_train.result.arrays)):
        for j in range(len(data_train.result.arrays[i].array)):
            X1.append(np.asarray(encoding.get_a(data_train.result.arrays[i].array[j], 1)).ravel())
            Y1.append(data_train.result.arrays[i].name)

    df_x1 = pd.DataFrame(X1)
    y1 = np.array(Y1)

    X2 = []
    Y2 = []

    for i in range(len(data_test.result.arrays)):
        for j in range(len(data_test.result.arrays[i].array)):
            X2.append(np.asarray(encoding.get_a(data_test.result.arrays[i].array[j], 1)).ravel())
            Y2.append(data_test.result.arrays[i].name)

    df_x2 = pd.DataFrame(X2)
    y2 = np.array(Y2)

    x1_train, x1_test, y1_train, y1_test = train_test_split(df_x1, y1, test_size=percent,
                                                            shuffle=True, stratify=y1, random_state=seed)
    x2_train, x2_test, y2_train, y2_test = train_test_split(df_x2, y2, test_size=percent,
                                                            shuffle=True, stratify=y2, random_state=seed)

    print('debug')
    return x1_train, x2_test, y1_train, y2_test
