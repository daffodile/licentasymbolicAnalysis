from input_reader.InitDataSet import InitDataSet
from utils.Utils import get_trial_values_and_outsiders, get_doa_of_level
from utils.mark_bursts.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions
import numpy as np
import plotly.graph_objects as go

initialization = InitDataSet(levels=['deep', 'medium', 'light'])
doas = initialization.get_dataset_as_doas()
# mark_bursts_regions(doas)

all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
                31, 32]

labels = ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17',
          'C18', 'C19', 'C20', 'C21', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30',
          'C31', 'C32']


def get_channel_nonbursts_mean(doas, doa_level, channel_number):
    doa = get_doa_of_level(doas, doa_level)
    all_bursts = []
    for trial_number in range(240):
        trial_values, trial_values_outsiders = get_trial_values_and_outsiders(doa,
                                                                              channel_number,
                                                                              trial_number + 1)
        trial_nonbursts = []
        for i in range(len(trial_values_outsiders)):
            if (trial_values_outsiders[i] != 1):
                trial_nonbursts.append(trial_values[i])
        all_bursts.extend(trial_nonbursts)

    return np.mean(np.abs(all_bursts))


def get_channel_bursts_mean(doas, doa_level, channel_number):
    doa = get_doa_of_level(doas, doa_level)
    all_bursts = []
    for trial_number in range(240):
        trial_values, trial_values_outsiders = get_trial_values_and_outsiders(doa,
                                                                              channel_number,
                                                                              trial_number + 1)
        trial_bursts = []
        for i in range(len(trial_values_outsiders)):
            if (trial_values_outsiders[i] == 1):
                trial_bursts.append(trial_values[i])
        all_bursts.extend(trial_bursts)

    return np.mean(np.abs(all_bursts))


def get_channel_mean(doas, doa_level, channel_number):
    doa = get_doa_of_level(doas, doa_level)
    channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
    all_trials = []
    for trial in channel.trials:
        all_trials.extend(trial.spontaneous.values)
        all_trials.extend(trial.stimulus.values)
        all_trials.extend(trial.poststimulus.values)

    return np.mean(np.abs(all_trials))


def get_doa_means_statistics(doas, doa_level, all_channels):
    channels_means = []
    channels_bursts_means = []
    channels_nonbursts_means = []

    for ch_nr in range(len(all_channels)):
        channels_means.append(get_channel_mean(doas, doa_level, all_channels[ch_nr]))
        channels_bursts_means.append(get_channel_bursts_mean(doas, doa_level, all_channels[ch_nr]))
        channels_nonbursts_means.append(get_channel_nonbursts_mean(doas, doa_level, all_channels[ch_nr]))

    return channels_means, channels_bursts_means, channels_nonbursts_means


def get_channel_maximum_burst(doas, doa_level, channel_number):
    doa = get_doa_of_level(doas, doa_level)
    channel_max_bursts_amplitudes = []
    for trial_number in range(240):
        trial_values, trial_values_outsiders = get_trial_values_and_outsiders(doa,
                                                                              channel_number,
                                                                              trial_number + 1)
        trial_bursts_amplitudes = []
        for i in range(len(trial_values_outsiders)):
            if (trial_values_outsiders[i] == 1):
                trial_bursts_amplitudes.append(trial_values[i])
        channel_max_bursts_amplitudes.extend(trial_bursts_amplitudes)
    return max(channel_max_bursts_amplitudes)


# for ch_nr in range(len(all_channels)):
#     print('Channel ' + str(all_channels[ch_nr]) + ' deep ' + str(
#         get_channel_maximum_burst(doas, 'deep', all_channels[ch_nr])))
#     print('Channel ' + str(all_channels[ch_nr]) + ' medium ' + str(
#         get_channel_maximum_burst(doas, 'medium', all_channels[ch_nr])))
#     print('Channel ' + str(all_channels[ch_nr]) + ' light ' + str(
#         get_channel_maximum_burst(doas, 'light', all_channels[ch_nr])))

def format_values(initial_array):
    formatted = []
    for i in range(len(initial_array)):
        formatted.append(float("{:.2f}".format(initial_array[i])))
    return formatted


def plot_means(labels, arrays, title):
    fig = go.Figure()
    colors = ['indianred', 'lightsalmon', 'lightpink']
    doa_levels = ['deep', 'medium', 'light']
    for i in range(len(arrays)):
        fig.add_trace(go.Bar(
            x=labels,
            y=format_values(arrays[i]),
            text=format_values(arrays[i]),
            textposition='inside',
            name=doa_levels[i],
            marker_color=colors[i]
        ))

    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(
        title=title,
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Mean Report',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.3,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.25,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1  # gap between bars of the same location coordinate.
    )
    fig.show()


deep_channels_means, deep_channels_bursts_means, deep_channels_nonbursts_means = get_doa_means_statistics(doas,
                                                                                                          'deep',
                                                                                                          all_channels)
medium_channels_means, medium_channels_bursts_means, medium_channels_nonbursts_means = get_doa_means_statistics(doas,
                                                                                                                'medium',
                                                                                                                all_channels)
light_channels_means, light_channels_bursts_means, light_channels_nonbursts_means = get_doa_means_statistics(doas,
                                                                                                             'light',
                                                                                                             all_channels)

# plot1 --- mean_burts / mean_total
deep_bursts_div_total = np.divide(deep_channels_bursts_means, deep_channels_means)
medium_bursts_div_total = np.divide(medium_channels_bursts_means, medium_channels_means)
light_bursts_div_total = np.divide(light_channels_bursts_means, light_channels_means)
f = open("plot1.txt", "w+")
f.write("deep\n")
for i in range(len(deep_bursts_div_total)):
    f.write(str(deep_bursts_div_total[i]) + "\n")
f.write("medium\n")
for i in range(len(medium_bursts_div_total)):
    f.write(str(medium_bursts_div_total[i]) + "\n")
f.write("light\n")
for i in range(len(light_bursts_div_total)):
    f.write(str(light_bursts_div_total[i]) + "\n")
f.close()
plot_means(labels, [deep_bursts_div_total, medium_bursts_div_total, light_bursts_div_total], 'Bursts Mean reported to Full Channel Mean')

# plot2 --- mean_burts / mean non_bursts
deep_bursts_div_nonbursts = np.divide(deep_channels_bursts_means, deep_channels_nonbursts_means)
medium_bursts_div_nonbursts = np.divide(medium_channels_bursts_means, medium_channels_nonbursts_means)
light_bursts_div_nonbursts = np.divide(light_channels_bursts_means, light_channels_nonbursts_means)
f = open("plot2.txt", "w+")
f.write("deep\n")
for i in range(len(deep_bursts_div_nonbursts)):
    f.write(str(deep_bursts_div_nonbursts[i]) + "\n")
f.write("medium\n")
for i in range(len(medium_bursts_div_nonbursts)):
    f.write(str(medium_bursts_div_nonbursts[i]) + "\n")
f.write("light\n")
for i in range(len(light_bursts_div_nonbursts)):
    f.write(str(light_bursts_div_nonbursts[i]) + "\n")
f.close()
plot_means(labels, [deep_bursts_div_nonbursts, medium_bursts_div_nonbursts, light_bursts_div_nonbursts],
           'Bursts Mean reported to Non-Bursts Mean')
