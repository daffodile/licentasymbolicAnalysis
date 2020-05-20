import os

from sklearn.ensemble import VotingClassifier
from sklearn.metrics import classification_report
from sklearn.svm import SVC

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import obtain_A_features_from_doa, train_test_doa_remake_balanced

all_channels = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 23, 24, 25, 26, 27, 28, 29, 30,
                31, 32]

encoding = Encoding('./../../../data_to_be_saved/alphabet_3.txt')
data_dir = os.path.join('../..', '..')
levels = ['deep2', 'light4']
initialization = InitDataSet(current_directory=data_dir, subject_directory="m014", filtering_directory="classic",
                             levels=levels)
doas = initialization.get_dataset_as_doas()

doas_train, doas_test, ind_test = train_test_doa_remake_balanced(doas)
X_train, y_train = obtain_A_features_from_doa(doas_train, 6, encoding)
x_test, y_test = obtain_A_features_from_doa(doas_test, 6, encoding)

classifiers_no = 10

estimators = []
for index in range(classifiers_no):
    estimators.append((f'SVM{index}', SVC(gamma='auto')))

ensemble = VotingClassifier(estimators=estimators,
                            voting='soft').fit(X_train, y_train)

print('The accuracy for VotingClassifier is: ')
predictions = ensemble.predict(x_test)

report = classification_report(y_test, predictions, output_dict=True)
print(report)
