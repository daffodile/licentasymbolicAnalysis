import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split

# try to use train and test splitting on this example
Y = [1, 0, 1, 1, 0, 1, 1, 0, 0, 0]  # 1 is for odds and 0 for evens
X = [[1, 3, 5, 7], [2, 4, 6, 8], [11, 13, 15, 17], [21, 23, 25, 27], [12, 14, 16, 18], [31, 33, 35, 37],
     [41, 43, 45, 47], [22, 24, 26, 28], [32, 34, 36, 38], [42, 44, 46, 48]]

df = pd.DataFrame(X)
y = np.array(Y)

# create training and testing vars
X_train, X_test, y_train, y_test = train_test_split(df, y, test_size=0.2, shuffle=False)
print(X_train)
print(y_train.shape)
print(X_test.shape)
print(y_test.shape)

# next we use X_train and y_train
