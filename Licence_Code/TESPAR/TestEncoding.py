import numpy as np

from TESPAR.Encoding import Encoding
import os
import sys

en = Encoding('./symbols_3_s10.txt')
array = []

file_deep_stimulus = 'DataSet/deep/stimulus'
project_path = os.path.join('', '..')
data_dir = os.path.join(project_path, file_deep_stimulus, '')
sys.path.append(project_path)

file_name = "channel0.txt"
with open(os.path.join(data_dir, file_name), 'r') as f:
    line = f.readline()
    line = line.replace("[", "")
    line = line.replace("]", "")
    array = np.fromstring(line, dtype=np.float, sep=', ')

en.get_symbols(array)
en.get_s()

