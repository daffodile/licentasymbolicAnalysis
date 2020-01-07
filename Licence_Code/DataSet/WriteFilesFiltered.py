import os
import sys
import numpy as np

# creating the directories tree and saving the data in here
from DataSet.HighPassFilterPreProcessing import HighPassFilterPreProcessing
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
    os.makedirs(path+"/lightFiltered/spontaneous")
    os.makedirs(path+"/lightFiltered/stimulus")
    os.makedirs(path+"/lightFiltered/poststimulus")
    os.makedirs(path + "/mediumFiltered/spontaneous")
    os.makedirs(path + "/mediumFiltered/stimulus")
    os.makedirs(path + "/mediumFiltered/poststimulus")
    os.makedirs(path + "/deepFiltered/spontaneous")
    os.makedirs(path + "/deepFiltered/stimulus")
    os.makedirs(path + "/deepFiltered/poststimulus")
except OSError:
    print("Creation of the directories failed")
else:
    print("Successfully created the directories")

# writing the data from all channels

# LIGHT
trial_light = TrialExtractorEPD(data_dir, ssd_file_light)
contor = 0
for i in range(30):
    fileName = path + "/lightFiltered/spontaneous/" + "channel" + str(i) + ".txt"
    buffer = []
    for j in range(240):
        hp = HighPassFilterPreProcessing(trial_light.storage[128][contor])
        buffer.append(hp.finalArray)
        contor += 1
    np.savetxt(fileName, np.array(buffer), fmt="%s")

contor = 0
for i in range(30):
    fileName = path + "/lightFiltered/stimulus/" + "channel" + str(i) + ".txt"
    buffer = []
    for j in range(240):
        hp = HighPassFilterPreProcessing(trial_light.storage[129][contor])
        buffer.append(hp.finalArray)
        contor += 1
    np.savetxt(fileName, np.array(buffer), fmt="%s")

contor = 0
for i in range(30):
    fileName = path + "/lightFiltered/poststimulus/" + "channel" + str(i) + ".txt"
    buffer = []
    for j in range(240):
        hp = HighPassFilterPreProcessing(trial_light.storage[150][contor])
        buffer.append(hp.finalArray)
        contor += 1
    np.savetxt(fileName, np.array(buffer), fmt="%s")

# MEDIUM
trial_medium = TrialExtractorEPD(data_dir, ssd_file_medium)
contor = 0
for i in range(30):
    fileName = path + "/mediumFiltered/spontaneous/" + "channel" + str(i) + ".txt"
    buffer = []
    for j in range(240):
        hp = HighPassFilterPreProcessing(trial_medium.storage[128][contor])
        buffer.append(hp.finalArray)
        contor += 1
    np.savetxt(fileName, np.array(buffer), fmt="%s")

contor = 0
for i in range(30):
    fileName = path + "/mediumFiltered/stimulus/" + "channel" + str(i) + ".txt"
    buffer = []
    for j in range(240):
        hp = HighPassFilterPreProcessing(trial_medium.storage[129][contor])
        buffer.append(hp.finalArray)
        contor += 1
    np.savetxt(fileName, np.array(buffer), fmt="%s")
contor = 0

for i in range(30):
    fileName = path + "/mediumFiltered/poststimulus/" + "channel" + str(i) + ".txt"
    buffer = []
    for j in range(240):
        hp = HighPassFilterPreProcessing(trial_medium.storage[150][contor])
        buffer.append(hp.finalArray)
        contor += 1
    np.savetxt(fileName, np.array(buffer), fmt="%s")

# DEEP
trial_deep = TrialExtractorEPD(data_dir, ssd_file_deep)
contor = 0
for i in range(30):
    fileName = path + "/deepFiltered/spontaneous/" + "channel" + str(i) + ".txt"
    buffer = []
    for j in range(240):
        hp = HighPassFilterPreProcessing(trial_deep.storage[128][contor])
        buffer.append(hp.finalArray)
        contor += 1
    np.savetxt(fileName, np.array(buffer), fmt="%s")

contor = 0
for i in range(30):
    fileName = path + "/deepFiltered/stimulus/" + "channel" + str(i) + ".txt"
    buffer = []
    for j in range(240):
        hp = HighPassFilterPreProcessing(trial_deep.storage[129][contor])
        buffer.append(hp.finalArray)
        contor += 1
    np.savetxt(fileName, np.array(buffer), fmt="%s")

contor = 0
for i in range(30):
    fileName = path + "/deepFiltered/poststimulus/" + "channel" + str(i) + ".txt"
    buffer = []
    for j in range(240):
        hp = HighPassFilterPreProcessing(trial_deep.storage[150][contor])
        buffer.append(hp.finalArray)
        contor += 1
    np.savetxt(fileName, np.array(buffer), fmt="%s")