from pandas import DataFrame
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.svm import SVC
import xlsxwriter

from classification.SplitData import SplitData
from classification.Train_and_Test import TrainTestSplitting
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet

# # once per filter hereee
channels_range = 31
segments = ['spontaneous', 'stimulus', 'poststimulus']

initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
encoding = Encoding('./../../data_to_be_saved/alphabet_1hz.txt')

# SplitData(self, doas, channels, levels, segment, orientation):
split_data = SplitData(doas, [13], ['light', 'deep'], ['spontaneous'], ['all'])

encoding = Encoding('./../../data_to_be_saved/alphabet_3hz.txt')

for i in range(10):
    row = 0
    trainTestSplit = TrainTestSplitting(split_data, encoding, 1)

    print("run " + str(i))
    X_train, x_test, y_train, y_test = trainTestSplit.splitData(0.2)

    model = SVC()

    model.fit(X_train, y_train)

    predictions = model.predict(x_test)

    print(confusion_matrix(y_test, predictions))
    print('\n')
    report = classification_report(y_test, predictions, output_dict=True)
    df_report = DataFrame(report).transpose()
    df_report.to_excel('svm_report.xlsx', index=False, startrow=row, engine='xlsxwriter')
    row += 5

##################### RUN FOR 1 CHANNEL & WORKS #########################3
# initialization = InitDataSet()
#
# doas = initialization.get_dataset_as_doas()
#
# #           SplitData(self, doas, channels, levels, segment, orientation):
# split_data = SplitData(doas, [13], ['light', 'deep'], ['spontaneous'], ['all'])
#
# encoding = Encoding('./../../data_to_be_saved/alphabet_3hz.txt')
# trainTestSplit = TrainTestSplitting(split_data, encoding)
#
# X_train, x_test, y_train, y_test = trainTestSplit.splitData(0.2)
# print("am train test split")
#
# model = SVC()
#
# model.fit(X_train, y_train)
#
# predictions = model.predict(x_test)
#
# print(confusion_matrix(y_test, predictions))
# print('\n')
# print(classification_report(y_test, predictions))
