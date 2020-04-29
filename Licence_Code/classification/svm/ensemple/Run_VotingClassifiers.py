import os

from sklearn.ensemble import BaggingClassifier, VotingClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.svm import SVC

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import obtain_A_features_from_doa, train_test_doa_remake_balanced

all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
                31, 32]

encoding = Encoding('./../../../data_to_be_saved/alphabet_3.txt')
data_dir = os.path.join('../..', '..')
initialization = InitDataSet(data_dir=data_dir)
doas = initialization.get_dataset_as_doas()

doas_train, doas_test = train_test_doa_remake_balanced(doas)

estimators = []

for channel in all_channels:

    print(f"############# train of channel {channel}#####################")

    X_train, y_train = obtain_A_features_from_doa(doas_train, channel, encoding)

    svm_model = SVC(gamma=0.0001, C=10.0)

    svm_model.fit(X_train, y_train)

    estimators.append(svm_model)

ensemble = VotingClassifier(estimators=estimators, voting='soft')

for channel in all_channels:
    X_test, y_test = obtain_A_features_from_doa(doas_test, channel, encoding)
    predict = ensemble.predict(X_test)

    report = classification_report(y_test, predict)
    print(f"############# test from channel {channel}#####################")
    print(report)
    print(confusion_matrix(y_test, predict))
