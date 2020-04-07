import numpy as np

'''
    method to get the sum of all A matrix of a channel, segment
'''


def get_A_matrix__segment_channel(doa, encoding, segment, channel_number):
    channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
    a_matrix_all = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
    for trial in channel.trials:
        trial_values = getattr(trial, segment).values
        a_matrix = encoding.get_a(trial_values)
        a_matrix_all = np.add(a_matrix_all, a_matrix)
    return a_matrix_all


def get_doa_of_level(doas, level):
    return list(filter(lambda doa: (doa.level == level), doas))[0]


'''
    get the all the values from all the trials of a particular channel
    in a DOA, in a given segment
'''


def get_channel_segment_values(doa, segment, channel_number):
    channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
    channel_values = []
    for trial in channel.trials:
        channel_values.extend(getattr(trial, segment).values)
    return channel_values


'''
    get the values of a particular trial in a specified channel
    in a DOA, in a given segment
'''


def get_channel_segment_values(doa, segment, channel_number, trial_number):
    channel = list(filter(lambda ch: (ch.number == channel_number), doa.channels))[0]
    trial = list(filter(lambda tr: (tr.trial_number == trial_number), channel.trials))[0]
    return getattr(trial, segment).values


'''

obtain all floats values from a DOA object
'''


def obtain_floats_from_DOA(doa):
    resulting_floats = []
    for channel in doa.channels:
        for trial in channel.trials:
            resulting_floats.append(trial.spontaneous.values)
            resulting_floats.append(trial.stimulus.values)
            resulting_floats.append(trial.poststimulus.values)

    return resulting_floats


#  NOT USED
# method to obtain an array of reports from a classification_report
def classification_report_csv(report):
    report_data = []
    lines = report.split('\n')
    for line in lines[2:-3]:
        row = {}
        row_data = line.split('      ')
        # row_data = line.split(' ')
        # row_data = list(filter(None, row_data))
        row['class'] = row_data[0]
        row['precision'] = float(row_data[1])
        row['recall'] = float(row_data[2])
        row['f1_score'] = float(row_data[3])
        row['support'] = float(row_data[4])
        report_data.append(row)
    dataframe = pd.DataFrame.from_dict(report_data)
    dataframe.to_csv('classification_report.csv', index=False)
