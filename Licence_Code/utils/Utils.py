'''

here a function to obtain a float array from a doa

'''


def obtain_floats_from_DOA(doa):
    resulting_floats = []
    for channel in doa.channels:
        for trial in channel.trials:
            resulting_floats.append(trial.spontaneous.values)
            resulting_floats.append(trial.stimulus.values)
            resulting_floats.append(trial.poststimulus.values)

    return resulting_floats
