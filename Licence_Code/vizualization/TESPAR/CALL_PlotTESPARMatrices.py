import os

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from vizualization.TESPAR.PlotTESPARMatrices import get_channel_matrix_A

current_dir = os.path.join('..', '..')

levels = ['deep2', 'medium3', 'light4']

# def __init__(self, current_directory, subject_directory, filtering_directory, levels=['deep', 'medium', 'light'], trials_to_skip=None):
initialization = InitDataSet(current_directory=current_dir, subject_directory="m014", filtering_directory="classic",
                             levels=levels)
doas = initialization.get_dataset_as_doas()

encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')

channels = [2, 6, 20, 29]

for level in levels:
    for channel in channels:
        get_channel_matrix_A(encoding, doas, level, 'stimulus', channel, log=False)
        get_channel_matrix_A(encoding, doas, level, 'stimulus', channel, log=True)
