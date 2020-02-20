import os

import sys
from pylab import *
import numpy
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.signal import argrelextrema, find_peaks

from TESPAR.FindMinimum import FindMinimum

project_path = os.path.join('', '..')
data_dir = os.path.join(project_path, 'DataSet/lightFiltered/stimulus', '')
sys.path.append(project_path)
file_name = "channel10.txt"
channel_values = []
signal_array = [],,
with open(os.path.join(data_dir, file_name), 'r') as f:
    line = f.readline()
    line = line.replace("[", "")
    line = line.replace("]", "")
    new_array = np.fromstring(line, dtype=np.float, sep=', ')
    for i in range(60):
        signal_array.append(new_array[i])

    print(signal_array)

# plot the signal

plt.plot(signal_array)
plt.ylim(-20, 20)
plt.axhline(linewidth=1, color='r')
plt.show()

# make ds matrix
d = 0
s = 0
ds_matrix = [[0 for i in range(100)] for j in range(100)]
aOffset = 0
current_epoch = 0
last_zero_crossing = aOffset
test_epoch = []
markers_on = []

length = len(signal_array)
last_value = signal_array[0]
positive = signal_array[0] > 0
test_epoch.append(signal_array[0])
for i in range(1, length):
    # create array of every epoch

    if signal_array[i] * last_value < 0 or i == length - 1:  # Zero Crossing -> new Epoch
        positive = signal_array[i] > 0
        d = i - last_zero_crossing

        print("the epoch")
        print(test_epoch)

        if i == length - 1:
            test_epoch.append(signal_array[i])
            positive = not positive

        if positive:
            for j in range(len(test_epoch)):
                test_epoch[j] = abs(test_epoch[j])

        series = np.array(test_epoch)
        peaks, _ = find_peaks(series)
        mins, _ = find_peaks(series * -1)
        x = np.linspace(0, 10, len(series))
        plt.plot(x, series, color='black');
        plt.plot(x[mins], series[mins], 'x', label='mins')
        plt.plot(x[peaks], series[peaks], '*', label='peaks')
        plt.legend()
        plt.ylim(-20, 20)
        plt.show()

        s = len(mins)
        ds_matrix[d][s] += 1
        # plotul cu toate epocile
        for j in range(len(mins)):
            markers_on.append(mins[j] + last_zero_crossing)

        test_epoch = []
        test_epoch.append(signal_array[i])
        last_zero_crossing = i
        current_epoch = current_epoch + 1
        d = 0
        s = 0
    else:
        test_epoch.append(signal_array[i])

    last_value = signal_array[i]

print(markers_on)
plt.plot(signal_array, '-gD', markevery=markers_on)
plt.axhline(linewidth=1, color='r')
plt.ylim(-20, 20)
plt.show()

print(ds_matrix)
