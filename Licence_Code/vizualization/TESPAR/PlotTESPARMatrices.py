import os

import matplotlib.pyplot as plt
import numpy as np

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.Utils import get_all_trials_values_from_doa_by_segment_with_bursts_flags, \
    get_one_trial__all_segments_values_from_doa_by_channel_with_bursts_flags, get_doa_of_level, \
    get_one_trial_segment_values_from_doas_by_channel_with_bursts_flags, get_all_trials_values_from_doa_by_segment, \
    get_one_trial__more_segments_values_from_doa_by_channel
from utils.Utils_master import get_channel_trials_segment_values_and_outsiders, get_channel_trials_values_more_seg, \
    get_channel_trials_values_and_outsiders_more_seg


def plot_matrix_S(values, title, plot_name):
    plt.hist(x=values, bins=32)
    plt.yscale('log', nonposy='clip')
    plt.title(title)
    plt.xlabel("Symbol")
    plt.ylabel("log10(#)")
    plt.savefig(plot_name)
    plt.show()


def plot_matrix_A(values, title, plot_name):
    fig = plt.figure(figsize=(30, 25))
    ax = fig.add_subplot()
    cax = ax.matshow(values, cmap=plt.cm.jet)
    cbar = fig.colorbar(cax)
    # if (title[0:3] == 'Log'):
    cbar.mappable.set_clim(vmin = -0.7, vmax=3.7)
    # cbar.mappable.set_clim(0, 500.0)
    cbar.ax.tick_params(labelsize=30)
    ax.tick_params(labelsize=30)
    ax.invert_yaxis()
    ax.xaxis.tick_bottom()
    fig.suptitle(title, fontsize=35, y=0.99,
                 fontweight='bold')
    plt.xlabel("Symbol")
    plt.ylabel("Symbol")
    plt.show()
    fig.savefig(plot_name)


def plot_matrix_A_Difference(values, title, plot_name):
    fig = plt.figure(figsize=(30, 25))
    ax = fig.add_subplot()
    cax = ax.matshow(values, cmap=plt.cm.Spectral_r)
    cbar = fig.colorbar(cax)
    cbar.mappable.set_clim(-200.0, 200.0)
    cbar.ax.tick_params(labelsize=30)
    ax.tick_params(labelsize=30)
    for i in range(32):
        for j in range(32):
            c = int(values[j, i])
            ax.text(i, j, str(c), va='center', ha='center', fontsize=20)
    ax.invert_yaxis()
    ax.xaxis.tick_bottom()
    fig.suptitle(title, fontsize=35, y=0.99,
                 fontweight='bold')
    plt.show()
    fig.savefig(plot_name)

def plot_matrix_A_Difference_float(values, title, plot_name):
    fig = plt.figure(figsize=(30, 25))
    ax = fig.add_subplot()
    cax = ax.matshow(values, cmap=plt.cm.Spectral_r)
    cbar = fig.colorbar(cax)
    # cbar.mappable.set_clim(-200.0, 200.0)
    cbar.ax.tick_params(labelsize=30)
    ax.tick_params(labelsize=30)
    for i in range(32):
        for j in range(32):
            c = f'{values[j, i]:.1f}'
            ax.text(i, j, c, va='center', ha='center', fontsize=20)
    ax.invert_yaxis()
    ax.xaxis.tick_bottom()
    fig.suptitle(title, fontsize=35, y=0.99,
                 fontweight='bold')
    plt.show()
    fig.savefig(plot_name)

def get_channel_matrix_A(encoding, doas, doa_level, segment, channel_number, log):
    channel_trials_values, channel_trials_outliers = get_all_trials_values_from_doa_by_segment_with_bursts_flags(doas,
                                                                                                                 doa_level,
                                                                                                                 segment,
                                                                                                                 channel_number)

    a_matrix_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
    for i in range(len(channel_trials_values)):
        # valabil pt remove bursts
        count_zero = list(channel_trials_outliers[i]).count(0)
        if (count_zero != 0):
            time_scaler = len(channel_trials_outliers[i]) / count_zero
            a_matrix = encoding.get_a(channel_trials_values[i], channel_trials_outliers[i])
            a_matrix = a_matrix * time_scaler
            a_matrix_all = np.add(a_matrix_all, a_matrix)

    if (log == True):
        a_matrix_all = np.log10(a_matrix_all + 1)
        title = 'Log A Matrix '
        plot_name = 'log_ch'
    else:
        title = 'A Matrix '
        plot_name = 'ch'
    title += doa_level + " " + segment + " ch: " + str(channel_number)
    plot_name += str(channel_number) + "_" + doa_level + "_" + segment + "_A.png"
    plot_matrix_A(values=a_matrix_all, title=title, plot_name=plot_name)


def get_channel_matrix_A_encode_no_bursts(encoding, doas, doa_level, segment, channel_number, log):
    # channel_trials_values, channel_trials_outsiders = get_all_trials_values_from_doa_by_segment_with_bursts_flags(doas,
    #                                                                                                               doa_level,
    #                                                                                                               segment,
    #                                                                                                               channel_number)

    channel_trials_values = get_all_trials_values_from_doa_by_segment(doas, doa_level, segment, channel_number)
    a_matrix_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
    for i in range(len(channel_trials_values)):
        a_matrix = encoding.get_a(channel_trials_values[i])
        a_matrix_all = np.add(a_matrix_all, a_matrix)
    if (log == True):
        a_matrix_all = np.log10(a_matrix_all + 1)
        title = 'Log A Matrix '
        plot_name = 'log_ch'
    else:
        title = 'A Matrix '
        plot_name = 'ch'
    title += doa_level + " " + segment + " ch: " + str(channel_number)
    plot_name += str(channel_number) + "_" + doa_level + "_" + segment + "_A.png"
    plot_matrix_A(values=a_matrix_all, title=title, plot_name=plot_name)


