import os
import sys

import numpy as np

from DataSet.InitDataSet import InitDataSet
from DataSet.MetadataReaderEPD import MetadataReaderEPD
from DataSet.MetadataReaderETI import MetadataReaderETI
from DataSet.CreateDOA import CreateDOA

# line = '1,2,3'
# # print(line.split(','))
# project_path = os.path.join('', '..')
# data_dir = os.path.join(project_path, 'Data', '')
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
#
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


initialization = InitDataSet()

# initialization.serialize_doas('test.json')
# data = initialization.deserialize_doas('test.json')
# print(data)
