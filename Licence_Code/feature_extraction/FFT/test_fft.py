import numpy as np

from feature_extraction.FFT.Welch import Welch
from input_reader.InitDataSet import InitDataSet
from utils.TreatBurstingSegmentsInTrials import mark_outsiders

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
# mark_outsiders(doas)


FFT = Welch(doas, [5], ['light'], ['stimulus'], ['all'])
band_fft_max = FFT.get_max_band_power(1)
band_fft_avg = FFT.get_average_band_power(1)


# FFT.get_PSD(137)
# FFT.get_PSD_Welch(137)

for k in band_fft_avg:
    print(k)

# print(band_fft_max)
# print(band_fft_avg)

# array = [[1,2,3,4], [1,2,3,6], [1,3,6,7]]
# print(10*np.log10(np.mean(np.array(array), axis = 0)))