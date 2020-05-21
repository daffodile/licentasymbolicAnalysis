from input_reader.InitDataSet import InitDataSet
from utils.Utils import get_trial_values_and_outsiders, get_doa_of_level
from utils.mark_bursts.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions
import numpy as np
import plotly.graph_objects as go

initialization = InitDataSet(levels=['deep', 'medium', 'light'])
doas = initialization.get_dataset_as_doas()
mark_bursts_regions(doas)

all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
                31, 32]
doa_levels = ['deep', 'medium', 'light']
labels = ['C2', 'C3', 'C4', 'C5', 'C6', 'C7', 'C8', 'C9', 'C10', 'C11', 'C12', 'C13', 'C14', 'C15', 'C16', 'C17',
          'C18', 'C19', 'C20', 'C21', 'C23', 'C24', 'C25', 'C26', 'C27', 'C28', 'C29', 'C30',
          'C31', 'C32']


def get_channel_nonbursts_mean(doas, doa_levels, channel_number):
    all_nonbursts = []
    for level in doa_levels:
        doa = get_doa_of_level(doas, level)
        for trial_number in range(240):
            trial_values, trial_values_outsiders = get_trial_values_and_outsiders(doa,
                                                                                  channel_number,
                                                                                  trial_number + 1)
            trial_nonbursts = []
            for i in range(len(trial_values_outsiders)):
                if (trial_values_outsiders[i] != 1):
                    trial_nonbursts.append(trial_values[i])
            all_nonbursts.extend(trial_nonbursts)

    return np.mean(np.abs(all_nonbursts))


def get_channel_bursts_mean(doas, doa_levels, channel_number):
    all_bursts = []
    for level in doa_levels:
        doa = get_doa_of_level(doas, level)
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


def get_channel_mean(doas, doa_levels, channel_number):
    all_trials = []
    for level in doa_levels:
        doa = get_doa_of_level(doas, level)
        channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
        for trial in channel.trials:
            all_trials.extend(trial.spontaneous.values)
            all_trials.extend(trial.stimulus.values)
            all_trials.extend(trial.poststimulus.values)

    return np.mean(np.abs(all_trials))


def format_values(initial_array):
    formatted = []
    for i in range(len(initial_array)):
        formatted.append(float("{:.2f}".format(initial_array[i])))
    return formatted


def plot_means(labels, values, title):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=labels,
        y=format_values(values),
        text=format_values(values),
        textposition='inside',
        marker_color='indianred'
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


channels_means = []
channels_bursts_means = []
channels_nonbursts_means = []

for ch_nr in range(len(all_channels)):
    channels_means.append(get_channel_mean(doas, doa_levels, all_channels[ch_nr]))
    channels_bursts_means.append(get_channel_bursts_mean(doas, doa_levels, all_channels[ch_nr]))
    channels_nonbursts_means.append(get_channel_nonbursts_mean(doas, doa_levels, all_channels[ch_nr]))

# plot1 --- mean_burts / mean_total
bursts_div_total = np.divide(channels_bursts_means, channels_means)
f = open("channel_total_bursts.txt", "w+")
for i in range(len(bursts_div_total)):
    f.write(str(bursts_div_total[i]) + "\n")
f.close()
# plot_means(labels, bursts_div_total, 'Bursts / All Channel')

# plot2 --- mean_burts / mean non_bursts
bursts_div_nonbursts = np.divide(channels_bursts_means, channels_nonbursts_means)
f = open("channel_total_non_bursts.txt", "w+")
for i in range(len(bursts_div_nonbursts)):
    f.write(str(bursts_div_nonbursts[i]) + "\n")
f.close()
# plot_means(labels, bursts_div_nonbursts, 'Bursts / Non Bursts')
