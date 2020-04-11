from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet

all_channels = [1, 5, 14, 16, 19, 26]
good_channels = [1, 5, 14]
bad_channels = [19, 19, 26]

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
encoder = Encoding('../../input_reader/initialize_TESPAR_alphabet/alphabet.txt')

# normal matrix
# log matrix
# for i in range(len(all_channels)):
# channel_values_deep = get_channel_values(doas, 0, all_channels[i])
# channel_values_medium = get_channel_values(doas, 1, all_channels[i])
# channel_values_light = get_channel_values(doas, 2, all_channels[i])

# a_matrix_deep_normal = np.array(encoder.get_a(channel_values_deep, 1))
# a_matrix_deep_log = np.array(np.log10([[v + 1 for v in r] for r in encoder.get_a(channel_values_deep, 1)]))
# a_matrix_medium_normal = np.array(encoder.get_a(channel_values_medium, 1))
# a_matrix_medium_log = np.array(np.log10([[v + 1 for v in r] for r in encoder.get_a(channel_values_medium, 1)]))
# a_matrix_light_normal = np.array(encoder.get_a(channel_values_light, 1))
# a_matrix_light_log = np.array(np.log10([[v + 1 for v in r] for r in encoder.get_a(channel_values_light, 1)]))

# plotMatrixA_Single("Deep", "Poststimulus", all_channels[i], a_matrix_deep_normal)
# plotMatrixA_SingleLog("Deep", "Poststimulus", all_channels[i], a_matrix_deep_log)
# plotMatrixA_Single("Medium", "Poststimulus", all_channels[i], a_matrix_medium_normal)
# plotMatrixA_SingleLog("Medium", "Poststimulus", all_channels[i], a_matrix_medium_log)
# plotMatrixA_Single("Light", "Poststimulus", all_channels[i], a_matrix_light_normal)
# plotMatrixA_SingleLog("Light", "Poststimulus", all_channels[i], a_matrix_light_log)

# for i in range(len(all_channels)):
#     channel_value_deep = get_channel_values(doas, 0, all_channels[i])
#     channel_value_light = get_channel_values(doas, 2, all_channels[i])
#     a_matrix_deep = np.array(encoder.get_a(channel_value_deep, 1))
#     a_matrix_light = np.array(encoder.get_a(channel_value_light, 1))
#     dif_matrix = a_matrix_deep - a_matrix_light
#     plotMatrixA_Difference("Deep-Light", "Spontaneous", all_channels[i], dif_matrix)


###### use fct from util taht gets array of arrays of trials.values  ################
# channel_value_deep = get_channel_values(doas, 0, 1)
# channel_value_light = get_channel_values(doas, 2, 1)
# a_matrix_deep_log = np.array(np.log10([[v + 1 for v in r] for r in encoder.get_a(channel_value_deep, 1)]))
# # a_matrix_light_log = np.array(np.log10([[v + 1 for v in r] for r in encoder.get_a(channel_value_light, 1)]))
# # # dif_matrix = a_matrix_deep - a_matrix_light
# # # plotMatrixA_Difference("Deep-Light", "Stimulus", 1, dif_matrix)
# # plotMatrixA_SingleLog("Light", "Stimulus", 1, a_matrix_light_log)
# # plotMatrixA_SingleLog("Deep", "Stimulus", 1, a_matrix_deep_log)
