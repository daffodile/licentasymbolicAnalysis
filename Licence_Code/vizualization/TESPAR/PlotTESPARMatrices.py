import matplotlib.pyplot as plt
import numpy as np

from utils.Utils import get_channel_trials_segment_values_and_outsiders, get_trial_segment_values_and_outsiders, \
    get_trial_values_and_outsiders, get_doa_of_level


def plot_matrix_S(values, title, plot_name):
    plt.hist(x=values, bins=32)
    plt.yscale('log', nonposy='clip')
    plt.title(title)
    plt.xlabel("Symbol")
    plt.ylabel("log10(#)")
    plt.savefig(plot_name)
    plt.show()


def plot_matrix_A(values, title, plot_name):
    fig = plt.figure(figsize=(30, 25))
    ax = fig.add_subplot()
    cax = ax.matshow(values, cmap=plt.cm.jet)
    cbar = fig.colorbar(cax)
    # if (title[0:3] == 'Log'):
    #     cbar.mappable.set_clim(0, 4)
    # cbar.mappable.set_clim(0, 500.0)
    cbar.ax.tick_params(labelsize=30)
    ax.tick_params(labelsize=30)
    ax.invert_yaxis()
    ax.xaxis.tick_bottom()
    fig.suptitle(title, fontsize=35, y=0.99,
                 fontweight='bold')
    plt.show()
    fig.savefig(plot_name)


def plot_matrix_A_Difference(values, title, plot_name):
    fig = plt.figure(figsize=(30, 25))
    ax = fig.add_subplot()
    cax = ax.matshow(values, cmap=plt.cm.Spectral_r)
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
    fig.suptitle(title, fontsize=35, y=0.99,
                 fontweight='bold')
    plt.show()
    fig.savefig(plot_name)


def get_channel_matrix_S(encoding, doas, doa_level, segment, channel_number, log):
    channel_trials_values, channel_trials_outsiders = get_channel_trials_segment_values_and_outsiders(doas, doa_level,
                                                                                                      segment,
                                                                                                      channel_number)
    all_symbols = []
    for i in range(len(channel_trials_values)):
        symbols = encoding.get_symbols(channel_trials_values[i], channel_trials_outsiders[i])
        all_symbols.extend(symbols)
    title = 'S Matrix ' + doa_level + " " + segment + " ch: " + str(channel_number)
    plot_name = 'compare_channels/ch' + str(channel_number) + "_" + doa_level + "_" + segment + "_S.png"
    plot_matrix_S(values=all_symbols, title=title, plot_name=plot_name)


def get_channel_matrix_A(encoding, doas, doa_level, segment, channel_number, log):
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
        plot_name = 'compare_channels/log_ch'
    else:
        title = 'A Matrix '
        plot_name = 'compare_channels/ch'
    title += doa_level + " " + segment + " ch: " + str(channel_number)
    plot_name += str(channel_number) + "_" + doa_level + "_" + segment + "_A.png"
    plot_matrix_A(values=a_matrix_all, title=title, plot_name=plot_name)


def get_channel_trial_matrix_A(encoding, doas, doa_level, channel_number, trial_number, log):
    doa = get_doa_of_level(doas, doa_level)
    channel_trial_values, channel_trial_outsiders = get_trial_values_and_outsiders(doa, channel_number, trial_number)

    a_matrix = encoding.get_a(channel_trial_values, channel_trial_outsiders)
    if (log == True):
        a_matrix = np.log10(a_matrix + 1)
        title = 'Log A Matrix '
        plot_name = 'compare_channels/log_ch'
    else:
        title = 'A Matrix '
        plot_name = 'compare_channels/ch'
    title += doa_level + " " + " ch: " + str(channel_number) + " tr: " + str(trial_number)
    plot_name += str(channel_number) + "_" + str(trial_number) + "_" + doa_level + "_A.png"
    plot_matrix_A(values=a_matrix, title=title, plot_name=plot_name)


def get_channels_difference_matrix_A(encoding, doas, doa_levels, segment, channels, log):
    channel1_trials_values, channel1_trials_outsiders = get_channel_trials_segment_values_and_outsiders(doas,
                                                                                                        doa_levels[0],
                                                                                                        segment,
                                                                                                        channels[0])
    channel2_trials_values, channel2_trials_outsiders = get_channel_trials_segment_values_and_outsiders(doas,
                                                                                                        doa_levels[1],
                                                                                                        segment,
                                                                                                        channels[1])
    a_matrix1_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
    for i in range(len(channel1_trials_values)):
        a_matrix1 = encoding.get_a(channel1_trials_values[i], channel1_trials_outsiders[i])
        a_matrix1_all = np.add(a_matrix1_all, a_matrix1)

    a_matrix2_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
    for i in range(len(channel2_trials_values)):
        a_matrix2 = encoding.get_a(channel2_trials_values[i], channel2_trials_outsiders[i])
        a_matrix2_all = np.add(a_matrix2_all, a_matrix2)

    if (log == True):
        a_matrix1_all = np.log10(a_matrix1_all + 1)
        a_matrix2_all = np.log10(a_matrix2_all + 1)
        title = 'Log A Matrix Diff '
        plot_name = 'compare_channels/log_ch'
    else:
        title = 'A Matrix Diff'
        plot_name = 'compare_channels/ch'

    diff_matrix = a_matrix1_all - a_matrix2_all

    title += doa_levels[0] + "-"
    doa_levels[1] + " " + segment + " ch: " + str(channels[0]) + "-" + str(channels[1])
    plot_name += str(channels[0]) + "-" + str(channels[1]) + "_" + doa_levels[0] + "-" + doa_levels[
        1] + "_" + segment + "_A.png"
    plot_matrix_A_Difference(values=diff_matrix, title=title, plot_name=plot_name)
