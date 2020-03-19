from sklearn.metrics import confusion_matrix, classification_report
from sklearn.svm import SVC

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

for segment in segments:
    for channel in range(1, channels_range):
        print(str(channel) + ' ' + segment + '\n')

        # SplitData(self, doas, channels, levels, segment, orientation):
        split_data = SplitData(doas, [channel], ['light', 'deep'], [segment], ['all'])

        # encoding = Encoding('./../../data_to_be_saved/alphabet_3hz.txt')
        trainTestSplit = TrainTestSplitting(split_data, encoding)

        X_train, x_test, y_train, y_test = trainTestSplit.splitData(0.2)
        # print("am train test split")

        model = SVC()

        model.fit(X_train, y_train)

        predictions = model.predict(x_test)

        print(confusion_matrix(y_test, predictions))
        print('\n')
        print(classification_report(y_test, predictions))

        print('debug')

# initialization = InitDataSet()
#
# doas = initialization.get_dataset_as_doas()
#
# #           SplitData(self, doas, channels, levels, segment, orientation):
# split_data = SplitData(doas, [0], ['light', 'deep'], ['spontaneous'], ['all'])
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
