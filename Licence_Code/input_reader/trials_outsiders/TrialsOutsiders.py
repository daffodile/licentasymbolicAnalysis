import numpy as np
from scipy.signal import hilbert


def mark_outsiders(doas, liberty=2, use_hilbert_transform=False):
    print("START marking outliners for trials")
    for doa in doas:
        print(f'doa {doa.level}')
        for channel in doa.channels:
            all_trials = []
            for trial in channel.trials:
                all_trials.extend(trial.spontaneous.values)
                all_trials.extend(trial.stimulus.values)
                all_trials.extend(trial.poststimulus.values)

            channel.mean = np.mean(all_trials)
            channel.std_der = np.std(all_trials)
            # print(f'ch {channel.number} mean:{channel.mean} std_dev {channel.std_der}')

            for trial in channel.trials:
                if (use_hilbert_transform):
                    analytic_signal_1 = hilbert(trial.spontaneous.values)
                    values_outsiders = np.where(np.abs(analytic_signal_1) < liberty * channel.std_der, 0, 1)
                    trial.spontaneous.set_values_outsiders(values_outsiders)

                    analytic_signal_2 = hilbert(trial.stimulus.values)
                    values_outsiders = np.where(np.abs(analytic_signal_2) < liberty * channel.std_der, 0, 1)
                    trial.stimulus.set_values_outsiders(values_outsiders)

                    analytic_signal_3 = hilbert(trial.poststimulus.values)
                    values_outsiders = np.where(np.abs(analytic_signal_3) < liberty * channel.std_der, 0, 1)
                    trial.poststimulus.set_values_outsiders(values_outsiders)

                else:
                    values_outsiders = np.where(np.abs(trial.spontaneous.values) < liberty * channel.std_der, 0, 1)
                    trial.spontaneous.set_values_outsiders(values_outsiders)

                    values_outsiders = np.where(np.abs(trial.stimulus.values) < liberty * channel.std_der, 0, 1)
                    trial.stimulus.set_values_outsiders(values_outsiders)

                    values_outsiders = np.where(np.abs(trial.poststimulus.values) < liberty * channel.std_der, 0, 1)
                    trial.poststimulus.set_values_outsiders(values_outsiders)
            # print("debug")
    print("COMPLETED marking outliners for trials")
