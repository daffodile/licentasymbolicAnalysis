# # once per filter hereee
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.svm import SVC

from classification.SplitData import SplitData
from classification.Train_and_Test import TrainTestSplitting
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet

channels_range = 31

segments = ['spontaneous', 'stimulus', 'poststimulus']
initialization = InitDataSet()
doas = initialization.get_dataset_as_doas()
split_data = SplitData(doas, [1, 2, 3, 4, 5], ['light', 'deep'], segments, ['all'])
trainTestSplit = TrainTestSplitting(split_data, 'alphabet_3hz', 1)

X_train, X_test, y_train, y_test = trainTestSplit.splitData(0.2)
print("am train test split")

clf1 = DecisionTreeClassifier()
clf2 = RandomForestClassifier()
clf3 = SVC()

eclf1 = VotingClassifier(estimators=[('dt', clf1), ('rf', clf2), ('svm', clf3)], voting='hard')
eclf1 = eclf1.fit(X_train, y_train)
predictions = eclf1.predict(X_test)

score = eclf1.score(X_test, y_test)
print(score)
