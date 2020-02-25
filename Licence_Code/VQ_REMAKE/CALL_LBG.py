'''
    how to call LBG alg:
        - read a DS frequency matrix from a file
        - call VQ_LBG and set params: k=number of clusters
                                      alpha = threshold for distorsion of overall alg
                                      t = max nr of iterations
                                      scale_s = how important to be s in the error/ distortion calculation
                                      epsilon = how much to recenter the clusters
'''

import numpy as np

from VQ_REMAKE.LBG import VQ_LGB

# citeste o matrice din orice fisier
input_matrix = np.loadtxt(fname='./global_DS_matrix.txt', dtype='i')

# # check the read matrix
# for i in range(len(input_matrix)):
#     print('\n')
#     for j in range(len(input_matrix[0])):
#         print(str(input_matrix[i][j]) + ' ')

# apply alg
lbg = VQ_LGB(k=32, alpha=0.00005, t=10000, scale_s=5, epsilon=0.1)

# after creating it,  set the dataset
lbg.set_dataset(input_matrix[0:250, 0:80])
lbg.run()
