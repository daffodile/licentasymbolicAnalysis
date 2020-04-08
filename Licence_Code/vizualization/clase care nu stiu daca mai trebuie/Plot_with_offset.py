import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from input_reader.InitDataSet import InitDataSet
from input_reader.trials_outsiders.TrialsOutsiders import mark_outsiders

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
mark_outsiders(doas)

#################data
trial1 = []
trial_values_spontaneous = doas[0].channels[0].trials[14 - 1].spontaneous.values
trial1.extend(trial_values_spontaneous)
trial_values_stimulus = doas[0].channels[0].trials[14 - 1].stimulus.values
trial1.extend(trial_values_stimulus)
trial_values_poststimulus = doas[0].channels[0].trials[14 - 1].poststimulus.values
trial1.extend(trial_values_poststimulus)

trial2 = []
trial_values_spontaneous2 = doas[0].channels[10].trials[14 - 1].spontaneous.values
trial2.extend(trial_values_spontaneous2)
trial_values_stimulus2 = doas[0].channels[10].trials[14 - 1].stimulus.values
trial2.extend(trial_values_stimulus2)
trial_values_poststimulus2 = doas[0].channels[10].trials[14 - 1].poststimulus.values
trial2.extend(trial_values_poststimulus2)
#################data


len_trial1 = []
for i in range(len(trial1)):
    len_trial1.append(i)

len_trial2 = []
for i in range(len(trial2)):
    len_trial2.append(i)
trials = []
trials.append((len_trial1, trial1))
trials.append((len_trial2, trial2))

contor = 0
for j in range(len(trials)):
    plt.plot(trials[j][0], list(map(lambda x: x + contor, trials[j][1])))
    contor += 50

# plt.plot(len_trial1, trial1)
# plt.plot(len_trial2, )

# for i in range(len(trials)):
#
#
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.plot(trial1)
# ax.plot(trial2)

plt.show()
