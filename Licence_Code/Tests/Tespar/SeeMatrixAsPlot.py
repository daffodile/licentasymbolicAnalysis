import numpy as np
import matplotlib.pyplot as plt

symbols_matrix = np.loadtxt(fname='../../TESPAR/clusters_light_stim_others.txt', dtype='i')

print(symbols_matrix)

plt.matshow(symbols_matrix)
plt.title("Tespar Clusters assigned ", fontdict=None)
plt.xlabel("S")
plt.ylabel("D")
plt.savefig("./symbols_matrix_others")
plt.show()
