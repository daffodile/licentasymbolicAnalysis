from vizualization.TESPAR.AnalyzeChannels import plotMatrixA_Single
from feature_extraction.TESPAR.Encoding import Encoding
from feature_extraction.TESPAR.Encoding_no_burst import EncodingNoBurst
from input_reader.InitDataSet import InitDataSet
from utils.TrialsOutsiders import mark_outsiders
from utils.Utils import get_channel_trials_values_and_outsiders
import numpy as np

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()

encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')

encoding_no_burst = EncodingNoBurst('./../../data_to_be_saved/alphabet_3.txt')

######################## here code to encode with old encoder and also no_burst_encoder to compare A
# data = ExtractData(doas, [2], ['deep'], ['spontaneous'], ['all'])
#
# X = []
# X_validate = []
# for i in range(len(data.result.arrays)):
#     for j in range(len(data.result.arrays[i].array_data)):
#         X.append(data.result.arrays[i].array_data[j])
#     for j in range(len(data.result.arrays[i].array_validate)):
#         X_validate.append(data.result.arrays[i].array_validate[j])
#
# # TEST with and without burst
# a_full = encoding.get_a(X[0])
# # def plotMatrixA_Single(DOA, segment, channel_number, values):
# plotMatrixA_Single('DEEP_full', 'spontaneous', 2, a_full)
#
# a_no_bursts = encoding_no_burst.get_a(X[0], X_validate[0])
# plotMatrixA_Single('DEEP_no_bursts', 'spontaneous', 2, a_no_bursts)


############### test getting all values in a channel and plotting tespar A of it ##################

mark_outsiders(doas)

all_trials_values, all_trials_outsiders = get_channel_trials_values_and_outsiders(doas, 'deep', 'spontaneous', 2)
a_matrix_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
for i in range(len(all_trials_values)):
    a_matrix = encoding_no_burst.get_a(all_trials_values[i], all_trials_outsiders[i])
    a_matrix_all = np.add(a_matrix_all, a_matrix)
print('debug')
a_matrix_all = np.log10(a_matrix_all + 1)
plotMatrixA_Single(DOA='DEEP_all_no_bursts_log', segment='spontaneous', channel_number=2, values=a_matrix_all)
