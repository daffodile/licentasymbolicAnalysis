def obtain_features_labels_quality(inputData, encoding, selected_symbols=32):
    X = []
    Y = []

    for i in range(len(inputData.result.arrays)):
        for j in range(len(inputData.result.arrays[i].array_data)):
            Tespar_features = np.asarray(encoding.get_a(inputData.result.arrays[i].array_data[j],
                                                        inputData.result.arrays[i].array_validate[j],
                                                        selected_symbols=selected_symbols))

            Tespar_features = Tespar_features.ravel()

            quality_feature = (len(inputData.result.arrays[i].array_validate[j]) -
                               [np.count_nonzero(inputData.result.arrays[i].array_validate[j])]) / (
                                  len(inputData.result.arrays[i].array_validate[j]))

            Features_Array = []
            Features_Array.append(Tespar_features.tolist())
            Features_Array.append(quality_feature)

            Features_List = list(flatten(Features_Array))

            X.append(np.asarray(Features_List).ravel())
            Y.append(inputData.result.arrays[i].name)

    return pd.DataFrame(X), Y
