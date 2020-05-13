import os

import matplotlib.pyplot as plt
import numpy as np

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.Utils import get_all_trials_values_from_doa_by_segment_with_bursts_flags, \
    get_one_trial__all_segments_values_from_doa_by_channel_with_bursts_flags, get_doa_of_level, \
    get_one_trial_segment_values_from_doas_by_channel_with_bursts_flags
from utils.Utils_master import get_channel_trials_segment_values_and_outsiders, get_channel_trials_values_more_seg


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


def get_channel_matrix_A(encoding, doas, doa_level, segment, channel_number, log):
    channel_trials_values, channel_trials_outsiders = get_all_trials_values_from_doa_by_segment_with_bursts_flags(doas,
                                                                                                                  doa_level,
                                                                                                                  segment,
                                                                                                                  channel_number)
    a_matrix_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
    for i in range(len(channel_trials_values)):
        a_matrix = encoding.get_a(channel_trials_values[i], channel_trials_outsiders[i])
        a_matrix_all = np.add(a_matrix_all, a_matrix)
    if (log == True):
        a_matrix_all = np.log10(a_matrix_all + 1)
        title = 'Log A Matrix '
        plot_name = 'log_ch'
    else:
        title = 'A Matrix '
        plot_name = 'ch'
    title += doa_level + " " + segment + " ch: " + str(channel_number)
    plot_name += str(channel_number) + "_" + doa_level + "_" + segment + "_A.png"
    plot_matrix_A(values=a_matrix_all, title=title, plot_name=plot_name)


def get_channel_trial_matrix_A(encoding, doas, doa_level, channel_number, trial_number, log):
    channel_trial_values, channel_trial_outsiders = get_one_trial__all_segments_values_from_doa_by_channel_with_bursts_flags(
        doas, doa_level, channel_number, trial_number)

    a_matrix = encoding.get_a(channel_trial_values, channel_trial_outsiders)
    if (log == True):
        a_matrix = np.log10(a_matrix + 1)
        title = 'Log A Matrix '
        plot_name = 'log_ch'
    else:
        title = 'A Matrix '
        plot_name = 'ch'
    title += doa_level + " " + " ch: " + str(channel_number) + " tr: " + str(trial_number)
    plot_name += str(channel_number) + "_" + str(trial_number) + "_" + doa_level + "_A.png"
    plot_matrix_A(values=a_matrix, title=title, plot_name=plot_name)


def get_channels_difference_matrix_A(encoding, doas, doa_levels, segment, channels, log):
    # def get_all_trials_values_from_doa_by_segment_with_bursts_flags(doas, level, segment, channel_number):
    channel1_trials_values, channel1_trials_outsiders = get_all_trials_values_from_doa_by_segment_with_bursts_flags(
        doas, doa_levels[0], segment, channels[0])
    channel2_trials_values, channel2_trials_outsiders = get_all_trials_values_from_doa_by_segment_with_bursts_flags(
        doas, doa_levels[1], segment, channels[1])

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
        plot_name = 'log_ch'
    else:
        title = 'A Matrix Diff ' + str(channels[0]) + " "
        plot_name = 'ch'

    diff_matrix = a_matrix1_all - a_matrix2_all

    title += doa_levels[0] + "-" + doa_levels[1]
    doa_levels[1] + " " + segment + " ch: " + str(channels[0]) + "-" + str(channels[1])
    plot_name += str(channels[0]) + "_" + doa_levels[0] + "-" + doa_levels[
        1] + "_" + segment + "_A.png"
    plot_matrix_A_Difference(values=diff_matrix, title=title, plot_name=plot_name)


def get_channel_matrix_S(encoding, doas, doa_level, segment, channel_number, log):
    channel_trials_values, channel_trials_outsiders = get_channel_trials_segment_values_and_outsiders(doas, doa_level,
                                                                                                      segment,
                                                                                                      channel_number)
    all_symbols = []
    for i in range(len(channel_trials_values)):
        symbols = encoding.get_symbols(channel_trials_values[i], channel_trials_outsiders[i])
        all_symbols.extend(symbols)
    title = 'S Matrix ' + doa_level + " " + segment + " ch: " + str(channel_number)
    plot_name = 'ch' + str(channel_number) + "" + doa_level + "" + segment + "_S.png"
    plot_matrix_S(values=all_symbols, title=title, plot_name=plot_name)


