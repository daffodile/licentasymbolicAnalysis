import numpy as np

from input_reader.InitDataSet import InitDataSet
from utils.Utils import get_doa_of_level
from vizualization.analysis.ploting_functions import plot_hist


def get_channel_from_doa(doas, level, ch_number):
    doa = get_doa_of_level(doas, level)
    channel = list(filter(lambda ch: (ch.number == ch_number), doa.channels))[0]
    return channel


initialization = InitDataSet(levels=['deep', 'medium', 'light'])
# initialization = InitDataSet(levels=['light'])
doas = initialization.get_dataset_as_doas()
print('doas is initialized')

#################################################### bad channel ###################################################
# distribution of amplitudes for channel 20 DEEP
# ch_deep = get_channel_from_doa(doas, 'deep', 20)
#
# trials_values_deep = []
# for trial in ch_deep.trials:
#     trials_values_deep.extend(trial.spontaneous.values)
#     trials_values_deep.extend(trial.stimulus.values)
#
# plot_hist(trials_values_deep, bins=100, log=False, to_save=True, file_name='20deep.png', title="DEEP ch 20 spon_stim",
#           x_label='Amplitudes', y_label='Counts')
#
#
# # distribution of amplitudes for channel 5 MEDIUM
# ch_medium = get_channel_from_doa(doas, 'medium', 20)
#
# trials_values_medium = []
# for trial in ch_medium.trials:
#     trials_values_medium.extend(trial.spontaneous.values)
#     trials_values_medium.extend(trial.stimulus.values)

# plot_hist(trials_values_medium, bins=100, to_save=True, file_name='20medium.png', title="MEDIUM ch 20 spon_stim",
#           x_label='Amplitudes', y_label='Counts')
# plot_hist(np.abs(trials_values_medium), bins=100, to_save=True, file_name='20medium_abs.png',
#           title="MEDIUM ch 20 spon_stim", x_label='Amplitudes',
#           y_label='Counts')

# distribution of amplitudes for channel 5 LIGHT
# ch_light = get_channel_from_doa(doas, 'light', 20)
#
# trials_values_light = []
# for trial in ch_light.trials:
#     trials_values_light.extend(trial.spontaneous.values)
#     trials_values_light.extend(trial.stimulus.values)
#
# plot_hist(trials_values_light, bins=100, to_save=True, file_name='20light.png', title="LIGHT ch 20 spon_stim",
#           x_label='Amplitudes', y_label='Counts')
# # plot_hist(np.abs(trials_values_light), bins=100, to_save=True, file_name='20light_abs.png',
# #           title="LIGHT ch 20 spon_stim", x_label='Amplitudes', y_label='Counts')
#
# trials_all = []
# trials_all.extend(trials_values_deep)
# trials_all.extend(trials_values_medium)
# trials_all.extend(trials_values_light)
#
# plot_hist(trials_all, bins=100, to_save=True, file_name='20all.png', title="All DOAs ch 20 spon_stim",
#           x_label='Amplitudes', y_label='Counts')
# # plot_hist(np.abs(trials_all), bins=100, to_save=True, file_name='20all_abs.png', title="All DOAs ch 20 spon_stim",
# #           x_label='Amplitudes', y_label='Counts')
#
# ########################################## good channel #####################################################
# # # distribution of amplitudes for channel 5 DEEP
# ch_deep = get_channel_from_doa(doas, 'deep', 5)
#
# trials_values_deep = []
# for trial in ch_deep.trials:
#     trials_values_deep.extend(trial.spontaneous.values)
#     trials_values_deep.extend(trial.stimulus.values)
#
# plot_hist(trials_values_deep, bins=100, to_save=True, file_name='5deep.png', title="DEEP ch 5 spon_stim",
#           x_label='Amplitudes', y_label='Counts')
# # plot_hist(np.abs(trials_values_deep), bins=100, to_save=True, file_name='5deep_abs.png', title="DEEP ch 5 spon_stim",
# #           x_label='Amplitudes', y_label='Counts')
#
# # distribution of amplitudes for channel 5 MEDIUM
# ch_medium = get_channel_from_doa(doas, 'medium', 5)
#
# trials_values_medium = []
# for trial in ch_medium.trials:
#     trials_values_medium.extend(trial.spontaneous.values)
#     trials_values_medium.extend(trial.stimulus.values)
#
# plot_hist(trials_values_medium, bins=100, to_save=True, file_name='5medium.png', title="MEDIUM ch 5 spon_stim",
#           x_label='Amplitudes', y_label='Counts')
# # plot_hist(np.abs(trials_values_medium), bins=100, to_save=True, file_name='5medium_abs.png',
# #           title="MEDIUM ch 5 spon_stim", x_label='Amplitudes', y_label='Counts')

# # distribution of amplitudes for channel 5 LIGHT
# ch_light = get_channel_from_doa(doas, 'light', 5)
#
# trials_values_light = []
# for trial in ch_light.trials:
#     trials_values_light.extend(trial.spontaneous.values)
#     trials_values_light.extend(trial.stimulus.values)
#
# plot_hist(trials_values_light, bins=100,  to_save=True, file_name='5light.png', title="LIGHT ch 5 spon_stim", x_label='Amplitudes', y_label='Counts')
# plot_hist(np.abs(trials_values_light), bins=100,  to_save=True, file_name='5light_abs.png', title="LIGHT ch 5 spon_stim", x_label='Amplitudes', y_label='Counts')

# trials_all = []
# trials_all.extend(trials_values_deep)
# trials_all.extend(trials_values_medium)
# trials_all.extend(trials_values_light)
#
# plot_hist(trials_all, bins=100, to_save=True, file_name='5all.png', title="All DOAs ch 5 spon_stim",
#           x_label='Amplitudes', y_label='Counts')
# # plot_hist(np.abs(trials_all), bins=100, to_save=True, file_name='5all_abs.png', title="All DOAs ch 5 spon_stim",
# #           x_label='Amplitudes', y_label='Counts')
