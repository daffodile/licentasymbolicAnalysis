import numpy as np

from TESPAR.Encoding import Encoding
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns


class Show_TESPAR_Matrices:

    def __init__(self, encoding):
        self.encoding = encoding

    def plot_matrix_S(self, DOA, segment, channel_nr, filter_freq):

        file_path = './DataSet/cutoff' + str(filter_freq) + 'hz/' + str(DOA) + '/' + str(segment) \
            # + '\channel' + str(channel_nr) + '.txt'
        project_path = os.path.join('', '..')
        file_dir = os.path.join(project_path, file_path, '')
        sys.path.append(project_path)
        file_name = "channel" + str(channel_nr) + ".txt"

        channel_values = []

        with open(os.path.join(file_dir, file_name), 'r') as f:
            line = f.readline()
            while line:
                line = line.replace("[", "")
                line = line.replace("]", "")
                new_array = np.fromstring(line, dtype=np.float, sep=', ')
                channel_values.extend(new_array)
                line = f.readline()

        channel_symbols = self.encoding.get_symbols(channel_values)
        counts, bins = np.histogram(a=channel_symbols, bins=32)
        # print('get_s ' + str(self.encoding.get_s()))
        # print('bins  ' + str(bins[:1]))
        # print('counts  ' + str(counts))

        plt.hist(x=channel_symbols, bins=32)
        plt.yscale('log', nonposy='clip')
        plt.title("S Matrix " + DOA + " " + segment + " ch: " + str(channel_nr))
        plt.xlabel("Symbol")
        plt.ylabel("log10(#)")
        plot_name = 'S/channel' + str(channel_nr) + "_" + DOA + "_" + segment + "_S.png"
        plt.savefig(plot_name)
        plt.show()

    def plot_matrix_A(self, DOA, segment, channel_nr, filter_freq, lag):

        file_path = './DataSet/cutoff' + str(filter_freq) + 'hz/' + str(DOA) + '/' + str(segment) \
            # + '\channel' + str(channel_nr) + '.txt'
        project_path = os.path.join('', '..')
        file_dir = os.path.join(project_path, file_path, '')
        sys.path.append(project_path)
        file_name = "channel" + str(channel_nr) + ".txt"

        channel_values = []

        with open(os.path.join(file_dir, file_name), 'r') as f:
            line = f.readline()
            while line:
                line = line.replace("[", "")
                line = line.replace("]", "")
                new_array = np.fromstring(line, dtype=np.float, sep=', ')
                channel_values.extend(new_array)
                line = f.readline()

        self.encoding.get_symbols(channel_values)
        a_matrix = self.encoding.get_a(lag)
        ax = sns.heatmap(np.log10([[v + 1 for v in r] for r in a_matrix]), cmap="YlGnBu", vmin=0, vmax=1)
        # ax = sns.heatmap(a_matrix, cmap="YlGnBu", vmin=0, vmax=8)
        ax.invert_yaxis()
        plt.xlabel("Symbols lag " + str(lag))
        plt.ylabel("Symbols lag " + str(lag))
        plt.title("A Matrix " + DOA + " " + segment + " ch: " + str(channel_nr))
        plot_name = 'log/channel' + str(channel_nr) + "_" + DOA + "_" + segment + "_lag" + str(lag) + "_A.png"
        plt.savefig(plot_name)
        plt.show()

    def plot_symbols(self, DOA, segment, channel_nr, trial_nr, filter_freq):

        file_path = './DataSet/cutoff' + str(filter_freq) + 'hz/' + str(DOA) + '/' + str(segment) \
            # + '\channel' + str(channel_nr) + '.txt'
        project_path = os.path.join('', '..')
        file_dir = os.path.join(project_path, file_path, '')
        sys.path.append(project_path)
        file_name = "channel" + str(channel_nr) + ".txt"

        channel_values = []

        with open(os.path.join(file_dir, file_name), 'r') as f:
            for i, line in enumerate(f):
                # trial_nr  => line trial_nr+1 form the file
                if i == trial_nr:
                    line = line.replace("[", "")
                    line = line.replace("]", "")
                    new_array = np.fromstring(line, dtype=np.float, sep=', ')
                    channel_values.extend(new_array)

        channel_symbols = self.encoding.get_symbols(channel_values)

        series = np.array(channel_symbols)
        x = np.linspace(0, len(series), len(series))
        plt.plot(x, series, color='blue');

        # plt.plot(channel_symbols)
        plt.title("Trial " + str(trial_nr) + " Symbols " + DOA + " " + segment + " ch: " + str(channel_nr))
        plt.xlabel("Time")
        plt.ylabel("Symbols")
        plot_name = 'symbols/channel' + str(channel_nr) + "_" + DOA + "_" + segment + "_trial" + str(
            trial_nr) + "_symbols" + ".png"
        plt.savefig(plot_name)
        plt.show()


