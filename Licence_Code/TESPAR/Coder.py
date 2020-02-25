import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Coder:
    '''
    parameters:  - filePath: - name of the directory from which we get the 30 channels
    '''

    def __init__(self, filePath):
        # self.distributionD = [0] * 550
        # self.distributionS = [0] * 250
        self.channel_values = []
        self.maxD = -1
        self.maxS = -1
        self.filePath = filePath

        self.read_file()
        self.aOffset = 0

        self.symbolic_array = []
        self.create_matrix()

    '''
    changed to read all 30 channels in a directory
        open each channel and save each of its line as an element in "channel_values"
            -> channel_values should have size 30*240, each array having 2672 floats  
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
        d = 0
        s = 0
        current_epoch = 0
        last_zero_crossing = self.aOffset
        '''
        declare the DS matrix of 150*150 as we ignore outside values as being artifacts
        '''
        self.test_matrix = [[0 for i in range(150)] for j in range(150)]

        for channel in range(len(self.channel_values)):  # length 30*240
            length = len(self.channel_values[channel])
            last_value = self.channel_values[channel][0]
            positive = self.channel_values[channel][0] > 0
            for i in range(1, length - 1):
                if self.channel_values[channel][i] * last_value < 0:  # Zero Crossing -> new Epoch
                    positive = self.channel_values[channel][i] > 0
                    d = i - last_zero_crossing
                    # self.distributionD[d] = self.distributionD[d] + 1
                    # self.distributionS[s] = self.distributionS[s] + 1
                    # if d > self.maxD:
                    #     self.maxD = d
                    # if s > self.maxS:
                    #     self.maxS = s

                    '''       
                    values for d > 150 are cut
                    values of s > 30 are cut // remaining are multiplied with 5 
                    ///
                    values for d > 100 are cut
                    values of s > 50 are cut // remaining are multiplied with 5
                    '''
                    if d < 100 and s < 50:
                        self.test_matrix[d][s] += 1
                    last_zero_crossing = i
                    current_epoch = current_epoch + 1
                    d = 0
                    s = 0

                tmp1 = last_value - self.channel_values[channel][i]

                tmp2 = self.channel_values[channel][i] - self.channel_values[channel][i + 1]
                if tmp1 * tmp2 < 0:  # We have an extremum
                    if positive:
                        if tmp1 > 0:
                            s = s + 1
                    if tmp1 < 0:
                        s = s + 1
                last_value = self.channel_values[channel][i]

            d = 0
            s = 0
            current_epoch = 0
            last_zero_crossing = 0

        # return self.symbolic_array
