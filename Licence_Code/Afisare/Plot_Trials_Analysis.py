import numpy as np
import matplotlib.pyplot as plt
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
import seaborn as sns

all_channels = [2, 6, 17]
all_trials = [[8, 15, 23], [1, 3, 18], [5, 17, 19]]

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../data_to_be_saved/alphabet_3.txt')


def get_channel_values(doas, doa_level, channel_number, trials_values):
    channel_values = []
    
    for i in range(len(trials_values)):
        channel_values.append(doas[doa_level].channels[channel_number - 1].trials[trials_values[i - 1]].stimulus.values)
    return channel_values


for i in range(len(all_channels)):
    channel_values_deep = get_channel_values(doas, 0, all_channels[i], all_trials[i])
    channel_values_light = get_channel_values(doas, 2, all_channels[i], all_trials[i])
