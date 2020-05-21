import os
import numpy as np
from input_reader.InitDataSet import InitDataSet
from utils.mark_bursts.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions

data_dir = os.path.join('..', '..')
initialization = InitDataSet(current_directory=data_dir, subject_directory='m014', filtering_directory='highpass10',
                             levels=['light1', 'deep2', 'medium3', 'light4', 'medium5'])
doas = initialization.get_dataset_as_doas()
mark_bursts_regions(doas)

all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
                31, 32]

labels = ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17',
          'C18', 'C19', 'C20', 'C21', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30',
          'C31', 'C32']

light1_channels_means, light1_channels_bursts_means, light1_channels_nonbursts_means = get_doa_means_statistics(doas,
                                                                                                                'light1',
                                                                                                                all_channels)
deep2_channels_means, deep2_channels_bursts_means, deep2_channels_nonbursts_means = get_doa_means_statistics(doas,
                                                                                                             'deep2',
                                                                                                             all_channels)
medium3_channels_means, medium3_channels_bursts_means, medium3_channels_nonbursts_means = get_doa_means_statistics(doas,
                                                                                                                   'medium3',
                                                                                                                   all_channels)
light4_channels_means, light4_channels_bursts_means, light4_channels_nonbursts_means = get_doa_means_statistics(doas,
                                                                                                                'light4',
                                                                                                                all_channels)
medium5_channels_means, medium5_channels_bursts_means, medium5_channels_nonbursts_means = get_doa_means_statistics(doas,
                                                                                                                   'medium5',
                                                                                                                   all_channels)

# plot1 --- mean_burts / mean_total
light1_bursts_div_total = np.divide(light1_channels_bursts_means, light1_channels_means)
deep2_bursts_div_total = np.divide(deep2_channels_bursts_means, deep2_channels_means)
medium3_bursts_div_total = np.divide(medium3_channels_bursts_means, medium3_channels_means)
light4_bursts_div_total = np.divide(light4_channels_bursts_means, light4_channels_means)
medium5_bursts_div_total = np.divide(medium5_channels_bursts_means, medium5_channels_means)
f = open("plot1_m014classic.txt", "w+")
f.write("light1\n")
for i in range(len(light1_bursts_div_total)):
    f.write(str(light1_bursts_div_total[i]) + "\n")
f.write("deep2\n")
for i in range(len(deep2_bursts_div_total)):
    f.write(str(deep2_bursts_div_total[i]) + "\n")
f.write("medium3\n")
for i in range(len(medium3_bursts_div_total)):
    f.write(str(medium3_bursts_div_total[i]) + "\n")
f.write("light4\n")
for i in range(len(light4_bursts_div_total)):
    f.write(str(light4_bursts_div_total[i]) + "\n")
f.write("medium5\n")
for i in range(len(medium5_bursts_div_total)):
    f.write(str(medium5_bursts_div_total[i]) + "\n")
f.close()
plot_means(labels, [light1_bursts_div_total, deep2_bursts_div_total, medium3_bursts_div_total, light4_bursts_div_total,
                    medium5_bursts_div_total],
           'Bursts Mean reported to Full Channel Mean - M014 Classic')

# plot2 --- mean_burts / mean non_bursts
light1_bursts_div_nonbursts = np.divide(light1_channels_bursts_means, light1_channels_nonbursts_means)
deep2_bursts_div_nonbursts = np.divide(deep2_channels_bursts_means, deep2_channels_nonbursts_means)
medium3_bursts_div_nonbursts = np.divide(medium3_channels_bursts_means, medium3_channels_nonbursts_means)
light4_bursts_div_nonbursts = np.divide(light4_channels_bursts_means, light4_channels_nonbursts_means)
medium5_bursts_div_nonbursts = np.divide(medium5_channels_bursts_means, medium5_channels_nonbursts_means)
f = open("plot2_m014classic.txt", "w+")
f.write("light1\n")
for i in range(len(light1_bursts_div_nonbursts)):
    f.write(str(light1_bursts_div_nonbursts[i]) + "\n")
f.write("deep2\n")
for i in range(len(deep2_bursts_div_nonbursts)):
    f.write(str(deep2_bursts_div_nonbursts[i]) + "\n")
f.write("medium3\n")
for i in range(len(medium3_bursts_div_nonbursts)):
    f.write(str(medium3_bursts_div_nonbursts[i]) + "\n")
f.write("light4\n")
for i in range(len(light4_bursts_div_nonbursts)):
    f.write(str(light4_bursts_div_nonbursts[i]) + "\n")
f.write("medium5\n")
for i in range(len(medium5_bursts_div_nonbursts)):
    f.write(str(medium5_bursts_div_nonbursts[i]) + "\n")
f.close()
plot_means(labels, [light1_bursts_div_nonbursts, deep2_bursts_div_nonbursts, medium3_bursts_div_nonbursts,
                    light4_bursts_div_nonbursts, medium5_bursts_div_nonbursts],
           'Bursts Mean reported to Non-Bursts Mean - M014 Classic')

for ch_nr in range(len(all_channels)):
    print('Channel ' + str(all_channels[ch_nr]) + ' light1 ' + str(
        get_channel_maximum_burst(doas, 'light1', all_channels[ch_nr])))
    print('Channel ' + str(all_channels[ch_nr]) + ' deep2 ' + str(
        get_channel_maximum_burst(doas, 'deep2', all_channels[ch_nr])))
    print('Channel ' + str(all_channels[ch_nr]) + ' medium3 ' + str(
        get_channel_maximum_burst(doas, 'medium3', all_channels[ch_nr])))
    print('Channel ' + str(all_channels[ch_nr]) + ' light4 ' + str(
        get_channel_maximum_burst(doas, 'light4', all_channels[ch_nr])))
    print('Channel ' + str(all_channels[ch_nr]) + ' medium5 ' + str(
        get_channel_maximum_burst(doas, 'medium5', all_channels[ch_nr])))
