'''
    cum apelez LBG alg

'''
import numpy as np

from VQ_REMAKE.LBG import VQ_LGB

# citeste o matrice din orice fisier
input_matrix = np.loadtxt(fname='../Statistics/distributions_100_50/global_matrix_DS.txt', dtype='i')

lbg = VQ_LGB(k=32, alpha=0.00005, t=10000, freq_replacer=0.00001, scale_s=1, epsilon= 0.1)
lbg.set_dataset(input_matrix)
lbg.run()