def get_channel_matrix_A_emphasize_stim(encoding, doas, doa_level, segment, channel_number, log=True):
    spontaneous_channel_trials_values = get_all_trials_values_from_doa_by_segment(doas, doa_level, 'spontaneous',
                                                                                  channel_number)
    stimulus_channel_trials_values = get_all_trials_values_from_doa_by_segment(doas, doa_level, 'stimulus',
                                                                               channel_number)

    a_matrix_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)

    for i in range(len(spontaneous_channel_trials_values)):
        a_sponaneous = encoding.get_a(spontaneous_channel_trials_values[i])
        a_stimulus = encoding.get_a(stimulus_channel_trials_values[i])
        a_sponaneous = a_sponaneous * len(stimulus_channel_trials_values) / len(
            spontaneous_channel_trials_values)  # normalizare la lungime
        a_stim_resp = a_stimulus - a_sponaneous
        # print(a_stim_resp)

        a_matrix_all = np.add(a_matrix_all, a_stim_resp)
    if (log == True):
        a_matrix_all = np.log10(a_matrix_all + 1)
        title = 'Log A Matrix '
        plot_name = 'log_ch'
    else:
        title = 'A Matrix '
        plot_name = 'ch'
    title += doa_level + " " + segment + " ch: " + str(channel_number) + 'stim-spon'
    plot_name += str(channel_number) + "_" + doa_level + "_" + segment + "_A_stim-spon.png"
    plot_matrix_A(values=a_matrix_all, title=title, plot_name=plot_name)


def get_average_matrix_A_doa(encoding, doas, doa_level, log=True):
    all_matrices_array = []
    doa = get_doa_of_level(doas, doa_level)
    for channel in doa.channels:
        a_matrix_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
        channel_trials_values = get_channel_trials_values_more_seg(doas, doa_level, channel.number)
        for i in range(len(channel_trials_values)):
            a_matrix = encoding.get_a(channel_trials_values[i])
            a_matrix_all = np.add(a_matrix_all, a_matrix)
        all_matrices_array.append(a_matrix_all)

    all_matrices_mean = np.mean(all_matrices_array, axis=0)

    title = f'Average cumulative A matrix on {doa_level}'
    if (log == True):
        all_matrices_mean = np.log10(all_matrices_mean + 1)
        title += ' Log'
        plot_name = 'log_ch'
    else:
        plot_name = 'ch'
    plot_name += "average_A_matrix_" + doa_level + "_full_average_A.png"
    plot_matrix_A(values=all_matrices_mean, title=title, plot_name=plot_name)


def get_average_matrix_A_doa_remove_bursts(encoding, doas, doa_level, log=True):
    all_matrices_array = []
    doa = get_doa_of_level(doas, doa_level)
    for channel in doa.channels:
        a_matrix_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
        channel_trials_values, channel_trials_outliers = get_channel_trials_values_and_outsiders_more_seg(doas,
                                                                                                          doa_level,

                                                                                                          channel.number)
        for i in range(len(channel_trials_values)):
            # valabil pt remove bursts
            count_zero = list(channel_trials_outliers[i]).count(0)
            if (count_zero != 0):
                time_scaler = len(channel_trials_outliers[i]) / count_zero
                a_matrix = encoding.get_a(channel_trials_values[i], channel_trials_outliers[i])
                a_matrix = a_matrix * time_scaler
                a_matrix_all = np.add(a_matrix_all, a_matrix)

        a_matrix_all = np.array(a_matrix_all)
        a_matrix_all = a_matrix_all * 240 / len(channel_trials_values)  # normalizare numar de trials diferit
        all_matrices_array.append(a_matrix_all)  # lista celor 30, medie per canal

    all_matrices_mean = np.mean(all_matrices_array, axis=0)  # mean la cele 30

    title = f'Average cumulative A matrix on {doa_level}'
    plot_name = ''
    if (log == True):
        all_matrices_mean = np.log10(all_matrices_mean + 1)
        title += ' Log'
        plot_name += 'log_'
    plot_name += "average_A_matrix_" + doa_level + ".png"
    plot_matrix_A(values=all_matrices_mean, title=title, plot_name=plot_name)


def get_average_matrix_A_doa_per_trial(encoding, doas, doa_level, log=True):
    all_matrices_array = []
    doa = get_doa_of_level(doas, doa_level)
    for channel in doa.channels:
        a_matrix_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
        channel_trials_values = get_channel_trials_values_more_seg(doas, doa_level, channel.number)
        for i in range(len(channel_trials_values)):
            a_matrix = encoding.get_a(channel_trials_values[i])
            a_matrix_all = np.add(a_matrix_all, a_matrix)
        a_matrix_all = np.array(a_matrix_all)
        a_matrix_all = a_matrix_all / len(channel_trials_values)
        all_matrices_array.append(a_matrix_all)

    all_matrices_mean = np.mean(all_matrices_array, axis=0)

    title = f'Average cumulative A matrix on {doa_level} per trial'
    plot_name = ''
    if (log == True):
        all_matrices_mean = np.log10(all_matrices_mean + 1)
        title += ' Log'
        plot_name += 'log_'
    plot_name += doa_level + "_trial_average_A.png"
    plot_matrix_A(values=all_matrices_mean, title=title, plot_name=plot_name)


