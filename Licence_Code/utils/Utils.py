def get_doa_of_level(doas, level):
    '''
    :param doas: array of DOA objects
    :param level: str 'deep', 'medium', 'light'
    :return: the DOA having this level
    '''
    return list(filter(lambda doa: (doa.level == level), doas))[0]


def get_all_trials_values_from_doa_by_segment(doas, level, segment, channel_number):
    """

    :param doa: DOA object
    :param segment: str 'spontaneous'. 'stimulus' or 'poststimulus'
    :param channel_number: int value of channel.number we search for
    :return: array of all values in all trials of the given segment in the channel

    example of usage:
    all_trials_values = get_channel_trials_values(doas[0], 'spontaneous', 2)
    a_matrix_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
    for values in all_trials_values:
        a_matrix = encoding.get_a(values)
        a_matrix_all = np.add(a_matrix_all, a_matrix)
    """
    doa = get_doa_of_level(doas, level)
    channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
    channel_trials = []
    for trial in channel.trials:
        channel_trials.append(getattr(trial, segment).values)
    return channel_trials


def get_all_trials_values_from_doa_by_segment_with_bursts_flags(doas, level, segment, channel_number):
    """
    :return: 2 arrays, one containing arrays of all the trials values
                    the second one containing all the arrays of values_outsiders
    """
    doa = get_doa_of_level(doas, level)
    channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
    channel_trials = []
    channel_outsiders_trials = []
    for trial in channel.trials:
        channel_trials.append(getattr(trial, segment).values)
        channel_outsiders_trials.append(getattr(trial, segment).values_outsiders)
    return channel_trials, channel_outsiders_trials


def get_trial_from_doas(doas, level, channel_number, trial_number):
    """
    :return: the particular trial searched in a doa,
    given he channel_number and segment
    """
    doa = get_doa_of_level(doas, level)
    channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
    if list(filter(lambda tr: (tr.trial_number == trial_number), channel.trials)):
        return list(filter(lambda tr: (tr.trial_number == trial_number), channel.trials))[0]
    else:
        print(f'There is no trial no {trial_number}  in channel no [{channel_number} of doa {level}')
        return None

def get_one_trial_segment_values_from_doas_by_channel(doas, level, segment, channel_number, trial_number):
    """
    :return: the values of the particular trial searched in a doa,
    given he channel_number and segment
    """
    doa = get_doa_of_level(doas, level)
    channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
    trial = list(filter(lambda tr: (tr.trial_number == trial_number), channel.trials))[0]
    return getattr(trial, segment).values


def get_one_trial_segment_values_from_doas_by_channel_with_bursts_flags(doas, level, segment, channel_number,
                                                                        trial_number):
    """
    :return: the values of the particular trial searched in a doa,
    given he channel_number and segment
    """
    doa = get_doa_of_level(doas, level)
    channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
    trial = list(filter(lambda tr: (tr.trial_number == trial_number), channel.trials))[0]
    return getattr(trial, segment).values, getattr(trial, segment).values_outsiders


def get_one_trial__all_segments_values_from_doa_by_channel_with_bursts_flags(doas, level, channel_number, trial_number):
    """
    :return: the values and the outsiders of the particular trial searched in a doa,
    given the channel_number and doa level
    """
    doa = get_doa_of_level(doas, level)
    channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
    trial = list(filter(lambda tr: (tr.trial_number == trial_number), channel.trials))[0]
    trial_values = []
    trial_values_outsiders = []
    for segment in ['spontaneous', 'stimulus', 'poststimulus']:
        trial_values.extend(getattr(trial, segment).values)
        trial_values_outsiders.extend(getattr(trial, segment).values_outsiders)

    return trial_values, trial_values_outsiders


def obtain_floats_from_DOA(doa):
    """
    :return: array of all floats values from all trials and segments of a DOA object
    """
    resulting_floats = []
    for channel in doa.channels:
        for trial in channel.trials:
            resulting_floats.append(trial.spontaneous.values)
            resulting_floats.append(trial.stimulus.values)
            resulting_floats.append(trial.poststimulus.values)

    return resulting_floats


def get_channel_index(doa, channel_number):
    """
    :return: the index of the specified channel number
    """
    for i in range(30):
        if doa.channels[i].number == channel_number:
            return i


#  NOT USED
# method to obtain an array of reports from a classification_report
# def classification_report_csv(report):
#     report_data = []
#     lines = report.split('\n')
#     for line in lines[2:-3]:
#         row = {}
#         row_data = line.split('      ')
#         # row_data = line.split(' ')
#         # row_data = list(filter(None, row_data))
#         row['class'] = row_data[0]
#         row['precision'] = float(row_data[1])
#         row['recall'] = float(row_data[2])
#         row['f1_score'] = float(row_data[3])
#         row['support'] = float(row_data[4])
#         report_data.append(row)
#     dataframe = pd.DataFrame.from_dict(report_data)
#     dataframe.to_csv('classification_report.csv', index=False)
