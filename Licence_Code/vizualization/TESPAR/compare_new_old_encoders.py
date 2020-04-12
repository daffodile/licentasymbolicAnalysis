"""
    SCRIPT to encode tespar matrix with initial encoder, no bursts treated
    and with renew encoder, treating bursts regions

    test for same channel in both cases, meaning same DOA and segment from the trial too

    * last lines call the method
"""
from feature_extraction.TESPAR.Encoding import Encoding
from feature_extraction.TESPAR.EncodingCheckBursts import EncodingCheckBursts
import numpy as np

from input_reader.InitDataSetWithBurstsFlags import InitDataSetWithBurstsFlags
from utils.Utils import get_all_trials_values_from_doa_by_segment, \
    get_all_trials_values_from_doa_by_segment_with_bursts_flags
from vizualization.TESPAR.PlotTESPARMatrices import plot_matrix_A


def compare_TESPAR_encodings(doas, level, segment, channel_no):
    # 2 encoders, one that treats bursting and one that does not
    encoding_before = Encoding('./../../data_to_be_saved/alphabet_3.txt')
    encoding = EncodingCheckBursts('./../../data_to_be_saved/alphabet_3.txt')

    all_trials_values = get_all_trials_values_from_doa_by_segment(doas, level=level, segment=segment,
                                                                  channel_number=channel_no)
    a_before = np.zeros((encoding_before.no_symbols, encoding_before.no_symbols), dtype=int)
    for i in range(len(all_trials_values)):
        a_matrix = encoding_before.get_a(all_trials_values[i])
        a_before = np.add(a_before, a_matrix)
    print("a_before:")
    print(a_before)
    a_before = np.log10(a_before + 1)
    plot_matrix_A(DOA=level + '_before', segment=segment, channel_number=channel_no, values=a_before)

    trials_values, outsiders_values = get_all_trials_values_from_doa_by_segment_with_bursts_flags(doas, level=level,
                                                                                                  segment=segment,
                                                                                                  channel_number=channel_no)
    a_now = np.zeros((encoding.no_symbols, encoding.no_symbols), dtype=int)
    for i in range(len(trials_values)):
        a_matrix_ = encoding.get_a(trials_values[i], outsiders_values[i])
        a_now = np.add(a_now, a_matrix_)
    print("a_now:")
    print(a_now)
    a_now = np.log10(a_now + 1)
    plot_matrix_A(DOA=level + '_now', segment=segment, channel_number=channel_no, values=a_now)
    # 2 methods to test matrix equality
    if np.allclose(a_before, a_now):
        print('allclose: Matrix are equal, SAFE')
    else:
        print("allclose: Matrix are different, NOT SAFE")

    if np.array(a_before).all() == np.array(a_now).all():
        print('all() == .all(): Matrix are equal, SAFE')
    else:
        print("all() == .all(): Matrix are different, NOT SAFE")


################ CALL THE ABOVE FUNCTION ##########################

initialization = InitDataSetWithBurstsFlags(levels=['deep', 'light'])
doas = initialization.get_dataset_as_doas()

compare_TESPAR_encodings(doas, 'deep', 'spontaneous', 5)

compare_TESPAR_encodings(doas, 'light', 'spontaneous', 5)

print('debug')
