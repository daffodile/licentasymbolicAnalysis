import numpy as np
import scipy.signal as signal
import matplotlib.pyplot as plt


class HighPassFilterPreProcessing:

    def __init__(self, array):
        self.finalArray = []
        self.array = array
        self.fileteredArray = []
        self.filter()


    def filter(self):
        order = 5  # order of the filter
        btype = 'highpass'  # type
        f_sampling = 1000.0  # my sampling freq
        nyqvist_freq = f_sampling / 2  # Nyqvist frequency in function of my sampling frequency
        cut_off_Hz = 1.0  # my cutoff frequency in Hz
        cutoff_frequency = cut_off_Hz / nyqvist_freq  # normalized cut_off frequency
        analog = False  # digital filter
        b, a = signal.butter(order, cutoff_frequency, btype, analog)
        w, h = signal.freqs(b, a)
        self.fileteredArray = signal.filtfilt(b, a, self.array)
        for i in range(len(self.fileteredArray)):
            self.finalArray.append(self.fileteredArray[i])

        # plt.plot(self.carrierPhase)
        # plt.plot(self.array)
        # plt.show()
