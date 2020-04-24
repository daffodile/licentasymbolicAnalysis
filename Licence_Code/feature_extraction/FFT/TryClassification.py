from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

from feature_extraction.FFT.FFTFeatures import obtain_TESPAR_A_FFT_features
from feature_extraction.TESPAR.Encoding import Encoding
from input_reader.InitDataSet import InitDataSet
from utils.DataSpliting import train_test_doa_check_trials
from utils.ExtractData import ExtractData
from utils.TreatBurstingSegmentsInTrials import mark_outsiders
from utils.mark_bursts.MarkOutsiderWithBurstFlags_SeparateThresholds import mark_bursts_regions
from utils.mark_bursts.MarkOutsidersWithBurstsFlags import remove_bursted_trials_when_segment
from utils.mark_bursts.MarkOutsidersWithBurstsFlags_OneThreshold import mark_bursts_regions_one_threshold

channel = 2
segment = 'stimulus'


def initData():
    initialization = InitDataSet()
    doas = initialization.get_dataset_as_doas()
    encoding = Encoding('./../../data_to_be_saved/alphabet_3.txt')
    # SAU 1 SAU 2
    #  1 th
    mark_bursts_regions_one_threshold(doas)

    # diff th
    # mark_bursts_regions(doas)

    # remove_bursted_trials_when_segment(doas)


    # doas_train, doas_test, ind_test = train_test_doa(doas, 0.2)
    # sa imi fac propriul test and train
    doas_train, doas_test, ind_test = train_test_doa_check_trials(doas, 0.2)

    train_data = ExtractData(doas_train, [channel], ['light', 'medium', 'deep'], [segment], ['all'])
    test_data = ExtractData(doas_test, [channel], ['light', 'medium', 'deep'], [segment], ['all'])

    # doar fft features
    X_train, y_train = obtain_TESPAR_A_FFT_features(train_data)
    x_test, y_test = obtain_TESPAR_A_FFT_features(test_data)

    return X_train, y_train, x_test, y_test


def test():
    train_features, train_labels, test_features, test_labels = initData()
    clf_important = RandomForestClassifier(n_estimators=5000,max_depth=5, min_samples_split=5,  min_samples_leaf=10)
    clf_important.fit(train_features, train_labels)
    clf_accuracy = evaluate(clf_important, test_features, test_labels)


def evaluate(model, test_features, test_labels):
    predictions = model.predict(test_features)
    report_test = classification_report(test_labels, predictions, output_dict=True)

    acc_test = report_test['accuracy']
    f1sc_test = report_test['weighted avg']['f1-score']

    print("accuracy  " + str(acc_test) + ' test')
    print("f1-score" + str(f1sc_test) + ' test')

test()