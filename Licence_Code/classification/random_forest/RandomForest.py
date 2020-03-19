import numpy as np
from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from classification.SplitData import SplitData
from classification.random_forest.TrainTest import TrainTestSplitting
from feature_extraction.TESPAR.Encoding import Encoding

test_percentage = 0.2
class RandomForest:

    def __init__(self, filter, lag,  doas, channels, levels, segment, orientation):
        #dataset
        self.doas = doas
        #features alphabet
        self.lag = lag
        self.alphabet_path = 'alphabet_' + str(filter)
        #features
        self.channels = channels
        self.levels = levels
        self.segment = segment
        self.orientation = orientation


        #functie care imi ia doar datele selectate based on features
        split_data = SplitData(self.doas, channels, levels, segment, orientation)

        #cu rezultatul de la functie fac splitul in train si test
        trainTestSplit = TrainTestSplitting(split_data)
        self.train_X, self.test_X, self.train_Y, self.test_Y = trainTestSplit.splitData(0.2)

        #get encoder
        self.en = Encoding('./../data_to_be_saved/' + self.alphabet_path + '.txt')

        #functie care antreneaza
        self.train()


    def train(self):
        #encode the data
        train_encoded_X = []
        test_encoded_X = []
        for i in self.test_X:
            test_encoded_X.append(np.asarray(self.en.get_a(i, self.lag)).ravel())

        for i in self.train_X:
            train_encoded_X.append(np.asarray(self.en.get_a(i, self.lag)).ravel())

        # Create a Gaussian Classifier
        clf = RandomForestClassifier(n_estimators=100)

        # Train the model using the training sets y_pred=clf.predict(X_test)
        clf.fit(train_encoded_X, self.train_Y)

        y_pred = clf.predict(test_encoded_X)

        # Model Accuracy, how often is the classifier correct?
        print("Accuracy:", metrics.accuracy_score(self.test_Y, y_pred))