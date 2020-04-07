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

# print('Obtain the floats array from DOA-s')
# floats_Array = []
# for doa in doas:
#     doa_floats_list = Utils.obtain_floats_from_DOA(doa)
#     floats_Array.extend(doa_floats_list)

# 2) DOAS ca floats pusa in fisier corresp
# print('write trials_as_floats')
# np.savetxt("trials_as_floats.txt", floats_Array, fmt="%s")
# print('trials_as_floats is written\n')

# 3) arrayul de floats data la un Coder scrie o matrice ds
# print('coder generates DS freq matrix')
# coderFinal = Coder(path_save_file="ds_freq.txt", path_floats_file="trials_as_floats.txt")
# print('after coder, ds freq matrix should be written\n')

print('load ds freq matrix for vq alg')

input_matrix = np.loadtxt(fname='../../data_to_be_saved/ds_freq.txt', dtype='i')
print(' ds freq matrix is loaded, start vq lbg alg\n')
lbg = VQ_LGB(k=32, alpha=0.0001, t=200, scale_s=10, epsilon=0.1)
lbg.set_dataset(input_matrix)
lbg.run(file_alphabet='alphabet10.txt')
print('DONE!!!')
