import numpy as np
import matplotlib.pyplot as plt
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
import seaborn as sns

all_channels = [1, 5, 14, 16, 19, 26]
good_channels = [1, 5, 14]
bad_channels = [19, 19, 26]

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
encoder = Encoding('../../data_to_be_saved/alphabet_1_150hz.txt')


def plotMatrixA_SingleLog(DOA, segment, channel_number, values):
    fig = plt.figure(figsize=(30, 25))
    ax = fig.add_subplot()
    cax = ax.matshow(values, cmap=plt.cm.Blues)
    cbar = fig.colorbar(cax)
    # TODO
    cbar.mappable.set_clim(0, 3.5)
    cbar.ax.tick_params(labelsize=30)
    ax.tick_params(labelsize=30)
    ax.invert_yaxis()
    ax.xaxis.tick_bottom()
    fig.suptitle("Log A Matrix - " + DOA + " " + segment + " ch: " + str(channel_number), fontsize=35, y=0.99,
                 fontweight='bold')
    plot_name = 'compare_channels/log/blues/Channel_' + str(
        channel_number) + "_" + DOA + "_" + segment + "_Log" + "_A.png"
    plt.show()
    fig.savefig(plot_name)


def plotMatrixA_Single(DOA, segment, channel_number, values):
    fig = plt.figure(figsize=(30, 25))
    ax = fig.add_subplot()
    cax = ax.matshow(values, cmap=plt.cm.Blues)
    cbar = fig.colorbar(cax)
    cbar.mappable.set_clim(0, 500.0)
    cbar.ax.tick_params(labelsize=30)
    ax.tick_params(labelsize=30)
    ax.invert_yaxis()
    ax.xaxis.tick_bottom()
    fig.suptitle("A Matrix - " + DOA + " " + segment + " ch: " + str(channel_number), fontsize=35, y=0.99,
                 fontweight='bold')
    plot_name = 'compare_channels/normal/blues/Channel_' + str(channel_number) + "_" + DOA + "_" + segment + "_A.png"
    plt.show()
    fig.savefig(plot_name)


def plotMatrixA_Difference(DOA, segment, channel_number, values):
    fig = plt.figure(figsize=(30, 25))
    ax = fig.add_subplot()
    cax = ax.matshow(values, cmap=plt.cm.Spectral)
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
    fig.suptitle("A Matrix - " + DOA + " " + segment + " ch: " + str(channel_number), fontsize=35, y=0.99,
                 fontweight='bold')
    plot_name = 'compare_channels/diff/Channels_' + str(channel_number) + "_" + DOA + "_" + segment + "_A.png"
    plt.show()
    fig.savefig(plot_name)


def get_channel_values(doas, doa_level, channel_number):
    channel_values = []
    for i in range(240):
        channel_values.extend(doas[doa_level].channels[channel_number].trials[i].stimulus.values)
    return channel_values


# normal matrix
# log matrix
for i in range(len(all_channels)):
    # channel_values_deep = get_channel_values(doas, 0, all_channels[i])
    # channel_values_medium = get_channel_values(doas, 1, all_channels[i])
    channel_values_light = get_channel_values(doas, 2, all_channels[i])

    # a_matrix_deep_normal = np.array(encoder.get_a(channel_values_deep, 1))
    # a_matrix_deep_log = np.array(np.log10([[v + 1 for v in r] for r in encoder.get_a(channel_values_deep, 1)]))
    # a_matrix_medium_normal = np.array(encoder.get_a(channel_values_medium, 1))
    # a_matrix_medium_log = np.array(np.log10([[v + 1 for v in r] for r in encoder.get_a(channel_values_medium, 1)]))
    # a_matrix_light_normal = np.array(encoder.get_a(channel_values_light, 1))
    a_matrix_light_log = np.array(np.log10([[v + 1 for v in r] for r in encoder.get_a(channel_values_light, 1)]))

    # plotMatrixA_Single("Deep", "Stimulus", all_channels[i], a_matrix_deep_normal)
    # plotMatrixA_SingleLog("Deep", "Stimulus", all_channels[i], a_matrix_deep_log)
    # plotMatrixA_Single("Medium", "Stimulus", all_channels[i], a_matrix_medium_normal)
    # plotMatrixA_SingleLog("Medium", "Stimulus", all_channels[i], a_matrix_medium_log)
    # plotMatrixA_Single("Light", "Stimulus", all_channels[i], a_matrix_light_normal)
    plotMatrixA_SingleLog("Light", "Stimulus", all_channels[i], a_matrix_light_log)

# for i in range(len(all_channels)):
#     channel_value_deep = get_channel_values(doas, 0, all_channels[i])
#     channel_value_light = get_channel_values(doas, 2, all_channels[i])
#     a_matrix_deep = np.array(encoder.get_a(channel_value_deep, 1))
#     a_matrix_light = np.array(encoder.get_a(channel_value_light, 1))
#     dif_matrix = a_matrix_deep - a_matrix_light
#     plotMatrixA_Difference("Deep-Light", "Spontaneous", all_channels[i], dif_matrix)
