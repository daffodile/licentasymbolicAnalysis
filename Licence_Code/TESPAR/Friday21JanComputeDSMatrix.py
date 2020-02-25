import os

import numpy as np

from TESPAR.Friday21Jan import Coder

file_deep_stimulus = 'DataSet/deepFiltered/stimulus'
file_deep_spontaneous = 'DataSet/deepFiltered/spontaneous'
file_deep_post = 'DataSet/deepFiltered/poststimulus'

file_medium_stimulus = 'DataSet/mediumFiltered/stimulus'
file_medium_spontaneous = 'DataSet/mediumFiltered/spontaneous'
file_medium_poststimulus = 'DataSet/mediumFiltered/poststimulus'

file_light_stimulus = 'DataSet/lightFiltered/stimulus'
file_light_spontaneous = 'DataSet/lightFiltered/spontaneous'
file_light_poststimulus = 'DataSet/lightFiltered/poststimulus'

filesToOpen = [file_light_stimulus, file_light_spontaneous, file_light_poststimulus,
               file_medium_stimulus, file_medium_spontaneous, file_medium_poststimulus,
               file_deep_stimulus, file_deep_spontaneous, file_deep_post]

# filesToWriteDistributions = ['mat_light_stimulus', 'mat_light_spontaneous', 'mat_light_poststimulus',
#                              'mat_medium_stimulus', 'mat_medium_spontaneous', 'mat_medium_poststimulus',
#                              'mat_deep_stimulus', 'mat_deep_spontaneous', 'mat_deep_poststimulus']

mat_global = [[0 for i in range(250)] for j in range(550)]

for i in range(len(filesToOpen)):
    # coder for this DOA and segment
    cd = Coder(filesToOpen[i])

    # add to total freq matrix
    mat_global = np.add(mat_global, cd.test_matrix)


path = os.getcwd()
fileName = path + "/global_DS_matrix.txt"
f = open(fileName, "w")

for d in range(550):
    for s in range(250):
        f.write(str(mat_global[d][s]) + " ")
    f.write("\n")
f.close()
print("done for " + filesToOpen[i])