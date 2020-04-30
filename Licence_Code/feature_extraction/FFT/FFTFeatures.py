import numpy as np

import pandas as pd

from feature_extraction.FFT.Welch import Welch, get_average_band_power


def getList(dictFFTBands):
    # return dict.keys(), dict.values()
    return list(dictFFTBands.values())

    # values = []
    # for key in dictFFTBands:
    #     values.extend(list(dictFFTBands[key]))
    # return values
    # for deleting the empty strings
    # values = list(filter(None, values))


def obtain_FFT_features_labels(inputData):
    X = []
    Y = []

    for i in range(len(inputData.result.arrays)):
        for j in range(len(inputData.result.arrays[i].array_data)):
            valid = True
            band_fft_avg = get_average_band_power(inputData.result.arrays[i].array_data[j],
                                                  inputData.result.arrays[i].array_validate[j])
            # band_fft_max = Welch.get_max_band_power(inputData.result.arrays[i].array_data[j],
            #                                         inputData.result.arrays[i].array_validate[j])
            x1 = np.asarray(getList(band_fft_avg))
            if x1[0] == 0:
                valid = False
            if valid:
                X.append(np.asarray(getList(band_fft_avg)))
                Y.append(inputData.result.arrays[i].name)

    return pd.DataFrame(X), Y


def obtain_TESPAR_A_FFT_features(inputData, encoding, selected_symbols=32):
    X = []
    Y = []

    for i in range(len(inputData.result.arrays)):
        for j in range(len(inputData.result.arrays[i].array_data)):
            valid = True
            band_fft_avg = get_average_band_power(inputData.result.arrays[i].array_data[j],
                                                  inputData.result.arrays[i].array_validate[j])
            arr = []
            x1 = np.asarray(getList(band_fft_avg))
            x2 = np.asarray(encoding.get_a(inputData.result.arrays[i].array_data[j],
                                           inputData.result.arrays[i].array_validate[j],
                                           selected_symbols)).ravel()
            if x1[0] == 0:
                valid = False
            arr.extend(x1)
            arr.extend(x2)
            # arr.append(x2)
            # print(arr)
            if valid:
                X.append(arr)
                Y.append(inputData.result.arrays[i].name)

    return pd.DataFrame(X), Y


def obtain_TESPAR_S_FFT_features(inputData, encoding, selected_symbols=32):
    X = []
    Y = []

    for i in range(len(inputData.result.arrays)):
        for j in range(len(inputData.result.arrays[i].array_data)):
            valid = True
            band_fft_avg = get_average_band_power(inputData.result.arrays[i].array_data[j],
                                                  inputData.result.arrays[i].array_validate[j])
            arr = []
            x1 = np.asarray(getList(band_fft_avg))
            x2 = np.asarray(encoding.get_s(inputData.result.arrays[i].array_data[j],
                                           inputData.result.arrays[i].array_validate[j])).ravel()
            if x1[0] == 0:
                valid = False
            arr.extend(x1)
            arr.extend(x2)
            # arr.append(x2)
            # print(arr)
            if valid:
                X.append(arr)
                Y.append(inputData.result.arrays[i].name)

    return pd.DataFrame(X), Y


def obtain_concatenate_segments_fft(inputData):
    X = []
    Y = []

    for i in range(len(inputData.result.arrays)):
        count = len(inputData.result.arrays[i].array_data) / 2
        print("length is :" + str(count))
        for j in range(int(count)):

            valid = True
            band_fft_avg1 = get_average_band_power(inputData.result.arrays[i].array_data[j * 2],
                                                   inputData.result.arrays[i].array_validate[j * 2])
            band_fft_avg2 = get_average_band_power(inputData.result.arrays[i].array_data[j * 2 + 1],
                                                   inputData.result.arrays[i].array_validate[j * 2 + 1])
            x1 = np.asarray(getList(band_fft_avg1))
            x2 = np.asarray(getList(band_fft_avg2))
            if x1[0] == 0 or x2[0] == 0:
                valid = False
            if valid:
                X.append(np.append(x1, x2))
                Y.append(inputData.result.arrays[i].name)

    return pd.DataFrame(X), Y


def obtain_concatenate_segments_FFT_TESPAR_A(inputData, encoding):
    X = []
    Y = []

    for i in range(len(inputData.result.arrays)):
        count = len(inputData.result.arrays[i].array_data) / 2
        print("length is :" + str(count))
        for j in range(int(count)):
            valid = True
            arr1 = []
            arr2 = []
            band_fft_avg1 = get_average_band_power(inputData.result.arrays[i].array_data[j * 2],
                                                   inputData.result.arrays[i].array_validate[j * 2])

            x1 = np.asarray(getList(band_fft_avg1))
            t1 = np.asarray(encoding.get_a(inputData.result.arrays[i].array_data[j * 2],
                                           inputData.result.arrays[i].array_validate[j * 2])).ravel()

            arr1.extend(x1)
            arr1.extend(t1)

            band_fft_avg2 = get_average_band_power(inputData.result.arrays[i].array_data[j * 2 + 1],
                                                   inputData.result.arrays[i].array_validate[j * 2 + 1])

            x2 = np.asarray(getList(band_fft_avg2))
            t2 = np.asarray(encoding.get_s(inputData.result.arrays[i].array_data[j * 2 + 1],
                                           inputData.result.arrays[i].array_validate[j * 2 + 1])).ravel()
            arr2.extend(x2)
            arr2.extend(t2)

            if x1[0] == 0 or x2[0] == 0:
                valid = False

            # valid = True
            # band_fft_avg1 = get_average_band_power(inputData.result.arrays[i].array_data[j * 2],
            #                                        inputData.result.arrays[i].array_validate[j * 2])
            # band_fft_avg2 = get_average_band_power(inputData.result.arrays[i].array_data[j * 2 + 1],
            #                                        inputData.result.arrays[i].array_validate[j * 2 + 1])
            # x1 = np.asarray(getList(band_fft_avg1))
            # x2 = np.asarray(getList(band_fft_avg2))
            # if x1[0] == 0 or x2[0] == 0:
            #     valid = False
            # array1 = np.asarray(encoding.get_a(inputData.result.arrays[i].array_data[j * 2],
            #                                    inputData.result.arrays[i].array_validate[j * 2])).ravel()
            # array2 = np.asarray(encoding.get_a(inputData.result.arrays[i].array_data[j * 2 + 1],
            #                                    inputData.result.arrays[i].array_validate[j * 2 + 1])).ravel()
            # arr = []
            # arr.extend(np.append(array1, array2))
            # arr.extend(np.append(x1, x2))
            if valid:
                X.append(np.append(arr1, arr2))
                Y.append(inputData.result.arrays[i].name)

    return pd.DataFrame(X), Y
