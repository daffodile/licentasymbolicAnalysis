import pandas as pd
import csv
import matplotlib.pyplot as plt

import numpy as np
import scipy.stats as stats
import pylab as pl


# data = pd.read_csv(csv_file, dtype={'accuracy': float,
#                                     'acc avr': float,
#                                     'acc std_dev': float,
#                                     'f1-score': float,
#                                     'f1-sc avr': float,
#                                     'f1-sc std_dev': float, },
#                    error_bad_lines=False, na_filter=False, na_values=0)
# # data= pd.read_csv('svm.csv',na_values=['nan'], keep_default_na=False)
#
# data.head(10)
# def plot_distr(arr, mean, std_dev):
#
#     plt.plot(arr.sort())
#     x1 = np.linspace(mean - 3 * std_dev, mean + 3 * std_dev, 100)
#     plt.plot(x1, stats.norm.pdf(x1, mean, std_dev))
#     plt.title(f'Accuracy distr, mean {mean} std_dev {std_dev}')
#     plt.xlabel('Accuracy value')
#     plt.ylabel('Density')
#     plt.show()

def plot_distr(arr, mean, std_dev, title):
    fit = stats.norm.pdf(np.sort(arr), mean, std_dev)  # this is a fitting indeed

    pl.plot(np.sort(arr), fit, '-o')

    pl.hist(np.sort(arr), normed=True, color='grey')  # use this to draw histogram of your data
    pl.title(title + f'Acc mean=' + "{0:.2f}".format(100 * mean) + ' and std_dev=' + "{0:.2f}".format(100 * std_dev))
    pl.xlabel('Accuracy value')
    pl.ylabel('Density')
    plt.savefig(title + '.png')
    pl.show()

file_name = '../../classification/results/svm_report_1_150.csv'

331

with open(file_name) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    acc = []
    # avr = 0
    # std = 0
    ch = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            if line_count > 330:
                # print(f'\t{row[0]}, {row[1]}, {row[2]}, {row[3]} acc is {row[4]}, f1-score is  {row[7]}.')
                if row[0] == '10':
                    print(f'\tavr acc is {row[5]} and std_dev is {row[6]}')
                    # if float(row[5]) > 0.7:
                    print(f'add to plot {row[5]}')
                    plot_distr(acc, float(row[5]), float(row[6]), f'Ch {ch} seg {seg} ')
                    print('debug')
                    acc = []
                else:
                    acc.append(float(row[4]))
                    ch = int(row[1])
                    seg = row[2]
            line_count += 1
    print(f'Processed {line_count} lines.')

# file_name = '../../classification/results/svm_30.csv'
#
# with open(file_name) as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     acc = []
#     avr = 0
#     std = 0
#     ch = 0
#     seg = ''
#     line_count = 0
#     for row in csv_reader:
#         if line_count == 0:
#             print(f'Column names are {", ".join(row)}')
#             line_count += 1
#         else:
#             # print(f'\t{row[0]}, {row[1]}, {row[2]}, {row[3]} acc is {row[4]}, f1-score is  {row[7]}.')
#             if row[0] == '30':
#                 avr = float(row[4])
#             else:
#                 if row[0] == '31':
#                     std = float(row[4])
#                     print(f'\tavr acc is {avr} and {std}')
#                     plot_distr(acc, avr, std, f'Ch {ch} seg {seg} ')
#                     print('debug')
#                     acc = []
#                 else:
#                     acc.append(float(row[4]))
#                     ch = int(row[1])
#                     seg = row[2]
#     line_count += 1
# print(f'Processed {line_count} lines.')
