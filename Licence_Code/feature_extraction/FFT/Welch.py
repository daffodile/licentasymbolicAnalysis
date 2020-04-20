from asyncio.windows_events import NULL

import matplotlib.pyplot as plt
import numpy as np
from scipy import signal
from scipy.integrate import simps

import pandas as pd
from scipy.signal import detrend

from utils.ExtractData import ExtractData

eeg_bands = {'Delta': (1.5, 4),
                          'Theta': (4, 8),
                          'Alpha': (8, 12),
                          'Beta': (12, 30),
                          'GammaLow': (30, 50),
                          'GammaHigh': (50, 80),
                          'Fast': (80, 150)}

def window_no_burst(trial_validate, array, index, window_size=250):
    # get rid of windows that have 20% values with burst
    nr_burst = 0
    for i in range(len(array)):
        if trial_validate[i + index] == 1:
            nr_burst += 1
    # 20% of 250 samples in window
    threshold_burst = 20 * window_size / 100
    if nr_burst > threshold_burst:
        return False
    return True


def get_PSD(trial, trial_validate):
    # frequency sampling
    fs = 1000
    # ca sa am precizia de frecventa de 4 Hz
    window_size = 250
    window_step = 62
    array = trial
    # parcurg eu semnalul cu o fereastra de 250 si pe daca e ok ii fac fft pe ea, ii iau power-ul si il adaug la medie
    i = 0
    index = 0
    power_spectrum = []

    while index < len(array):
        index = i + 250
        array_window = array[i:index]

        # if window is without burst
        if window_no_burst(trial_validate, array_window, i):
            # calculte power for this window
            nfft = len(array_window)
            array_window = detrend(array_window)
            window = signal.windows.blackman(nfft)
            # window =signal.get_window('blackman', window_size)
            data = window * array_window

            x_fourier = np.fft.rfft(data)
            power = np.abs(x_fourier) ** 2
            # Multiply by 2 (except DC & Nyquist) to calculate one-sided spectrum
            power[1: 126] = power[1: 126] * 2
            # Divide by Fs to calculate spectral  density.
            # scale = 2.0 / nfft * nfft
            power = power / (window_size * window_size)
            if len(power) == 126:
                # freq = np.fft.fftfreq(nfft, 1 / fs)
                power_spectrum.append(power)

        i = i + window_step

    if len(power_spectrum) != 0:
        freq = np.fft.fftfreq(window_size, 1 / fs)
        psd = np.mean(np.array(power_spectrum), axis=0)
        # print("asta e lungimea power" + str(len(power_spectrum)))
        # print(psd)
        # print(np.mean(np.array(power_spectrum), axis=0))
        # print(freq[0:126])
        # plt.plot(freq[0:126], 10 * np.log10(np.mean(np.array(power_spectrum), axis=0)))
        # plt.title('Periodogram Using FFT')
        # plt.xlabel('Frequency (Hz)')
        # plt.ylabel('Power/Frequency (dB/Hz)')
        # plt.xlim(0, np.max(freq[0:126]))
        # plt.show()
        return freq[0:126], psd
    else:
        return [], []


def get_PSD_Welch(trial):
    # frequency sampling
    fs = 1000
    # ca sa am precizia de frecventa de 4 Hz
    window_size = 250
    # overlapping - 75%
    overlap = 187
    # window = signal.get_window('blackman', window_size)
    window = signal.windows.blackman(window_size)

    f, Pxx_den = signal.welch(trial, fs, window=window, nperseg=window_size, noverlap=overlap)
    Pxx_den_dB = 10 * np.log10(Pxx_den)  # Scale to dB

    # print(Pxx_den)
    # print(f)
    # # plot data
    # plt.title(
    #     "spectrum for " + str(self.level) + " " + str(self.segment) + " segment channel " + str(self.channels))
    # # plot PDS
    # plt.plot(f, Pxx_den_dB)
    # plt.xlabel('frequency [Hz]')
    # # plt.ylabel('PSD [V**2/Hz]')
    # plt.ylabel('PSD Db')
    # plt.show()
    return f, Pxx_den


