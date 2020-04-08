import np as np
import numpy as np

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from input_reader.Models import DOA
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import seaborn as sns

encoder = Encoding('./../data_to_be_saved/alphabet_3hz.txt')


def plot_matrix_A(a_matrix, DOA, trial, segment, channel_nr, lag):
    # ax = sns.heatmap(np.log10([[v + 1 for v in r] for r in a_matrix]), cmap="YlGnBu", vmin=0, vmax=5)
    ax = sns.heatmap(a_matrix, cmap="YlGnBu",  vmin=0, vmax=10)
    ax.invert_yaxis()
    plt.xlabel("Symbols lag " + str(lag))
    plt.ylabel("Symbols lag " + str(lag))
    plt.title("A Matrix " + DOA + " " + str(trial) + " " + str(segment) + " ch: " + str(channel_nr))
    plot_name = 'log/channel' + str(channel_nr) + "_" + DOA + "_" + segment + "_lag" + str(lag) + "_A.png"
    # plt.savefig(plot_name)
    plt.show()


def differences_A(doas, ch_nr, trial_nr, segment):

    # doas_array = np.array(doas, dtype=DOA)
    # # open the wanted DOAs - DEEP and LIGHT
    # doa_deep = np.extract(condition=(lambda x: x.level == "deep"), arr=doas_array)[0]
    # doa_light = np.extract(condition=(lambda x: x.level == "light"), arr=doas_array)[0]

    t_deep = doas[0].channels[ch_nr].trials[trial_nr]
    t_light = doas[2].channels[ch_nr].trials[trial_nr]

    deep_spontaneous_a = np.array(encoder.get_a(t_deep.spontaneous.values, 1))
    print(deep_spontaneous_a)
    plot_matrix_A(deep_spontaneous_a, 'deep',  trial_nr, segment, ch_nr, 1)

    light_spontaneous_a = np.array(encoder.get_a(t_light.spontaneous.values, 1))
    print(light_spontaneous_a)
    plot_matrix_A(light_spontaneous_a, 'light', trial_nr, segment, ch_nr, 1)

    diff_spontaneous = np.absolute(deep_spontaneous_a - light_spontaneous_a)
    plot_matrix_A(diff_spontaneous, 'deep-light', trial_nr, segment, ch_nr, 1)

    # diff_stimulus = np.absolute(np.array(encoder.get_a(t_deep.stimulus.values, lag)) -
    #                              np.array(encoder.get_a(t_light.stimulus.values, lag)))
    #
    # diff_poststimulus += np.absolute(np.array(encoder.get_a(t_deep.poststimulus.values, lag)) -
    #                                  np.array(encoder.get_a(t_light.poststimulus.values, lag)))

    # plt.figure()
    # fig, axs = plt.subplots(nrows=2, ncols=2, sharex=True)


initialization = InitDataSet()

doas = initialization.get_dataset_as_doas()

differences_A(doas, 13, 24, "spontaneous")
print('a 2 a')
differences_A(doas, 11, 100, "spontaneous")
