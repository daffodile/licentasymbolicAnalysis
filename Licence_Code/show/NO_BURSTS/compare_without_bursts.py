from feature_extraction.TESPAR.AnalyzeChannels import plotMatrixA_Single
from feature_extraction.TESPAR.Encoding import Encoding
from feature_extraction.TESPAR.Encoding_no_burst import EncodingNoBurst
from input_reader.InitDataSet import InitDataSet
from input_reader.trials_outsiders.TrialsOutsiders import mark_outsiders
from utils.ExtractData import ExtractData
from utils.Utils import get_channel_segment_values

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
# mark_outsiders(doas)
#
# encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')
# encoding_no_burst = EncodingNoBurst('./../../data_to_be_saved/alphabet_3.txt')
#
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

this_trial = get_channel_segment_values(doas[0], 'stimulus', 2, 5)
print('debug')
