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

from feature_extraction.TESPAR.VQ.LBG import VQ_LGB

####  read the DS freq matrix for this filtering cutoff  ###
# input_matrix = np.loadtxt(fname='./../../../data_to_be_saved/ds_matrix_doas_1hz.txt', dtype='i')
# input_matrix = np.loadtxt(fname='./../../../data_to_be_saved/ds_matrix_doas_3hz.txt', dtype='i')
input_matrix = np.loadtxt(fname='./../../../data_to_be_saved/ds_matrix_doas_1_150hz.txt', dtype='i')

# apply alg
lbg = VQ_LGB(k=32, alpha=0.000005, t=10000, scale_s=5, epsilon=0.1)
# lbg = VQ_LGB(k=32, alpha=0.0005, t=100, scale_s=1, epsilon=0.1)

lbg.set_dataset(input_matrix)
lbg.run()