def get_matrices_S_more_doas(encoding, doas, doa_levels, segments, channels, string_about_channels):
    '''
    from_doas[0] -> 15 arrays, one per channel, in an array are the symbols of that channel

    '''
    from_doas = [[] for i in range(len(doa_levels))]

    for ind_doa, doa_level in enumerate(doa_levels):
        for channel_number in channels:
            this_channel_symbols = []
            channel_trials_values = get_channel_trials_values_more_seg(doas, doa_level, channel_number, segments)
            for i in range(len(channel_trials_values)):
                symbols = encoding.get_symbols(channel_trials_values[i])
                this_channel_symbols.extend(symbols)
            from_doas[ind_doa].append(this_channel_symbols)

    fig_name = f'S_matrices_{doa_levels[0]}_{doa_levels[1]} {string_about_channels}.png'
    plot_matrices_S_2_doas(from_doas=from_doas, doa_levels=doa_levels, fig_name=fig_name,
                           string_about_channels=string_about_channels)

    fig_name = f'S_matrices_{doa_levels[0]}_{doa_levels[1]} {string_about_channels}_bar.png'
    plot_matrices_S_2_doas_same_hist(from_doas=from_doas, doa_levels=doa_levels, fig_name=fig_name,
                                     string_about_channels=string_about_channels)


def plot_matrices_S_2_doas(from_doas, doa_levels, fig_name, string_about_channels):
    array_of_hists = [[] for i in range(len(from_doas))]

    fig, axses = plt.subplots(2)

    for ind_doa, doa_level in enumerate(doa_levels):
        plt.subplot(2, 1, ind_doa + 1)
        n, bins, patches = plt.hist(x=from_doas[ind_doa], bins=32)
        plt.cla()

        means_n = np.mean(n, axis=0)
        print(means_n)

        plt.bar(range(len(means_n)), means_n)
        plt.yscale('log', nonposy='clip')
        plt.title(f'S matrix {doa_levels[ind_doa]} {string_about_channels}')
        plt.xlabel("Symbol")
        plt.ylabel("log10(#)")

    plt.savefig(fig_name)  # arg  fig_name = f'S_matrices_{doa_levels[0]}_{doa_levels[1]}.png'
    plt.show()


def plot_matrices_S_2_doas_same_hist(from_doas, doa_levels, fig_name, string_about_channels):
    array_of_hists = [[] for i in range(len(from_doas))]
    for ind_doa, doa_level in enumerate(doa_levels):
        for array_of_symbols in from_doas[ind_doa]:
            array_of_hists[ind_doa].extend(array_of_symbols)

    n, bins, patches = plt.hist(x=array_of_hists, bins=32, label=doa_levels)
    plt.cla()

    n_new = np.array(n)
    n_new = n_new / len(from_doas[0])  # divide by 15 the count as it belongs to all channels
    # data to plot
    n_groups = 32

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.30
    opacity = 0.8
    rects1 = plt.bar(index, n_new[0], bar_width, alpha=opacity, color='b', label=doa_levels[0])
    rects2 = plt.bar(index + bar_width, n_new[1], bar_width, alpha=opacity, color='g', label=doa_levels[1])

    plt.yscale('log', nonposy='clip')
    plt.xlabel("TESPAR Symbol")
    plt.ylabel(f'Mean number of symbols in {len(from_doas[0])} channels, log10(#)')
    plt.title(f'S matrix {doa_levels[0]} - {doa_levels[1]} {string_about_channels}')
    plt.xticks(index + bar_width, index, fontsize=9)
    plt.legend()

    plt.tight_layout()
    plt.savefig(fig_name)  # arg  fig_name = f'S_matrices_{doa_levels[0]}_{doa_levels[1]}.png'
    plt.show()




