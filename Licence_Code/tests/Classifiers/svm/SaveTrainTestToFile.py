import numpy as np

from tests.Classifiers.SplitData import SplitData
from tests.Classifiers.decision_tree.Train_and_Test import TrainTestSplitting
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet

initialization = InitDataSet()

doas = initialization.get_dataset_as_doas()

#           SplitData(self, doas, channels, levels, segment, orientation):
split_data = SplitData(doas, [13], ['light', 'deep'], ['spontaneous'], ['all'])

encoding = Encoding('./../../data_to_be_saved/alphabet_3hz.txt')
trainTestSplit = TrainTestSplitting(split_data, encoding)

test_x_train, test_x_test, test_y_train, test_y_test = trainTestSplit.splitData(0.2)
print("am percents")
# pot salva aici

dir_train = "ch13_spontaneous/train/"
dir_test = "ch13_spontaneous/test/"

for i, x in enumerate(test_x_train):
    f = open(dir_train + str(i) + ".txt", 'w')
    f.write(test_y_train[i] + '\n')
    np.savetxt(f, x, fmt="%s", newline=" ")
    f.close()

for i, x in enumerate(test_x_test):
    f = open(dir_test + str(i) + ".txt", 'w')
    f.write(test_y_test[i] + '\n')
    np.savetxt(f, x, fmt="%s", newline=" ")
    f.close()
