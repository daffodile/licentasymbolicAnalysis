import os

import numpy as np


# https://github.com/marronedantas/Vector-Quantization---LBG/blob/master/Vector_Quantization.py

class CLUSTER:

    def __init__(self, centroid):

        self.patterns = []
        self.centroid = centroid

    def add_pattern(self, pattern):

        self.patterns.append(pattern)

    def set_centroid(self, centroid):

        self.centroid = centroid

    def update_centroid(self):

        if (len(self.patterns) != 0):
            pattern_matrix = np.asanyarray(self.patterns)
            mean_matrix = pattern_matrix.mean(0)
            self.centroid = list(mean_matrix)

    def get_distance_centroid(self, pattern):

        return np.linalg.norm(np.asarray(self.centroid) - np.asarray(pattern))

    def clean_patterns(self):

        self.patterns = []

    def get_partial_distorcion(self):

        partial_distocion = 0

        for index in range(len(self.patterns)):
            partial_distocion += np.linalg.norm(np.asarray(self.centroid) - np.asarray(self.patterns[index]))

        return partial_distocion

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

    def __init__(self, dataset, k, alpha, t):

        self.dataset = dataset
        self.k = k
        self.aplha = alpha
        self.t = t
        self.clusters = []
        self.old_distorcion = 0
        self.new_distorcion = 0
        self.codebook = []

    def set_codebook(self):

        for index in range(len(self.clusters)):
            self.codebook.append(self.clusters[index].centroid)

    def get_codebook(self):

        return np.asarray(self.codebook)

    def clean_clusters(self):

        for index in range(len(self.clusters)):
            self.clusters[index].clean_patterns()

    def add_cluster(self, centroid):

        cluster = CLUSTER(centroid)
        self.clusters.append(cluster)

    def generate_clusters(self):

        indexes = np.random.choice(range(len(self.dataset)), self.k, replace=False)

        for index in indexes:
            self.add_cluster(list(self.dataset[index]))

    def alocate_closest_cluster(self):

        for pattern in self.dataset:

            lowest_distance = float("inf")
            lowest_index = -1

            for index in range(len(self.clusters)):

                distance = self.clusters[index].get_distance_centroid(list(pattern))

                if distance < lowest_distance:
                    lowest_distance = distance
                    lowest_index = index

            self.clusters[lowest_index].add_pattern(list(pattern))

    def update_centroids(self):

        for index in range(len(self.clusters)):
            self.clusters[index].update_centroid()

    def set_distorcion(self):

        distorcion = 0

        for index in range(len(self.clusters)):
            distorcion += self.clusters[index].get_partial_distorcion()

        self.old_distorcion = self.new_distorcion
        self.new_distorcion = distorcion

    def get_distorcion_flag(self):

        return (self.old_distorcion - self.new_distorcion) / self.new_distorcion

    def print_clusters(self):

        file_name = os.getcwd() + "/light_stimulus_filtered_32_clusters.txt"

        f = open(file_name, 'a+')  # so that we append thi sequence of pairs to the file

        count = 0

        for cluster in self.clusters:
            count += 1
            f.write("\n")
            f.write("-----CENTROID  " + str(count)+"  -------\n")
            cluster.print_cluster(f)

    def run(self):

        # Generating the initial clusters

        self.generate_clusters()

        t_partial = 1

        # Make twice to iniate distocions

        for i in range(2):
            # Clear the patterns on the clusters

            self.clean_clusters()

            # Alocate the initial patterns to the clusters

            self.alocate_closest_cluster()

            # First update

            self.update_centroids()

            # Set the first distorcion

            self.set_distorcion()

            # Set the t initial

            t_partial += 1

        # While t_partial is different of max iterations and distorcion flag > alpha

        while ((t_partial < self.t) and (self.get_distorcion_flag() > self.aplha)):
            # Clear the patterns on the clusters

            self.clean_clusters()

            # Alocate the patterns to the clusters

            self.alocate_closest_cluster()

            # Update centroids

            self.update_centroids()

            # Set the new distorcion

            self.set_distorcion()

            # Update t_patial

            t_partial += 1

        # Setting the codebook

        self.set_codebook()
