import numpy as np

from DataSet.InitDataSet import InitDataSet
from DataSet.Models import DOA


def differences_A(doas, ch_nr, trial_nr):
    doas_array = np.array(doas, dtype=DOA)
    # open the wanted DOAs - DEEP and LIGHT
    doa_deep = np.extract(condition=(lambda x: x.level == "deep"), arr=doas_array)[0]
    doa_light = np.extract(condition=(lambda x: x.level == "light"), arr=doas_array)[0]

    print('ia doas correct')  # hehhe merge


initialization = InitDataSet()

doas = initialization.get_dataset_as_doas()

differences_A(doas, 3, 24)
