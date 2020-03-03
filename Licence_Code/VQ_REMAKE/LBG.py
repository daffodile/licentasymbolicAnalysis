import os
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd
import seaborn as sns


# https://github.com/marronedantas/Vector-Quantization---LBG/blob/master/Vector_Quantization.py

class CLUSTER:

    def __init__(self, centroid: list):

        self.patterns = []
        self.centroid = centroid
        self.old_error = 0  # corresponding to distortion from the LBG alg
        self.new_error = 0

    def add_pattern(self, pattern):

        self.patterns.append(pattern)

    def update_centroid(self):

        sum_d = 0
        sum_s = 0
        sum_freq = 0
        for pattern in self.patterns:
            sum_d += pattern[0] * pattern[2]  # suma ponderata data de freq
            sum_s += pattern[1] * pattern[2]
            sum_freq += pattern[2]

        self.centroid = [sum_d / sum_freq, sum_s / sum_freq]

    def get_distance_centroid(self, pattern, scale_s):

        dist_d = abs(self.centroid[0] - pattern[0])  # centroid.d - pattern.d
        dist_s = abs(self.centroid[1] - pattern[1])  # centroid.s - pattern.s

        # ! scale_s to increase importance of s dist
        return np.sqrt(dist_d ** 2 + scale_s * (dist_s ** 2))  # sqrt euclidean dist

    def clean_patterns(self):

        self.patterns = []

    def set_cluster_error(self, scale_s):

        total_error = 0

        for pattern in self.patterns:
            total_error += self.get_distance_centroid(pattern, scale_s) * pattern[2]

        self.old_error = self.new_error
        self.new_error = total_error

    def get_relative_error(self):
        if self.new_error != 0:
            return abs(self.new_error - self.old_error) / self.new_error
        else:
            print(' eroare 0 ' + str(self.centroid[0]) + ' ' + str(self.centroid[1]))
            return 0

    def get_partial_distortion(self):

        return self.new_error

    def print_cluster(self, f):

        # print("-----CENTROID-------")

        # print(self.centroid)
        np.savetxt(f, self.centroid, fmt="%s", newline=" ")
        f.write("\n")

        # print("-------PATTERNS-----")
        f.write("-------PATTERNS-----\n")

        # print(self.patterns)
        np.savetxt(f, self.patterns, fmt="%s", newline=" ")
        f.write("\n")

        # print("------------")
        f.write("------------")


