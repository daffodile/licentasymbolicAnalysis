import csv

import plotly.graph_objects as go


def get_accuracies(filename):
    accuracies = []
    with open(filename) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        ch = 0
        for row in csv_reader:
            if line_count == 0:
                print(filename + ' was processed')
            else:
                accuracies.append(float("{:.2f}".format(float(row[3]))))
            line_count += 1
    return accuracies


def plot_accuracies(labels, arrays, legends, segment, title):
    fig = go.Figure()
    colors = ['indianred', 'lightsalmon', 'lightpink', 'wheat']
    for i in range(len(arrays)):
        fig.add_trace(go.Bar(x=labels,
                             y=arrays[i],
                             text=arrays[i],
                             textposition='inside',
                             name=legends[i],
                             marker_color=colors[i]
                             ))
    fig.update_layout(
        title=title + ' - ' + segment,
        xaxis_tickfont_size=14,
        yaxis=dict(
            title='Accuracies',
            titlefont_size=16,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.3,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.25,  # gap between bars of adjacent location coordinates.
        bargroupgap=0.1  # gap between bars of the same location coordinate.
    )
    fig.show()