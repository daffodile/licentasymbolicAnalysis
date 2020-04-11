import numpy as np
import plotly
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
import pandas as pd
import plotly.graph_objs as go

COLOR_LIST_DISTRIBUTION_PLOTS = [
    'blueviolet',
    'coral',
    'forestgreen',
    'red',
    'fuchsia',
    'pink',
    'rosybrown',
]


# generate a distribution based on mean and standard deviation
def generate_distribution(desired_mean, desired_std_dev, num_samples=1000):
    # generate a distribution with (approximately) the desired std
    samples = np.random.normal(loc=0.0, scale=desired_std_dev, size=num_samples)

    # find actual mean
    actual_mean = np.mean(samples)

    # transform it in a zero mean distribution
    zero_mean_samples = samples - (actual_mean)

    # compute the std of the zero mean distribution
    zero_mean_std = np.std(zero_mean_samples)

    # scale the distribution to the actual desired std
    scaled_samples = zero_mean_samples * (desired_std_dev / zero_mean_std)

    # make the distribution have the desired mean
    final_samples = scaled_samples + desired_mean

    return final_samples


def plot_distributions(distr_info, names):
    distributions = []

    for distr in distr_info:
        # for each pair of mean and std_dev, create a distr an add it to collection
        distributions.append(generate_distribution(distr[0], distr[1]))

    distribution_plot = ff.create_distplot(distributions, names, show_hist=False)
    distribution_plot.update_layout(title='Ch 1 spontaneous')
    figure = go.Figure()

    for count in range(len(distributions)):
        figure.add_trace(
            go.Scatter(
                distribution_plot['data'][count],
                name=names[count],
                mode='lines',
                line=dict(
                    color=COLOR_LIST_DISTRIBUTION_PLOTS[count]
                )
            )
        )
        figure.add_trace(
            go.Scatter(
                x=[distr_info[count][0], distr_info[count][0]],
                y=[0, max(distribution_plot['data'][count].y)],
                name=f'Means {names[count]} {distr_info[count][0]}',
                mode='lines',
                line=dict(
                    color=COLOR_LIST_DISTRIBUTION_PLOTS[count]
                )
            )
        )

        figure.add_trace(
            go.Scatter(
                y=[0, 0],
                x=[distr_info[count][0] - distr_info[count][1],
                   distr_info[count][0] + distr_info[count][1]],
                name=f'IQR {names[count]} {distr_info[count][1]}',
                mode='lines',
                line=dict(
                    color=COLOR_LIST_DISTRIBUTION_PLOTS[count]
                )
            )
        )

    figure.show()
