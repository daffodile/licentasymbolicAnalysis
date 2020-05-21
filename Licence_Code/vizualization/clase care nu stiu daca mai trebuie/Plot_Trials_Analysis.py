import numpy as np
import matplotlib.pyplot as plt
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
import seaborn as sns

from utils.TreatBurstingSegmentsInTrials import mark_outsiders

all_channels = [2, 6, 17]
trial_number = 14

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
# mark_outsiders(doas)
encoding = Encoding('./../data_to_be_saved/m014_classic_alphabet_3.txt')


def statistic(doas):
    for doa in doas:
        for channel in doa.channels:
            all_trials = []
            for trial in channel.trials:
                all_trials.extend(trial.spontaneous.values)
                all_trials.extend(trial.stimulus.values)
                all_trials.extend(trial.poststimulus.values)

            # channel.mean = np.mean(all_trials)
            # channel.std_der = np.std(all_trials)
