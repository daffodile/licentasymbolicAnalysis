import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_dataset_clusters(self, current_k, title):
    # figure
    fig, ax1 = plt.subplots()
    fig.set_size_inches(13, 10)

    # labels
    ax1.set_xlabel('D')
    ax1.set_ylabel('S')
    ax1.set_title(str(current_k) + ' ' + title)

    d_axis = []
    s_axis = []
    clusters = []

    for patterns in self.dataset:
        if patterns[2] > 0:
            d_axis.append(patterns[0])
            s_axis.append(patterns[1])
            clusters.append(self.dataset_clusters[patterns[0] * self.dimS + patterns[1]])
    norm_data = pd.DataFrame({'d_axis': d_axis, 's_axis': s_axis, 'cluster_values': clusters})

    clusters_range = []
    c_x = []
    c_y = []
    c_counts = []

    for c in range(current_k):
        if len(self.clusters[c].patterns) == 0:
            print(str(current_k) + ' e gol \n')
        clusters_range.append(c)
        c_x.append(self.clusters[c].centroid[0])
        c_y.append(self.clusters[c].centroid[1])
        c_counts.append(len(self.clusters[c].patterns))  # here count the nr of elem in cluster

    sns.set()

    diverge = sns.diverging_palette(h_neg=240, h_pos=10, n=current_k)
    g = sns.scatterplot(data=norm_data, x='d_axis', y='s_axis', hue='cluster_values', edgecolor='none',
                        palette=diverge, legend=False)

    plt.scatter(c_x, c_y, color='red', s=0.5)  # centroids here

    if (current_k > 30):
        plt.savefig('{}_alphabet_dsfinal.png'.format(current_k))
    fig.show()


alphabet_path = "alphabet.txt"
alphabet_matrix = np.loadtxt(fname=alphabet_path, dtype='i')
plt.matshow(alphabet_matrix[:100, ])
plt.gca().invert_yaxis()
plt.tick_params(axis='x', labelbottom=True)
plt.tick_params(axis='x', labeltop=False)
plt.tick_params(axis='x', top=False)
plt.xlabel("S")
plt.ylabel("D")
plt.colorbar()
plt.title("Alphabet")
plt.show()
# ax = sns.heatmap(alphabet_matrix[:100, ], cmap="YlGnBu")
# plt.show()
