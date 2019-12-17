import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import argrelextrema

from TESPAR.Coder import Coder

project_path = os.path.join('', '..')
data_dir = os.path.join(project_path, 'DataSet/light/stimulus', '')
sys.path.append(project_path)
light_stimulus_0 = 'channel0.txt'

line = None
channel_values = []
with open(os.path.join(data_dir, light_stimulus_0), 'r') as f:
    line = f.readline()
    while line:
        line = line.replace("[", "")
        line = line.replace("]", "")
        new_array = np.fromstring(line, dtype=np.float, sep=', ')
        channel_values.append(new_array)
        line = f.readline()


class TesparPair:
    def __init__(self, duration, shape):
        self.duration = duration  # the number of samples
        self.shape = shape  # the number of local minimas


tesparPairs = []

# print(channel_values[0])
# # find local minimas from the first line
# local_minimas_indices_0 = argrelextrema(channel_values[0], np.less)  # the indices of the local minimas in a tuple
# local_minimas_values_0 = []
# print(len(local_minimas_indices_0[0]))
# for i in range(len(local_minimas_indices_0[0])):
#     local_minimas_values_0.append(channel_values[0][local_minimas_indices_0[0][i]])
# print(local_minimas_values_0)
#
# df = pd.DataFrame(channel_values[0], columns=['data'])
#
# n = 50  # number of points to be checked before and after
# # Find local peaks
# df['min'] = df.iloc[argrelextrema(df.data.values, np.less_equal, order=n)[0]]['data']
# df['max'] = df.iloc[argrelextrema(df.data.values, np.greater_equal, order=n)[0]]['data']
#
# # Plot results
# plt.scatter(df.index, df['min'], c='r')
# plt.scatter(df.index, df['max'], c='g')
# plt.plot(df.index, df['data'])
# plt.show()

# ZERO CROSSING
my_array = np.array(channel_values[0])
# for i in range(len(my_array)-1):
#     if my_array[i] * my_array[i + 1] < 0:
#

contor = ((my_array[:-1] * my_array[1:]) < 0).sum()
print("atatea trebe sa fie teoretic " + str(contor))

# for i in range(len(channel_values)):
#     print(i)
#     my_array = np.array(channel_values[i])
#     contor = ((my_array[:-1] * my_array[1:]) < 0).sum()
#     print("atatea trebe sa fie teoretic " + str(contor))
cd = Coder(channel_values[0], 0, 2672)
print(cd.symbolic_array)
plt.plot(cd.symbolic_array)
plt.show()

# tespar S
s_matrix = []
for i in range(29):
    s_matrix.append(0)
for i in range(len(cd.symbolic_array)):
    s_matrix[cd.symbolic_array[i]] += 1

plt.hist(cd.symbolic_array, bins='auto')
plt.title("Tespar S", fontdict=None)
plt.xlabel("Symbols")
plt.ylabel("No of app")
plt.show()

# tespar A
lag = 1
a_matrix = [[0 for i in range(29)] for j in range(29)]
# temp_arr = []
# for i in range(len(cd.symbolic_array)):
#     a_matrix.append([])
#     temp_arr.append(0)
# for i in range(len(cd.symbolic_array)):
#     for j in range(len(cd.symbolic_array)):
#         a_matrix[i][j] = temp_arr

for i in range(len(cd.symbolic_array) - 1):
    current = cd.symbolic_array[i]
    next = cd.symbolic_array[i + 1]
    if current + lag == next or next + lag == current:
        a_matrix[current][next] += 1

print("matrix")
print(a_matrix)
plt.matshow(a_matrix)
plt.colorbar()
plt.show()

