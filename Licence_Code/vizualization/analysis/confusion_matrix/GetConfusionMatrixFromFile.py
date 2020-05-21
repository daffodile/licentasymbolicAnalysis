import seaborn as sn
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29,
                30, 31, 32]


def get_mean_and_std_dev_confusion_matrices_per_channels(file_name, shape):
    # keep an array of matrices for each channel
    confusion_matrices = {}
    for ch in all_channels:
        confusion_matrices.update({ch: []})

    # read from confion matrix file
    line = None
    with open(file_name, 'r') as f:
        line = f.readline()
        while line:
            values_run = np.fromstring(line, dtype=np.int, sep=' ')
            channel_nr = values_run[1]
            # print(channel_nr)  #works

            line = f.readline()
            conf_m = np.fromstring(line, dtype=np.int, sep=' ')
            conf_m = np.reshape(conf_m, shape)
            # print(conf_m) # works
            confusion_matrices[channel_nr].append(conf_m)
            line = f.readline()

    mean_conf_matrix = []
    std_dev_conf_matrix = []

    for key, value in confusion_matrices.items():
        # print(key)
        # print(value)
        # variable to calc the mean value of the 20 matrices corresponding to this channel
        mean_this_channel = np.mean(value, axis=0, dtype=float)
        # print(mean_this_channel)
        mean_conf_matrix.append(mean_this_channel)
        # variable to calc the std dev of 1 channel
        std_dev_this_channel = np.std(value, axis=0, dtype=float)
        # print(std_dev_this_channel)
        std_dev_conf_matrix.append(std_dev_this_channel)

    return mean_conf_matrix, std_dev_conf_matrix


# how to call function
# m, sd = get_mean_and_std_dev_confusion_matrices_per_channels(file_name)

def get_mean_and_std_dev_confusion_matrix_total(file_name, shape):
    m, sd = get_mean_and_std_dev_confusion_matrices_per_channels(file_name, shape=shape)
    total_mean = np.mean(m, axis=0, dtype=float)
    total_std_dev = np.mean(sd, axis=0, dtype=float)

    return total_mean, total_std_dev


def get_mean_and_std_dev_confusion_matrices_per_channels_from_results_file(file_name, shape, lines_begin,
                                                                           lines_inter_results):
    all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29,
                    30, 31, 32]

    # keep an array of matrices for each channel
    confusion_matrices = {}
    for ch in all_channels:
        confusion_matrices.update({ch: []})

    # read from confion matrix file
    line = None
    with open(file_name, 'r') as f:
        for i in range(lines_begin):
            f.readline()
        line = f.readline()
        while line:
            values_run = line.split()
            channel_nr = int(values_run[4])
            # print(f'channels: {channel_nr}')  #works
            for i in range(lines_inter_results):
                f.readline()
            line = f.readline()
            conf_m = np.fromstring(line, dtype=np.int, sep=' ')
            conf_m = np.reshape(conf_m, shape)
            # print(f'connf_m: {conf_m}')  #works
            confusion_matrices[channel_nr].append(conf_m)
            line = f.readline()

    mean_conf_matrix = []
    std_dev_conf_matrix = []

    for key, value in confusion_matrices.items():
        # print(key)
        # print(value)
        # variable to calc the mean value of the 20 matrices corresponding to this channel
        mean_this_channel = np.mean(value, axis=0, dtype=float)
        # print(mean_this_channel)
        mean_conf_matrix.append(mean_this_channel)
        # variable to calc the std dev of 1 channel
        std_dev_this_channel = np.std(value, axis=0, dtype=float)
        # print(std_dev_this_channel)
        std_dev_conf_matrix.append(std_dev_this_channel)

    return mean_conf_matrix, std_dev_conf_matrix


def get_mean_and_std_dev_confusion_matrix_from_results_file_total(file_name, shape, lines_begin, lines_inter_results):
    m, sd = get_mean_and_std_dev_confusion_matrices_per_channels_from_results_file(file_name, shape, lines_begin,
                                                                                   lines_inter_results)
    total_mean = np.mean(m, axis=0, dtype=float)
    total_std_dev = np.mean(sd, axis=0, dtype=float)

    return total_mean, total_std_dev


def plot_confusion_matrix(confusion_matrix, title, labels=['light1', 'deep2']):
    df_cm = pd.DataFrame(confusion_matrix, index=[i for i in labels],
                         columns=[i for i in labels])
    sn.set(font_scale=1.4)  # for label size
    sn.heatmap(df_cm, cmap='BuGn', annot=True, annot_kws={"size": 16})  # font size
    # set ticklabels rotation
    plt.title('Confusion matrix ' + str(title))
    plt.show()


def plot_confusion_mat_and_std(confusion_matrix, confusion_matrix_std, title, labels=['light1', 'deep2']):
    cm = confusion_matrix
    cm_sum = np.sum(cm, axis=1, keepdims=True)
    cm_std = confusion_matrix_std
    annot = np.empty_like(cm).astype(str)
    nrows, ncols = cm.shape
    for i in range(nrows):
        for j in range(ncols):
            c = cm[i, j]
            p = cm_std[i, j]
            if i == j:
                s = cm_sum[i]
                annot[i, j] = '%.1f\n%d/%d' % (p, c, s)
            elif c == 0:
                annot[i, j] = ''
            else:
                annot[i, j] = '%.1f\n%d' % (p, c)

    cm = pd.DataFrame(confusion_matrix, index=[i for i in labels],
                      columns=[i for i in labels])
    cm.index.name = 'Actual'
    cm.columns.name = 'Predicted'
    fig, ax = plt.subplots(figsize=(10, 10))
    sn.heatmap(cm, annot=annot, fmt='', cmap='BuGn', ax=ax)
    # plt.savefig(filename)
    plt.title('Confusion matrix ' + str(title))
    plt.show()


# how to call function
print('DTC classic ')
svm_classic = 'confusion_matrix_5classes.txt'
m, sd = get_mean_and_std_dev_confusion_matrix_total(svm_classic, (5, 5))
plot_confusion_matrix(m, 'DTC classic', labels=['light1', 'deep2', 'light4', 'medium3', 'medium5'])
plot_confusion_mat_and_std(m, sd, 'DTC classic', labels=['light1', 'deep2', 'light4', 'medium3', 'medium5'])
print(m)
print(sd)
