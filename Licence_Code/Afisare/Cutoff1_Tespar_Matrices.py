import numpy as np

from TESPAR.Encoding import Encoding
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns

en = Encoding('./../VQ_REMAKE/symbols_cutoff1_s10_sorted.txt')

array_27 = []
array_29 = []

file_deep_stimulus = './DataSet/cutoff1hz/deep/poststimulus'
project_path = os.path.join('', '..')
data_dir = os.path.join(project_path, file_deep_stimulus, '')
sys.path.append(project_path)


### S matrix for whole channel:

channel_values27 = []

with open(os.path.join(data_dir, "channel29.txt"), 'r') as f:
    line = f.readline()
    while line:
        line = line.replace("[", "")
        line = line.replace("]", "")
        new_array = np.fromstring(line, dtype=np.float, sep=', ')
        channel_values27.extend(new_array)
        line = f.readline()

symbols_channel27 = en.get_symbols(channel_values27)

counts, bins = np.histogram(a=symbols_channel27, bins=32)
print('get_s ' + str(en.get_s()))
print('bins  ' + str(bins[:1]))
print('counts  ' + str(counts))


######################## a matrix ########################
matrix_a = en.get_a(1)

ax = sns.heatmap(matrix_a, cmap="YlGnBu", vmin=0, vmax=8)
ax.invert_yaxis()
plt.xlabel("Symbols lag 1")
plt.title("A Matrix deep/poststimulus/29")
plt.ylabel("Symbols")
plt.show()

file_light_stimulus = './DataSet/cutoff1hz/light/poststimulus'
project_path = os.path.join('', '..')
data_dir = os.path.join(project_path, file_light_stimulus, '')
sys.path.append(project_path)
file_name = "channel29.txt"
channel_values27 = []

with open(os.path.join(data_dir, file_name), 'r') as f:
    line = f.readline()
    while line:
        line = line.replace("[", "")
        line = line.replace("]", "")
        new_array = np.fromstring(line, dtype=np.float, sep=', ')
        channel_values27.extend(new_array)
        line = f.readline()

symbols_channel27 = en.get_symbols(channel_values27)
matrix_a = en.get_a(1)
ax = sns.heatmap(matrix_a, cmap="YlGnBu", vmin=0, vmax=8)
ax.invert_yaxis()
plt.xlabel("Symbols lag 1")
plt.title("A Matrix light/poststimulus/29")
plt.ylabel("Symbols")
plt.show()
