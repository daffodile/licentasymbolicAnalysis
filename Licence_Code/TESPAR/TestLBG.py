import os

from TESPAR.Coder import Coder
from TESPAR.LBG import VQ_LGB

# Coder for the directory containing the values of 'DataSet/lightFiltered/stimulus'
cd = Coder('DataSet/lightFiltered/stimulus')
print("done coder")

mat = []

for i in range(250):
    for j in range(250):
        temp = []
        temp.append(cd.test_matrix[i][j])
        mat.append(temp)
print("added data")

# vq_lg = VQ_LGB(mat, 32, 0.00005, 3000)
vq_lg = VQ_LGB(mat, 32, 0.005, 1000)
vq_lg.run()
outout = vq_lg.get_codebook()

# print(outout.size)
vq_lg.print_clusters()

print("run clustering")

alphabet_matrix = [[0 for i in range(250)] for j in range(250)]

# file_name = os.getcwd() + "/clusters_light_stim_others.txt"
file_name = os.getcwd() + "/clusters_light_stim.txt"
f = open(file_name, 'w')

for x in range(250):
    for y in range(250):
        for index in range(len(vq_lg.clusters)):
            flattened_patterns = [item for items in vq_lg.clusters[index].patterns for item in items]
            if cd.test_matrix[x][y] in flattened_patterns:
                alphabet_matrix[x][y] = index
                f.write(str(index) + ' ')
    f.write('\n')

f.close()
