import os

from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report
from sklearn.svm import SVC

from feature_extraction.TESPAR.EncodingCheckBursts import EncodingCheckBursts
from input_reader.InitDataSetWithBurstsFlags import InitDataSetWithBurstsFlags
from utils.DataSpliting import train_test_doa_balanced, obtain_A_features_from_doa_with_bursts_frags

print(__doc__)

encoding = EncodingCheckBursts('./../../../data_to_be_saved/alphabet_3.txt')

data_dir = os.path.join('../..', '..')
initialization = InitDataSetWithBurstsFlags(data_dir=data_dir, levels=['deep', 'light'])
doas = initialization.get_dataset_as_doas()

# mark_bursts_regions(doas)
#
# remove_bursted_trials_when_segment(doas)

doas_train, doas_test, ind_test = train_test_doa_balanced(doas)

X_train, y_train = obtain_A_features_from_doa_with_bursts_frags(doas_train, 2, 'stimulus', encoding)
x_test, y_test = obtain_A_features_from_doa_with_bursts_frags(doas_test, 2, 'stimulus', encoding)


# Set the parameters by cross-validation
tuned_parameters = [{'kernel': ['rbf'], 'gamma': [1e-3, 1e-4],
                     'C': [1, 10, 100, 1000]},
                    {'kernel': ['linear'], 'C': [1, 10, 100, 1000]}]

scores = ['precision', 'recall']

for score in scores:
    print("# Tuning hyper-parameters for %s" % score)
    print()

    clf = GridSearchCV(
        SVC(), tuned_parameters, scoring='%s_macro' % score
    )
    clf.fit(X_train, y_train)

    print("Best parameters set found on development set:")
    print()
    print(clf.best_params_)
    print()
    print("Grid scores on development set:")
    print()
    means = clf.cv_results_['mean_test_score']
    stds = clf.cv_results_['std_test_score']
    for mean, std, params in zip(means, stds, clf.cv_results_['params']):
        print("%0.3f (+/-%0.03f) for %r"
              % (mean, std * 2, params))
    print()

    print("Detailed classification report:")
    print()
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    print()
    y_true, y_pred = y_test, clf.predict(x_test)
    print(classification_report(y_true, y_pred))
    print()

# Note the problem is too easy: the hyperparameter plateau is too flat and the
# output model is the same for precision and recall with ties in quality.