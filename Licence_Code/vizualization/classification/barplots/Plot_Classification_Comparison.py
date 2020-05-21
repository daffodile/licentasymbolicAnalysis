import csv
import numpy as np
import plotly.graph_objects as go


def get_acc_and_std(filename):
    accuracies = []
    std_devs = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        ch = 0
        for row in csv_reader:
            if line_count == 0:
                print(filename + ' was processed')
            else:
                accuracies.append(float("{:.2f}".format(float(row[3]))))
                std_devs.append(float("{:.2f}".format(float(row[4]))))
            line_count += 1
    return accuracies, std_devs


def plot_acc_and_std(labels, acc_arrays, acc_std_devs, legends, segment, title):
    fig = go.Figure()
    colors = ['indianred', 'lightsalmon', 'lightpink']
    for i in range(len(acc_arrays)):
        fig.add_trace(go.Bar(x=labels,
                             y=acc_arrays[i],
                             error_y=dict(type='data', array=acc_std_devs[i]),
                             text=acc_arrays[i],
                             textposition='auto',
                             name=legends[i],
                             marker_color=colors[i]
                             ))
    fig.update_layout(
        title=title + ' - ' + segment,
        xaxis=dict(
            title='Channels',
            tickfont_size=14,
        ),
        yaxis=dict(
            title='Burst Percent',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0.5,
            y=1.3,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.25,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1  # gap between bars of the same location coordinate.
    )
    fig.show()
