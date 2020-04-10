import matplotlib.pyplot as plt
import numpy as np

from utils.Utils import get_channel_trials_segment_values_and_outsiders


def plot_matrix_A(DOA, segment, channel_number, values, title):
    fig = plt.figure(figsize=(30, 25))
    ax = fig.add_subplot()
    cax = ax.matshow(values, cmap=plt.cm.jet_r)
    cbar = fig.colorbar(cax)
    if (title[0:3] != 'Log'):
        cbar.mappable.set_clim(0, 500.0)
    cbar.mappable.set_clim(0, 4)
    cbar.ax.tick_params(labelsize=30)
    ax.tick_params(labelsize=30)
    ax.invert_yaxis()
    ax.xaxis.tick_bottom()
    fig.suptitle(title + DOA + " " + segment + " ch: " + str(channel_number), fontsize=35, y=0.99,
                 fontweight='bold')
    plot_name = 'compare_channels/ch' + str(channel_number) + "_" + DOA + "_" + segment + "_A.png"
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
    plot_name = 'ch' + str(channel_number) + "_" + DOA + "_" + segment + "_A.png"
    plt.show()
    fig.savefig(plot_name)


def get_matrix_A(encoding, doas, doa_level, segment, channel_number, log):
    channel_trials_values, channel_trials_outsiders = get_channel_trials_segment_values_and_outsiders(doas, doa_level,
                                                                                                      segment,
                                                                                                      channel_number)
    a_matrix_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
    for i in range(len(channel_trials_values)):
        a_matrix = encoding.get_a(channel_trials_values[i], channel_trials_outsiders[i])
        a_matrix_all = np.add(a_matrix_all, a_matrix)
    if (log == True):
        a_matrix_all = np.log10(a_matrix_all + 1)
        title = 'Log A Matrix '
    else:
        title = 'A Matrix '
    plot_matrix_A(DOA=doa_level, segment=segment, channel_number=channel_number, values=a_matrix_all, title=title)


def get_matrix_A(encoding, doas, doa_level, segment, channel_number, log):
    channel_trials_values, channel_trials_outsiders = get_channel_trials_segment_values_and_outsiders(doas, doa_level,
                                                                                                      segment,
                                                                                                      channel_number)
    a_matrix_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
    for i in range(len(channel_trials_values)):
        a_matrix = encoding.get_a(channel_trials_values[i], channel_trials_outsiders[i])
        a_matrix_all = np.add(a_matrix_all, a_matrix)
    if (log == True):
        a_matrix_all = np.log10(a_matrix_all + 1)
        title = 'Log A Matrix '
    else:
        title = 'A Matrix '
    plot_matrix_A(DOA=doa_level, segment=segment, channel_number=channel_number, values=a_matrix_all, title=title)



# for i in range(len(all_channels)):
#     channel_value_deep = get_channel_values(doas, 0, all_channels[i])
#     channel_value_light = get_channel_values(doas, 2, all_channels[i])
#     a_matrix_deep = np.array(encoder.get_a(channel_value_deep, 1))
#     a_matrix_light = np.array(encoder.get_a(channel_value_light, 1))
#     dif_matrix = a_matrix_deep - a_matrix_light
#     plotMatrixA_Difference("Deep-Light", "Spontaneous", all_channels[i], dif_matrix)