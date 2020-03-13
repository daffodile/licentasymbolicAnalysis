from sklearn.metrics import confusion_matrix, classification_report
from sklearn.svm import SVC

from classification.SplitData import SplitData
from classification.Train_and_Test import TrainTestSplitting
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet

initialization = InitDataSet()

doas = initialization.get_dataset_as_doas()

#           SplitData(self, doas, channels, levels, segment, orientation):
split_data = SplitData(doas, [13], ['light', 'deep'], ['spontaneous'], ['all'])

encoding = Encoding('./../../data_to_be_saved/alphabet_3hz.txt')
trainTestSplit = TrainTestSplitting(split_data, encoding)

X_train, x_test, y_train, y_test = trainTestSplit.splitData(0.2)
print("am train test split")

model = SVC()

model.fit(X_train, y_train)

predictions = model.predict(y_test)

print(confusion_matrix(y_test, predictions))
print('\n')
print(classification_report(y_test, predictions))
