import numpy as np

from classification.SplitData import SplitData
from feature_extraction.FFT.Welch import Welch
from feature_extraction.TESPAR.Encoding import Encoding
from feature_extraction.TESPAR.Encoding_no_burst import EncodingNoBurst
from input_reader.InitDataSet import InitDataSet
from utils.ExtractData import ExtractData

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()

encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')
encoding_no_burst = EncodingNoBurst('./../../data_to_be_saved/alphabet_3.txt')

data = ExtractData(doas, [1], ['light'], ['stimulus'], ['all'])

X = []
X_validate = []
for i in range(len(data.result.arrays)):
    for j in range(len(data.result.arrays[i].array_data)):
        X.append(data.result.arrays[i].array_data[j])
    for j in range(len(data.result.arrays[i].array_validate)):
        X_validate.append(data.result.arrays[i].array_validate[j])

# TEST with and without burst
encoding.get_a(X[0], 1)
encoding.get_s(X[0])

encoding_no_burst.get_a(X[0], X_validate[0], 1)
encoding_no_burst.get_s(X[0], X_validate[0])
