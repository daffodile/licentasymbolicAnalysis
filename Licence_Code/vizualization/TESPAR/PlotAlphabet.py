import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_dataset_clusters(alphabet, cut_d, cut_s):
    alphabet_path = "../../data_to_be_saved/" + alphabet + ".txt"
    alphabet_matrix = np.loadtxt(fname=alphabet_path, dtype='i')

    ds_matrix = np.loadtxt(fname="../../data_to_be_saved/ds_freq.txt", dtype='i')

    # figure
    fig, ax1 = plt.subplots()
    fig.set_size_inches(13, 10)

    # labels
    ax1.set_xlabel('D', fontsize=18)
    ax1.set_ylabel('S', fontsize=18)

    d_axis = []
    s_axis = []
    clusters = []

    for ind_d in range(cut_d):
        for ind_s in range(cut_s):
            if (ds_matrix[ind_d][ind_s] != 0):
                d_axis.append(ind_d)
                s_axis.append(ind_s)
                clusters.append(alphabet_matrix[ind_d][ind_s])

    norm_data = pd.DataFrame({'d_axis': d_axis, 's_axis': s_axis, 'cluster_values': clusters})
    nr_of_colors = len(np.unique(norm_data['cluster_values']))

    sns.set()

    # diverge = sns.diverging_palette(h_neg=240, h_pos=10, n=nr_of_colors)
    diverge = sns.color_palette("Paired", nr_of_colors)
    g = sns.scatterplot(data=norm_data, x='d_axis', y='s_axis', hue='cluster_values', edgecolor='none',
                        palette=diverge, legend="full", marker="s")

    plt.title(alphabet, fontsize=20)
    plt.savefig(alphabet + '_' + str(cut_d) + '.png')
    fig.show()
