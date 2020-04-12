import numpy as np
from input_reader.InitDataSet import InitDataSet
from utils.Utils import get_doa_of_level
from vizualization.classification.barplots.Plot_Classidications_Comparison import plot_accuracies

initialization = InitDataSet(levels=['deep', 'medium', 'light'])
doas = initialization.get_dataset_as_doas()
print('doas is initialized')

for doa in doas:
    for channel in doa.channels:
        all_trials = []
        for trial in channel.trials:
            all_trials.extend(trial.spontaneous.values)
            all_trials.extend(trial.stimulus.values)
            all_trials.extend(trial.poststimulus.values)

        channel.mean = np.mean(all_trials)
        channel.std_der = np.std(all_trials)

        print(f'ch {channel.number}  mean:{channel.mean} std_dev:{channel.std_der}')

deep_ch_std_dev = []
doa_deep = get_doa_of_level(doas, 'deep')
for channel in doa_deep.channels:
    deep_ch_std_dev.append(channel.std_der)
print(deep_ch_std_dev)

medium_ch_std_dev = []
doa_medium = get_doa_of_level(doas, 'medium')
for channel in doa_medium.channels:
    medium_ch_std_dev.append(channel.std_der)
print(medium_ch_std_dev)

light_ch_std_dev = []
doa_light = get_doa_of_level(doas, 'light')
for channel in doa_light.channels:
    light_ch_std_dev.append(channel.std_der)
print(light_ch_std_dev)

liberty = 2

# deep_ch_std_dev = np.array([15.6277895, 16.456755, 18.791197, 16.401697, 15.685874, 16.447874, 18.92527, 20.633675, 15.507578, 15.592471, 15.443601, 15.675891, 19.181395, 17.218128, 21.537216, 17.998425, 22.012562, 19.509695, 15.313929, 19.00414, 18.008686, 18.062094, 18.94927, 14.584183, 18.82349, 14.412116, 18.882706, 19.533562, 17.911766, 21.255026])
deep_ch_std_dev = np.array(deep_ch_std_dev)
deep_ch_std_dev = deep_ch_std_dev * liberty
print(deep_ch_std_dev)

# medium_ch_std_dev = np.array([16.174229, 16.917479, 18.701847, 16.88359, 16.242363, 16.923082, 18.840908, 20.409002, 15.665453, 15.745739, 15.588113, 15.854504, 19.7175, 17.374565, 21.349606, 16.54929, 20.286026, 16.036114, 12.739031, 15.6571045, 15.506242, 15.573513, 16.013988, 13.672046, 15.902976, 13.516427, 15.95255, 17.489334, 16.470045, 19.2989])
medium_ch_std_dev = np.array(medium_ch_std_dev)
medium_ch_std_dev = medium_ch_std_dev * liberty
print(medium_ch_std_dev)

# light_ch_std_dev = np.array([17.049717, 18.720375, 21.32228, 18.700912, 17.126062, 18.74221, 21.481865, 23.899158, 17.39078, 17.472637, 17.298206, 17.191605, 22.519993, 19.408073, 25.111269, 16.135138, 23.386026, 15.873243, 11.343981, 14.894734, 15.115401, 15.193554, 16.718191, 13.493089, 16.593454, 13.3432, 16.65473, 18.18171, 16.058987, 21.77484])
light_ch_std_dev = np.array(light_ch_std_dev)
light_ch_std_dev = light_ch_std_dev * liberty
print(light_ch_std_dev)

labels = ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17',
          'C18', 'C19', 'C20', 'C21', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30',
          'C31', 'C32']

legend_names = ['deep', 'medium', 'light']

plot_accuracies(labels, [deep_ch_std_dev, medium_ch_std_dev, light_ch_std_dev], legend_names,
                segment=f'liberty={liberty}',
                title='Channels amplitudes')
