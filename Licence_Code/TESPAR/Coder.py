import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

from TESPAR.Alphabet import Alphabet

# added a file to write the values before transforming them to a symbol
# fileName = 'Pairs/channel_2_pairs.txt'


class Coder:
    '''
    parameters:  - file_epd: - name of the file with extension .epd
    '''

    def __init__(self):
        self.channel_values = []
        self.maxD = -1
        self.maxS = -1

        self.read_file()
        self.aOffset = 0
        # self.lastValue = segment_array[aOffset]
        # self.segment_array = segment_array
        self.symbolic_array = []

        # self.positive = self.segment_array[aOffset] > 0
        self.create_matrix()

    '''
    changed to read all 30 channels in a directory
        open each channel and save each of its line as an element in "channel_values"
            -> channel_values should have size 30*240, each array having 2672 floats
            
    maxD is 996  # for 'DataSet/light/stimulus'
    maxS 0s 337  # for 'DataSet/light/stimulus'
    
    - normalized d / 9 => range 0 to 111
    - normalized s / 3 => range 0 to 112
        
    '''
    def read_file(self):
        project_path = os.path.join('', '..')
        data_dir = os.path.join(project_path, 'DataSet/light/stimulus', '')
        sys.path.append(project_path)
        # file_name = file_name

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

        self.test_matrix = [[0 for i in range(113)] for j in range(111)]

        saving_pairs = []
        for channel in range(len(self.channel_values)):
            length = len(self.channel_values[channel])
            last_value = self.channel_values[channel][0]
            positive = self.channel_values[channel][0] > 0
            for i in range(1, length-1):
                if self.channel_values[channel][i] * last_value < 0:  # Zero Crossing -> new Epoch
                    positive = self.channel_values[channel][i] > 0
                    d = i - last_zero_crossing
                    if d > self.maxD:
                        self.maxD = d
                    if s > self.maxS:
                        self.maxS = s

                    self.test_matrix[int(d / 9)][int(s / 3)] += 1
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
