import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import gridspec

from tests.Tespar.Encoding_before_checking_bursts import Encoding

encoder = Encoding('../../data_to_be_saved/alphabet_1_150hz.txt')


def plot_S_matrix(s_matrix, DOA, trial, segment, channel_nr):
    plt.plot(s_matrix, bins=32)
    plt.yscale('log', nonposy='clip')
    plt.title("S Matrix " + DOA + " " + str(trial) + " " + segment + " ch: " + str(channel_nr))
    plt.xlabel("Symbol")
    plt.ylabel("log10(#)")
    plot_name = 'S/channel' + str(channel_nr) + "_" + DOA + "_" + segment + "_S.png"
    plt.savefig(plot_name)
    plt.show()


def plot_A_matrix(a_matrix, DOA, segment, channel_nr):
    # ax = sns.heatmap(np.log10([[v + 1 for v in r] for r in a_matrix]), cmap="YlGnBu", vmin=0, vmax=1)
    ax = sns.heatmap(a_matrix, cmap="YlGnBu", vmin=0, vmax=8)
    ax.invert_yaxis()
    plt.xlabel("Symbols")
    plt.ylabel("Symbols")
    plt.title("A Matrix " + DOA + " " + segment + " ch: " + str(channel_nr))
    # plot_name = 'compare_channels/channel' + str(channel_nr) + "_" + DOA + "_" + segment + "_A.png"
    # plt.savefig(plot_name)
    plt.show()
    return plt


def matrixA_1channel_differences(doas, ch_nr, trial_nr, segment):
    t_deep = doas[0].channels[ch_nr].trials[trial_nr]
    t_light = doas[2].channels[ch_nr].trials[trial_nr]

    deep_spontaneous_a = encoder.get_a(t_deep.spontaneous.values, 1)
    light_spontaneous_a = encoder.get_a(t_light.spontaneous.values, 1)
    # diff_spontaneous = np.absolute(np.array(deep_spontaneous_a) - np.array(light_spontaneous_a))
    diff_spontaneous = (np.array(deep_spontaneous_a) - np.array(light_spontaneous_a))

    # Create 1x3 sub plots
    gs = gridspec.GridSpec(1, 3)

    fig = plt.figure(figsize=(15, 5))
    ax1 = plt.subplot(gs[0, 0])  # row 0, col 0
    ax1 = sns.heatmap(np.log10([[v + 1 for v in r] for r in deep_spontaneous_a]), cmap="YlGnBu", vmin=0, vmax=1)
    ax1.invert_yaxis()
    fig.add_subplot(ax1)

    ax2 = plt.subplot(gs[0, 1])  # row 0, col 1
    ax2 = sns.heatmap(np.log10([[v + 1 for v in r] for r in light_spontaneous_a]), cmap="YlGnBu", vmin=0, vmax=1)
    ax2.invert_yaxis()
    fig.add_subplot(ax2)

    ax3 = plt.subplot(gs[0, 2])  # row 0, col 2
    ax3 = sns.heatmap(np.log10([[v + 1 for v in r] for r in diff_spontaneous]), cmap="YlGnBu", vmin=0, vmax=1)
    ax3.invert_yaxis()
    fig.add_subplot(ax3)

    fig.suptitle("Deep and Light Analysis on Channel " + str(ch_nr) + " Trial " + str(trial_nr) + " " + segment)

    fig.show()


def matrixA_2channels_differences(doas, ch_nr, trial_nr, segment):
    t_deep = doas[0].channels[ch_nr].trials[trial_nr]
    t_light = doas[2].channels[ch_nr].trials[trial_nr]

    deep_spontaneous_a = encoder.get_a(t_deep.spontaneous.values, 1)
    light_spontaneous_a = encoder.get_a(t_light.spontaneous.values, 1)
    # diff_spontaneous = np.absolute(np.array(deep_spontaneous_a) - np.array(light_spontaneous_a))
    diff_spontaneous = (np.array(deep_spontaneous_a) - np.array(light_spontaneous_a))

    # Create 1x3 sub plots
    gs = gridspec.GridSpec(1, 3)

    fig = plt.figure(figsize=(15, 5))
    ax1 = plt.subplot(gs[0, 0])  # row 0, col 0
    ax1 = sns.heatmap(np.log10([[v + 1 for v in r] for r in deep_spontaneous_a]), cmap="YlGnBu", vmin=0, vmax=1)
    ax1.invert_yaxis()
    fig.add_subplot(ax1)

    ax2 = plt.subplot(gs[0, 1])  # row 0, col 1
    ax2 = sns.heatmap(np.log10([[v + 1 for v in r] for r in light_spontaneous_a]), cmap="YlGnBu", vmin=0, vmax=1)
    ax2.invert_yaxis()
    fig.add_subplot(ax2)

    ax3 = plt.subplot(gs[0, 2])  # row 0, col 2
    ax3 = sns.heatmap(np.log10([[v + 1 for v in r] for r in diff_spontaneous]), cmap="YlGnBu", vmin=0, vmax=1)
    ax3.invert_yaxis()
    fig.add_subplot(ax3)

    fig.suptitle("Deep and Light Analysis on Channel " + str(ch_nr) + " Trial " + str(trial_nr) + " " + segment)

    fig.show()

# from input_reader.InitDataSet import InitDataSet

# initialization = InitDataSet()

# doas = initialization.get_dataset_as_doas()

# matrixA_2channels_differences(doas, 13, 24, "spontaneous")
