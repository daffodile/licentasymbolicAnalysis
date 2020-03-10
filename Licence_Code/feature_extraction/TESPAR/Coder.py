import os
import sys

import numpy as np
from scipy.signal import find_peaks


class Coder:
    '''
    parameters:  - doas: - array of doas containing the whole dataset
    '''

    def __init__(self, path_save_file):

        self.path_to_save_file = path_save_file

        self.channel_values = []

        self.aOffset = 0
        self.symbolic_array = []

        # print('Obtain the floats array from DOA-s')
        # # for doa in doas:
        # #     doa_floats_list = Utils.obtain_floats_from_DOA(doa)
        # #     self.channel_values.extend(doa_floats_list)
        #
        # self.channel_values = Utils.obtain_floats_from_DOA(doas[0])[0:100]
        #
        # print('Floats are set')
        # # self.ds_matrix = [[0 in range(48)] in range(222)]

        self.read_file()

        max_d, max_s = self.set_matrix_dimensions()

        self.maxD = max_d
        self.maxS = max_s

        print('create matrix now: ')
        self.create_matrix()

    def read_file(self):
        project_path = os.path.join('.', '..')
        data_dir = os.path.join(project_path, 'input_reader', '')
        sys.path.append(project_path)

        line = None
        file_name = "trials_as_floats_1hz.txt"
        with open(os.path.join(data_dir, file_name), 'r') as f:
            line = f.readline()
            while line:
                line = line.replace("[", "")
                line = line.replace("]", "")
                new_array = np.fromstring(line, dtype=np.float32, sep=', ')
                self.channel_values.append(new_array)
                line = f.readline()
        print('read_file: length of list of arrays of floats:  ' + str(len(self.channel_values)))

    def create_matrix(self):
        # self.ds_matrix = [[0 in range(self.maxS)] in range(self.maxD)]
        self.ds_matrix = np.zeros((self.maxD, self.maxS), dtype='i')

        for channel in range(len(self.channel_values)):  # length 30*240
            d = 0
            s = 0
            current_epoch = 0
            last_zero_crossing = self.aOffset

            test_epoch = []

            length = len(self.channel_values[channel])
            last_value = self.channel_values[channel][0]

            for i in range(1, length):
                if self.channel_values[channel][i] * last_value < 0:  # Zero Crossing -> new Epoch

                    positive = self.channel_values[channel][i] > 0
                    d = i - last_zero_crossing

                    if positive:
                        for j in range(len(test_epoch)):
                            test_epoch[j] = abs(test_epoch[j])

                    series = np.array(test_epoch)
                    peaks, _ = find_peaks(series)
                    mins, _ = find_peaks(series * -1)

                    s = len(mins)

                    self.ds_matrix[d][s] += 1

                    test_epoch = []
                    test_epoch.append(self.channel_values[channel][i])
                    last_zero_crossing = i
                    current_epoch = current_epoch + 1
                    d = 0
                    s = 0
                else:
                    test_epoch.append(self.channel_values[channel][i])

                last_value = self.channel_values[channel][i]

        print('se scrie DS matrix in fisier')
        # path = os.getcwd()
        # fileName = path + self.path_to_save_file
        f = open(self.path_to_save_file, "w")
        for d in range(self.maxD):
            for s in range(self.maxS):
                f.write(str(self.ds_matrix[d][s]) + " ")
            f.write("\n")
        f.close()

    def set_matrix_dimensions(self):

        maxD = 0
        maxS = 0
        for channel in range(len(self.channel_values)):
            d = 0
            s = 0
            current_epoch = 0
            last_zero_crossing = self.aOffset

            test_epoch = []

            length = len(self.channel_values[channel])
            last_value = self.channel_values[channel][0]

            for i in range(1, length):
                if self.channel_values[channel][i] * last_value < 0:  # Zero Crossing -> new Epoch

                    positive = self.channel_values[channel][i] > 0
                    d = i - last_zero_crossing

                    if positive:
                        for j in range(len(test_epoch)):
                            test_epoch[j] = abs(test_epoch[j])

                    series = np.array(test_epoch)
                    peaks, _ = find_peaks(series)
                    mins, _ = find_peaks(series * -1)

                    s = len(mins)

                    if s > maxS:
                        maxS = s
                        print('higher s: ' + str(s))

                    if d > maxD:
                        maxD = d
                        print('higher d: ' + str(d))

                    test_epoch = []
                    test_epoch.append(self.channel_values[channel][i])
                    last_zero_crossing = i
                    current_epoch = current_epoch + 1
                    d = 0
                    s = 0
                else:
                    test_epoch.append(self.channel_values[channel][i])

                last_value = self.channel_values[channel][i]

        maxD += 1
        maxS += 1
        print('find_matrix_dimensions  maxD +1: ' + str(maxD) + '  maxS +1: ' + str(maxS))

        return maxD, maxS
