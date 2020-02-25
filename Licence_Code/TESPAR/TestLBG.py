import os

import numpy as np

from TESPAR.Coder import Coder
from TESPAR.LBG import VQ_LGB

# # Coder for the directory containing the values of 'DataSet/lightFiltered/stimulus'
# cd = Coder('DataSet/lightFiltered/stimulus')
# print("done coder")
#
# mat = []
#
# for i in range(100):
#     for j in range(50):
#         temp = []
#         temp.append(cd.test_matrix[i][j])
#         mat.append(temp)
# print("added data")

input_mat = np.loadtxt(fname='../Statistics/distributions_100_50/global_matrix_DS.txt', dtype='i')

mat = []

for i in range(100):
    for j in range(50):
        temp = []
        temp.append(input_mat[i][j])
        mat.append(temp)
print("added data")

# vq_lg = VQ_LGB(mat, 32, 0.00005, 3000)
vq_lg = VQ_LGB(mat, 32, 0.00005, 30000)
vq_lg.run()

# print(outout.size)
vq_lg.print_clusters()

print("run clustering")

alphabet_matrix = [[0 for i in range(50)] for j in range(100)]

# file_name = os.getcwd() + "/clusters_light_stim_others.txt"
# file_name = os.getcwd() + "/LBG_clusters_ result_30000.txt"
file_name = os.getcwd() + "nume fisier de unde citesc"
f = open(file_name, 'w')

for x in range(100):
    for y in range(50):
        for index in range(len(vq_lg.clusters)):
            flattened_patterns = [item for items in vq_lg.clusters[index].patterns for item in items]
            if input_mat[x][y] in flattened_patterns:
                alphabet_matrix[x][y] = index
                f.write(str(index) + ' ')
    f.write('\n')

f.close()
