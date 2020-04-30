import pandas as pd
from scipy import signal
import matplotlib.pyplot as plt
import numpy as np

from feature_extraction.FFT.Welch import Welch, get_average_band_power, get_max_band_power
from input_reader.InitDataSet import InitDataSet
from utils.TreatBurstingSegmentsInTrials import mark_outsiders
from utils.mark_bursts.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions
from utils.mark_bursts.MarkOutsidersWithBurstsFlags import remove_bursted_trials_when_segment

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
mark_bursts_regions(doas)
#
remove_bursted_trials_when_segment(doas)

# delta_avg = 0
# beta_avg = 0
# gamma_lo_avg = 0
# gamma_hi_avg = 0
# theta_avg = 0
# alpha_avg = 0
# fast_avg = 0

delta = []
beta=[]
theta = []
gamma_hi = []
gamma_lo = []
alpha = []
fast = []

FFT = Welch(doas, [10], ['light'], ['stimulus'], ['all'])
FFT_data, data_validate = FFT.get_data()

for i in range(len(FFT_data)):
    # dataset, channels, levels, segment, trial, orientation
    # FFT = Welch(doas, [1], ['deep'], ['stimulus'], [i], ['all'])
    band_fft_avg = get_average_band_power(FFT_data[i], data_validate[i])
    band_fft_max = get_max_band_power(FFT_data[i], data_validate[i])

    # delta_avg = delta_avg + band_fft_max['Delta']
    # beta_avg = beta_avg + band_fft_max['Beta']
    # theta_avg = theta_avg + band_fft_max['Theta']
    # alpha_avg = alpha_avg + band_fft_max['Alpha']
    # gamma_hi_avg = gamma_hi_avg + band_fft_max['GammaHigh']
    # gamma_lo_avg = gamma_lo_avg + band_fft_max['GammaLow']
    # fast_avg = fast_avg + band_fft_max['Fast']
    if band_fft_avg['Delta'] != 0:
        delta.append(band_fft_max['Delta'])
    if band_fft_avg['Theta'] != 0:
        theta.append(band_fft_max['Theta'])
    if band_fft_avg['Beta'] != 0:
        beta.append(band_fft_max['Beta'])
    if band_fft_avg['Alpha'] != 0:
        alpha.append(band_fft_max['Alpha'])
    if band_fft_avg['GammaHigh'] != 0:
        gamma_hi.append(band_fft_max['GammaHigh'])
    if band_fft_avg['GammaLow'] != 0:
        gamma_lo.append(band_fft_max['GammaLow'])
    if band_fft_avg['Fast'] != 0:
        fast.append(band_fft_max['Fast'])


delta_avg = np.mean(delta)
beta_avg = np.mean(beta)
theta_avg = np.mean(theta)
alpha_avg = np.mean(alpha)
gamma_hi_avg = np.mean(gamma_hi)
gamma_lo_avg = np.mean(gamma_lo)
fast_avg = np.mean(fast)

delta_stddev = np.std(delta, axis=0)
theta_stddev = np.std(theta, axis=0)
alpha_stddev = np.std(alpha, axis=0)
beta_stddev = np.std(beta, axis=0)
gamma_lo_stddev = np.std(gamma_lo, axis=0)
gamma_hi_stddev = np.std(gamma_hi, axis=0)
fast_stddev = np.std(fast)

# Define EEG bands
eeg_bands = {'Delta': (1.5, 4),
             'Theta': (4, 8),
             'Alpha': (8, 12),
             'Beta': (12, 30),
             'GammaLow': (30, 50),
             'GammaHigh': (50, 80),
             'Fast': (80, 150)}

band_fft_average_all_trial = dict()
band_fft_stddev_all_trial = dict()
band_fft_average_all_trial['Delta'] = delta_avg
band_fft_average_all_trial['Theta'] = theta_avg
band_fft_average_all_trial['Alpha'] = alpha_avg
band_fft_average_all_trial['Beta'] = beta_avg
band_fft_average_all_trial['GammaLow'] = gamma_lo_avg
band_fft_average_all_trial['GammaHigh'] = gamma_hi_avg
band_fft_average_all_trial['Fast'] = fast_avg

band_fft_stddev_all_trial['Delta'] = delta_stddev
band_fft_stddev_all_trial['Theta'] = theta_stddev
band_fft_stddev_all_trial['Alpha'] = alpha_stddev
band_fft_stddev_all_trial['Beta'] = beta_stddev
band_fft_stddev_all_trial['GammaLow'] = gamma_lo_stddev
band_fft_stddev_all_trial['GammaHigh'] = gamma_lo_stddev
band_fft_stddev_all_trial['Fast'] = fast_stddev

df = pd.DataFrame(columns=['band', 'val'])
df['band'] = eeg_bands.keys()
df['val'] = [band_fft_average_all_trial[band] for band in eeg_bands]
ax = df.plot.bar(x='band', y='val', legend=False, ylim=[0, 10])
ax.set_xlabel("freq band")
ax.set_ylabel("Avg Max band Amplitude")
plt.title("Average - Medium Level Stimulus All Trials from channel 10")
plt.show()
print(band_fft_average_all_trial)

df1 = pd.DataFrame(columns=['band', 'val'])
df1['band'] = eeg_bands.keys()
df1['val'] = [band_fft_stddev_all_trial[band] for band in eeg_bands]
ax = df1.plot.bar(x='band', y='val', legend=False, ylim=[0, 10])
ax.set_xlabel("freq band")
ax.set_ylabel("Std Deviation band Amplitude")
plt.title("Std Deviation- Medium Level Stimulus All Trials from channel 10")
plt.show()
print(band_fft_stddev_all_trial)