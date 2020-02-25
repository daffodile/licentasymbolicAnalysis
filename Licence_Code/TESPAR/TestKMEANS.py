from random import randint

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.cluster import KMeans

# here number of clusters
k = 32

# DS matrix is 100*50
symbols_matrix = np.loadtxt(fname='../Statistics/distributions_100_50/global_matrix_DS.txt', dtype='i')
a = np.asanyarray(symbols_matrix)
df = pd.DataFrame(a)
kmeans = KMeans(n_clusters=k)
kmeans.fit(df)

# labels = kmeans.predict(df)
# print(labels)
# centroids = kmeans.cluster_centers_
# fig = plt.figure(figsize=(5, 5))
#
# # colmap = {1: 'r', 2: 'g', 3: 'b',
# #           4: 'c', 5: 'm', 6: 'y'}
#
# # generate 32 of random colors to be the labels of clusters
# colmap = []
# for i in range(k):
#     colmap.append('#%06X' % randint(0, 0xFFFFFF))
#
# colors = map(lambda x: colmap[x], labels)
#
# plt.scatter(df[0], df[1], color=list(colors), alpha=0.5, edgecolor='k')
# for idx, centroid in enumerate(centroids):
#     plt.scatter(*centroid, color=colmap[idx])
# plt.xlim(0, 100)
# plt.ylim(0, 50)

# ax = sns.heatmap(symbols_matrix)
# plt.savefig("./global_DS_matrix")

fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True, figsize=(10, 6))
ax1.set_title('k means')
ax1.scatter(df[0], df[1], c=kmeans.labels_, cmap='rainbow')
plt.xlim(0, 10000)
plt.ylim(0, 10000)
plt.show()
