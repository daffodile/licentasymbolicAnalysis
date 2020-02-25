from random import randint

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from TESPAR.Coder import Coder

# def update(centroids, df):
#     for i in centroids.keys():
#         centroids[i][0] = np.mean(df[df['closest'] == i][0])
#         centroids[i][1] = np.mean(df[df['closest'] == i][1])
#     return centroids
#
# def assignment(df, centroids, colmap):
#     for i in centroids.keys():
#         # sqrt((x1 - x2)^2 - (y1 - y2)^2)
#         df['distance_from_{}'.format(i)] = (
#             np.sqrt(
#                 (df[0] - centroids[i][0]) ** 2
#                 + (df[1] - centroids[i][1]) ** 2
#             )
#         )
#     centroid_distance_cols = ['distance_from_{}'.format(i) for i in centroids.keys()]
#     df['closest'] = df.loc[:, centroid_distance_cols].idxmin(axis=1)
#     df['closest'] = df['closest'].map(lambda x: int(x.lstrip('distance_from_')))
#     df['color'] = df['closest'].map(lambda x: colmap[x])
#     return df
#
#
# class KMeans:
#
#     def __init__(self):
#         self.initialize()
#
#     def initialize(self):
#         cd = Coder('channel0.txt')
#         a = np.asmatrix(cd.test_matrix)
#         df = pd.DataFrame(a)
#         # df = pd.DataFrame(cd.test_matrix)
#
#         np.random.seed(200)
#         k = 6
#         # centroids[i] = [x, y]
#         centroids = {
#             i + 1: [np.random.randint(0, 260), np.random.randint(0, 883)]
#             for i in range(k)
#         }
#
#         fig = plt.figure(figsize=(5, 5))
#         plt.scatter(df[0], df[1], color='k')
#         colmap = {1: 'r', 2: 'g', 3: 'b',
#                   4: 'c', 5: 'm', 6: 'y'}
#         for i in centroids.keys():
#             plt.scatter(*centroids[i], color=colmap[i])
#         plt.xlim(0, 260)
#         plt.ylim(0, 883)
#         plt.show()
#         # assignment
#
#         df2 = assignment(df, centroids, colmap)
#         print(df2.head())
#
#         fig = plt.figure(figsize=(5, 5))
#         plt.scatter(df2[0], df2[1], color=df2['color'], alpha=0.5, edgecolor='k')
#         for i in centroids.keys():
#             plt.scatter(*centroids[i], color=colmap[i])
#         plt.xlim(0, 260)
#         plt.ylim(0, 883)
#         plt.show()
#
#         #update
#         old_centroids = copy.deepcopy(centroids)
#         centroids = update(centroids, df2)
#
#         fig = plt.figure(figsize=(10, 10))
#         ax = plt.axes()
#         plt.scatter(df2[0], df2[1], color=df2['color'], alpha=0.5, edgecolor='k')
#         for i in centroids.keys():
#             plt.scatter(*centroids[i], color=colmap[i])
#         plt.xlim(0, 260)
#         plt.ylim(0, 883)
#         for i in old_centroids.keys():
#             old_x = old_centroids[i][0]
#             old_y = old_centroids[i][1]
#             dx = (centroids[i][0] - old_centroids[i][0]) * 0.75
#             dy = (centroids[i][1] - old_centroids[i][1]) * 0.75
#             ax.arrow(old_x, old_y, dx, dy, head_width=2, head_length=3, fc=colmap[i], ec=colmap[i])
#         plt.show()

from sklearn.cluster import KMeans

# here number of clusters
k = 32

cd = Coder('DataSet/lightFiltered/stimulus')
a = np.asmatrix(cd.test_matrix)
df = pd.DataFrame(a)
kmeans = KMeans(n_clusters=k)
kmeans.fit(df)

labels = kmeans.predict(df)
print(labels)
centroids = kmeans.cluster_centers_
fig = plt.figure(figsize=(5, 5))

# colmap = {1: 'r', 2: 'g', 3: 'b',
#           4: 'c', 5: 'm', 6: 'y'}

# generate 32 of random colors to be the labels of clusters
colmap = []
for i in range(k):
    colmap.append('#%06X' % randint(0, 0xFFFFFF))

colors = map(lambda x: colmap[x], labels)

plt.scatter(df[0], df[1], color=list(colors), alpha=0.5, edgecolor='k')
for idx, centroid in enumerate(centroids):
    plt.scatter(*centroid, color=colmap[idx])
# plt.xlim(0, 250)
# plt.ylim(0, 250)
plt.show()

'''
#  before, for 6 clusters

from sklearn.cluster import KMeans

cd = Coder('channel0.txt')
a = np.asmatrix(cd.test_matrix)
df = pd.DataFrame(a)
kmeans = KMeans(n_clusters=6)
kmeans.fit(df)

labels = kmeans.predict(df)
print(labels)
centroids = kmeans.cluster_centers_
fig = plt.figure(figsize=(5, 5))
colmap = {1: 'r', 2: 'g', 3: 'b',
          4: 'c', 5: 'm', 6: 'y'}
colors = map(lambda x: colmap[x + 1], labels)

plt.scatter(df[0], df[1], color=colors, alpha=0.5, edgecolor='k')
for idx, centroid in enumerate(centroids):
    plt.scatter(*centroid, color=colmap[idx + 1])
plt.xlim(0, 260)
plt.ylim(0, 883)
plt.show()
'''