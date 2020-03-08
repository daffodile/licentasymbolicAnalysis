import os
import sys
import numpy as np

import matplotlib.pyplot as plt

from Tests.DataSet.TrialExtractorEPD import TrialExtractorEPD

project_path = os.path.join('..', '..')
data_dir = os.path.join(project_path, 'data', '')
sys.path.append(project_path)
ssd_file_deep = 'M014_S001_SRCS3L_25,50,100_0002.epd'
ssd_file_medium = 'M014_S001_SRCS3L_25,50,100_0003.epd'
ssd_file_light = 'M014_S001_SRCS3L_25,50,100_0004.epd'

# constant for establishing the limits of the plots
scale_conts = 10
# PRINT LIGHT, MEDIUM AND DEEP PLOTS FOR A CHANNEL

# # DEEP
# trial_deep = TrialExtractorEPD(data_dir, ssd_file_deep)
# # print(len(trial_deep.storage[129]))
# # # cleaning the storage to have only arrays with length 2672, so delete the last element if the size is 2673
# for i in range(len(trial_deep.storage[129])):
#     # print(len(trial.storage[129][i]))
#     if len(trial_deep.storage[129][i]) > 2672:
#         trial_deep.storage[129][i] = trial_deep.storage[129][i][:-1]
#
# myArray_deep = np.array(trial_deep.storage[129])
# myMatrix_deep = np.asmatrix(myArray_deep)
# avgMatrix_deep = myMatrix_deep.mean(0)
# avgArray_deep = np.squeeze(np.asarray(avgMatrix_deep))
# # avgArray_deep_scaled = np.interp(avgArray_deep,-6,6, )
#
# plt.plot(avgArray_deep)
# plt.ylim(-scale_conts, scale_conts)
# plt.title("channel 2 deep", fontdict=None)
# plt.xlabel("samples")
# plt.ylabel("voltages")
# plt.show()
#
# # MEDIUM
# trial_medium = TrialExtractorEPD(data_dir, ssd_file_medium)
# print(len(trial_medium.storage[129]))
# # # cleaning the storage to have only arrays with length 2672, so delete the last element if the size is 2673
# for i in range(len(trial_medium.storage[129])):
#     # print(len(trial_medium.storage[129][i]))
#     if len(trial_medium.storage[129][i]) != 2672:
#         trial_medium.storage[129][i] = trial_medium.storage[129][i][:-1]
#
# myArray_medium = np.array(trial_medium.storage[129])
# myMatrix_medium = np.asmatrix(myArray_medium)
# avgMatrix_medium = myMatrix_medium.mean(0)
# avgArray_medium = np.squeeze(np.asarray(avgMatrix_medium))
#
# plt.plot(avgArray_medium)
# plt.ylim(-scale_conts, scale_conts)
# plt.title("channel 2 medium", fontdict=None)
# plt.xlabel("samples")
# plt.ylabel("voltages")
# plt.show()
#
# # LIGHT
# trial_light = TrialExtractorEPD(data_dir, ssd_file_light)
# print(len(trial_light.storage[129]))
# # # # cleaning the storage to have only arrays with length 2672, so delete the last element if the size is 2673
# for i in range(len(trial_light.storage[129])):
#     print(len(trial_light.storage[129][i]))
#     if len(trial_light.storage[129][i]) != 2672:
#         trial_light.storage[129][i] = trial_light.storage[129][i][:-1]
#
# myArray_light = np.array(trial_light.storage[129])
# myMatrix_light = np.asmatrix(myArray_light)
# avgMatrix_light = myMatrix_light.mean(0)
# avgArray_light = np.squeeze(np.asarray(avgMatrix_light))
#
# plt.plot(avgArray_light)
# plt.ylim(-scale_conts, scale_conts)
# plt.title("channel 2 light", fontdict=None)
# plt.xlabel("samples")
# plt.ylabel("voltages")
# plt.show()

# SAVE THE SEGMENT

# LIGHT
trial_light = TrialExtractorEPD(data_dir, ssd_file_light)

print("SEGMETS LENGTH ")
print(len(trial_light.segments))

for i in range(len(trial_light.storage[129])):
    if len(trial_light.storage[129][i]) != 2672:
        trial_light.storage[129][i] = trial_light.storage[129][i][:-1]

myArray_light_STIMULUS = np.array(trial_light.storage[129])