def get_average_matrix_A_doa_per_trial_remove_bursts(encoding, doas, doa_level, log=True):
    all_matrices_array = []
    doa = get_doa_of_level(doas, doa_level)
    for channel in doa.channels:
        a_matrix_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
        channel_trials_values, channel_trials_outliers = get_channel_trials_values_and_outsiders_more_seg(doas,
                                                                                                          doa_level,

                                                                                                          channel.number)
        for i in range(len(channel_trials_values)):
            # valabil pt remove bursts
            count_zero = list(channel_trials_outliers[i]).count(0)
            if (count_zero != 0):
                time_scaler = len(channel_trials_outliers[i]) / count_zero
                a_matrix = encoding.get_a(channel_trials_values[i], channel_trials_outliers[i])
                a_matrix = a_matrix * time_scaler
                a_matrix_all = np.add(a_matrix_all, a_matrix)

        # for i in range(len(channel_trials_values)):
        #     a_matrix = encoding.get_a(channel_trials_values[i], channel_trials_outliers[i])
        #     a_matrix_all = np.add(a_matrix_all, a_matrix)

        a_matrix_all = np.array(a_matrix_all)
        a_matrix_all = a_matrix_all / len(channel_trials_values)  # in canalul asta, media per trial
        all_matrices_array.append(a_matrix_all)  # lista celor 30, medie per canal

    all_matrices_mean = np.mean(all_matrices_array, axis=0)

    title = f'Average cumulative A matrix on {doa_level} per trial'
    plot_name = ''
    if (log == True):
        all_matrices_mean = np.log10(all_matrices_mean + 1)
        title += ' Log'
        plot_name += 'log_'
    plot_name += doa_level + "_trial_average_A.png"
    plot_matrix_A(values=all_matrices_mean, title=title, plot_name=plot_name)


def get_channel_trial_matrix_A(encoding, doas, doa_level, channel_number, trial_number, log):
    # channel_trial_values, channel_trial_outsiders = get_one_trial__all_segments_values_from_doa_by_channel_with_bursts_flags(
    #     doas, doa_level, channel_number, trial_number)
    # get_one_trial__more_segments_values_from_doa_by_channel(doas, level, channel_number, trial_number,
    #                                                             segments=['spontaneous', 'stimulus']):

    this_trial_values = get_one_trial__more_segments_values_from_doa_by_channel(doas=doas, level=doa_level,
                                                                                trial_number=trial_number,
                                                                                channel_number=channel_number)
    a_matrix = encoding.get_a(this_trial_values)
    if (log == True):
        a_matrix = np.log10(a_matrix + 1)
        title = 'Log A Matrix '
        plot_name = 'log_ch'
    else:
        title = 'A Matrix '
        plot_name = 'ch'
    title += doa_level + " " + " ch: " + str(channel_number) + " tr: " + str(trial_number)
    plot_name += str(channel_number) + "_tr" + str(trial_number) + "_" + doa_level + "_A.png"
    plot_matrix_A(values=a_matrix, title=title, plot_name=plot_name)


def get_channels_difference_matrix_A(encoding, doas, doa_levels, segment, channels, log):
    # def get_all_trials_values_from_doa_by_segment_with_bursts_flags(doas, level, segment, channel_number):
    channel1_trials_values, channel1_trials_outsiders = get_all_trials_values_from_doa_by_segment_with_bursts_flags(
        doas, doa_levels[0], segment, channels[0])
    channel2_trials_values, channel2_trials_outsiders = get_all_trials_values_from_doa_by_segment_with_bursts_flags(
        doas, doa_levels[1], segment, channels[1])

    a_matrix1_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
    for i in range(len(channel1_trials_values)):
        a_matrix1 = encoding.get_a(channel1_trials_values[i], channel1_trials_outsiders[i])
        a_matrix1_all = np.add(a_matrix1_all, a_matrix1)

    a_matrix2_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
    for i in range(len(channel2_trials_values)):
        a_matrix2 = encoding.get_a(channel2_trials_values[i], channel2_trials_outsiders[i])
        a_matrix2_all = np.add(a_matrix2_all, a_matrix2)

    if (log == True):
        a_matrix1_all = np.log10(a_matrix1_all + 1)
        a_matrix2_all = np.log10(a_matrix2_all + 1)
        title = 'Log A Matrix Diff '
        plot_name = 'log_ch'
    else:
        title = 'A Matrix Diff ' + str(channels[0]) + " "
        plot_name = 'ch'

    diff_matrix = a_matrix1_all - a_matrix2_all

    title += doa_levels[0] + "-" + doa_levels[1]
    doa_levels[1] + " " + segment + " ch: " + str(channels[0]) + "-" + str(channels[1])
    plot_name += str(channels[0]) + "_" + doa_levels[0] + "-" + doa_levels[
        1] + "_" + segment + "_A.png"
    plot_matrix_A_Difference(values=diff_matrix, title=title, plot_name=plot_name)


