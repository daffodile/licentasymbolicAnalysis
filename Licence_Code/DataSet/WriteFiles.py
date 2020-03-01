import os
import sys
import numpy as np

# creating the directories tree and saving the data in here

from DataSet.TrialExtractorEPD import TrialExtractorEPD

project_path = os.path.join('', '..')
data_dir = os.path.join(project_path, 'Data', '')
sys.path.append(project_path)
ssd_file_deep = 'M014_S001_SRCS3L_25,50,100_0002.epd'
ssd_file_medium = 'M014_S001_SRCS3L_25,50,100_0003.epd'
ssd_file_light = 'M014_S001_SRCS3L_25,50,100_0004.epd'

# creating the directories structure
path = os.getcwd()
print("The current working directory is %s" % path)

try:
    os.makedirs(path+"/cutoff3hz/light/spontaneous")
    os.makedirs(path+"/cutoff3hz/light/stimulus")
    os.makedirs(path+"/cutoff3hz/light/poststimulus")
    os.makedirs(path + "/cutoff3hz/medium/spontaneous")
    os.makedirs(path + "/cutoff3hz/medium/stimulus")
    os.makedirs(path + "/cutoff3hz/medium/poststimulus")
    os.makedirs(path + "/cutoff3hz/deep/spontaneous")
    os.makedirs(path + "/cutoff3hz/deep/stimulus")
    os.makedirs(path + "/cutoff3hz/deep/poststimulus")
except OSError:
    print("Creation of the directories failed")
else:
    print("Successfully created the directories")

# writing the data from all channels

# LIGHT
trial_light = TrialExtractorEPD(data_dir, ssd_file_light)
contor = 0
for i in range(30):
    fileName = path + "/cutoff3hz/light/spontaneous/" + "channel" + str(i) + ".txt"
    buffer = []
    for j in range(240):
        buffer.append(trial_light.storage[128][contor])
        contor += 1
    np.savetxt(fileName, np.array(buffer), fmt="%s")

contor = 0
for i in range(30):
    fileName = path + "/cutoff3hz/light/stimulus/" + "channel" + str(i) + ".txt"
    buffer = []
    for j in range(240):
        buffer.append(trial_light.storage[129][contor])
        contor += 1
    np.savetxt(fileName, np.array(buffer), fmt="%s")

contor = 0
for i in range(30):
    fileName = path + "/cutoff3hz/light/poststimulus/" + "channel" + str(i) + ".txt"
    buffer = []
    for j in range(240):
        buffer.append(trial_light.storage[150][contor])
        contor += 1
    np.savetxt(fileName, np.array(buffer), fmt="%s")

# MEDIUM
trial_medium = TrialExtractorEPD(data_dir, ssd_file_medium)
contor = 0
for i in range(30):
    fileName = path + "/cutoff3hz/medium/spontaneous/" + "channel" + str(i) + ".txt"
    buffer = []
    for j in range(240):
        buffer.append(trial_medium.storage[128][contor])
        contor += 1
    np.savetxt(fileName, np.array(buffer), fmt="%s")

contor = 0
for i in range(30):
    fileName = path + "/cutoff3hz/medium/stimulus/" + "channel" + str(i) + ".txt"
    buffer = []
    for j in range(240):
        buffer.append(trial_medium.storage[129][contor])
        contor += 1
    np.savetxt(fileName, np.array(buffer), fmt="%s")
contor = 0

for i in range(30):
    fileName = path + "/cutoff3hz/medium/poststimulus/" + "channel" + str(i) + ".txt"
    buffer = []
    for j in range(240):
        buffer.append(trial_medium.storage[150][contor])
        contor += 1
    np.savetxt(fileName, np.array(buffer), fmt="%s")

# DEEP
trial_deep = TrialExtractorEPD(data_dir, ssd_file_deep)
contor = 0
for i in range(30):
    fileName = path + "/cutoff3hz/deep/spontaneous/" + "channel" + str(i) + ".txt"
    buffer = []
    for j in range(240):
        buffer.append(trial_deep.storage[128][contor])
        contor += 1
    np.savetxt(fileName, np.array(buffer), fmt="%s")

contor = 0
for i in range(30):
    fileName = path + "/cutoff3hz/deep/stimulus/" + "channel" + str(i) + ".txt"
    buffer = []
    for j in range(240):
        buffer.append(trial_deep.storage[129][contor])
        contor += 1
    np.savetxt(fileName, np.array(buffer), fmt="%s")

contor = 0
for i in range(30):
    fileName = path + "/cutoff3hz/deep/poststimulus/" + "channel" + str(i) + ".txt"
    buffer = []
    for j in range(240):
        buffer.append(trial_deep.storage[150][contor])
        contor += 1
    np.savetxt(fileName, np.array(buffer), fmt="%s")