class VQ_LGB():
    '''
    k=number of clusters
    alpha = threshold for distortion of overall alg
    t = max nr of iterations
    scale_s = how important to be s in the error/ distortion calculation
    epsilon = how much to recenter the clusters
    '''

    def __init__(self, k, alpha, t, scale_s, epsilon):

        self.dataset = []
        self.k = k
        self.alpha = alpha
        self.t = t
        self.scale_s = scale_s
        self.epsilon = epsilon
        self.clusters = []
        self.old_distortion = 0
        self.new_distortion = 0
        self.codebook = []
        # resulting cluster corresponding to an input of dataset
        self.dataset_clusters = []
        # mai am dimS, dimD din set_dataset
        self.dimD = None
        self.dimS = None

    def set_dataset(self, input_matrix):
        self.dimD = len(input_matrix)
        self.dimS = len(input_matrix[0])

        for d in range(len(input_matrix)):
            for s in range(len(input_matrix[0])):
                self.dataset.append([d, s, input_matrix[d][s]])

        self.dataset_clusters = [0 for i in range(len(self.dataset))]

    def first_cluster(self):
        sum_d = 0
        sum_s = 0
        sum_freq = 0
        for pattern in self.dataset:
            sum_d += pattern[0] * pattern[2]  # suma ponderata data de freq
            sum_s += pattern[1] * pattern[2]
            sum_freq += pattern[2]

        self.clusters.append(CLUSTER([sum_d / sum_freq, sum_s / sum_freq]))

        # self.allocate_closest_cluster()

    # def set_codebook(self):
    #
    #     for index in range(len(self.clusters)):
    #         self.codebook.append(self.clusters[index].centroid)
    #
    # def get_codebook(self):
    #
    #     return np.asarray(self.codebook)

    def clean_clusters(self):

        for index in range(len(self.clusters)):
            self.clusters[index].clean_patterns()

    def add_cluster(self, centroid):
        cluster = CLUSTER(centroid)
        self.clusters.append(cluster)

    def remove_cluster(self, cluster):
        self.clusters.remove(cluster)

    # split cluster having the highest relative error
    def get_highest_relative_error_index(self):
        highest_error = -1
        highest_error_index = -1

        for index in range(len(self.clusters)):

            absolute_error = self.clusters[index].get_relative_error()

            if absolute_error > highest_error:
                highest_error = absolute_error
                highest_error_index = index

        return highest_error_index

    def allocate_closest_cluster(self):

        for idx, pattern in enumerate(self.dataset):

            lowest_distance = float("inf")
            lowest_index = -1

            for index in range(len(self.clusters)):

                distance = self.clusters[index].get_distance_centroid(pattern, self.scale_s)

                if distance < lowest_distance:
                    lowest_distance = distance
                    lowest_index = index

            self.clusters[lowest_index].add_pattern(pattern)
            if pattern[2] == 0:
                self.dataset_clusters[idx] = -1
            else:
                self.dataset_clusters[idx] = lowest_index

    def update_centroids(self):

        for index in range(len(self.clusters)):
            self.clusters[index].update_centroid()

    def set_distortion(self):

        distortion = 0

        for index in range(len(self.clusters)):
            # update individual errors per clusters
            self.clusters[index].set_cluster_error(self.scale_s)

            distortion += self.clusters[index].get_partial_distortion()

        # on whole algorithm
        self.old_distortion = self.new_distortion
        self.new_distortion = distortion

    def get_distortion_flag(self):

        return abs(self.old_distortion - self.new_distortion) / self.new_distortion

    def plot_dataset_clusters(self, current_k, title):

        # print('in plot_dataset_clusters\n')

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

        # for patterns in self.dataset:
        #     d_axis.append(patterns[0])
        #     s_axis.append(patterns[1])
        # norm_data = pd.DataFrame({'d_axis': d_axis, 's_axis': s_axis, 'cluster_values': self.dataset_clusters})

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

        # cmap = sns.cubehelix_palette(dark=.8, light=.3, as_cmap=True, n_colors=current_k)
        # x = sns.dark_palette(n_colors=current_k, color='blue', )

        diverge = sns.diverging_palette(h_neg=240, h_pos=10, n=current_k)

        # diverge = sns.color_palette(n_colors=current_k, desat=0.3)

        g = sns.scatterplot(data=norm_data, x='d_axis', y='s_axis', hue='cluster_values', edgecolor='none',
                            palette=diverge, legend=False)

        # heatmap_matrix = np.reshape(self.dataset_clusters, (self.dimD, self.dimS))
        # sns.heatmap(data=heatmap_matrix, cbar=True)

        plt.scatter(c_x, c_y, color='black', s=0.5)  # centroids here

        plt.savefig('{} window s5.png'.format(current_k))
        fig.show()

    def run(self):

        # start with 1 cluster representing the average of th dataset
        self.first_cluster()

        current_k = 1

        # Make twice to initiate distortions
        for i in range(2):
            # Clear the patterns on the clusters
            self.clean_clusters()

            # Allocate the initial patterns to the clusters
            self.allocate_closest_cluster()  # distance with scale_s

            # First update
            self.update_centroids()

            # Set the first distortion
            self.set_distortion()

        while current_k <= self.k:

            t_partial = 1

            # while < max number of iterations t and relative distortion is less than a threshold alpha
            while (t_partial < self.t) and (self.get_distortion_flag() > self.alpha):
                # Clear the patterns on the clusters
                self.clean_clusters()

                # Allocate the patterns to the clusters
                self.allocate_closest_cluster()

                # Update centroids
                self.update_centroids()

                # Set the new distortion
                self.set_distortion()

                # Update t_patial
                t_partial += 1

            # afiseaza clusterele pe culori ################################################################
            print('k=' + str(current_k) + '\n')
            # m = np.reshape(self.dataset_clusters, (100, 50))
            # print(m)
            if current_k % 5 == 0 or current_k == 32:
                print('aici ar trebui sa printez')
                self.plot_dataset_clusters(current_k, 'cutoff 1 clusters s3 window')

            # self.plot_dataset_clusters(current_k)

            if current_k < 32:
                # find the cluster having the highest relative error
                cluster_to_replace = self.clusters[self.get_highest_relative_error_index()]

                d1 = cluster_to_replace.centroid[0] - self.epsilon
                s1 = cluster_to_replace.centroid[1] - self.epsilon

                d2 = cluster_to_replace.centroid[0] + self.epsilon
                s2 = cluster_to_replace.centroid[1] + self.epsilon

                # remove that cluster
                self.remove_cluster(cluster_to_replace)

                # slightly replace the removed cluster with 2 closed ones
                # c.d-e, c.s-e
                self.add_cluster([d1, s1])

                #  c.d + e, c.s + e
                self.add_cluster([d2, s2])

                # Clear the patterns on the clusters
                self.clean_clusters()

                # Allocate the patterns to the clusters
                self.allocate_closest_cluster()

                # Update centroids
                self.update_centroids()

                # Set the new distortion
                self.set_distortion()

            else:
                # path = os.getcwd()
                # fileName = path + "/symbols_cutoff3_s5_unsorted_fdw.txt"
                # f = open(fileName, "w")
                # for d in range(self.dimD):
                #     for s in range(self.dimS):
                #         f.write(str(self.dataset_clusters[self.dimS * d + s]) + " ")
                #     f.write("\n")
                # f.close()

                #     sort clusters by D and S

                # clean patterns array, only keep centroids
                self.clean_clusters()

                # sort the clusters based on centroid which is am array with D and S
                a = np.array(self.clusters, dtype=CLUSTER)
                # np.sort(a, order='centroid[0]')
                # result = sorted(a, key=lambda x: x.centroid[0].fget)
                result = sorted(a, key=lambda x: getattr(x, 'centroid'))

                # replace the clusters with sorted ones
                self.clusters = result

                # re-distribute the symbols
                self.allocate_closest_cluster()

                self.plot_dataset_clusters(current_k, 'cutoff1 clusters s5 sorted')
                path = os.getcwd()
                fileName = path + "/symbols_cutoff1_s5_sorted_fdw.txt"
                f = open(fileName, "w")
                for d in range(self.dimD):
                    for s in range(self.dimS):
                        f.write(str(self.dataset_clusters[self.dimS * d + s]) + " ")
                    f.write("\n")
                f.close()

            current_k += 1
