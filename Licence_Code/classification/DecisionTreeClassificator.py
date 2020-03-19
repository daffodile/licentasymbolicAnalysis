# Load libraries
import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix
from sklearn.tree import DecisionTreeClassifier  # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split  # Import train_test_split function
from sklearn import metrics  # Import scikit-learn metrics module for accuracy calculation


class DecisionTreeClassificator:
    def __init__(self, X_train, X_test, Y_train, Y_test):
        self.X_train = X_train
        self.X_test = X_test
        self.Y_train = Y_train
        self.Y_test = Y_test

    def classify(self):
        # Create Decision Tree classifer object
        clf = DecisionTreeClassifier(criterion='entropy')

        # Train Decision Tree Classifer
        clf = clf.fit(self.X_train, self.Y_train)

        # Predict the response for test dataset
        y_pred = clf.predict(self.X_test)

        confusion = confusion_matrix(self.Y_test, y_pred)
        confusion = confusion / confusion.astype(np.float).sum(axis=1)
        confusion = np.round(confusion, decimals=2)

        score = clf.score(self.X_test, self.Y_test)
        print(score)
        print(confusion)
        # Model Accuracy, how often is the classifier correct?
        print("Accuracy:", metrics.accuracy_score(self.Y_test, y_pred))
