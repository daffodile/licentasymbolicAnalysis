# def __init__(self, doas, channels, levels, segment, orientation=['all']):

#
# '''
#     am laut deja clasele pe care le vreauaici
#
# '''
# # def filter_DOAS(doas):
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import obtain_features_labels_from_doa

encoding = Encoding('./../data_to_be_saved/alphabet_3.txt')

initialization = InitDataSet(levels=['deep'])
doas = initialization.get_dataset_as_doas()

x, y = obtain_features_labels_from_doa(doas, 2, 'stimulus', encoding, )
