import os

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, StratifiedKFold
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier

from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import obtain_features_labels_from_doa

encoding = Encoding('./../../../data_to_be_saved/alphabet_3.txt')

data_dir = os.path.join('../..', '..')

initialization = InitDataSet(data_dir=data_dir, levels=['deep', 'medium', 'light'])
doas = initialization.get_dataset_as_doas()

X_train, y_train = obtain_features_labels_from_doa(doas, 2, 'spontaneous', encoding)

models = []
models.append(("LR", LogisticRegression()))
models.append(("NB", GaussianNB()))
models.append(("RF", RandomForestClassifier()))
models.append(("SVC", SVC(gamma='auto')))
models.append(("Dtree", DecisionTreeClassifier()))
# models.append(("XGB", xgb.XGBClassifier()))
models.append(("KNN", KNeighborsClassifier()))

for name, model in models:
    # kfold = KFold(n_splits=5, random_state=22)
    skf = StratifiedKFold()
    cv_result = cross_val_score(model, X_train, y_train, cv=skf, scoring="accuracy")
    average_res = cv_result.mean()
    print(name, average_res)
