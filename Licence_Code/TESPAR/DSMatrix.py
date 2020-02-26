import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

from DataSet.HighPassFilterPreProcessing import HighPassFilterPreProcessing
from TESPAR.Coder import Coder

maxD_allocate = 550
maxS_Allocate = 210

file_deep_stimulus = 'DataSet/cutoff1hz/deep/stimulus'
file_deep_spontaneous = 'DataSet/cutoff1hz/deep/spontaneous'
file_deep_post = 'DataSet/cutoff1hz/deep/poststimulus'

file_medium_stimulus = 'DataSet/cutoff1hz/medium/stimulus'
file_medium_spontaneous = 'DataSet/cutoff1hz/medium/spontaneous'
file_medium_poststimulus = 'DataSet/cutoff1hz/medium/poststimulus'

file_light_stimulus = 'DataSet/cutoff1hz/light/stimulus'
file_light_spontaneous = 'DataSet/cutoff1hz/light/spontaneous'
file_light_poststimulus = 'DataSet/cutoff1hz/light/poststimulus'

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

mat_global = [[0 for i in range(maxS_Allocate)] for j in range(maxD_allocate)]

for i in range(len(filesToOpen)):
    # coder for this DOA and segment
    cd = Coder(filesToOpen[i])
    print(str(i) + ' maxD: ' + str(cd.maxD))
    print(str(i) + ' maxS: ' + str(cd.maxS))

    # add to total freq matrix
    mat_global = np.add(mat_global, cd.ds_matrix)

# input_matrix = np.loadtxt(fname='./global_DS_matrix-1.txt', dtype='i')

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
path = os.getcwd()
fileName = path + "/global_DS_matrix_cutoff1hz.txt"
f = open(fileName, "w")
for d in range(maxD_allocate):
    for s in range(maxS_Allocate):
        f.write(str(mat_global[d][s]) + " ")
    f.write("\n")
f.close()

print("done writing")

# cmap = plt.cm.OrRd
# cmap.set_under(color='black')
# plt.imshow(mat_global, interpolation='none', cmap=cmap, vmin=0.0000001)

#       AICIA CRAPA
ax = sns.heatmap(np.log10(mat_global), cmap="YlGnBu", vmin=0, vmax=7)
ax.invert_yaxis()
plt.xlabel("S")
plt.title("DS frequency cutoff 1Hz log10")
plt.ylabel("D")
plt.show()
