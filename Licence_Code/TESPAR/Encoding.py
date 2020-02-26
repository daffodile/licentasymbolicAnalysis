'''
this file will serve for writing the methods that encode according with an alphabet
'''
import numpy as np
from scipy.signal import find_peaks


class Encoding:
    '''
    alphabet - a matrix of DS having the corresponding 'symbol' on each position
    '''

    def __init__(self, alphabet_path):
        self.alphabet_path = alphabet_path
        self.symbols_array = []
        self.alphabet_matrix = [[0 for i in range(536)] for j in range(106)]
        self.rows = 0
        self.cols = 0
        self.set_alphabet()

    '''
    method to initialize the alphabet based on values read from a given file
    symbols_file - full path, name of the file
    rows and cols - the dim of the alphabet
    '''

    def set_alphabet(self):
        self.alphabet_matrix = np.loadtxt(fname=self.alphabet_path, dtype='i')
        # print(self.alphabet_matrix)

    def get_symbols(self, trial):
        trial_array = trial
        d = 0
        s = 0
        current_epoch = 0
        last_zero_crossing = 0

        test_epoch = []
        markers_on = []

        length = len(trial_array)
        last_value = trial_array[0]

        for i in range(1, length):
            if trial_array[i] * last_value < 0 or i == length - 1:  # Zero Crossing -> new Epoch
                positive =trial_array[i] > 0
                d = i - last_zero_crossing

                if i == length - 1:
                    test_epoch.append(trial_array[i])
                    positive = not positive

                if positive:
                    for j in range(len(test_epoch)):
                        test_epoch[j] = abs(test_epoch[j])

                series = np.array(test_epoch)
                peaks, _ = find_peaks(series)
                mins, _ = find_peaks(series * -1)

                s = len(mins)

                self.symbols_array.append(self.alphabet_matrix[d][s])

                test_epoch = []
                test_epoch.append(trial_array[i])
                last_zero_crossing = i
                current_epoch = current_epoch + 1
                d = 0
                s = 0
            else:
                test_epoch.append(trial_array[i])

            last_value = trial_array[i]
        print(self.symbols_array)






    # def read_alphabet(self, symbols_file, rows, cols):
    #     self.cols = cols
    #     self.rows = rows
    #     f = open(symbols_file, 'r')
    #     self.alphabet = [[0 for i in range(cols)] for j in range(rows)]
    #     for i in range(rows):
    #         for j in range(cols):
    #             f.read(self.alphabet[i][j])
    #
    # def get_symbol(self, d, s):
    #     if d < len(self.alphabet) and s < len(self.alphabet[0]):
    #         return self.alphabet[d][s]
