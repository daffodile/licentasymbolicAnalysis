from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet


def get_channel_values(doas, doa_level, channel_number):
    channel_values = []
    for i in range(240):
        channel_values.extend(doas[doa_level].channels[channel_number].trials[i].stimulus.values)
    return channel_values


all_channels = [1, 5, 14, 19, 26, 29]
good_channels = [1, 5, 14]
bad_channels = [19, 26, 29]

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
encoder = Encoding('../../data_to_be_saved/alphabet_1_150hz.txt')

# # todo
# # 6 matrici a deep normal
# # 6 matrici a light normal
# # 6 matrici a deep log
# # 6 matrici a light log
# # - print theem

import numpy as np
import matplotlib.pyplot as plt


def plotMatrixA(DOA, segment, channel_number, values):
    fig = plt.figure(figsize=(30, 25))
    ax = fig.add_subplot()
    min_val, max_val = 0, 32
    cax = ax.matshow(values, cmap=plt.cm.Blues)
    cbar = fig.colorbar(cax)
    cbar.mappable.set_clim(-200.0, 200.0)
    cbar.ax.tick_params(labelsize=30)
    ax.tick_params(labelsize=30)
    for i in range(32):
        for j in range(32):
            c = values[j, i]
            ax.text(i, j, str(c), va='center', ha='center', fontsize=20)
    ax.invert_yaxis()
    ax.xaxis.tick_bottom()
    fig.suptitle("A Matrix " + DOA + " " + segment + " ch: " + str(channel_number), fontsize=35)
    plt.show()


# for i in range(len(all_channels)):
# channel_values = get_channel_values(doas, 0, all_channels[i])
# channel_values = get_channel_values(doas, 2, all_channels[i])
# a_matrix = np.array(encoder.get_a(channel_values, 1))
# plotMatrixA("Deep", "Stimulus", all_channels[i], a_matrix)
# plotMatrixA("Light", "Stimulus", str(all_channels[i]), a_matrix)


good_channel_values = get_channel_values(doas, 0, 1)
bad_channel_values = get_channel_values(doas, 2, 1)
good_a_matrix = np.array(encoder.get_a(good_channel_values, 1))
bad_a_matrix = np.array(encoder.get_a(bad_channel_values, 1))
dif_matrix = good_a_matrix - bad_a_matrix
plotMatrixA("Medium", "Stimulus", "14", good_a_matrix)
