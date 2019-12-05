import os
import sys
import numpy as np

from matplotlib import pyplot as plt
from DataSet.MetadataReaderEPD import MetadataReaderEPD
from DataSet.TrialExtractorEPD import TrialExtractorEPD

# project_path = os.path.join('..', '..')
# data_dir = os.path.join(project_path, 'Data', 'M017_0002_sorted_full')
# sys.path.append(project_path)
# ssd_file = 'M017_S001_SRCS3L_25,50,100_0002.ssd'
# mr = MetadataReader(data_dir, ssd_file)
# print(mr.no_units)
# mr.print_metadata()

project_path = os.path.join('..', '..')
# data_dir = os.path.join(project_path, 'Data', 'M017_0002_sorted_full')
data_dir = os.path.join(project_path, 'Data', '')
sys.path.append(project_path)
ssd_file_deep = 'M014_S001_SRCS3L_25,50,100_0002.epd'
ssd_file_medium = 'M014_S001_SRCS3L_25,50,100_0003.epd'
ssd_file_light = 'M014_S001_SRCS3L_25,50,100_0004.epd'
# mr = MetadataReaderEPD(data_dir, ssd_file)
# mr.print_metadata()

trial_deep = TrialExtractorEPD(data_dir, ssd_file_deep)
print(len(trial_deep.storage[129]))
# # cleaning the storage to have only arrays with length 2672, so delete the last element if the size is 2673
for i in range(len(trial_deep.storage[129])):
    # print(len(trial.storage[129][i]))
    if len(trial_deep.storage[129][i]) > 2672:
        trial_deep.storage[129][i] = trial_deep.storage[129][i][:-1]

# myArray = np.array(trial.storage[129])
# myMatrix = np.asmatrix(myArray)
#
# matriceFinala = np.zeros(shape=(240,30), dtype=myArray.dtype)
# for i in range(240):
#     myVec = []
#     for j in range(0,7200,240):
#         myVec.append(myArray[j])
#     matriceFinala[i] = myVec
#
# # print(len(matriceFinala[0]))
# matriceTemp = np.zeros(shape = (240,80160))
#
# for i in range(240):
#     tempVec = []
#     for j in range(30):
#         # np.concatenate([tempVec,matriceFinala[i][j]])
#         np.append(tempVec, matriceFinala[i][j])
#     matriceTemp[i] = tempVec

myArray_deep = np.array(trial_deep.storage[129])
myMatrix_deep = np.asmatrix(myArray_deep)
avgMatrix_deep = myMatrix_deep.mean(0)
avgArray_deep = np.squeeze(np.asarray(avgMatrix_deep))

plt.plot(avgArray_deep)
plt.title("channel 2 deep", fontdict=None,)
plt.show()


trial_medium = TrialExtractorEPD(data_dir, ssd_file_medium)
print(len(trial_medium.storage[129]))
# # cleaning the storage to have only arrays with length 2672, so delete the last element if the size is 2673
for i in range(len(trial_medium.storage[129])):
    # print(len(trial_medium.storage[129][i]))
    if len(trial_medium.storage[129][i]) != 2672:
        trial_medium.storage[129][i] = trial_medium.storage[129][i][:-1]

myArray_medium = np.array(trial_medium.storage[129])
myMatrix_medium = np.asmatrix(myArray_medium)
avgMatrix_medium = myMatrix_medium.mean(0)
avgArray_medium = np.squeeze(np.asarray(avgMatrix_medium))

plt.plot(avgArray_medium)
plt.title("channel 2 medium", fontdict=None)
plt.show()


trial_light = TrialExtractorEPD(data_dir, ssd_file_light)
print(len(trial_light.storage[129]))
# # # cleaning the storage to have only arrays with length 2672, so delete the last element if the size is 2673
for i in range(len(trial_light.storage[129])):
    print(len(trial_light.storage[129][i]))
    if len(trial_light.storage[129][i]) != 2672:
        trial_light.storage[129][i] = trial_light.storage[129][i][:-1]

myArray_light = np.array(trial_light.storage[129])
myMatrix_light = np.asmatrix(myArray_light)
avgMatrix_light = myMatrix_light.mean(0)
avgArray_light = np.squeeze(np.asarray(avgMatrix_light))

plt.plot(avgArray_light)
plt.title("channel 2 light", fontdict=None)
plt.show()

# print("SIZEEE")
#
# print(len(trial.storage[129]))
#
# for i in range(len(trial.storage[129])):
#     print(len(trial.storage[129][i]))
#
# average_segment = []
# contor = 0
# sum = 0
# for i in range(len(trial.storage[129])):
#     sum += trial.storage[129][i][contor]
#     contor += 1

# for i in range(len(average_segment)):
#     print(average_segment[i])
# print(trial.storage[129][i])

# dict = {}
# dict[0] = [[1,2,3]]
# dict[1] = []
# # tempList = dict[0]
# # tempList.append([5,6])
# # tempD = {0 : tempList}
# # dict.update(tempD)
# print(dict[0])