def get_difference_matrix_A(encoding, doas, doa_levels, segments, log):
    doa1 = get_doa_of_level(doas, doa_levels[0])
    channel_number = len(doa1.channels)

    a_matrices_all = []
    trial_numbers = []

    for ind_doa, doa_level in enumerate(doa_levels):
        doa = get_doa_of_level(doas, doa_levels[ind_doa])
        trials_nr = len(doa.channels[0].trials)
        trial_numbers.append(trials_nr)

        # the variable is a list of al matrices A from a DOA = all channels, all trials
        all_a_matrices = get_a_matrices_full_doa_remove_burst(encoding=encoding, doas=doas, doa_level=doa_level,
                                                              segments=segments)

        a_matrices_sum = np.sum(all_a_matrices, axis=0)
        a_matrices_sum = a_matrices_sum / channel_number
        a_matrices_sum = a_matrices_sum * 240 / trials_nr
        a_matrices_all.append(a_matrices_sum)

    # first the difference bt the conditions
    diff_matrix_all = a_matrices_all[0] - a_matrices_all[1]

    diff_matrix_per_trial = diff_matrix_all / 240

    if (log == True):
        diff_matrix_all = np.sign(diff_matrix_all) * np.log10(abs(diff_matrix_all) + 1)
        diff_matrix_per_trial = np.sign(diff_matrix_per_trial) * np.log10(abs(diff_matrix_per_trial) + 1)
        title_all = 'Log A Matrix Diff '
        title_trial = 'Log A Matrix Diff '
        plot_name_all = 'log_'
        plot_name_trial = 'log_'
    else:
        title_all = 'A Matrix Diff '
        title_trial = 'A Matrix Diff '
        plot_name_all = ''
        plot_name_trial = ''

    title_all += doa_levels[0] + "-" + doa_levels[1]
    title_trial += doa_levels[0] + "-" + doa_levels[1]

    plot_name_all += f'_{doa_levels[0]}-{doa_levels[1]}_A_full.png'
    plot_name_trial += f'_{doa_levels[0]}-{doa_levels[1]}_A_per_trial.png'

    plot_matrix_A_Difference(values=diff_matrix_all, title=title_all, plot_name=plot_name_all)
    plot_matrix_A_Difference_float(values=diff_matrix_per_trial, title=title_trial, plot_name=plot_name_trial)


def get_difference_matrix_A_PER_TRIAL(encoding, doas, doa_levels, segments, log):
    doa1 = get_doa_of_level(doas, doa_levels[0])
    channel_number = len(doa1.channels)

    a_matrices_all = []
    trial_numbers = []

    for ind_doa, doa_level in enumerate(doa_levels):
        doa = get_doa_of_level(doas, doa_levels[ind_doa])
        trials_nr = len(doa.channels[0].trials)
        trial_numbers.append(trials_nr)

        # the variable is a list of al matrices A from a DOA = all channels, all trials
        all_a_matrices = get_a_matrices_full_doa_remove_burst(encoding=encoding, doas=doas, doa_level=doa_level,
                                                              segments=segments)

        a_matrices_sum = np.sum(all_a_matrices, axis=0)
        a_matrices_sum = a_matrices_sum / channel_number
        a_matrices_sum = a_matrices_sum * 240 / trials_nr
        a_matrices_all.append(a_matrices_sum)

    # first the difference bt the conditions
    diff_matrix = a_matrices_all[0] - a_matrices_all[1]

    if (log == True):
        diff_matrix = np.sign(diff_matrix) * np.log10(abs(diff_matrix) + 1)
        title = 'Log A Matrix Diff '
        plot_name = 'log_'
    else:
        title = 'A Matrix Diff '
        plot_name = ''

    title += doa_levels[0] + "-" + doa_levels[1]

    plot_name += f'_{doa_levels[0]}"-"{doa_levels[1]}_A.png'
    plot_matrix_A_Difference(values=diff_matrix, title=title, plot_name=plot_name)


def get_channel_matrix_S(encoding, doas, doa_level, segment, channel_number, log):
    channel_trials_values, channel_trials_outsiders = get_channel_trials_segment_values_and_outsiders(doas, doa_level,
                                                                                                      segment,
                                                                                                      channel_number)
    all_symbols = []
    for i in range(len(channel_trials_values)):
        symbols = encoding.get_symbols(channel_trials_values[i], channel_trials_outsiders[i])
        all_symbols.extend(symbols)
    title = 'S Matrix ' + doa_level + " " + segment + " ch: " + str(channel_number)
    plot_name = 'ch' + str(channel_number) + "" + doa_level + "" + segment + "_S.png"
    plot_matrix_S(values=all_symbols, title=title, plot_name=plot_name)


def get_matrices_S_more_doas(encoding, doas, doa_levels, segments, channels, string_about_channels):
    '''
    from_doas[0] -> 15 arrays, one per channel, in an array are the symbols of that channel

    '''
    from_doas = [[] for i in range(len(doa_levels))]

    for ind_doa, doa_level in enumerate(doa_levels):
        for channel_number in channels:
            this_channel_symbols = []
            channel_trials_values = get_channel_trials_values_more_seg(doas, doa_level, channel_number, segments)
            for i in range(len(channel_trials_values)):
                symbols = encoding.get_symbols(channel_trials_values[i])
                this_channel_symbols.extend(symbols)
            from_doas[ind_doa].append(this_channel_symbols)

    fig_name = f'S_matrices_{doa_levels[0]}_{doa_levels[1]} {string_about_channels}.png'
    plot_matrices_S_2_doas(from_doas=from_doas, doa_levels=doa_levels, fig_name=fig_name,
                           string_about_channels=string_about_channels)

    fig_name = f'S_matrices_{doa_levels[0]}_{doa_levels[1]} {string_about_channels}_bar.png'
    plot_matrices_S_2_doas_same_hist(from_doas=from_doas, doa_levels=doa_levels, fig_name=fig_name,
                                     string_about_channels=string_about_channels)

    fig_name = f's_matrices_{doa_levels[0]}_{doa_levels[1]}_difference'
    # plot_matrices_S_2_doas_difference(from_doas, doa_levels, fig_name, string_about_channels)
    plot_matrices_S_2_doas_difference(from_doas=from_doas, doa_levels=doa_levels, fig_name=fig_name,
                                      string_about_channels=string_about_channels)
    fig_name = f's_matrices_{doa_levels[0]}_{doa_levels[1]}_difference_per_trial'
    plot_matrices_S_2_doas_difference_per_trial(from_doas, doa_levels, fig_name, string_about_channels, nr_trials1=240,
                                                nr_trials2=240)


