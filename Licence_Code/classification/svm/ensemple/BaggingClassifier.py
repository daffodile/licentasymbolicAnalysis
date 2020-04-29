import os

from sklearn.ensemble import BaggingClassifier
from sklearn.metrics import classification_report
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
doas_train, doas_test, ind_test = train_test_doa_remake_balanced(doas)
X_train, y_train = obtain_A_features_from_doa(doas_train, 2, encoding)
x_test, y_test = obtain_A_features_from_doa(doas_test, 2, encoding)


bagging_classifier = BaggingClassifier(base_estimator=SVC(gamma='auto'),
                                       n_estimators=16, random_state=0).fit(X_train, y_train)

for channel in all_channels:
    X_train, y_train = obtain_A_features_from_doa(doas_train, channel, encoding)

    svm_model = SVC()

predictions = bagging_classifier.predict(x_test)

report = classification_report(y_test, predictions, output_dict=True)
print(report)

#  69 76 79 80 72 75 79