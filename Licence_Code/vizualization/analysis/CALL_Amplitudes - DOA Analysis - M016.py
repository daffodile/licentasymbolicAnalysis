import os
import numpy as np
from input_reader.InitDataSet import InitDataSet
from utils.mark_bursts.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions

data_dir = os.path.join('..', '..')
initialization = InitDataSet(current_directory=data_dir, subject_directory='m016', filtering_directory='classic',
                             levels=['deep6', 'light7', 'medium8', 'deep9', 'medium10', 'light11'])
doas = initialization.get_dataset_as_doas()
mark_bursts_regions(doas)


all_channels = [1, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
                30,
                31, 32]
labels = ['C1', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17',
          'C18', 'C19', 'C20', 'C21', 'C22', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30',
          'C31', 'C32']

deep6_channels_means, deep6_channels_bursts_means, deep6_channels_nonbursts_means = get_doa_means_statistics(doas,
                                                                                                                'deep6',
                                                                                                                all_channels)
light7_channels_means, light7_channels_bursts_means, light7_channels_nonbursts_means = get_doa_means_statistics(doas,
                                                                                                             'light7',
                                                                                                             all_channels)
medium8_channels_means, medium8_channels_bursts_means, medium8_channels_nonbursts_means = get_doa_means_statistics(doas,
                                                                                                                   'medium8',
                                                                                                                   all_channels)
deep9_channels_means, deep9_channels_bursts_means, deep9_channels_nonbursts_means = get_doa_means_statistics(doas,
                                                                                                                'deep9',
                                                                                                                all_channels)
medium10_channels_means, medium10_channels_bursts_means, medium10_channels_nonbursts_means = get_doa_means_statistics(doas,
                                                                                                                   'medium10',
                                                                                                                   all_channels)
light11_channels_means, light11_channels_bursts_means, light11_channels_nonbursts_means = get_doa_means_statistics(doas,
                                                                                                                   'light11',
                                                                                                                   all_channels)

# plot1 --- mean_burts / mean_total
deep6_bursts_div_total = np.divide(deep6_channels_bursts_means, deep6_channels_means)
light7_bursts_div_total = np.divide(light7_channels_bursts_means, light7_channels_means)
medium8_bursts_div_total = np.divide(medium8_channels_bursts_means, medium8_channels_means)
deep9_bursts_div_total = np.divide(deep9_channels_bursts_means, deep9_channels_means)
medium10_bursts_div_total = np.divide(medium10_channels_bursts_means, medium10_channels_means)
light11_bursts_div_total = np.divide(light11_channels_bursts_means, light11_channels_means)
f = open("plot1_m016classic.txt", "w+")
f.write("deep6\n")
for i in range(len(deep6_bursts_div_total)):
    f.write(str(deep6_bursts_div_total[i]) + "\n")
f.write("light7\n")
for i in range(len(light7_bursts_div_total)):
    f.write(str(light7_bursts_div_total[i]) + "\n")
f.write("medium8\n")
for i in range(len(medium8_bursts_div_total)):
    f.write(str(medium8_bursts_div_total[i]) + "\n")
f.write("deep9\n")
for i in range(len(deep9_bursts_div_total)):
    f.write(str(deep9_bursts_div_total[i]) + "\n")
f.write("medium10\n")
for i in range(len(medium10_bursts_div_total)):
    f.write(str(medium10_bursts_div_total[i]) + "\n")
f.write("light11\n")
for i in range(len(light11_bursts_div_total)):
    f.write(str(light11_bursts_div_total[i]) + "\n")
f.close()
plot_means(labels, [deep6_bursts_div_total, light7_bursts_div_total, medium8_bursts_div_total, deep9_bursts_div_total,
                    medium10_bursts_div_total,light11_bursts_div_total],
           'Bursts Mean reported to Full Channel Mean - M016 Classic')

# plot2 --- mean_burts / mean non_bursts
deep6_bursts_div_nonbursts = np.divide(deep6_channels_bursts_means, deep6_channels_nonbursts_means)
light7_bursts_div_nonbursts = np.divide(light7_channels_bursts_means, light7_channels_nonbursts_means)
medium8_bursts_div_nonbursts = np.divide(medium8_channels_bursts_means, medium8_channels_nonbursts_means)
deep9_bursts_div_nonbursts = np.divide(deep9_channels_bursts_means, deep9_channels_nonbursts_means)
medium10_bursts_div_nonbursts = np.divide(medium10_channels_bursts_means, medium10_channels_nonbursts_means)
light11_bursts_div_nonbursts = np.divide(light11_channels_bursts_means, light11_channels_nonbursts_means)
f = open("plot2_m016classic.txt", "w+")
f.write("deep6\n")
for i in range(len(deep6_bursts_div_nonbursts)):
    f.write(str(deep6_bursts_div_nonbursts[i]) + "\n")
f.write("light7\n")
for i in range(len(light7_bursts_div_nonbursts)):
    f.write(str(light7_bursts_div_nonbursts[i]) + "\n")
f.write("medium8\n")
for i in range(len(medium8_bursts_div_nonbursts)):
    f.write(str(medium8_bursts_div_nonbursts[i]) + "\n")
f.write("deep9\n")
for i in range(len(deep9_bursts_div_nonbursts)):
    f.write(str(deep9_bursts_div_nonbursts[i]) + "\n")
f.write("medium10\n")
for i in range(len(medium10_bursts_div_nonbursts)):
    f.write(str(medium10_bursts_div_nonbursts[i]) + "\n")
f.write("light11\n")
for i in range(len(light11_bursts_div_nonbursts)):
    f.write(str(light11_bursts_div_nonbursts[i]) + "\n")
f.close()
plot_means(labels, [deep6_bursts_div_nonbursts, light7_bursts_div_nonbursts, medium8_bursts_div_nonbursts,
                    deep9_bursts_div_nonbursts, medium10_bursts_div_nonbursts,light11_bursts_div_nonbursts],
           'Bursts Mean reported to Non-Bursts Mean - M016 Classic')

for ch_nr in range(len(all_channels)):
    print('Channel ' + str(all_channels[ch_nr]) + ' deep6 ' + str(
        get_channel_maximum_burst(doas, 'deep6', all_channels[ch_nr])))
    print('Channel ' + str(all_channels[ch_nr]) + ' light7 ' + str(
        get_channel_maximum_burst(doas, 'light7', all_channels[ch_nr])))
    print('Channel ' + str(all_channels[ch_nr]) + ' medium8 ' + str(
        get_channel_maximum_burst(doas, 'medium8', all_channels[ch_nr])))
    print('Channel ' + str(all_channels[ch_nr]) + ' deep9 ' + str(
        get_channel_maximum_burst(doas, 'deep9', all_channels[ch_nr])))
    print('Channel ' + str(all_channels[ch_nr]) + ' medium10 ' + str(
        get_channel_maximum_burst(doas, 'medium10', all_channels[ch_nr])))
    print('Channel ' + str(all_channels[ch_nr]) + ' light11 ' + str(
        get_channel_maximum_burst(doas, 'light11', all_channels[ch_nr])))
