import os
import numpy as np
from sqlalchemy import false

from TESPAR.Alphabet import Alphabet


class Coder:
    '''
    parameters:  - file_epd: - name of the file with extension .epd
    '''

    def __init__(self, segment_array, aOffset, aLength):
        self.aOffset = aOffset
        self.lastValue = segment_array[aOffset]
        self.segment_array = segment_array
        self.length = aLength
        self.symbolic_array = []

        self.positive = self.segment_array[aOffset] > 0
        self.create_matrix()

    def create_matrix(self):
        d = 0
        s = 0
        current_epoch = 0
        last_zero_crossing = self.aOffset

        for i in range(1, self.length-1):
            if self.segment_array[i] * self.lastValue < 0:  # Zero Crossing -> new Epoch
                self.positive = self.segment_array[i] > 0
                d = i - last_zero_crossing
                alphabet = Alphabet(d, s)
                self.symbolic_array.append(alphabet.value_to_return)
                last_zero_crossing = i;
                current_epoch = current_epoch + 1;
                d = 0
                s = 0

            tmp1 = self.lastValue - self.segment_array[i]

            tmp2 = self.segment_array[i] - self.segment_array[i + 1];
            if tmp1 * tmp2 < 0:  # We have an extremum
                if self.positive:
                    if tmp1 > 0:
                        s = s + 1
                if tmp1 < 0:
                    s = s + 1
            self.lastValue = self.segment_array[i]

        return self.symbolic_array;
