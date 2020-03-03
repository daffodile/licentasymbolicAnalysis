from Afisare.Show_TESPAR_Matrices import Show_TESPAR_Matrices
from TESPAR.Encoding import Encoding

en = Encoding('./../VQ_REMAKE/symbols_cutoff3_s10_sorted.txt')
stm = Show_TESPAR_Matrices(en)

# channel 27
# DOA, segment, channel_nr, filter_freq - S
# DOA, segment, channel_nr, filter_freq, lag - A
# DOA, segment, channel_nr, trial_nr, filter_freq - symbols
stm.plot_matrix_A("deep", "spontaneous", 27, 3, 1)
stm.plot_matrix_A("deep", "spontaneous", 27, 3, 3)
stm.plot_matrix_A("deep", "spontaneous", 27, 3, 5)

stm.plot_matrix_A("deep", "poststimulus", 27, 3, 1)
stm.plot_matrix_A("deep", "poststimulus", 27, 3, 3)
stm.plot_matrix_A("deep", "poststimulus", 27, 3, 5)

stm.plot_matrix_S("deep", "spontaneous", 27, 3)
stm.plot_matrix_S("deep", "poststimulus", 27, 3)

stm.plot_symbols("deep", "spontaneous", 27, 5, 3)
stm.plot_symbols("deep", "poststimulus", 27, 5, 3)

stm.plot_matrix_A("light", "spontaneous", 27, 3, 1)
stm.plot_matrix_A("light", "spontaneous", 27, 3, 3)
stm.plot_matrix_A("light", "spontaneous", 27, 3, 5)

stm.plot_matrix_A("light", "poststimulus", 27, 3, 1)
stm.plot_matrix_A("light", "poststimulus", 27, 3, 3)
stm.plot_matrix_A("light", "poststimulus", 27, 3, 5)

stm.plot_matrix_S("light", "spontaneous", 27, 3)
stm.plot_matrix_S("light", "poststimulus", 27, 3)

stm.plot_symbols("light", "spontaneous", 27, 5, 3)
stm.plot_symbols("light", "poststimulus", 27, 5, 3)


# channel 29
# DOA, segment, channel_nr, filter_freq, lag - A,S
# DOA, segment, channel_nr, trial_nr, filter_freq, lag - symbols

stm.plot_matrix_A("deep", "spontaneous", 29, 3, 1)
stm.plot_matrix_A("deep", "spontaneous", 29, 3, 3)
stm.plot_matrix_A("deep", "spontaneous", 29, 3, 5)

stm.plot_matrix_A("deep", "poststimulus", 29, 3, 1)
stm.plot_matrix_A("deep", "poststimulus", 29, 3, 3)
stm.plot_matrix_A("deep", "poststimulus", 29, 3, 5)

# stm.plot_matrix_S("deep", "spontaneous", 29, 3)
# stm.plot_matrix_S("deep", "poststimulus", 29, 3)
#
# stm.plot_symbols("deep", "spontaneous", 29, 5, 3)
# stm.plot_symbols("deep", "poststimulus", 29, 5, 3)

stm.plot_matrix_A("light", "spontaneous", 29, 3, 1)
stm.plot_matrix_A("light", "spontaneous", 29, 3, 3)
stm.plot_matrix_A("light", "spontaneous", 29, 3, 5)

stm.plot_matrix_A("light", "poststimulus", 29, 3, 1)
stm.plot_matrix_A("light", "poststimulus", 29, 3, 3)
stm.plot_matrix_A("light", "poststimulus", 29, 3, 5)

# stm.plot_matrix_S("light", "spontaneous", 29, 3)
# stm.plot_matrix_S("light", "poststimulus", 29, 3)
#
# stm.plot_symbols("light", "spontaneous", 29, 5, 3)
# stm.plot_symbols("light", "poststimulus", 29, 5, 3)
