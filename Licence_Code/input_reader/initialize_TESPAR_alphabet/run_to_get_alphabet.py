'''
SO:
1) InitDataSet cu cutoff 1
2) DOAS ca floats pusa in fisier corresp => trials_as_floats_1hz.txt
3) arrayul de floats data la un Coder care scrie un alfabet
'''
import numpy as np

from feature_extraction.TESPAR.Coder import Coder
from feature_extraction.TESPAR.VQ.LBG import VQ_LGB
from input_reader.InitDataSet import InitDataSet

# 1) InitDataSet cu cutoff 1
from utils import Utils

# print('Initialization of doas start\n')
# initialization = InitDataSet()
# doas = initialization.get_dataset_as_doas()
#
# print('Obtain the floats array from DOA-s')
# floats_Array = []
# for doa in doas:
#     doa_floats_list = Utils.obtain_floats_from_DOA(doa)
#     floats_Array.extend(doa_floats_list)
#
# # 2) DOAS ca floats pusa in fisier corresp
# print('write trials_as_floats_1hz')
# np.savetxt("trials_as_floats_dsfull.txt", floats_Array, fmt="%s")
# print('trials_as_floats_1hz is written\n')

# 3) arrayul de floats data la un Coder scrie o matrice ds
# print('coder generates DS freq matrix')
# # file_name = "trials_as_floats_1_150hz.txt"
# coder1hz = Coder(path_save_file="ds_matrix_doas_dsfinal.txt", path_floats_file="trials_as_floats_dsfull.txt")
# print('after coder, ds freq matrix should be written\n')

print('load ds freq matrix for vq alg')

input_matrix = np.loadtxt(fname='./ds_matrix_doas_dsfinal.txt', dtype='i')
print(' ds freq matrix is loaded, start vq lbg alg\n')
lbg = VQ_LGB(k=32, alpha=0.00005, t=1000, scale_s=5, epsilon=0.1)
lbg.set_dataset(input_matrix)
lbg.run(file_alphabet='alphabet_dsfinal.txt')
print('DONE!!!')