def get_matrices_S_more_doas_remove_bursts(encoding, doas, doa_levels, segments, string_about_channels):
    '''
    from_doas[0] -> 15 arrays, one per channel, in an array are the symbols of that channel

    '''
    from_doas = []
    nr_trials = []
    doa_curr = get_doa_of_level(doas, doa_levels[0])
    nr_channels = len(doa_curr.channels)

    for ind_doa, doa_level in enumerate(doa_levels):
        all_histograms_doa = get_s_matrices_full_doa_remove_burst(encoding=encoding, doas=doas, doa_level=doa_level,
                                                                  segments=segments)
        print(f'for  {doa_level} the are {len(all_histograms_doa)} trials')
        # print(f'{len(doas[ind_doa].channels[0].trials)} trials in a channel')
        from_doas.append(all_histograms_doa)
        doa_curr = get_doa_of_level(doas, doa_level)
        nr_trials.append(len(doa_curr.channels[0].trials))

    # plot S matrices of the 2 selected DOAS on the same fig, different hists SCALED IN TIME
    fig_name = f'scaled_S_matrices_{doa_levels[0]}_{doa_levels[1]} {string_about_channels}.png'
    plot_matrices_S_2_doas_remove_bursts(from_doas=from_doas, doa_levels=doa_levels, nr_channels=nr_channels,
                                         fig_name=fig_name, string_about_channels=string_about_channels)

    #  plot S matrices of the 2 selected DOAS same bar plot SCALED IN TIME
    # (from_doas, doa_levels, nr_channels, nr_trials, fig_name,  string_about_channels)
    fig_name = f'scaled_S_matrices_{doa_levels[0]}_{doa_levels[1]} {string_about_channels}_bar.png'
    plot_matrices_S_2_doas_same_hist_remove_bursts(from_doas=from_doas, doa_levels=doa_levels, nr_channels=nr_channels,
                                                   nr_trials=nr_trials, fig_name=fig_name,
                                                   string_about_channels=string_about_channels)

    #  plot difference bt S matrices of the 2 selected DOAS one hist ####################################
    fig_name = f'scaled_s_matrices_{doa_levels[0]}_{doa_levels[1]}_difference'
    plot_matrices_S_2_doas_difference_remove_bursts(from_doas=from_doas, doa_levels=doa_levels, fig_name=fig_name,
                                                    nr_channels=nr_channels,
                                                    nr_trials=nr_trials,
                                                    string_about_channels=string_about_channels)
    #
    # (from_doas, doa_levels, fig_name, nr_channels, nr_trials,string_about_channels)
    fig_name = f'scaled_s_matrices_{doa_levels[0]}_{doa_levels[1]}_difference_per_trial'
    plot_matrices_S_2_doas_difference_per_trial_remove_bursts(from_doas=from_doas, doa_levels=doa_levels,
                                                              fig_name=fig_name,
                                                              nr_channels=nr_channels, nr_trials=nr_trials,
                                                              string_about_channels=string_about_channels, log=True)
    plot_matrices_S_2_doas_difference_per_trial_remove_bursts(from_doas=from_doas, doa_levels=doa_levels,
                                                              fig_name=fig_name,
                                                              nr_channels=nr_channels, nr_trials=nr_trials,
                                                              string_about_channels=string_about_channels, log=False)


def plot_matrices_S_2_doas(from_doas, doa_levels, fig_name, string_about_channels):
    array_of_hists = [[] for i in range(len(from_doas))]

    fig, axses = plt.subplots(2)

    for ind_doa, doa_level in enumerate(doa_levels):
        plt.subplot(2, 1, ind_doa + 1)
        n, bins, patches = plt.hist(x=from_doas[ind_doa], bins=32)
        plt.cla()

        means_n = np.mean(n, axis=0)
        print(means_n)

        plt.bar(range(len(means_n)), means_n)
        plt.yscale('log', nonposy='clip')
        plt.title(f'S matrix {doa_levels[ind_doa]} {string_about_channels}')
        plt.xlabel("Symbol")
        plt.ylabel("log10(#)")

    plt.savefig(fig_name)
    plt.show()


