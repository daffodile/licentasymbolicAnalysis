import matplotlib.pyplot as plt
import pandas as pd

from DataSet.HighPassFilterPreProcessing import HighPassFilterPreProcessing
from TESPAR.Coder import Coder

file_deep_stimulus = 'DataSet/lightFiltered/stimulus'
file_deep_spontaneous = 'DataSet/lightFiltered/spontaneous'
file_deep_post = 'DataSet/lightFiltered/poststimulus'

file_medium_stimulus = 'DataSet/mediumFiltered/stimulus'
file_medium_spontaneous = 'DataSet/mediumFiltered/spontaneous'
file_medium_poststimulus = 'DataSet/mediumFiltered/poststimulus'


file_light_stimulus = 'DataSet/lightFiltered/stimulus'
file_light_spontaneous = 'DataSet/lightFiltered/spontaneous'
file_light_poststimulus = 'DataSet/lightFiltered/poststimulus'

cd = Coder(file_light_stimulus)

total_d = sum(cd.distributionD)
total_s = sum(cd.distributionS)
print(total_d)
print(total_s)

distribution_s = [0] * 210
distribution_d = [0] * 550
for i in range(len(cd.distributionS)):
    distribution_s[i] = cd.distributionS[i]/total_s
for i in range(len(cd.distributionD)):
    distribution_d[i] = cd.distributionD[i]/total_d

print(distribution_s)
print(distribution_d)

# print(cd.test_matrix)
plt.plot(distribution_d)
# print(cd.test_matrix)
# plt.xlabel("D")
# plt.ylabel("S")
# plt.title("DS MATRIX")
# plt.matshow(cd.test_matrix)
plt.show()
