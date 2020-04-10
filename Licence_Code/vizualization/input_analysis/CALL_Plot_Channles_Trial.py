'''
    written by Ioana Onofrei
'''
from input_reader.InitDataSet import InitDataSet
from utils.TrialsOutsiders import mark_outsiders
from vizualization.input_analysis.Plot_Channels_Trial import plot_channels_trial

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
mark_outsiders(doas)

# to view the plot in a new window
# go to file - settings - tools - python scientific - unmark the "show plots in tool window"
# then run the class
# after you are done go back and mark it again :)
channel_numbers = [2, 3, 4]
trial_number = 14
stdX = 2
plot_channels_trial(doas, 'deep', channel_numbers, trial_number, stdX)

plot_channels_trial(doas, 'deep', [10], 100, stdX)