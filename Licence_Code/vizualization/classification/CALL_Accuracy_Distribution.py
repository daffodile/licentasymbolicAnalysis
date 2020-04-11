from vizualization.classification.Accuracy_distribution import plot_distributions

d_i = [[0.65516, 0.04155], [0.6612, 0.04247], [0.72826, 0.05265]]
n = ['all trials', 'without bad', 'without maybe&bad']

plot_distributions(d_i, n)