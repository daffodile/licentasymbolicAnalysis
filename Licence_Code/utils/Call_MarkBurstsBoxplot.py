from input_reader.InitDataSetWithBurstsFlags import InitDataSetWithBurstsFlags
from utils.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions
from vizualization.input_analysis.Plot_Channels_Trial import plot_channels_trial

initialization = InitDataSetWithBurstsFlags(levels=['deep', 'medium', 'light'])
doas = initialization.get_dataset_as_doas()



mark_bursts_regions(doas, to_extend_margins=True)

# select some trials and some channels
channel_numbers = [2, 3, 4]
stdX = 2
plot_channels_trial(doas, 'deep', channel_numbers, 5, stdX)
plot_channels_trial(doas, 'deep', channel_numbers, 6, stdX)
plot_channels_trial(doas, 'deep', channel_numbers, 14, stdX)
plot_channels_trial(doas, 'deep', channel_numbers, 11, stdX)

plot_channels_trial(doas, 'medium', channel_numbers, 5, stdX)
plot_channels_trial(doas, 'medium', channel_numbers, 6, stdX)
plot_channels_trial(doas, 'medium', channel_numbers, 14, stdX)

plot_channels_trial(doas, 'light', channel_numbers, 8, stdX)
plot_channels_trial(doas, 'light', channel_numbers, 11, stdX)
plot_channels_trial(doas, 'light', channel_numbers, 14, stdX)