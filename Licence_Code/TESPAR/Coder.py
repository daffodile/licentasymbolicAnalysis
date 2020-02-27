import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema, find_peaks



# added a file to write the values before transforming them to a symbol
# fileName = 'Pairs/channel_2_pairs.txt'

maxD_allocate = 222
maxS_Allocate = 48

class Coder:
    '''
    parameters:  - file_epd: - name of the file with extension .epd
    '''

    def __init__(self, filePath):

        self.ds_matrix = [[0 for i in range(maxS_Allocate)] for j in range(maxD_allocate)]
        self.distributionD = [0] * maxD_allocate
        self.distributionS = [0] * maxS_Allocate
        self.channel_values = []
        self.maxD = -1
        self.maxS = -1
        self.filePath = filePath

        self.read_file()
        self.aOffset = 0

        self.symbolic_array = []
        self.test_epoch = []
        self.create_matrix()

    '''
    changed to read all 30 channels in a directory
        open each channel and save each of its line as an element in "channel_values"
            -> channel_values should have size 30*240, each array having 2672 floats
            
    # maxD is 996  # for 'DataSet/light/stimulus'
    # maxS 0s 337  # for 'DataSet/light/stimulus'
    # 
    # - normalized d / 9 => range 0 to 111
    # - normalized s / 3 => range 0 to 112
        
    '''

    def read_file(self):
        project_path = os.path.join('', '..')
        data_dir = os.path.join(project_path, self.filePath, '')
        sys.path.append(project_path)

        for i in range(30):
            line = None
            file_name = "channel" + str(i) + ".txt"
            with open(os.path.join(data_dir, file_name), 'r') as f:
                line = f.readline()
                while line:
                    line = line.replace("[", "")
                    line = line.replace("]", "")
                    new_array = np.fromstring(line, dtype=np.float, sep=', ')
                    self.channel_values.append(new_array)
                    line = f.readline()

    def create_matrix(self):
        for channel in range(len(self.channel_values)):  # length 30*240
            d = 0
            s = 0
            current_epoch = 0
            last_zero_crossing = self.aOffset

            test_epoch = []
            markers_on = []

            length = len(self.channel_values[channel])
            # print("length = " + str(length))
            last_value = self.channel_values[channel][0]

            for i in range(1, length):
                # create array of every epoch

                if self.channel_values[channel][i] * last_value < 0 :#or i == length-1:  # Zero Crossing -> new Epoch

                    positive = self.channel_values[channel][i] > 0
                    d = i - last_zero_crossing

                    # print("the epoch")
                    # print(test_epoch)

                    # if i == length-1 and len(test_epoch) > 1:
                    #     test_epoch.append(self.channel_values[channel][i])
                    #     positive = not positive

                    if positive:
                        for j in range(len(test_epoch)):
                            test_epoch[j] = abs(test_epoch[j])

                    series = np.array(test_epoch)
                    peaks, _ = find_peaks(series)
                    mins, _ = find_peaks(series * -1)
                    x = np.linspace(0, 10, len(series))
                    # plt.plot(x, series, color='black');
                    # plt.plot(x[mins], series[mins], 'x', label='mins')
                    # plt.plot(x[peaks], series[peaks], '*', label='peaks')
                    # plt.legend()
                    # plt.ylim(-20, 20)
                    # plt.show()

                    s = len(mins)
                    self.ds_matrix[d][s] += 1

                    if s > self.maxS:
                        self.maxS = s
                    if d > self.maxD:
                        self.maxD = d
                    # print(s)
                    # print(d)
                    # plotul cu toate epocile
                    for j in range(len(mins)):
                        markers_on.append(mins[j] + last_zero_crossing)

                    test_epoch = []
                    test_epoch.append(self.channel_values[channel][i])
                    last_zero_crossing = i
                    current_epoch = current_epoch + 1
                    d = 0
                    s = 0
                else:
                    test_epoch.append(self.channel_values[channel][i])

                last_value = self.channel_values[channel][i]
