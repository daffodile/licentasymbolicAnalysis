import matplotlib.pyplot as plt
import pandas as pd

from TESPAR.Coder import Coder

cd = Coder('channel0.txt')

plt.plot(cd.channel_values[0][0])
print(cd.test_matrix)
plt.xlabel("D")
plt.ylabel("S")
plt.title("DS MATRIX")
plt.matshow(cd.test_matrix)
plt.show()
