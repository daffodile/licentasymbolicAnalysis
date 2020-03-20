import numpy as np
from pandas import DataFrame
from sklearn.svm import SVC
from sklearn.metrics import classification_report, confusion_matrix

from classification.SplitData import SplitData
from classification.svm.Train_and_Test_TESPAR import splitData
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet

run_nr = 10

initialization = InitDataSet()

doas = initialization.get_dataset_as_doas()

######    SplitData(self, doas, channels, levels, segment, orientation):
split_data = SplitData(doas, [13], ['light', 'deep'], ['spontaneous'], ['all'])
print("data from channel 13, light deep spontaneous")

encoding = Encoding('./../../data_to_be_saved/alphabet_3hz.txt')

column_names = ['channel', 'segment', 'run', 'accuracy', 'f1-score']
df = DataFrame(columns=column_names)
df.to_csv("svm_report.csv", mode='a', header=True)


accuracies = []
f1scores = []

for i in range(run_nr):
    X_train_1, x_test_1, y_train_1, y_test_1 = splitData(split_data, encoding, 0.2)

    model = SVC()

    model.fit(X_train_1, y_train_1)

    predictions = model.predict(x_test_1)
    report = classification_report(y_test_1, predictions, output_dict=True)
    acc = report['accuracy']
    f1sc = report['weighted avg']['f1-score']
    df = df.append({'channel': 13, 'segment': 'spontaneous', 'run': i, 'accuracy': acc, 'f1-score': f1sc},
                   ignore_index=True)
    accuracies.append(acc)
    f1scores.append(f1sc)
df.to_csv("svm_report.csv", mode='a', header=False)
print('count after filling  ' + str(df.count()))
df = df.iloc[0:0]
print('coun after iloc' + str(df.count()))

df = df.append({'channel': '', 'segment': '', 'run': 'mean', 'accuracy': np.mean(np.array(accuracies)),
                'f1-score': np.mean(np.array(f1scores))}, ignore_index=True)
df = df.append({'channel': '', 'segment': '', 'run': 'std_dev', 'accuracy': np.std(np.array(accuracies)),
                'f1-score': np.std(np.array(f1scores))}, ignore_index=True)
df.to_csv("svm_report.csv", mode='a', header=False)
print('coun after means' + str(df.count()))
