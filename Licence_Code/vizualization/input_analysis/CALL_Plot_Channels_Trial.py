from input_reader.InitDataSet import InitDataSet
from utils.mark_bursts.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions

from vizualization.input_analysis.Plot_Channels_Trial import plot_channels_trial

initialization = InitDataSet(levels=['deep', 'medium', 'light'])
doas = initialization.get_dataset_as_doas()
mark_bursts_regions(doas)

# to view the plot in a new window
# go to file - settings - tools - python scientific - unmark the "show plots in tool window"
# then run the class
# after you are done go back and mark it again :)
channel_numbers = [2, 3, 4]
# trial_number = 8
trial_number = 11
plot_channels_trial(doas, 'deep', channel_numbers, trial_number)
plot_channels_trial(doas, 'light', channel_numbers, trial_number)

# plot_channels_trial(doas, 'deep', [10], 100, stdX)

# def plot_trials_channel(doas, doa_level, channel_number, trial_numbers, stdX):
# plot_trials_channel(doas, 'deep', 2, [8, 15, 23], stdX)
# plot_trials_channel(doas, 'light', 2, [8, 15, 23], stdX)
# plot_trials_channel(doas, 'deep',6, [1,3,18], stdX)
# plot_trials_channel(doas, 'light', 6, [1,3,18], stdX)