my_averages = []
contor = 0
for i in range(30):
    my_array = []
    for j in range(240):
        my_array.append(myArray_light_STIMULUS[contor])
        contor = contor + 1

    for m in range(len(my_array)):
        if len(my_array[i]) != 2672:
            my_array[i] = my_array[i][:-1]
    myMatrix_light = np.asmatrix(my_array)
    avgMatrix_light = myMatrix_light.mean(0)
    avgArray_light = np.squeeze(np.asarray(avgMatrix_light))
    my_averages.append(avgArray_light)

print(len(my_averages[0]))
# media canalelor
myArray_light = np.array(trial_light.storage[129])
myMatrix_average = np.asmatrix(my_averages)
avgMatrix_light_avg = myMatrix_average.mean(0)
avgArray_light_final = np.squeeze(np.asarray(avgMatrix_light_avg))
print(len(avgArray_light_final))
plt.plot(avgArray_light_final)
plt.hlines(0, 0, 2800, "red")
plt.ylim(-scale_conts, scale_conts)
plt.title("media_canalelor_light", fontdict=None)
plt.xlabel("samples in time")
plt.ylabel("voltages")
# save plt somewhere
plot_name = plt.title
# plt.savefig("./Plots/averages/'" + plot_name)
plt.show()

# MEDIUM
trial_medium = TrialExtractorEPD(data_dir, ssd_file_medium)
# truncate to same nr in all segments
for i in range(len(trial_medium.storage[129])):
    if len(trial_medium.storage[129][i]) != 2672:
        trial_medium.storage[129][i] = trial_medium.storage[129][i][:-1]

myArray_medium_STIMULUS = np.array(trial_medium.storage[129])

my_averages = []
contor = 0
for i in range(30):
    my_array = []
    for j in range(240):
        my_array.append(myArray_medium_STIMULUS[contor])
        contor = contor + 1

    for m in range(len(my_array)):
        if len(my_array[i]) != 2672:
            my_array[i] = my_array[i][:-1]
    myMatrix_medium = np.asmatrix(my_array)
    avgMatrix_medium = myMatrix_medium.mean(0)
    avgArray_medium = np.squeeze(np.asarray(avgMatrix_medium))
    my_averages.append(avgArray_medium)

print(len(my_averages[0]))
# media canalelor
myArray_medium = np.array(trial_medium.storage[129])
myMatrix_average = np.asmatrix(my_averages)
avgMatrix_medium_avg = myMatrix_average.mean(0)
avgArray_medium_final = np.squeeze(np.asarray(avgMatrix_medium_avg))
print(len(avgArray_medium_final))
plt.hlines(0, 0, 2800, "red")
plt.plot(avgArray_medium_final)
plt.ylim(-scale_conts, scale_conts)
plt.title("media_canalelor_medium", fontdict=None)
plt.xlabel("samples in time")
plt.ylabel("voltages")
# save plt somewhere
# plt.savefig("./Plots/averages'" + plt.title)
plt.show()

# DEEP
trial_deep = TrialExtractorEPD(data_dir, ssd_file_deep)
# truncate to same nr in all segments
for i in range(len(trial_deep.storage[129])):
    if len(trial_deep.storage[129][i]) != 2672:
        trial_deep.storage[129][i] = trial_deep.storage[129][i][:-1]

myArray_deep_STIMULUS = np.array(trial_deep.storage[129])

my_averages = []
contor = 0
for i in range(30):
    my_array = []
    for j in range(240):
        my_array.append(myArray_deep_STIMULUS[contor])
        contor = contor + 1

    for m in range(len(my_array)):
        if len(my_array[i]) != 2672:
            my_array[i] = my_array[i][:-1]
    myMatrix_deep = np.asmatrix(my_array)
    avgMatrix_deep = myMatrix_deep.mean(0)
    avgArray_deep = np.squeeze(np.asarray(avgMatrix_deep))
    my_averages.append(avgArray_deep)

print(len(my_averages[0]))

# media canalelor
myArray_deep = np.array(trial_deep.storage[129])
myMatrix_average = np.asmatrix(my_averages)
avgMatrix_deep_avg = myMatrix_average.mean(0)
avgArray_deep_final = np.squeeze(np.asarray(avgMatrix_deep_avg))
print(len(avgArray_deep_final))
plt.hlines(0, 0, 2800, "red")
plt.plot(avgArray_deep_final)
plt.ylim(-scale_conts, scale_conts)
plt.title("media_canalelor_deep", fontdict=None)
plt.xlabel("samples in time")
plt.ylabel("voltages")
# save plt somewhere
# plt.savefig("./Plots/averages'" + plt.title)
plt.show()

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
