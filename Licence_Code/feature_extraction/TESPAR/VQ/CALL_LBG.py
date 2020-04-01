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
from timeit import default_timer as timer

from feature_extraction.TESPAR.VQ.LBG import VQ_LGB

####  read the DS freq matrix for this filtering cutoff  ###

input_matrix = np.loadtxt(fname='./../../../data_to_be_saved/ds_freq.txt', dtype='i')

start = timer()
print('start time' + str(start))  # Time in seconds

# apply alg
lbg = VQ_LGB(k=32, alpha=0.0001, t=100, scale_s=3)
# lbg = VQ_LGB(k=32, alpha=0.0005, t=100, scale_s=1, epsilon=0.1)

lbg.set_dataset(input_matrix)
lbg.run('alphabet_1.txt')

end = timer()
print('end time ' + str(end))  # Time in seconds

print(str(end - start) + ' secs')  # Time in seconds
print(str((end - start) / 60) + ' mins')  # Time in seconds