def plot_matrices_S_2_doas_remove_bursts(from_doas, doa_levels, nr_channels, fig_name, string_about_channels):
    fig, axses = plt.subplots(2)
    index = np.arange(32)

    for ind_doa, doa_level in enumerate(doa_levels):
        plt.subplot(2, 1, ind_doa + 1)

        all_histograms_doa_mean = np.sum(from_doas[ind_doa], axis=0)  # sum 30*nr_trials hists
        all_histograms_doa_mean = all_histograms_doa_mean / nr_channels

        plt.bar(index, all_histograms_doa_mean)
        axses[ind_doa].grid(zorder=0)

        plt.yscale('log', nonposy='clip')
        plt.ylabel("Count symbol log10(#)")
        plt.title(f'S matrix {doa_levels[ind_doa]} {string_about_channels}')
        plt.xlabel("TESPAR Symbol")

    plt.savefig(fig_name)
    plt.show()


def plot_matrices_S_2_doas_same_hist(from_doas, doa_levels, fig_name, string_about_channels):
    array_of_hists = [[] for i in range(len(from_doas))]
    for ind_doa, doa_level in enumerate(doa_levels):
        for array_of_symbols in from_doas[ind_doa]:
            array_of_hists[ind_doa].extend(array_of_symbols)

    n, bins, patches = plt.hist(x=array_of_hists, bins=32, label=doa_levels)
    plt.cla()

    n_new = np.array(n)
    n_new = n_new / len(from_doas[0])  # divide by 15 the count as it belongs to all channels
    # data to plot
    n_groups = 32

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.30
    opacity = 0.8
    rects1 = plt.bar(index, n_new[0], bar_width, alpha=opacity, color='b', label=doa_levels[0])
    rects2 = plt.bar(index + bar_width, n_new[1], bar_width, alpha=opacity, color='g', label=doa_levels[1])
    ax.grid(zorder=0)

    plt.yscale('log', nonposy='clip')
    plt.xlabel("TESPAR Symbol")
    plt.ylabel(f'Mean number of symbols in {len(from_doas[0])} channels, log10(#)')
    plt.title(f'S matrix {doa_levels[0]} - {doa_levels[1]} {string_about_channels}')
    plt.xticks(index + bar_width, index, fontsize=9)
    plt.legend()

    plt.tight_layout()
    plt.savefig(fig_name)  # arg  fig_name = f'S_matrices_{doa_levels[0]}_{doa_levels[1]}.png'
    plt.show()


def plot_matrices_S_2_doas_same_hist_remove_bursts(from_doas, doa_levels, nr_channels, nr_trials, fig_name,
                                                   string_about_channels):
    all_histograms_doa_means = []
    for ind_doa, doa_level in enumerate(doa_levels):
        all_histograms_doa_mean_this = np.sum(from_doas[ind_doa], axis=0)  # sum 30*nr_trials hists
        all_histograms_doa_mean_this = all_histograms_doa_mean_this / nr_channels  # media pe canale
        all_histograms_doa_mean_this = all_histograms_doa_mean_this * 240 / nr_trials[ind_doa]
        all_histograms_doa_means.append(all_histograms_doa_mean_this)

    n_groups = 32
    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.30
    opacity = 0.8
    rects1 = plt.bar(index, all_histograms_doa_means[0], bar_width, alpha=opacity, color='b', label=doa_levels[0])
    rects2 = plt.bar(index + bar_width, all_histograms_doa_means[1], bar_width, alpha=opacity, color='g',
                     label=doa_levels[1])
    ax.grid(zorder=0)

    plt.yscale('log', nonposy='clip')
    plt.xlabel("TESPAR Symbol")
    plt.ylabel(f'Mean number of symbols in all channels, log10(#)')
    plt.title(f'S matrix {doa_levels[0]} - {doa_levels[1]} {string_about_channels}')
    plt.xticks(index + bar_width, index, fontsize=9)
    plt.legend()

    plt.tight_layout()
    plt.savefig(fig_name)  # arg  fig_name = f'S_matrices_{doa_levels[0]}_{doa_levels[1]}.png'
    plt.show()


def plot_matrices_S_2_doas_difference(from_doas, doa_levels, fig_name, string_about_channels):
    array_of_hists = [[] for i in range(len(from_doas))]
    for ind_doa, doa_level in enumerate(doa_levels):
        for array_of_symbols in from_doas[ind_doa]:
            array_of_hists[ind_doa].extend(array_of_symbols)

    n, bins, patches = plt.hist(x=array_of_hists, bins=32, label=doa_levels)
    plt.cla()

    n_new = np.array(n)
    n_new = n_new / len(from_doas[0])  # divide by nr of channels

    x = n_new[0] - n_new[1]

    t = np.sign(x) * np.log10(abs(x) + 1)
    # data to plot
    n_groups = 32

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    rects1 = plt.bar(index, t, label=f'{doa_levels[0]} - {doa_levels[1]}')
    ax.grid(zorder=0)

    # plt.yscale('log', nonposy='clip')  # log10 on t line
    plt.xlabel("TESPAR Symbol")
    plt.ylabel(f'Mean number of symbols in {len(from_doas[0])} channels , log10(#)')
    plt.title(f'S matrix {doa_levels[0]} - {doa_levels[1]} {string_about_channels}')
    plt.xticks(index, index, fontsize=9)
    plt.legend()
    plt.tight_layout()
    plt.savefig(fig_name)
    plt.show()


