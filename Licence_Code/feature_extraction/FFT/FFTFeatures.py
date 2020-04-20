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
            band_fft_avg = get_average_band_power(inputData.result.arrays[i].array_data[j],
                                                  inputData.result.arrays[i].array_validate[j])
            # band_fft_max = Welch.get_max_band_power(inputData.result.arrays[i].array_data[j],
            #                                         inputData.result.arrays[i].array_validate[j])
            X.append(np.asarray(getList(band_fft_avg)))
            Y.append(inputData.result.arrays[i].name)

    return pd.DataFrame(X), Y


def obtain_TESPAR_FFT_features(inputData, encoding, selected_symbols=32):
    X = []
    Y = []

    for i in range(len(inputData.result.arrays)):
        for j in range(len(inputData.result.arrays[i].array_data)):
            band_fft_avg = get_average_band_power(inputData.result.arrays[i].array_data[j],
                                                  inputData.result.arrays[i].array_validate[j])
            arr = []
            x1 = np.asarray(getList(band_fft_avg))
            x2 = np.asarray(encoding.get_a(inputData.result.arrays[i].array_data[j],
                                           inputData.result.arrays[i].array_validate[j],
                                           selected_symbols)).ravel()
            arr.extend(x1)
            arr.extend(x2)
            # arr.append(x2)
            # print(arr)
            X.append(arr)

            #
            # # X_all.append(x1)
            # # X_all.append(x2)
            # # X.append(X_all)
            # X.append(np.concatenate(x1,x1))

            # X.append(np.asarray(encoding.get_a(inputData.result.arrays[i].array_data[j],
            #                                    inputData.result.arrays[i].array_validate[j],
            #                                    selected_symbols)).ravel())
            # X.extend(np.asarray(getList(band_fft_avg)))
            Y.append(inputData.result.arrays[i].name)

    return pd.DataFrame(X), Y
