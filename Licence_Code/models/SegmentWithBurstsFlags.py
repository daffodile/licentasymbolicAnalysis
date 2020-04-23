import sys
import numpy as np

from models.Models import JsonEncoder

'''
    another version of Segment class, but one that keeps flags for all the values in regions considered burst
'''


class SegmentWithBurstsFlags(JsonEncoder):
    def __init__(self, start_time, end_time, start_code, end_code):
        self.start_time = start_time
        self.end_time = end_time
        self.start_code = start_code
        self.end_code = end_code
        self.values = []
        self.values_outsiders = []

    def set_values(self, float_arr):
        self.values = float_arr
        self.values_outsiders = np.zeros(len(float_arr))

    def set_values_outsiders(self, values_outsiders):
        if len(values_outsiders) != len(self.values):
            sys.exit("The length of values_outsiders does not correspond to the length of values")
        self.values_outsiders = values_outsiders