def get_average_band_power(trial, trial_validate):
    f, PSD = get_PSD(trial, trial_validate)
    band_fft_avg = dict()
    # Take the mean of the fft amplitude for each EEG band
    if len(PSD) != 0:
        for band in eeg_bands:
            freq_ix = np.where((f >= eeg_bands[band][0]) &
                               (f <= eeg_bands[band][1]))[0]

            band_fft_avg[band] = np.mean(PSD[freq_ix])
    else:
        for band in eeg_bands:
            band_fft_avg[band] = 0
            # self.band_fft_avg[band] = simps(PSD[freq_ix], dx=4)
    # plot if u want
    # df = pd.DataFrame(columns=['band', 'val'])
    # df['band'] = self.eeg_bands.keys()
    # df['val'] = [self.band_fft_avg[band] for band in self.eeg_bands]
    # ax = df.plot.bar(x='band', y='val', legend=False, ylim=[0, 20])
    # ax.set_xlabel("freq band")
    # ax.set_ylabel("Avg band Amplitude")
    # plt.title("Avg Values of bands for " + str(self.level) + " " + str(self.segment) + " segment, trial " + str(
    #     trial) + ", channel " + str(self.channels))
    # plt.show()
    return band_fft_avg


def get_max_band_power(trial):
    band_fft_max = dict()
    f, PSD = get_PSD(trial)
    if len(PSD) != 0:
        for band in eeg_bands:
            freq_ix = np.where((f >= eeg_bands[band][0]) &
                               (f <= eeg_bands[band][1]))[0]
            band_fft_max[band] = np.ndarray.max(PSD[freq_ix])
    else:
        for band in eeg_bands:
            band_fft_max[band] = 0

    # plot if u want
    # df = pd.DataFrame(columns=['band', 'val'])
    #         # df['band'] = self.eeg_bands.keys()
    #         # df['val'] = [self.band_fft_max[band] for band in self.eeg_bands]
    #         # ax = df.plot.bar(x='band', y='val', legend=False, ylim=[0, 70])
    #         # ax.set_xlabel("freq band")
    #         # ax.set_ylabel("Max band Amplitude")
    #         # plt.title("Max Values of bands for " + str(self.level) + " " + str(self.segment) + " segment, trial " + str(
    #         #     trial) + ", channel " + str(self.channels))
    #         # plt.show()
    return self.band_fft_max


class Welch:

    def __init__(self, doas, channels, level, segment, orientation):
        # dataset
        self.doas = doas
        # features
        self.channels = channels
        # self.trial = trial
        self.level = level
        self.segment = segment
        self.orientation = orientation
        # freg bands
        self.band_fft_avg = dict()
        self.band_fft_max = dict()
        self.eeg_bands = {'Delta': (1.5, 4),
                          'Theta': (4, 8),
                          'Alpha': (8, 12),
                          'Beta': (12, 30),
                          'GammaLow': (30, 50),
                          'GammaHigh': (50, 80),
                          'Fast': (80, 150)}
        # functie care imi ia doar datele selectate based on features
        self.get_data()

    def get_data(self):

        #     initialization = InitDataSet()
        #     doas = initialization.get_dataset_as_doas()

        # dataset, channels, levels, segment, orientation
        # split_data = SplitData(self.doas, self.channels, self.level, self.segment, self.orientation)
        split_data = ExtractData(self.doas, self.channels, self.level, self.segment, self.orientation)
        self.X = []
        self.X_validate = []
        for i in range(len(split_data.result.arrays)):
            for j in range(len(split_data.result.arrays[i].array_data)):
                self.X.append(split_data.result.arrays[i].array_data[j])
            for j in range(len(split_data.result.arrays[i].array_validate)):
                self.X_validate.append(split_data.result.arrays[i].array_validate[j])
