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

# method to obtain an array of reports from a classification_report
def classification_report_csv(report):
    report_data = []
    lines = report.split('\n')
    for line in lines[2:-3]:
        row = {}
        row_data = line.split('      ')
        # row_data = line.split(' ')
        # row_data = list(filter(None, row_data))
        row['class'] = row_data[0]
        row['precision'] = float(row_data[1])
        row['recall'] = float(row_data[2])
        row['f1_score'] = float(row_data[3])
        row['support'] = float(row_data[4])
        report_data.append(row)
    dataframe = pd.DataFrame.from_dict(report_data)
    dataframe.to_csv('classification_report.csv', index = False)