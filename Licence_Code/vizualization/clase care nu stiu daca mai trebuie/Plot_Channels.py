import numpy as np
import matplotlib.pyplot as plt

from Afisare.Gui import MyApp

from input_reader.InitDataSet import InitDataSet

from input_reader.trials_outsiders.TrialsOutsiders import mark_outsiders

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
mark_outsiders(doas)


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

        trial_values = doas[doa_level].channels[channel_index].trials[trial_number - 1].spontaneous.values
        trial_values.extend(doas[doa_level].channels[channel_index].trials[trial_number - 1].stimulus.values)
        trial_values.extend(doas[doa_level].channels[channel_index].trials[trial_number - 1].poststimulus.values)

        trial_values_outsiders = []
        trial_values_outsiders.extend(doas[doa_level].channels[channel_index].trials[
                                          trial_number - 1].spontaneous.values_outsiders)
        trial_values_outsiders.extend(
            doas[doa_level].channels[channel_index].trials[trial_number - 1].stimulus.values_outsiders)
        trial_values_outsiders.extend(
            doas[doa_level].channels[channel_index].trials[trial_number - 1].poststimulus.values_outsiders)

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

        bursts_x = list(map(lambda x: x[0], outsider_points))
        bursts_y = list(map(lambda x: x[1], outsider_points))

        plt.plot(len(trial_values), list(map(lambda x: x + contor, trial_values)))

        # plt.axhline(y=channel_mean, linewidth=0.3, color='r')
        # plt.axhline(y=stdX * channel_std_der, linewidth=0.3, color='g', linestyle='--')
        # plt.axhline(y=-stdX * channel_std_der, linewidth=0.3, color='g', linestyle='--')
        #
        # for i in range(0, len(bursts_x), 2):
        #     point1 = [bursts_x[i], bursts_y[i]]
        #     point2 = [bursts_x[i + 1], bursts_y[i + 1]]
        #     x_values = [point1[0], point2[0]]
        #     y_values = [point1[1], point2[1]]
        #     if (all(i > channel_mean for i in y_values)):
        #         y_values = [stdX * channel_std_der, stdX * channel_std_der]
        #     else:
        #         y_values = [-stdX * channel_std_der, -stdX * channel_std_der]
        #     plt.plot(x_values, list(map(lambda x: x + contor, y_values)), color='black')
        #     # plt.scatter(x_values, y_values, c='black')
        contor += 50
    plt.show()

    # app = MyApp(trial_values, outsider_points, channel_number, trial_number, channel_mean, channel_std_der, y_min,
    #             y_max, stdX)
    # app.MainLoop()


channel_numbers = [2, 3]
trial_number = 14
stdX = 2

get_channel_values(doas, 0, channel_numbers, trial_number, stdX)
