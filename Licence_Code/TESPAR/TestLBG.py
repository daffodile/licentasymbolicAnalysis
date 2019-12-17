from sklearn import datasets
import numpy as np
from TESPAR.Coder import Coder
from TESPAR.LBG import VQ_LGB

cd = Coder('channel0.txt')
# a = np.asmatrix(cd.test_matrix)
# df = pd.DataFrame(a)
mat = []
for i in range (883):
    for j in range(260):
        temp = []
        temp.append(cd.test_matrix[i][j])
        mat.append(temp)
print(mat[261])
# a = np.squeeze(np.asarray(cd.test_matrix)
vq_lg = VQ_LGB(mat, 32, 0.00005, 3000)
vq_lg.run()
outout = vq_lg.get_codebook()

print(outout.size)
vq_lg.print_clusters()