def compare_cannel(self, file_name1, file_name2, ch_number):
    # open first file, read lines
    file1 = open(file_name1)
    lines1 = file1.readlines()
    # open second file, read lines
    file2 = open(file_name2)
    lines2 = file2.readlines()

    symbols1 = self.encoding.symbols_array(lines1[5])
    symbols2 = self.encoding.symbols_array(lines2[5])

# en = Encoding('./../VQ_REMAKE/symbols_cutoff3_s10.txt')
#
# array_27 = []
# array_29 = []
#
# file_deep_stimulus = './DataSet/cutoff1hz/deep/poststimulus'
# project_path = os.path.join('', '..')
# data_dir = os.path.join(project_path, file_deep_stimulus, '')
# sys.path.append(project_path)

# with open(os.path.join(data_dir, "channel27.txt"), 'r') as f:
#     line = f.readline()
#     line = line.replace("[", "")
#     line = line.replace("]", "")
#     array_27 = np.fromstring(line, dtype=np.float, sep=', ')
#
# with open(os.path.join(data_dir, "channel29.txt"), 'r') as f:
#     line = f.readline()
#     line = line.replace("[", "")
#     line = line.replace("]", "")
#     array_29 = np.fromstring(line, dtype=np.float, sep=', ')
#
# symbols27 = en.get_symbols(array_27)
# symbols29 = en.get_symbols(array_29)
#
# series27 = np.array(symbols27)
# x = np.linspace(0, len(series27), len(series27))
# plt.plot(x, series27, color='blue');
#
# series29 = np.array(symbols29)
# x = np.linspace(0, len(series29), len(series27))
# plt.plot(x, series27, color='red');
# plt.ylim(-1, 32)
# plt.legend()
# plt.show()


### S matrix for whole channel:

# channel_values27 = []
#
# with open(os.path.join(data_dir, "channel29.txt"), 'r') as f:
#     line = f.readline()
#     while line:
#         line = line.replace("[", "")
#         line = line.replace("]", "")
#         new_array = np.fromstring(line, dtype=np.float, sep=', ')
#         channel_values27.extend(new_array)
#         line = f.readline()
#
# symbols_channel27 = en.get_symbols(channel_values27)
#
# counts, bins = np.histogram(a=symbols_channel27, bins=32)
# print('get_s ' + str(en.get_s()))
# print('bins  ' + str(bins[:1]))
# print('counts  ' + str(counts))
# #
# # plt.hist(x=symbols_channel27, bins=32)
# # plt.yscale('log', nonposy='clip')
# #
# # # plt.hist(symbols_channel27, bins='auto')
# # plt.title("Tespar S deep/stimulus/channel27", fontdict=None)
# # plt.xlabel("Symbol")
# # plt.ylabel("log10(#)")
# # plt.show()
#
#
# ######################## a matrix ########################
# matrix_a = en.get_a(1)
#
# ax = sns.heatmap(matrix_a, cmap="YlGnBu", vmin=0, vmax=8)
# ax.invert_yaxis()
# plt.xlabel("Symbols lag 1")
# plt.title("A Matrix deep/poststimulus/29")
# plt.ylabel("Symbols")
# plt.show()
#
# file_light_stimulus = './DataSet/cutoff1hz/light/poststimulus'
# project_path = os.path.join('', '..')
# data_dir = os.path.join(project_path, file_light_stimulus, '')
# sys.path.append(project_path)
# file_name = "channel29.txt"
# channel_values27 = []
#
# with open(os.path.join(data_dir, file_name), 'r') as f:
#     line = f.readline()
#     while line:
#         line = line.replace("[", "")
#         line = line.replace("]", "")
#         new_array = np.fromstring(line, dtype=np.float, sep=', ')
#         channel_values27.extend(new_array)
#         line = f.readline()
#
# symbols_channel27 = en.get_symbols(channel_values27)
# matrix_a = en.get_a(1)
# ax = sns.heatmap(matrix_a, cmap="YlGnBu", vmin=0, vmax=8)
# ax.invert_yaxis()
# plt.xlabel("Symbols lag 1")
# plt.title("A Matrix light/poststimulus/29")
# plt.ylabel("Symbols")
# plt.show()
