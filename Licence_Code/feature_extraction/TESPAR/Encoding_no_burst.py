import sys

import numpy as np
from scipy.signal import find_peaks


class EncodingNoBurst:
    '''
       alphabet - a matrix of DS having the corresponding 'symbol' on each position
       '''

    def __init__(self, alphabet_path, no_symbols=32):
        self.no_symbols = no_symbols
        self.s_matrix = [0 for i in range(no_symbols)]
        self.a_matrix = [[0 for i in range(no_symbols)] for j in range(no_symbols)]
        self.alphabet_path = alphabet_path
        self.symbols_array = []
        self.alphabet_matrix = None
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
        self.rows = len(self.alphabet_matrix)
        self.cols = len(self.alphabet_matrix[0])

    def get_symbols(self, trial, trial_validate):

        self.symbols_array = []

        trial_array = trial
        trial_validate = trial_validate
        d = 0
        s = 0
        current_epoch = 0
        last_zero_crossing = 0

        test_epoch = []
        length = len(trial_array)
        length_validate = len(trial_validate)
        if length_validate != length:
            print('this trial does not have a corresponding valid trial  ' + str(length_validate),
                  file=sys.stderr)
            sys.exit()

        last_value = trial_array[0]
        if trial_validate[0] == 0:
            valid = True
        else:
            valid = False

        for i in range(1, length):
            if trial_array[i] * last_value < 0 or i == length - 1:  # Zero Crossing -> new Epoch
                positive = trial_array[i] > 0
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

                if d < self.rows and s < self.cols and valid:
                    self.symbols_array.append(self.alphabet_matrix[d][s])

                valid = True
                test_epoch = []
                test_epoch.append(trial_array[i])
                last_zero_crossing = i
                current_epoch = current_epoch + 1
                d = 0
                s = 0
            else:
                if trial_validate[i] == 1:
                    valid = False
                test_epoch.append(trial_array[i])

            last_value = trial_array[i]

        return self.symbols_array

    def get_s(self, trial, trial_validate):

        symbols_array = self.get_symbols(trial, trial_validate)

        s_matrix = [0 for i in range(32)]

        for i in range(len(symbols_array)):
            s_matrix[symbols_array[i]] += 1

        return s_matrix

    def get_a(self, trial, trial_validate, lag=1, selected_symbols=32):

        if (selected_symbols < 1 or selected_symbols > self.no_symbols):
            print('selected_symbols has an illegal value. Try a value between 0 and ' + str(self.no_symbols),
                  file=sys.stderr)
            sys.exit()

        symbols_array = self.get_symbols(trial, trial_validate)

        # a_matrix = [[0 for i in range(self.no_symbols)] for j in range(self.no_symbols)]
        a_matrix = np.zeros((self.no_symbols, self.no_symbols), dtype=int)

        for i in range(len(symbols_array) - lag - 1):
            current = symbols_array[i]
            current_pair = symbols_array[i + 1 + lag]
            a_matrix[current][current_pair] += 1

        return a_matrix[:selected_symbols, :selected_symbols]