def plot_matrices_S_2_doas_difference_remove_bursts(from_doas, doa_levels, nr_channels, nr_trials, fig_name,
                                                    string_about_channels):
    all_histograms_doa_means = []
    for ind_doa, doa_level in enumerate(doa_levels):
        all_histograms_doa_mean_this = np.sum(from_doas[ind_doa], axis=0)  # sum 30*nr_trials hists
        all_histograms_doa_mean_this = all_histograms_doa_mean_this / nr_channels  # media pe canale
        all_histograms_doa_mean_this = all_histograms_doa_mean_this * 240 / nr_trials[ind_doa]
        all_histograms_doa_means.append(all_histograms_doa_mean_this)

    x = all_histograms_doa_means[0] - all_histograms_doa_means[1]

    t = np.sign(x) * np.log10(abs(x) + 1)

    n_groups = 32
    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    rects1 = plt.bar(index, t, color='b', label=f'{doa_levels[0]}-{doa_levels[1]}')
    ax.grid(zorder=0)
    plt.xlabel("TESPAR Symbol")
    plt.ylabel(f'Mean number of symbols in all channels, log10(#)')
    plt.title(f'S matrix {doa_levels[0]} - {doa_levels[1]} {string_about_channels}')
    plt.xticks(index, index, fontsize=9)
    plt.legend()

    plt.tight_layout()
    plt.savefig(fig_name)  # arg  fig_name = f'S_matrices_{doa_levels[0]}_{doa_levels[1]}.png'
    plt.show()


def plot_matrices_S_2_doas_difference_per_trial(from_doas, doa_levels, fig_name, string_about_channels, nr_trials1,
                                                nr_trials2):
    array_of_hists = [[] for i in range(len(from_doas))]
    for ind_doa, doa_level in enumerate(doa_levels):
        for array_of_symbols in from_doas[ind_doa]:
            array_of_hists[ind_doa].extend(array_of_symbols)

    n, bins, patches = plt.hist(x=array_of_hists, bins=32, label=doa_levels)
    plt.cla()

    n_new = np.array(n)
    n_new = n_new / len(from_doas[0])  # divide by NR OF CHANNELS
    # obtine media pe trial
    n_new[0] = n_new[0] / nr_trials1
    n_new[1] = n_new[1] / nr_trials2

    x = n_new[0] - n_new[1]
    # data to plot
    n_groups = 32

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    rects1 = plt.bar(index, x, label=f'{doa_levels[0]} - {doa_levels[1]}')
    ax.grid(zorder=0)

    # plt.yscale('log', nonposy='clip')
    plt.ylim(-30, 12)
    plt.xlabel("TESPAR Symbol")
    plt.ylabel(f'Average # of symbols that differ')
    plt.title(f'S matrix {doa_levels[0]} - {doa_levels[1]} {string_about_channels} per trial')
    plt.xticks(index, index, fontsize=9)
    plt.legend()

    plt.tight_layout()
    plt.savefig(fig_name)  # arg  fig_name = f'S_matrices_{doa_levels[0]}_{doa_levels[1]}.png'
    plt.show()


def plot_matrices_S_2_doas_difference_per_trial_remove_bursts(from_doas, doa_levels, fig_name, nr_channels, nr_trials,
                                                              string_about_channels, log=True):
    all_histograms_doa_means = []
    for ind_doa, doa_level in enumerate(doa_levels):
        all_histograms_doa_mean_this = np.sum(from_doas[ind_doa], axis=0)  # sum 30*nr_trials hists
        all_histograms_doa_mean_this = all_histograms_doa_mean_this / nr_channels  # media pe canale
        all_histograms_doa_mean_this = all_histograms_doa_mean_this / nr_trials[ind_doa]  # media pe trialurile lui
        all_histograms_doa_means.append(all_histograms_doa_mean_this)

    # calculate the difference here
    x = all_histograms_doa_means[0] - all_histograms_doa_means[1]
    if log:
        x = np.sign(x) * np.log10(abs(x) + 1)
        fig_name = 'log_' + fig_name

    n_groups = 32

    # create plot
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    rects1 = plt.bar(index, x, label=f'{doa_levels[0]} - {doa_levels[1]}')
    ax.grid(zorder=0)

    # plt.ylim(-30, 12)
    plt.xlabel("TESPAR Symbol")
    plt.ylabel(f'Average # of symbols that differ')
    plt.title(f'S matrix {doa_levels[0]} - {doa_levels[1]} {string_about_channels} per trial')
    plt.xticks(index, index, fontsize=9)
    plt.legend()

    plt.tight_layout()
    plt.savefig(fig_name)  # arg  fig_name = f'S_matrices_{doa_levels[0]}_{doa_levels[1]}.png'
    plt.show()


# method used to get alla the TESPAR symbolf from a DOA in a single  list, from all channels, all trials
def get_symbols_full_doa(encoding, doas, doa_level, segments=['spontaneous', 'stimulus']):
    all_symbols = []
    doa = get_doa_of_level(doas, doa_level)

    for channel in doa.channels:
        this_channel_symbols = []
        channel_trials_values = get_channel_trials_values_more_seg(doas, doa_level, channel.number, segments)
        for i in range(len(channel_trials_values)):
            symbols = encoding.get_symbols(channel_trials_values[i])
            this_channel_symbols.extend(symbols)
        all_symbols.extend(this_channel_symbols)
    return all_symbols


