import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

symbols_matrix = np.loadtxt(fname='../../TESPAR/global_DS_matrix_cutoff1hz.txt', dtype='i')

# print(symbols_matrix)

# plt.matshow(symbols_matrix)
# plt.title("Tespar Clusters assigned ", fontdict=None)
# plt.xlabel("S")
# plt.ylabel("D")
# plt.savefig("./symbols_matrix_others")
# plt.show()

ax = sns.heatmap(symbols_matrix)
plt.title("Tespar Clusters assigned", fontdict=None)
plt.xlabel("S")
plt.ylabel("D")
plt.savefig("./global_DS_matrix_100_50")
plt.show()
