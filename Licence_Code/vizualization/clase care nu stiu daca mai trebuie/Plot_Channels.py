import numpy as np
import matplotlib.pyplot as plt

from input_reader.InitDataSet import InitDataSet
from utils.TrialsOutsiders import mark_outsiders
from utils.Utils import get_trial_values_and_outsiders


def get_channel_index(doas, channel_number):
    for i in range(30):
        if doas[0].channels[i].number == channel_number:
            return i


def get_channel_values(doas, doa_level, channel_numbers, trial_number, stdX):
    contor = 0
    for ch_number in range(len(channel_numbers)):
        channel_index = get_channel_index(doas, channel_numbers[ch_number])

        channel_mean = doas[doa_level].channels[channel_index].mean
        channel_std_der = doas[doa_level].channels[channel_index].std_der

        trial_values, trial_values_outsiders = get_trial_values_and_outsiders(doas, 'deep',
                                                                              channel_numbers[ch_number],
                                                                              trial_number)
        outsider_points = []
        if (trial_values_outsiders[0] == 1):
            outsider_points.append((0, trial_values[0]))
        for i in range(len(trial_values_outsiders) - 1):
            if (trial_values_outsiders[i] == 0 and trial_values_outsiders[i + 1] == 1):
                outsider_points.append((i + 1, trial_values[i + 1]))
            if (trial_values_outsiders[i] == 1 and trial_values_outsiders[i + 1] == 0):
                outsider_points.append((i, trial_values[i]))
        if (trial_values_outsiders[len(trial_values_outsiders) - 1] == 1):
            outsider_points.append((len(trial_values_outsiders) - 1, trial_values[len(trial_values_outsiders) - 1]))

        print(outsider_points)

        plt.plot(np.arange(0, len(trial_values)), list(map(lambda x: x + contor, trial_values)),
                 label='Channel ' + str(channel_numbers[ch_number]))

        plt.axhline(y=channel_mean + contor, linewidth=0.3, color='r')

        for i in range(0, len(outsider_points), 2):
            x_values = [outsider_points[i][0], outsider_points[i + 1][0]]
            y_values = [channel_mean + contor, channel_mean + contor]
            plt.plot(x_values, y_values, color='black')
        contor += 100

    # plt.legend(loc=(1.05, 0.5))
    # plt.tight_layout()

    plt.ylabel('Amplitudes')
    plt.xlabel('Relative Timestamp')
    plt.title('Trial ' + str(trial_number) + ' Snapshot')
    # Put a legend below current axis
    plt.legend(loc='upper center', bbox_to_anchor=(0.2, -0.05),
              fancybox=True, shadow=True, ncol=5)
    plt.show()

    # app = MyApp(trial_values, outsider_points, channel_number, trial_number, channel_mean, channel_std_der, y_min,
    #             y_max, stdX)
    # app.MainLoop()


initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
mark_outsiders(doas)

channel_numbers = [2,3,4]
trial_number = 14
stdX = 2

# to view the plot in a new window
# go to file - settings - tools - python scientific - unmark the "show plots in tool window"
# then run the class
# after you are done go back and mark it again :)
get_channel_values(doas, 0, channel_numbers, trial_number, stdX)
