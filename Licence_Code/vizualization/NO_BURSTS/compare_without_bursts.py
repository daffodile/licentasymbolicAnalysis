from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from tests.NO_BURSTS.TrialsOutsiders import mark_outsiders
from utils.Utils import get_channel_trials_values_and_outsiders
import numpy as np

from vizualization.TESPAR.PlotTESPARMatrices import plot_matrix_A

# encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')
#
# initialization = InitDataSet()
# doas = initialization.get_dataset_as_doas()
#
# # encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')
#
# ######################## here code to encode with old encoder and also no_burst_encoder to compare A
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
# a = encoding.get_a(X[13], X_validate[13])
# # def plotMatrixA_Single(DOA, segment, channel_number, values):
# plot_matrix_A('DEEP_t14', 'spontaneous', 2, a)
#
# a = encoding.get_a(X[36], X_validate[36])
# # def plotMatrixA_Single(DOA, segment, channel_number, values):
# plot_matrix_A('DEEP_t37', 'spontaneous', 2, a)
#
# a_no_bursts = encoding.get_a(X[0], X_validate[0])
# plot_matrix_A('DEEP_no_bursts', 'spontaneous', 2, a_no_bursts)
#
#
# mark_outsiders(doas)
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
# a = encoding.get_a(X[13], X_validate[13])
# # def plotMatrixA_Single(DOA, segment, channel_number, values):
# plot_matrix_A('DEEP_t14_no_bursts', 'spontaneous', 2, a)
#
# a = encoding.get_a(X[36], X_validate[36])
# # def plotMatrixA_Single(DOA, segment, channel_number, values):
# plot_matrix_A('DEEP_t37_no_bursts', 'spontaneous', 2, a)
#
# a_no_bursts = encoding.get_a(X[0], X_validate[0])
# plot_matrix_A('DEEP_no_bursts', 'spontaneous', 2, a_no_bursts)

############### test getting all values in a channel and plotting tespar A of it ##################

encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()

# all_trials_values, all_trials_outsiders = get_channel_trials_values_and_outsiders(doas, 'light', 'spontaneous', 2)
# a_matrix_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
# for i in range(len(all_trials_values)):
#     a_matrix = encoding.get_a(all_trials_values[i], all_trials_outsiders[i])
#     a_matrix_all = np.add(a_matrix_all, a_matrix)
# # print('debug')
# a_matrix_all = np.log10(a_matrix_all + 1)
# plot_matrix_A(DOA='LIGHT_all', segment='spontaneous', channel_number=2, values=a_matrix_all)
#
# all_trials_values, all_trials_outsiders = get_channel_trials_values_and_outsiders(doas, 'light', 'spontaneous', 7)
# a_matrix_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
# for i in range(len(all_trials_values)):
#     a_matrix = encoding.get_a(all_trials_values[i], all_trials_outsiders[i])
#     a_matrix_all = np.add(a_matrix_all, a_matrix)
# a_matrix_all = np.log10(a_matrix_all + 1)
# plot_matrix_A(DOA='LIGHT_all', segment='spontaneous', channel_number=7, values=a_matrix_all)

mark_outsiders(doas)

all_trials_values, all_trials_outsiders = get_channel_trials_values_and_outsiders(doas, 'deep', 'spontaneous', 2)
a_matrix_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
for i in range(len(all_trials_values)):
    a_matrix = encoding.get_a(all_trials_values[i], all_trials_outsiders[i])
    a_matrix_all = np.add(a_matrix_all, a_matrix)
a_matrix_all = np.log10(a_matrix_all + 1)
plot_matrix_A(DOA='DEEP_all_no_bursts', segment='spontaneous', channel_number=2, values=a_matrix_all)

# all_trials_values, all_trials_outsiders = get_channel_trials_values_and_outsiders(doas, 'light', 'spontaneous', 7)
# a_matrix_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
# for i in range(len(all_trials_values)):
#     a_matrix = encoding.get_a(all_trials_values[i], all_trials_outsiders[i])
#     a_matrix_all = np.add(a_matrix_all, a_matrix)
# a_matrix_all = np.log10(a_matrix_all + 1)
# plot_matrix_A(DOA='lib2_LIGHT_all_no_bursts_log', segment='spontaneous', channel_number=7, values=a_matrix_all)

mark_outsiders(doas, liberty=1.68)


all_trials_values, all_trials_outsiders = get_channel_trials_values_and_outsiders(doas, 'deep', 'spontaneous', 2)
a_matrix_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
for i in range(len(all_trials_values)):
    a_matrix = encoding.get_a(all_trials_values[i], all_trials_outsiders[i])
    a_matrix_all = np.add(a_matrix_all, a_matrix)
a_matrix_all = np.log10(a_matrix_all + 1)
plot_matrix_A(DOA='lib1.68_DEEP_all_no_bursts', segment='spontaneous', channel_number=2, values=a_matrix_all)

all_trials_values, all_trials_outsiders = get_channel_trials_values_and_outsiders(doas, 'deep', 'spontaneous', 7)
a_matrix_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
for i in range(len(all_trials_values)):
    a_matrix = encoding.get_a(all_trials_values[i], all_trials_outsiders[i])
    a_matrix_all = np.add(a_matrix_all, a_matrix)
a_matrix_all = np.log10(a_matrix_all + 1)
plot_matrix_A(DOA='lib1.68_DEEP_all_no_bursts_log', segment='spontaneous', channel_number=7, values=a_matrix_all)
