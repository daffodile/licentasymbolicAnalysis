import os

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

sns.set()

'''
    compute the global sum of the number of DS values from 
        9 files, containing DS matrix for all combinations
'''
dir_name = os.getcwd() + '/distributions_100_50/'

matrix_files = {'mat_deep_poststimulus.txt', 'mat_deep_spontaneous.txt', 'mat_deep_stimulus.txt',
                'mat_medium_poststimulus.txt', 'mat_medium_spontaneous.txt', 'mat_medium_stimulus.txt',
                'mat_light_poststimulus.txt', 'mat_light_spontaneous.txt', 'mat_light_stimulus.txt'}

mat_global = [[0 for i in range(50)] for j in range(100)]

for file_name in matrix_files:
    # print(' deschid fisier')  #works
    # open each file and save the integers matrix, skipping first 4 lines
    current_matrix = np.loadtxt(fname=str(dir_name + file_name), dtype='i')
    # print(current_matrix)  #works
    mat_global = np.add(mat_global, current_matrix)

# path = os.getcwd() + '/distributions_100_50'
# fileName = path + "/global_matrix_DS.txt"
# f = open(fileName, "w")
#
# for d in range(100):
#     for s in range(50):
#          f.write(str(mat_global[d][s]) + " ")
#     f.write("\n")
#
# f.close()

# # print(mat_global)
# plt.matshow(mat_global)
# plt.title("Global Count Matrix DS", fontdict=None)
# plt.xlabel("S")
# plt.ylabel("D")
# plt.tight_layout()
# plt.savefig("./global_DS_matrix")
# plt.show()

# ax = sns.heatmap(mat_global[0:40, 0:20])

ax = sns.heatmap(np.log(mat_global))
plt.savefig("./distributions_100_50/global_DS_matrix_log")
plt.show()
