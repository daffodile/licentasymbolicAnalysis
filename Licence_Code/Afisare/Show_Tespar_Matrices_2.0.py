import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


class Show_TESPAR_Matrices_2:

    def plot_matrix_S(self, s_matrix, DOA, trial, segment, channel_nr):
        plt.plot(s_matrix, bins=32)
        plt.yscale('log', nonposy='clip')
        plt.title("S Matrix " + DOA + " " + trial + " " + segment + " ch: " + str(channel_nr))
        plt.xlabel("Symbol")
        plt.ylabel("log10(#)")
        plot_name = 'S/channel' + str(channel_nr) + "_" + DOA + "_" + segment + "_S.png"
        plt.savefig(plot_name)
        plt.show()

    def plot_matrix_A(self, a_matrix, DOA, trial, segment, channel_nr, lag):
        ax = sns.heatmap(np.log10([[v + 1 for v in r] for r in a_matrix]), cmap="YlGnBu", vmin=0, vmax=1)
        ax.invert_yaxis()
        plt.xlabel("Symbols lag " + str(lag))
        plt.ylabel("Symbols lag " + str(lag))
        plt.title("A Matrix " + DOA + " " + trial + " " + segment + " ch: " + str(channel_nr))
        plot_name = 'log/channel' + str(channel_nr) + "_" + DOA + "_" + segment + "_lag" + str(lag) + "_A.png"
        plt.savefig(plot_name)
        plt.show()
