import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

from TESPAR.Coder import Coder

cd = Coder('channel0.txt')
df = pd.DataFrame(cd.test_matrix)

np.random.seed(200)
k = 6
# centroids[i] = [x, y]
centroids = {
    i + 1: [np.random.randint(0, 260), np.random.randint(0, 883)]
    for i in range(k)
}

fig = plt.figure(figsize=(5, 5))
plt.scatter(df.shape[0], df.shape[1], color='k')
colmap = {1: 'r', 2: 'g', 3: 'b',
          4: 'c', 5: 'm', 6: 'y'}
for i in centroids.keys():
    plt.scatter(*centroids[i], color=colmap[i])
plt.xlim(0, 260)
plt.ylim(0, 883)
plt.show()