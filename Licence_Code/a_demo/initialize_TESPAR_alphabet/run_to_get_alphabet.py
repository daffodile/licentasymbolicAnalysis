'''
    when getting a new dataset run the following steps in order to get:
            - initialize dataset as DOA array
            - DS frequency matrix as .txt
            - TESPAR alphabet with Vector Quantization LBG

1) InitDataSet
2) DOAS ca floats =>  trials_as_floats.txt
3) floats array for Coder =>  ds_freq.txt
4) DS_freq => alphabet.txt

'''
import os

import numpy as np

from feature_extraction.TESPAR.Coder import Coder
from feature_extraction.TESPAR.VQ.LBG import VQ_LGB
from input_reader.InitDataSet import InitDataSet

# 1) InitDataSet cu cutoff 1
# from utils import Utils
# print('Initialization of doas start\n')
#
# levels=['deep6', 'light7', 'medium8', 'deep9', 'medium10', 'light11']
# data_dir = os.path.join('..', '..')
# initialization = InitDataSet(current_directory=data_dir, subject_directory="m016", filtering_directory="highpass10",
#                              levels=levels)
# doas = initialization.get_dataset_as_doas()
#
# print('Obtain the floats array from DOA-s')
# floats_Array = []
# for doa in doas:
#     doa_floats_list = Utils.obtain_floats_from_DOA(doa)
#     floats_Array.extend(doa_floats_list)

# 2) DOAS ca floats pusa in fisier corresp
# print('write trials_as_floats_m016_highpass')
# np.savetxt("trials_as_floats_m016_highpass.txt", floats_Array, fmt="%s")
# print('trials_as_floats_m016_highpass is written\n')

# 3) arrayul de floats data la un Coder scrie o matrice ds
# print('coder generates DS freq matrix')
# coderFinal = Coder(path_save_file="ds_freq_m016_highpass.txt", path_floats_file="trials_as_floats_m016_highpass.txt")
# print('after coder, ds freq matrix should be written\n')
#
# print('load ds freq matrix for vq alg')

# # 4) Get the Alphabet
input_matrix = np.loadtxt(fname='../../data_to_be_saved/ds_freq_m016_highpass.txt', dtype='i')
print(' ds freq matrix is loaded, start vq lbg alg\n')
lbg = VQ_LGB(k=32, alpha=0.0001, t=200, scale_s=3, epsilon=0.1)
lbg.set_dataset(input_matrix)
lbg.run(file_alphabet='m016_highpass_alphabet_3.txt')
print('DONE!!!')
