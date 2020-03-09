import os
import sys
import numpy as np

import matplotlib.pyplot as plt

from Tests.DataSet.TrialExtractorEPD import TrialExtractorEPD

project_path = os.path.join('', '..')
data_dir = os.path.join(project_path, 'data', '')
sys.path.append(project_path)
ssd_file_deep = 'M014_S001_SRCS3L_25,50,100_0002.epd'
ssd_file_medium = 'M014_S001_SRCS3L_25,50,100_0003.epd'
ssd_file_light = 'M014_S001_SRCS3L_25,50,100_0004.epd'

# # LIGHT
# trial_light = TrialExtractorEPD(data_dir, ssd_file_light)
#
# for i in range(len(trial_light.storage[129])):
#     if len(trial_light.storage[129][i]) != 2672:
#         trial_light.storage[129][i] = trial_light.storage[129][i][:-1]
#
# myArray_light_STIMULUS = np.array(trial_light.storage[129])
# print(myArray_light_STIMULUS[0])
#
# symbols_array = []
# d = 0    # number of values in this interval
# s = 0    # number fo local minima in this array
#
# # for i in range(len(myArray_light_STIMULUS[0])):
# #     if myArray_light_STIMULUS[i] == 0:
# #         symbols_array.append({d, })
# #

# LIGHT
trial_light = TrialExtractorEPD(data_dir, ssd_file_light)
# print(len(trial_light.storage[129]))   # 21600

# # # cleaning the storage to have only arrays with length 2672, so delete the last element if the size is 2673
# for i in range(len(trial_light.storage[129])):
#     print(len(trial_light.storage[129][i]))
#     if len(trial_light.storage[129][i]) != 2672:
#         trial_light.storage[129][i] = trial_light.storage[129][i][:-1]

array_0_0_light = np.array(trial_light.storage[129][413])
array_to_plot = np.squeeze(array_0_0_light)
scale_conts = 80
plt.plot(array_to_plot)
plt.hlines(0, 0, 2800, "red")
plt.title("channel 2 trial 174 light", fontdict=None)
plt.ylim(-scale_conts, scale_conts)
plt.xlabel("samples")
plt.ylabel("voltages")
plt.savefig("../Plots/channels/channel_2_trial_174_light80")
plt.show()

array_0_0_light = np.array(trial_light.storage[129][359])
array_to_plot = np.squeeze(array_0_0_light)
scale_conts = 80
plt.plot(array_to_plot)
plt.hlines(0, 0, 2800, "red")
plt.title("channel 2 trial 120 light", fontdict=None)
plt.ylim(-scale_conts, scale_conts)
plt.xlabel("samples")
plt.ylabel("voltages")
plt.savefig("../Plots/channels/channel_2_trial_120_light80")
plt.show()

array_0_0_light = np.array(trial_light.storage[129][363])
array_to_plot = np.squeeze(array_0_0_light)
scale_conts = 80
plt.plot(array_to_plot)
plt.hlines(0, 0, 2800, "red")
plt.title("channel 2 trial 124 light", fontdict=None)
plt.ylim(-scale_conts, scale_conts)
plt.xlabel("samples")
plt.ylabel("voltages")
plt.savefig("../Plots/channels/channel_2_trial_124_light80")
plt.show()

array_0_0_light = np.array(trial_light.storage[129][327])
array_to_plot = np.squeeze(array_0_0_light)
scale_conts = 80
plt.plot(array_to_plot)
plt.hlines(0, 0, 2800, "red")
plt.title("channel 2 trial 88 light", fontdict=None)
plt.ylim(-scale_conts, scale_conts)
plt.xlabel("samples")
plt.ylabel("voltages")
plt.savefig("../Plots/channels/channel_2_trial_88_light80")
plt.show()

array_0_0_light = np.array(trial_light.storage[129][408])
array_to_plot = np.squeeze(array_0_0_light)
scale_conts = 80
plt.plot(array_to_plot)
plt.hlines(0, 0, 2800, "red")
plt.title("channel 2 trial 168 light", fontdict=None)
plt.ylim(-scale_conts, scale_conts)
plt.xlabel("samples")
plt.ylabel("voltages")
plt.savefig("../Plots/channels/channel_2_trial_168_light80")
plt.show()

array_0_0_light = np.array(trial_light.storage[129][410])
array_to_plot = np.squeeze(array_0_0_light)
scale_conts = 80
plt.plot(array_to_plot)
plt.hlines(0, 0, 2800, "red")
plt.title("channel 2 trial 170 light", fontdict=None)
plt.ylim(-scale_conts, scale_conts)
plt.xlabel("samples")
plt.ylabel("voltages")
plt.savefig("../Plots/channels/channel_2_trial_170_light80")
plt.show()

array_0_0_light = np.array(trial_light.storage[129][414])
array_to_plot = np.squeeze(array_0_0_light)
scale_conts = 80
plt.plot(array_to_plot)
plt.hlines(0, 0, 2800, "red")
plt.title("channel 2 trial 172 light", fontdict=None)
plt.ylim(-scale_conts, scale_conts)
plt.xlabel("samples")
plt.ylabel("voltages")
plt.savefig("../Plots/channels/channel_2_trial_172_light80")
plt.show()

array_0_0_light = np.array(trial_light.storage[129][414])
array_to_plot = np.squeeze(array_0_0_light)
scale_conts = 80
plt.plot(array_to_plot)
plt.hlines(0, 0, 2800, "red")
plt.title("channel 2 trial 174 light", fontdict=None)
plt.ylim(-scale_conts, scale_conts)
plt.xlabel("samples")
plt.ylabel("voltages")
plt.savefig("../Plots/channels/channel_2_trial_174_light80")
plt.show()
