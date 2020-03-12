import os

# line = '1,2,3'
# # print(line.split(','))
# project_path = os.path.join('', '..')
# data_dir = os.path.join(project_path, 'data', '')
# sys.path.append(project_path)
# ssd_file_deep = 'M014_S001_SRCS3L_25,50,100_0002.epd'
# eti_file_deep = 'Results M014_S001_SRCS3L_25,50,100_0002 Variable contrast, all orientations.eti'
# # reader = MetadataReaderEPD(data_dir,ssd_file_deep)
# reader = MetadataReaderETI(data_dir, eti_file_deep)
# reader.print_description()
# print(reader.trials_description)
# #
# creation = CreateDOA(data_dir, ssd_file_deep, eti_file_deep, 'medium')
# creation.run()
# print(creation.doa)

# line = '4,18, 25, 225,4174577,250.00,'
# current_line = line.rstrip()
# attributes = current_line.split(',')
#
# attributes[0] = int(attributes[0])
# attributes[5] = float(attributes[5])
# print(attributes)
# dict = {'a': [1, 2], 'b': [15, 6]}
# dict.append('a', [6])
# print(dict)
#
# arr = [1, 2, 3, 4, 5]
# badch = [2, 4]
# newarr = []
# for i in range(len(arr)):
#     if i + 1 not in badch:
#         newarr.append(arr[i])
# arr = newarr
# print(arr)
# from feature_extraction.TESPAR.Coder import Coder
# from utils import Utils
#
import numpy as np

from input_reader.InitDataSet import InitDataSet
from utils import Utils

initialization = InitDataSet()

doas = initialization.get_dataset_as_doas()

# doa_light = np.extract(condition=(lambda x: x.level == "light"), arr=doas)[0]
#
# print(len(doa_light.channels))


floats_Array = []
print('Obtain the floats array from DOA-s')

for doa in doas:
    doa_floats_list = Utils.obtain_floats_from_DOA(doa)
    floats_Array.extend(doa_floats_list)

print('numa de break point hehehhe')
np.savetxt("all_floats_array.txt", floats_Array, fmt="%s")
#

# coder = Coder()
# print(coder.ds_matrix)


######    serialize JSON hereee
# initialization.serialize_doas('test.json')
# data = initialization.deserialize_doas('test.json')
# print(data)
# trial_counter=0
# for i in range(trial_counter, trial_counter +4 ):
#     print(i)
# trial_counter +=4
# for i in range(trial_counter, trial_counter + 4):
#     print(i)
