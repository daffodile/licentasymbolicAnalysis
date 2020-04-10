import csv
from scipy import stats


def compute_zscores(file_name):
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        accuracies = []
        ch = 0
        for row in csv_reader:
            if line_count == 0:
                print(file_name + ' was processed')
            else:
                accuracies.append(float(row[3]))
            line_count += 1
        zscores = []

        spontaneous_zscore = stats.zscore(accuracies[:30])
        zscores.append(spontaneous_zscore)

        stimulus_zscore = stats.zscore(accuracies[30:60])
        zscores.append(stimulus_zscore)

        poststimulus_zscore = stats.zscore(accuracies[60:90])
        zscores.append(poststimulus_zscore)

        return zscores


def convert_to_tuples_array(simple_array):
    tuples_array = []
    for i in range(len(simple_array)):
        tuples_array.append((i + 1, simple_array[i]))
    return tuples_array


def get_good_bad_channels_indexes(avg_array):
    tuples_array = convert_to_tuples_array(avg_array)
    sorted_array = sorted(tuples_array, key=lambda tup: tup[1], reverse=True)
    good_channels = sorted_array[:5]
    bad_channels = sorted_array[-5:][::-1]
    return good_channels, bad_channels


def get_channels_numbers(doas, indexes_array):
    channels_numbers = []
    for i in range(len(indexes_array)):
        channels_numbers.append(doas[0].channels[indexes_array[i][0] - 1].number)
    return channels_numbers


def get_channels(doas, zscores_array):
    """
    :param doas: where to search for the channels numbers
    :param zscores_array: the array with computed zscores
    :return: best 5 and worst 5 channels for the given array
    """
    indexes_good, indexex_bad = get_good_bad_channels_indexes(zscores_array)
    channels_good = get_channels_numbers(doas, indexes_good)
    channels_bad = get_channels_numbers(doas, indexex_bad)
    print("GOOD" + str(channels_good))
    print("BAD" + str(channels_bad))
