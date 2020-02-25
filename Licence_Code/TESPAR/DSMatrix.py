import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

from DataSet.HighPassFilterPreProcessing import HighPassFilterPreProcessing
from TESPAR.Coder import Coder

file_deep_stimulus = 'DataSet/deep/stimulus'
file_deep_spontaneous = 'DataSet/deep/spontaneous'
file_deep_post = 'DataSet/deep/poststimulus'

file_medium_stimulus = 'DataSet/medium/stimulus'
file_medium_spontaneous = 'DataSet/medium/spontaneous'
file_medium_poststimulus = 'DataSet/medium/poststimulus'

file_light_stimulus = 'DataSet/light/stimulus'
file_light_spontaneous = 'DataSet/light/spontaneous'
file_light_poststimulus = 'DataSet/light/poststimulus'

# total_d = sum(cd.distributionD)
# total_s = sum(cd.distributionS)
# print(total_d)
# print(total_s)
#
# distribution_s = [0] * 210
# distribution_d = [0] * 550
# for i in range(len(cd.distributionS)):
#     distribution_s[i] = cd.distributionS[i]/total_s
# for i in range(len(cd.distributionD)):
#     distribution_d[i] = cd.distributionD[i]/total_d
#
# print(distribution_s)
# print(distribution_d)


filesToOpen = [file_light_stimulus, file_light_spontaneous, file_light_poststimulus,
               file_medium_stimulus, file_medium_spontaneous, file_medium_poststimulus,
               file_deep_stimulus, file_deep_spontaneous, file_deep_post]

mat_global = [[0 for i in range(536)] for j in range(106)]

# for i in range(len(filesToOpen)):
#     # coder for this DOA and segment
#     cd = Coder(filesToOpen[i])
#
#     # add to total freq matrix
#     mat_global = np.add(mat_global, cd.ds_matrix)


input_matrix = np.loadtxt(fname='./global_DS_matrix.txt', dtype='i')

# print(cd.test_matrix)
# plt.xlabel("D")
# plt.ylabel("S")
# plt.title("DS MATRIX")
# plt.matshow(cd.test_matrix)

# temp = [[0 for i in range(100)] for j in range(250)]
# for i in range (250):
#     for j in range (100):
#         temp[i][j] = np.log(input_matrix[i][j])

# wite matrix
# path = os.getcwd()
# fileName = path + "/global_DS_matrix.txt"
# f = open(fileName, "w")
# for d in range(536):
#     for s in range(106):
#         f.write(str(mat_global[d][s]) + " ")
#     f.write("\n")
# f.close()
# print("done writing" )
# cmap = plt.cm.OrRd
# cmap.set_under(color='black')
# plt.imshow(mat_global, interpolation='none', cmap=cmap, vmin=0.0000001)

ax = sns.heatmap(np.log10(input_matrix), cmap="YlGnBu", vmin=0, vmax=7)
ax.invert_yaxis()
plt.xlabel("S")
plt.title("DS frequency log10")
plt.ylabel("D")
plt.show()
