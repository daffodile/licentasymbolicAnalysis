import numpy as np

from input_reader.InitDataSet import InitDataSet


def mark_outsiders(doas, liberty=2):
    for doa in doas:
        print('doa {}', doa.level)
        for channel in doa.channels:
            all_trials = np.array([])
            for trial in channel.trials:
                all_trials.extend(trial.spontaneous)
                all_trials.extend(trial.stimulus)
                all_trials.extend(trial.poststimulus)

            channel.mean = np.mean(all_trials)
            channel.std_der = np.std(all_trials)

            print('ch {} mean:{} std_dev {}', channel.number, channel.mean, channel.std_der)

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()

mark_outsiders(doas)

print('debug')