# method used to get all the TESPAR S MATRICES per trial from a DOA in a single list, from all channels, all trials, skiping bursts
def get_s_matrices_full_doa_remove_burst(encoding, doas, doa_level, segments=['spontaneous', 'stimulus']):
    all_histograms_doa = []
    doa = get_doa_of_level(doas, doa_level)

    for channel in doa.channels:
        # this_channel_symbols = []
        channel_trials_values, channel_trials_outliers = get_channel_trials_values_and_outsiders_more_seg(doas,
                                                                                                          doa_level,
                                                                                                          channel.number,
                                                                                                          segments)
        for i in range(len(channel_trials_values)):
            count_zero = list(channel_trials_outliers[i]).count(0)
            # print(f'{i} {count_zero} outliers: {channel_trials_outliers[i]}')
            if (count_zero != 0):
                time_scaler = len(channel_trials_outliers[i]) / list(channel_trials_outliers[i]).count(0)
                current_s_matrix = np.array(encoding.get_s(channel_trials_values[i], channel_trials_outliers[i]))
                current_s_matrix = current_s_matrix * time_scaler  # pe fiecare TRIAL in parte aici
                all_histograms_doa.append(current_s_matrix)
            else:
                all_histograms_doa.append(np.zeros(encoding.no_symbols))

    return all_histograms_doa


def get_a_matrices_full_doa_remove_burst(encoding, doas, doa_level, segments=['spontaneous', 'stimulus']):
    # all_histograms_doa = []
    all_a_matrices = []

    doa = get_doa_of_level(doas, doa_level)

    for channel in doa.channels:
        # this_channel_symbols = []
        channel_trials_values, channel_trials_outliers = get_channel_trials_values_and_outsiders_more_seg(doas,
                                                                                                          doa_level,
                                                                                                          channel.number,
                                                                                                          segments)
        for i in range(len(channel_trials_values)):
            count_zero = list(channel_trials_outliers[i]).count(0)
            # print(f'{i} {count_zero} outliers: {channel_trials_outliers[i]}')
            if (count_zero != 0):
                time_scaler = len(channel_trials_outliers[i]) / count_zero
                current_a_matrix = encoding.get_a(channel_trials_values[i], channel_trials_outliers[i])
                current_a_matrix = current_a_matrix * time_scaler  # pe fiecare TRIAL in parte aici
                all_a_matrices.append(current_a_matrix)
            else:
                all_a_matrices.append(np.zeros((encoding.no_symbols, encoding.no_symbols)))

    return all_a_matrices


def plot_average_matrix_S(values, doa_level, title, plot_name, nr_channels):
    '''

    :param values: from more channels together
    :param title: title of the plot
    :param plot_name: for saving fig
    :param nr_channels: for averaging
    :return: plots the fig
    '''
    n, bins, patches = plt.hist(x=values, bins=32)
    plt.cla()
    n_new = np.array(n)
    n_new = n_new / nr_channels
    fig, ax = plt.subplots()
    index = np.arange(32)

    plt.bar(index, n_new)
    ax.grid(zorder=0)

    plt.yscale('log', nonposy='clip')
    plt.title(title)
    plt.xlabel("TESPAR Symbol")
    plt.ylabel(f'Mean number of symbols in {doa_level} channels, log10(#)')
    plt.tight_layout()
    plt.savefig(plot_name)
    plt.show()


def plot_average_sum_S_matrix_doa(all_histograms_doa, doa_level, title, plot_name, nr_channels):
    all_histograms_doa_mean = np.sum(all_histograms_doa, axis=0)
    all_histograms_doa_mean = all_histograms_doa_mean / nr_channels
    fig, ax = plt.subplots()
    index = np.arange(32)

    plt.bar(index, all_histograms_doa_mean)
    ax.grid(zorder=0)
    y_label = f'Mean number of symbols in {doa_level} channels'
    plt.yscale('log', nonposy='clip')
    y_label += ', log10(#)'
    plot_name = 'log_' + plot_name
    plt.title(title)
    plt.xlabel("TESPAR Symbol")
    plt.ylabel(y_label)
    plt.tight_layout()
    plt.savefig(plot_name)
    plt.show()


def plot_average_sum_S_matrix_doa_per_trial(all_histograms_doa, doa_level, title, plot_name, log=True):
    all_histograms_doa_mean = np.mean(all_histograms_doa, axis=0)

    fig, ax = plt.subplots()
    index = np.arange(32)

    plt.bar(index, all_histograms_doa_mean)
    ax.grid(zorder=0)
    y_label = f'Mean number of symbols in a trial {doa_level}'
    if log:
        plt.yscale('log', nonposy='clip')
        y_label += ', log10(#)'
        plot_name = 'log_' + plot_name

    plt.title(title)
    plt.xlabel("TESPAR Symbol")
    plt.ylabel(y_label)
    plt.tight_layout()
    plt.savefig(plot_name)
    plt.show()


def plot_average_matrix_S_per_trial(values, doa_level, title, plot_name, nr_channels, nr_trials, log=True):
    '''

    :param values: from more channels together
    :param title: title of the plot
    :param plot_name: for saving fig
    :param nr_channels: for averaging
    :return: plots the fig
    '''
    n, bins, patches = plt.hist(x=values, bins=32)
    plt.cla()
    n_new = np.array(n)
    n_new = n_new / nr_channels
    n_new = n_new / nr_trials
    fig, ax = plt.subplots()
    index = np.arange(32)

    ax.grid(zorder=0)
    plt.bar(index, n_new)
    y_label = f'Mean number of symbols in {doa_level} channels'
    if log:
        plt.yscale('log', nonposy='clip')
        y_label += ', log10(#)'
        plot_name = 'log_' + plot_name
    plt.title(title)
    plt.xlabel("TESPAR Symbol")
    plt.ylabel(y_label)
    plt.tight_layout()
    plt.savefig(plot_name)
    plt.show()
