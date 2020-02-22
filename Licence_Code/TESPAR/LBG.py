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
        self.relative_error = [0, 0]
        self.absolute_error = [0, 0]

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

    def get_distance_centroid(self, pattern):

        dist_d = abs(self.centroid[0] - pattern[0])  # centroid.d - pattern.d
        dist_s = abs(self.centroid[1] - pattern[1])  # centroid.s - pattern.s

        return dist_d ** 2 + dist_s ** 2  # non sqrt euclidean dist

    def clean_patterns(self):

        self.patterns = []

    def get_partial_distortion(self):

        partial_distortion = 0

        # sum of all dist inside this cluster * freq of that  DS combination
        for index in range(len(self.patterns)):
            partial_distortion += self.get_distance_centroid(self.patterns[index]) * self.patterns[index][2]

        return partial_distortion

    # return the average value of the relative errors among this patterns list
    def get_relative_error(self):
        relative_error = [0, 0]
        count = 0
        if len(self.patterns) != 0:
            for pattern in self.patterns:
                relative_error[0] += abs(self.centroid[0] - pattern[0]) / pattern[0] * pattern[2]
                relative_error[1] += abs(self.centroid[1] - pattern[1]) / pattern[0] * pattern[2]
                count += pattern[2]

            self.relative_error = np.array(relative_error) / count

        return self.relative_error

    # return the average value of the absolute errors among this patterns list
    def get_absolute_error(self):
        absolute_error = [0, 0]
        count = 0
        if len(self.patterns) != 0:
            for pattern in self.patterns:
                absolute_error[0] += abs(self.centroid[0] - pattern[0]) * pattern[2]
                absolute_error[1] += abs(self.centroid[1] - pattern[1]) * pattern[2]
                count += pattern[2]

            self.absolute_error = np.array(absolute_error) / count

        return self.absolute_error

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

    def __init__(self, k, alpha, t, freq_replacer, scale_s, epsilon):

        self.dataset = []
        self.k = k
        self.alpha = alpha
        self.t = t
        self.freq_replacer = freq_replacer  # 10^-5 for example
        self.scale_s = scale_s
        self.epsilon = epsilon
        self.clusters = []
        self.old_distortion = 0
        self.new_distortion = 0
        self.codebook = []
        # resulting cluster corresp to an input of dataset
        self.dataset_clusters = []
        # mai am dimS, dimD din set_dataset
        self.dimD = None
        self.dimS = None

    def set_dataset(self, input_matrix):
        self.dimD = len(input_matrix)
        self.dimS = len(input_matrix[0])

        for d in range(len(input_matrix)):
            for s in range(len(input_matrix[0])):
                # self.dataset.append([d, s, input_matrix[d][s]])
                if input_matrix[d][s] > 0:
                    self.dataset.append([d, s, input_matrix[d][s]])
                else:
                    self.dataset.append([d, s, self.freq_replacer])

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

    # now it is ABSOLUTE error
    def get_highest_relative_error_index(self):
        highest_error = [-1, -1]
        highest_error_index = -1

        for index in range(len(self.clusters)):

            relative_error = self.clusters[index].get_absolute_error()

            if relative_error[0] > highest_error[0] or relative_error[1] > highest_error[1]:
                highest_error = relative_error
                highest_error_index = index

        return highest_error_index

    def allocate_closest_cluster(self):

        for idx, pattern in enumerate(self.dataset):

            lowest_distance = float("inf")
            lowest_index = -1

            for index in range(len(self.clusters)):

                distance = self.clusters[index].get_distance_centroid(pattern)

                if distance < lowest_distance:
                    lowest_distance = distance
                    lowest_index = index

            self.clusters[lowest_index].add_pattern(pattern)
            self.dataset_clusters[idx] = lowest_index

    def update_centroids(self):

        for index in range(len(self.clusters)):
            self.clusters[index].update_centroid()

    def set_distortion(self):

        distortion = 0

        for index in range(len(self.clusters)):
            distortion += self.clusters[index].get_partial_distortion()

        self.old_distortion = self.new_distortion
        self.new_distortion = distortion

    def get_distortion_flag(self):

        return (self.old_distortion - self.new_distortion) / self.new_distortion

    def plot_dataset_clusters(self, current_k):

        print('in plot_dataset_clusters\n')
        # figure
        fig, ax1 = plt.subplots()
        fig.set_size_inches(13, 10)

        # labels
        ax1.set_xlabel('D')
        ax1.set_ylabel('S')
        ax1.set_title(str(current_k) + 'clusters')

        d_axis = []
        s_axis = []
        for patterns in self.dataset:
            d_axis.append(patterns[0])
            s_axis.append(patterns[1])

        clusters_range = []
        c_x = []
        c_y = []

        for c in range(current_k):
            clusters_range.append(c)
            c_x.append(self.clusters[c].centroid[0])
            c_y.append(self.clusters[c].centroid[1])

        norm_data = pd.DataFrame({'d_axis': d_axis, 's_axis': s_axis, 'cluster_values': self.dataset_clusters})

        # norm_data = pd.DataFrame({'d_axis': d_axis, 's_axis': s_axis})

        # norm_data.assign(cluster_value=lambda x: self.dataset_clusters[self.dimD * x['d_axis'] + x['s_axis']])
        # norm_data.assign(cluster_value=self.dataset_clusters[norm_data['d_axis']*self.dimD+norm_data['s_axis']])

        sns.set()

        cmap = sns.cubehelix_palette(dark=.3, light=.8, as_cmap=True)

        sns.scatterplot(data=norm_data, x='d_axis', y='s_axis', hue='cluster_values', edgecolor='none', palette=cmap)
        sns.heatmap()
        plt.scatter(c_x, c_y, color='red')
        plt.show()

    def run(self):

        # start with 1 cluster representing the average of th dataset
        self.first_cluster()

        current_k = 1

        # Make twice to initiate distortions
        for i in range(2):
            # Clear the patterns on the clusters
            self.clean_clusters()

            # Allocate the initial patterns to the clusters
            self.allocate_closest_cluster()

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

                # Alocate the patterns to the clusters
                self.allocate_closest_cluster()

                # Update centroids
                self.update_centroids()

                # Set the new distortion
                self.set_distortion()

                # Update t_patial
                t_partial += 1

            # afiseaza clusterele pe culori #####################################################################
            print('k=' + str(current_k) + '\n')
            # m = np.reshape(self.dataset_clusters, (100, 50))
            # print(m)
            self.plot_dataset_clusters(current_k)

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

            # Alocate the patterns to the clusters
            self.allocate_closest_cluster()

            # Update centroids
            self.update_centroids()

            # Set the new distortion
            self.set_distortion()

            current_k += 1
