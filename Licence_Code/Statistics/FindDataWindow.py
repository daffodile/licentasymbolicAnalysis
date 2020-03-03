import sys

import numpy as np


class FDW:
    def __init__(self):
        print('fdw def')

    def get_pool(self, freq_matrix, percent):
        if percent < 0 or percent > 1:
            sys.exit('Wrong percent value, introduce a value in [0, 1]')

        else:
            maxD = len(freq_matrix)
            maxS = len(freq_matrix[0])

            print(maxD)
            print(maxS)
            s = 0
            d = 0
            per = 0

            total = freq_matrix.sum()
            print(total)

            normalized_matrix = np.divide(freq_matrix, total)
            # print(normalized_matrix)
            changeS = True
            changeD = True

            while per < percent:
                if changeS:
                    for i in range(d):
                        per += normalized_matrix[i][s]

                if changeD:
                    for j in range(s):
                        per += normalized_matrix[d][j]
                if s < maxS - 1:
                    s += 1
                else:
                    changedS = False
                if d < maxD - 1:
                    d += 1
                else:
                    changeD = False
                per += normalized_matrix[d][s]
                print(per)

            print('d: ' + str(d) + '  s: ' + str(s))

            return d, s


freq_matrix = np.loadtxt(fname='./../TESPAR/global_DS_matrix_cutoff1hz.txt', dtype='i')

fdw = FDW()
outd, outs = fdw.get_pool(freq_matrix, 0.99)
print(outd)
print(outs)
